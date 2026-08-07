# 01 — Sampling

**Sampling** = técnica que permite a un servidor MCP **pedirle al cliente que genere texto con un modelo de lenguaje**, en vez de acceder el servidor directamente a un LLM.

## El problema que resuelve

Un servidor MCP que quiera usar un LLM tendría que:

- gestionar **claves de API**,
- gestionar **autenticación**,
- pagar los **costes de tokens**.

Sampling **traslada la responsabilidad del acceso al LLM del servidor al cliente**. El servidor no necesita ninguna de esas tres cosas.

## Arquitectura

```
Servidor                Cliente                    LLM
   │                       │                        │
   │ crea petición ──────► │                        │
   │                       │ ── callback ─────────► │
   │                       │ ◄──── texto generado ──│
   │ ◄──── texto ───────── │                        │
```

1. El **servidor** crea una petición de mensaje.
2. El **cliente** la recibe a través de su **sampling callback**.
3. El **cliente** llama al LLM.
4. El **cliente** devuelve el texto generado al servidor.

## Beneficios

- Elimina la complejidad de integrar un LLM en el servidor.
- **Quita el requisito de claves de API** del servidor.
- **Evita el uso no autorizado de tokens** en servidores públicos.

> **Caso de uso principal:** servidores MCP **accesibles públicamente** que necesitan capacidades de LLM sin acceso directo a uno, ni los costes ni los problemas de seguridad asociados.

## Implementación

- **Servidor** — usa la función `create_message()` con una lista de mensajes.
- **Cliente** — implementa un **sampling callback** que atiende las peticiones del LLM y devuelve un `create_message_result`.

---

## Walkthrough de código

### Servidor — `server.py`

```python
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user", content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**① Iniciar el sampling** — en el servidor, durante una llamada a herramienta, ejecuta `create_message()` pasándole los mensajes que quieres enviar a un modelo de lenguaje.

**⑥ Recoger el resultado** — cuando el cliente ha generado y devuelto el texto, llega al servidor. Puedes hacer con él lo que quieras:

- usarlo como parte de un flujo dentro de tu herramienta,
- decidir hacer **otra** llamada de sampling,
- devolver el texto generado.

### Cliente — `client.py`

```python
import asyncio
from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)

anthropic_client = AsyncAnthropic()
model = "claude-sonnet-4-0"

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text


async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=sampling_callback
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                name="summarize",
                arguments={"text_to_summarize": "lots of text"},
            )
            print(result.content)
```

**② El sampling callback** — en el cliente **debes** implementarlo. Recibe la lista de mensajes que le pasa el servidor.

**③ Formatos de mensaje** — los mensajes que envía el servidor están formateados **para comunicación en MCP**. No hay garantía de que sean compatibles con el SDK de LLM que estés usando.

> Si usas el SDK de Anthropic, tendrás que escribir **algo de lógica de conversión** para pasar de mensajes MCP al formato del SDK. Eso es la función `chat()`.

**④ Devolver el texto generado** — tras generar con el LLM, devuelves un `CreateMessageResult` con el texto dentro.

**⑤ Conectar el callback** — no lo olvides: el callback hay que **pasárselo a `ClientSession`**. Si no, el servidor pedirá sampling y no habrá nadie escuchando.

---

> **Ojo para el capítulo 6:** el sampling exige que el **servidor le pida algo al cliente**. Esa dirección de comunicación es exactamente la que HTTP no da gratis.
