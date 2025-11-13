BACKTEST FIX v1.5 - README
=========================
This fixed backtest script ensures:
- JSON report is always written (even when no trades executed)
- Robust directory creation and file naming with timestamps
- Replaces deprecated pandas.Series.fillna(method='ffill') with .ffill()
- Writes a small note file if no trades executed to help auditing
Usage:
    python -m ml.backtesting.backtest_v1_5 --signals <signals_csv> --mode C --hold 5 --capital 10000 --commission 6.0 --slippage 0.0005 --risk 0.01
