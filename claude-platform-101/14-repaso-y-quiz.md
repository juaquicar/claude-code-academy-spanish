# 14 — Repaso y quiz

*15 minutos*

El curso **sí trae quiz oficial**: `Claude Platform 101 Quiz`, **8 preguntas** en la plataforma. De esas 8, solo **5 son de opción múltiple evaluables**; las otras 3 son encuesta de satisfacción, NPS y texto libre. El aprobado se calcula sobre las evaluables (aquí: **6 de 6, 100 %**).

---

## Parte 1 · Las preguntas oficiales

Reproducidas literalmente, con **la respuesta correcta marcada** y los distractores tal cual. La plataforma no da explicación textual por pregunta, así que el «por qué» de abajo sale del material del curso.

### 1. Which three parameters does the `messages.create` call itself require?

- A model, a system prompt, and an API key
- ✅ **A model, a max tokens limit, and a list of messages**
- A system prompt, a temperature, and a list of messages
- An API key, a workspace, and a max tokens limit

**Por qué.** Los tres que pide la llamada son **model**, **max tokens** y **messages**. El **system prompt es opcional** (moldea la persona) y **la API key no es un parámetro de la llamada**: vive en el cliente y en tu `.env.local`. → [capítulo 02](02-tu-primera-llamada-a-la-api.md)

### 2. When Claude decides to use a tool, who actually executes it?

- Claude runs it inside the model during the response
- Anthropic runs it on their servers automatically
- ✅ **Your code runs it and sends the result back**
- The SDK blocks the request until a human approves it

**Por qué.** Claude **pide** la llamada; **tu código ejecuta** la función y devuelve el `tool_result`. La única excepción son las **server tools** (web search, code execution, web fetch), que **sí** ejecuta Anthropic — y por eso ésas **no necesitan bucle de agente**. → [capítulo 05](05-que-es-el-uso-de-tools.md) y [07](07-tools-integradas.md)

### 3. Why does context management matter for long-running agents?

- Claude refuses requests that use more than half the window
- Old messages are deleted automatically after ten turns
- ✅ **The window is finite and you pay for what's in it — so the goal is fitting the right things in**
- Bigger contexts always improve quality, so you want them full

**Por qué.** El contexto es la entrada de cada llamada: **lo pagas al entrar y al salir**, y **cuando la ventana se llena la petición falla**. El objetivo no es meterlo todo, es meter lo correcto. → [capítulo 10](10-gestion-del-contexto.md)

### 4. Which jobs are the best fit for a managed agent?

- Single questions that need one fast answer
- ✅ **Long-running, sandboxed, or background work**
- High-volume classification at the lowest cost
- Anything where you need to inspect every tool call yourself

**Por qué.** Se recurre a ellos cuando el bucle **correría demasiado tiempo, haría demasiadas cosas o necesitaría sobrevivir a un percance**. Una pregunta rápida es una llamada normal; el volumen barato es Haiku; y **si quieres control total sobre cada llamada, escribes el bucle tú**. → [capítulo 12](12-construir-tu-primer-agente-gestionado.md)

### 5. In Claude Code, which slash command invokes the built-in skill for working with the Claude API?

- `/anthropic-api`
- `/claude-sdk`
- ✅ **`/claude-api`**
- `/api-tools`

**Por qué.** Además se **carga sola** cuando Claude Code detecta el SDK de TypeScript. Si no aparece: `/plugin marketplace add AnthropicsSkills` — **con `s` al final de Anthropics**. → [capítulo 13](13-construir-con-claude-code.md)

### 6–8. No evaluables

Encuesta de satisfacción (escala de 5), NPS (escala de 5) y un campo de texto libre, que **es obligatorio** para poder enviar el quiz.

---

## Parte 2 · Banco extra

El oficial toca 5 conceptos. Estas van a por el resto.

**1.** ¿Cuáles son las tres capas de la plataforma y cuál es el lema?
<details><summary>Respuesta</summary>

**Primitives** (Messages API, tool use, files, web search, code execution, MCP, skills), **infrastructure** (managed agents, reintentos, colas, observabilidad) y **controls** (dashboards, evals). El lema: **build with primitives, scale on infrastructure, run with control.** → cap. 01
</details>

**2.** ¿Por qué `response.content` es un array y no una cadena?
<details><summary>Respuesta</summary>

Porque Claude puede devolver **varios bloques** — `text`, llamadas a tools, thinking. Siempre **iteras y compruebas el `type`**. → cap. 02
</details>

**3.** ¿Dónde va la API key y por qué?
<details><summary>Respuesta</summary>

En un fichero **`.env.local`**, fuera del control de versiones. Hardcodearla en el código es cómo acaban filtradas en GitHub. → cap. 02
</details>

**4.** ¿Cuántos ejemplos recomienda el curso para una evaluación inicial, y en qué orden se prueban los modelos?
<details><summary>Respuesta</summary>

**20 o 30 ejemplos representativos de tu carga real.** Se prueba **de Haiku hacia arriba** y te paras en **el modelo más barato cuya salida publicarías de verdad**. → cap. 03
</details>

**5.** ¿Qué campo te dice sobre qué se calcula tu factura?
<details><summary>Respuesta</summary>

**`response.usage`**: tokens de entrada y salida. → cap. 03
</details>

**6.** ¿Qué tier está **por encima** de Opus y qué advertencia lleva?
<details><summary>Respuesta</summary>

**Claude Fable**, con **coste significativamente mayor** que Opus: resérvalo para trabajo donde la capacidad extra compense. En el momento de grabar el curso **no estaba disponible de forma general**. → cap. 03
</details>

**7.** ¿Cuál es la condición de parada del bucle de agente?
<details><summary>Respuesta</summary>

Que el **stop reason sea `end_turn`**. Con **`tool_use`** ejecutas las tools y sigues iterando. → cap. 04
</details>

**8.** «Tú eres dueño de X. Claude es dueño de Y.» Completa.
<details><summary>Respuesta</summary>

**Tú eres dueño del bucle y de las tools. Claude es dueño del razonamiento.** → cap. 04
</details>

**9.** ¿Cuáles son las tres partes de una definición de tool?
<details><summary>Respuesta</summary>

**`name`**, **`description`** e **`input_schema`**. Van en el array `tools` de la petición. → cap. 05
</details>

**10.** ¿Cuál es la causa número uno de que los agentes fallen con las tools?
<details><summary>Respuesta</summary>

**Descripciones vagas.** La `description` es lo que Claude lee para decidir si llamar a la tool. → cap. 05
</details>

**11.** ¿Qué te ahorra el tool runner y en qué lenguajes está?
<details><summary>Respuesta</summary>

Te ahorra **el bucle `while`, el switch de stop reason, devolver resultados a mano y escribir JSON schemas** — los construye a partir de tus funciones reales. Está en el SDK para **TypeScript, Python y Ruby**. `runner.untilDone()` devuelve el mensaje final. → cap. 05
</details>

**12.** ¿Dónde va exactamente el parámetro `effort` y cuáles son sus niveles?
<details><summary>Respuesta</summary>

**Dentro de `output_config`**, no junto al bloque `thinking`. Niveles: **`low`, `medium`, `high` (por defecto), `xhigh`, `max`**. → cap. 06
</details>

**13.** ¿Cuándo **no** conviene activar el extended thinking?
<details><summary>Respuesta</summary>

En **clasificación simple, extracción y boilerplate**: ahí solo añade **latencia y coste** sin mejorar el resultado. → cap. 06
</details>

**14.** ¿Qué tres server tools nombra el curso, y qué necesitan que las tools normales sí necesitan?
<details><summary>Respuesta</summary>

**Web search, code execution y web fetch.** **No necesitan bucle de agente**: Anthropic las ejecuta y el resultado viene en la misma respuesta, en bloques **`server_tool_use`** y de resultado. → cap. 07
</details>

**15.** ¿Qué dos client tools nombra el curso?
<details><summary>Respuesta</summary>

**Memory** (leer y escribir memoria entre sesiones) y **Bash** (un shell persistente). Corren donde corre tu código, pero **el SDK trae el schema y un runner**. → cap. 07
</details>

**16.** Tools, skills y MCP: ¿la regla de tres?
<details><summary>Respuesta</summary>

**Las tools son para tus cosas, las skills para tus procesos, y MCP para las cosas de todos los demás.** → cap. 09
</details>

**17.** ¿Cómo se adjunta una skill a una petición y qué implica que sea una lista?
<details><summary>Respuesta</summary>

Con **`container.skills`**, cada entrada con `skill_id` y `version`. Al ser **lista**, puedes **apilar varias skills** en una misma llamada. Se suben antes con `client.beta.skills.create`. → cap. 08
</details>

**18.** ¿Cómo dejas un servidor MCP en solo lectura?
<details><summary>Respuesta</summary>

Con **`default_config: {"enabled": False}`** y activando tools concretas en **`configs`** — por ejemplo `search_messages` y `list_channels` de Slack, dejando fuera publicar y borrar. → cap. 09
</details>

**19.** ¿Qué dos claves hacen falta para conectar un servidor MCP y qué **no** hace falta escribir?
<details><summary>Respuesta</summary>

**`mcp_servers`** (tipo, URL, nombre, token opcional) y una tool de tipo **`mcp_toolset`**. **No escribes ni un schema**: Claude **introspecciona** el servidor. → cap. 09
</details>

**20.** De los cuatro patrones de contexto, ¿cuál **no** es una funcionalidad de la API?
<details><summary>Respuesta</summary>

**Just-in-time context** — es un **patrón de diseño**: una decisión deliberada sobre qué cargas y cuándo. Los otros tres (compactación en servidor, prompt caching, memory tool) sí son de primera clase. → cap. 10
</details>

**21.** ¿Qué modo de fallo ataca cada patrón de contexto?
<details><summary>Respuesta</summary>

**Coste**, **tamaño de ventana** y **ausencia de estado**. Elige los que encajen con lo que se te rompe. → cap. 10
</details>

**22.** ¿Quién implementa el almacenamiento de la memory tool y qué inyecta Anthropic?
<details><summary>Respuesta</summary>

**El backend lo implementas tú** en el cliente (ficheros, base de datos, almacén cifrado). Anthropic **auto-inyecta una instrucción de sistema** para que Claude **consulte el directorio de memoria antes de empezar**. → cap. 10
</details>

**23.** ¿Cuáles son los cuatro primitivos de los managed agents, en orden?
<details><summary>Respuesta</summary>

**Agent** (persona reutilizable) → **Environment** (dónde corre) → **Session** (una ejecución; la unidad de trabajo) → **Events** (todo lo que entra y sale). → cap. 12
</details>

**24.** ¿Por qué hay que abrir el event stream antes de enviar el mensaje inicial?
<details><summary>Respuesta</summary>

Porque el stream **solo entrega eventos que ocurren después de abrirse**. Si envías primero, te pierdes el arranque. → cap. 12
</details>

**25.** ¿Qué tres eventos vigila la demo del contador de líneas?
<details><summary>Respuesta</summary>

**`agent.message`** (texto), **`agent.tool_use`** (qué tool eligió) y **`session.status_idle`** (terminado). → cap. 12
</details>

**26.** ¿Qué son las rúbricas y los graders?
<details><summary>Respuesta</summary>

La **rúbrica** define qué significa "hecho" (por ejemplo: Lighthouse > 90, sin recursos que bloqueen el render, imágenes con lazy load). El **grader** es un evaluador **separado, en su propia ventana de contexto**, que puntúa la salida contra esos criterios; **Claude lee el feedback y vuelve a iterar**. → cap. 11
</details>

**27.** En el ejemplo de respuesta a incidentes, ¿qué impide que el resumen salga a Slack sin supervisión?
<details><summary>Respuesta</summary>

La **política de permisos**: ves el borrador, lo apruebas y entonces sale. **Las acciones sensibles esperan a un humano.** → cap. 11
</details>

**28.** ¿Qué tres cosas debe nombrar un buen prompt para Claude Code?
<details><summary>Respuesta</summary>

**El fichero**, **el patrón** y **el estado final** esperado. → cap. 13
</details>
