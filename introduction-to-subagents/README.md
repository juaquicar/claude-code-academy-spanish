# Introduction to Subagents — Anthropic Academy

Curso: https://anthropic.skilljar.com/introduction-to-subagents

**Idea central:** usar y crear subagentes en Claude Code para gestionar el contexto, delegar tareas y montar flujos especializados que mantengan limpia y enfocada la conversación principal.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página web: diagramas interactivos, comparador de modelos, generador de config, decisor delegar/no delegar, flashcards y quiz con corrección al momento. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo |
|---|----------|
| 01 | [¿Qué son los subagentes?](01-que-son-los-subagentes.md) |
| 02 | [Crear un subagente](02-crear-un-subagente.md) |
| 03 | [Diseñar subagentes eficaces](03-disenar-subagentes-eficaces.md) |
| 04 | [Usar subagentes con criterio](04-usar-subagentes-con-criterio.md) |
| 05 | [Repaso y autoevaluación](05-repaso-y-quiz.md) |

> Este curso **no tiene quiz oficial** en la plataforma: son 4 lecciones y nada más. El capítulo 05 es una autoevaluación construida a partir del material.

## Hilo conductor

Un subagente es **una ventana de contexto aparte**. Recibe dos cosas —un system prompt propio y una descripción de tarea escrita por el agente padre—, trabaja por su cuenta y **devuelve solo un resumen**. Toda su conversación se descarta después.

Eso te da el beneficio y te cobra el precio:

| Ganas | Pierdes |
|---|---|
| El contexto principal se queda limpio | **Visibilidad** de cómo llegó a la conclusión |
| Recibes solo la información que necesitas | El detalle intermedio, comprimido en un resumen |
| Cada subagente se concentra en una tarea | Lo que no pidas explícitamente en el formato de salida |

### La regla de decisión, que resume el curso entero

> **¿Importa el trabajo intermedio?**
>
> **No** → solo quieres el resultado final → **delega a un subagente**.
> **Sí** → necesitas ver y reaccionar a lo que pasa por el camino → **quédatelo en el hilo principal**.

### Las cuatro características de un subagente eficaz

1. **Descripción específica** — controla *cuándo* se lanza y *qué instrucciones recibe*.
2. **Salida estructurada** — le da puntos de parada naturales y evita que corra de más.
3. **Reporte de obstáculos** — para que el hilo principal no redescubra los mismos workarounds.
4. **Acceso limitado a herramientas** — solo lo que el trabajo necesita.
