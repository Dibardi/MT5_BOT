# infra/data_pipeline_v2.py
"""
INFRA v2.0 - Recompute features used by ML and produce merged_data_features.csv
Usage:
    python infra/data_pipeline_v2.py --input infra/processed/merged_data.csv --output infra/processed/merged_data_features.csv
Notes:
- Assumes merged_data.csv contains Date index and columns including: Open, High, Low, Close, Adj Close, Volume, Ticker
- Produces technical indicators: MA_5, MA_20, EMA_9, EMA_21, RSI_14, MACD, MACD_signal, MACD_hist, ATR_14
- Produces target_return_5d and saves CSV ready for model prediction and signal generation.
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # ensure numeric
    for c in ['Close','High','Low','Open','Volume','Adj Close']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    # Moving averages
    df['MA_5'] = df['Close'].rolling(window=5, min_periods=1).mean()
    df['MA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()
    # EMA
    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
    # RSI 14 (smoothed)
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/14, adjust=False).mean()
    ma_down = down.ewm(alpha=1/14, adjust=False).mean()
    rs = ma_up / ma_down
    df['RSI_14'] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    # ATR (14)
    high_low = df['High'] - df['Low']
    high_prev = (df['High'] - df['Close'].shift()).abs()
    low_prev = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_prev, low_prev], axis=1).max(axis=1)
    df['ATR_14'] = tr.ewm(alpha=1/14, adjust=False).mean()
    # Return (daily)
    df['Return'] = df['Close'].pct_change()
    # Target: 5-day return
    df['target_return_5d'] = df['Close'].shift(-5) / df['Close'] - 1
    return df

def main(input_path: Path, output_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    df = pd.read_csv(input_path, index_col=0, parse_dates=True)
    # If merged contains multiple tickers stacked (same Date repeated), keep as is.
    # Process per ticker if Ticker column present.
    if 'Ticker' in df.columns:
        out_frames = []
        for t in df['Ticker'].astype(str).unique():
            sub = df[df['Ticker'].astype(str) == t].sort_index()
            sub_proc = compute_indicators(sub)
            out_frames.append(sub_proc)
        df_out = pd.concat(out_frames).sort_index()
    else:
        df_out = compute_indicators(df.sort_index())
    # Clean infinite and NaN target rows
    df_out = df_out.replace([np.inf, -np.inf], pd.NA)
    # drop rows where target_return_5d is NaN (can't train/predict on them)
    # but keep features where possible
    df_out = df_out.dropna(subset=['target_return_5d'], how='any')
    # Save file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(output_path, index=True)
    print(f"[INFRA_v2] Saved features file: {output_path} (rows: {len(df_out)})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="infra/processed/merged_data.csv")
    parser.add_argument("--output", type=str, default="infra/processed/merged_data_features.csv")
    args = parser.parse_args()
    main(Path(args.input), Path(args.output))
