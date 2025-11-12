# 💻 HARDWARE — Perfil de Equipos de Cómputo

**Última actualización:** 2025-11-11

---

## 🖥️ PC Principal — Ryzen 7 2700X

| Componente | Especificación | Evaluación Técnica |
|-------------|----------------|--------------------|
| **CPU** | AMD Ryzen 7 2700X (8 núcleos / 16 hilos, 3.7–4.3 GHz) | Excelente para tareas paralelas; rendimiento alto en entrenamiento ML en CPU. |
| **GPU** | NVIDIA GTX 980 Ti (6 GB) + GTX 1050 (3 GB) | GPUs disponibles; **uso opcional** para experimentos acelerados. CPU será el motor principal. |
| **RAM** | 64 GB DDR4 | Óptima para datasets medianos y backtesting simultáneo sin swap. |
| **Discos** | SSD 1 TB (para datasets y modelos), SSD 224 GB (SO y entornos), HDD 466 GB (backups) | Excelente distribución; alto rendimiento de lectura/escritura. |
| **Sistema Operativo** | Windows 10 64 bits | Adecuado; se recomienda usar WSL2 o dual boot Linux para tareas largas. |

---

## ⚙️ Estrategia de uso de recursos

### 🧠 CPU (modo principal)
- **Prioridad absoluta** para entrenamiento, optimización y backtesting.  
- Aprovechar los **16 hilos** con `n_jobs=8–12` para balancear rendimiento y estabilidad.  
- Paralelización segura para Optuna / LightGBM / Scikit-learn.  
- Evitar saturar el 100 % de CPU durante largos periodos; reservar 2 núcleos para el sistema.

### 🧮 GPU (modo opcional)
- **Uso experimental**, solo para cargas específicas de entrenamiento o inferencia.  
- Activar GPU en frameworks compatibles (LightGBM, PyTorch) solo bajo demanda.  
- No usar múltiples GPUs simultáneamente (VRAM desbalanceada).

### 💾 Almacenamiento
- **SSD 1 TB:** datasets y modelos.  
- **SSD 224 GB:** sistema y entornos virtuales.  
- **HDD 466 GB:** backups y registros históricos.

### 🧩 Configuración sugerida
| Recurso | Parámetro | Recomendación |
|----------|------------|----------------|
| CPU Threads | `n_jobs=8–12` | Paralelismo seguro. |
| GPU Uso | Opcional | Activar solo si se solicita. |
| Memoria RAM | 64 GB | Reservar 8 GB para SO. |
| Sistema de Archivos | SSD principal | Evitar operaciones intensivas en HDD. |
| Monitoreo | HWMonitor / MSI Afterburner | Controlar temperatura CPU/GPU. |

---

## 🔁 Resumen operativo
- **Modo por defecto:** CPU.  
- **GPU:** opcional para pruebas o aceleración.  
- **Objetivo:** rendimiento máximo sin sacrificar estabilidad del sistema.

---

📘 Este perfil sustituye al anterior y se alinea con las políticas de desarrollo modular del proyecto **MT5_BOT**.

---

## 💼 Notebook Secundario — Intel Core i5‑9300H

| Componente | Especificación | Evaluación Técnica |
|-------------|----------------|--------------------|
| **CPU** | Intel Core i5‑9300H (4 núcleos / 8 hilos, 2.4–4.1 GHz) | Buen desempeño para tareas de validación y monitoreo; limitado para HPO intensivo. |
| **GPU** | Intel UHD Graphics 630 + NVIDIA GTX 1650 (Notebook) | GPU discreta eficiente para inferencia ligera o testing; no recomendada para entrenamiento prolongado. |
| **RAM** | 24 GB instalados (19 GB utilizables) | Suficiente para testing, backtesting pequeño o validación parcial. |
| **Discos** | SSD 224 GB (Windows 11), SSD 119 GB (libres), HDD 932 GB (libres) | Buena configuración híbrida; SSD para datos activos, HDD para almacenamiento. |
| **Sistema Operativo** | Windows 11 64 bits | Actualizado y estable; ideal para tareas móviles. |

### ⚙️ Estrategia de uso

- **Rol secundario:** testing, validación, monitoreo remoto del bot MT5.  
- **Uso de CPU:** tareas ligeras, pruebas locales, compilaciones pequeñas.  
- **Uso de GPU (GTX 1650):** opcional; puede acelerar inferencias o entrenamientos rápidos con batch pequeño.  
- **RAM:** adecuada para ejecución de notebooks o entrenamiento simple (< 1 GB dataset).  
- **Discos:** mantener datasets en SSD, backups en HDD.  

### 🧩 Configuración sugerida

| Recurso | Parámetro | Recomendación |
|----------|------------|----------------|
| CPU Threads | `n_jobs=4` | Balanceado; evita sobrecarga térmica. |
| GPU Uso | Opcional (1 tarea a la vez) | Activar solo en pruebas controladas. |
| Memoria RAM | 24 GB | Reservar 5 GB para SO. |
| Sistema de Archivos | SSD principal + HDD backup | Optimiza lectura. |
| Monitoreo | HWMonitor / MSI Afterburner | Vigilar temperatura. |

---

## 🔁 Roles combinados

| Equipo | Rol | Función principal |
|--------|------|------------------|
| **PC Ryzen 7 2700X** | Estación de entrenamiento y optimización | CPU principal, entrenamiento ML, backtesting. |
| **Notebook i5‑9300H** | Estación de validación y monitoreo | Testing ligero, paper trading, actualizaciones de campo. |

---

📘 **Actualización registrada el 2025-11-11.**
