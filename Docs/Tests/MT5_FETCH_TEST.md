# 🧪 Prueba controlada — fetch_b3_data (guía paso a paso)

**Última actualización:** 2025-11-11

Este documento explica paso a paso cómo ejecutar la **prueba corta** del módulo `infra/fetch_b3_data.py` asegurando que **todos los archivos descargados queden dentro de la carpeta del proyecto MT5_BOT**.

---

## 1) Requisitos previos (resumen)
- Tener Python 3.10+ instalado.  
- Abrir una terminal en la **carpeta raíz del proyecto** (donde existe la carpeta `infra/`).  
- Instalar dependencias (recomendado en un virtualenv):
```bash
python -m venv .venv
source .venv/bin/activate        # Linux / WSL
.venv\Scripts\activate         # Windows PowerShell
pip install --upgrade pip
pip install pandas yfinance joblib tqdm
```

> **IMPORTANTE:** Ejecutar los comandos desde la carpeta raíz del proyecto garantiza que las rutas relativas (`./infra/data/`) se resuelvan dentro de `MT5_BOT`. Además, el módulo ha sido ajustado para resolver rutas relativas con seguridad incluso si se ejecuta desde otra carpeta.

---

## 2) Confirmar ruta de almacenamiento (opcional)
El archivo de configuración `infra/config_data.json` contiene la ruta de almacenamiento por defecto:
```json
{
  "data_source": "yfinance",
  "storage_path": "./infra/data/",
  "update_frequency": "daily"
}
```
El código ahora resuelve `./infra/data/` respecto al **directorio raíz del proyecto**, por lo que todos los CSV se guardarán dentro de la carpeta `MT5_BOT/infra/data/` independientemente de la carpeta de ejecución.

---

## 3) Ejecutar la prueba corta (comando recomendado)
Desde la carpeta raíz del proyecto ejecuta (ejemplo de 30 días):
```bash
python infra/fetch_b3_data.py --tickers PETR4.SA VALE3.SA --start 2024-10-10 --end 2024-11-10 --interval 1d --n_jobs 4
```
Parámetros que puedes ajustar:
- `--tickers`: lista de tickers B3 (ej. PETR4.SA)  
- `--start` / `--end`: periodo en `YYYY-MM-DD`  
- `--interval`: `1d`, `1wk`, `60m`, etc.  
- `--n_jobs`: nivel de paralelismo (recomendado 4 en Ryzen 2700X)  

---

## 4) Verificar resultados
1. Revisa la carpeta `infra/data/` dentro del proyecto: deberías encontrar archivos `.csv` nombrados como `PETR4_SA_1d_2024-10-10_2024-11-10.csv`.  
2. Abre el CSV con Excel/VSCode para confirmar columnas: `Open, High, Low, Close, Adj Close, Volume`.  
3. En la terminal deberías ver mensajes `Downloaded X rows for TICKER ... Saved to ...`.

---

## 5) Transferir datos entre equipos (Ryzen → Notebook)
Para mover datos del proyecto entre máquinas, copia **únicamente** la carpeta `infra/data/` o empaqueta el proyecto entero `MT5_BOT/infra/data/`:
- Empaquetar y copiar (Windows PowerShell):
```powershell
Compress-Archive -Path .\infra\data\* -DestinationPath MT5_data_pack.zip
```
- En Linux/WSL:
```bash
zip -r MT5_data_pack.zip infra/data/
```
Luego lleva `MT5_data_pack.zip` al otro equipo y extrae dentro del mismo proyecto (`MT5_BOT/infra/data/`) para mantener rutas idénticas.

---

## 6) Buenas prácticas
- Ejecuta pruebas inicialmente con `--n_jobs 1` si no estás seguro de la carga del sistema.  
- Usa el SSD del proyecto para datasets (por ejemplo `infra/data/` en SSD 1TB).  
- Mantén backups periódicos de `infra/data/` en el HDD externo o en cloud.  
- Si ejecutas en Windows, considera WSL2 para mayor compatibilidad POSIX.

---

## 7) Soporte y seguimiento
Cuando ejecutes la prueba, copia aquí los logs de la consola (o una captura rápida) y te ayudaré a interpretar tiempos, tamaños y cualquier alerta.  
Si quieres que ejecute la prueba **aquí** en el entorno sandbox, confírmalo explícitamente (ten en cuenta que la sandbox no tiene conexión a internet).

---

> Esta guía garantiza que **todos los datos** descargados por `fetch_b3_data.py` queden **dentro de la carpeta MT5_BOT**, facilitando la portabilidad entre tus equipos y manteniendo orden y trazabilidad.
