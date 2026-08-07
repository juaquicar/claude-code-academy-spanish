# 06 — El transporte StreamableHTTP

**StreamableHTTP** = transporte MCP que permite la comunicación cliente-servidor **sobre conexiones HTTP**, habilitando **alojar el servidor remotamente** — al contrario que STDIO, que exige que ambos estén en la misma máquina.

## La ventaja

**Alojamiento remoto.** Los servidores pueden ser **accesibles públicamente** en una URL como `mcpserver.com`, lo que amplía enormemente lo que se puede hacer con un servidor MCP.

## La limitación crítica

> **Funcionalidad restringida de mensajería servidor → cliente**, por la naturaleza unidireccional de HTTP.

Los clientes piden cosas al servidor sin problema. **Los servidores no pueden iniciar peticiones al cliente con facilidad.**

### Por qué exactamente

- El servidor **no conoce la dirección del cliente**.
- El cliente **puede no ser accesible públicamente**.

Con eso, una petición del servidor hacia el cliente no tiene a dónde ir.

## Qué se ve afectado

Todos los tipos de mensaje que necesitan comunicación **servidor → cliente**:

- **Peticiones de sampling** → capítulo 01
- **Listado de roots** → capítulo 03
- **Notificaciones de progreso** → capítulo 02
- **Notificaciones de logging** → capítulo 02

**Es exactamente todo el primer bloque del curso.**

## Los dos flags que lo cambian todo

| Flag | Valor por defecto |
|---|---|
| **stateless HTTP** | `false` |
| **JSON response** | `false` |

> **Ponerlos a `true` reduce la funcionalidad**: rompe las barras de progreso, las notificaciones de logging, las notificaciones de progreso y las peticiones de sampling.

Los detalles de cada uno, en el [capítulo 08](08-estado-y-flags.md).

## El fallo de despliegue clásico

> La aplicación funciona **perfectamente en local con STDIO** y **falla al desplegarla con HTTP**, por estas restricciones de mensajería.

Es el error que este capítulo existe para prevenir.

## Hay solución

StreamableHTTP **tiene apaños** para el problema de la comunicación servidor → cliente — **pero con condiciones**. Cómo funcionan, en el [capítulo 07](07-streamablehttp-en-profundidad.md).
