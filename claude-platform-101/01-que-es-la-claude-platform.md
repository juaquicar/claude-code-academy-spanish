# 01 — ¿Qué es la Claude Platform?

*15 minutos* · [Vídeo](https://www.youtube.com/embed/RfeC02NmLqs)

**Al terminar sabrás:** de qué piezas se compone la plataforma · las tres capas y su lema · cómo se ve una integración real con `messages.create` · qué hace cada parámetro.

---

La **Claude Platform** es la infraestructura de Anthropic para **construir con Claude programáticamente**. En vez de chatear con Claude en un navegador, **envías peticiones estructuradas desde tu código** y recibes respuestas estructuradas, con control sobre cada detalle: qué modelo usar, cuántos tokens gastar, qué tools puede usar Claude y qué instrucciones de sistema sigue.

En concreto, la plataforma la forman:

- Una **API REST** que puedes llamar desde cualquier lenguaje
- **SDKs** para distintos lenguajes de programación
- **Interfaces de línea de comandos**
- Una **consola** donde gestionas API keys, monitorizas el uso, despliegas agentes gestionados y pruebas prompts

## Las tres capas de la plataforma

Una forma útil de imaginarse la plataforma es como **tres capas apiladas**:

| Capa | Qué contiene | Para qué |
|---|---|---|
| **Primitives** | Messages API, tool use, files, web search, code execution, servidores MCP, skills | Los bloques de construcción que **llamas desde tu código** |
| **Infrastructure** | Managed agents, reintentos, colas, observabilidad | Lo que necesitas para **escalar** sistemas agénticos más allá del prototipo: la fontanería que aguanta cuando una llamada a Claude se convierte en mil |
| **Controls** | Dashboards, evals | Los diales que usa tu equipo **una vez está en producción** |

> **El lema, que es lo que se pregunta:** **build with primitives, scale on infrastructure, run with control.**

Esta estructura se refleja en la propia **Claude Console**: ahí viven las capas de infraestructura y control, con secciones para construir, gestionar agentes y ver analíticas.

## Un ejemplo real: redactar respuestas de un help desk

Supón que gestionas una aplicación básica de help desk y te piden una funcionalidad: **redactar una respuesta a partir del contenido de un ticket**, siguiendo el tono y las directrices de tu equipo, conectada a un botón de la interfaz.

Es un caso perfecto para la **Messages API**. El flujo es:

1. Definir un cliente
2. Recuperar el ticket al que se refiere
3. Llamar a `messages.create`
4. Devolver la respuesta al botón para que la renderice

```
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",   # Haiku: buen encaje para una redacción sencilla
    max_tokens=1024,
    system=TONE_AND_GUIDELINES,
    messages=[
        {"role": "user", "content": ticket_content}
    ],
)

draft = response.content
```

Cada parámetro tiene un trabajo concreto:

| Parámetro | Qué hace |
|---|---|
| **`model`** | Qué modelo atiende la petición. Aquí **Haiku**, porque redactar una respuesta es una tarea sencilla |
| **`max_tokens`** | **Limita la longitud** de la respuesta de Claude |
| **`system`** | El **system prompt**, donde defines el rol que juega Claude. Aquí van el tono y las directrices |
| **`messages`** | Un **array de objetos**. El rol `user` le dice a Claude que esto es entrada del usuario; ahí va el contenido del ticket |

## De «preguntarle a Claude» a «Claude es parte de mi producto»

Fíjate en lo que ha pasado en ese ejemplo: **no estás construyendo un chatbot desde cero**. Estás **metiendo a Claude dentro de un producto que ya existe**, y la API es cómo lo enchufas.

Esa es la idea central. Y cuando tu producto necesita agentes, la plataforma no se limita a darte el modelo: con los **managed agents**, **te los ejecuta**.

## Conclusiones

- La Claude Platform es la infraestructura de Anthropic para construir con Claude programáticamente: **API REST, SDKs, CLIs y una consola** para keys, uso, agentes gestionados y pruebas de prompts.
- Piénsala en tres capas: **primitives** (Messages API, tool use, files, web search, code execution, servidores MCP, skills), **infrastructure** (managed agents, reintentos, colas, observabilidad) y **controls** (dashboards, evals).
- El lema: **build with primitives, scale on infrastructure, run with control.**
- Una sola llamada a `messages.create` te da control total sobre modelo, longitud de respuesta, system prompt y entrada del usuario — suficiente para enchufar Claude a una funcionalidad existente.
- La plataforma te lleva de preguntarle cosas a Claude a **hacer de Claude parte de tu producto** — y con los agentes gestionados, puede además ejecutar tus agentes por ti.
