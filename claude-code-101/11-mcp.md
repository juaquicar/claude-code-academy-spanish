# 11 — MCP

*15 minutos* · [Vídeo](https://www.youtube.com/embed/kkBFmwkDzdo)

**Al terminar sabrás:** qué resuelve MCP · los dos tipos de servidor y los tres alcances · cuánto contexto cuestan · el umbral del 10 % que activa el modo de búsqueda de tools.

---

**Model Context Protocol (MCP) es un estándar abierto** que permite a Claude Code conectarse a **herramientas y fuentes de datos externas**. Cuando haces una pregunta, Claude entiende automáticamente cuándo debe usar esas tools para atenderla mejor.

> Buena parte de tu contexto **vive fuera de tu base de código** — en bases de datos, apps de productividad o repositorios públicos. **MCP salva esa distancia.**

## Qué puedes hacer con él

Primero conviene entender el concepto de "tools" en la IA agéntica: **las tools dan a agentes como Claude Code la capacidad de ejecutar acciones** que les ayudan a completar tareas de forma más efectiva. Esto es distinto de la IA típica, donde solo recibes una respuesta de texto.

Ejemplos:

- Si tu equipo usa **Linear** para gestión de proyectos, puedes añadir un servidor MCP de Linear para traer los detalles de tus issues concretos.
- Si necesitas **documentación actualizada** de una dependencia, un servidor MCP de docs como **Context7** puede proporcionársela a Claude Code.

## Añadir un servidor MCP

Los servidores se añaden con el comando `claude mcp add`. Hay **dos tipos principales**:

| Tipo | Para qué |
|---|---|
| **HTTP servers** | Servicios **remotos**, alojados por el proveedor, conectados por red |
| **Stdio servers** | **Procesos locales** que corren en tu máquina |

Puedes gestionarlos con **`/mcp`** dentro de una sesión de Claude Code: ver qué está conectado, comprobar el estado y **desactivar los que no necesites**.

## Alcances

Los servidores MCP se pueden acotar de **tres formas**:

1. **Local** — disponible solo en el proyecto actual, solo para ti.
2. **User** — disponible en **todos** tus proyectos.
3. **Project** — usa un fichero **`.mcp.json`** que versionas en el repositorio, para que **cualquiera que trabaje en el código obtenga exactamente los mismos servidores automáticamente**.

## El coste en contexto

Los servidores MCP **añaden definiciones de tools a tu ventana de contexto, incluso cuando no las estás usando**. Si tienes muchos servidores configurados, eso se come tu contexto disponible. Ejecuta `/mcp` para ver qué hay conectado y desactivar lo que no uses.

Tres alternativas más baratas en contexto:

- **Si una tool tiene equivalente en CLI** (como `gh` para GitHub o `aws` para AWS), **la CLI es más eficiente en contexto** porque no añade definiciones de tools persistentes.
- **Una Skill**, que carga en contexto solo nombre y descripción, y **el contenido completo solo cuando Claude determina que necesita usarla**.
- **Desactivar** sin más lo que no esté en uso.

> **El número que hay que recordar:** si tus tools de MCP **superan el 10 % de tu ventana de contexto**, Claude Code cambia automáticamente a **tool search mode**, que descubre las tools adecuadas bajo demanda — **aunque puede que no funcione de forma tan fiable**.

## Conclusiones

MCP conecta Claude Code con tus herramientas y fuentes de datos externas. Añade servidores con `claude mcp add`. Acótalos a tu proyecto con `.mcp.json` para que tu equipo los reciba automáticamente. Y **vigila el consumo de contexto** desactivando los servidores que no estés usando activamente.

> **¿Quieres profundizar?** Los cursos dedicados: [Introduction to MCP](../introduction-to-model-context-protocol/README.md) y [MCP: Advanced Topics](../model-context-protocol-advanced-topics/README.md).
