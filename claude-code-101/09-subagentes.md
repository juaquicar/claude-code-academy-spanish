# 09 — Subagentes

*10 minutos* · [Vídeo](https://www.youtube.com/embed/jKErNxuxPXg)

**Al terminar sabrás:** qué gana tu contexto al delegar en un subagente · cómo crear uno con `/agents` · qué son la memoria persistente y las skills precargadas.

---

Claude puede **delegar tareas en subagentes** que las descomponen y ejecutan sus partes en paralelo, mejorando tu gestión del contexto. **Cada subagente opera en su propia ventana de contexto aislada.**

## Cómo funciona

Gestionar el contexto en Claude Code es importante. Buena parte de la ventana se consume en cosas como llamadas a tools explorando tu base de código o búsquedas web de investigación. **Lo que Claude descubre durante esa exploración no siempre es relevante** para la funcionalidad principal que estás desarrollando.

Aquí entran los subagentes. Claude lanza un subagente para una tarea como "explórame esta base de código". El subagente:

1. Corre **en paralelo, con su propia ventana de contexto**.
2. Hace todo el trabajo de exploración.
3. Al terminar, **resume sus hallazgos** y devuelve ese resumen a Claude.

> **El resultado:** obtienes la respuesta que buscabas, **sin que todo el viaje que hizo falta para llegar a ella ensucie tu contexto principal**.

## Crear tu propio subagente

Los subagentes se definen en **ficheros Markdown con frontmatter YAML**. La forma más fácil de empezar es dejar que Claude te genere uno. Ejecuta:

```
/agents
```

Luego selecciona **"Create new agent"**. Pasarás por unos pasos: elegir el **alcance** del agente, definir su **propósito**, seleccionar las **tools** a las que tiene acceso e incluso escoger un **color**.

Claude generará un **nombre, una descripción y un prompt** para el subagente. Esto también le dice a Claude **cuándo llamar al subagente** en función de los prompts que le des.

## Personalización adicional

Los subagentes se pueden personalizar más. Dos puntos destacados:

- **Memoria persistente** — permite que tu subagente **retenga memoria entre conversaciones**. Útil si lo usas de forma consistente en los mismos proyectos.
- **Precargar skills** — añadiendo la clave **`skill`** y listando las skills por nombre. **Ojo:** a diferencia de las skills en tu conversación principal, aquí **la skill entera se carga en contexto**.

## Conclusiones

Mantener limpia tu ventana de contexto es una de las mejores formas de seguir siendo productivo con Claude Code. Con los subagentes puedes ejecutar un agente en segundo plano que se encargue del trabajo pesado y **devuelva solo la respuesta** a tu ventana de contexto principal.

> **¿Quieres profundizar?** El curso dedicado: [Introduction to subagents](https://anthropic.skilljar.com/introduction-to-subagents) — y su [resumen en este repo](../introduction-to-subagents/README.md).
