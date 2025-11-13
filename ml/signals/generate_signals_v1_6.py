# generate_signals_v1_6.py
"""Generate signals using trained regressor + classifier for a ticker.

Usage:
    python ml/signals/generate_signals_v1_6.py --ticker PETR4 --data ml/data/features_PETR4.csv --model-dir ml/models/PETR4 --out ml/signals/tickers/
"""
import argparse, joblib
from pathlib import Path
import pandas as pd
import numpy as np

def generate(ticker, data_file, model_dir, out_dir='ml/signals/tickers', ret_thr=0.005, p_thr=0.6):
    data_file = Path(data_file)
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    df = pd.read_csv(data_file, index_col=0, parse_dates=True)
    features = [c for c in df.columns if c not in ['target_ret_5d','target_bin_5d','Ticker']]
    X = df[features].fillna(0)
    model_dir = Path(model_dir) / ticker
    scaler = joblib.load(model_dir / f"scaler_v1_6_{ticker}.pkl")
    reg = joblib.load(model_dir / f"model_v1_6_reg_{ticker}.pkl")
    clf = joblib.load(model_dir / f"model_v1_6_clf_{ticker}.pkl")
    Xs = scaler.transform(X)
    preds_reg = reg.predict(Xs)
    preds_proba = clf.predict_proba(Xs)[:,1] if hasattr(clf, 'predict_proba') else None
    df['pred_reg'] = preds_reg
    df['pred_proba'] = preds_proba
    df['Signal'] = np.where((df['pred_reg'] >= ret_thr) & (df['pred_proba'] >= p_thr), 'BUY', 'HOLD')
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"generated_signals_v1_6_{ticker}.csv"
    df.to_csv(out_file)
    print(f"[SIGNALS] Saved {out_file}")
    return out_file

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ticker', required=True)
    p.add_argument('--data', required=True)
    p.add_argument('--model-dir', required=True)
    p.add_argument('--out', default='ml/signals/tickers')
    p.add_argument('--ret-thr', default=0.005, type=float)
    p.add_argument('--p-thr', default=0.6, type=float)
    args = p.parse_args()
    generate(args.ticker, args.data, args.model_dir, args.out, args.ret_thr, args.p_thr)
