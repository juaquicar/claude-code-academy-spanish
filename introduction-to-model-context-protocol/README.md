# Introduction to Model Context Protocol — Anthropic Academy

Curso: https://anthropic.skilljar.com/introduction-to-model-context-protocol

**Idea central:** MCP traslada el trabajo de escribir esquemas y funciones de herramienta **del desarrollador de la aplicación al mantenedor del servidor MCP**.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: diagrama de las tres primitivas por quién las controla, recorrido del flujo cliente-servidor paso a paso, comparador de resources vs. tools vs. prompts, flashcards y quiz. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo |
|---|----------|
| 01 | [Qué es MCP](01-que-es-mcp.md) |
| 02 | [Clientes MCP y el proyecto](02-clientes-mcp.md) |
| 03 | [Definir tools](03-definir-tools.md) |
| 04 | [Implementar un cliente](04-implementar-un-cliente.md) |
| 05 | [Resources](05-resources.md) |
| 06 | [Prompts](06-prompts.md) |
| 07 | [Las tres primitivas](07-las-tres-primitivas.md) |
| 08 | [Repaso y evaluación](08-repaso-y-evaluacion.md) |

## El hilo conductor

Un servidor MCP tiene **tres primitivas**, y la lección final del curso las ordena con una idea que lo aclara todo de golpe: **se distinguen por quién decide cuándo se usan**.

| Primitiva | Control | A quién sirve | Ejemplo real |
|---|---|---|---|
| **Tools** | **El modelo** decide cuándo ejecutarlas | Al **modelo** | Ejecución de código para cálculos |
| **Resources** | **El código de la aplicación** decide cuándo traer los datos | A la **aplicación** | Selección de documentos de Google Drive |
| **Prompts** | **El usuario**, con un clic o un slash command | Al **usuario** | Los botones de inicio de chat de Claude |

Y de ahí sale la regla de decisión:

> **¿Necesitas capacidades para Claude? → tools.**
> **¿Necesitas datos para tu app? → resources.**
> **¿Necesitas flujos para el usuario? → prompts.**

## Sobre el material

El curso es **de vídeo**: las páginas de lección solo llevan el reproductor. Estos resúmenes se han elaborado a partir de las **notas oficiales** que Anthropic embebe en la plataforma — 11 notas, una por lección de contenido.

El curso trae una **evaluación final oficial** (*Final assessment on MCP*) que está **sin hacer a propósito**: la harás tú al terminar de estudiar. Cuando la hagas, pásame los resultados y registro aquí las preguntas reales con su feedback.

> **Relación con los otros cursos del repo:** este curso cubre el mismo terreno que el [capítulo 09 de *Claude with the Anthropic API*](../claude-with-the-anthropic-api/09-mcp.md), pero con una lección por tema en vez de un resumen, y añade la lección de las tres primitivas que allí no está. Para lo que viene *después* —sampling, roots, transportes y los flags que rompen el despliegue— sigue con [MCP: Advanced Topics](../model-context-protocol-advanced-topics/).
