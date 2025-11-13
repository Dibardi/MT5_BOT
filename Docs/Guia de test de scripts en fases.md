Serie de ordenes secuenciales para prueba de fases

>>>Infra
python infra\fetch_b3_data.py --tickers PETR4.SA VALE3.SA --start 2018-01-01 --end 2025-11-12

python infra\data_pipeline.py

>>>ML
python ml/training/model_check.py

>>>>TRAINER

python -m ml.training.trainer

>>>>OPTUNA

python -m ml.optimization.optimize_model --trials 200

Cómo usar ML v1.2.5
🔸 Usar modelo optimizado (por defecto):
python -m ml.signals.signal_generator


#### NUEVA NUEVA NUEVA VERSION OPTUNA 

🧪 Cómo probar ahora
Para generar señales del modelo optimizado:
python -m ml.signals.signal_generator --model v1_3

Para modelo base y agregar al maestro:
python -m ml.signals.signal_generator --model v1_2 --append

Para comparar modelos:
python -m ml.signals.signal_compare


Esto producirá:

ml/signals/signal_comparison_latest.csv


>>>>>BACKTESTING MODULE

 python -m ml.backtesting.backtest --signals ml/signals/generated_signals_master.csv --hold 5 --capital 10000 --commission 0.0 --slippage 0.0


 Ejecuta (ejemplo, generar para todos y añadir al master):

python -m ml.signals.signal_generator_fix_final --model v1_3 --ticker ALL --append


O para tickers específicos:

python -m ml.signals.signal_generator_fix_final --model v1_3 --ticker PETR4,VALE3 --append

#### FINAL ####
python -m ml.signals.signal_generator_fix_final_v2 --model v1_3 --ticker ALL --append

Verifica:

python - <<'PY'
import pandas as pd
df = pd.read_csv("ml/signals/generated_signals_master.csv", parse_dates=['Date'])
print(df['Signal'].value_counts())
print("Unique tickers:", df['Ticker'].nunique())
print(df.head())
PY


Si ahora tienes BUY con tickers reales, ejecuta el backtest:

python -m ml.backtesting.backtest --signals ml/signals/generated_signals_master.csv --hold 5 --

