# ⚙️ Guía de Configuración de Visual Studio Code para el Proyecto MT5_BOT

**Versión:** 1.0  
**Autor:** GPT-5 & Luis Longobardi  
**Fecha:** 2025-11-12

---

## 🧭 Objetivo

Esta guía detalla cómo configurar **Visual Studio Code (VS Code)** para trabajar correctamente con el proyecto **MT5_BOT**, incluyendo extensiones, entorno virtual, ejecución y depuración.

---

## 🧩 1️⃣ Requisitos previos

- Python 3.11+ instalado y agregado al PATH  
  Verifica desde PowerShell o CMD:
  ```bash
  python --version
  ```

- Visual Studio Code instalado desde:  
  👉 [https://code.visualstudio.com/](https://code.visualstudio.com/)

- Carpeta del proyecto ubicada en:
  ```
  C:\MT5_BOT\
  ```

---

## 🧱 2️⃣ Extensiones esenciales

Instala las siguientes extensiones desde el panel (`Ctrl + Shift + X`):

| Extensión | Autor | Descripción |
|------------|--------|--------------|
| Python | Microsoft | Soporte completo para ejecución, linting y debugging de Python. |
| Pylance | Microsoft | Autocompletado inteligente y análisis de código. |
| Jupyter | Microsoft | Permite ejecutar notebooks `.ipynb`. |
| Code Runner *(opcional)* | Jun Han | Ejecuta scripts rápidamente. |
| Material Icon Theme *(opcional)* | Philipp Kief | Íconos visuales para cada archivo. |

---

## ⚙️ 3️⃣ Abrir el proyecto

1. En VS Code: **Archivo → Abrir carpeta...**
2. Selecciona:
   ```
   C:\MT5_BOT\
   ```

---

## 🐍 4️⃣ Configurar entorno virtual

### Crear entorno (solo la primera vez)
```bash
python -m venv .venv
```

### Activar entorno
```bash
.venv\Scripts\activate
```

Aparecerá en terminal:
```
(.venv) C:\MT5_BOT>
```

Selecciona el intérprete:
```
Ctrl + Shift + P → Python: Select Interpreter → .venv
```

---

## 📦 5️⃣ Instalar dependencias

```bash
pip install pandas numpy scikit-learn joblib matplotlib yfinance tqdm
```

---

## 🧰 6️⃣ Ejecutar un script

Abre:
```
infra/data_pipeline.py
```

Presiona:
```
Ctrl + F5
```

Salida esperada:
```
[INFO] Cargados 10 archivos — total filas: 19570
[PIPELINE] Ejecución completada correctamente.
```

---

## 🧠 7️⃣ Ejecutar módulo ML

```bash
python ml/training/trainer.py
```

---

## 🧪 8️⃣ Recomendaciones

| Ajuste | Acción |
|---------|--------|
| Formato de código | `pip install black` o `pip install autopep8` |
| Linting | `Ctrl + Shift + P → Python: Enable Linting` |
| Tema visual | “Material Icon Theme” y tema oscuro. |

---

## 🧭 9️⃣ Estructura esperada

```
C:\MT5_BOT\
├─ infra/
├─ ml/
│   └─ training/
├─ Docs/
│   └─ Guides/
└─ .venv/
```

---

## ✅ Resultado esperado

- Log limpio y sin advertencias al ejecutar `data_pipeline.py`.  
- Entorno virtual activo.  
- Extensiones funcionando sin conflictos.  
- Autocompletado y depuración habilitados.
