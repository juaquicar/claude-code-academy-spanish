# Claude Code in Action — Anthropic Academy

Curso: https://anthropic.skilljar.com/claude-code-in-action

**Idea central:** llevar Claude Code más allá de la tarea rápida y poder *confiar* en el resultado. Cubre acotar sesiones largas, configurar Claude con instrucciones que sí se cumplen, automatizar trabajo repetitivo y verificar ejecuciones sin supervisión.

**Público:** desarrolladores que ya usan Claude Code con prompts sueltos y quieren pasar a flujos largos, menos supervisados y compartidos por todo el equipo.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página web: diagramas interactivos, diales, 35 flashcards, las 8 preguntas reales del quiz oficial más 15 de repaso, con corrección al momento, seguimiento de progreso, buscador y tema claro/oscuro. Se abre con doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Sección |
|---|----------|---------|
| 01 | [Dirigir sesiones largas](01-dirigir-sesiones-largas.md) | Steer the Work |
| 02 | [Un CLAUDE.md que se cumple](02-claude-md-que-se-cumple.md) | Configure Claude |
| 03 | [Skills de verificación](03-skills-de-verificacion.md) | Configure Claude |
| 04 | [Modos de permisos](04-modos-de-permisos.md) | Configure Claude |
| 05 | [Hooks](05-hooks.md) | Configure Claude |
| 06 | [Routines y modo headless](06-routines-y-headless.md) | Automate Repeat Work |
| 07 | [GitHub Actions y Code Review](07-github-actions-y-code-review.md) | Automate Repeat Work |
| 08 | [Verificar ejecuciones no supervisadas](08-verificar-ejecuciones-no-supervisadas.md) | Verify and Share |
| 09 | [Plugins](09-plugins.md) | Verify and Share |
| 10 | [Quiz del curso](10-quiz.md) — **8/8, superado** | Quiz |

## Hilo conductor del curso

Tres superficies de instrucción, cada una con su trabajo:

| Superficie | Qué es | Cuándo usarla |
|---|---|---|
| `CLAUDE.md` | Guía, no configuración obligatoria | Convenciones que aplican siempre (nombres, ubicación de ficheros) |
| Skills | Procedimientos empaquetados, se cargan bajo demanda | Recetas ligadas a un tipo de tarea concreto |
| Hooks | Código determinista que se ejecuta | Reglas que Claude **no puede** saltarse |

Regla de oro: si saltarse la regla no es aceptable, no la dejes en manos de "seguir instrucciones" — hook.

Y el cierre: **verifica en proporción a la cuerda que diste**. Cuanto menos miraste, más verificas.
