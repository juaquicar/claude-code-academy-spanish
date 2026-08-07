# Introduction to Agent Skills — Anthropic Academy

Curso: https://anthropic.skilljar.com/introduction-to-agent-skills

**Idea central:** una skill es un fichero markdown que le enseña a Claude cómo hacer algo **una vez**, y que Claude aplica **automáticamente** cuando viene al caso.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: constructor de `SKILL.md` en vivo, comparador de las cinco funcionalidades de personalización, diagrama de prioridades, diagnosticador de problemas y flashcards. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Tiempo |
|---|----------|--------|
| 01 | [¿Qué son las skills?](01-que-son-las-skills.md) | 15 min |
| 02 | [Crear tu primera skill](02-crear-tu-primera-skill.md) | 20 min |
| 03 | [Configuración y skills multi-fichero](03-configuracion-y-multi-fichero.md) | 20 min |
| 04 | [Skills vs. otras funcionalidades](04-skills-vs-otras-funcionalidades.md) | 15 min |
| 05 | [Compartir skills](05-compartir-skills.md) | 20 min |
| 06 | [Solución de problemas](06-solucion-de-problemas.md) | 15 min |
| 07 | [Repaso y autoevaluación](07-repaso-y-quiz.md) | — |

## El hilo conductor

> **Cada vez que le explicas a Claude los estándares de código de tu equipo, te estás repitiendo.** En cada revisión de PR vuelves a describir cómo quieres el feedback. En cada commit le recuerdas tu formato preferido.
>
> **Las skills arreglan eso.**

### La regla de oro

**Si te encuentras explicándole lo mismo a Claude una y otra vez, eso es una skill esperando a ser escrita.**

### Lo que distingue a una skill

Claude Code tiene varias formas de personalizarse. Las skills son únicas porque son **automáticas y específicas de una tarea**:

| | Cuándo se carga | Cómo se activa |
|---|---|---|
| **CLAUDE.md** | En **todas** las conversaciones | Siempre |
| **Skills** | **Bajo demanda**, al coincidir con tu petición | Claude reconoce la situación |
| **Slash commands** | Al invocarlos | **Los escribes tú** |

Al arrancar, Claude **solo carga el nombre y la descripción** de cada skill, no su contenido. Por eso no llenan tu ventana de contexto: tu checklist de revisión de PR no tiene por qué estar en contexto mientras depuras.

### La descripción lo es todo

Es el campo del que depende absolutamente todo el curso:

- **Decide si la skill se activa** — Claude compara tu petición con las descripciones disponibles mediante **coincidencia semántica**.
- Cuando algo falla, **el problema casi siempre está ahí** — la lección 6 lo confirma.

Una buena descripción responde **dos preguntas: qué hace la skill y cuándo debe usarla Claude.**

## Sobre el material

A diferencia de otros cursos de la academia, **este es de texto**: cada lección tiene su vídeo pero también el contenido escrito completo, con objetivos de aprendizaje, conclusiones clave y preguntas de reflexión. Estos resúmenes se han elaborado directamente de ahí.

**El curso no tiene quiz oficial.** El capítulo 07 es una autoevaluación construida a partir del material.
