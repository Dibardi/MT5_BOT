# ml/training/trainer.py
"""
Trainer for ML v1.2 - RandomForestRegressor
Fixed RMSE computation for compatibility with older sklearn versions.
"""

import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml.training.dataset_builder import build_dataset

OUTPUT_MODEL = Path('ml/models')
OUTPUT_MODEL.mkdir(parents=True, exist_ok=True)

LOGS = Path('Docs/Logs/MLLogs')
LOGS.mkdir(parents=True, exist_ok=True)

def main():
    print('[TRAINER] Construyendo dataset...')
    X, y = build_dataset()

    if len(X) < 50:
        print('[ERROR] Dataset muy pequeño:', len(X))
        return

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f'[TRAIN] Entrenando RandomForestRegressor con {len(X_train)} filas...')
    model = RandomForestRegressor(
        n_estimators=100,
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    # Compute RMSE manually for full compatibility
    mse = mean_squared_error(y_test, preds)
    rmse = float(np.sqrt(mse))

    metrics = {
        'MAE': float(mean_absolute_error(y_test, preds)),
        'RMSE': rmse,
        'R2': float(r2_score(y_test, preds)),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test))
    }

    # Save model
    model_file = OUTPUT_MODEL / 'model_v1_2_rfr.pkl'
    joblib.dump(model, model_file)

    # Save metrics
    metrics_file = LOGS / 'metrics_v1_2.json'
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

    print('[OK] Entrenamiento completado. Metrics saved to', metrics_file)
    print('[OK] Model saved to', model_file)

if __name__ == '__main__':
    main()
