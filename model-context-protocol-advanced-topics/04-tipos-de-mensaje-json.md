# 04 — Tipos de mensaje JSON

La comunicación en MCP son **mensajes JSON entre clientes y servidores**. Cada tipo de mensaje tiene un propósito distinto.

## Las dos categorías

| Categoría | Qué es | Ejemplos |
|---|---|---|
| **Pares Request / Result** | **Siempre van juntos**: a cada petición le corresponde un resultado | `call_tool_request` + `call_tool_result`<br>`initialize_request` + `initialize_result` |
| **Notifications** | Eventos que **no necesitan respuesta** | `progress_notification`<br>`logging_message_notification`<br>`tool_change_notification` |

## Clasificación por dirección

- **Client messages** — los envía el cliente MCP al servidor.
- **Server messages** — los envía el servidor MCP al cliente.

## La idea que hay que retener

> **Los servidores pueden enviar mensajes AL cliente**: hay *server requests* y *server notifications*.
>
> **Esa capacidad direccional se convierte en la limitación crítica del transporte StreamableHTTP.**

Es la frase bisagra del curso. Todo lo de los capítulos 01–03 son mensajes en esa dirección, y todo lo del 06 al 08 es lo que pasa cuando esa dirección deja de ser gratis.

## Detalles

**Definición del esquema** — un fichero TypeScript en el repositorio de la especificación de MCP: **`schema.ts`**. **No es código ejecutable**, solo descripciones de tipos por comodidad.

**Estructura del mensaje** — formato **JSON-RPC**, con campos `method`, `params` e `ID`.
