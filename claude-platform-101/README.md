# Claude Platform 101 — Anthropic Academy

Curso: https://anthropic.skilljar.com/claude-platform-101

**Idea central:** hay un abismo entre chatear con Claude y **publicar algo con Claude dentro**. Este curso lo cruza en línea recta: de una llamada `messages.create` a un agente que corre solo, con tools, en la infraestructura de Anthropic.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: constructor de peticiones en vivo, simulador del bucle de agente turno a turno, selector de modelo, decisor tools/skills/MCP, comparador de los cuatro patrones de contexto, línea de tiempo de los primitivos de managed agents, flashcards y el quiz con corrección al momento. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Módulo | Tiempo |
|---|----------|--------|--------|
| 01 | [¿Qué es la Claude Platform?](01-que-es-la-claude-platform.md) | La plataforma | 15 min |
| 02 | [Tu primera llamada a la API](02-tu-primera-llamada-a-la-api.md) | La plataforma | 15 min |
| 03 | [Elegir el modelo adecuado](03-elegir-el-modelo-adecuado.md) | La plataforma | 15 min |
| 04 | [El bucle del agente](04-el-bucle-del-agente.md) | Enseñar al agente | 20 min |
| 05 | [¿Qué es el uso de tools?](05-que-es-el-uso-de-tools.md) | Enseñar al agente | 20 min |
| 06 | [¿Qué es el thinking?](06-que-es-el-thinking.md) | Enseñar al agente | 15 min |
| 07 | [Tools integradas](07-tools-integradas.md) | Ampliar el agente | 15 min |
| 08 | [Skills](08-skills.md) | Ampliar el agente | 15 min |
| 09 | [MCP](09-mcp.md) | Ampliar el agente | 15 min |
| 10 | [Gestión del contexto](10-gestion-del-contexto.md) | Ampliar el agente | 15 min |
| 11 | [¿Qué son los agentes gestionados?](11-que-son-los-agentes-gestionados.md) | Agentes gestionados | 20 min |
| 12 | [Construir tu primer agente gestionado](12-construir-tu-primer-agente-gestionado.md) | Agentes gestionados | 20 min |
| 13 | [Construir con Claude Code](13-construir-con-claude-code.md) | Construir con Claude Code | 10 min |
| 14 | [Repaso y quiz](14-repaso-y-quiz.md) | Quiz | 15 min |

## El hilo conductor

### 1 · Todo sale de una llamada

`messages.create` con **modelo, límite de tokens y mensajes**. El `system` prompt moldea la persona. Y el `content` de la respuesta **es un array de bloques**, no una cadena — porque ahí caben texto, llamadas a tools y thinking.

Todo lo demás del curso es **esa misma llamada con más cosas encima**.

### 2 · El modelo se elige midiendo, no adivinando

Cuatro tiers — **Fable** por encima de Opus para lo más duro, **Opus** para razonamiento profundo, **Sonnet** para el día a día, **Haiku** para volumen.

El método: **20 o 30 ejemplos de tu carga real**, ejecutados **de Haiku hacia arriba**, parándote en el primero que aguante.

> **El modelo correcto es el más barato cuya salida publicarías de verdad.**

En producción no eliges uno: **enrutas por tarea dentro del mismo endpoint**.

### 3 · Un agente es Claude en bucle

Observar, decidir, actuar, repetir — hasta que el **stop reason** sea `end_turn`.

> **Tú eres dueño del bucle y de las tools. Claude es dueño del razonamiento.**

Y sobre ese bucle, tres formas de dejar de escribirlo tú:

| Nivel de delegación | Qué delegas |
|---|---|
| **Bucle a mano** | Nada. Control total |
| **Tool runner** | El bucle y los schemas (a partir de tus funciones reales) |
| **Server tools** | La ejecución de esa tool concreta — sin bucle siquiera |
| **Managed agents** | **El agente entero**: bucle, sandbox y reanudabilidad |

### 4 · Tools, skills y MCP no compiten

> **Las tools son para tus cosas, las skills para tus procesos, y MCP para las cosas de todos los demás.**

Con un matiz que decide muchos diseños: **quién mantiene la integración**. Con tools personalizadas, tú. Con MCP, **el proveedor del servicio**.

### 5 · El contexto es finito y se paga

Todo lo que Claude ve en un turno cuenta: system prompt, historial, definiciones y resultados de tools, ficheros, skills, thinking. **Cuando la ventana se llena, la petición falla.**

Cuatro patrones, tres modos de fallo:

| Patrón | ¿Funcionalidad de API? | Ataca |
|---|---|---|
| **Just-in-time context** | **No — es patrón de diseño** | Tamaño de ventana |
| **Compactación en servidor** | Sí (`context_management`) | Tamaño de ventana |
| **Prompt caching** | Sí | **Coste** |
| **Memory tool** | Sí | **Ausencia de estado entre sesiones** |

### 6 · Y cuando el bucle es demasiado largo, lo delegas entero

**Agent → Environment → Session → Events.** La sesión es la unidad de trabajo, el agente es reutilizable, y **el stream se abre antes del mensaje inicial** porque solo entrega lo que ocurre después.

Alrededor: rúbricas con **graders independientes**, memoria entre ejecuciones, MCP, tools propias, políticas de permisos para las acciones sensibles y coordinación multi-agente.

> **Tú defines qué significa "hecho". Claude trabaja hasta llegar ahí.**

## Sobre el material

Curso **de vídeo con texto de apoyo completo** en cada lección; estos resúmenes salen de ahí. Los ejemplos de código están **verbatim** del curso, en Python o TypeScript según los usara la lección.

**El curso sí tiene quiz oficial** (8 preguntas, de las que 5 son evaluables). El [capítulo 14](14-repaso-y-quiz.md) recoge las preguntas reales con sus distractores, más un banco extra de 28 preguntas sobre lo que el oficial deja fuera.
