# 🧠 MT5_RESPUESTA_IA — Análisis y Decisiones Técnicas


## 🧠 Actualización de Hardware y Estrategia de Cómputo — 2025-11-11

Tras la incorporación del perfil técnico completo del **Notebook Intel i5‑9300H** junto al **PC Ryzen 7 2700X**, se realizó un análisis comparativo de recursos y distribución de tareas de cómputo para el proyecto **MT5_BOT**.

### 🔍 Evaluación Técnica
- El **Ryzen 7 2700X** (8 núcleos / 16 hilos, 64 GB RAM) ofrece rendimiento óptimo en entrenamiento ML por CPU.
- Las GPUs disponibles (**GTX 980 Ti y GTX 1050**) son útiles, pero no esenciales para la carga de trabajo actual.
- El **Notebook i5‑9300H** (4 núcleos / 8 hilos, 24 GB RAM) cumple perfectamente como estación de testing y validación.

### 🧭 Decisión IA
1. **Priorizar CPU como motor principal** para entrenamiento, optimización y backtesting.  
2. **Definir GPU como recurso opcional**, solo para experimentación o inferencia acelerada.  
3. **Distribuir roles**:  
   - *PC Ryzen*: entrenamiento, optimización, simulación.  
   - *Notebook i5*: testing, validación, monitoreo.  

### ⚙️ Recomendaciones técnicas asociadas
- Configurar `n_jobs=8–12` en Ryzen para Optuna / LightGBM / Scikit-learn.  
- Usar `n_jobs=4` en Notebook para tareas ligeras.  
- Evitar uso simultáneo de múltiples GPUs.  
- Mantener datasets y modelos en SSD principal.

📘 Esta decisión asegura **estabilidad, eficiencia y reproducibilidad** durante las fases iniciales de entrenamiento ML y backtesting del proyecto.

---

## 🧠 Creación de Estructura Modular — 2025-11-11

Se implementó el **esqueleto base del proyecto MT5_BOT** conforme a la Guía de Desarrollo Modular.  
La estructura creada incluye los módulos principales (`ml/`, `risk/`, `execution/`, `backtest/`, `infra/`) y la documentación `MT5_IMPLEMENTACION_003.md`.

### 🔹 Decisiones técnicas
- Se mantiene el enfoque modular y escalable.  
- CPU es el motor principal de ejecución (coherente con hardware disponible).  
- GPU permanece opcional.  
- Se documentan los primeros scripts del módulo `infra/` para manejo de datos (fetch, pipeline, configuración).

📘 Este cambio marca el inicio formal del desarrollo técnico del proyecto.

## 🧠 Implementación fetch_b3_data — 2025-11-11

Se creó el módulo `infra/fetch_b3_data.py` con funciones para descargar datos B3 usando yfinance, gestionar caching en CSV y paralelizar descargas respetando recursos. El diseño prioriza CPU y evita saturar la máquina. Se registró en continuidad.

## 🧠 Ajuste de fetch_b3_data — 2025-11-11

Se adaptó `ensure_data_dir` en `infra/fetch_b3_data.py` para resolver rutas relativas respecto al root del proyecto y así garantizar que todos los datos descargados queden dentro de `MT5_BOT/infra/data/`. Se agregó la guía de prueba `Docs/Tests/MT5_FETCH_TEST.md`.
