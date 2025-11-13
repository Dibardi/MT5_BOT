# ML v1.4 - Backtesting Module
## Cómo usar
1. Asegúrate de tener `ml/signals/generated_signals_master.csv` o archivos `generated_signals_{model}_*.csv` en `ml/signals/`.
2. Ejecuta:
   ```
   python -m ml.backtesting.backtest --signals ml/signals/generated_signals_master.csv --hold 5 --capital 10000 --commission 6.0 --slippage 0.0005
   ```
3. Salidas:
   - `ml/backtesting/output/trade_log_<signals_file>_<ts>.csv`
   - `ml/backtesting/output/equity_curve_<signals_file>_<ts>.csv`
   - `Docs/Reports/backtest_report_<signals_file>_<ts>.json`

## Notas
- El backtester asume entrada en la siguiente jornada (Open) y salida al Close tras `hold` días.
- No implementa posiciones short (SELL) en esta versión; SELL signals se ignoran por ahora.
- Ajusta `commission` y `slippage` según tu broker.
