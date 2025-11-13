# =========================================================
# MT5_BOT — infra/fetch_b3_data.py (v4.4)
# ---------------------------------------------------------
# - Elimina FutureWarning de yfinance
# - Mantiene compatibilidad con pipeline v1.8.2
# - Estructura clara, mensajes uniformes
# =========================================================

import yfinance as yf
import pandas as pd
from pathlib import Path
from joblib import Parallel, delayed
from datetime import datetime
import argparse, json, sys

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "infra" / "data"
LOG_DIR = Path(__file__).resolve().parents[2] / "Docs" / "Logs" / "ExecLogs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def fetch_ticker(ticker, start, end, interval):
    print(f"[FETCH] Descargando {ticker}...")
    try:
        df = yf.download(
            ticker, start=start, end=end, interval=interval,
            progress=False, auto_adjust=False
        )
        if df.empty:
            print(f"[WARN] Sin datos para {ticker}")
            return None

        df.index = pd.to_datetime(df.index, errors="coerce")
        df.index.name = "Date"
        out = OUTPUT_DIR / f"{ticker.replace('.', '_')}_{interval}_{start}_{end}.csv"
        df.to_csv(out, date_format="%Y-%m-%d", index=True)
        print(f"[OK] {ticker} guardado en {out}")
        return {"ticker": ticker, "rows": len(df), "path": str(out)}
    except Exception as e:
        print(f"[ERROR] {ticker}: {e}")
        return {"ticker": ticker, "error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--interval", default="1d")
    args = parser.parse_args()

    start, end = args.start, args.end
    tickers = args.tickers
    print(f"[INFO] Descargando {len(tickers)} tickers desde {start} hasta {end}...")

    results = Parallel(n_jobs=-1)(
        delayed(fetch_ticker)(t, start, end, args.interval) for t in tickers
    )
    log_path = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}_FETCH_LOG.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[LOG] Registro guardado en {log_path}")
    print("[FETCH] Proceso completado correctamente.")

if __name__ == "__main__":
    main()
