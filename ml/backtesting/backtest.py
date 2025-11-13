# ml/backtesting/backtest.py
"""
ML v1.4 - Backtesting module for MT5_BOT
Assumptions:
- Signals CSV must include Date, Ticker, Signal (BUY/SELL/HOLD), predicted_return_5d
- Entry executed at next day's Open price (or same-day Close if Open not available)
- Exit executed at Close after hold_period days (default 5)
- Position sizing: fixed fraction (default 1.0 meaning full position per trade)
- Supports commission and slippage per trade
Outputs:
- trade_log.csv (one row per trade)
- equity_curve.csv (daily equity)
- performance_report.json (metrics overall and per-ticker)
- comparison files if multiple models' signals are provided
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json

BASE = Path('.')
SIGNALS_DIR = BASE / 'ml' / 'signals'
DATA_DIR = BASE / 'infra' / 'processed'
OUTPUT_DIR = BASE / 'ml' / 'backtesting' / 'output'
LOGS_DIR = BASE / 'Docs' / 'Logs' / 'Backtests'
REPORTS_DIR = BASE / 'Docs' / 'Reports'

for d in [OUTPUT_DIR, LOGS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def load_price_data(ticker):
    # Expects infra/processed/merged_data.csv with Ticker column and Date index
    df = pd.read_csv(DATA_DIR / 'merged_data.csv', index_col=0, parse_dates=True)
    if 'Ticker' in df.columns:
        df = df[df['Ticker'] == ticker].copy()
    else:
        raise FileNotFoundError("Ticker column not found in merged_data.csv")
    return df.sort_index()

def run_backtest(signals_file: Path, hold_period:int=5, capital:float=10000.0, commission:float=0.0, slippage:float=0.0):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    signals = pd.read_csv(signals_file, parse_dates=['Date'])
    # expect Date, Ticker, Signal columns
    trades = []
    equity_series = []
    # maintain daily equity by date from earliest price to latest
    all_dates = pd.date_range(start=signals['Date'].min(), end=signals['Date'].max())
    equity = pd.Series(index=all_dates, dtype=float)
    equity.iloc[:] = np.nan
    cash = capital
    positions = []  # list of dicts: {ticker, entry_date, exit_date, entry_price, exit_price, size, pnl}
    # For each signal row, if BUY create a trade, if SELL create short trade (not implemented - skip)
    for idx, row in signals.iterrows():
        sig = row.get('Signal', None)
        if sig != 'BUY':
            continue
        ticker = row['Ticker'] if 'Ticker' in row else None
        date = row['Date']
        # load price data for ticker
        try:
            df_price = load_price_data(ticker)
        except Exception as e:
            print(f"[WARN] Price data for {ticker} not available: {e}")
            continue
        # find entry price at next trading day open after signal date
        future_dates = df_price.index[df_price.index >= pd.Timestamp(date) + pd.Timedelta(days=1)]
        if len(future_dates) == 0:
            continue
        entry_idx = future_dates[0]
        entry_row = df_price.loc[entry_idx]
        entry_price = entry_row.get('Open', entry_row.get('Close'))
        exit_idx_pos = df_price.index.get_loc(entry_idx) + hold_period - 1
        if exit_idx_pos >= len(df_price):
            # not enough data to exit
            continue
        exit_idx = df_price.index[exit_idx_pos]
        exit_row = df_price.iloc[exit_idx_pos]
        exit_price = exit_row.get('Close')
        size = capital / entry_price  # full allocation (1.0)
        gross_pnl = (exit_price - entry_price) * size
        trade_commission = commission * 2  # entry + exit
        trade_slippage = slippage * entry_price * 2  # approximate
        net_pnl = gross_pnl - trade_commission - trade_slippage
        trades.append({
            'Ticker': ticker,
            'signal_date': date.strftime('%Y-%m-%d'),
            'entry_date': entry_idx.strftime('%Y-%m-%d'),
            'exit_date': exit_idx.strftime('%Y-%m-%d'),
            'entry_price': float(entry_price),
            'exit_price': float(exit_price),
            'size': float(size),
            'gross_pnl': float(gross_pnl),
            'net_pnl': float(net_pnl)
        })
    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        print("[BACKTEST] No trades executed.")
        return None
    trades_file = OUTPUT_DIR / f"trade_log_{signals_file.stem}_{ts}.csv"
    trades_df.to_csv(trades_file, index=False)
    # build equity curve by summing net_pnl cumulatively on exit dates
    trades_df['exit_date'] = pd.to_datetime(trades_df['exit_date'])
    equity_df = trades_df.groupby('exit_date')['net_pnl'].sum().sort_index().cumsum()
    # expand to daily series
    full_idx = pd.date_range(start=equity_df.index.min(), end=equity_df.index.max())
    daily = pd.Series(index=full_idx, data=0.0)
    for d, v in equity_df.items():
        daily.loc[d] = v
    daily = daily.cumsum()
    equity_file = OUTPUT_DIR / f"equity_curve_{signals_file.stem}_{ts}.csv"
    daily.to_csv(equity_file, header=['equity'])
    # metrics
    total_return = daily.iloc[-1] / capital
    pnl = trades_df['net_pnl'].sum()
    wins = trades_df[trades_df['net_pnl'] > 0]
    win_rate = len(wins) / len(trades_df)
    max_dd = compute_max_drawdown(daily.values)
    metrics = {
        'n_trades': int(len(trades_df)),
        'total_pnl': float(pnl),
        'total_return': float(total_return),
        'win_rate': float(win_rate),
        'max_drawdown': float(max_dd)
    }
    metrics_file = REPORTS_DIR / f"backtest_report_{signals_file.stem}_{ts}.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    print("[BACKTEST] Trade log:", trades_file)
    print("[BACKTEST] Equity curve:", equity_file)
    print("[BACKTEST] Report:", metrics_file)
    return {
        'trades_file': str(trades_file),
        'equity_file': str(equity_file),
        'report': str(metrics_file)
    }

def compute_max_drawdown(equity_array):
    # equity_array is cumulative equity series
    peak = -np.inf
    max_dd = 0.0
    for x in equity_array:
        if x > peak:
            peak = x
        dd = (peak - x)
        if dd > max_dd:
            max_dd = dd
    return float(max_dd)

def batch_run_master(master_file: Path, hold_period:int=5, capital:float=10000.0, commission:float=0.0, slippage:float=0.0):
    # run backtest per model file in master signals (if contains model flag), otherwise use file names
    res = []
    files = sorted(Path('ml/signals').glob('generated_signals_*.csv'))
    for f in files:
        out = run_backtest(f, hold_period=hold_period, capital=capital, commission=commission, slippage=slippage)
        if out:
            res.append(out)
    return res

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--signals', type=str, default='ml/signals/generated_signals_master.csv', help='Signals master file or pattern')
    parser.add_argument('--hold', type=int, default=5)
    parser.add_argument('--capital', type=float, default=10000.0)
    parser.add_argument('--commission', type=float, default=0.0)
    parser.add_argument('--slippage', type=float, default=0.0)
    args = parser.parse_args()
    batch_run_master(args.signals, hold_period=args.hold, capital=args.capital, commission=args.commission, slippage=args.slippage)
