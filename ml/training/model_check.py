# ==============================================
# MT5_BOT — ml/training/model_check.py
# Versión 1.2 (Modo estricto con log automático)
# ==============================================

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path(__file__).resolve().parents[2] / "infra" / "processed" / "merged_data.csv"
LOG_PATH = Path(__file__).resolve().parents[2] / "Docs" / "Logs" / "MLLogs" / "check_report.json"

def verify_data(cfg):
    """Verifica la consistencia de los datos antes de entrenar."""
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "OK",
        "rows": 0,
        "columns_checked": [],
        "missing_columns": [],
        "non_numeric_columns": [],
        "notes": ""
    }
    print("[CHECK] Verificando consistencia de datos...")

    # Archivo CSV
    if not DATA_PATH.exists():
        print(f"[ERROR] No se encontró {DATA_PATH}")
        report["status"] = "ERROR"
        report["notes"] = "Archivo no encontrado."
        LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise FileNotFoundError("Archivo merged_data.csv no encontrado.")

    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    report["rows"] = len(df)
    if len(df) < 200:
        print(f"[ERROR] Dataset muy pequeño: {len(df)} filas (mínimo 200).")
        report["status"] = "ERROR"
        report["notes"] = "Dataset insuficiente."
        LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise ValueError("Dataset insuficiente.")

    # Columnas
    features = cfg.get("features", [])
    target = cfg["target_column"]
    expected = features + [target]
    report["columns_checked"] = expected
    missing = [c for c in expected if c not in df.columns]
    if missing:
        print(f"[ERROR] Faltan columnas: {missing}")
        report["status"] = "ERROR"
        report["missing_columns"] = missing
        LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise KeyError(f"Columnas faltantes: {missing}")

    # Tipos numéricos
    non_numeric = [c for c in features if not pd.api.types.is_numeric_dtype(df[c])]
    if non_numeric:
        print(f"[ERROR] Columnas no numéricas: {non_numeric}")
        report["status"] = "ERROR"
        report["non_numeric_columns"] = non_numeric
        LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise TypeError(f"Columnas no numéricas: {non_numeric}")

    # Índice de fechas
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        print("[ERROR] Índice no temporal.")
        report["status"] = "ERROR"
        report["notes"] = "Índice no temporal."
        LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise TypeError("El índice no es datetime.")

    print("[OK] Verificación completada correctamente.")
    report["notes"] = "All checks passed successfully."
    LOG_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return True
