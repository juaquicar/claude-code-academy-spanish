# 01 — ¿Qué son los subagentes?

[Vídeo](https://www.youtube.com/embed/jKErNxuxPXg)

Los subagentes son **asistentes especializados a los que Claude Code puede delegar tareas**. Ayudantes enfocados: cada uno corre en **su propia ventana de contexto**, hace su trabajo y **devuelve un resumen** al hilo principal.

Los pasos intermedios —todas las lecturas de fichero, búsquedas y llamadas a herramientas— **quedan aislados y nunca ensucian tu conversación principal**.

## Por qué importan

Cada vez que hablas con Claude Code estás añadiendo a la ventana de contexto principal: cada llamada a herramienta, cada fichero leído, cada resultado de búsqueda se almacena ahí. Ese espacio **es finito**, y cuando se llena, Claude empieza a perder el hilo de las partes anteriores de la conversación.

Los subagentes lo resuelven **levantando una ventana de contexto separada**. El subagente recibe dos cosas:

- **Un system prompt propio**, desde tu fichero de configuración, que define su rol y su comportamiento.
- **Una descripción de tarea** escrita por el agente padre a partir de lo que pediste.

A partir de ahí trabaja solo: lee ficheros, busca, edita código, lo que necesite. Cuando termina, **solo el resumen vuelve** a tu conversación principal. **La conversación completa del subagente se descarta.**

## El trato: qué ganas y qué pierdes

| Ganas | Pierdes |
|---|---|
| Tu contexto principal se queda limpio | **Visibilidad** sobre cómo llegó a sus conclusiones |
| Obtienes la respuesta sin el ruido del viaje | El detalle intermedio queda comprimido |

Es un intercambio explícito, no un efecto secundario. Tenlo presente al decidir.

## Ejemplo práctico

Exploras un codebase desconocido y quieres saber **qué servicio gestiona los reembolsos**.

- **Sin subagente:** Claude podría leer 15 ficheros, lanzar varias búsquedas y rastrear múltiples llamadas a función. Todo eso llena tu ventana de contexto, **aunque solo necesitabas un dato**.
- **Con subagente:** preguntas, el subagente *Explore* se levanta, hace toda la excavación en su propio contexto y te devuelve una respuesta enfocada.

Tu ventana de contexto principal **solo registra la pregunta y el resumen** — no los 15 ficheros que se leyeron por el camino.

## Subagentes integrados

Claude Code trae varios listos para usar:

| Subagente | Para qué |
|---|---|
| **General purpose** | Tareas multipaso que requieren **exploración y acción** |
| **Explore** | Búsqueda y navegación **rápidas** por el codebase |
| **Plan** | Se usa en plan mode: investigación y análisis del codebase **antes de presentar un plan** |

## Subagentes propios

Más allá de los integrados, puedes crear los tuyos con **system prompts y acceso a herramientas a medida**. Eso te permite definir agentes especializados para tu flujo de trabajo: un revisor de código, un escritor de tests, un generador de documentación, o lo que necesites.

## Conclusiones clave

Los subagentes dan tres beneficios:

1. **Trocean el trabajo** en piezas enfocadas, y cada subagente se concentra en una tarea concreta.
2. **Mantienen limpia la ventana de contexto principal** aislando todo el trabajo intermedio.
3. **Devuelven justo la información que necesitas**, como resumen conciso.

> Cuanto menos ruido en tu contexto principal, **más largo y más eficaz** puede ser tu trabajo.
