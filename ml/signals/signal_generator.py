# ml/signals/signal_generator_fix.py
"""
Fixed signal generator that preserves Ticker from infra/processed/merged_data.csv
Usage:
    python -m ml.signals.signal_generator_fix --model v1_3 --append
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib

# Paths
MODELS_DIR = Path("ml/models")
SIGNALS_DIR = Path("ml/signals")
SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR = Path("Docs/Logs/MLLogs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MASTER_FILE = SIGNALS_DIR / "generated_signals_master.csv"
MERGED_DATA = Path("infra/processed/merged_data.csv")

def load_model_path(model_version: str) -> Path:
    if model_version == "v1_2":
        return MODELS_DIR / "model_v1_2_rfr.pkl"
    elif model_version == "v1_3":
        return MODELS_DIR / "model_v1_3_optuna.pkl"
    else:
        raise ValueError("Unknown model version. Use v1_2 or v1_3.")

def generate_signals(model_version: str, do_append: bool = False):
    model_path = load_model_path(model_version)
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    model = joblib.load(model_path)
    if not MERGED_DATA.exists():
        raise FileNotFoundError(f"Merged data not found: {MERGED_DATA}")

    # Load merged_data with Ticker column preserved. Keep original row order.
    merged = pd.read_csv(MERGED_DATA, index_col=0, parse_dates=True)
    # Ensure Ticker column exists
    if 'Ticker' not in merged.columns:
        raise RuntimeError("Merged data does not contain 'Ticker' column. Please regenerate merge with Ticker present.")

    # Apply the same feature engineering used in training (if needed).
    # Simpler and safe approach: reconstruct X by reusing the feature columns present in merged.
    # We expect merged already contains the engineered features (MA_5, MA_20, EMA_9, RSI_14, etc).
    # Identify feature columns by excluding Ticker and any target columns.
    candidate_cols = [c for c in merged.columns if c not in ['Ticker', 'target_return_5d']]
    X = merged[candidate_cols].copy()

    # Drop rows that don't have enough data (NaNs)
    X = X.replace([pd.NA, pd.NaT], pd.NA).dropna(axis=0, how='any')
    # Align ticker column to X (keep same index/rows)
    ticker_series = merged.loc[X.index, 'Ticker'].astype(str)

    # Now predict
    print(f"[SIGNALS_FIX] Generating predictions for {len(X)} rows using model {model_path.name} ...")
    preds = model.predict(X)

    df_out = X.reset_index().copy()  # Date becomes a column
    df_out['Ticker'] = ticker_series.values
    df_out['predicted_return_5d'] = preds

    # Classification rules (same as before)
    def classify(ret):
        if ret > 0.015:
            return "BUY"
        elif ret < -0.01:
            return "SELL"
        else:
            return "HOLD"

    df_out['Signal'] = df_out['predicted_return_5d'].apply(classify)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = SIGNALS_DIR / f"generated_signals_{model_version}_{ts}.csv"
    df_out.to_csv(output_file, index=False)
    print("[SIGNALS_FIX] Signals saved to:", output_file)

    # Append to master if requested (avoid duplicates using Date + Ticker)
    if do_append:
        if MASTER_FILE.exists():
            master = pd.read_csv(MASTER_FILE, parse_dates=['Date'])
            combined = pd.concat([master, df_out], ignore_index=True)
            combined = combined.drop_duplicates(subset=['Date', 'Ticker'], keep='last')
            combined.to_csv(MASTER_FILE, index=False)
        else:
            df_out.to_csv(MASTER_FILE, index=False)
        print("[SIGNALS_FIX] Appended to master:", MASTER_FILE)

    # Save small log
    log = {"model_used": model_version, "rows": len(df_out), "output_file": str(output_file), "appended": bool(do_append)}
    with open(LOGS_DIR / f"signal_generation_fix_log_{ts}.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print("[SIGNALS_FIX] Log saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="v1_3", help="v1_2 or v1_3")
    parser.add_argument("--append", action="store_true")
    args = parser.parse_args()
    generate_signals(args.model, do_append=args.append)
