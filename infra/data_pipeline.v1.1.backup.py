# ==============================================
# MT5_BOT — data_pipeline.py (versión 1.0)
# Última actualización: 2025-11-11
# ==============================================
# Módulo de procesamiento de datos descargados desde fetch_b3_data.py.
# Este pipeline prepara los datos para análisis, ML y backtesting.
# ----------------------------------------------

import pandas as pd
from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------
# 1️⃣ Carga de datos
# ----------------------------------------------
def load_data():
    """Carga todos los archivos CSV desde infra/data/ y los concatena."""
    files = list(DATA_DIR.glob("*.csv"))
    if not files:
        print("[WARN] No se encontraron archivos CSV en infra/data/")
        return pd.DataFrame()
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, index_col=0, parse_dates=True)
            df.index.name = "Date"
            df["Ticker"] = f.stem.split("_")[0]
            dfs.append(df)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar {f.name}: {e}")
    if dfs:
        merged = pd.concat(dfs, axis=0)
        print(f"[INFO] Cargados {len(dfs)} archivos — total filas: {len(merged)}")
        return merged
    else:
        return pd.DataFrame()

# ----------------------------------------------
# 2️⃣ Limpieza de datos
# ----------------------------------------------
def clean_data(df: pd.DataFrame):
    """Limpia los datos eliminando nulos, duplicados y fechas inválidas."""
    if df.empty:
        print("[WARN] DataFrame vacío en clean_data()")
        return df
    df = df.dropna(how="any")
    df = df[~df.index.duplicated(keep="first")]
    df = df.sort_index()
    print(f"[INFO] Datos limpiados — filas restantes: {len(df)}")
    return df

# ----------------------------------------------
# 3️⃣ Normalización y features básicas
# ----------------------------------------------
def normalize_data(df: pd.DataFrame):
    """Genera columnas derivadas como retornos y medias móviles simples."""
    if df.empty:
        return df
    df["Return"] = df.groupby("Ticker")["Adj Close"].pct_change()
    df["MA_5"] = df.groupby("Ticker")["Adj Close"].transform(lambda x: x.rolling(5).mean())
    df["MA_20"] = df.groupby("Ticker")["Adj Close"].transform(lambda x: x.rolling(20).mean())
    print("[INFO] Variables derivadas agregadas (Return, MA_5, MA_20)")
    return df

# ----------------------------------------------
# 4️⃣ Guardado de datos procesados
# ----------------------------------------------
def save_processed_data(df: pd.DataFrame):
    """Guarda el DataFrame procesado y genera resumen estadístico."""
    if df.empty:
        print("[WARN] No hay datos para guardar.")
        return
    out_file = OUTPUT_DIR / "merged_data.csv"
    df.to_csv(out_file)
    print(f"[OK] Datos procesados guardados en {out_file}")

    # Generar metadatos
    meta = {
        "total_rows": len(df),
        "tickers": df["Ticker"].nunique(),
        "start_date": str(df.index.min().date()),
        "end_date": str(df.index.max().date())
    }
    meta_file = OUTPUT_DIR / "metadata_summary.json"
    meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"[OK] Metadatos guardados en {meta_file}")

# ----------------------------------------------
# 5️⃣ Flujo principal
# ----------------------------------------------
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
