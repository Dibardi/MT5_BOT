# =========================================================
# MT5_BOT — infra/data_pipeline.py (v1.8.4)
# ---------------------------------------------------------
# - Elimina UserWarning de formato de fechas
# - Asegura índice datetime limpio y validado
# - Mantiene compatibilidad completa con fetch_b3_data v4.4
# =========================================================

import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "infra" / "data"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "infra" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def merge_data() -> pd.DataFrame:
    print("[PIPELINE] Fusionando datos descargados...")
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("[ERROR] No se encontraron archivos CSV en", DATA_DIR)
        return pd.DataFrame()

    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, index_col=0, parse_dates=True)
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d", errors="coerce")
            df = df[~df.index.isna()]
            df["Ticker"] = file.stem.split("_")[0]
            dfs.append(df)
        except Exception as e:
            print(f"[WARN] Error al leer {file.name}: {e}")

    if not dfs:
        print("[ERROR] Ningún archivo pudo ser leído correctamente.")
        return pd.DataFrame()

    df_merged = pd.concat(dfs)
    print(f"[OK] {len(df_merged)} filas combinadas de {len(csv_files)} archivos.")
    return df_merged

def clean_and_convert(df: pd.DataFrame) -> pd.DataFrame:
    print("[CLEAN] Convirtiendo columnas numéricas...")
    numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Close"])
    print(f"[OK] Conversión completada. Filas válidas: {len(df)}")
    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    print("[FEATURES] Generando columnas MA_5, MA_20 y Return...")
    if "Close" not in df.columns:
        print("[ERROR] No se encontró columna 'Close'.")
        return df

    df["MA_5"] = df["Close"].rolling(window=5, min_periods=1).mean()
    df["MA_20"] = df["Close"].rolling(window=20, min_periods=1).mean()
    df["Return"] = df["Close"].pct_change()
    print("[OK] Columnas de features creadas correctamente.")
    return df

def save_processed_data(df: pd.DataFrame):
    if df.empty:
        print("[WARN] No hay datos para guardar.")
        return

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors="coerce")
    df = df[~df.index.isna()].sort_index()
    df.index.name = "Date"

    out_file = OUTPUT_DIR / "merged_data.csv"
    df.to_csv(out_file, date_format="%Y-%m-%d", index=True)
    print(f"[OK] Datos procesados guardados en {out_file}")

    start_date = df.index.min()
    end_date = df.index.max()
    meta = {
        "total_rows": int(len(df)),
        "tickers": int(df["Ticker"].nunique()) if "Ticker" in df.columns else None,
        "start_date": str(start_date.date()) if pd.notna(start_date) else None,
        "end_date": str(end_date.date()) if pd.notna(end_date) else None,
        "features": ["MA_5", "MA_20", "Return"]
    }
    meta_file = OUTPUT_DIR / "metadata_summary.json"
    meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"[OK] Metadatos guardados en {meta_file}")

if __name__ == "__main__":
    df = merge_data()
    if not df.empty:
        df = clean_and_convert(df)
        df = add_features(df)
        save_processed_data(df)
        print("[PIPELINE] Proceso completado exitosamente.")
    else:
        print("[PIPELINE] No se generó DataFrame válido.")
