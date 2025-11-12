# ==============================================
# MT5_BOT — ml/training/trainer.py (versión 1.1.3)
# Última actualización: 2025-11-12
# ==============================================
# Corrección: prints con f-strings evaluables y compatibilidad de RMSE en evaluate_model.
# ----------------------------------------------

import pandas as pd
import json
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from model_utils import split_data, train_model, evaluate_model, save_model

DATA_PATH = Path(__file__).resolve().parents[2] / "infra" / "processed" / "merged_data.csv"
CONFIG_PATH = Path(__file__).resolve().parent / "config_ml.json"
LOG_PATH = Path(__file__).resolve().parents[2] / "Docs" / "Logs" / "MLLogs"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "randomforest_model.pkl"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    cfg = load_config()
    print(f"[INFO] Configuración cargada: {cfg['model_type']}")


    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    df.index.name = "Date"
    print(f"[INFO] Datos cargados: {len(df)} filas")


    features = cfg.get("features", [])
    target = cfg["target_column"]

    # Keep only the necessary columns: features + target
    cols_needed = features + [target]
    df = df[cols_needed].dropna()
    print(f"[INFO] Features: {features} | Target: {target} | Filas válidas: {len(df)}")


    # Split using features list to avoid non-numeric columns
    X_train, X_test, y_train, y_test = split_data(df, target, features=features, test_size=cfg["validation_split"], random_state=cfg["random_state"]) 

    print("[TRAIN] Entrenando modelo RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=cfg["n_estimators"],
        max_depth=cfg["max_depth"],
        random_state=cfg["random_state"]
    )
    model = train_model(model, X_train, y_train)
    print("[OK] Entrenamiento completado.")

    metrics = evaluate_model(model, X_test, y_test)
    print(f"[METRICS] MAE={metrics['MAE']:.6f} | RMSE={metrics['RMSE']:.6f} | R²={metrics['R2']:.4f}")


    save_model(model, MODEL_PATH)

    LOG_PATH.mkdir(parents=True, exist_ok=True)
    report = {
        "model": cfg["model_type"],
        "parameters": {
            "n_estimators": cfg["n_estimators"],
            "max_depth": cfg["max_depth"],
            "validation_split": cfg["validation_split"]
        },
        "metrics": metrics,
        "timestamp": "2025-11-12"
    }
    report_path = LOG_PATH / "training_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[OK] Reporte guardado en {report_path}")


if __name__ == "__main__":
    main()
