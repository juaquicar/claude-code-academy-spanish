# 05 — ¿Qué es el uso de tools?

*20 minutos* · [Vídeo](https://www.youtube.com/embed/Ao759wXbRc0)

**Al terminar sabrás:** quién ejecuta realmente una tool · las tres partes de una definición · por qué la descripción es la causa número uno de fallos · cómo se despacha entre varias tools · qué te ahorra el tool runner.

---

Tus flujos de trabajo dependen de un montón de tecnologías distintas — software de gestión de proyectos, bases de datos, ficheros. **Claude no puede consultar esas cosas por sí mismo.** En su lugar depende de **tools**, que le dan acceso a datos y acciones externas.

## Qué es una tool

Dicho simple: una tool es **una función que tú defines y expones a Claude**. Describes qué hace y qué entradas toma, y **Claude decide cuándo llamarla**.

> **Lo que hay que interiorizar: Claude no ejecuta la tool — tu código sí.**

El flujo:

1. **Claude pide** una llamada a la tool.
2. **Tu código ejecuta** la función.
3. **El resultado vuelve a Claude**, y sigue.

> **Trampa de examen.** No la ejecuta el modelo «por dentro» de la respuesta, ni Anthropic en sus servidores (salvo las **server tools** del capítulo 07), ni el SDK bloquea esperando a un humano. **La ejecuta tu código y le devuelve el resultado.** Es la pregunta 2 del quiz oficial.

## Cómo se definen

Las tools son **JSON schemas con tres partes**: un **name**, una **description** y un **input schema**. Se las pasas a Claude en el cuerpo de la petición, en un array **`tools`**.

> **La `description` es lo que Claude lee para decidir si llamar a la tool.** Si escribes una descripción vaga, obtienes mal uso de tools. **Esta es la razón número uno por la que los agentes fallan** o no cogen las tools disponibles. Sé específico.

```
{
  "name": "lookup_building_code",
  "description": "Look up a specific building code section by its identifier. Returns the full text of that code section.",
  "input_schema": {
    "type": "object",
    "properties": {
      "section": {
        "type": "string",
        "description": "The building code section to look up"
      }
    },
    "required": ["section"]
  }
}
```

¿Qué pasa al usarla? Si le mandamos a un agente un informe de cumplimiento, en el primer turno Claude vuelve con **`stop_reason: "tool_use"`** — esa es la señal. Nuestro bucle llama a `lookup_building_code` con el parámetro que Claude pidió y le devuelve el resultado como **tool result**: un mensaje de usuario que contiene un bloque `tool_result` **ligado al id de la llamada**. Y Claude sigue. A partir de ahí podemos seguir llamando tools y devolviendo resultados hasta que tenga lo que necesita.

## Varias tools: dejar que Claude elija

Una tool es útil, pero lo interesante es darle **varias** y ver cuál elige y en qué orden.

Imagina que preparas un viaje de tres días a Denver y quieres el tiempo de hoy **y** la previsión de los próximos días. Declaramos dos tools:

```
const tools = [
  {
    name: "get_weather",
    description: "Get today's current weather for a city.",
    input_schema: {
      type: "object",
      properties: {
        city: { type: "string", description: "The city to check" }
      },
      required: ["city"]
    }
  },
  {
    name: "get_forecast",
    description: "Get the weather forecast for the next few days for a city.",
    input_schema: {
      type: "object",
      properties: {
        city: { type: "string", description: "The city to check" }
      },
      required: ["city"]
    }
  }
];
```

El bucle es **idéntico** al que ya hemos visto. La única pieza nueva es una función `runTool` que **despacha según el nombre de la tool** con un switch — ese bloque es literalmente donde corre tu código:

```
function runTool(name, input) {
  switch (name) {
    case "get_weather":
      return getWeather(input.city);
    case "get_forecast":
      return getForecast(input.city);
  }
}

while (true) {
  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages,
    tools,
  });

  if (response.stop_reason !== "tool_use") {
    // Claude is done — this is the final answer
    break;
  }

  messages.push({ role: "assistant", content: response.content });

  const toolResults = response.content
    .filter((block) => block.type === "tool_use")
    .map((block) => ({
      type: "tool_result",
      tool_use_id: block.id,
      content: runTool(block.name, block.input),
    }));

  messages.push({ role: "user", content: toolResults });
}
```

Y ese es todo el patrón. **¿Una tercera tool? La añades al array, añades un case al switch, y ya.**

Al ejecutarlo verás a Claude llamar a `get_weather` y luego a `get_forecast` — a veces en el mismo turno, a veces uno tras otro. Y luego responde: lleva capas, hoy nieve ligera, va templando durante la semana.

Fíjate en **cómo** eligió: **leyó las descripciones**, mapeó tu prompt a "el tiempo de hoy" y "los próximos días", y eligió la tool correcta para cada uno. **Por eso importan tanto tus descripciones.**

## El tool runner: saltarse el boilerplate

Probablemente ya has visto dos banderas rojas en lo que acabamos de escribir:

- Es **mucho código** para dos consultas simples.
- En una base de código real **no quieres escribir JSON schemas a mano** para cada función que tienes. Es como escribir el código dos veces.

Ahí entra el **tool runner**. Viene en el SDK de Claude para **TypeScript, Python y Ruby**. El runner **toma tus funciones reales, lee los tipos y la documentación para construir el schema por ti**, y **gestiona internamente todo el ciclo de tool use / tool result**.

Tu código se reduce a: describe la tool, envía el prompt, espera el resultado.

```
// The same two lookups we ran by hand — just plain TypeScript functions
function getWeather(city: string) {
  // ...existing lookup
}

function getForecast(city: string) {
  // ...existing lookup
}

const runner = client.beta.messages.toolRunner({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content:
        "I'm packing for a three-day trip to Denver. What's the weather today and over the next few days?",
    },
  ],
  tools: [getWeather, getForecast],
});

// Returns the final assistant message after all the tool ping-pong has settled
const finalMessage = await runner.untilDone();
```

Mismo escenario, una fracción del código:

- **Sin bucle `while`**, sin switch de stop reason, sin meter resultados a mano en `messages` — el runner se encarga.
- **Sin JSON schemas**, así que no escribes las cosas dos veces.
- `runner.untilDone()` devuelve **el mensaje final del assistant** cuando todo se ha asentado.

## Las tools reales envuelven código que ya tienes

En la vida real tus tools no serían datos de tiempo hardcodeados: serían **envoltorios finos sobre funciones que ya existen en tu aplicación**. Un agente de revisión de cumplimiento tiene como tools envoltorios sobre `lookup_building_code` y `search_building_code`, que ya están en la base de código. Con el tool runner **le pasas esas funciones directamente**, y el agente cita secciones concretas del código en cada hallazgo — sin escribir schemas.

## Conclusiones

- **Las tools dan a Claude acceso a tus sistemas.** Tú defines y expones la función; Claude decide cuándo llamarla y **tu código la ejecuta**.
- Son **JSON schemas** con **name**, **description** e **input schema**, pasados en el array `tools`.
- **Escribe descripciones específicas.** Las descripciones vagas son la causa número uno de que los agentes fallen.
- **`stop_reason: "tool_use"`** es tu señal para ejecutar la tool y devolver el resultado.
- Con varias tools, **despachas por nombre**. Añadir una tool es añadirla al array y añadir un case.
- El **tool runner** del SDK (TypeScript, Python, Ruby) construye los schemas a partir de tus funciones reales y gestiona todo el bucle — o lo ejecutas tú.
- Tú ejecutas, o delegas el bucle. En el extremo de ese espectro, **los managed agents delegan el agente entero** en Anthropic.
