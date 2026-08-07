# 04 — Skills vs. otras funcionalidades de Claude Code

*15 minutos* · [Vídeo](https://www.youtube.com/embed/IgNN4v0BJdU)

**Al terminar sabrás:** comparar skills con CLAUDE.md, subagentes, hooks y servidores MCP · elegir la funcionalidad correcta para cada caso · diseñar un montaje complementario que combine varias.

---

Claude Code ofrece cinco opciones de personalización. **Resuelven problemas distintos**, y saber cuándo usar cada una evita que construyas lo que no es.

## La tabla que resume el capítulo

| Funcionalidad | Se activa por | Dónde vive el trabajo |
|---|---|---|
| **CLAUDE.md** | Siempre — en cada conversación | El contexto actual |
| **Skills** | **Tu petición** (request-driven) | El contexto actual |
| **Subagentes** | Delegación explícita | **Un contexto separado** |
| **Hooks** | **Eventos** (event-driven) | Fuera de la conversación |
| **Servidores MCP** | Herramientas externas | Otra categoría entera |

---

## CLAUDE.md vs. skills

**CLAUDE.md se carga en todas las conversaciones, siempre.** Si quieres que Claude use el modo estricto de TypeScript en tu proyecto, eso va en CLAUDE.md.

**Las skills se cargan bajo demanda.** Tu checklist de revisión de PR no tiene por qué estar en contexto mientras escribes código nuevo: se activa cuando pides una revisión.

| Usa CLAUDE.md para | Usa skills para |
|---|---|
| Estándares de proyecto que **siempre** aplican | **Experiencia específica de una tarea** |
| Restricciones como *"nunca modifiques el esquema de la base de datos"* | Conocimiento que **solo a veces** es relevante |
| Preferencias de framework y estilo de código | Procedimientos detallados que **ensuciarían todas las conversaciones** |

## Skills vs. subagentes

**Las skills añaden conocimiento a tu conversación actual.** Al activarse, sus instrucciones se unen al contexto existente.

**Los subagentes corren en un contexto separado.** Reciben una tarea, trabajan de forma independiente y devuelven resultados. Están **aislados** de la conversación principal.

| Usa subagentes cuando | Usa skills cuando |
|---|---|
| Quieres **delegar** a un contexto de ejecución separado | Quieres **mejorar el conocimiento** de Claude para la tarea actual |
| Necesitas **acceso a herramientas distinto** del de la conversación principal | La experiencia aplica **a lo largo de toda la conversación** |
| Quieres **aislamiento** entre el trabajo delegado y tu contexto | |

## Skills vs. hooks

**Los hooks disparan por eventos.** Un hook puede ejecutar un linter cada vez que Claude guarda un fichero, o validar la entrada antes de ciertas llamadas a herramienta. Son **event-driven**.

**Las skills disparan por peticiones.** Se activan según lo que estás pidiendo. Son **request-driven**.

| Usa hooks para | Usa skills para |
|---|---|
| Operaciones que deben correr **en cada guardado** | Conocimiento que **informa cómo** Claude atiende las peticiones |
| **Validación** antes de llamadas concretas | Directrices que **afectan a su razonamiento** |
| **Efectos secundarios automáticos** de las acciones de Claude | |

## Juntándolo todo

Un montaje típico incluye las cinco:

| Pieza | Su especialidad |
|---|---|
| **CLAUDE.md** | Estándares de proyecto **siempre activos** |
| **Skills** | Experiencia específica de tarea, **bajo demanda** |
| **Hooks** | Operaciones automáticas **disparadas por eventos** |
| **Subagentes** | Contextos de ejecución **aislados** para trabajo delegado |
| **Servidores MCP** | **Herramientas externas** e integraciones |

> **Cada una gestiona su especialidad. No fuerces todo dentro de las skills cuando otra opción encaja mejor — y puedes usar varias a la vez.**

**Usa skills cuando tengas conocimiento que Claude deba aplicar automáticamente cuando el tema sea relevante**, y combínalas con el resto para una personalización completa.

## Reflexión

- Mira tu CLAUDE.md actual. ¿Hay algo ahí que funcionaría mejor como skill, cargándose solo cuando es relevante?
- Piensa en el flujo de tu equipo. ¿Qué combinación de funcionalidades atacaría vuestros puntos de dolor más habituales?
