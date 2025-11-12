# ⚙️ MT5_IMPLEMENTACION_003 — Infraestructura de Datos (Módulo `infra/`)

**Fecha de creación:** 2025-11-11  
**Versión:** 1.0  
**Estado:** 🟢 Completado (Esqueleto base creado)

---

## 🧭 Objetivo
Establecer la **infraestructura base del módulo `infra/`** para el manejo de datos históricos del mercado bursátil brasileño (B3).  
Este módulo será responsable de **descargar, limpiar, normalizar y almacenar** datos utilizados por los modelos de predicción y backtesting.

---

## 📁 Estructura creada
```
infra/
├─ fetch_b3_data.py        → descarga de datos históricos (B3)
├─ data_pipeline.py        → procesamiento y normalización de datos
├─ config_data.json        → configuración de rutas y frecuencia de actualización
└─ __init__.py             → inicialización del módulo
```

---

## 🧩 Descripción técnica
- `fetch_b3_data.py`: contendrá las funciones para conectar con APIs o fuentes de datos (B3, Yahoo Finance, etc.).  
- `data_pipeline.py`: gestionará limpieza, feature engineering y validaciones.  
- `config_data.json`: define parámetros globales (fuente de datos, paths, intervalos).  
- Todo el módulo será accesible mediante `import infra` dentro del proyecto principal.

---

## 🧠 Próximos pasos
1. Implementar la función `fetch_b3_data()` con conexión a datos reales (API B3, CSV, o Yahoo Finance).  
2. Desarrollar la función `normalize_data()` en `data_pipeline.py`.  
3. Crear validaciones de integridad de datos y registro de logs.  
4. Integrar con el módulo `ml/` para entrenamiento de modelos.

---

📘 Este módulo cumple con la Guía de Desarrollo Modular y constituye la **base del pipeline de datos** del proyecto MT5_BOT.
