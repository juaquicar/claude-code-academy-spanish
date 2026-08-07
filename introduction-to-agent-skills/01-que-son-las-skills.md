# 01 — ¿Qué son las skills?

*15 minutos* · [Vídeo](https://www.youtube.com/embed/bjdBVZa66oU)

**Al terminar sabrás:** qué son las skills y cómo funcionan · dónde viven (personales vs. de proyecto) · en qué se distinguen de CLAUDE.md y de los slash commands · en qué escenarios son la herramienta de personalización correcta.

---

## El problema

> Cada vez que le explicas a Claude los estándares de código de tu equipo, **te estás repitiendo**. En cada revisión de PR vuelves a describir cómo quieres el feedback estructurado. En cada commit le recuerdas tu formato preferido.

**Una skill es un fichero markdown que le enseña a Claude cómo hacer algo una vez.** Claude aplica ese conocimiento **automáticamente** siempre que sea relevante.

## Qué son

Las skills son **carpetas de instrucciones y recursos** que Claude Code puede descubrir y usar para resolver tareas con más precisión. Cada skill vive en un fichero **`SKILL.md`** con un nombre y una descripción en su frontmatter.

```yaml
---
name: pr-review
description: Reviews pull requests for code quality. Use when reviewing PRs or checking code changes.
---
```

Bajo el frontmatter escribes las instrucciones reales: tu checklist de revisión, tus preferencias de formato, o lo que Claude necesite saber para esa tarea.

> **La descripción es cómo Claude decide si usar la skill.** Cuando le pides revisar un PR, compara tu petición con todas las descripciones disponibles y activa las que encajan.

## Dónde viven

| Tipo | Ubicación | Alcance |
|---|---|---|
| **Personales** | `~/.claude/skills` | **Te siguen a todos tus proyectos** — tu estilo de mensajes de commit, tu formato de documentación, cómo te gusta que te expliquen el código |
| **De proyecto** | `.claude/skills` en la raíz del repositorio | **Cualquiera que clone el repo las obtiene automáticamente** — aquí viven los estándares de equipo, las guías de marca de tu empresa, las tipografías y colores para diseño web |

En Windows, las personales están en `C:/Users/<tu-usuario>/.claude/skills`.

Las de proyecto **se versionan junto al código**, así que todo el equipo las comparte.

## Skills vs. CLAUDE.md vs. slash commands

Las skills son únicas porque son **automáticas y específicas de una tarea**.

| | Cuándo se carga | Quién la dispara |
|---|---|---|
| **CLAUDE.md** | En **todas** las conversaciones | Siempre está |
| **Skills** | **Bajo demanda**, al coincidir con tu petición | **Claude**, al reconocer la situación |
| **Slash commands** | Al invocarlos | **Tú, escribiéndolos explícitamente** |

> **El detalle que las hace baratas:** al arrancar, Claude **solo carga el nombre y la descripción**, no el contenido. Por eso no llenan tu ventana de contexto. Tu checklist de revisión de PR no tiene por qué estar en contexto mientras depuras: se carga cuando pides una revisión de verdad.

Si quieres que Claude use siempre el modo estricto de TypeScript, eso va en **CLAUDE.md**.

Cuando Claude empareja una skill con tu petición, **lo ves cargarse en el terminal**.

## Cuándo usar skills

Funcionan mejor para **conocimiento especializado que aplica a tareas concretas**:

- Estándares de revisión de código de tu equipo
- Formatos de mensaje de commit que prefieres
- Guías de marca de tu organización
- Plantillas de documentación para tipos concretos de documento
- Checklists de depuración para frameworks concretos

> ### La regla de oro
>
> **Si te encuentras explicándole lo mismo a Claude una y otra vez, eso es una skill esperando a ser escrita.**

## Reflexión

- Piensa en tus interacciones recientes con Claude Code. ¿Qué instrucciones te viste repitiendo? ¿Cuánto tiempo te habría ahorrado una skill?
- Piensa en el flujo de trabajo de tu equipo. ¿Qué estándares o procesos se beneficiarían más de estar codificados como skills?
