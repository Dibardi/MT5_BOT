# ==============================================
# MT5_BOT — ml/training/model_utils.py (v1.1.3)
# Última actualización: 2025-11-12
# ==============================================
# Funciones auxiliares para entrenamiento, evaluación y guardado de modelos ML.
# Compatibilidad: evitar uso de parámetros recientes de sklearn para RMSE.
# ----------------------------------------------

import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import math

def split_data(df, target_col, features=None, test_size=0.2, random_state=42):
    """Divide el dataset en entrenamiento y validación.
    Si `features` es provisto, usará únicamente esas columnas como X.
    De lo contrario, usará todas las columnas excepto target_col.
    Esto evita pasar columnas no numéricas (como 'Ticker') a sklearn.
    """
    if features is not None:
        X = df[features]
    else:
        X = df.drop(columns=[target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = math.sqrt(mse)
    metrics = {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2_score(y_test, preds))
    }
    return metrics

def save_model(model, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"[OK] Modelo guardado en {path}")
