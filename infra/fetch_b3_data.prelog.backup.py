# ==============================================
# MT5_BOT — fetch_b3_data.py (versión con modo automático)
# Última actualización: 2025-11-11
# ==============================================

import yfinance as yf
import pandas as pd
from pathlib import Path
import argparse
import json
from datetime import datetime
from tqdm import tqdm
from joblib import Parallel, delayed

def load_config_defaults():
    config_path = Path(__file__).resolve().parent / "config_data.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def ensure_data_dir(storage_path):
    path = Path(storage_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def fetch_ticker_data(ticker, start, end, interval, storage_path):
    df = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
    if df.empty:
        print(f"[WARN] No data for {ticker}")
        return None
    filename = f"{ticker.replace('.', '_')}_{interval}_{start}_{end}.csv"
    file_path = Path(storage_path) / filename
    df.to_csv(file_path)
    print(f"[OK] Saved {ticker} → {file_path.name} ({len(df)} rows)")
    return file_path

def main():
    parser = argparse.ArgumentParser(description="Descarga datos bursátiles de la B3 (Yahoo Finance).")
    parser.add_argument("--tickers", "-t", nargs="+", required=False, help="Lista de tickers (opcional si están en config_data.json)")
    parser.add_argument("--start", type=str, help="Fecha de inicio (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="Fecha de fin (YYYY-MM-DD)")
    parser.add_argument("--interval", type=str, default="1d", help="Intervalo de tiempo (1d, 1h, etc.)")
    parser.add_argument("--n_jobs", type=int, default=4, help="Número de descargas paralelas")
    parser.add_argument("--storage_path", type=str, default="./infra/data/", help="Ruta donde se guardarán los archivos CSV")
    args = parser.parse_args()

    # Cargar configuración predeterminada
    cfg = load_config_defaults()
    if not args.tickers:
        args.tickers = cfg.get("tickers", [])
        args.start = args.start or cfg.get("start_date", "2020-01-01")
        args.end = args.end or cfg.get("end_date", "today")
        print("[AUTO] Ejecutando en modo automático — tickers cargados desde config_data.json")
    else:
        print("[MANUAL] Ejecutando en modo manual — tickers definidos por argumentos")

    if not args.tickers:
        raise ValueError("No se encontraron tickers ni en los argumentos ni en config_data.json")

    data_dir = ensure_data_dir(args.storage_path)
    print(f"[INFO] Guardando datos en: {data_dir.resolve()}")
    print(f"[INFO] Período: {args.start} → {args.end}")
    print(f"[INFO] Total de tickers: {len(args.tickers)}")

    Parallel(n_jobs=args.n_jobs)(
        delayed(fetch_ticker_data)(ticker, args.start, args.end, args.interval, data_dir)
        for ticker in tqdm(args.tickers, desc="Descargando datos", unit="ticker")
    )

if __name__ == "__main__":
    main()
