# data_pipeline.py — Versión corregida (fechas + numéricos)

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("infra/data")
OUTPUT_FILE = Path("infra/processed/merged_data.csv")

def load_and_fix_csv(f: Path):
    df = pd.read_csv(f, index_col=0, parse_dates=False)

    # Intentar parsear columna Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        df = df.set_index("Date")
    else:
        try:
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d", errors="coerce")
        except:
            df.index = pd.to_datetime(df.index, errors="coerce")

    df = df[~df.index.isna()]

    # Forzar numéricos
    numeric_cols = ["Adj Close", "Close", "Open", "High", "Low", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Adj Close"])

    return df


def main():
    print("[PIPELINE] Procesando CSVs...")

    all_files = list(DATA_DIR.glob("*.csv"))
    if not all_files:
        print("[PIPELINE] No hay archivos CSV en infra/data/")
        return

    dfs = []
    for f in all_files:
        df = load_and_fix_csv(f)
        dfs.append(df)

    merged = pd.concat(dfs).sort_index()

    # Cálculo de Return por ticker
    if "Ticker" in merged.columns:
        merged["Return"] = merged.groupby("Ticker")["Adj Close"].apply(lambda s: s.pct_change())
    else:
        merged["Return"] = merged["Adj Close"].pct_change()

    merged.to_csv(OUTPUT_FILE)
    print(f"[PIPELINE] Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
