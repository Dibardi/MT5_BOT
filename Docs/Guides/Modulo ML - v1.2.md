FASE ML — Versión 1.2
Objetivo Real:

Crear el primer modelo entrenable, completamente funcional, utilizando los datos ya procesados por tu pipeline.

//////////////////////////////////////////

# 🚀 FASE ML — Versión 1.2  
### **Guía Oficial del Módulo de Aprendizaje Automático (Machine Learning)**  
Proyecto: **MT5_BOT**

---

# 🎯 Objetivo de la Fase ML v1.2

Construir el **primer modelo entrenable y funcional**, capaz de hacer predicciones sobre movimientos de precio en el mercado bursátil brasileño utilizando datos históricos ya preprocesados en la Fase INFRA.

Esta fase incorpora:
- Ingeniería avanzada de características (features)
- Definición del target (variable a predecir)
- Preparación del dataset
- Entrenamiento del modelo
- Validación y reporte de resultados

---

# 1️⃣ Feature Engineering Avanzado

Ya contamos con features base provenientes del pipeline:
- `MA_5`
- `MA_20`
- `Return`

En esta fase agregaremos indicadores técnicos esenciales para Swing Trading:

### 📌 Indicadores nuevos

| Indicador | Propósito | Relevancia para Swing Trading |
|----------|-----------|-------------------------------|
| **RSI (14)** | Mide fuerza del movimiento | Identifica sobrecompra/sobreventa |
| **MACD (MACD, Signal, Hist.)** | Momentum + cruces | Detecta cambios de tendencia |
| **EMA 9 y EMA 21** | Tendencias de corto y medio plazo | Base de estrategias swing |
| **ATR (Volatilidad)** | Rango real del precio | Ajusta el riesgo y selección de trade |

Estos indicadores ayudan al modelo a identificar:
- Giros probables
- Continuación de tendencia
- Exhaustión de movimientos

---

# 2️⃣ Definición del Target  
## **Target elegido por el usuario:**
### 🟦 **Precio de cierre dentro de 5 días**  
```python
target = df["Close"].shift(-5)

Esto es un modelo de regresión, donde el modelo aprende a “mirar hacia adelante”.

✔️ Ventaja:

Mantiene coherencia con estrategias swing de 3–10 días.

3️⃣ Preparación del Dataset para ML

A partir del merged_data.csv se crea:

✔️ Features (X)

Incluye:

MAs

RSI

MACD

EMAs

ATR

Return

Volumen

Tendencia reciente (rolling windows)

Señales codificadas

✔️ Target (y)

Es el valor futuro del precio:  Close_future_5d

4️⃣ Entrenador ML v1.2

Incluye:

Selección de features

Train/test split (80/20)

Normalización opcional

Modelos iniciales:

RandomForestRegressor

GradientBoostingRegressor

Metrics:

MAE

RMSE

R²

5️⃣ Validación Final

El script genera:

Métricas

Comparación Real vs Predicho

Tablas de validación

Resumen consolidado

///////////////////////////////////////////////////////

📌 Resumen

Fase ML v1.2 establece todos los cimientos del aprendizaje automático del bot:
datos → features → target → modelo → validación → modelo listo para usar.

---

# ✔️ 2) CONFIRMADO  
Usaremos como TARGET:  
## **Precio de cierre dentro de 5 días (`Close.shift(-5)`)**

Esto es coherente con Swing Trading real.

---

# 🧠 3) ¿Qué tipo de TARGET recomiendo para tu modelo?

### 🤖 Mi recomendación profesional para tu proyecto:
## ⭐ **TARGET: Retorno porcentual en 5 días**  
```python
df["target"] = df["Close"].shift(-5) / df["Close"] - 1

✔️ Ventajas:

Es universal: no depende de la escala del precio

Facilita detectar señales de compra/venta

Permite definir reglas como:

“Comprar si el retorno esperado > 2%”

“Evitar operativas con riesgo alto”

Entrena mejor que el precio absoluto (menos ruido)

✔️ Para Swing Trading es el industry standard.

🟦 Mi recomendación final:

Usa como TARGET: retorno a 5 días (target_return_5d).
(Es el más sólido para estrategias de Swing ML y optimización futura.)

Pero si quieres comenzar con precio futuro (como elegiste), también es válido.
///////////////////////////////////////////////////////////


🧠 Qué incluye la Fase ML v1.2

Esta fase agrega 3 módulos fundamentales:

1️⃣ Feature Engineering Avanzado

Ya tenemos:

MA_5

MA_20

Return

Vamos a agregar indicadores técnicos clave para Swing Trading:

Indicador	Por qué importa
RSI	Identifica sobrecompra/sobreventa
MACD (MACD, Signal, Histogram)	Punto de giro y momentum
EMA 9, EMA 21	Tendencia de corto y medio plazo
Volatility (ATR o std dev)	Para ajustar el riesgo

Estos indicadores son esenciales porque Swing Trading se basa en:

📌 detectar momentos de giro,
📌 identificar inicio o agotamiento de tendencias,
📌 y anticipar movimientos de continuidad a 3-30 días.

2️⃣ Preparación del Dataset para ML

Crearemos:

X: Features

y: Target → Precio futuro en N días (por ejemplo +5 días)

Esto define tu tipo de modelo:

Regresor → estima precio futuro

Luego convertimos la predicción en señal: BUY / SELL / HOLD

3️⃣ Entrenador ML v1.2

Agregaré al módulo trainer.py:

Split Train/Test

Normalización opcional

Modelos iniciales:

RandomForestRegressor

GradientBoostingRegressor

Guardado automático del modelo entrenado

Logs en /Docs/Logs/MLLogs/

4️⃣ Validación del Modelo

Generará automáticamente:

MAE

RMSE

R²

Gráfico simple de pred vs real (si tú lo habilitas)

Y paso a paso podrás ver si el modelo es útil o no.

5️⃣ Infraestructura de Guardado

Se generará:

ml/models/
   model_v1_2.pkl
ml/reports/
   metrics_v1_2.json
Docs/Backups/ML/
   trainer_backup_<fecha>.py



////////////////////////////////////////

👉 ML v1.2.5 — Generación de señales BUY/SELL basadas en predicción.
👉 ML v1.3 — Optimizador inteligente del modelo (Optuna / Random Search)

/////////////////////

🔵 1) ML v1.3 — Optimización Automática del Modelo (Recomendado)

Usar:

Random Search

o Optuna

Para mejorar:

profundidad de árboles

nº estimadores

features importantes

curva de rendimiento

reducción de overfitting

maximizar R²

🔥 Esta etapa hace que tu modelo pase de “funciona” a “funciona bien”.

🟢 2) ML v1.2.5 — Generación de señales BUY/SELL

Basado en la predicción de retorno:

Predicted > 0.015 → BUY

Predicted < -0.01 → SELL

Sino → HOLD

Y crear:

ml/signals/signal_generator.py

🟣 3) ML v1.4 — Backtesting inicial

Simular resultado real con tu modelo:

Aciertos

MAE por período

Retorno acumulado

Drawdown

Comparación con buy-and-hold

///////////////////////////////////

🚀 PLAN EXACTO DE ML v1.3 – OPTUNA

A continuación te muestro cómo funcionará la optimización y luego te pregunto si quieres que te genere directamente el módulo + ZIP listo para usar.

🎛️ 1) ¿Qué optimizaremos con Optuna?

El modelo base sigue siendo:

RandomForestRegressor


Pero Optuna encontrará automáticamente:

Hiperparámetro	Rango
n_estimators	100 – 1000
max_depth	3 – 20
min_samples_split	2 – 20
min_samples_leaf	1 – 10
max_features	"sqrt", "log2"
bootstrap	True/False

Estos son hiperparámetros críticos en modelos financieros.

🎯 2) Qué intentará Optuna maximizar

Utilizaremos como objetivo:

maximize(R²)


¿Por qué R²?

Penaliza predicciones alejadas de la realidad

Tiene buena sensibilidad en modelos de regresión

Funciona muy bien en modelos sobre retornos futuros

⚙️ 3) Flujo interno de la optimización

Cada trial de Optuna hará:

Cargar dataset completo

Crear un modelo con hiperparámetros sugeridos por Optuna

Entrenarlo

Evaluar en test

Retornar R²

Optuna repetirá esto 50–200 veces (tú eliges), ajustando inteligentemente los parámetros.

📁 4) Archivos que vas a recibir

Cuando generemos ML v1.3 tendrás:

ml/optimization/optimize_model.py
ml/optimization/best_params.json
ml/models/model_v1_3_rfr_optuna.pkl
Docs/Logs/MLLogs/optuna_study.db
Docs/Backups/optimize_model_backup_<fecha>.py


Con eso podrás:

Ejecutar optimización

Analizar estudios

Guardar el mejor modelo

Comparar contra v1.2

🔥 5) Comando para ejecutar optimización

Desde la raíz del proyecto:

python -m ml.optimization.optimize_model


Y verás algo así:

[OPTUNA] Trial 1: R2=0.147
[OPTUNA] Trial 2: R2=0.163
[OPTUNA] Trial 3: R2=0.201
...
[OPTUNA] BEST R2 = 0.234 with params {...}
[OK] Best model saved to ml/models/model_v1_3_rfr_optuna.pkl

💾 6) Requisitos adicionales

Necesitas instalar Optuna en el .venv:

pip install optuna

🟦 CONFIRMACIÓN FINAL ANTES DE GENERAR TODO

Antes de generarte el módulo completo ML v1.3 con ZIP descargable, necesito una única confirmación:

❓ ¿Cuántos trials quieres que ejecute Optuna?
Opciones:

1️⃣ 50 trials → rápido (3–5 minutos)
2️⃣ 100 trials → equilibrio ideal
3️⃣ 200 trials → exhaustivo (más precisión)
4️⃣ Tú defines otro número

////////////////////////////////

⚠️ IMPORTANTE ANTES DE GENERAR EL MÓDULO

Necesito que confirmes DOS PUNTOS antes de generar el paquete ML v1.3:

✅ 1) ¿Quieres optimizar SOLO RandomForestRegressor, o deseas comparar también con GradientBoostingRegressor?

Opciones:

1️⃣ Solo RandomForest (más rápido y consistente)
2️⃣ Optimizar RFR + GradientBoosting (doble poder predictivo)
3️⃣ Optimizar RFR + GradientBoosting + ExtraTrees (muy potente)

Recomendación mía:
👉 Opción 2: RFR + GradientBoosting
Es estable, potente y no duplica el tiempo demasiado.

✅ 2) ¿Quieres que el objetivo de Optuna sea MAXIMIZAR:**

1️⃣ R² (recomendado, estándar en regresión financiera)
2️⃣ RMSE negativo (minimizar error)
3️⃣ MAE negativo (suaviza outliers)

Recomendación mía:
👉 1 — Maximizar R²
Es más estable para modelos que predicen retornos.

//////////////////////////////

🚀 SIGUIENTE ETAPA
ML v1.2.5 → Generación de Señales BUY / SELL / HOLD

Y luego:

ML v1.4 → Backtesting basado en señales
📌 ¿Qué es ML v1.2.5?

En esta etapa vamos a convertir las predicciones continuas del modelo en señales operativas reales, compatibles con tu objetivo Swing Trading.

🎯 OBJETIVO DE ML v1.2.5

Crear un módulo que:

Cargue el modelo entrenado (v1.2 o v1.3)

Prediga el retorno futuro a 5 días (target_return_5d)

Convierta la predicción en una señal:

BUY

SELL

HOLD

Calcule probabilidad o confianza

Genere un CSV con las señales ordenadas por ticker y fecha

📊 REGLAS DE DECISIÓN (propuestas por mí, puedes ajustar)
⭐ Versión recomendada para Swing Trading BR:
if predicted_return > 0.015:
    signal = "BUY"

elif predicted_return < -0.010:
    signal = "SELL"

else:
    signal = "HOLD"


Justificación:

+1.5% en 5 días → buena oportunidad swing

–1% en 5 días → riesgo significativo → señal de venta

Entre ambos → ruido → no operar

///////////////////////////////////////////////////////////

🧠 ¿Qué opción es mejor para el proyecto MT5_BOT?
📌 Respuesta clara y fundamentada:
👉 La mejor opción es la C — permitir usar ambos modelos, seleccionable por parámetro.
💡 Por qué esta es la opción profesional
1. La optimización (v1.3) no siempre supera al modelo base

Aunque Optuna mejora hiperparámetros, hay casos donde:

Datos ruidosos

Errores de mercado

Comportamientos no lineales

Cambios de régimen

hacen que un modelo optimizado tenga mejor R² pero peor comportamiento operativo (menor ganancia real).

En trading, ganar dinero es más importante que tener un R² alto.

Por eso debes poder comparar ambos.

2. Permite backtesting A/B

Para ML v1.4, podremos hacer:

Backtest con modelo v1.2

Backtest con modelo v1.3

Y comparar:

Retorno acumulado

Drawdown

Ratio de aciertos

Exposición

Sharpe-like

Rentabilidad por ticker

Esto es imposible si obligas al sistema a usar solo un modelo.

3. Evita dependencias innecesarias

Si el modelo v1.3 falla (por baja calidad de datos, ruido o overfitting), puedes volver al v1.2 en un clic.

////////////////////////////////////

✅ ¿Qué contiene este módulo?
1) ml/signals/signal_generator.py

Incluye:

Carga dinámica del modelo:

--model v1_2

--model v1_3

Predicción de target_return_5d

Reglas:

> 0.015 → BUY  
< -0.01 → SELL  
else → HOLD


Exportación de señales a:

ml/signals/generated_signals.csv


Log de generación a:

Docs/Logs/MLLogs/signal_generation_log.json

2) Backups automáticos

En:

Docs/Backups/signal_generator_backup_<fecha>.py

3) Estructura completa y limpia

Lista para integrar en tu repo GitHub.

🧪 Cómo usar ML v1.2.5
🔸 Usar modelo optimizado (por defecto):
python -m ml.signals.signal_generator

🔸 Elegir explícitamente modelo v1.3:
python -m ml.signals.signal_generator --model v1_3

🔸 Usar v1.2 (modelo base):
python -m ml.signals.signal_generator --model v1_2


////////////////////////////////////////

✅ 1) Vista Consolidada Lado a Lado (ML v1.2.6)

Este nuevo archivo:

ml/signals/signal_compare.py


Hará lo siguiente:

✔ Cargar ambos CSV generados:

generated_signals_v1_2_*.csv

generated_signals_v1_3_*.csv

✔ Unirlos por:

Date

Ticker

✔ Crear columnas comparativas:
pred_return_v1_2
pred_return_v1_3
signal_v1_2
signal_v1_3
signal_match   (boolean)
signal_diff    ("BUY→HOLD", "SELL→BUY", etc)

✔ Guardar salida:
ml/signals/signal_comparison_latest.csv

✔ Aplicaciones:

Detectar divergencias entre modelos

Ver cuál modelo es más agresivo o conservador

Elegir el “champion model” antes del backtesting

✅ 2) Agregar columna Ticker en cada archivo de señales

Ya detecté que tu pipeline sí tiene Ticker en merged_data, pero en el código de señales se pierde al recomponer X.

Voy a mejorar el generador:

📌 Implementación:

Antes de hacer X = X.reset_index()
→ vamos a reagrupar los tickers desde el dataset original

Añadiremos:
df["Ticker"] = df_original["Ticker"].values


Esto permitirá:

Filtrar señales por acción

Backtesting por activo individual

Evaluar precisión por ticker

Integrar correctamente con ML v1.4 (Backtesting)

El nuevo CSV tendrá:

Date | Ticker | predicted_return_5d | Signal | todas las features…

✅ 3) Automatizar ejecución con Windows Task Scheduler

Te prepararé un script .BAT y un .PS1 para programar tareas:

Archivos generados:
automation/run_signal_generation_v1_3.bat
automation/run_signal_generation_v1_3.ps1
automation/run_signal_generation_v1_2.bat
automation/run_signal_generation_v1_2.ps1

Ejemplo para modelo v1.3:

run_signal_generation_v1_3.bat:

@echo off
cd C:\MT5_BOT
call .venv\Scripts\activate
python -m ml.signals.signal_generator --model v1_3 --append

Uso en Task Scheduler:

Abrir Programador de tareas

Crear tarea -> “Nueva tarea básica”

Acción → “Iniciar un programa”

Programa →

C:\MT5_BOT\automation\run_signal_generation_v1_3.bat


Configurar frecuencia:

cada día

cada hora

cada 30 min

Resultado:

✔ Señales actualizadas automáticamente
✔ Histórico consolidado en generated_signals_master.csv
✔ Log automático con timestamp


/////////////////////////

🚀 SIGUIENTE PASO

Ahora sí estamos listos para:

ML v1.4 — Backtesting completo

Equity curve

Acertos

Rentabilidad

Drawdown

Comparación modelo v1.2 vs v1.3

Buy & Hold vs modelo

Estadísticas por ticker

Qué contiene (resumen)

ml/backtesting/backtest.py — backtester principal (batch over signal files, per-trade log, equity curve, report JSON).

ml/backtesting/README_BACKTEST.md — instrucciones de uso.

Estructura para guardar salidas en:

ml/backtesting/output/

Docs/Logs/Backtests/

Docs/Reports/

Cómo probarlo (rápido)

Asegúrate de tener señales en ml/signals/ (ideal: usar --append para crear generated_signals_master.csv).

Ejecuta (desde raíz del proyecto):

python -m ml.backtesting.backtest --signals ml/signals/generated_signals_master.csv --hold 5 --capital 10000 --commission 0.0 --slippage 0.0


Revisa:

ml/backtesting/output/trade_log_*.csv

ml/backtesting/output/equity_curve_*.csv

Docs/Reports/backtest_report_*.json

Notas importantes

Entradas asumidas: next-day Open; salidas: Close after hold days.

SELL signals are currently ignored (no shorting implemented). We can add short support later.

The module is designed to be simple, auditable and fast to run locally. For large-scale simulations or intraday logic, we'll need more advanced market modeling.


