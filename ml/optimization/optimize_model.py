# ml/optimization/optimize_model.py
"""
Optuna optimization for ML v1.3
Optimizes RandomForestRegressor and GradientBoostingRegressor over specified search spaces.
Saves best model, best parameters, study db and trial dataframe.
"""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import optuna
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from ml.training.dataset_builder import build_dataset

LOGS_DIR = Path('Docs/Logs/MLLogs')
MODELS_DIR = Path('ml/models')
OPT_DIR = Path('ml/optimization')
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
OPT_DIR.mkdir(parents=True, exist_ok=True)

def objective(trial):
    # choose model type
    model_choice = trial.suggest_categorical("model", ["rfr", "gbr"])
    X, y = build_dataset()
    if len(X) < 50:
        raise optuna.exceptions.TrialPruned()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_choice == "rfr":
        n_estimators = trial.suggest_int("rfr_n_estimators", 100, 1000)
        max_depth = trial.suggest_int("rfr_max_depth", 3, 20)
        min_samples_split = trial.suggest_int("rfr_min_samples_split", 2, 20)
        min_samples_leaf = trial.suggest_int("rfr_min_samples_leaf", 1, 10)
        max_features = trial.suggest_categorical("rfr_max_features", ["sqrt", "log2"])
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            n_jobs=-1,
            random_state=42
        )
    else:
        n_estimators = trial.suggest_int("gbr_n_estimators", 100, 1000)
        learning_rate = trial.suggest_float("gbr_learning_rate", 1e-3, 0.5, log=True)
        max_depth = trial.suggest_int("gbr_max_depth", 3, 20)
        min_samples_split = trial.suggest_int("gbr_min_samples_split", 2, 20)
        min_samples_leaf = trial.suggest_int("gbr_min_samples_leaf", 1, 10)
        subsample = trial.suggest_float("gbr_subsample", 0.5, 1.0)
        max_features = trial.suggest_categorical("gbr_max_features", ["sqrt", "log2"])
        model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            subsample=subsample,
            max_features=max_features,
            random_state=42
        )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2 = float(r2_score(y_test, preds))
    trial.set_user_attr("n_train", len(X_train))
    trial.set_user_attr("n_test", len(X_test))
    return r2

def run_optuna(trials:int=200, study_name:str="mt5_optuna_study", storage_path:Path=LOGS_DIR / "optuna_study.db"):
    storage_url = f"sqlite:///{storage_path.resolve()}"
    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction="maximize", sampler=sampler, study_name=study_name, storage=storage_url, load_if_exists=True)
    print(f"[OPTUNA] Starting optimization: study={study_name}, trials={trials}, storage={storage_url}")
    study.optimize(objective, n_trials=trials, show_progress_bar=True)

    print("[OPTUNA] Optimization completed. Best trial:")
    best = study.best_trial
    print(f"  R2: {best.value}")
    print(f"  Params: {best.params}")

    best_params_file = OPT_DIR / "best_params.json"
    with open(best_params_file, "w", encoding="utf-8") as f:
        json.dump({"value": best.value, "params": best.params}, f, indent=2)

    # retrain best model on full train set
    X, y = build_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    params = best.params
    if params.get("model", "rfr") == "rfr" or ("rfr_n_estimators" in params):
        rfr_params = {
            "n_estimators": params.get("rfr_n_estimators", 100),
            "max_depth": params.get("rfr_max_depth", None),
            "min_samples_split": params.get("rfr_min_samples_split", 2),
            "min_samples_leaf": params.get("rfr_min_samples_leaf", 1),
            "max_features": params.get("rfr_max_features", "sqrt"),
            "n_jobs": -1,
            "random_state": 42
        }
        best_model = RandomForestRegressor(**rfr_params)
    else:
        gbr_params = {
            "n_estimators": params.get("gbr_n_estimators", 100),
            "learning_rate": params.get("gbr_learning_rate", 0.1),
            "max_depth": params.get("gbr_max_depth", 3),
            "min_samples_split": params.get("gbr_min_samples_split", 2),
            "min_samples_leaf": params.get("gbr_min_samples_leaf", 1),
            "subsample": params.get("gbr_subsample", 1.0),
            "max_features": params.get("gbr_max_features", "sqrt"),
            "random_state": 42
        }
        best_model = GradientBoostingRegressor(**gbr_params)

    print("[OPTUNA] Retraining best model on full train set...")
    best_model.fit(X_train, y_train)
    preds = best_model.predict(X_test)
    best_r2 = float(r2_score(y_test, preds))
    metrics = {"best_r2_test": best_r2}
    metrics_file = LOGS_DIR / "optuna_best_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    model_file = MODELS_DIR / "model_v1_3_optuna.pkl"
    joblib.dump(best_model, model_file)
    print("[OPTUNA] Best model saved to", model_file)
    try:
        df = study.trials_dataframe(attrs=("number", "value", "params", "state"))
        df_file = OPT_DIR / "trials_dataframe.csv"
        df.to_csv(df_file, index=False)
    except Exception as e:
        print("[OPTUNA] Could not save trials dataframe:", e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200)
    args = parser.parse_args()
    run_optuna(trials=args.trials)
