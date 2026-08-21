# 09 — MCP

*15 minutos* · [Vídeo](https://www.youtube.com/embed/hftmYd97LBw)

**Al terminar sabrás:** qué problema resuelve MCP y de quién es el problema · la regla de tres para elegir entre tools, skills y MCP · cómo se declara una conexión y se concede acceso · cómo dejar un servidor en solo lectura.

---

Tenemos tools, skills y conectores. ¿Entonces por qué existe **MCP**? A primera vista parece **una segunda API encima de la API**. Pregunta justa — y la respuesta se reduce a **quién mantiene el código de integración**.

## El problema de mantenimiento

Digamos que tu agente necesita sacar tareas de Asana, mirar un Google Calendar y buscar en Slack, todo de una vez. Con tools personalizadas tienes que escribir **tres integraciones**. Eso es factible. **La parte dolorosa viene después: también tienes que mantenerlas** cada vez que uno de esos servicios cambia su API, lo que pasa a menudo. Enhorabuena, ahora mantienes **una pila de envoltorios de APIs de terceros**.

> **MCP traslada ese mantenimiento al proveedor del servicio.** Asana publica un servidor MCP. Slack publica el suyo. Google el suyo. Cada servidor expone sus propias tools — con descripciones, schemas y autenticación — **a través de un protocolo estándar**. Cuando su API cambia, ellos actualizan su servidor. **Tú no cambias nada.**

## Tools vs. skills vs. MCP

| | Para qué | Quién mantiene |
|---|---|---|
| **Tools** | Conectar Claude con **tus sistemas internos**: tu base de datos, tu gestor de proyectos, tus APIs propias | **Tú** — tuyo el código, tuyo el mantenimiento |
| **Skills** | Enseñarle a Claude **un procedimiento**: tu plantilla de informe, tu checklist de revisión. Son instrucciones, no necesariamente integraciones | Tú |
| **MCP** | Conectar Claude con **servicios de terceros** | **El proveedor del servicio.** Tú no escribes el envoltorio de Asana — lo hizo Asana |

> **La versión corta: las tools son para tus cosas, las skills para tus procesos, y MCP para las cosas de todos los demás.**

## Conectarse a un servidor MCP

La forma más limpia de cogerle el tacto es apuntar Claude a cualquier servidor MCP y dejar que descubra qué hay. En el ejemplo, el servidor MCP de Linear, con los datos de conexión y el token de auth en un fichero `.env`.

**Dos piezas trabajan juntas en la petición:**

- La clave **`mcp_servers`** declara la conexión: un **tipo**, una **URL**, un **nombre** para referirse a ella y, opcionalmente, un **token de autorización**.
- Una tool con tipo **`mcp_toolset`** configura **qué tools puede usar Claude** de ese servidor. Por defecto, todas; si quieres acotarlo, es aquí.

```
import os
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What tools do you have available?"}
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcp.linear.app/mcp",
            "name": "linear",
            "authorization_token": os.environ["LINEAR_MCP_TOKEN"],
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "linear",
        }
    ],
    betas=["mcp-client-2025-11-20"],
)

print(response)
```

Fíjate en que **no escribimos ni un solo schema de tool**. Claude **introspecciona el servidor**, recibe la lista de tools y sus schemas, y elige la adecuada para el prompt. A fecha de la lección, el **conector MCP está en beta** — de ahí el beta header.

Al ejecutarlo, si tu URL apunta al endpoint MCP de Linear, Claude lista las tools de Linear y llama a una. Lo mismo vale para prácticamente cualquier servidor que cumpla el protocolo. **No definimos ni una tool. No escribimos un cliente de Linear. Eso lo mantiene Linear.**

## Filtrar qué tools puede usar Claude

Los servidores MCP suelen exponer **muchísimas** tools — y no siempre quieres que Claude las use todas. Quizá no quieres darle permisos de escritura, o simplemente no quieres todas esas definiciones ocupando contexto.

El arreglo: **desactivar todo por defecto y activar solo lo que quieras**.

```
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "slack",
        "default_config": {
            "enabled": False,
        },
        "configs": {
            "search_messages": {"enabled": True},
            "list_channels": {"enabled": True},
        },
    }
]
```

Ahora Claude puede buscar en Slack y listar canales, **pero no puede publicar ni borrar**. Útil cuando confías en un servicio para lecturas pero no quieres que Claude escriba en tu nombre por accidente.

## Conclusiones

- **MCP existe para que no tengas que mantener integraciones** que otro ya ha construido. El proveedor publica su servidor MCP y lo mantiene al día; **tú no cambias nada cuando su API cambia**.
- Elige la funcionalidad correcta: **tools para tus datos, skills para tu proceso, MCP para servicios de terceros**.
- Declara la conexión en **`mcp_servers`** (tipo, URL, nombre, token opcional) y concede acceso con una entrada **`mcp_toolset`** en `tools`. Claude **introspecciona** el servidor y descubre las tools solo — **sin schemas que escribir**.
- Acota el acceso con **`default_config: {"enabled": False}`** y activando tools concretas en **`configs`** — cómodo para dejar un servidor **en solo lectura**.
- El conector MCP está **en beta**: incluye el beta header.
- Visita **modelcontextprotocol.io** para la lista de servidores disponibles y para aprender más del protocolo.

> **¿Quieres profundizar?** Los cursos dedicados: [Introduction to MCP](../introduction-to-model-context-protocol/README.md) y [MCP: Advanced Topics](../model-context-protocol-advanced-topics/README.md).
