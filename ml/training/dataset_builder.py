# ml/training/dataset_builder.py
"""
Build dataset X,y for training from processed merged_data.csv
Fully aligned version (1.2.1)
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, List
from ml.training.feature_engineering import add_technical_indicators

DATA_PATH = Path('infra/processed/merged_data.csv')

def build_dataset(tickers: List[str]=None) -> Tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)

    if tickers is not None and 'Ticker' in df.columns:
        df = df[df['Ticker'].isin(tickers)]

    # Apply features + target
    df = add_technical_indicators(df)

    # Remove infinite and NaN values globally (features + target)
    df = df.replace([float('inf'), float('-inf')], pd.NA)
    df = df.dropna(axis=0, how="any")

    # Select features
    drop_cols = ['Ticker'] if 'Ticker' in df.columns else []
    feature_cols = [c for c in df.columns if c not in drop_cols + ['target_return_5d']]

    # Build X and y
    X = df[feature_cols].copy()
    y = df['target_return_5d'].copy()

    # Force alignment
    common_index = X.index.intersection(y.index)
    X = X.loc[common_index]
    y = y.loc[common_index]

    return X, y
