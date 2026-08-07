# 01 — Acceder a Claude con el API

## Los tres modelos

Claude tiene **tres familias de modelo**, optimizadas para prioridades distintas. Todas comparten las capacidades base —generación de texto, código, análisis de imágenes—; lo que cambia es **el foco de optimización**.

| Modelo | Para qué | Contrapartida |
|---|---|---|
| **Opus** | La mayor inteligencia. Tareas complejas, multipaso, que exigen razonamiento profundo y planificación | Mayor coste y latencia |
| **Sonnet** | Equilibrado: buena inteligencia, velocidad y coste. Fuerte en programación y edición precisa de código | — |
| **Haiku** | El más rápido, optimizado para velocidad y coste. **No tiene las capacidades de razonamiento de Opus/Sonnet** | Menos profundidad |

**Marco de elección:** prioridad inteligencia → **Opus**. Prioridad velocidad → **Haiku**. Requisitos equilibrados → **Sonnet**.

> **Enfoque habitual:** usar **varios modelos en la misma aplicación** según lo que pida cada tarea, en vez de elegir uno solo para todo.

## Cómo se accede al API

El flujo de 5 pasos, de la entrada del usuario a la respuesta en pantalla:

**Paso 1 · El cliente envía el texto a tu servidor.**

> ⚠ **Nunca accedas al API de Anthropic directamente desde una aplicación cliente**: la clave de API debe permanecer secreta.

**Paso 2 · Tu servidor llama al API**, con un SDK (Python, TypeScript, JavaScript, Go, Ruby) o HTTP plano. Parámetros obligatorios: **clave de API + nombre del modelo + lista de mensajes + `max_tokens`**.

**Paso 3 · La generación de texto, en cuatro etapas:**

| Etapa | Qué hace |
|---|---|
| **Tokenización** | Parte la entrada en **tokens** — palabras, trozos de palabra, símbolos, espacios |
| **Embedding** | Convierte los tokens en listas de números que representan todos los significados posibles de esa palabra |
| **Contextualización** | Ajusta los embeddings según los tokens vecinos, para fijar el significado preciso |
| **Generación** | La capa de salida produce probabilidades para la siguiente palabra; el modelo la selecciona combinando probabilidad y aleatoriedad, la añade y repite |

**Paso 4 · El modelo se detiene** al alcanzar `max_tokens` o al generar un token especial de fin de secuencia.

**Paso 5 · El API devuelve** el texto generado + los contadores de uso + el `stop_reason`. Tu servidor se lo pasa al cliente.

### Vocabulario

- **Token** — trozo de texto: palabra, parte de palabra o símbolo.
- **Embedding** — representación numérica de significados.
- **Contextualización** — afinar el significado usando las palabras vecinas.
- **`max_tokens`** — **límite de longitud de generación**, no una longitud objetivo.
- **`stop_reason`** — por qué dejó de generar el modelo.

## Conseguir una clave de API

1. Ve a [console.anthropic.com](https://console.anthropic.com/) e inicia sesión.
2. Botón **Get API Keys**, arriba a la derecha del panel principal.
3. Botón **Create Key**.
4. Elige el workspace `Default` y ponle un nombre identificativo (p. ej. `Anthropic Course`).
5. **Copia la clave.** Se muestra **una sola vez**. Si cierras la ventana sin copiarla, borra la clave y genera otra.

## La primera petición

**Preparación:**

1. `pip install anthropic python-dotenv`
2. Crea un `.env` con `ANTHROPIC_API_KEY="tu_clave"` — **ignóralo en el control de versiones**.
3. Carga la variable con `python-dotenv`.
4. Crea el cliente y define la variable del modelo.

**Estructura de la petición** — función `client.messages.create()`:

| Argumento | Qué es |
|---|---|
| `model` | Nombre del modelo de Claude |
| `max_tokens` | **Límite de seguridad** de longitud, no la longitud deseada |
| `messages` | Lista con los intercambios de la conversación |

```python
client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is quantum computing?"}]
)
```

- **Mensaje de usuario:** `{"role": "user", "content": "tu texto"}` — contenido escrito por humanos.
- **Mensaje de asistente:** contiene las respuestas generadas por el modelo.
- **Acceder al texto:** la respuesta completa trae metadatos y estructura anidada; el texto suelto está en **`message.content[0].text`**.

## Conversaciones multi-turno

> **La limitación clave: el API de Anthropic no almacena ningún mensaje.** Cada petición es independiente y no recuerda nada de las anteriores.

La solución tiene dos partes:

1. **Mantener la lista de mensajes a mano**, en tu código.
2. **Enviar el historial completo** con cada petición de seguimiento.

**Flujo de la conversación:**

1. Envía el mensaje de usuario inicial.
2. Recibe la respuesta del asistente.
3. **Añade la respuesta del asistente al historial.**
4. Añade el nuevo mensaje del usuario al historial.
5. Envía el historial completo para que el seguimiento tenga contexto.

**Funciones auxiliares que hacen falta:**

- `add_user_message(messages, text)`
- `add_assistant_message(messages, text)`
- `chat(messages)` — envía el historial al API y devuelve la respuesta

> Sin historial, las respuestas pierden contexto y continuidad. Con historial completo, Claude mantiene el hilo.

## System prompts

**Técnica para personalizar el estilo y el tono** de Claude asignándole un rol o un patrón de comportamiento.

> **Controlan *cómo* responde Claude, no *qué* responde.**

- Se pasa como cadena al argumento `system` de `create`.
- **Estructura:** la primera línea suele asignar el rol (*"You are a patient math tutor"*), seguida de instrucciones de comportamiento concretas.
- La misma pregunta recibe un tratamiento distinto según el rol asignado.

**Implementación:** crea un diccionario `params`, añade la clave `system` **solo si hay prompt**, y pásalo a `create` con `**`. Si no hay system prompt, **excluye el parámetro por completo** en vez de pasar `None`.

**Ejemplo de uso:** un tutor de matemáticas que da pistas en vez de soluciones completas, para que el alumno piense.

## Temperature

Parámetro de **0 a 1** que controla la aleatoriedad influyendo en las probabilidades de selección de token.

| Valor | Efecto | Cuándo |
|---|---|---|
| **0** | Salida **determinista**: siempre elige el token más probable | Extracción de datos, tareas factuales que exigen consistencia |
| **Cercano a 1** | Aumenta la probabilidad de elegir tokens menos probables: salidas más creativas e inesperadas | Brainstorming, escritura, chistes, marketing |

> Subir la temperatura **no garantiza** una salida distinta: solo aumenta la probabilidad de variación. Manipula directamente la distribución de probabilidad del siguiente token.

## Streaming de respuestas

Mostrar la respuesta **trozo a trozo mientras se genera**, en vez de esperar a que esté completa.

**Problema que resuelve:** una respuesta puede tardar 10-30 segundos. Los usuarios esperan feedback inmediato, no un spinner.

**Cómo funciona:**

1. Tu servidor envía el mensaje a Claude.
2. Claude manda enseguida una respuesta inicial — sin texto, solo acuse de recibo.
3. Sigue un flujo de eventos, cada uno con un trozo de texto.
4. Tu servidor reenvía los trozos al frontend para mostrarlos en tiempo real.

**Tipos de evento:**

| Evento | Qué es |
|---|---|
| `message_start` | Acuse de recibo inicial |
| `content_block_start` | Empieza la generación de texto |
| **`content_block_delta`** | **Contiene los trozos de texto reales** — el más importante |
| `content_block_stop` / `message_stop` | Generación completa |

**Implementación:**

- Básica: `client.messages.create(stream=True)` devuelve un iterador de eventos.
- Simplificada: `client.messages.stream()` con la propiedad **`text_stream`** extrae solo el texto.
- Mensaje final: **`stream.get_final_message()`** ensambla todos los trozos, para guardarlos.

## Controlar la salida del modelo

Dos técnicas que van más allá de reescribir el prompt.

### Pre-fill del mensaje de asistente

Añadir a mano un mensaje de asistente al final de la conversación para **dirigir la respuesta**.

- Claude ve ese mensaje como contenido **que ya escribió él**.
- **Continúa desde el final exacto** del texto pre-rellenado.

> ⚠ Continúa desde el punto exacto, **no desde frases completas**. Tendrás que unir el pre-fill con la respuesta generada.

Ejemplo: pre-fill *"Coffee is better because"* → Claude sigue con la justificación.

### Stop sequences

Fuerzan a Claude a **detener la generación** cuando aparece una cadena concreta.

- Le pasas la cadena a la función de chat.
- Cuando Claude genera esa cadena exacta, la respuesta se corta al instante.
- **El texto de la stop sequence no se incluye** en la salida final.

Ejemplo: prompt *"cuenta del 1 al 10"* + stop sequence `"five"` → sale `"one, two, three, four, "`. Afinándola a `", five"` → sale limpio: `"one, two, three, four"`.

## Datos estructurados

Combinar **pre-fill + stop sequence** para obtener salida cruda sin las cabeceras y comentarios que Claude añade por su cuenta.

**Problema:** Claude añade automáticamente formato markdown, encabezados y comentarios al generar JSON o código. Muchas veces solo quieres el dato, listo para copiar y pegar.

**El patrón:**

1. **Mensaje de usuario** — la petición del dato estructurado.
2. **Pre-fill del asistente** — el delimitador de apertura, p. ej. ` ```json `.
3. **Stop sequence** — el delimitador de cierre, ` ``` `.

Claude ve el mensaje pre-rellenado, asume que ya empezó a responder, **genera solo el contenido pedido** y se detiene al llegar al delimitador.

> Funciona para **cualquier** tipo de dato estructurado —JSON, código Python, listas—, no solo JSON. Úsalo siempre que necesites salida limpia y parseable sin texto explicativo.
