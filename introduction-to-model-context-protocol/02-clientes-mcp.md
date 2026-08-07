# 02 — Clientes MCP y el proyecto

## Qué es un cliente MCP

**Interfaz de comunicación entre tu servidor y el servidor MCP**, que te da acceso a sus herramientas.

- **Agnóstico del transporte** — pueden comunicarse por varios protocolos: **stdin/stdout, HTTP, WebSockets**…
- **Montaje habitual:** ambos en la **misma máquina**, usando stdin/stdout.

La comunicación es un **intercambio de mensajes definido por la especificación de MCP**.

## Los mensajes clave

| Mensaje | Qué hace |
|---|---|
| **`list tools request`** | El cliente pide al servidor las herramientas disponibles |
| **`list tools result`** | El servidor responde con la lista |
| **`call tool request`** | El cliente pide ejecutar una herramienta con argumentos |
| **`call tool result`** | El servidor devuelve el resultado de la ejecución |

## El flujo completo

1. **El usuario** consulta a tu servidor.
2. **Tu servidor** pide las herramientas al cliente MCP.
3. **El cliente MCP** manda `list tools request` al servidor MCP.
4. **El servidor MCP** responde; tu servidor obtiene la lista.
5. **Tu servidor** envía la consulta + las herramientas a **Claude**.
6. **Claude** pide ejecutar una herramienta.
7. **Tu servidor** pide al cliente MCP que la ejecute.
8. **El cliente MCP** manda `call tool request`.
9. **El servidor MCP** la ejecuta — p. ej. una llamada al API de GitHub.
10. **Los resultados vuelven por toda la cadena**, Claude formula la respuesta final y el usuario la recibe.

> **El cliente MCP actúa de intermediario:** **no ejecuta las herramientas él mismo**, solo facilita la comunicación entre tu servidor y el servidor MCP que sí las ejecuta.

---

## El proyecto del curso

**Chatbot de línea de comandos** que implementa **cliente y servidor** con fines didácticos.

| Componente | Detalle |
|---|---|
| **Estructura** | Un cliente MCP propio conecta con un servidor MCP propio, **ambos en el mismo proyecto** |
| **Documentos** | Documentos falsos guardados **solo en memoria**, sin persistencia |
| **Herramientas del servidor** | **Dos**: leer el contenido de un documento y actualizarlo |

> ⚠ **Aviso de contexto real:** normalmente un proyecto implementa **el cliente O el servidor, no ambos**. Aquí se hacen los dos para aprender.

**Montaje:** descarga `CLI_project.zip`, extráelo, configura el `.env` con tu clave de API e instala dependencias.

**Ejecución:** `uv run main.py` (con UV) o `python main.py` (sin UV).

**Verificación:** aparece el prompt de chat y responde a consultas básicas como *"what's one plus one"*.
