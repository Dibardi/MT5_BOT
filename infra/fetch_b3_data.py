# ==============================================
# MT5_BOT — fetch_b3_data.py (versión 4.2 — date-only fix)
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
import time

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

def parse_dates_safe(start, end, fallback_start="2018-01-01"):
    try:
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y-%m-%d").date()
        if isinstance(end, str):
            if end.lower() == "today":
                end = datetime.now().date()
            else:
                end = datetime.strptime(end, "%Y-%m-%d").date()
    except Exception as e:
        print(f"[WARN] Error interpretando fechas: {e} — usando rango por defecto ({fallback_start} → hoy)")
        start = datetime.strptime(fallback_start, "%Y-%m-%d").date()
        end = datetime.now().date()
    return start, end

def fetch_ticker_data(ticker, start, end, interval, storage_path, max_retries=3):
    success = False
    rows = 0
    status = "⚠️ No data"
    for attempt in range(1, max_retries + 1):
        try:
            start_dt, end_dt = parse_dates_safe(start, end)
            df = yf.download(ticker, start=start_dt, end=end_dt, interval=interval, progress=False)
            if not df.empty:
                first_date = df.index.min().strftime("%Y-%m-%d")
                last_date = df.index.max().strftime("%Y-%m-%d")
                if first_date < "2000-01-01":
                    status = "⚠️ Out of range (data before 2000)"
                    print(f"[WARN] {ticker} devolvió datos fuera de rango ({first_date}–{last_date})")
                else:
                    status = "✅ OK"
                filename = f"{ticker.replace('.', '_')}_{interval}_{start_dt}_{end_dt}.csv"
                file_path = Path(storage_path) / filename
                df.to_csv(file_path)
                rows = len(df)
                success = True
                return ticker, file_path.name, rows, status
            else:
                print(f"[WARN] No data for {ticker} (Intento {attempt}/{max_retries})")
        except Exception as e:
            print(f"[ERROR] {ticker} — intento {attempt}/{max_retries} fallido: {e}")
        time.sleep(2)
    return ticker, None, rows, status

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
        args.start = args.start or cfg.get("start_date", "2018-01-01")
        args.end = args.end or cfg.get("end_date", "today")
        print("[AUTO] Ejecutando en modo automático — tickers cargados desde config_data.json")
        mode = "AUTO"
    else:
        print("[MANUAL] Ejecutando en modo manual — tickers definidos por argumentos")
        mode = "MANUAL"

    if not args.tickers:
        raise ValueError("No se encontraron tickers ni en los argumentos ni en config_data.json")

    data_dir = ensure_data_dir(args.storage_path)
    print(f"[INFO] Guardando datos en: {data_dir.resolve()}")
    print(f"[INFO] Período: {args.start} → {args.end}")
    print(f"[INFO] Total de tickers: {len(args.tickers)}")

    start_time = time.time()
    results = Parallel(n_jobs=args.n_jobs)(
        delayed(fetch_ticker_data)(ticker, args.start, args.end, args.interval, data_dir)
        for ticker in tqdm(args.tickers, desc="Descargando datos", unit="ticker")
    )
    duration = round(time.time() - start_time, 2)

    # === Crear log automático ===
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    project_root = Path(__file__).resolve().parents[1]  # raíz del proyecto
    log_dir = project_root / "Docs" / "Logs" / "ExecLogs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{timestamp}_FETCH_LOG.md"

    log_lines = [
        f"# 🧾 Registro de descarga automática — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"## ⚙️ Modo: {mode}\n",
        f"## 📊 Tickers descargados: {', '.join(args.tickers)}\n",
        "## 📂 Resultados:\n",
        "| Archivo | Filas | Estado |\n|----------|--------|--------|\n"
    ]

    for ticker, file_name, rows, status in results:
        log_lines.append(f"| {file_name or ticker} | {rows} | {status} |\n")

    log_lines.append(f"\n## ⏱️ Duración total:\n`{duration} segundos`\n")
    log_file.write_text("".join(log_lines), encoding="utf-8")
    print(f"[LOG] Registro creado en: {log_file}")

if __name__ == "__main__":
    main()
