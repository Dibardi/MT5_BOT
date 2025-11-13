# ml/training/feature_engineering.py
"""Feature engineering for MT5_BOT ML v1.2
Generates technical indicators and target_return_5d.
"""
import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
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
    # MACD and signal
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    # ATR (14) approximate
    high_low = df['High'] - df['Low']
    high_prev = (df['High'] - df['Close'].shift()).abs()
    low_prev = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_prev, low_prev], axis=1).max(axis=1)
    df['ATR_14'] = tr.ewm(alpha=1/14, adjust=False).mean()
    # MA fallback
    if 'MA_5' not in df.columns:
        df['MA_5'] = df['Close'].rolling(window=5, min_periods=1).mean()
    if 'MA_20' not in df.columns:
        df['MA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()
    # Return (daily)
    df['Return'] = df['Close'].pct_change()
    # Target: 5-day return
    df['target_return_5d'] = df['Close'].shift(-5) / df['Close'] - 1
    df = df.replace([np.inf, -np.inf], pd.NA)
    df = df.dropna(subset=['target_return_5d'])
    return df
