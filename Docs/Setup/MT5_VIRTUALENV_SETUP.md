# 🧱 Configuración de entorno virtual (virtualenv) — Proyecto MT5_BOT

**Última actualización:** 2025-11-11

Esta guía documenta el procedimiento oficial para crear, mantener y transferir entornos virtuales del proyecto **MT5_BOT**, garantizando trazabilidad y consistencia entre equipos.

---

## 🧭 1) Ubicación recomendada del proyecto
Coloca el proyecto en una carpeta estable, por ejemplo:
```
D:\MT5_BOT\
```
o
```
C:\Users\Luis\Documents\MT5_BOT\
```

Asegúrate de que la estructura del proyecto sea la siguiente:
```
MT5_BOT/
├─ infra/
│   ├─ fetch_b3_data.py
│   ├─ config_data.json
│   └─ data/
└─ Docs/
    └─ Setup/
        └─ MT5_VIRTUALENV_SETUP.md
```

---

## ⚙️ 2) Crear el entorno virtual

### En Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### En Linux o WSL
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Si el entorno se activó correctamente, el prompt mostrará algo como:
```
(.venv) D:\MT5_BOT>
```

---

## 📦 3) Instalar dependencias necesarias
Con el entorno activado, ejecuta:
```bash
pip install --upgrade pip
pip install pandas yfinance joblib tqdm
```

Estas librerías son suficientes para realizar las pruebas iniciales del módulo `fetch_b3_data.py`.

---

## 🧪 4) Ejecutar prueba de descarga (fetch_b3_data)
Desde la carpeta raíz del proyecto:
```bash
python infra/fetch_b3_data.py --tickers PETR4.SA VALE3.SA --start 2024-10-10 --end 2024-11-10 --interval 1d --n_jobs 4
```

Los archivos CSV descargados se guardarán automáticamente en:
```
MT5_BOT/infra/data/
```

Verifica los archivos generados (por ejemplo, `PETR4_SA_1d_2024-10-10_2024-11-10.csv`).

---

## 💾 5) Cierre y reactivación del entorno
Para salir del entorno virtual:
```bash
deactivate
```

Para volver a activarlo:
```bash
.venv\Scripts\activate
```

---

## 🔁 6) Transferencia del proyecto a otro equipo
Copia el proyecto completo `MT5_BOT/` (sin necesidad de incluir `.venv`).  
En el nuevo equipo:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

(El archivo `requirements.txt` será generado automáticamente más adelante).

---

## 🧩 Confirmación
Cuando el entorno esté listo y las dependencias instaladas, puedes ejecutar las pruebas o continuar con el desarrollo modular.

---

📘 Esta guía forma parte del registro técnico del proyecto y asegura reproducibilidad y consistencia entre los entornos de desarrollo (Ryzen y Notebook).
