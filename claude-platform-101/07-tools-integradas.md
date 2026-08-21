# 07 — Tools integradas

*15 minutos* · [Vídeo](https://www.youtube.com/embed/pm8iwdSIs3M)

**Al terminar sabrás:** qué son las server tools y por qué **no** necesitan bucle de agente · los nuevos tipos de bloque que aparecen en la respuesta · qué son las client tools · el aviso sobre fiarse de la web.

---

Puedes construir tus propias tools, pero **algunas capacidades son tan comunes que Anthropic las trae ya hechas**. No escribes el código. No alojas el sandbox. **Declaras la tool y Anthropic la ejecuta.**

## Server tools: declaradas por ti, ejecutadas por Anthropic

Las **server tools** corren **en la infraestructura de Anthropic**. Tú no las ejecutas. Eso significa que **no necesitas un bucle de agente** para estas llamadas: Claude llama a las tools por su cuenta y **el resultado vuelve dentro de la misma respuesta**.

Las principales:

| Server tool | Qué hace |
|---|---|
| **Web search** | Busca en internet y devuelve resultados **con citas** |
| **Code execution** | Escribe y ejecuta **Python en un sandbox** |
| **Web fetch** | Recupera el contenido completo de URLs |

## Dos server tools en un fichero

Dos llamadas a `messages.create`, una con web search y otra con code execution:

```
import anthropic

client = anthropic.Anthropic()

# Call 1: web search — Anthropic runs the search server-side
search_response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
    messages=[
        {"role": "user", "content": "What is Anthropic's latest model release? Answer in one sentence."}
    ],
)

for block in search_response.content:
    if block.type == "server_tool_use":
        print(f"Tool call: {block.name} — {block.input}")
    elif block.type == "text":
        print(block.text)

# Call 2: code execution — Claude writes and runs Python in a sandbox
code_response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "code_execution_20260120", "name": "code_execution"}],
    messages=[
        {"role": "user", "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"}
    ],
)

for block in code_response.content:
    if block.type == "server_tool_use":
        print(f"Tool call: {block.name} — {block.input}")
    elif block.type == "bash_code_execution_tool_result":
        print(f"stdout: {block.content.stdout}")
    elif block.type == "text":
        print(block.text)
```

Dos cosas que mirar:

1. **Aquí no hay bucle de agente.** No conmutamos sobre `stop_reason`. No devolvemos resultados de tools. **Anthropic ejecuta la tool en el servidor y la respuesta ya trae el resultado.**
2. **La respuesta trae tipos de bloque nuevos.** Un bloque **`server_tool_use`** para la llamada, un bloque de resultado de ejecución de código para la salida, más los bloques `text` de siempre.

## Ejecutándolo

Para **web search** verás la llamada a la tool impresa, y luego una respuesta de una frase sobre el último lanzamiento de modelo, **con las citas de la búsqueda integradas**.

Para **code execution** verás el Python que Claude escribió de verdad, el **stdout** del sandbox ejecutándolo, y una respuesta de texto final.

No tuvimos que levantar un crawler de búsqueda. No ejecutamos un sandbox de Python. **Declaramos dos tools y obtuvimos las dos gratis.**

## La otra categoría: client tools

Conviene saber que existe la otra categoría. **Las client tools corren donde corre tu código.** Vienen en el SDK de Claude, así que **no tienes que definir el schema**. Dos ejemplos:

- **Memory** — Claude lee y escribe memoria **entre sesiones**
- **Bash** — un shell bash **persistente** para que Claude ejecute comandos

Tienen la misma forma que una tool personalizada, pero **el SDK te da el schema y un runner sensato**.

## Por qué importa en producción

En una app real, esto es el camino más corto hacia funcionalidades que si no llevarían semanas. Web search puede alimentar un endpoint de verificación que contrasta **cada afirmación numérica y regulatoria** de un borrador contra la web en vivo.

> **Un recordatorio, eso sí:** que algo esté validado en internet **no significa que sea verdad**. Comprueba siempre el trabajo de Claude.

## Conclusiones

- Las **server tools** — web search, code execution, web fetch — se declaran en tu array `tools`. **Las ejecuta Anthropic.**
- Recibes el resultado **en la misma respuesta**, **sin bucle de agente**. Busca bloques `server_tool_use` y de resultado de tool junto a los de texto.
- Las **client tools** como memory y bash corren donde corre tu código, pero el SDK te da el schema y un runner.
- La idea de "alojado por Anthropic" escala hasta arriba: **los managed agents la aplican al agente entero**, no solo a una tool.
