# Claude with the Anthropic API — Anthropic Academy

Curso: https://anthropic.skilljar.com/claude-with-the-anthropic-api

**El curso más grande de la academia:** 85 lecciones que van desde la primera llamada al API hasta construir agentes. Es el recorrido completo de desarrollador: pedir, medir, mejorar, extender y automatizar.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: selector de modelo, laboratorio de prompt engineering con las puntuaciones reales de cada técnica, diagramas de flujo de tool use y RAG, calculadora de caché, decisor workflow-vs-agente, flashcards y quiz. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Bloque |
|---|----------|--------|
| 01 | [Acceder a Claude con el API](01-acceder-al-api.md) | Fundamentos |
| 02 | [Evaluación de prompts](02-evaluacion-de-prompts.md) | Medir |
| 03 | [Prompt engineering](03-prompt-engineering.md) | Mejorar |
| 04 | [Tool use](04-tool-use.md) | Extender |
| 05 | [Herramientas avanzadas y predefinidas](05-herramientas-avanzadas.md) | Extender |
| 06 | [RAG](06-rag.md) | Extender |
| 07 | [Funcionalidades de Claude](07-funcionalidades-de-claude.md) | Extender |
| 08 | [Prompt caching](08-prompt-caching.md) | Optimizar |
| 09 | [MCP](09-mcp.md) | Integrar |
| 10 | [Claude Code y computer use](10-claude-code-y-computer-use.md) | Automatizar |
| 11 | [Agentes y workflows](11-agentes-y-workflows.md) | Arquitectura |
| 12 | [Repaso y evaluaciones](12-repaso-y-quizzes.md) | Cierre |

## El hilo conductor

El curso enseña una disciplina, no una lista de funcionalidades. En orden:

1. **Pide.** Una llamada al API es un modelo, un `max_tokens` y una lista de mensajes. Todo lo demás son matices sobre esos tres.
2. **Mide antes de retocar.** El error típico es probar un prompt dos veces y desplegarlo. Antes de tocar nada, monta una **eval**: dataset + prompt + LLM + grader.
3. **Mejora con técnicas, no a ojo.** Claro y directo, específico, XML, ejemplos. El curso mide cada técnica: **2,32 → 3,92 → 7,86**.
4. **Extiende.** Tool use para lo que Claude no sabe. RAG para lo que no cabe. Funcionalidades nativas para lo que ya viene resuelto.
5. **Optimiza.** El caché reutiliza el trabajo de procesar la entrada, y tiene reglas estrictas.
6. **Integra.** MCP traslada el peso de escribir esquemas y funciones del desarrollador al mantenedor del servidor.
7. **Decide la arquitectura.** Y aquí el consejo final del curso, que va a contracorriente: **prioriza workflows.** Los agentes solo cuando la flexibilidad haga falta de verdad.

> Los usuarios quieren productos que funcionen al 100%, no agentes vistosos. **Resuelve el problema de forma fiable primero; innova después.**

## Sobre el material

El curso es **de vídeo**: las páginas de lección solo llevan el reproductor y los ejercicios son notebooks descargables. Estos resúmenes se han elaborado a partir de las **notas oficiales del curso** que Anthropic embebe en la propia plataforma — 75 notas, una por lección de contenido.

## Evaluaciones

El curso trae **7 quizzes por bloque** más una **evaluación final**. Están sin hacer a propósito: los harás tú al terminar de estudiar, y luego se registran aquí las preguntas reales con su feedback. La lista está en el [capítulo 12](12-repaso-y-quizzes.md).
