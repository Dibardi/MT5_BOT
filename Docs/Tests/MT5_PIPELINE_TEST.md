# 🧪 MT5_PIPELINE_TEST.md — Guía de Validación del Módulo data_pipeline.py

**Fecha:** 2025-11-11  
**Versión:** 1.0  
**Objetivo:** Validar la correcta ejecución, limpieza y normalización de los datos procesados por `infra/data_pipeline.py`.

---

## 🧭 1️⃣ Preparación
Antes de ejecutar las pruebas, asegúrate de:
- Tener datos descargados en `infra/data/` (archivos `.csv` generados por `fetch_b3_data.py`).
- Haber activado tu entorno virtual (`.venv`).
- Ejecutar el comando:
  ```bash
  python infra/data_pipeline.py
  ```

Esto generará los archivos:
```
infra/processed/merged_data.csv
infra/processed/metadata_summary.json
```

---

## ⚙️ 2️⃣ Verificación del archivo merged_data.csv

Abre el archivo `infra/processed/merged_data.csv` con Excel, VSCode o Pandas.

### Comprueba:
| Validación | Descripción | Resultado esperado |
|-------------|--------------|--------------------|
| **Filas totales** | Coinciden con la suma de los CSV de `infra/data/`. | ✅ |
| **Columnas** | Deben incluir: `Open, High, Low, Close, Adj Close, Volume, Ticker, Return, MA_5, MA_20`. | ✅ |
| **Duplicados** | No deben existir filas repetidas. | ✅ |
| **Fechas** | Todas entre `2018-01-01` y `hoy`. | ✅ |
| **Valores nulos (NaN)** | Solo los primeros días de MA_5 y MA_20 pueden tener NaN. | ⚠️ Aceptable |
| **Orden cronológico** | Fechas ordenadas ascendentemente. | ✅ |

> Si detectas que faltan columnas o hay valores fuera de rango, revisa las funciones `clean_data()` y `normalize_data()` en `infra/data_pipeline.py`.

---

## 📊 3️⃣ Verificación de metadatos

Abre el archivo `infra/processed/metadata_summary.json` y revisa:

Ejemplo de contenido esperado:
```json
{
  "total_rows": 19500,
  "tickers": 10,
  "start_date": "2018-01-02",
  "end_date": "2025-11-11"
}
```

### Comprueba:
| Campo | Descripción | Resultado esperado |
|--------|--------------|--------------------|
| **total_rows** | Suma total de filas en merged_data.csv. | ✅ |
| **tickers** | Debe coincidir con el número de activos en `config_data.json`. | ✅ |
| **start_date / end_date** | Rango coherente con los CSV descargados. | ✅ |

---

## 🔎 4️⃣ Validaciones adicionales (opcional)

Puedes usar estos comandos en la consola de Python:

```python
import pandas as pd
df = pd.read_csv("infra/processed/merged_data.csv", parse_dates=["Date"], index_col="Date")
print(df.groupby("Ticker")["Return"].describe())
```

### Qué observar:
- Retornos medios cercanos a 0 (no extremadamente altos).  
- Columnas `MA_5` y `MA_20` con valores crecientes y sin huecos grandes.  
- No debe haber NaN fuera de los primeros 20 registros por ticker.

---

## ✅ 5️⃣ Resultado esperado

Si todas las verificaciones anteriores se cumplen:
> El pipeline de datos está **completamente validado** y listo para integrarse con el módulo de **Machine Learning (ml/)**.

---

📘 *Esta guía forma parte de la documentación técnica de pruebas del Proyecto MT5_BOT.*
