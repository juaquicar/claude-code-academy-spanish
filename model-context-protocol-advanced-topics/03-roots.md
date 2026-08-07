# 03 — Roots

**MCP Roots** = forma codificada de que un usuario **conceda a un servidor acceso a ficheros y carpetas concretos**.

## El problema sin roots

El usuario dice *"convierte bikin.mp4"*. Claude **no puede localizar el fichero** en un sistema de ficheros complejo sin la ruta completa. Y exigirle al usuario que escriba rutas completas es incómodo.

## La solución con roots

**Root** = fichero o carpeta al que el usuario concede permiso de acceso **por adelantado** — normalmente vía argumentos de línea de comandos al arrancar el servidor.

Se añaden **tres herramientas** al servidor MCP:

| Herramienta | Qué hace |
|---|---|
| **ConvertVideo** | la herramienta original |
| **ReadDirectory** | lista ficheros y carpetas de un directorio |
| **ListRoots** | devuelve los roots disponibles |

### Los dos beneficios

1. **Control de permisos** — limita el acceso del servidor solo a las zonas autorizadas.
2. **Descubrimiento autónomo** — Claude puede **buscar por los roots disponibles** para encontrar ficheros, sin que el usuario dé la ruta completa.

## ⚠ La limitación clave

> **El SDK de MCP no impone las restricciones de root automáticamente.** El desarrollador del servidor tiene que implementar las comprobaciones de acceso a mano.

Requisito de implementación: las herramientas **deben comprobar** que los ficheros y carpetas a los que acceden están contenidos dentro de los roots concedidos, con una función tipo `is_path_allowed()`.

> La herramienta **ListRoots es opcional**: como alternativa puedes meter la lista de roots directamente en el prompt. El patrón de herramienta permite a Claude **consultar dinámicamente** los roots disponibles cuando le hagan falta.

---

## Walkthrough de código

Proyecto de ejemplo: un conversor de vídeo con `ffmpeg` expuesto por MCP.

### Cliente — `mcp_client.py`

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import Root, ListRootsResult, ErrorData
from mcp.shared.context import RequestContext
from pathlib import Path
from pydantic import FileUrl


class MCPClient:
    def __init__(
        self,
        command: str,
        args: list[str],
        env: Optional[dict] = None,
        roots: Optional[list[str]] = None,
    ):
        self._command = command
        self._args = args
        self._env = env
        self._roots = self._create_roots(roots) if roots else []
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    def _create_roots(self, root_paths: list[str]) -> list[Root]:
        """Convert path strings to Root objects."""
        roots = []
        for path in root_paths:
            p = Path(path).resolve()
            file_url = FileUrl(f"file://{p}")
            roots.append(Root(uri=file_url, name=p.name or "Root"))
        return roots

    async def _handle_list_roots(
        self, context: RequestContext["ClientSession", None]
    ) -> ListRootsResult | ErrorData:
        """Callback for when server requests roots."""
        return ListRootsResult(roots=self._roots)

    async def connect(self):
        server_params = StdioServerParameters(
            command=self._command, args=self._args, env=self._env,
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(
                _stdio,
                _write,
                list_roots_callback=self._handle_list_roots
                if self._roots
                else None,
            )
        )
        await self._session.initialize()
```

**① Definir los roots** (`main.py`) — lo ideal es que sea **el usuario** quien dicte a qué ficheros y carpetas puede acceder el servidor MCP. El programa acepta una **lista de argumentos de línea de comandos** que se interpretan como las rutas a las que el usuario quiere dar acceso. Esa lista se pasa al `MCPClient`.

**② Crear los objetos Root** — según la especificación de MCP, **todos los roots deben tener una URI que empiece por `file://`**. `_create_roots()` convierte las rutas del usuario en objetos `Root`.

**③ El roots callback** — y aquí está el matiz:

> El cliente **no** entrega la lista de roots al servidor de entrada. El servidor puede **pedírsela en algún momento posterior**. Se registra un callback que se ejecutará cuando el servidor solicite los roots.

Se pasa como `list_roots_callback` a `ClientSession`.

### Servidor — `mcp_server.py`

```python
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context
from pydantic import Field
from core.video_converter import VideoConverter
from core.utils import file_url_to_path

mcp = FastMCP("VidsMCP", log_level="ERROR")


async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False


@mcp.tool()
async def convert_video(
    input_path: str = Field(description="Path to the input MP4 file"),
    format: str = Field(description="Output format (e.g. 'mov')"),
    *,
    ctx: Context,
):
    """Convert an MP4 video file to another format using ffmpeg"""
    input_file = VideoConverter.validate_input(input_path)

    # Ensure the input file is contained in a root
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)


@mcp.tool()
async def list_roots(ctx: Context):
    """
    List all directories that are accessible to this server.
    These are the root directories where files can be read from or written to.
    """
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    return [file_url_to_path(root.uri) for root in client_roots]


@mcp.tool()
async def read_dir(
    path: str = Field(description="Path to a directory to read"),
    *,
    ctx: Context,
):
    """Read directory contents. Path must be within one of the client's roots."""
    requested_path = Path(path).resolve()

    if not await is_path_allowed(requested_path, ctx):
        raise ValueError("Error: can only read directories within a root")

    return [entry.name for entry in requested_path.iterdir()]
```

**④ Usar los roots** — el servidor los usa en **dos escenarios**:

1. Cuando una herramienta **intenta acceder** a un fichero o carpeta.
2. Cuando un LLM como Claude **necesita resolver** un fichero o carpeta a su ruta completa — piensa en cuando el usuario dice *"lee el fichero todos.txt"*.

**⑤ Acceder a los roots** — se accede llamando a **`ctx.session.list_roots()`**. Eso **manda un mensaje de vuelta al cliente**, que ejecuta su callback de listado de roots.

**⑥ Autorizar el acceso** — recuerda: **el SDK de MCP no intenta limitar a qué ficheros o carpetas accedan tus herramientas.** Esa comprobación la implementas tú. `is_path_allowed()` decide comparando la ruta pedida con los roots.

**⑦ Usarla en todas partes** — una vez montada la función de autorización, **úsala en todas tus herramientas** para asegurar que la ruta pedida es accesible. Fíjate en que tanto `convert_video` como `read_dir` la llaman antes de tocar nada.

---

> **Ojo para el capítulo 6:** `ctx.session.list_roots()` es, otra vez, **el servidor pidiéndole algo al cliente**. Tercera capacidad que depende de esa dirección.
