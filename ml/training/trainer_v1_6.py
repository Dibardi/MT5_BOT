# trainer_v1_6.py
"""Train regression & classification models per ticker (ML v1.6)

Usage:
    python -m ml.training.trainer_v1_6 --ticker PETR4 --data ml/data/features_PETR4.csv --model-dir ml/models
"""
import argparse, json
from pathlib import Path
import pandas as pd, numpy as np, joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, roc_auc_score, precision_score, recall_score

def train(ticker, data_path, model_dir, n_estimators=200, max_depth=8):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    features = [c for c in df.columns if c not in ['target_ret_5d','target_bin_5d','Ticker']]
    if len(features) == 0:
        raise RuntimeError('No features found in dataset.')
    X = df[features].fillna(0)
    y_reg = df['target_ret_5d']
    y_clf = df['target_bin_5d']
    n = len(X)
    split_idx = int(n*0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train_reg, y_test_reg = y_reg.iloc[:split_idx], y_reg.iloc[split_idx:]
    y_train_clf, y_test_clf = y_clf.iloc[:split_idx], y_clf.iloc[split_idx:]
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    rfr = RandomForestRegressor(n_estimators=int(n_estimators), max_depth=int(max_depth), random_state=42, n_jobs=-1)
    rfc = RandomForestClassifier(n_estimators=int(n_estimators), max_depth=int(max_depth), random_state=42, n_jobs=-1)
    rfr.fit(X_train_s, y_train_reg)
    rfc.fit(X_train_s, y_train_clf)
    preds_reg = rfr.predict(X_test_s)
    preds_clf = rfc.predict(X_test_s)
    preds_clf_proba = rfc.predict_proba(X_test_s)[:,1] if hasattr(rfc, 'predict_proba') else None
    metrics = {
        'reg_rmse': float(mean_squared_error(y_test_reg, preds_reg, squared=False)),
        'reg_mse': float(mean_squared_error(y_test_reg, preds_reg, squared=True)),
        'clf_accuracy': float(accuracy_score(y_test_clf, preds_clf)),
        'clf_auc': float(roc_auc_score(y_test_clf, preds_clf_proba)) if preds_clf_proba is not None and len(set(y_test_clf))>1 else None,
        'clf_precision': float(precision_score(y_test_clf, preds_clf, zero_division=0)),
        'clf_recall': float(recall_score(y_test_clf, preds_clf, zero_division=0)),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test))
    }
    model_dir = Path(model_dir) / ticker
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(rfr, model_dir / f"model_v1_6_reg_{ticker}.pkl")
    joblib.dump(rfc, model_dir / f"model_v1_6_clf_{ticker}.pkl")
    joblib.dump(scaler, model_dir / f"scaler_v1_6_{ticker}.pkl")
    report = {
        'ticker': ticker,
        'features': features,
        'metrics': metrics,
        'models': {
            'regressor': str(model_dir / f"model_v1_6_reg_{ticker}.pkl"),
            'classifier': str(model_dir / f"model_v1_6_clf_{ticker}.pkl"),
            'scaler': str(model_dir / f"scaler_v1_6_{ticker}.pkl")
        }
    }
    out_report = Path('Docs') / 'Reports'
    out_report.mkdir(parents=True, exist_ok=True)
    with open(out_report / f"trainer_report_{ticker}.json","w") as f:
        json.dump(report, f, indent=2)
    print(f"[TRAINER] Done. Metrics: {metrics}")
    return report

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ticker', required=True)
    p.add_argument('--data', required=True)
    p.add_argument('--model-dir', default='ml/models')
    p.add_argument('--n-estimators', default=200)
    p.add_argument('--max-depth', default=8)
    args = p.parse_args()
    train(args.ticker, args.data, args.model_dir, args.n_estimators, args.max_depth)
