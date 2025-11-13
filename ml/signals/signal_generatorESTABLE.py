# ml/signals/signal_generator.py
"""
ML v1.2.5 — Signal Generator (BUY / SELL / HOLD) - FIXED
Now saves separate output files per model + timestamp and can append to a master file.
Usage:
    python -m ml.signals.signal_generator --model v1_3 --append
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib
from ml.training.dataset_builder import build_dataset

MODELS_DIR = Path("ml/models")
SIGNALS_DIR = Path("ml/signals")
SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR = Path("Docs/Logs/MLLogs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

MASTER_FILE = SIGNALS_DIR / "generated_signals_master.csv"

def generate_signals(model_version: str, do_append: bool = False):
    print(f"[SIGNALS] Loading model version: {model_version}")

    if model_version == "v1_2":
        model_path = MODELS_DIR / "model_v1_2_rfr.pkl"
    elif model_version == "v1_3":
        model_path = MODELS_DIR / "model_v1_3_optuna.pkl"
    else:
        raise ValueError("Unknown model version. Use v1_2 or v1_3.")

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    model = joblib.load(model_path)

    X, y = build_dataset()

    print(f"[SIGNALS] Generating predictions for {len(X)} rows...")
    preds = model.predict(X)

    df = X.copy()
    df = df.reset_index()  # keep Date as column for clarity
    df["predicted_return_5d"] = preds

    # Decision rules
    def classify(ret):
        if ret > 0.015:
            return "BUY"
        elif ret < -0.01:
            return "SELL"
        else:
            return "HOLD"

    df["Signal"] = df["predicted_return_5d"].apply(classify)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = SIGNALS_DIR / f"generated_signals_{model_version}_{timestamp}.csv"

    df.to_csv(output_file, index=False)
    print("[SIGNALS] Signals saved to:", output_file)

    # Optionally append to master file (keeps history of all runs)
    if do_append:
        if MASTER_FILE.exists():
            master_df = pd.read_csv(MASTER_FILE)
            # avoid duplicate rows by index columns (Date and any unique feature combination)
            combined = pd.concat([master_df, df], ignore_index=True)
            combined = combined.drop_duplicates(subset=df.columns.tolist(), keep="last")
            combined.to_csv(MASTER_FILE, index=False)
        else:
            df.to_csv(MASTER_FILE, index=False)
        print("[SIGNALS] Appended to master file:", MASTER_FILE)

    log = {
        "model_used": model_version,
        "rows": len(df),
        "output_file": str(output_file),
        "master_appended": bool(do_append)
    }

    with open(LOGS_DIR / f"signal_generation_log_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    print("[SIGNALS] Log saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="v1_3", help="Choose model: v1_2 or v1_3")
    parser.add_argument("--append", action="store_true", help="Append results to master signals file")
    args = parser.parse_args()

    generate_signals(args.model, do_append=args.append)
