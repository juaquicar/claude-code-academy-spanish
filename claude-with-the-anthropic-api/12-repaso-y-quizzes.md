# 12 — Repaso y evaluaciones

## Las evaluaciones oficiales — pendientes

El curso trae **7 quizzes por bloque** más una **evaluación final**. Están sin hacer a propósito: los harás tú al terminar de estudiar.

| # | Evaluación | Bloque | Estado |
|---|---|---|---|
| 1 | Quiz on accessing Claude with the API | Cap. 01 | ⬜ pendiente |
| 2 | Quiz on prompt evaluation | Cap. 02 | ⬜ pendiente |
| 3 | Quiz on prompt engineering techniques | Cap. 03 | ⬜ pendiente |
| 4 | Quiz on tool use with Claude | Cap. 04-05 | ⬜ pendiente |
| 5 | Quiz on features of Claude | Cap. 07-08 | ⬜ pendiente |
| 6 | Quiz on Model Context Protocol | Cap. 09 | ⬜ pendiente |
| 7 | Quiz on Agents and Workflows | Cap. 11 | ⬜ pendiente |
| — | **Final Assessment** | Todo | ⬜ pendiente |

> **Cuando los hagas, pásame los resultados** y registro aquí las preguntas reales con su feedback y los distractores, como en `claude-code-in-action/10-quiz.md`.
>
> Por el patrón de los otros cursos de la academia, espera preguntas **de escenario**: te plantean una situación y eliges la herramienta, con distractores que son herramientas reales usadas en el sitio equivocado.

---

## Chuleta

### Modelos y API

- **Opus** = máxima inteligencia, tareas complejas multipaso · **Sonnet** = equilibrio, fuerte en código · **Haiku** = el más rápido, **sin las capacidades de razonamiento** de los otros dos.
- Enfoque habitual: **varios modelos en la misma aplicación** según la tarea.
- **Nunca llames al API desde el cliente**: la clave se queda en tu servidor.
- Obligatorios: **clave + modelo + messages + `max_tokens`**.
- Generación en 4 etapas: **tokenización → embedding → contextualización → generación**.
- **`max_tokens` es un límite de seguridad**, no una longitud objetivo.
- **El API no almacena mensajes.** El historial lo mantienes tú y lo envías entero cada vez.
- **System prompt** = controla **cómo** responde, no **qué** responde.
- **Temperature** 0 = determinista (extracción de datos) · cerca de 1 = creativo. Subirla **no garantiza** salida distinta.
- Streaming: el evento que importa es **`content_block_delta`**. `stream.text_stream` para el texto, **`get_final_message()`** para guardar.
- **Pre-fill** = Claude continúa desde el **final exacto** del texto, no desde frases completas.
- **Stop sequence** = el texto que la dispara **no se incluye** en la salida.
- **Datos estructurados** = pre-fill con ` ```json ` + stop sequence ` ``` `.

### Evaluación de prompts

- Las dos trampas: probar una o dos veces y desplegar; o retocar a ojo para casos límite.
- Núcleo del pipeline: **dataset + prompt + LLM + grader**.
- Workflow de 6 pasos: prompt inicial → dataset → variaciones → respuestas → puntuar → iterar.
- Tres graders: **código** (validación programática), **modelo** (llamada extra al API), **humano**.
- ⚠ En un model grader, **pide fortalezas, debilidades y razonamiento antes que la puntuación**: si solo pides la nota, tiende a valores mediocres.
- Grading por código: `validate_json` / `validate_python` / `validate_regex` → 10 si válido, 0 si error.
- **Puntuación final = (puntuación del modelo + puntuación de sintaxis) / 2.**

### Prompt engineering — con las cifras

| Técnica | Puntuación |
|---|---|
| Prompt básico | **2,32** |
| + claro y directo | **3,92** |
| + específico | **7,86** |

- **Claro y directo:** verbo de acción en la **primera línea**, que es la parte más crítica.
- **Específico:** Tipo A = **atributos** (casi siempre) · Tipo B = **pasos** (problemas complejos).
- **XML:** nombres descriptivos (`sales_records`, no `data`). Ayuda incluso con contenido corto.
- **Ejemplos:** envuélvelos en XML, incluye el **razonamiento** de por qué son ideales, colócalos **después** de las instrucciones, y **usa como plantilla los de mejor puntuación de tus evals**.

### Tool use

- Los **mensajes de error son visibles para Claude**: escríbelos para que pueda reintentar corregido.
- Esquema: `name` + `description` de **3-4 frases** + `input_schema`.
- Truco: pídele el esquema a claude.ai **adjuntando la página de tool use de la documentación**.
- Envuelve el esquema con **`ToolParam()`**.
- **Añade `response.content` entero al historial**, no solo el texto.
- **`tool_use_id`** empareja cada petición con su resultado cuando hay varias llamadas simultáneas.
- ⚠ **El bloque de resultado va en un mensaje de USUARIO.**
- Incluye los esquemas originales en el seguimiento **aunque no vayas a usar herramientas**.
- **`stop_reason == "tool_use"`** = quiere llamar a una herramienta. Es la condición del bucle.
- Añadir herramienta = **esquema + enrutado + implementación**.

### Herramientas avanzadas

- **Batch tool** = engañar a Claude para paralelizar, dándole una herramienta que recibe una lista de `invocations`. Claude *puede* mandar varios bloques `tool_use` pero **rara vez lo hace**.
- **Datos estructurados por herramienta** = más fiable, más complejo. ⚠ Fuerza la llamada con **`tool_choice = {"type": "tool", "name": "..."}`**. Sale de `response.content[0].input`, **sin tool result**.
- **Fine-grained** = desactiva la validación de JSON del API → más rápido pero **JSON posiblemente inválido**. Evento nuevo: `input_json_delta` con `partial_json` y `snapshot`.
- **Text edit tool** = solo el **esquema** viene integrado; **la implementación la escribes tú**. El string de tipo cambia según la versión del modelo.
- **Web search tool** = **no hace falta código**, Claude busca solo. `max_uses` por defecto **5**, `allowed_domains` para restringir.

### RAG

- Dos opciones: meter el documento entero (choca con límites, caro, lento) o **trocear y recuperar**.
- Troceado: **por tamaño** (el más común, con **solapamiento** para no perder contexto), **por estructura** (requiere formato garantizado), **semántico** (el más avanzado). **No hay método universalmente mejor.**
- **Embedding** = lista de números de **-1 a +1**; su significado real es desconocido.
- Anthropic recomienda **Voyage AI**.
- Flujo de 7 pasos: trocear → embeddings → normalizar → base vectorial ‖ consulta → similitud → ensamblar prompt.
- **Similitud coseno** de -1 a 1, **cerca de 1 = similar**. **Distancia** = 1 − similitud, **cerca de 0 = similar**.
- ⚠ **Guarda el texto original junto al embedding** o los resultados no sirven.
- **BM25** = léxico. **Términos raros pesan más** que los comunes. Compensa que la búsqueda semántica se pierde coincidencias exactas.
- **Reciprocal Rank Fusion** = `Σ 1/(rank+1)` para fusionar índices.
- **Reranking** = un LLM reordena los resultados. Usa **IDs, no texto completo**. Sube precisión, **añade latencia**.
- **Contextual retrieval** = añadir contexto a cada trozo **antes** de generar su embedding. Si el documento no cabe: trozos iniciales + los inmediatamente anteriores, saltándose los del medio.

### Funcionalidades

- **Extended thinking:** budget mínimo **1024 tokens**, y **`max_tokens` debe superarlo**. El bloque de pensamiento lleva **firma criptográfica** anti-manipulación. Actívalo **cuando optimizar el prompt no baste**.
- **Imágenes:** máximo **100 por petición**, consumen tokens según píxeles. **La precisión depende del prompt, no de la imagen.**
- **PDF:** `type: "document"` + `media_type: "application/pdf"`. Lee texto, imágenes, gráficas y tablas.
- **Citations:** `"citations": {"enabled": true}` + campo `title`. `citation_page_location` para PDF, `citation_char_location` para texto plano.
- **Code execution:** contenedores Docker **sin acceso a red**; la entrada/salida va por la **Files API**.

### Prompt caching

- Duración **1 hora**. Activación **manual** con cache breakpoints.
- ⚠ **La forma corta (`content = "texto"`) no admite cache control.** Hace falta la forma larga con lista de bloques.
- **Orden de procesado: tools → system prompt → messages.**
- **Máximo 4 breakpoints** por petición. **Mínimo 1024 tokens** para cachear.
- Se cachea **todo hasta el breakpoint incluido**. **Cualquier cambio antes del breakpoint invalida el caché entero.**
- `cache_control` de tipo **`"ephemeral"`**. Buena práctica: **clona la lista de herramientas** antes de modificarla.
- Campos de uso: **`cache_creation_input_tokens`** (escritura) y **`cache_read_input_tokens`** (lectura).

### MCP

- Traslada la carga de integración **del desarrollador de la aplicación al mantenedor del servidor MCP**.
- **MCP y tool use son complementarios**: MCP decide **quién** hace el trabajo.
- Mensajes: `list tools request/result`, `call tool request/result`.
- **`@mcp.tool`** auto-genera el JSON Schema desde la firma de la función. `Field()` para describir argumentos.
- **`mcp dev servidor.py`** abre el **Inspector** en el navegador, para probar sin integrar la aplicación.
- **Resources**: URI **directa** (`docs://documents`) o **con plantilla** (`docs://documents/{doc_id}`). Decorador `@mcp.resource` con URI y MIME type.
- ⚠ **Resources = datos, proactivos. Tools = acciones, reactivas.**
- El cliente **deserializa**: si `mime_type == "application/json"` → `json.loads`, si no → texto.
- **Prompts** = plantillas probadas que define el autor del servidor; aparecen como **slash commands** en el cliente.

### Claude Code y computer use

- `init` → escanea el codebase y crea **`claude.md`**, incluido automáticamente después.
- **`#`** añade notas a la memoria. Memorias: proyecto, local, usuario.
- Dos métodos: **analizar → planificar → implementar**, o **TDD**.
- `claude mcp add [nombre] [comando]` amplía capacidades en caliente.
- **Paralelizar = git work trees**, un espacio aislado por instancia. Comandos propios en `.claude/commands/*.md` con **`$ARGUMENTS`**.
- ⚠ **Claude no manipula directamente el ordenador.** Computer use = tool use + un entorno Docker que aportas tú.

### Agentes y workflows

- **Workflow** = pasos conocidos. **Agente** = pasos desconocidos.
- Patrones: **evaluador-optimizador**, **paralelización**, **encadenado**, **enrutado**.
- El encadenado sirve sobre todo cuando **Claude ignora restricciones** en prompts largos: acepta la salida imperfecta y pide una reescritura señalando las violaciones.
- **Da herramientas abstractas** (`bash`, `web_fetch`, `file_write`), no especializadas (`refactor_tool`).
- **Inspección del entorno** = feedback más allá del retorno de la herramienta: captura tras cada acción, leer el fichero antes de editarlo.
- **Workflows: más fáciles de probar, mayor tasa de éxito. Agentes: impredecibles, menor tasa de éxito.**

> **Prioriza workflows. Los usuarios quieren productos que funcionen al 100%, no agentes vistosos. Resuelve de forma fiable primero; innova después.**
