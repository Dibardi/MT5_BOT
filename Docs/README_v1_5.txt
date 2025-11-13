ML v1.5 - Professional Backtesting package
Contents:
- tools/clean_signals.py  -> reorganize ml/signals into master/, tickers/, archive/
- ml/backtesting/backtest_v1_5.py -> professional backtester with modes A/B/C
- Docs/README_v1_5.txt -> usage notes
Usage quickstart:
1) Backup current ml/signals if you want.
2) Run cleanup to reorganize signals:
   python tools/clean_signals.py --keep-last 3
3) Run backtest in mode C (risk-based 1% default):
   python -m ml.backtesting.backtest_v1_5 --signals ml/signals/master/generated_signals_master.csv --mode C --hold 5 --capital 10000 --commission 6.0 --slippage 0.0005 --risk 0.01
Notes:
- Mode C uses ATR_14 for stop distance; ensure infra/processed/merged_data_features.csv exists and contains ATR_14 and Ticker.
- Review outputs in ml/backtesting/output_v1_5/ and Docs/Reports/
