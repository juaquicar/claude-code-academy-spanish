# 05 — Compartir skills

*20 minutos* · [Vídeo](https://www.youtube.com/embed/OCBi3eScNLk)

**Al terminar sabrás:** compartir skills con tu equipo por Git · distribuirlas entre proyectos con plugins y marketplaces · desplegarlas a toda la organización con managed settings · configurar subagentes propios para que usen skills concretas.

---

> Una skill de revisión de PR que solo usas tú es útil. **Esa misma skill compartida con todo tu equipo estandariza la revisión de código** y crea una experiencia consistente en toda la organización.

## Los tres métodos de distribución

| Método | Alcance | Cuándo |
|---|---|---|
| **Commit al repositorio** | Tu equipo | Estándares del equipo, flujos del proyecto |
| **Plugins y marketplaces** | La comunidad | Skills no demasiado específicas del proyecto |
| **Enterprise managed settings** | Toda la organización | Estándares **obligatorios** |

---

### 1 · Commit al repositorio

El método más simple. Las pones en **`.claude/skills`** y **cualquiera que clone el repo las obtiene automáticamente** — sin instalación extra. Cuando publicas actualizaciones, todos las reciben en el siguiente pull.

Funciona bien para:

- Estándares de código del equipo
- Flujos específicos del proyecto
- Skills que **referencian la estructura de tu codebase**

> El directorio `.claude` contiene tus **agentes, hooks, skills y settings** — todo versionado y compartido con el equipo por flujos de Git normales.

### 2 · Plugins

Los plugins extienden Claude Code con funcionalidad propia, pensada para compartirse entre equipos y proyectos.

En tu proyecto de plugin, crea un directorio **`skills`** que siga una estructura similar a la del directorio `.claude`: **cada skill en su propia carpeta con un `SKILL.md` dentro**.

Tras distribuir el plugin a un marketplace, otros usuarios pueden descubrirlo e instalarlo.

> Este enfoque es el mejor **cuando tus skills no son demasiado específicas del proyecto** y pueden ser útiles a gente más allá de tu equipo.

### 3 · Enterprise managed settings

Los administradores pueden desplegar skills a toda la organización. **Las skills enterprise tienen la máxima prioridad**: sobrescriben a las personales, de proyecto y de plugin con el mismo nombre.

El fichero de managed settings soporta cosas como **`strictKnownMarketplaces`**, para controlar desde dónde se pueden instalar plugins:

```json
"strictKnownMarketplaces": [
  {
    "source": "github",
    "repo": "acme-corp/approved-plugins"
  },
  {
    "source": "npm",
    "package": "@acme-corp/compliance-plugins"
  }
]
```

> Es la opción correcta para **estándares obligatorios**, requisitos de seguridad, flujos de cumplimiento y prácticas de código que **deben** ser consistentes en toda la organización. **La palabra clave es "deben".**

---

## Skills y subagentes

> ### ⚠ Esto sorprende a mucha gente
>
> **Los subagentes NO ven tus skills automáticamente.** Cuando delegas una tarea a un subagente, **arranca con un contexto limpio y nuevo**.

Tres distinciones importantes:

| | ¿Puede usar skills? |
|---|---|
| **Agentes integrados** (Explorer, Plan, Verify) | ❌ **No pueden acceder a skills en absoluto** |
| **Subagentes propios** que defines tú | ✅ Sí, **pero solo si las listas explícitamente** |

Y un matiz de comportamiento: **en un subagente las skills se cargan al arrancar**, no bajo demanda como en la conversación principal.

### Cómo configurarlo

Añade un fichero markdown de agente en **`.claude/agents`**. Puedes usar el comando **`/agents`** de Claude Code para crearlo de forma interactiva.

El fichero generado incluye un campo **`skills`** que lista cuáles cargar:

```yaml
---
name: frontend-security-accessibility-reviewer
description: "Use this agent when you need to review frontend code for accessibility..."
tools: Bash, Glob, Grep, Read, WebFetch, WebSearch, Skill...
model: sonnet
skills: accessibility-audit, performance-check
---
```

Al delegar a ese subagente, **tiene ambas skills cargadas** y las aplica a cada revisión.

**El orden:** primero asegúrate de que las skills existen en tu `.claude/skills`, luego crea el subagente o añade el campo `skills` a uno existente.

Este patrón funciona muy bien cuando:

- Quieres **delegación aislada con experiencia concreta**
- **Distintos subagentes necesitan distintas skills** — revisor de frontend vs. revisor de backend
- Quieres **imponer estándares en el trabajo delegado sin depender de los prompts**

## Reflexión

- ¿Qué método de distribución tiene más sentido para las skills que has estado pensando construir?
- ¿Tienes flujos donde subagentes propios con skills concretas mejorarían la consistencia del trabajo delegado?
