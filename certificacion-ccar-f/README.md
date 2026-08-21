# Claude Certified Architect – Foundations (CCAR-F)

Guía completa en español de la certificación, construida a partir del **Exam Guide oficial v1.0** (efectiva julio 2026) y de la información pública de la Anthropic Partner Academy.

> **No es un curso de la Anthropic Academy.** Es la guía de certificación hacia la que apuntan los cursos que hay resumidos en este repo. Si buscas los cursos, están en el [índice del repositorio](../README.md).

**[▶ certificacion-interactiva.html](certificacion-interactiva.html)** — todo esto en una página que se abre con doble clic: blueprint interactivo, los 30 task statements navegables, simulacro de 60 preguntas por dominio con historial, flashcards y panel de preparación.

---

## Índice

| # | Capítulo | Qué hay dentro |
|---|---|---|
| 1 | [La certificación](01-la-certificacion.md) | Ficha técnica, blueprint, puntuación, registro, políticas, repeticiones, renovación |
| 2 | [Dominio 1 — Agentic Architecture & Orchestration](02-dominio-1-arquitectura-agentica.md) | **27 %** · 7 task statements. Bucles agénticos, coordinador-subagente, `Task`, hooks, descomposición, sesiones |
| 3 | [Dominio 2 — Tool Design & MCP Integration](03-dominio-2-herramientas-y-mcp.md) | **18 %** · 5 task statements. Descripciones de tool, errores estructurados, `tool_choice`, `.mcp.json`, tools integradas |
| 4 | [Dominio 3 — Claude Code Configuration & Workflows](04-dominio-3-claude-code.md) | **20 %** · 6 task statements. Jerarquía de `CLAUDE.md`, commands, skills, reglas por ruta, plan mode, CI/CD |
| 5 | [Dominio 4 — Prompt Engineering & Structured Output](05-dominio-4-prompting-y-salida-estructurada.md) | **20 %** · 6 task statements. Criterios explícitos, few-shot, JSON schemas, validación, batch, multi-pasada |
| 6 | [Dominio 5 — Context Management & Reliability](06-dominio-5-contexto-y-fiabilidad.md) | **15 %** · 6 task statements. Case facts, lost-in-the-middle, escalado, propagación de errores, confianza, procedencia |
| 7 | [Los seis escenarios](07-los-seis-escenarios.md) | Los 6 escenarios publicados, qué pregunta cada uno, y el mapa escenario ↔ dominio |
| 8 | [Las 12 preguntas oficiales](08-preguntas-oficiales.md) | Las preguntas de muestra de la guía, con opciones y explicación oficial |
| 9 | [Plan de estudio](09-plan-de-estudio.md) | Preparación oficial, 4 ejercicios, mapa curso ↔ dominio, huecos del repo, temas dentro y fuera de alcance |

---

## El hilo conductor

El CCAR-F **no pregunta sintaxis**. Pregunta **criterio de arquitectura**: te da un problema de producción con síntomas concretos y cuatro arreglos plausibles, y tienes que elegir el que ataca la causa raíz con el esfuerzo proporcionado.

Léete las [12 preguntas de muestra](08-preguntas-oficiales.md) y el sesgo salta a la vista. El examen premia:

- **El arreglo más simple que funciona.** Mejorar una descripción de tool gana a montar una capa de routing.
- **Determinismo cuando el resultado lo exige.** Reembolsos y verificación de identidad se garantizan con **hooks y puertas programáticas**, no con instrucciones de prompt.
- **Diagnosticar dónde está el fallo de verdad.** Si cada subagente hizo bien su trabajo pero el informe está incompleto, el culpable es **la descomposición del coordinador**.

Y castiga tres cosas de forma sistemática: sobreingeniería, confiar en lo probabilístico donde hace falta garantía, y culpar a componentes que funcionan bien.

---

## Los números que hay que saberse

| | |
|---|---|
| **60** | ítems |
| **120** | minutos |
| **4 de 6** | escenarios, al azar |
| **720** | nota de corte, sobre escala **100–1.000** |
| **125 USD** | tasa, por intento |
| **12 meses** | validez |
| **14 / 30 / 90** | días de espera tras el 1.º, 2.º y 3.º suspenso |
| **4** | intentos máximos en 12 meses |
| **27 / 18 / 20 / 20 / 15** | pesos de los dominios 1 a 5, en % |

---

## Fuentes

- [Claude Certified Architect – Foundations Exam Guide (PDF, v1.0)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf) — el documento autoritativo
- [Partner Certifications](https://anthropic-partners.skilljar.com/page/partner-certifications) — las cuatro credenciales, precios y prep paths
- [Prep courses de CCAR-F](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
- [Pearson VUE · Anthropic](https://www.pearsonvue.com/us/en/anthropic.html) — agenda, resultados, soporte

---

## Aviso

Guía de estudio derivada de la documentación pública de certificación de Anthropic, redactada en español. **La guía oficial es la única referencia autoritativa** y puede cambiar sin previo aviso — comprueba siempre la versión vigente antes de registrarte. Este repositorio **no está afiliado ni respaldado por Anthropic PBC**.

El contenido del examen real está bajo acuerdo de confidencialidad. Aquí no hay ni habrá preguntas reales del examen: solo las **12 de muestra que la propia guía publica** y una autoevaluación construida a partir de los objetivos del blueprint.
