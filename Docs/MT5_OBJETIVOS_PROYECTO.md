# 🎯 MT5_OBJETIVOS_PROYECTO — Proyecto MT5_BOT

P25-11-11

## 1. Visión del usuario (Luis)
Desarrollar un **robot de trading automatizado** que sea capaz de **aprender y predecir** para operar en **MetaTrader5**, con el objetivo de **ganar dinero con poca inversión** y **minimizar pérdidas**, siempre priorizando la rentabilidad. El enfoque es **swing trading** aplicado al **mercado bursátil fraccionario de Brasil (B3)**, utilizando **Python** como lenguaje principal. El bot será **semiautónomo** (requiere confirmación humana antes de ejecutar operaciones reales).

---

## 2. Resumen ejecutivo de la estrategia de desarrollo
- Desarrollo **modular** y **paso a paso** (ml/, risk/, execution/, backtest/, infra/).  
- Implementación en **2 fases**:
  1. **Fase 1 — Aprendizaje Predictivo Estático** (recomendado como inicio): modelos tradicionales (LightGBM, RandomForest, Logistic Regression) entrenados offline; señales generadas y validadas manualmente.  
  2. **Fase 2 — Aprendizaje Adaptativo (Avanzado)**: entrenamiento incremental, reentrenamiento automatizado controlado, retroalimentación de ejecución y posible ajuste dinámico de hiperparámetros.

---

## 3. Recomendación sobre HLS
> Nota: la sigla **HLS** se refiere a **Hyper Latin Cube Sampling**, una técnica de muestreo estadístico avanzado útil para la optimización de hiperparámetros en modelos de Machine Learning.

### ¿Qué es Hyper Latin Cube Sampling (HLS)?
**Hyper Latin Cube Sampling (HLS)** es una extensión multidimensional del *Latin Hypercube Sampling (LHS)*. Es una técnica de muestreo estratificado que cubre uniformemente el espacio de parámetros para seleccionar combinaciones representativas sin tener que evaluar todas las combinaciones posibles (como en Grid Search).

### ¿Por qué usar HLS en MT5_BOT?
- Permite una exploración eficiente del espacio de hiperparámetros para modelos como LightGBM, RandomForest o XGBoost.  
- Cubre el espacio de búsqueda de manera más uniforme que el muestreo aleatorio, mejorando la probabilidad de encontrar buenas configuraciones.  
- Reduce el costo computacional frente a Grid Search, facilitando la experimentación en equipos locales (tu PC Ryzen).  
- Facilita la reproducibilidad mediante control de semilla y es compatible con marcos de optimización avanzados (Optuna, Bayesian Optimization).

### Integración propuesta
- Añadir un submódulo en `ml/` llamado `hyperparameter_optimization/` con un script `hls_optimizer.py`.  
- El optimizador HLS generará muestras de configuraciones, evaluará modelos con validación temporal (walk-forward) y registrará resultados en `/Docs/Updates/MT5_RESPUESTA_IA.md`.  
- Mantener la trazabilidad de experimentos y permitir re-ejecución reproducible con la misma semilla.

---

---

## 4. Características técnicas recomendadas (Fase 1)
- **Modelos sugeridos:** LightGBM, RandomForest, Logistic Regression (baseline).  
- **Features / Señales:** precios, retornos, volumen, medias móviles, RSI, MACD, ATR, Bollinger Bands, y **High-Level Signals (HLS)** agregadas.  
- **Target / Horizonte:** probabilidades de movimiento en 2–10 días (swing).  
- **Entrenamiento:** offline, con validación temporal (walk-forward) y separación estricta train/validation/test por tiempo.  
- **Validación y métricas:** Sharpe ratio estimado, Profit factor, max drawdown, precision/recall sobre señales, simulaciones de cartera.  
- **Infraestructura:** pipelines reproducibles (scripts), almacenamiento de datasets, notebooks de experimentación, logs de entrenamiento y versiones del modelo.

---

## 5. Operación y control (modo semiautónomo)
- **Generación de señal:** el ML sugiere probabilidades y señales; el operador valida (confirmación manual) antes de ejecución.  
- **Reglas de ejecución automáticas opcionales:** en fases futuras se puede permitir ejecución parcial automática bajo condiciones estrictas (por ejemplo, cuando varias señales HLS convergen y el riesgo calculado está por debajo de un umbral).  
- **Gestión de riesgo:** tamaño de posición dinámico basado en volatilidad (ATR) y límite de exposición total; stop loss y trailing stop integrados.  
- **Monitoreo:** dashboards y alertas sobre rendimiento y drawdown.

---

## 6. Roadmap técnico (alto nivel)
1. **Infra & Datos:** pipeline de descarga y almacenamiento de históricos B3 (ajustar a fraccionario).  
2. **Features & HLS:** construir featurization y reglas de HLS.  
3. **Modelos & Backtesting:** prototipar modelos offline y ejecutar backtests.  
4. **Integración MT5:** adaptar conectores y gestión de órdenes (modo semiautónomo).  
5. **Validación en demo / paper trading:** operar en entorno simulado.  
6. **Evolución a Fase 2:** habilitar reentrenamiento controlado y automatización gradual.

---

## 7. Documentos relacionados (en el repositorio)
- `/Docs/HARDWARE.md` — especificaciones de equipos.  
- `/Docs/Implementations/MT5_IMPLEMENTACION_002.md` — implementación #2 (hardware docs).  
- `/Docs/MT5_GUIA_DESARROLLO_MODULAR.md` — guía de trabajo modular.  
- `/Docs/Updates/MT5_CONTINUIDAD.md` — historial de acciones.  
- `/Docs/Updates/MT5_RESPUESTA_IA.md` — decisiones y análisis IA.

---

## 8. Próximos pasos propuestos (puedo ejecutar ahora si confirmas)
- Crear estructura de carpetas esqueleto (ml/, risk/, execution/, backtest/, infra/).  
- Implementar pipeline de datos históricos (descarga B3).  
- Construir primer set de features y HLS.  
- Entrenar primer modelo LightGBM y generar report inicial de backtest.

Si confirmas, creo **/Docs/MT5_OBJETIVOS_PROYECTO.md** (ya generado) y procedo con el siguiente paso que elijas.

---

> Si quieres que cambie alguna redacción o amplíe un apartado, lo edito y actualizo el archivo inmediatamente.
