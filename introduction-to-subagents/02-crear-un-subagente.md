# 02 — Crear un subagente

[Vídeo](https://www.youtube.com/embed/arD6qEWa2Xc)

Los subagentes propios se especializan en tareas concretas — revisar código, escribir tests, comprobar documentación. Se definen como **ficheros markdown con frontmatter YAML** que le dicen a Claude **cuándo** usar el subagente y **cómo** debe comportarse.

## El flujo de creación

La forma más fácil es el slash command **`/agents`**, que abre la interfaz principal de gestión de subagentes. Desde ahí, **Create new agent**.

### 1 · Elegir el ámbito

| Ámbito | Alcance |
|---|---|
| **Project-level** | Solo disponible en el proyecto actual |
| **User-level** | Compartido entre todos los proyectos de tu máquina |

### 2 · Elegir cómo crearlo

Puedes escribir la configuración a mano, pero **lo recomendado es dejar que Claude la genere**: describes qué quieres que haga el subagente y Claude produce el `name`, la `description` y el system prompt a partir de eso.

### 3 · Personalizar las herramientas

Durante la creación puedes ajustar a qué herramientas accede. Categorías:

- Read-only tools
- Edit tools
- Execution tools
- MCP tools
- Other tools

> **Piensa en lo que el subagente realmente necesita.** Un revisor de código probablemente **no necesita edit tools** — debe leer y analizar, no cambiar. Aunque sí puede interesar dejarle **execution tools** activas para que identifique más fácilmente los cambios pendientes.

### 4 · Elegir modelo

| Opción | Cuándo |
|---|---|
| **Haiku** | Tareas rápidas y ligeras |
| **Sonnet** | Buen término medio entre velocidad y profundidad |
| **Opus** | Análisis complejo |
| **Inherit** | Usa el modelo que esté corriendo tu conversación principal |

### 5 · Elegir color

Aparece en la interfaz para que sepas de un vistazo qué subagente está activo. Detalle pequeño, pero ayuda cuando tienes varios corriendo.

## El fichero de configuración

Al terminar, el config se guarda en tu proyecto, típicamente en **`.claude/agents/tu-agente.md`**:

```markdown
---
name: code-quality-reviewer
description: Use this agent when you need to review recently written or modified code for quality, security, and best practice compliance.
tools: Bash, Glob, Grep, Read, WebFetch, WebSearch
model: sonnet
color: purple
---

You are an expert code reviewer specializing in quality assurance, security best practices, and
adherence to project standards. Your role is to thoroughly examine recently written or modified code
and identify issues that could impact reliability, security, maintainability, or performance.
```

### Los campos

| Campo | Qué hace |
|---|---|
| **`name`** | Identificador único. Así lo referencias: pidiéndoselo a Claude directamente o escribiendo **`@agent code-quality-reviewer`** en tu mensaje. |
| **`description`** | **Controla cuándo decide Claude usar el subagente.** Debe ser **una sola línea** (usa `\n` escapado si necesitas saltos). Puedes incluir aquí conversaciones de ejemplo para que Claude entienda cuándo delegar. |
| **`tools`** | Qué herramientas puede usar. Coincide con lo que seleccionaste al generarlo, pero **puedes editar la lista aquí cuando quieras**. |
| **`model`** | `sonnet`, `opus`, `haiku` o `inherit`. |
| **`color`** | Color de identificación en la interfaz. |

## El system prompt

**El cuerpo del markdown** (todo lo que hay bajo el frontmatter YAML) **es el system prompt**. Ahí le das las instrucciones: en qué debe centrarse, cómo debe analizar y **cómo debe reportar los hallazgos** de vuelta al agente principal.

> Un system prompt bien escrito es la diferencia entre un subagente útil y uno que no pilla el punto. Sé específico sobre **qué debe buscar** y **cómo debe estructurar su salida**.

## Que Claude lo use automáticamente

Si quieres que Claude delegue sin que se lo pidas explícitamente, incluye la palabra **"proactively"** en el campo `description`:

```
description: Proactively suggest running this agent after major code changes...
```

También puedes añadir **conversaciones de ejemplo** a la description para que Claude entienda escenarios concretos donde debe usarse. **Cuanto más concretos los ejemplos, mejor sabe Claude cuándo delegar.**

## Probarlo

Después de crearlo, pruébalo: haz algunos cambios de código y pídele a Claude que los revise.

> Si el subagente **no se está usando** cuando esperas que se use, **vuelve a la `description`**. Añadir ejemplos más específicos y escenarios de disparo es lo que ayuda a Claude a entender cuándo delegarle el trabajo.
