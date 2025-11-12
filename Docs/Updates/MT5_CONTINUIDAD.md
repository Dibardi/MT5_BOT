# 🧭 MT5_CONTINUIDAD — Registro Interno de Avances

- [2025-11-12] Versión 1.1 del módulo `ml/training/`: implementado entrenamiento real con RandomForestRegressor, cálculo de métricas, guardado de modelo `.pkl` y reporte JSON automático.
- [2025-11-12] Versión 1.1.1 de `trainer.py`: corregida la lectura del archivo CSV para manejar índices de fechas sin modificar la estructura del pipeline ni romper compatibilidad.
- [2025-11-12] Versión 1.1.2 del módulo `ml/training/`: corregido manejo de features para evitar pasar columnas no numéricas a sklearn.
- [2025-11-12] Versión 1.1.3 del módulo `ml/training/`: compatibilidad RMSE y corrección de mensajes (prints f-strings evaluables).
