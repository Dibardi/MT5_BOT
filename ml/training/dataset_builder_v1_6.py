# dataset_builder_v1_6.py
"""Build per-ticker feature CSVs from infra/processed/merged_data.csv

Usage:
    python ml/training/dataset_builder_v1_6.py --ticker PETR4 --merged infra/processed/merged_data.csv --out ml/data/
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def build_for_ticker(ticker, merged_path, out_dir):
    merged_path = Path(merged_path)
    if not merged_path.exists():
        raise FileNotFoundError(f"Merged data not found: {merged_path}")
    df = pd.read_csv(merged_path, index_col=0, parse_dates=True)
    if 'Ticker' in df.columns:
        df_t = df[df['Ticker'].astype(str).str.upper().str.contains(ticker.upper())].copy()
    else:
        df_t = df.copy()
    if df_t.empty:
        raise RuntimeError(f"No data for ticker {ticker} in {merged_path}")
    df_t = df_t.sort_index()
    # Ensure numeric
    for c in ['Adj Close','Close','Open','High','Low','Volume','ATR_14']:
        if c in df_t.columns:
            df_t[c] = pd.to_numeric(df_t[c], errors='coerce')
    price_col = 'Adj Close' if 'Adj Close' in df_t.columns else 'Close'
    df_t['close'] = df_t[price_col].astype(float)
    # Features
    df_t['MA_5'] = df_t['close'].rolling(5, min_periods=1).mean()
    df_t['MA_20'] = df_t['close'].rolling(20, min_periods=1).mean()
    df_t['MA_ratio'] = df_t['MA_5'] / df_t['MA_20']
    df_t['ret_1d'] = df_t['close'].pct_change(1)
    df_t['ret_3d'] = df_t['close'].pct_change(3)
    df_t['ret_5d'] = df_t['close'].pct_change(5)
    df_t['vol_5'] = df_t['ret_1d'].rolling(5).std()
    df_t['vol_20'] = df_t['ret_1d'].rolling(20).std()
    # ATR
    if 'ATR_14' not in df_t.columns or df_t['ATR_14'].isna().all():
        high = df_t['High'] if 'High' in df_t.columns else df_t['close']
        low = df_t['Low'] if 'Low' in df_t.columns else df_t['close']
        prev_close = df_t['close'].shift(1)
        tr = pd.concat([high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
        df_t['ATR_14'] = tr.rolling(14, min_periods=1).mean()
    df_t['ATR_pct'] = df_t['ATR_14'] / df_t['close']
    # RSI 14
    delta = df_t['close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / (ema_down + 1e-9)
    df_t['RSI_14'] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df_t['close'].ewm(span=12, adjust=False).mean()
    ema26 = df_t['close'].ewm(span=26, adjust=False).mean()
    df_t['MACD'] = ema12 - ema26
    df_t['MACD_signal'] = df_t['MACD'].ewm(span=9, adjust=False).mean()
    df_t['MACD_hist'] = df_t['MACD'] - df_t['MACD_signal']
    # Target and label
    df_t['target_ret_5d'] = df_t['close'].shift(-5) / df_t['close'] - 1
    df_t['target_bin_5d'] = (df_t['target_ret_5d'] >= 0.005).astype(int)
    df_t = df_t.dropna(subset=['target_ret_5d'])
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"features_{ticker}.csv"
    df_t.to_csv(out_file)
    print(f"[DATASET] Saved {out_file} ({len(df_t)} rows)")
    return out_file

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ticker', required=True)
    p.add_argument('--merged', default='infra/processed/merged_data.csv')
    p.add_argument('--out', default='ml/data/')
    args = p.parse_args()
    build_for_ticker(args.ticker, args.merged, args.out)
