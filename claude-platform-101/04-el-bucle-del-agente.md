# 04 — El bucle del agente

*20 minutos* · [Vídeo](https://www.youtube.com/embed/tBIdyIoCQVU)

**Al terminar sabrás:** qué es un agente en una frase · los cinco pasos del bucle · cómo se implementa entero en un script · qué cambia al llevarlo a producción.

---

Ya has hecho llamadas a la API, pero **una sola llamada devuelve una sola respuesta**. Si quieres automatizar un flujo de trabajo, Claude necesita **actuar, mirar el resultado, decidir qué sigue y continuar**. Ese patrón es lo que la gente quiere decir cuando habla de **flujos agénticos**.

## Qué es un agente

> **Un agente es una versión autónoma de Claude que ejecuta los dos lados del bucle de mensajes sin un humano en medio.** Recibe una tarea, elige una tool y ejecuta código **en bucle hasta que Claude decide que la tarea está hecha**.

La forma más fácil de implementarlo:

1. Enviar un mensaje a Claude **con tools disponibles**.
2. Claude responde con **una respuesta final** o con **una petición de usar una tool** que tú definiste.
3. **Tu código ejecuta esa tool.**
4. Le **devuelves el resultado** a Claude.
5. Repetir **hasta que el stop reason sea `end_turn`**.

Piénsalo como una conversación por turnos: el usuario arranca, el agente llama a una tool, la tool devuelve un resultado, y el agente sigue hasta tener respuesta.

## Un ejemplo mínimo que funciona

Para ver el bucle de punta a punta sin arrastrar una base de datos ni una interfaz, montamos una tool falsa `get_weather` y preguntamos qué ponerse hoy en Austin. Claude no tiene forma de saber el tiempo por sí mismo, así que **tiene que llamar a la tool, leer el resultado y luego responderte**.

```
import anthropic

client = anthropic.Anthropic()

# The tools array tells Claude what's available:
# a name, a description, and a JSON schema for the inputs.
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for",
                }
            },
            "required": ["city"],
        },
    }
]

# run_tool is just a hardcoded lookup.
# In a real app, this would hit your database, an API, whatever.
def run_tool(name, tool_input):
    if name == "get_weather":
        return f"Weather in {tool_input['city']}: 95F, sunny"
    raise ValueError(f"Unknown tool: {name}")

messages = [
    {"role": "user", "content": "What should I wear in Austin today?"}
]

# The agent loop. Each iteration sends messages to Claude
# and switches on the response's stop reason.
while True:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        # Claude is done. Print the final text and break.
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    if response.stop_reason == "tool_use":
        # Find the tool use blocks in the response and run each one.
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = run_tool(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        # Push the assistant's response and our tool results
        # back into messages, then loop again so Claude can answer.
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

Tres piezas que mirar:

- **El array `tools`** le dice a Claude qué hay disponible: un **nombre**, una **descripción** y un **JSON schema** para las entradas.
- **`run_tool`** es solo una búsqueda hardcodeada. En una app real esto iría a tu base de datos, a una API, a lo que sea.
- **El bucle.** Cada iteración envía los mensajes a Claude y **conmuta según el stop reason**. Con `end_turn`, Claude ha terminado: imprime el texto final y sal. Con `tool_use`, busca los bloques de tool use, ejecuta cada uno, mete la respuesta del assistant y tus resultados de tool en `messages`, y vuelve al bucle para que Claude responda.

## Ejecutándolo

Al ejecutar el script verás **dos turnos**:

1. **Turno uno:** el stop reason es **`tool_use`**. Claude pide `get_weather` para Austin, y tu código devuelve temperatura y condiciones.
2. **Turno dos:** el stop reason es **`end_turn`**, y Claude te dice que te pongas algo ligero y transpirable.

**Dos llamadas a la API, una ejecución de tool, una respuesta final.** Ese es el bucle entero. Todo lo que construyas con la Claude API va a parecerse a esto.

## El mismo bucle en producción

En un entorno real, este mismo bucle mueve algo como un endpoint de auto-revisión: un agente de cumplimiento que lee un informe estructural, consulta los códigos de edificación relevantes vía una tool y escribe hallazgos de riesgo en la base de datos uno a uno según trabaja.

**La forma del bucle es idéntica** a la que acabas de ejecutar. Lo que cambia:

- Tools reales en vez de una consulta de tiempo simulada.
- Los resultados **llegan a la interfaz por server-sent events**.
- Los hallazgos **se persisten** en una tabla.

## Conclusiones

- Un agente es **Claude en bucle**: observar, decidir, actuar, repetir.
- El bucle es simple: envía mensajes con tools, ejecuta la tool que Claude pida, devuelve el resultado y **para cuando el stop reason sea `end_turn`**.
- **Tú eres dueño del bucle y de las tools. Claude es dueño del razonamiento.**
- La misma forma escala del demo simulado a un agente de cumplimiento en producción: **solo cambian las tools y la fontanería**.
- Cuando **no** quieras ser dueño del bucle, los **managed agents** ejecutan exactamente este bucle por ti.
