# ml/signals/signal_generator_fix_final_v2.py
"""
Signal generator updated to use infra/processed/merged_data_features.csv (INFRA v2)
Usage:
    python -m ml.signals.signal_generator_fix_final_v2 --model v1_3 --ticker ALL --append
"""
import argparse, json
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib

MODELS_DIR = Path("ml/models")
SIGNALS_DIR = Path("ml/signals")
SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR = Path("Docs/Logs/MLLogs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MASTER_FILE = SIGNALS_DIR / "generated_signals_master.csv"
FEATURES_FILE = Path("infra/processed/merged_data_features.csv")

def load_model_path(model_version: str) -> Path:
    if model_version == "v1_2":
        return MODELS_DIR / "model_v1_2_rfr.pkl"
    elif model_version == "v1_3":
        return MODELS_DIR / "model_v1_3_optuna.pkl"
    else:
        raise ValueError("Unknown model version. Use v1_2 or v1_3.")

def prepare_features(merged_df: pd.DataFrame):
    # Identify feature columns (exclude Ticker and target)
    exclude = set(['Ticker', 'target_return_5d'])
    feature_cols = [c for c in merged_df.columns if c not in exclude]
    X = merged_df[feature_cols].copy()
    # Drop rows with NaNs to keep model happy
    X = X.replace([pd.NA, pd.NaT], pd.NA).dropna(axis=0, how='any')
    return X, feature_cols

def classify_return(ret: float) -> str:
    if ret > 0.015:
        return "BUY"
    elif ret < -0.01:
        return "SELL"
    else:
        return "HOLD"

def generate_for_tickers(model, merged_df: pd.DataFrame, tickers_list, model_version:str, do_append:bool=False):
    results = []
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for t in tickers_list:
        df_t = merged_df[merged_df['Ticker'].astype(str) == t].copy()
        if df_t.empty:
            print(f"[WARN] No rows for ticker {t} in merged_data_features.csv - skipping")
            continue
        X_t, feature_cols = prepare_features(df_t)
        if X_t.empty:
            print(f"[WARN] No valid feature rows for ticker {t} after dropping NaNs - skipping")
            continue
        ticker_series = df_t.loc[X_t.index, 'Ticker'].astype(str)
        preds = model.predict(X_t)
        out = X_t.reset_index().copy()
        out['Ticker'] = ticker_series.values
        out['predicted_return_5d'] = preds
        out['Signal'] = out['predicted_return_5d'].apply(classify_return)
        safe_t = t.replace('*','ALL') if t == 'ALL' else t
        output_file = SIGNALS_DIR / f"generated_signals_{model_version}_{safe_t}_{ts}.csv"
        out.to_csv(output_file, index=False)
        print(f"[SIGNALS_FIX_FINAL_v2] Signals saved to: {output_file} (rows: {len(out)})")
        if do_append:
            if MASTER_FILE.exists():
                master = pd.read_csv(MASTER_FILE, parse_dates=['Date'], infer_datetime_format=True)
                combined = pd.concat([master, out], ignore_index=True)
                if 'Date' in combined.columns:
                    combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')
                combined = combined.drop_duplicates(subset=['Date', 'Ticker'], keep='last')
                combined.to_csv(MASTER_FILE, index=False)
            else:
                out.to_csv(MASTER_FILE, index=False)
            print(f"[SIGNALS_FIX_FINAL_v2] Appended to master: {MASTER_FILE}")
        log = {"model_used": model_version, "ticker": t, "rows": int(len(out)), "output_file": str(output_file), "appended": bool(do_append)}
        with open(LOGS_DIR / f"signal_generation_fix_final_v2_{t}_{ts}.json", "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)
        results.append(str(output_file))
    return results

def main(model_version: str, ticker_arg: str, do_append: bool):
    model_path = load_model_path(model_version)
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    model = joblib.load(model_path)
    if not FEATURES_FILE.exists():
        raise FileNotFoundError(f"Features file not found: {FEATURES_FILE}; run infra/data_pipeline_v2.py first.")
    merged = pd.read_csv(FEATURES_FILE, index_col=0, parse_dates=True)
    if 'Ticker' not in merged.columns:
        raise RuntimeError("Features file does not contain 'Ticker' column.")
    if ticker_arg.upper() == 'ALL':
        tickers_list = merged['Ticker'].astype(str).unique().tolist()
    else:
        tickers_list = [t.strip() for t in ticker_arg.split(',') if t.strip()]
    print(f"[SIGNALS_FIX_FINAL_v2] Model: {model_path.name} | Tickers: {len(tickers_list)} | Append: {do_append}")
    results = generate_for_tickers(model, merged, tickers_list, model_version, do_append)
    print("[SIGNALS_FIX_FINAL_v2] Completed. Files generated:", results)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="v1_3")
    parser.add_argument("--ticker", type=str, default="ALL")
    parser.add_argument("--append", action="store_true")
    args = parser.parse_args()
    main(args.model, args.ticker, args.append)
