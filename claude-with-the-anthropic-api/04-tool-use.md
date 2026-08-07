# 04 — Tool use

**Tool use** = método para que Claude acceda a **información externa** más allá de sus datos de entrenamiento.

**La limitación por defecto:** Claude solo conoce lo que había en su entrenamiento. No tiene información actual ni en tiempo real.

## El flujo, en 5 pasos

1. Envías la petición inicial a Claude **más las instrucciones** para acceder a datos externos.
2. Claude **evalúa si necesita** datos externos y pide información concreta.
3. **Tu servidor ejecuta código** para obtener esos datos de la fuente externa.
4. Envías una **petición de seguimiento** a Claude con los datos recuperados.
5. Claude genera la **respuesta final** usando el prompt original + los datos externos.

> Ejemplo del tiempo: el usuario pregunta el tiempo actual → Claude pide datos meteorológicos → tu servidor llama a una API del tiempo → Claude recibe los datos → Claude responde informado.

**La idea:** las herramientas permiten a Claude aumentar sus respuestas con información viva, **orquestando la recuperación de datos entre sus propias peticiones**.

## El proyecto del curso

**Objetivo:** enseñar a Claude a poner recordatorios con fecha y hora.

> Usuario: *"Ponme un recordatorio para la cita del médico, dentro de una semana desde el jueves"* → Claude: *"Te avisaré en ese momento"*

**Tres problemas que obligan a usar herramientas:**

| Problema | Por qué |
|---|---|
| **Desconoce la hora** | Claude sabe la fecha actual, pero no la hora exacta |
| **Calcula mal el tiempo** | A veces se equivoca sumando fechas (p. ej. 379 días desde el 13 de enero de 1973) |
| **No puede poner recordatorios** | Entiende el concepto, pero no tiene forma de implementarlo |

**Tres herramientas correspondientes:**

1. **Fecha y hora actuales** — obtiene ambas.
2. **Sumar duración** — añade una duración a una fecha/hora.
3. **Poner recordatorio** — lo crea de verdad.

Se construyen **de una en una**, hasta coordinar varias.

## Las funciones de herramienta

Funciones Python normales que se ejecutan cuando Claude determina que necesita datos adicionales.

**Tres buenas prácticas:**

1. **Nombres descriptivos** de función y de argumentos.
2. **Validación de entradas**, lanzando el error de inmediato si son inválidas.
3. **Mensajes de error con significado**, que guíen la corrección.

> **Los mensajes de error son visibles para Claude**, así que puede reintentar con los parámetros corregidos. Escríbelos pensando en que los va a leer él.

```python
def get_current_datetime(date_format="%Y%m%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date format cannot be empty")
    return datetime.now().strftime(date_format)
```

**El ciclo:** Claude detecta que necesita información → llama a la función → recibe resultado o error → si hubo error, puede reintentar corregido.

## Los esquemas de herramienta

**Tool schema** = especificación en **JSON Schema** que describe la función y sus parámetros para el modelo.

> **JSON Schema** es una especificación de validación de datos **que no es específica de ML**; la comunidad la adoptó para tool calling.

| Campo | Contenido |
|---|---|
| `name` | Identificador de la herramienta |
| `description` | **3-4 frases** explicando qué hace, cuándo usarla y qué datos devuelve |
| `input_schema` | El JSON Schema con los argumentos, sus tipos y descripciones |

### El truco para generar esquemas

1. Lleva tu función a claude.ai.
2. Pídele: *"write valid JSON schema spec for tool calling for this function, follow best practices in attached documentation"*.
3. **Adjunta la página de tool use de la documentación del API de Anthropic.**
4. Copia el esquema generado.

**Convenciones:** nombra las funciones de forma descriptiva, nombra los esquemas como `[nombre_función]_schema`, importa **`ToolParam`** desde `anthropic.types` y **envuelve el diccionario del esquema con `ToolParam()`** para evitar errores de tipo.

## Bloques de mensaje

Al hacer peticiones con herramientas, incluyes los esquemas junto al mensaje de usuario mediante el argumento **`tools`**.

**Y cambia la estructura del contenido:** los mensajes pasan a contener **varios bloques**, no solo bloques de texto.

La respuesta de Claude con herramienta trae:

- **Bloque de texto** — la explicación de cara al usuario.
- **Bloque tool use** — el nombre de la función y los argumentos.

> ⚠ **Requisito crítico:** mantén el historial a mano, porque Claude no guarda nada. Y al añadir la respuesta al historial, **añade `response.content` entero (todos los bloques)**, no solo el texto.

Las funciones `add_user_message` y `add_assistant_message` hay que **actualizarlas para soportar múltiples bloques**.

## Enviar resultados de herramienta

**Estructura del bloque de resultado:**

| Campo | Qué es |
|---|---|
| **`tool_use_id`** | Coincide con el ID del bloque tool use original. **Empareja peticiones con resultados** |
| `content` | La salida de la función convertida a cadena, normalmente JSON |
| `is_error` | Booleano para errores de ejecución. Por defecto `false` |

> **Para qué sirve el `tool_use_id`:** enlaza cada petición con su resultado cuando Claude hace **varias llamadas simultáneas**. Cada tool use tiene un ID único y cada resultado debe referenciar el suyo.

**Requisitos de la petición de seguimiento:**

- Incluir el **historial completo**: mensaje de usuario original + mensaje de asistente con el tool use + nuevo mensaje de usuario con el resultado.
- **Incluir los esquemas originales**, aunque no vayas a usar herramientas otra vez.
- ⚠ **El bloque de resultado va en un mensaje de usuario, no de asistente.**

## Conversaciones multi-turno con herramientas

Conversaciones donde Claude usa **varias herramientas en secuencia** para responder a una sola consulta.

**El encadenado:** usuario pregunta → Claude pide la primera herramienta → se ejecuta → devuelve resultado → Claude pide la segunda → se ejecuta → devuelve resultado → Claude da la respuesta final.

> Ejemplo: *"¿qué día es dentro de 103 días?"* → `get_current_datetime` → `add_duration_to_datetime` → respuesta.

**Patrón de implementación:** un bucle `while` que sigue llamando a Claude hasta que no pida más herramientas, comprobando cada respuesta en busca de bloques `tool_use`.

**Refactorizaciones necesarias:**

- `add_user_message` / `add_assistant_message` → manejar múltiples bloques.
- `chat` → aceptar el parámetro `tools` y devolver **el mensaje entero**, no solo el primer bloque de texto.
- `text_from_message` → helper que extrae todos los bloques de texto de un mensaje.

> **La clave:** no puedes predecir cuántas herramientas necesitará una consulta, así que el sistema debe manejar **cadenas arbitrarias** de llamadas automáticamente.

## Implementar los múltiples turnos

**`stop_reason`** = campo que indica por qué dejó de generar Claude. **`stop_reason == "tool_use"`** significa que quiere llamar a una herramienta. Hay otros valores, pero este es el que se comprueba casi siempre.

### `run_conversation` — el bucle principal

1. Llama a Claude con los mensajes + las herramientas disponibles.
2. Añade la respuesta al historial.
3. Comprueba `stop_reason` — si **no** es `tool_use`, **sale del bucle**.
4. Si lo es, llama a `run_tools`.
5. Añade los resultados como **mensaje de usuario**.
6. Repite.

### `run_tools` — procesa varios bloques

1. Filtra `message.content` por bloques con `type="tool_use"`.
2. Itera sobre cada petición.
3. Ejecuta la función vía `run_tool`.
4. Crea bloques `tool_result` con `type`, `tool_use_id`, `content` (JSON) e `is_error`.
5. Devuelve la lista de todos los resultados.

### `run_tool` — el dispatcher

Recibe `tool_name` y `tool_input`, usa condicionales para emparejar nombres con funciones, ejecuta la que toque. **Escalable** para añadir más herramientas.

**Manejo de errores** con `try`/`except` alrededor de la ejecución: éxito → `is_error=false` con la salida; fallo → `is_error=true` con el mensaje de error.

**Puntos de arquitectura:**

- Un mensaje de asistente puede contener **varios bloques**: texto + varios `tool_use`.
- **Cada bloque `tool_use` recibe su propio `tool_result`.**
- Todos los resultados vuelven **en un mensaje de usuario**.
- El proceso se repite hasta que Claude devuelve una respuesta final solo de texto.

## Añadir más herramientas

Una vez montado el andamiaje, añadir una herramienta son **3 pasos**:

1. Añadir su **esquema** a la lista `tools` de `run_conversation`.
2. Añadir un **caso condicional** en `run_tool` para su nombre.
3. **Implementar la función**.

En el ejemplo se añaden `AddDurationToDateTime` (calcula fecha con desplazamiento) y `SetReminder` (implementación simulada que imprime confirmación).

> **Encadenado:** Claude puede usar varias herramientas en secuencia dentro de una misma conversación — primero calcular la fecha, luego poner el recordatorio con ese resultado.

**Escalabilidad:** tras el montaje inicial, añadir herramientas se vuelve un patrón mecánico de **esquema + enrutado + implementación**.
