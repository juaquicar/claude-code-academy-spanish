# Claude Code 101 — Anthropic Academy

Curso: https://anthropic.skilljar.com/claude-code-101

**Idea central:** Claude Code no es un chat que te sugiere código, es **un agente que entra en tu repositorio y hace el trabajo** — y sacarle partido consiste en dominar dos cosas: **el flujo Explore → Plan → Code → Commit** y **qué ocupa tu ventana de contexto**.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: simulador del bucle agéntico, ciclador de modos de permisos, decisor `/compact` vs. `/clear`, medidor de coste en contexto, constructor de hooks en vivo, flashcards y el quiz con corrección al momento. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Módulo | Tiempo |
|---|----------|--------|--------|
| 01 | [¿Qué es Claude Code?](01-que-es-claude-code.md) | Qué es Claude Code | 10 min |
| 02 | [Cómo funciona Claude Code](02-como-funciona-claude-code.md) | Qué es Claude Code | 10 min |
| 03 | [Instalar Claude Code](03-instalar-claude-code.md) | Instalación | 10 min |
| 04 | [Tu primer prompt](04-tu-primer-prompt.md) | Instalación | 10 min |
| 05 | [El flujo explore → plan → code → commit](05-explore-plan-code-commit.md) | Flujos diarios | 15 min |
| 06 | [Gestión del contexto](06-gestion-del-contexto.md) | Flujos diarios | 15 min |
| 07 | [Revisión de código](07-revision-de-codigo.md) | Flujos diarios | 10 min |
| 08 | [El fichero CLAUDE.md](08-el-fichero-claude-md.md) | Personalización | 15 min |
| 09 | [Subagentes](09-subagentes.md) | Personalización | 10 min |
| 10 | [Skills](10-skills.md) | Personalización | 5 min |
| 11 | [MCP](11-mcp.md) | Personalización | 15 min |
| 12 | [Hooks](12-hooks.md) | Personalización | 15 min |
| 13 | [Repaso y quiz](13-repaso-y-quiz.md) | Quiz | 15 min |

## El hilo conductor

### 1 · Es un agente, no un chat

Un agente es **software que interactúa con su entorno y ejecuta acciones** para completar un objetivo, con un modelo operando en bucle. Claude Code lee tu código, edita ficheros, ejecuta comandos y busca en la web. La diferencia con Claude.ai no es de calidad de respuesta: es que **entra y hace el trabajo**.

El bucle agéntico, en cinco pasos: **prompt → reunir contexto → actuar → verificar → repetir o terminar.** Y durante todo el bucle puedes añadir contexto, interrumpir o redirigir.

### 2 · El flujo es la lección

> **Si te llevas una sola cosa de este curso, que sea este flujo.**

| Fase | Qué aporta | Con qué |
|---|---|---|
| **Explore** | El contexto relevante del proyecto | Plan Mode o el subagente de explore |
| **Plan** | Un plan que sirve de **criterio de éxito** | Plan Mode (`Shift + Tab`) |
| **Code** | El ida y vuelta hasta el resultado final | Tests, tools, criterio explícito |
| **Commit** | Revisión sin sesgo y subida | **Subagente revisor**, `/commit-push-pr` |

El motivo de que Plan Mode importe tanto: **es el único punto donde corriges el rumbo antes de que exista código que deshacer**.

### 3 · El contexto es el recurso escaso

Todo lo que Claude lee, ejecuta o recibe ocupa espacio. Cuando se llena, **se compacta automáticamente** — resumiendo lo importante y tirando resultados de tools, con **riesgo de perder detalles**.

Las tres palancas del curso:

- **`/compact`** para seguir con la misma funcionalidad · **`/clear`** para empezar otra · **`/context`** para ver qué te lo está comiendo.
- **Sé específico.** Un prompt vago no ahorra contexto: obliga a Claude a explorar y razonar más, y **gasta mucho más**.
- **Delega en subagentes.** Contexto aislado, y solo te vuelve el resumen.

### 4 · Las cuatro formas de personalizarlo

| | Qué es | Cuándo actúa |
|---|---|---|
| **CLAUDE.md** | Memoria persistente del proyecto | Se lee **al inicio de cada sesión** |
| **Subagentes** | Agentes con contexto aislado | Cuando Claude delega una tarea |
| **Skills** | Procedimientos empaquetados | Cuando Claude decide que aplica (solo nombre+descripción en contexto) |
| **MCP** | Conexión a herramientas y datos externos | Cuando la consulta lo pide (**todas** las tools en contexto) |
| **Hooks** | Comandos en el ciclo de vida | **Siempre. Son deterministas** |

La frase que resume el capítulo 12: **si algo tiene que pasar siempre y sin fallo, no lo pongas en un prompt, ponlo en un hook.**

## Sobre el material

Este curso es **de vídeo con texto de apoyo**: cada lección tiene su vídeo y su contenido escrito completo. Estos resúmenes se han elaborado directamente de ahí.

**Excepción:** la lección **Skills** no tiene texto en la plataforma — solo el vídeo y un enlace al curso dedicado. El [capítulo 10](10-skills.md) lo dice explícitamente y recoge lo que el resto del curso sí afirma sobre las skills, sin inventar el hueco.

**El curso sí tiene quiz oficial** (7 preguntas, de las que 4 son evaluables). El [capítulo 13](13-repaso-y-quiz.md) recoge las preguntas reales con sus distractores, más un banco extra de 24 preguntas sobre lo que el oficial no toca.
