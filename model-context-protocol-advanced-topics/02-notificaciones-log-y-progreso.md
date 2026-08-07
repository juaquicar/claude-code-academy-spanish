# 02 — Notificaciones de log y progreso

**Log and Progress Notifications** = capacidad del servidor MCP que da **feedback en tiempo real durante la ejecución de una herramienta**, para mejorar la experiencia de usuario.

## Para qué

Sin esto, una llamada a herramienta que tarda es una caja negra: el usuario no sabe si está trabajando, si se ha colgado o si ha fallado.

**Beneficios:**

- **Evita que el usuario crea que la llamada se ha atascado o ha fallado.**
- Da **visibilidad** sobre operaciones largas.
- Feedback **en tiempo real** durante la ejecución.

> Es una capacidad **opcional**: puedes prescindir de ella. Es puramente mejora de UX.

## Implementación

### En el servidor

- Las funciones de herramienta **reciben automáticamente un argumento `Context` como último parámetro**.
- El objeto `Context` ofrece métodos: **`info()`** para logs y **`report_progress()`** para avance.
- Llamar a esos métodos **envía mensajes al cliente automáticamente**.

### En el cliente

- Crea una **función callback para los logs**.
- Crea **otro callback aparte para el progreso**.
- Pasa el **callback de logging a `ClientSession`**.
- Pasa el **callback de progreso a `call_tool()`**.
- Los callbacks deciden **cómo mostrar** la información: salida por terminal, interfaz web, lo que sea.

> Dos callbacks, **dos sitios distintos** donde se registran. Es el detalle que más se confunde.

---

## Walkthrough de código

### Servidor — `server.py`

```python
from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**① La función recibe `Context`** — las funciones de herramienta reciben `Context` como **último argumento, automáticamente**. Ese objeto tiene los métodos de logging y de reporte de progreso hacia el cliente.

**② Generar logs y progreso** — a lo largo de tu función llama a **`info()`, `warning()`, `debug()` o `error()`** para registrar distintos tipos de mensaje para el cliente. Y llama a **`report_progress()`** para estimar cuánto queda.

### Cliente — `client.py`

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import LoggingMessageNotificationParams

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)


async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, logging_callback=logging_callback
        ) as session:
            await session.initialize()

            await session.call_tool(
                name="add",
                arguments={"a": 1, "b": 3},
                progress_callback=print_progress_callback,
            )
```

**③ Definir los callbacks en el cliente** — el cliente necesita definir el callback de logging y el de progreso. **Se llaman automáticamente** cada vez que el servidor emite un mensaje de log o de progreso. Estos callbacks deben encargarse de **mostrar** la información al usuario.

**④ Pasarlos a la función correcta** — y aquí está el detalle que importa:

| Callback | Dónde se pasa |
|---|---|
| **logging** | a `ClientSession(...)` |
| **progreso** | a `call_tool(...)` |

Tiene sentido: el logging es **de la sesión entera**; el progreso es **de una llamada concreta**.

---

> **Ojo para el capítulo 6:** igual que el sampling, esto exige que el **servidor mande mensajes al cliente**. Es lo segundo que se rompe al pasar a HTTP.
