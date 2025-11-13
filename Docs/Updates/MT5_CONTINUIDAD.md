# 🧭 MT5_CONTINUIDAD — Registro Interno de Avances

- [2025-11-12] Versión 1.1 del módulo `ml/training/`: implementado entrenamiento real con RandomForestRegressor, cálculo de métricas, guardado de modelo `.pkl` y reporte JSON automático.
- [2025-11-12] Versión 1.1.1 de `trainer.py`: corregida la lectura del archivo CSV para manejar índices de fechas sin modificar la estructura del pipeline ni romper compatibilidad.
- [2025-11-12] Versión 1.1.2 del módulo `ml/training/`: corregido manejo de features para evitar pasar columnas no numéricas a sklearn.
- [2025-11-12] Versión 1.1.3 del módulo `ml/training/`: compatibilidad RMSE y corrección de mensajes (prints f-strings evaluables).
- [2025-11-12] Versión 1.8.4 del módulo `infra/fetch_b3_data.py/`: descarga correcta via yfinance, indice date en formato iso, logs de ejecucion automaticos
- [2025-11-12] Versión 1.8.4 del módulo `infra/date_pipeline.py/`: lectura robusta de CSVs, conversion numerica segura, features generados, exportacion con indice datetime, metadatos sincronizados, sin errores, solo warning benigno de inferencia de panda
- [2025-11-12] Versión 1.8.4 del módulo `ml/training/model_check.py`: vaida integridad de datos, sin errores, funciona correctamente con pipeline 1.8.4