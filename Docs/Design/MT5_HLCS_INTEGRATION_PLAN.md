# 🧩 MT5_HLCS_INTEGRATION_PLAN — Plan de Integración de Hyper Latin Cube Sampling (HLCS)

**Fecha de creación:** 2025-11-11  
**Versión:** 1.0  
**Autor:** Sistema IA — Proyecto MT5_BOT

---

## 🎯 Objetivo
Definir la estrategia de integración del método **Hyper Latin Cube Sampling (HLCS)** dentro de la arquitectura modular de MT5_BOT, para la **Fase 2** del proyecto.

El HLCS permitirá realizar **muestreos multidimensionales eficientes** de hiperparámetros de modelos ML, maximizando cobertura y reduciendo redundancia en comparación con métodos aleatorios o deterministas tradicionales.

---

## 🧠 Rol del HLCS en el proyecto

| Componente | Función |
|-------------|----------|
| `ml/optimization/hlcs_sampler.py` | Implementará el algoritmo HLCS para generar combinaciones de hiperparámetros. |
| `ml/optimization/optuna_bridge.py` | Permitirá comparar HLCS vs Optuna en términos de eficiencia y convergencia. |
| `ml/training/trainer.py` | Integrará HLCS como método de exploración previo a entrenamientos masivos. |

---

## ⚙️ Arquitectura propuesta

```
ml/
├─ optimization/
│   ├─ hlcs_sampler.py       ← implementación base del método HLCS
│   ├─ optuna_bridge.py      ← integración con frameworks de optimización adaptativa
│   ├─ random_search.py
│   ├─ bayesian_optim.py
│   └─ __init__.py
└─ training/
    ├─ trainer.py            ← integración del sampler HLCS en los ciclos de entrenamiento
    └─ __init__.py
```

---

## 📊 Flujo operativo

1. Definir los rangos de hiperparámetros (ejemplo: learning_rate, n_estimators, max_depth).  
2. Generar combinaciones usando HLCS:  
   ```python
   from ml.optimization.hlcs_sampler import hlcs_generate_samples

   params = {
       "learning_rate": (0.001, 0.2),
       "n_estimators": (50, 500),
       "max_depth": (3, 12)
   }
   samples = hlcs_generate_samples(params, n_samples=50)
   ```
3. Pasar las muestras al motor de entrenamiento (`trainer.py`) para evaluación cruzada.  
4. Registrar los resultados en `mlflow` o `Docs/Logs/opt_results/`.  

---

## 🧩 Beneficios esperados
- Cobertura uniforme del espacio de búsqueda.
- Reducción del número de pruebas necesarias.
- Mejor estabilidad y reproducibilidad.
- Integración fluida con módulos ya existentes.

---

## 🔮 Próximos pasos
1. Implementar `hlcs_sampler.py` en la **Fase 2** del desarrollo.  
2. Probar comparativas con `random_search` y `optuna`.  
3. Documentar métricas de eficiencia y convergencia.  

---

📘 *Este plan se vincula directamente con la hoja de ruta técnica de la Fase 2 y debe considerarse parte integral del módulo `ml/optimization`.*
