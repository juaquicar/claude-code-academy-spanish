# 05 — Herramientas avanzadas y predefinidas

Cinco piezas que van más allá del patrón básico de tool use: dos trucos de diseño y tres herramientas que Claude ya trae.

---

## La batch tool

Herramienta que permite a Claude **ejecutar varias herramientas en paralelo dentro de un solo mensaje de asistente**, en vez de hacer peticiones secuenciales separadas.

**El problema:** Claude *puede* técnicamente enviar varios bloques `tool_use` en un mensaje, pero **rara vez lo hace en la práctica**. El resultado son llamadas secuenciales innecesarias.

**La solución:** crear un esquema de batch tool que reciba una **lista de invocaciones** (cada una con nombre de herramienta + argumentos). En vez de llamar a las herramientas directamente, Claude llama a la batch tool con un array de ejecuciones deseadas.

**Implementación:**

1. Añade la batch tool al esquema, con un parámetro `invocations`.
2. Crea `run_batch` que itere sobre la lista.
3. Extrae de cada invocación el nombre y los argumentos parseados de JSON.
4. Llama a `run_tool` por cada una.
5. Devuelve `batch_output` con los resultados de todas.

> **El mecanismo:** engaña a Claude para conseguir ejecución paralela, ofreciéndole una abstracción de más alto nivel que hace a mano lo que varios bloques `tool_use` harían automáticamente.

**Resultado:** un solo ciclo petición-respuesta en vez de varias rondas secuenciales para tareas paralelizables.

---

## Herramientas para datos estructurados

Método alternativo para extraer JSON estructurado **usando el sistema de herramientas** en vez del pre-fill + stop sequences del capítulo 1.

| | Pre-fill + stop sequence | Herramienta |
|---|---|---|
| Fiabilidad | Menor | **Mayor** |
| Complejidad de montaje | Menor | Mayor |
| Requiere JSON Schema | No | **Sí** |

**El proceso:**

1. Define un JSON Schema donde **las entradas de la herramienta son la estructura de datos que quieres**.
2. Envía el prompt + el esquema a Claude.
3. Claude llama a la herramienta con argumentos que encajan con el esquema.
4. Extrae el JSON del bloque `tool_use` — **no hace falta enviar un tool result**.

> ⚠ **Requisito crítico: fuerza la llamada** con el parámetro `tool_choice`:
> ```python
> tool_choice = {"type": "tool", "name": "tu_herramienta"}
> ```
> Así te aseguras de que Claude siempre llama a esa herramienta.

Los datos estructurados salen de **`response.content[0].input`**.

**Cuándo usar cuál:** los métodos por prompt son mejores para extracciones rápidas y simples; **las herramientas, para extracciones complejas donde la fiabilidad importa más que la simplicidad**.

---

## Fine-grained tool calling

### Streaming con herramientas

- El streaming normal devuelve eventos `content_block_delta`.
- El streaming con herramientas **añade eventos `input_json_delta`**, con `partial_json` (el trozo) y `snapshot` (la suma acumulada).
- Implementarlo requiere manejar ese tipo de evento adicional en tu pipeline.

### El comportamiento por defecto

1. Claude genera trozos de JSON para los argumentos de la herramienta.
2. **El API los almacena en búfer** hasta tener un par clave-valor de nivel superior completo.
3. **Valida el JSON contra el esquema** antes de enviarlos.
4. Resultado: retrasos seguidos de ráfagas de trozos llegando a la vez.

### El modo fine-grained (`fine_grained: true`)

- **Desactiva la validación de JSON** del lado del API.
- Envía los trozos **inmediatamente** conforme se generan.
- Da la experiencia de streaming tradicional.
- ⚠ **Requiere manejo de errores del lado del cliente** para JSON inválido.

| | Por defecto | Fine-grained |
|---|---|---|
| Velocidad | Más lento | **Más rápido** |
| JSON | **Validado** | Puede ser inválido (p. ej. `"undefined"` en vez de `null`) |

> Si en el modo por defecto llega JSON inválido, se envuelve como cadena en lugar de como estructura de objeto.

**Cuándo:** fine-grained es útil para **actualizar la interfaz al instante** o procesar argumentos de herramienta pronto. El modo por defecto basta cuando el retraso de validación es aceptable.

---

## La text edit tool

**Herramienta integrada** de Claude para operaciones de fichero y texto: leer, escribir, crear, reemplazar y deshacer en ficheros y directorios.

> **Solo el JSON Schema viene integrado en Claude; la implementación la escribes tú.**

**Características:**

- El **stub del esquema** que envías se auto-expande al esquema completo del lado de Claude.
- El **string de tipo varía según la versión del modelo** — 3.5 y 3.7 llevan fechas distintas.
- Convierte a Claude en un ingeniero de software **de fábrica**.

**Lo que tienes que implementar:** una clase o funciones que atiendan las peticiones de Claude — ver ficheros, reemplazar cadenas, crear ficheros… **Las operaciones reales sobre el sistema de ficheros no vienen dadas.**

**Flujo:**

1. Envías el stub mínimo (nombre + tipo con la fecha de tu versión).
2. Claude lo expande internamente al esquema completo.
3. Claude envía peticiones de tool use.
4. **Tu implementación ejecuta las operaciones reales.**
5. Los resultados vuelven a Claude.

**Casos de uso:** replicar un editor de código con IA, operaciones de ficheros donde no hay editor nativo, generación y refactorización automática de código, manipulación de proyectos multi-fichero.

---

## La web search tool

**Herramienta integrada** para buscar en la web información actualizada o especializada.

> **No hace falta código propio: Claude ejecuta la búsqueda automáticamente.** Es la diferencia con la text edit tool.

**Esquema:**

| Campo | Valor |
|---|---|
| `type` | `"web_search_20250305"` |
| `name` | `"web_search"` |
| `max_uses` | Límite de búsquedas totales. **Por defecto 5** |
| `allowed_domains` | Lista opcional para restringir la búsqueda a dominios concretos |

**Estructura de la respuesta:**

- **Bloques de texto** — la explicación de Claude.
- **Bloques tool use** — las consultas que ejecutó.
- **Bloques de resultado de búsqueda** — las páginas encontradas: título y URL.
- **Bloques de cita** — el texto concreto que respalda cada afirmación de Claude.

**Cómo renderizarlo:** los bloques de texto como texto normal, los resultados como lista de referencias, y las citas destacadas con su atribución — dominio, título, URL y el texto citado.

> **Ejemplo de uso:** restringir a `NIH.gov` para consejo médico o de ejercicio garantiza información con respaldo científico en vez de contenido genérico de la web.
