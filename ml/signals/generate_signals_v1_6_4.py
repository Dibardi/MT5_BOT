import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import joblib


def load_features(path, ticker):
    df = pd.read_csv(path)

    # Normalizar columna Date si existe
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Filtrar por ticker si viene en el dataset
    if "Ticker" in df.columns:
        df = df[df["Ticker"].astype(str).str.upper() == ticker.upper()].copy()

    if df.empty:
        raise RuntimeError(f"No hay filas válidas para el ticker {ticker} en {path}")

    # Verificación final de Date
    if "Date" not in df.columns:
        raise RuntimeError("El dataset de features NO contiene columna 'Date'. Esto es obligatorio.")

    if df["Date"].isna().any():
        raise RuntimeError("Hay fechas inválidas en la columna 'Date' del dataset.")

    df = df.sort_values("Date").reset_index(drop=True)
    return df


def load_models(model_dir, ticker):
    scaler_path = Path(model_dir) / ticker / f"scaler_v1_6_{ticker}.pkl"
    reg_path = Path(model_dir) / ticker / f"model_v1_6_reg_{ticker}.pkl"
    clf_path = Path(model_dir) / ticker / f"model_v1_6_clf_{ticker}.pkl"

    scaler = joblib.load(scaler_path)
    reg = joblib.load(reg_path)
    clf = joblib.load(clf_path)

    # Obtener nombres de columnas entrenadas
    if hasattr(scaler, "feature_names_in_"):
        features = list(scaler.feature_names_in_)
    else:
        raise RuntimeError(
            f"El scaler '{scaler_path}' NO contiene 'feature_names_in_'. "
            "Esto es requerido para alinear features."
        )

    return scaler, reg, clf, features


def generate_signals(df, scaler, reg, clf, features, ret_thr, p_thr, ticker):

    # Verificar todas las columnas necesarias
    missing = [c for c in features if c not in df.columns]
    if missing:
        raise RuntimeError(f"Faltan columnas requeridas para generar features: {missing}")

    # Ensamblar matriz
    X = df[features].copy().fillna(0)

    # Escalar
    Xs = scaler.transform(X)

    # Predicciones
    df["pred_reg"] = reg.predict(Xs)

    # Probabilidad BUY
    try:
        df["pred_proba"] = clf.predict_proba(Xs)[:, 1]
    except:
        scores = clf.decision_function(Xs)
        df["pred_proba"] = 1 / (1 + np.exp(-scores))

    # Señales
    df["Signal"] = np.where(
        (df["pred_reg"] >= ret_thr) & (df["pred_proba"] >= p_thr),
        "BUY",
        "HOLD"
    )

    # Mantener ticker
    df["Ticker"] = ticker

    return df


def main(ticker, data_path, model_dir, output_path, ret_thr, p_thr):

    # 1. Cargar features
    df = load_features(data_path, ticker)

    # 2. Cargar modelos
    scaler, reg, clf, features = load_models(model_dir, ticker)

    # 3. Generar señales
    df = generate_signals(df, scaler, reg, clf, features, ret_thr, p_thr, ticker)

    # 4. Guardar salida
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    out_file = output_path / f"generated_signals_v1_6_{ticker}.csv"
    df.to_csv(out_file, index=False)

    print(f"[OK] Señales generadas correctamente para {ticker}")
    print(f"[OK] Archivo: {out_file}")
    print(f"[OK] Filas: {len(df)}")
    print(f"[OK] Features utilizadas: {len(features)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de señales ML v1.6.4 final")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--ret-thr", type=float, default=0.005)
    parser.add_argument("--p-thr", type=float, default=0.6)

    args = parser.parse_args()

    main(
        ticker=args.ticker,
        data_path=args.data,
        model_dir=args.model_dir,
        output_path=args.out,
        ret_thr=args.ret_thr,
        p_thr=args.p_thr
    )