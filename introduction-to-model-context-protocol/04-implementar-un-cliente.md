# 04 — Implementar un cliente

## Las dos piezas

| Pieza | Qué es |
|---|---|
| **Client Session** | **La conexión real** al servidor MCP, del SDK de Python. **Requiere limpieza de recursos al cerrar** |
| **MCP Client** | **Clase envoltorio** alrededor de la sesión, que gestiona la conexión y la limpieza |

> **Práctica habitual:** envolver la client session en una clase mayor en vez de usarla directamente, **para gestionar mejor los recursos**.

La limpieza se maneja con las funciones **`connect`**, **`cleanup`**, **`async enter`** y **`async exit`**.

**Para qué sirve el cliente:** **exponer la funcionalidad del servidor MCP al resto de tu código**, sirviendo de interfaz entre tu aplicación y el servidor.

## Las dos funciones clave

```python
async def list_tools(self):
    result = await self.session.list_tools()
    return result.tools

async def call_tool(self, tool_name, tool_input):
    return await self.session.call_tool(tool_name, tool_input)
```

## El flujo de implementación

1. La aplicación pide la lista de herramientas para Claude.
2. El cliente llama a **`list_tools()`** para obtener las disponibles en el servidor.
3. **Claude selecciona una herramienta** y aporta los parámetros.
4. El cliente llama a **`call_tool()`** para ejecutarla en el servidor.
5. Los resultados vuelven a Claude.

## Probarlo

Ejecuta **`mcp client.py` directamente con un arnés de pruebas** para verificar la conexión y el listado de herramientas.

Una vez implementado, puedes lanzar la CLI y hacer que Claude use las herramientas — por ejemplo: *"what is contents of report.pdf document"*.
