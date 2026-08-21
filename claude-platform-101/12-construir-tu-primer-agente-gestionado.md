# 12 — Construir tu primer agente gestionado

*20 minutos* · [Vídeo](https://www.youtube.com/embed/1Rl3gZrlQJo)

**Al terminar sabrás:** los cuatro primitivos y su orden · los cinco pasos del código · **por qué el stream se abre antes del mensaje inicial** · los tres eventos que importan · cuándo delegar el bucle y cuándo no.

---

Si has construido un bucle de agente a mano, ya sabes la rutina: bucles while, switches de stop reason, ejecución de tools. Eso funciona, y **para muchas funcionalidades es la forma correcta**. Pero a veces ese bucle va a correr **mucho tiempo** — minutos, quizá horas — **a través de muchas tools, con estado que guardar, ficheros que escribir y trabajo que reanudar tras un corte de red**. Llegado ese punto, **no quieres ejecutar el bucle en tu servidor. Quieres delegarlo.** Eso son los **managed agents**.

## Qué es un agente gestionado

Un agente gestionado es **un bucle de agente que corre en la infraestructura de Anthropic en vez de en la tuya**. Describes el agente una vez, le das un entorno donde trabajar y arrancas una sesión. **Anthropic ejecuta el bucle y tú solo consumes los eventos** según trabaja.

> **Los managed agents están activados por defecto para toda cuenta de API** — no hace falta acceso especial.

## Los cuatro primitivos

Son cuatro, **y vienen en orden**:

| # | Primitivo | Qué es |
|---|---|---|
| 1 | **Agent** | La **persona**: modelo, system prompt y toolset. **Reutilizable** entre muchas ejecuciones |
| 2 | **Environment** | **Dónde** corre el agente: cloud o local, configuración de red, etc. |
| 3 | **Session** | **Una única ejecución** de un agente dentro de un entorno. **La sesión es la unidad de trabajo** |
| 4 | **Events** | Los mensajes que entran y salen: acciones del agente, llamadas a tools, resultados, respuestas |

Cómo encajan: **tu app habla con una sesión, la sesión mueve el trabajo dentro del entorno, y todo lo que pasa sale por el event stream.**

> **El cambio de mentalidad: no estás ejecutando un bucle while. Estás enviando eventos y leyendo eventos.**

## El agente gestionado más pequeño posible

Construimos el más pequeño que hace algo útil: **crear un fichero en el directorio temporal, contar sus líneas e informar**.

Para las tools usamos el **agent toolset** — el paquete de tools de fichero, bash y web de Anthropic. Nos sirven, así que **no definimos ninguna tool**.

### Paso 1 · Crear el agente

Fíjate en el agent toolset definido directamente en el array `tools`:

```
import anthropic

client = anthropic.Anthropic()

agent = client.beta.agents.create(
    name="Line Counter",
    model="claude-opus-4-8",
    system="You are a helpful agent that completes small file tasks.",
    tools=[
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}}
    ],
)
```

> Recuerda: **el agente es reutilizable.** Créalo una vez y ejecútalo en muchas sesiones.

### Paso 2 · Crear el entorno

Esto levanta la plantilla de contenedor — **cloud, con red sin restricciones**. Es el sandbox donde el fichero se escribe de verdad:

```
environment = client.beta.environments.create(
    name="line-counter-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
    },
)
```

### Paso 3 · Crear la sesión

Con nuestro agente y nuestro entorno, más un título opcional. **La sesión es la unidad de trabajo:**

```
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Count lines demo",
)
```

### Paso 4 · Abrir el stream y *luego* enviar el mensaje inicial

> **Aquí está la trampa del capítulo.** Abrimos el event stream **primero**. El stream **solo entrega eventos que ocurren después de abrirse**, así que **ábrelo siempre antes de enviar el mensaje inicial**.

```
with client.beta.sessions.events.stream(session_id=session.id) as stream:
    # Stream is open — now send the kickoff
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a file in the temp directory, "
                                "count its lines, and report back.",
                    }
                ],
            }
        ],
    )
```

Fíjate en que es **`events`** — en plural. **Los eventos son cómo fluye todo en esta API.**

### Paso 5 · Consumir el stream

Tres tipos de evento importan en esta demo:

| Evento | Qué es |
|---|---|
| **`agent.message`** | El texto de Claude |
| **`agent.tool_use`** | Qué tool eligió Claude |
| **`session.status_idle`** | El agente ha terminado |

```
    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "agent.tool_use":
            print(f"\n[tool] {event.name}")
        elif event.type == "session.status_idle":
            print("\n--- Agent done ---")
            break
```

Al ejecutarlo, la salida es el agente **razonando en voz alta** — texto real, las tools que elige y una respuesta final. Todo corriendo **dentro del contenedor de Anthropic, no del tuyo**.

## El trato

Normalmente con los agentes tenemos nuestro propio bucle y controlamos todo. Con los managed agents **delegas el bucle, el sandbox y la reanudabilidad** — y solo consumes el event stream según llega.

En producción, esta es la forma para tareas **de larga duración, que tocan ficheros, del tipo "ve y organízame esto"**. Piensa en una limpieza de un recurso compartido: un agente gestionado lee una especificación de estructura de directorios, recorre la carpeta de entrada hecha un desastre, mueve ficheros a las carpetas de proyecto correctas, archiva duplicados y basura de cero bytes, y **señala lo que no puede colocar con confianza** — todo en una sesión que puede correr minutos contra miles de ficheros.

## Conclusiones

- **Los managed agents son el bucle de agente, ejecutado por ellos** — en la infraestructura de Anthropic en vez de en tu servidor.
- El flujo es: **crear un agente, crear un entorno, crear una sesión, enviar eventos y consumir el stream de eventos**.
- El **agent** (modelo, system prompt, toolset) es **reutilizable**; la **session** es una única ejecución; los **events** son cómo fluye todo.
- **Abre el event stream antes de enviar tu mensaje inicial** — solo entrega eventos posteriores a su apertura.
- Vigila tres eventos: **`agent.message`** (texto), **`agent.tool_use`** (elección de tool) y **`session.status_idle`** (terminado).
- Recurre a los managed agents cuando el bucle **correría demasiado tiempo, haría demasiadas cosas o necesitaría sobrevivir a un percance**. Recurre a un bucle manual cuando quieras **control total**.
