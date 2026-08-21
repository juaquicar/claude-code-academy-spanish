# 02 — Tu primera llamada a la API

*15 minutos* · [Vídeo](https://www.youtube.com/embed/j0ftK_R5DTs)

**Al terminar sabrás:** dónde guardar la API key · los **tres** parámetros que pide `messages.create` · para qué sirve el system prompt · por qué `content` es un **array de bloques** y no una cadena.

---

## Preparación

Primero, consigue una **API key** en `platform.claude.com`. Necesitas **comprar créditos** antes.

Guarda la API key en un fichero **`.env.local`** para que quede fuera de tu control de versiones.

> **Hardcodear keys en ficheros de código es exactamente cómo acaban filtradas en GitHub.** Fuera, en ficheros de entorno.

Después, instala el SDK:

```
npm install @anthropic-ai/sdk
```

## La anatomía de una petición

Toda llamada a la API pasa por la función **`messages.create`**. Especificas **tres cosas**:

| Parámetro | Qué es |
|---|---|
| **model** | Qué modelo de Claude atiende la petición |
| **max tokens limit** | Un **tope** a la longitud de la respuesta |
| **messages** | Una lista de objetos con rol `user` o `assistant`, estructurados como una conversación con Claude |

> **Trampa de examen.** Los tres que pide la llamada **en sí** son **modelo, límite de tokens y lista de mensajes**. La **API key** no va ahí (va en el cliente/entorno) y el **system prompt es opcional**. Es la pregunta 1 del quiz oficial.

En su forma más básica:

```
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: "Hello, Claude",
  }],
});
```

## Un ejemplo real: revisar código con bugs

Démosle a Claude algo más interesante que un "hola": le apuntamos a código con un bug y le pedimos una revisión. Todo en un fichero, unas 20 líneas:

```
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const buggyCode = `
function add(a, b) {
  return a - b;
}
`;

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: "You are a terse senior code reviewer. Give feedback in one paragraph.",
  messages: [
    { role: "user", content: `Review this code:\n${buggyCode}` },
  ],
});

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

Dos cosas que mirar:

1. **El `system` prompt es donde moldeas la persona.** Si quieres un revisor senior escueto y no uno charlatán, lo dices y ya.
2. **El `content` de la respuesta es un array de bloques, no una cadena.** Para una respuesta de texto normal suele haber un solo bloque de tipo `text`, pero **Claude puede devolver varios bloques** — texto, llamadas a tools, thinking — así que **siempre iteras y compruebas el tipo**.

Ejecútalo y Claude detecta que `add` está restando, y te lo dice en un párrafo. Eso es toda la llamada a la API.

## Del script al producto

En un producto real, esta misma forma de `messages.create` es el motor de algo como un endpoint de resumen: sacas la transcripción de una reunión de la base de datos, se la das a Claude con un system prompt que diga "extrae conclusiones y riesgos", guardas el resultado en la fila y lo devuelves a la interfaz. **Es la misma llamada, envuelta en un route handler.**

## Conclusiones

- Tu primera llamada es **`messages.create`** con un **modelo**, un **límite de tokens** y unos **mensajes**.
- Guarda tu API key en un fichero **`.env.local`** para mantenerla fuera del control de versiones.
- Añade un **system prompt** para moldear el comportamiento de Claude.
- El `content` de la respuesta es un **array de bloques**: itera y comprueba el `type` de cada uno.
- A partir de aquí, **todo se construye sobre este patrón**.
