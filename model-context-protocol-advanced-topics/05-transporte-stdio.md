# 05 — El transporte STDIO

**Transporte MCP** = el mecanismo para **mover los mensajes JSON** entre cliente y servidor.

**Transporte STDIO** = el cliente **lanza el servidor como un proceso aparte** y se comunican por los **flujos de entrada y salida estándar**.

## Cómo se comunican

```
Cliente ──escribe──► stdin  del servidor
Cliente ◄───lee───── stdout del servidor
```

El cliente escribe en el `stdin` del servidor y lee de su `stdout`. El servidor escribe en su `stdout` y lee de su `stdin`.

## La ventaja

> **Comunicación bidireccional: cualquiera de los dos —cliente o servidor— puede iniciar una petición en cualquier momento.**

Por eso sampling, notificaciones y roots funcionan con STDIO sin ningún apaño.

## La limitación

**Solo funciona cuando cliente y servidor corren en la misma máquina física.**

## Patrones de intercambio

| Dirección | Cómo |
|---|---|
| **Cliente → servidor** | escribe en `stdin`, lee la respuesta de `stdout` |
| **Servidor → cliente** | el servidor escribe en `stdout`, el cliente responde por `stdin` |

## Secuencia de inicialización obligatoria

1. **Initialize request** — cliente → servidor
2. **Initialize result** — servidor → cliente
3. **Initialize notification** — cliente → servidor, **no requiere respuesta**

## Los tres tipos de mensaje

| Tipo | Espera respuesta |
|---|---|
| **Requests** | Sí |
| **Notifications** | No |
| **Results** | Son la respuesta a un request |

## En una frase

> **Soporte completo de comunicación bidireccional: ambas partes pueden iniciar peticiones.**

Y el contraste que abre el capítulo siguiente: **el transporte HTTP tiene limitaciones sobre las peticiones iniciadas por el servidor que STDIO no tiene.**
