# ==============================================
# MT5_BOT — data_pipeline.py (versión 1.6)
# Última actualización: 2025-11-11
# ==============================================
# Mejora: reemplazo del argumento obsoleto 'date_parser' por 'date_format'.
# Compatible con Pandas >= 2.2. Elimina todos los warnings de parsing.
# ----------------------------------------------

import pandas as pd
from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    files = list(DATA_DIR.glob("*.csv"))
    if not files:
        print("[WARN] No se encontraron archivos CSV en infra/data/")
        return pd.DataFrame()
    dfs = []
    for f in files:
        try:
            # Nueva sintaxis moderna sin warnings
            df = pd.read_csv(f, index_col=0, parse_dates=[0], date_format="%Y-%m-%d")
            if "Ticker" not in df.columns and "Close" not in df.columns:
                raise ValueError("Formato no estándar detectado, intentando modo yfinance")
        except Exception:
            try:
                df = pd.read_csv(f, skiprows=2)
                if "Price" in df.columns:
                    df.rename(columns={"Price": "Date"}, inplace=True)
                if "Date" not in df.columns:
                    raise ValueError("No se encontró columna Date")
                df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
                df.dropna(subset=["Date"], inplace=True)
                df.set_index("Date", inplace=True)
                df.index.name = "Date"
            except Exception as e:
                print(f"[ERROR] No se pudo cargar {f.name}: {e}")
                continue
        df["Ticker"] = f.stem.split("_")[0]
        dfs.append(df)
    if dfs:
        merged = pd.concat(dfs, axis=0)
        print(f"[INFO] Cargados {len(dfs)} archivos — total filas: {len(merged)}")
        return merged
    else:
        return pd.DataFrame()

def clean_data(df: pd.DataFrame):
    if df.empty:
        print("[WARN] DataFrame vacío en clean_data()")
        return df
    df = df.dropna(how="any")
    df = df[~df.index.duplicated(keep="first")]
    df = df.sort_index()
    print(f"[INFO] Datos limpiados — filas restantes: {len(df)}")
    return df

def normalize_data(df: pd.DataFrame):
    if df.empty:
        return df

    numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace(" ", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]

    df["Return"] = df.groupby("Ticker")["Adj Close"].pct_change(fill_method=None)
    df["MA_5"] = df.groupby("Ticker")["Adj Close"].transform(lambda x: x.rolling(5).mean())
    df["MA_20"] = df.groupby("Ticker")["Adj Close"].transform(lambda x: x.rolling(20).mean())
    print("[INFO] Variables derivadas agregadas (Return, MA_5, MA_20)")
    return df

def save_processed_data(df: pd.DataFrame):
    if df.empty:
        print("[WARN] No hay datos para guardar.")
        return
    out_file = OUTPUT_DIR / "merged_data.csv"
    df.to_csv(out_file)
    print(f"[OK] Datos procesados guardados en {out_file}")

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors="coerce")

    start_date = df.index.min()
    end_date = df.index.max()

    meta = {
        "total_rows": int(len(df)),
        "tickers": int(df["Ticker"].nunique()),
        "start_date": str(start_date.date()) if pd.notna(start_date) else None,
        "end_date": str(end_date.date()) if pd.notna(end_date) else None
    }
    meta_file = OUTPUT_DIR / "metadata_summary.json"
    meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"[OK] Metadatos guardados en {meta_file}")

def run_pipeline():
    df = load_data()
    if df.empty:
        print("[ERROR] No se pudo ejecutar el pipeline: no hay datos cargados.")
        return
    df = clean_data(df)
    df = normalize_data(df)
    save_processed_data(df)
    print("[PIPELINE] Ejecución completada correctamente.")

if __name__ == "__main__":
    run_pipeline()
