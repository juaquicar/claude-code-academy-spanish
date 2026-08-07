# MCP: Advanced Topics — Anthropic Academy

Curso: https://anthropic.skilljar.com/model-context-protocol-advanced-topics

**Idea central:** lo que MCP puede hacer más allá de exponer herramientas — que el **servidor** pida cosas al **cliente** — y por qué esa dirección de comunicación es la que se rompe al desplegar.

> **[▶ curso-interactivo.html](curso-interactivo.html)** — todo el curso en una sola página: diagramas de flujo de mensajes, walkthroughs de código navegables paso a paso, comparador de transportes, simulador de flags, flashcards y quiz. Doble clic, sin dependencias ni conexión.

## Índice

| # | Capítulo | Bloque |
|---|----------|--------|
| 01 | [Sampling](01-sampling.md) | Capacidades servidor → cliente |
| 02 | [Notificaciones de log y progreso](02-notificaciones-log-y-progreso.md) | Capacidades servidor → cliente |
| 03 | [Roots](03-roots.md) | Capacidades servidor → cliente |
| 04 | [Tipos de mensaje JSON](04-tipos-de-mensaje-json.md) | Protocolo y transportes |
| 05 | [El transporte STDIO](05-transporte-stdio.md) | Protocolo y transportes |
| 06 | [El transporte StreamableHTTP](06-transporte-streamablehttp.md) | Protocolo y transportes |
| 07 | [StreamableHTTP en profundidad](07-streamablehttp-en-profundidad.md) | Protocolo y transportes |
| 08 | [Estado: stateless y JSON response](08-estado-y-flags.md) | Protocolo y transportes |
| 09 | [Repaso y autoevaluación](09-repaso-y-quiz.md) | Cierre |

Las lecciones 01, 02 y 03 traen además un **walkthrough de código** en la plataforma: un editor con los ficheros del proyecto y pasos que van saltando de línea en línea. El código y los pasos están integrados en cada capítulo.

## El hilo conductor

Las tres primeras capacidades —**sampling**, **notificaciones** y **roots**— tienen algo en común que solo se ve al llegar al bloque de transportes:

> **Las tres necesitan que el servidor le pida algo al cliente.**

| Capacidad | El servidor pide al cliente… |
|---|---|
| **Sampling** | que genere texto con su LLM |
| **Log / progreso** | que muestre un mensaje o una barra de avance |
| **Roots** | que le diga a qué ficheros y carpetas tiene permiso de acceder |

Y ahí está el nudo del curso:

- **STDIO** es **bidireccional** por naturaleza — cliente y servidor escriben en los streams del otro, cualquiera de los dos puede iniciar una petición en cualquier momento. Las tres capacidades funcionan sin más.
- **HTTP es unidireccional**: el cliente pide, el servidor responde. El servidor **no sabe la dirección del cliente**, y el cliente puede ni siquiera ser accesible desde fuera. **StreamableHTTP** lo esquiva con **conexiones SSE**, pero es un apaño con condiciones.
- Dos flags —**`stateless_http`** y **`json_response`**— rompen ese apaño y **desactivan las tres capacidades**.

> **El fallo de despliegue clásico:** todo funciona en local con STDIO y se cae al desplegar con HTTP. Desarrolla con el mismo transporte con el que vas a producir.

## Sobre el material

El curso es **de vídeo**, no de texto: las páginas de lección solo llevan el reproductor. Estos resúmenes se han elaborado a partir de las **notas oficiales del curso** que Anthropic embebe en la propia plataforma (las que alimentan el botón *"Open in Claude"*), más el **código y los pasos de los tres walkthroughs**, extraídos de las lecciones interactivas.

El curso tiene una **evaluación oficial de 10 preguntas** (*Assessment on MCP Concepts*) que se hace en la plataforma. El capítulo 09 es preparación para ella.
