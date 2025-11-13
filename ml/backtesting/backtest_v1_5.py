# ml/backtesting/backtest_v1_5.py
"""
Backtest v1.5 - professional backtester with three modes:
 A - single position active at a time
 B - multi-position with equal capital allocation per ticker
 C - risk-based sizing (default) using risk% per trade and ATR-based stop
Usage example:
  python -m ml.backtesting.backtest_v1_5 --signals ml/signals/master/generated_signals_master.csv --mode C --hold 5 --capital 10000 --commission 6.0 --slippage 0.0005 --risk 0.01
Notes:
 - Expects infra/processed/merged_data_features.csv with Ticker, Close, Open, ATR_14 columns
 - Signals file must include Date (parseable), Ticker, Signal, predicted_return_5d
 - Entries executed at next trading day's Open (or Close fallback); exits at Close after hold days
 - Mode C uses ATR as stop distance; if missing uses 2% price
 - Outputs: trade_log, equity_curve (daily), report JSON
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import math, json
from datetime import timedelta

BASE = Path(".")
SIGNALS_DEFAULT = BASE / "ml" / "signals" / "master" / "generated_signals_master.csv"
DATA_FILE = BASE / "infra" / "processed" / "merged_data_features.csv"
OUTPUT_DIR = BASE / "ml" / "backtesting" / "output_v1_5"
REPORT_DIR = BASE / "Docs" / "Reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_price_data(ticker):
    df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    if 'Ticker' not in df.columns:
        raise RuntimeError("merged_data_features.csv must contain Ticker column")
    df_t = df[df['Ticker'].astype(str) == str(ticker)].sort_index()
    if df_t.empty:
        raise FileNotFoundError(f"No price data for ticker {ticker}")
    return df_t

def size_by_mode(mode, capital_available, risk, atr, entry_price, capital_alloc=None):
    if mode == "A":
        # use full available capital for single position
        size = math.floor(capital_available / entry_price)
        return max(0, size)
    elif mode == "B":
        # allocate equal capital per ticker (capital_alloc should be per-ticker allocation)
        if capital_alloc is None:
            capital_alloc = capital_available
        size = math.floor(capital_alloc / entry_price)
        return max(0, size)
    elif mode == "C":
        # risk-based sizing: risk percent of capital / (stop_distance * entry_price)
        stop_dist = atr if (atr is not None and not np.isnan(atr) and atr>0) else max(0.02*entry_price, 0.01*entry_price)
        risk_amount = capital_available * risk
        denom = stop_dist * entry_price
        if denom <= 0:
            return 0
        size = math.floor(risk_amount / denom)
        return max(0, size)
    else:
        raise ValueError("Unknown mode")

def run_backtest(signals_file: Path, mode="C", hold_period=5, capital=10000.0, commission=6.0, slippage=0.0005, risk=0.01):
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    signals = pd.read_csv(signals_file, parse_dates=['Date'])
    signals = signals[signals['Signal']=="BUY"].copy()
    if signals.empty:
        print("[BACKTEST_v1_5] No BUY signals found.")
        return None
    tickers = sorted(signals['Ticker'].unique().tolist())
    n_tickers = len(tickers)
    initial_capital = capital
    cash = capital
    reserved = 0.0
    open_positions = []
    trades = []
    price_cache = {}
    # Preload price data
    for t in tickers:
        price_cache[t] = load_price_data(t)
    # Prepare processed signals with entry/exit dates and price references
    processed = []
    for _, row in signals.iterrows():
        t = row['Ticker']
        date = pd.Timestamp(row['Date'])
        df_t = price_cache[t]
        future_idx = df_t.index[df_t.index >= date + pd.Timedelta(days=1)]
        if len(future_idx) == 0:
            continue
        entry_date = future_idx[0]
        entry_price = df_t.loc[entry_date].get('Open', df_t.loc[entry_date].get('Close'))
        pos = df_t.index.get_loc(entry_date) + hold_period - 1
        if pos >= len(df_t):
            continue
        exit_date = df_t.index[pos]
        exit_price = df_t.iloc[pos].get('Close')
        atr = df_t.loc[entry_date].get('ATR_14', np.nan) if 'ATR_14' in df_t.columns else np.nan
        processed.append({
            'ticker': t,
            'signal_date': date,
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': float(entry_price),
            'exit_price': float(exit_price),
            'atr': float(atr),
            'predicted_return_5d': row.get('predicted_return_5d', np.nan)
        })
    if not processed:
        print("[BACKTEST_v1_5] No valid processed signals (dates/prices).")
        return None
    processed = sorted(processed, key=lambda x: x['entry_date'])
    all_dates = pd.date_range(start=min([s['entry_date'] for s in processed]), end=max([s['exit_date'] for s in processed]))
    equity_series = []
    for current_date in all_dates:
        # close positions
        to_close = [p for p in open_positions if p['exit_date'] == current_date]
        for p in to_close:
            exit_price = p['exit_price'] * (1 - slippage)
            gross = (exit_price - p['entry_price']) * p['size']
            trade_comm = commission * 2
            net = gross - trade_comm
            trades.append({
                'Ticker': p['ticker'],
                'signal_date': p['signal_date'].strftime('%Y-%m-%d'),
                'entry_date': p['entry_date'].strftime('%Y-%m-%d'),
                'exit_date': p['exit_date'].strftime('%Y-%m-%d'),
                'entry_price': p['entry_price'],
                'exit_price': exit_price,
                'size': int(p['size']),
                'net_pnl': float(net)
            })
            # release reserved cash and update cash
            cash += p['size'] * exit_price
            cash -= trade_comm
            reserved -= p['reserved_cash']
            open_positions.remove(p)
        # open signals for current_date
        todays = [s for s in processed if s['entry_date'] == current_date]
        for s in todays:
            t = s['ticker']
            entry_price = s['entry_price'] * (1 + slippage)
            atr = s.get('atr', np.nan)
            if mode == "A":
                if len(open_positions) > 0:
                    continue
                size = size_by_mode(mode, cash, risk, atr, entry_price)
                reserved_cash = size * entry_price
            elif mode == "B":
                cap_alloc = initial_capital / max(1, n_tickers)
                size = size_by_mode(mode, cap_alloc, risk, atr, entry_price, capital_alloc=cap_alloc)
                reserved_cash = size * entry_price
                if reserved_cash > cash:
                    continue
            elif mode == "C":
                size = size_by_mode(mode, cash, risk, atr, entry_price)
                reserved_cash = size * entry_price
                if reserved_cash > cash:
                    continue
            else:
                continue
            if size <= 0:
                continue
            cash -= reserved_cash
            reserved += reserved_cash
            open_positions.append({
                'ticker': t,
                'signal_date': s['signal_date'],
                'entry_date': s['entry_date'],
                'exit_date': s['exit_date'],
                'entry_price': s['entry_price'],
                'exit_price': s['exit_price'],
                'size': size,
                'reserved_cash': reserved_cash
            })
        # mark-to-market of open positions
        mtm = 0.0
        for p in open_positions:
            dfp = price_cache.get(p['ticker'])
            if current_date in dfp.index:
                price = dfp.loc[current_date].get('Close', dfp.loc[current_date].get('Adj Close'))
            else:
                prev = dfp.index[dfp.index <= current_date]
                if len(prev) == 0:
                    price = p['entry_price']
                else:
                    price = dfp.loc[prev[-1]].get('Close', dfp.loc[prev[-1]].get('Adj Close'))
            mtm += price * p['size']
        equity_val = cash + mtm
        equity_series.append({'date': current_date.strftime('%Y-%m-%d'), 'equity': equity_val})
    # save outputs
    trades_df = pd.DataFrame(trades)
    equity_df = pd.DataFrame(equity_series).set_index('date')
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    trades_file = OUTPUT_DIR / f"trade_log_{signals_file.stem}_{ts}.csv"
    equity_file = OUTPUT_DIR / f"equity_curve_{signals_file.stem}_{ts}.csv"
    report_file = REPORT_DIR / f"backtest_report_{signals_file.stem}_{ts}.json"
    trades_df.to_csv(trades_file, index=False)
    equity_df.to_csv(equity_file)
    total_pnl = trades_df['net_pnl'].sum() if not trades_df.empty else 0.0
    total_return = (equity_df['equity'].iloc[-1] - initial_capital) / initial_capital if not equity_df.empty else 0.0
    win_rate = (trades_df['net_pnl']>0).sum() / len(trades_df) if len(trades_df)>0 else 0.0
    # max drawdown
    cum = equity_df['equity'].fillna(method='ffill').astype(float).values
    peak = -np.inf
    max_dd = 0.0
    for x in cum:
        if x > peak:
            peak = x
        dd = peak - x
        if dd > max_dd:
            max_dd = dd
    metrics = {
        'n_trades': int(len(trades_df)),
        'total_pnl': float(total_pnl),
        'total_return': float(total_return),
        'win_rate': float(win_rate),
        'max_drawdown': float(max_dd)
    }
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    print("[BACKTEST_v1_5] Trade log:", trades_file)
    print("[BACKTEST_v1_5] Equity curve:", equity_file)
    print("[BACKTEST_v1_5] Report:", report_file)
    return {'trades_file': str(trades_file), 'equity_file': str(equity_file), 'report': str(report_file)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", type=str, default=str(SIGNALS_DEFAULT))
    parser.add_argument("--mode", type=str, default="C", choices=["A","B","C"])
    parser.add_argument("--hold", type=int, default=5)
    parser.add_argument("--capital", type=float, default=10000.0)
    parser.add_argument("--commission", type=float, default=6.0)
    parser.add_argument("--slippage", type=float, default=0.0005)
    parser.add_argument("--risk", type=float, default=0.01)
    args = parser.parse_args()
    run_backtest(Path(args.signals), mode=args.mode, hold_period=args.hold, capital=args.capital, commission=args.commission, slippage=args.slippage, risk=args.risk)
