import pandas as pd
import numpy as np
from pathlib import Path

def load_csv(path):
    # Intentar cargar normalmente
    df = pd.read_csv(path)

    # Si la primera columna no tiene nombre, lo reparamos
    first_col = df.columns[0]

    if first_col.lower() not in ["date", "data"]:
        # Si el header parece numérico o timestamp → es la fecha sin nombre
        try:
            pd.to_datetime(df.iloc[0, 0])
            print("[FIX] Detectado CSV sin columna 'Date'. Corrigiendo...")
            df.rename(columns={first_col: "Date"}, inplace=True)
        except:
            raise RuntimeError("El CSV no contiene una columna de fecha válida.")

    # Convertir a datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Ordenar y limpiar
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def add_features(df):
    # ---- RETURNS ----
    df["Return"] = df["Close"].pct_change()
    df["ret_1d"] = df["Return"]
    df["ret_3d"] = df["Close"].pct_change(3)
    df["ret_5d"] = df["Close"].pct_change(5)

    # ---- MOVING AVERAGES ----
    df["MA_5"] = df["Close"].rolling(5).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["MA_ratio"] = df["MA_5"] / df["MA_20"]

    # ---- VOLUMEN ----
    df["vol_5"] = df["Volume"].rolling(5).mean()
    df["vol_20"] = df["Volume"].rolling(20).mean()

    # ---- ATR ----
    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR_14"] = tr.rolling(14).mean()
    df["ATR_pct"] = df["ATR_14"] / df["Close"]

    # ---- RSI ----
    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(14).mean()
    avg_loss = pd.Series(loss).rolling(14).mean()
    RS = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + RS))

    # ---- MACD ----
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"] = df["MACD"] - df["MACD_signal"]

    # ---- TARGETS ----
    df["target_ret_5d"] = df["Close"].shift(-5) / df["Close"] - 1
    df["target_bin_5d"] = (df["target_ret_5d"] > 0).astype(int)

    return df


def save_features(df, ticker):
    out = Path("ml/data") / f"features_{ticker}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"[OK] Features guardadas en: {out}")


def main():
    tickers = ["PETR4", "VALE3"]

    for ticker in tickers:
        raw = Path("infra/data") / f"{ticker}_SA_1d_2018-01-01_2025-11-12.csv"

        if not raw.exists():
            print(f"[WARN] No existe CSV: {raw}")
            continue

        print(f"[PIPELINE_v2_2] Procesando: {raw}")

        df = load_csv(raw)
        df = add_features(df)
        df["Ticker"] = ticker

        save_features(df, ticker)


if __name__ == "__main__":
    main()
    