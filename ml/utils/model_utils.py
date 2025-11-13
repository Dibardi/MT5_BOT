# ml/utils/model_utils.py
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    return {
        'MAE': float(mean_absolute_error(y_test, preds)),
        'RMSE': float(mean_squared_error(y_test, preds, squared=False)),
        'R2': float(r2_score(y_test, preds))
    }
