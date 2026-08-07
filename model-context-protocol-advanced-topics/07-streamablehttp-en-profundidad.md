# 07 — StreamableHTTP en profundidad

**StreamableHTTP** = transporte MCP sobre HTTP que usa **server-sent events (SSE)** para habilitar la comunicación servidor → cliente.

## El problema central

> MCP **necesita** peticiones del servidor al cliente —sampling, notificaciones, logging— pero **HTTP soporta de forma natural solo peticiones del cliente al servidor**.

## El apaño

Usar **conexiones SSE** para que el servidor pueda **hacer streaming de mensajes hacia el cliente**.

> Las respuestas SSE habilitan comunicación bidireccional sobre HTTP **manteniendo las conexiones abiertas** y enviando mensajes individuales del servidor al cliente.

## El Session ID

**Session ID** = identificador aleatorio asignado durante la inicialización, incluido en todas las peticiones posteriores **como cabecera HTTP**.

## Flujo de inicialización

1. El **cliente** envía la petición `initialize`.
2. El **servidor** responde con el resultado **+ la cabecera con el MCP session ID**.
3. El **cliente** envía la notificación `initialized` con el session ID.
4. El **cliente**, opcionalmente, hace una petición **GET** con el session ID para **establecer la conexión SSE**.

## Las dos conexiones SSE

Este es el punto que hay que retener del capítulo.

| Conexión | Vida | Para qué |
|---|---|---|
| **SSE de larga duración** | persistente | **Peticiones iniciadas por el servidor** — sampling, notificaciones |
| **SSE de corta duración** | se cierra sola | Respuestas a **una llamada a herramienta concreta**; se cierra automáticamente tras el resultado |

### Enrutado de mensajes

| Mensaje | Va por |
|---|---|
| Notificaciones de **progreso** | conexión **larga** |
| Mensajes de **logging** + **resultados de herramienta** | conexión **corta**, atada a esa petición concreta |

> Detalle contraintuitivo: **progreso y logging no viajan por la misma conexión**, aunque los emitas desde la misma función de herramienta con el mismo `ctx`.

## La limitación clave

> **Poner ciertos flags a `true` rompe el apaño**, lo que hace que StreamableHTTP sea complejo de entender y de usar correctamente.

Esos flags son el capítulo siguiente.
