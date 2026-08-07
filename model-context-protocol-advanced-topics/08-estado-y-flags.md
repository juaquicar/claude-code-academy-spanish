# 08 — Estado: los flags `stateless_http` y `json_response`

Los dos flags que rompen el apaño SSE del capítulo anterior. Entender qué apagan es lo que evita el fallo de despliegue.

---

## Flag 1 · Stateless HTTP

**Stateless HTTP** = flag que se pone a `true` cuando el servidor MCP necesita **escalado horizontal** entre varias instancias con un balanceador de carga.

### Por qué haría falta

Una sola instancia de servidor no puede con mucho tráfico. El escalado horizontal usa **varias copias del servidor + un balanceador** que reparte las peticiones **aleatoriamente**.

### El problema sin stateless

El cliente necesita **dos conexiones**:

- un **GET SSE** para las peticiones servidor → cliente,
- un **POST** para las peticiones cliente → servidor.

> El balanceador puede mandar cada una **a una instancia distinta**. Si una herramienta en el **Servidor A** necesita hacer una petición de sampling, tiene que salir por la conexión GET SSE que está abierta contra el **Servidor B** — y eso exige una coordinación compleja.

### Qué pasa con `stateless_http = true`

- **No se asignan session IDs** a los clientes.
- El servidor **no puede rastrear clientes individuales**.
- **Se desactiva la vía de respuesta GET SSE** → el servidor **no puede enviar peticiones al cliente**.
- **Elimina** sampling, logging de progreso y suscripciones a recursos.
- **No hace falta inicialización** del cliente: se salta la petición `initialize` y su notificación.
- **Reduce el tráfico** del servidor.

Es un intercambio directo: **escalabilidad a cambio de las capacidades servidor → cliente**.

---

## Flag 2 · JSON response

**JSON response** = flag que **desactiva las respuestas por streaming en las peticiones POST**.

### Qué pasa con `json_response = true`

- Las respuestas POST devuelven **solo el resultado final, en JSON plano**.
- **Sin mensajes intermedios por streaming.**
- **Sin sentencias de progreso ni de log** durante la ejecución.
- El cliente **espera a que la herramienta termine por completo** antes de recibir nada.

---

## Tabla comparativa

| | Por defecto | `stateless_http=true` | `json_response=true` |
|---|---|---|---|
| Session ID | sí | **no** | sí |
| Inicialización | obligatoria | **se salta** | obligatoria |
| GET SSE (servidor → cliente) | sí | **desactivada** | sí |
| Sampling | ✓ | **✗** | ✓ |
| Roots | ✓ | **✗** | ✓ |
| Progreso y logging | ✓ | **✗** | **✗** |
| Streaming en el POST | sí | sí | **no** |
| Escalado horizontal | difícil | **fácil** | igual |

---

## La conclusión del capítulo

> **Ambos flags cambian significativamente el comportamiento del servidor. Usa en desarrollo el mismo transporte que vas a usar en producción, para evitar problemas al desplegar.**

Es la misma advertencia del capítulo 06, y cierra el curso: lo que se rompe al desplegar no es tu código, es la **dirección de comunicación** que tu código daba por hecha.
