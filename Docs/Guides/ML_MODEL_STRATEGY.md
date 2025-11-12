# 🧠 Estrategia de Aprendizaje y Predicción — Proyecto MT5_BOT

**Versión:** 1.0  
**Autor:** GPT-5 & Luis Longobardi  
**Fecha:** 2025-11-12

---

## 🎯 Objetivo del modelo predictivo

El modelo predictivo del proyecto **MT5_BOT** tiene como finalidad detectar **oportunidades de compra y venta de acciones** en el mercado bursátil brasileño, buscando **comprar barato y vender caro** dentro de una ventana temporal de swing trading.

Su meta es **anticipar la dirección y magnitud del movimiento del precio**, utilizando aprendizaje automático (Machine Learning) para analizar patrones históricos de precios y volumen.

---

## 🧭 1️⃣ Enfoque general

El modelo no “sabe” de economía ni de estrategias humanas.  
Aprende **patrones estadísticos** de los datos del mercado.  
Su inteligencia consiste en reconocer combinaciones de indicadores que históricamente preceden subidas o bajadas de precio.

| Fase | Descripción |
|------|--------------|
| **Análisis** | Estudia tendencias, volumen y comportamiento reciente del precio. |
| **Predicción** | Estima si el retorno futuro (Return) será positivo o negativo. |
| **Decisión** | Si el modelo predice subida → comprar; si predice bajada → vender o esperar. |

---

## 🧩 2️⃣ Datos utilizados por el modelo

El modelo aprende a partir de los **datos procesados por el pipeline (`merged_data.csv`)**,  
que contienen variables derivadas de análisis técnico (features) y retornos históricos (target).

### 🔹 Features (entradas del modelo)
| Variable | Descripción | Interpretación |
|-----------|--------------|----------------|
| **MA_5** | Media móvil de 5 días | Tendencia de corto plazo. |
| **MA_20** | Media móvil de 20 días | Tendencia de mediano plazo. |
| **Volume** | Volumen negociado | Fuerza o debilidad del movimiento. |
| *(futuras features)* | RSI, MACD, Volatilidad, cruces de medias, etc. | Indicadores adicionales que mejoran la predicción. |

### 🔸 Target (variable objetivo)
El modelo intenta predecir el **retorno porcentual futuro** del precio:

```
Return = (Precio_actual - Precio_anterior) / Precio_anterior
```

| Día | Precio | Return | Acción sugerida |
|-----|---------|---------|-----------------|
| Lunes | 10.00 | — | — |
| Martes | 10.30 | +3.0% | Comprar o mantener |
| Miércoles | 9.80 | -4.8% | Vender o evitar entrada |

---

## 🧠 3️⃣ Cómo aprende el modelo

Durante el entrenamiento, el modelo analiza cada registro histórico (día, features, retorno)  
y ajusta sus parámetros internos para predecir correctamente el retorno futuro.

En el caso de **RandomForestRegressor**, el algoritmo crea múltiples árboles de decisión que aprenden reglas como:

> “Si MA_5 > MA_20 y el volumen sube, el retorno siguiente tiende a ser positivo.”

Después de miles de iteraciones, el modelo aprende patrones generalizables sobre cuándo el precio tiende a subir o bajar.

---

## 📊 4️⃣ Cómo se usa la predicción

El modelo no toma decisiones de trading por sí solo:  
su salida se convierte en **una señal de acción** para el módulo operativo del bot.

| Predicción del modelo | Acción del bot | Objetivo |
|------------------------|----------------|-----------|
| `Return_predicho > 0` | Comprar o mantener posición | Capturar subida |
| `Return_predicho < 0` | Vender o no abrir posición | Evitar pérdida |
| `Return_predicho ≈ 0` | Esperar | Evitar operaciones sin ventaja |

El sistema puede aplicar un **umbral de confianza**, por ejemplo:
> “Solo comprar si la probabilidad de subida supera el 70 %.”

---

## 🔄 5️⃣ Ciclo de aprendizaje y decisión

```
📊 Datos históricos (pipeline)
      ↓
🧠 Modelo ML (RandomForest)
      ↓
📈 Predicción de Return futuro
      ↓
🤖 Lógica de trading
      ├─ Si Return > 0 → COMPRAR
      ├─ Si Return < 0 → VENDER
      └─ Si Return ≈ 0 → ESPERAR
```

---

## ⚙️ 6️⃣ Próximas mejoras planificadas

| Versión | Mejora | Objetivo |
|----------|---------|----------|
| **v1.2** | Incorporar indicadores RSI, MACD, volatilidad | Mejorar sensibilidad a momentum. |
| **v1.3** | Clasificador binario (Sube/Baja) | Decisiones más discretas. |
| **v1.4+** | Aprendizaje por refuerzo (Reinforcement Learning) | El bot aprende de su propio rendimiento (recompensa = lucro). |

---

## 💡 Conclusión

El modelo predictivo es la base estadística del bot.  
Analiza el comportamiento de los precios y genera señales cuantitativas.  
Estas señales alimentarán la **lógica de ejecución** en MetaTrader5,  
donde el bot decidirá si abrir, mantener o cerrar una posición.

> En resumen:
> - 🔹 El modelo **aprende** de los datos.  
> - 🔹 Tú defines las **reglas operativas**.  
> - 🔹 El bot ejecuta las **acciones** buscando la mayor rentabilidad con el menor riesgo.

---

📘 *Este documento forma parte de la documentación técnica de inteligencia predictiva del proyecto MT5_BOT.  
Ubicación recomendada: `/Docs/Guides/ML_MODEL_STRATEGY.md`*
