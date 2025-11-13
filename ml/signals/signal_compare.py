# ml/signals/signal_compare.py
"""
ML v1.2.6 — Signal Comparison Module
Compares latest signals of model v1_2 vs v1_3 side by side.
"""

from pathlib import Path
import pandas as pd

SIGNALS_DIR = Path("ml/signals")

def load_latest(version: str):
    files = sorted(SIGNALS_DIR.glob(f"generated_signals_{version}_*.csv"))
    if not files:
        raise FileNotFoundError(f"No signal files found for {version}")
    return pd.read_csv(files[-1])

def compare():
    df2 = load_latest("v1_2")
    df3 = load_latest("v1_3")

    df = df2.merge(df3, on=["Date", "Ticker"], suffixes=("_v1_2", "_v1_3"))

    df["signal_match"] = df["Signal_v1_2"] == df["Signal_v1_3"]
    df["signal_diff"] = df["Signal_v1_2"] + " → " + df["Signal_v1_3"]

    output = SIGNALS_DIR / "signal_comparison_latest.csv"
    df.to_csv(output, index=False)
    print("[COMPARE] Comparison saved to:", output)

if __name__ == "__main__":
    compare()
