# 02 — Crear tu primera skill

*20 minutos* · [Vídeo](https://www.youtube.com/embed/Wx6_vjFFyHM)

**Al terminar sabrás:** crear una skill desde cero con el frontmatter correcto · probar y verificar que carga · explicar cómo empareja Claude las peticiones con las skills disponibles · describir la jerarquía de prioridad.

---

## Crear la skill

Vamos a construir una skill **personal** que enseña a Claude a escribir descripciones de PR en un formato consistente. Al ser personal, vive en tu directorio home y funciona en todos tus proyectos.

**Paso 1 — crea el directorio.** El nombre del directorio debe coincidir con el nombre de la skill:

```bash
mkdir -p ~/.claude/skills/pr-description
```

**Paso 2 — crea el `SKILL.md` dentro.** Tiene dos partes separadas por las líneas de guiones del frontmatter:

```markdown
---
name: pr-description
description: Writes pull request descriptions. Use when creating a PR, writing a PR, or when the user asks to summarize changes for a pull request.
---

When writing a PR description:

1. Run `git diff main...HEAD` to see all changes on this branch
2. Write a description following this format:

## What
One sentence explaining what this PR does.

## Why
Brief context on why this change is needed

## Changes
- Bullet points of specific changes made
- Group related changes together
- Mention any files deleted or renamed
```

| Parte | Qué hace |
|---|---|
| **`name`** | Identifica tu skill |
| **`description`** | **Le dice a Claude cuándo usarla — es el criterio de emparejamiento** |
| Todo tras el segundo grupo de guiones | Las instrucciones que Claude sigue cuando la skill se activa |

## Probarla

> **Claude Code carga las skills al arrancar**, así que **reinicia la sesión** después de crear una.

Verifica que está disponible consultando la lista de skills. Para probarla, haz cambios en una rama y di algo como *"write a PR description for my changes"*. Claude indicará que está usando la skill, mirará tu diff y escribirá la descripción siguiendo tu plantilla — **el mismo formato siempre**.

## Cómo funciona el emparejamiento

Cuando Claude Code arranca, **escanea cuatro ubicaciones** buscando skills, pero **solo carga el nombre y la descripción**, no el contenido completo. Es un detalle importante.

Cuando envías una petición, Claude la compara con las descripciones de todas las skills disponibles.

> **Es coincidencia semántica, no de palabras exactas.** *"explain what this function does"* emparejaría con una skill descrita como *"explain code with visual diagrams"*, porque **la intención se solapa**.

Una vez encontrada la coincidencia, **Claude te pide confirmación** antes de cargarla. Ese paso te mantiene consciente de qué contexto está incorporando. Tras confirmar, lee el `SKILL.md` completo y sigue sus instrucciones.

## Prioridad de skills

Si clonas un repositorio que tiene una skill con el mismo nombre que una tuya personal, ¿cuál gana?

| Orden | Nivel | Ubicación |
|---|---|---|
| **1** | **Enterprise** | Managed settings — **máxima prioridad** |
| **2** | **Personal** | `~/.claude/skills` |
| **3** | **Project** | `.claude/skills` del repositorio |
| **4** | **Plugins** | Plugins instalados — **mínima prioridad** |

> Esto permite a las organizaciones **imponer estándares** mediante skills enterprise, sin dejar de permitir la personalización individual. Si tu empresa tiene una skill enterprise `code-review` y tú creas una personal con el mismo nombre, **gana la de la empresa**.

**Para evitar conflictos, usa nombres descriptivos.** En vez de `review`, algo como `frontend-review` o `backend-review`.

## Actualizar y eliminar

- **Actualizar** → edita su `SKILL.md`.
- **Eliminar** → borra su directorio.
- **En ambos casos → reinicia Claude Code** para que los cambios surtan efecto.

## Reflexión

- ¿Qué tarea de tu flujo diario podrías convertir en skill ahora mismo? ¿Cómo sería su descripción?
- ¿Cómo afecta la jerarquía de prioridad a la estrategia de tu equipo? ¿Te apoyarías más en skills personales o de proyecto?
