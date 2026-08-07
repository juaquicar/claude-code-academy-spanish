# 08 — Repaso y evaluación

## La evaluación oficial — pendiente

El curso trae un **Final assessment on MCP** que se hace en la plataforma. Está **sin hacer a propósito**: lo harás tú al terminar de estudiar.

| Evaluación | Estado |
|---|---|
| **Final assessment on MCP** | ⬜ pendiente |

> **Cuando la hagas, pásame los resultados** y registro aquí las preguntas reales con su feedback y los distractores, como en `claude-code-in-action/10-quiz.md`.

---

## Chuleta

### Qué es MCP

- **Capa de comunicación** que aporta a Claude contexto y herramientas **sin escribir código tedioso**.
- Arquitectura: **cliente MCP → servidor MCP**, que contiene **tools, resources y prompts**.
- **Traslada la definición y ejecución de herramientas** del servidor del desarrollador a un servidor MCP dedicado.
- Un servidor MCP es una **interfaz a un servicio externo** que envuelve su funcionalidad en herramientas ya hechas.
- **Los escribe cualquiera**, pero a menudo los proveedores hacen implementaciones oficiales.
- **MCP y tool use son complementarios**, no lo mismo: MCP decide **quién hace el trabajo** de crear las herramientas.

### Clientes

- **Agnóstico del transporte**: stdin/stdout, HTTP, WebSockets. Lo habitual es **misma máquina por stdin/stdout**.
- Mensajes: **`list tools request/result`** y **`call tool request/result`**.
- ⚠ **El cliente no ejecuta las herramientas**: solo facilita la comunicación entre tu servidor y el servidor MCP, que sí las ejecuta.
- Se envuelve la **client session** en una clase mayor para gestionar la limpieza de recursos.
- Funciones clave: **`list_tools()`** y **`call_tool(nombre, entrada)`**.

### Tools

- Decorador **`@mcp.tool`** + función con parámetros tipados + **`Field()`** de pydantic para describirlos.
- **El SDK auto-genera el JSON Schema** desde la función decorada. Servidor en una línea.
- Patrón: **decorador → función → tipado → validación → lógica**.
- Valida la existencia antes de operar y **lanza `ValueError`** si falta.

### El inspector

- **`mcp dev fichero_servidor.py`** → depurador **en el navegador**, sin conectar ninguna aplicación.
- Interfaz: **Connect** en la izquierda → secciones **Resources / Prompts / Tools** arriba → panel derecho para probar.
- Flujo: selecciona herramienta → introduce parámetros → **Run Tool** → verifica salida.

### Resources

- **Exponen datos al cliente para operaciones de lectura.**
- Dos tipos: **directo/estático** (`docs://documents`) y **con plantilla** (`documents/{doc_id}`), cuyos parámetros **se convierten en argumentos con nombre**.
- Decorador **`@mcp.resource`** con **URI** y **MIME type**.
- **El SDK serializa a cadenas automáticamente**; el cliente deserializa según **`mime_type`**: `application/json` → `json.loads`, si no → texto plano.
- Se leen con **`read_resource(AnyUrl(uri))`**, y el dato está en **`result.contents[0]`**.
- **Un resource por cada operación de lectura distinta** — listar vs. traer uno.
- **Resultado clave:** el contenido llega al prompt **sin necesidad de herramientas** para leerlo durante el chat.

### Prompts

- **Instrucciones ya escritas y probadas** que el servidor expone; se invocan con **slash commands** (`/format`).
- Decorador **`@prompt`** con nombre y descripción; la función **devuelve una lista de mensajes**.
- Argumentos: **cliente → argumentos con nombre → interpolados en la plantilla → array de mensajes**.
- Funciones del cliente: **`list_prompts()`** y **`get_prompt(nombre, argumentos)`**.
- **Encapsulan la experiencia en prompt engineering del dominio** dentro del servidor.

### ⭐ Las tres primitivas, por quién las controla

| Primitiva | Control | Sirve a | Ejemplo en Claude |
|---|---|---|---|
| **Tools** | **El modelo** | Al modelo | Ejecución de código |
| **Resources** | **La aplicación** | A la app | Documentos de Google Drive |
| **Prompts** | **El usuario** | Al usuario | Botones de inicio de chat |

> **¿Capacidades para Claude? → tools. ¿Datos para tu app? → resources. ¿Flujos para el usuario? → prompts.**

---

## Autotest — 12 preguntas

Tapa las respuestas.

1. En una frase: ¿qué carga te quita MCP de encima?
2. ¿MCP sustituye al tool use?
3. ¿Ejecuta el cliente MCP las herramientas?
4. ¿Qué genera el SDK a partir de tu función decorada, y qué te ahorra?
5. ¿Cómo pruebas un servidor MCP sin tener aplicación?
6. Los dos tipos de resource y en qué se diferencian.
7. ¿Para qué sirve el MIME type de un resource?
8. ¿Qué deja de hacer falta cuando implementas resources bien?
9. ¿Quién escribe los prompts de un servidor MCP y por qué importa?
10. ¿Cómo llegan los argumentos desde el cliente hasta el texto del prompt?
11. Las tres primitivas, ordenadas por quién decide cuándo se usan.
12. Quieres que tu app muestre un desplegable con los documentos disponibles. ¿Qué primitiva?

<details>
<summary>Respuestas</summary>

1. **Escribir y mantener los esquemas y funciones de herramienta** de cada integración. Los escribe el mantenedor del servidor MCP.
2. **No: son complementarios.** En ambos casos hay herramientas; MCP decide **quién hace el trabajo de crearlas**.
3. **No.** Actúa de **intermediario**: facilita la comunicación entre tu servidor y el servidor MCP, que es quien las ejecuta.
4. **El JSON Schema**, a partir de la firma tipada y el decorador `@mcp.tool` con `Field()`. Te ahorra **escribirlo a mano**.
5. Con el **MCP Inspector**: `mcp dev fichero_servidor.py` abre un depurador **en el navegador** donde seleccionas la herramienta, metes parámetros y pulsas *Run Tool*.
6. **Directo/estático** con URI fija (`docs://documents`) y **con plantilla** con comodines (`documents/{doc_id}`), cuyos **parámetros de la URI se convierten en argumentos con nombre** de la función.
7. Es una **pista para el cliente** sobre el formato devuelto, para que sepa **cómo deserializarlo**: `application/json` → `json.loads`, si no → texto plano.
8. **Herramientas para leer el contenido de los documentos durante el chat.** El contenido del resource seleccionado **se incluye solo en el prompt**.
9. **Los autores del servidor**, no el usuario final. Importa porque son **prompts optimizados y ya probados** para ese dominio, en vez de dejar la calidad en manos de quien escriba.
10. **Argumentos del cliente → argumentos con nombre de la función del prompt → interpolados en la plantilla → array de mensajes** para el modelo.
11. **Tools** = las controla **el modelo**, sirven al modelo. **Resources** = los controla **la aplicación**, sirven a la app. **Prompts** = los controla **el usuario**, le sirven a él.
12. **Un resource.** Es tu **código de aplicación** el que decide cuándo traer esos datos para pintar la interfaz — exactamente el caso de la selección de documentos de Google Drive.

</details>
