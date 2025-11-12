# 📘 MT5_BOT — CONTINUIDAD Y COMPROMISO TÉCNICO  
**Versión:** 1.0  
**Fecha:** 2025-11-12  
**Autoría compartida:** Usuario (Propietario) + GPT-5 (Asistente técnico IA)

---

## 🧭 Propósito del documento
Garantizar la **continuidad, estabilidad y trazabilidad** del proyecto **MT5_BOT**, definiendo compromisos técnicos y operativos entre el desarrollador humano (Luis Longobardi) y la inteligencia asistente (GPT-5).

Este documento se considera parte integral de la documentación oficial en `Docs/Guides/`.

---

## ⚙️ 1. Alcance y objetivo
1. Establecer las condiciones que aseguran que **ninguna información crítica** del proyecto se pierda o sobrescriba sin autorización explícita.  
2. Definir un flujo de trabajo claro y estable basado en **GitHub como fuente maestra** de persistencia.  
3. Asegurar transparencia total sobre las **limitaciones técnicas** del entorno de la IA.  
4. Implementar mecanismos automáticos y manuales de **respaldo, control de versiones y validación**.

---

## 🔒 2. Compromisos técnicos

### 2.1. Compromisos del asistente (GPT-5)
- **Transparencia proactiva:**  
  Notificar inmediatamente si una acción o limitación técnica podría poner en riesgo información o generar pérdida de tiempo.

- **Persistencia garantizada:**  
  Toda documentación generada o modificada se sincronizará con el repositorio GitHub oficial.  
  El entorno temporal no se usará más como almacenamiento principal.

- **No destrucción:**  
  Ningún archivo del proyecto será sobrescrito o eliminado sin aprobación explícita del propietario.

- **Trazabilidad documental:**  
  Cada cambio importante será reflejado en un commit con comentario técnico, un registro en `Docs/Updates/MT5_CONTINUIDAD.md` y una etiqueta (`tag`) en Git.

- **Asistencia técnica extendida:**  
  El asistente podrá generar automáticamente herramientas complementarias (scripts, plantillas, documentación técnica) sin alterar el flujo del proyecto principal.

---

### 2.2. Compromisos del propietario (Luis Longobardi)
- **Control del repositorio:**  
  Mantendrá la propiedad y permisos administrativos del repositorio `MT5_BOT`.  
  Toda modificación será ejecutada manualmente mediante `git push` desde su entorno local o GitHub Desktop.

- **Ejecución local controlada:**  
  Las pruebas, compilaciones y ejecuciones se realizarán dentro de su entorno local (`C:\MT5_BOT\`) o notebook de desarrollo, garantizando independencia de la IA.

- **Validación previa:**  
  Confirmará cada paso crítico (instalaciones, actualizaciones, reinicios de estructura) antes de que el asistente los genere.

---

## 🔄 3. Flujo de trabajo Git oficial
1. **main** → Rama estable de producción.  
2. **dev** → Rama de desarrollo para pruebas y nuevas versiones.  
3. **Docs/** y **ml/** → Directorios principales bajo control de versión.  
4. **Tags automáticos:** Cada versión aprobada (`v1.2`, `v1.3`, etc.) se documentará en `Docs/Updates/MT5_CONTINUIDAD.md`.

---

## 🧩 4. Estrategias de respaldo y protección
- El repositorio GitHub es el **único repositorio maestro**.  
- Se mantendrán copias locales sincronizadas.  
- No se incluirán entornos virtuales (`.venv`) ni archivos temporales en control de versión.  
- Cada versión funcional incluirá logs validados (`Docs/Logs/MLLogs`).

---

## 🤝 5. Declaración de compromiso
Ambas partes (Propietario e IA) acuerdan mantener la integridad del proyecto **MT5_BOT**, trabajando bajo los principios de:
- **Transparencia**
- **Estabilidad**
- **Colaboración técnica responsable**
- **Documentación continua**

> *“Ningún cambio sin consentimiento, ningún progreso sin registro.”*

---

## 🧾 6. Historial del documento
| Fecha | Versión | Descripción |
|--------|----------|--------------|
| 2025-11-12 | 1.0 | Creación inicial del acuerdo de continuidad y compromiso técnico. |

---

📍 **Ubicación:** `Docs/Guides/CONTINUIDAD_Y_COMPROMISO.md`  
📘 Este documento forma parte permanente del proyecto y deberá actualizarse cuando cambien las políticas de flujo o persistencia.
