# 10 — Skills

*5 minutos* · [Vídeo](https://www.youtube.com/embed/bjdBVZa66oU)

> **Aviso sobre el material.** Esta lección del curso **no tiene contenido escrito**: en la plataforma es únicamente el vídeo más un enlace al curso dedicado. Lo que sigue **no es un resumen del vídeo**, sino lo que el propio Claude Code 101 dice sobre las skills en sus otras lecciones. Para el temario completo hay curso propio.

---

## Lo que este curso dice de las skills

**En [gestión del contexto](06-gestion-del-contexto.md):** las skills se presentan como la alternativa a los servidores MCP cuando el problema es el contexto. Los servidores MCP cargan todas sus tools en contexto por defecto; **las skills no lo cargan todo de entrada**.

**En [MCP](11-mcp.md):** la mecánica exacta. Una skill tiene **un nombre y una descripción cargados en contexto**, y **Claude solo carga el contenido completo de la skill cuando determina que necesita usarla**.

**En [revisión de código](07-revision-de-codigo.md):** `/commit-push-pr` es una skill — resuelve commit, push y creación de PR en un solo paso.

**En [subagentes](09-subagentes.md):** puedes **precargar skills** en un subagente con la clave `skill`, listándolas por nombre. Con una diferencia importante: ahí **la skill entera se carga en contexto**, al contrario que en la conversación principal.

## La regla que se deduce

| | Qué se carga al arrancar | Cuándo se carga el resto |
|---|---|---|
| **Servidor MCP** | **Todas** las definiciones de tools | — (ya está todo dentro) |
| **Skill** | Solo **nombre y descripción** | Cuando Claude decide que la necesita |

Por eso el curso propone las skills como sustituto de un servidor MCP que te está comiendo contexto sin que lo uses.

> **¿Quieres profundizar?** El curso dedicado: [Introduction to agent skills](https://anthropic.skilljar.com/introduction-to-agent-skills) — y su [resumen en este repo](../introduction-to-agent-skills/README.md).
