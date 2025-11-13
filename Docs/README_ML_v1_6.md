# ML v1.6 - Per-Ticker Training & Signal Generation

This package contains scripts to build datasets per ticker, train per-ticker models (regression + classifier),
and generate signals using a combined filter (regression magnitude + classifier probability).

Files:
- ml/training/dataset_builder_v1_6.py
- ml/training/trainer_v1_6.py
- ml/signals/generate_signals_v1_6.py

Typical workflow (run locally in your C:\MT5_BOT project with .venv active):

1) Build dataset for a ticker:
   python ml/training/dataset_builder_v1_6.py --ticker PETR4 --merged infra/processed/merged_data.csv --out ml/data/

2) Train models for that ticker:
   python -m ml.training.trainer_v1_6 --ticker PETR4 --data ml/data/features_PETR4.csv --model-dir ml/models --n-estimators 200 --max-depth 8

3) Generate signals using trained models:
   python ml/signals/generate_signals_v1_6.py --ticker PETR4 --data ml/data/features_PETR4.csv --model-dir ml/models --out ml/signals/tickers --ret-thr 0.005 --p-thr 0.6

4) Backtest signals with existing backtester:
   python -m ml.backtesting.backtest_v1_5 --signals ml/signals/tickers/generated_signals_v1_6_PETR4.csv --mode C --hold 5 --capital 10000 --commission 6.0 --slippage 0.0005 --risk 0.01

Notes:
- Thresholds (ret-thr, p-thr) are conservative defaults. Calibrate per ticker using validation.
- Use `git` to commit scripts and results. Keep models out of public repos or use git-lfs for large files.
- For production, implement walk-forward CV and Optuna hyperparameter tuning per ticker.
