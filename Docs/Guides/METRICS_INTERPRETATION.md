# 📊 Interpretación de Métricas del Modelo — Proyecto MT5_BOT

**Versión:** 1.0  
**Autor:** GPT-5 & Luis Longobardi  
**Fecha:** 2025-11-12

---

## 🎯 Objetivo

Este documento explica cómo interpretar las métricas generadas por el módulo de entrenamiento `ml/training/`, almacenadas en:
```
Docs/Logs/MLLogs/training_report.json
```

Las métricas clave (`MAE`, `RMSE`, `R²`) permiten evaluar la precisión, estabilidad y confiabilidad del modelo predictivo.

---

## 🧮 1️⃣ MAE — Mean Absolute Error (Error Absoluto Medio)

### 📘 Definición
Promedio de la diferencia absoluta entre el retorno real y el predicho.

\[
MAE = \frac{1}{n} \sum |Y_{real} - Y_{predicho}|
\]

### 📈 Interpretación
- **Valor bajo** = predicciones más precisas.
- **Valor alto** = mayor margen de error.

### 💡 En trading
Si el retorno promedio diario es ±1%, un **MAE < 0.001 (0.1%)** indica un modelo altamente preciso.

| Rango | Interpretación |
|--------|----------------|
| 🟢 `MAE < 0.001` | Excelente precisión |
| 🟡 `0.001 ≤ MAE < 0.01` | Aceptable |
| 🔴 `MAE ≥ 0.01` | Error alto, revisar datos o modelo |

---

## 📉 2️⃣ RMSE — Root Mean Squared Error (Raíz del Error Cuadrático Medio)

### 📘 Definición
Medida del error cuadrático medio, penaliza más los errores grandes.

\[
RMSE = \sqrt{\frac{1}{n} \sum (Y_{real} - Y_{predicho})^2}
\]

### 📈 Interpretación
- Indica estabilidad del modelo.  
- Si `RMSE ≈ MAE`, el modelo es consistente.  
- Si `RMSE ≫ MAE`, el modelo tiene fallas ante valores extremos.

| Rango | Interpretación |
|--------|----------------|
| 🟢 `RMSE < 0.002` | Modelo estable |
| 🟡 `0.002 ≤ RMSE < 0.01` | Aceptable |
| 🔴 `RMSE ≥ 0.01` | Inestabilidad, revisar profundidad o outliers |

---

## 🧠 3️⃣ R² — Coeficiente de Determinación

### 📘 Definición
Proporción de variabilidad del retorno que el modelo logra explicar.

\[
R^2 = 1 - \frac{SS_{res}}{SS_{tot}}
\]

### 📈 Interpretación
- `R² = 1.0` → El modelo explica todo el comportamiento (perfecto).  
- `R² = 0` → No explica nada.  
- `R² < 0` → Peor que adivinar.

| Rango | Interpretación |
|--------|----------------|
| 🟢 `R² ≥ 0.9` | Excelente capacidad predictiva |
| 🟡 `0.7 ≤ R² < 0.9` | Aceptable, requiere más variables |
| 🔴 `R² < 0.7` | Débil, necesita rediseño o más features |

---

## 📘 4️⃣ Conclusión rápida

| Métrica | Tipo de error | Qué mide | Valor ideal |
|----------|----------------|-----------|--------------|
| **MAE** | Error medio | Precisión diaria | `< 0.001` |
| **RMSE** | Error ponderado | Estabilidad | `< 0.002` |
| **R²** | Coeficiente de determinación | Potencia predictiva | `> 0.9` |

Si obtienes:
```
MAE < 0.001 | RMSE < 0.002 | R² > 0.9
```
➡️ Tu modelo es **sólido y confiable para predecir tendencias de precios**.

---

## 🧭 5️⃣ Qué hacer si las métricas no son buenas

| Problema | Causa posible | Solución sugerida |
|-----------|----------------|------------------|
| `MAE` y `RMSE` altos | Datos ruidosos o pocos árboles | Aumentar `n_estimators` o limpiar datos |
| `R²` bajo | Falta de variables predictivas | Añadir RSI, MACD, volatilidad, etc. |
| Overfitting (`R²=1.0` en train, bajo en test) | Modelo demasiado complejo | Reducir `max_depth` o usar `cross-validation` |

---

## 💹 6️⃣ Relación con decisiones de trading

El modelo predice **el retorno futuro esperado**, no las órdenes de compra o venta.  
El bot usa esas predicciones dentro de la lógica operativa:

```python
if predicted_return > 0.002:
    abrir_compra()
elif predicted_return < -0.002:
    abrir_venta()
else:
    mantener_posicion()
```

Estas reglas convierten las métricas cuantitativas en **acciones de trading concretas**.

---

## 🧩 7️⃣ Recomendaciones generales

- Reentrena el modelo cada 2–4 semanas con datos nuevos.  
- Analiza el log de métricas tras cada entrenamiento.  
- Guarda siempre los modelos `.pkl` y sus reportes JSON asociados.  
- Usa `R²`, `MAE` y `RMSE` juntos, nunca de forma aislada.

---

📘 *Este documento forma parte de la documentación técnica del proyecto MT5_BOT.  
Ubicación recomendada: `/Docs/Guides/METRICS_INTERPRETATION.md`*
