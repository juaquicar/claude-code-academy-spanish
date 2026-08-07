# 09 — MCP (Model Context Protocol)

**MCP** = capa de comunicación que aporta a Claude **contexto y herramientas** sin obligar al desarrollador a escribir código tedioso.

**Arquitectura:** un **cliente MCP** se conecta a un **servidor MCP**. El servidor contiene **tools, resources y prompts** como componentes internos.

## El problema que resuelve

Elimina la carga de escribir y mantener montones de esquemas y funciones de herramienta para integrar servicios.

> **Ejemplo:** un chatbot de GitHub exigiría implementar herramientas para repositorios, pull requests, issues y proyectos. Mucho trabajo de desarrollador.

**La solución:** el servidor MCP se encarga de **definir y ejecutar** las herramientas, en vez de tu servidor de aplicación. Los servidores MCP son **interfaces a servicios externos**, que envuelven su funcionalidad en herramientas listas para usar.

### Preguntas frecuentes del curso

| Pregunta | Respuesta |
|---|---|
| ¿Quién crea los servidores MCP? | **Cualquiera.** A menudo los propios proveedores hacen implementaciones oficiales (AWS, etc.) |
| ¿En qué se diferencia de llamar al API directamente? | MCP **te ahorra escribir tú los esquemas y las funciones** |
| ¿Y de tool use? | **Son complementarios.** MCP decide **quién hace el trabajo** (servidor vs. desarrollador); en ambos casos sigue habiendo herramientas |

> **El valor central: traslada la carga de integración del desarrollador de la aplicación al mantenedor del servidor MCP.**

## Clientes MCP

**Cliente MCP** = interfaz de comunicación entre tu servidor y el servidor MCP; te da acceso a sus herramientas.

- **Agnóstico del transporte** — pueden comunicarse por stdio, HTTP o WebSockets.
- **Montaje habitual:** cliente y servidor en la misma máquina, por entrada/salida estándar.

**Tipos de mensaje clave:**

| Mensaje | Qué es |
|---|---|
| `list tools request` | El cliente pide al servidor las herramientas disponibles |
| `list tools result` | El servidor responde con la lista |
| `call tool request` | El cliente pide ejecutar una herramienta con argumentos |
| `call tool result` | El servidor devuelve el resultado |

### El flujo completo, de 10 pasos

1. El usuario consulta a tu servidor.
2. Tu servidor pide la lista de herramientas al cliente MCP.
3. El cliente MCP manda `list tools request` al servidor MCP.
4. El servidor MCP responde con `list tools result`.
5. Tu servidor envía la consulta + las herramientas a Claude.
6. Claude pide ejecutar una herramienta.
7. Tu servidor pide al cliente MCP que la ejecute.
8. El cliente MCP manda `call tool request` al servidor MCP.
9. El servidor MCP ejecuta la herramienta — p. ej. llama al API de GitHub.
10. Los resultados vuelven por la cadena: servidor MCP → cliente MCP → tu servidor → Claude → usuario.

## El proyecto del curso

Chatbot de línea de comandos que enseña la interacción cliente-servidor.

**Componentes:** un **cliente MCP** que conecta con un **servidor MCP** propio que expone **dos herramientas** (leer documento, actualizar documento), sobre una colección de documentos falsos guardados **solo en memoria**.

> **Aviso:** un proyecto normal implementa **el cliente O el servidor**, no ambos. Aquí se hacen los dos por motivos didácticos.

**Montaje:** descargar `CLI_project.zip` → abrir en el editor → seguir el `readme.md` → añadir la clave de API al `.env` → instalar dependencias → `uv run main.py` o `python main.py`.

## Definir tools con MCP

El SDK de Python de MCP **auto-genera los JSON Schema a partir de las definiciones de función** de Python, mediante el decorador `@mcp.tool`.

**Sintaxis:** `@mcp.tool(name="...", description="...")` sobre una función con parámetros tipados, usando **`Field()`** para describir cada argumento.

Las dos herramientas del proyecto:

1. **`read_doc_contents`** — recibe un `doc_id`, devuelve el contenido del diccionario de documentos en memoria.
2. **`edit_document`** — recibe `doc_id`, `old_string` y `new_string`, hace buscar/reemplazar sobre el contenido.

**Manejo de errores:** comprobar si el `doc_id` existe en el diccionario y lanzar `ValueError` si no.

> **La ventaja:** el SDK **elimina la escritura manual de JSON Schema**, generándolo a partir de la firma de la función y los decoradores. Compara esto con el capítulo 4.

**Imports necesarios:** `Field` de pydantic para las descripciones de parámetros, y el paquete `mcp` para el servidor y los decoradores.

## El inspector del servidor

**MCP Inspector** = depurador **en el navegador** para probar servidores MCP **sin conectarlos a una aplicación**.

**Acceso:** ejecuta `mcp dev [fichero_servidor.py]` en el terminal → abre el servidor en un puerto → navega a la URL indicada.

**Interfaz:** botón *connect* en la barra lateral izquierda → menú superior con las secciones de resources, prompts y tools → la sección de tools lista las disponibles → al hacer clic se abre el panel derecho para probarla a mano.

**Flujo de prueba:** conectar → ir a tools → seleccionar herramienta → introducir parámetros → *run tool* → verificar la salida.

**Qué aporta:** pruebas en vivo durante el desarrollo, invocación manual, formularios de parámetros, feedback de éxito/fallo, **sin necesidad de integrar la aplicación completa**.

> La interfaz cambia con frecuencia durante el desarrollo, pero la funcionalidad base se mantiene.

## Implementar un cliente

**MCP Client** = clase envoltorio alrededor de la **client session**, para gestionar la limpieza de recursos y la conexión.

**Client Session** = la conexión real al servidor MCP, del SDK de Python. **Requiere limpieza de recursos al cerrar.**

**Para qué sirve el cliente:** exponer la funcionalidad del servidor MCP al resto de tu código, para pedir listas de herramientas y ejecutarlas.

```python
async def list_tools(self):
    result = await self.session.list_tools()
    return result.tools

async def call_tool(self, tool_name, tool_input):
    return await self.session.call_tool(tool_name, tool_input)
```

**Flujo de uso:** el cliente obtiene las definiciones para enviárselas a Claude, y después ejecuta las herramientas cuando Claude las pide.

> **Patrón habitual:** envolver la client session en una clase mayor para gestionar recursos, en vez de usar la sesión directamente.

## Definir resources

**MCP Resources** = mecanismo por el que los servidores MCP **exponen datos a los clientes para operaciones de lectura**.

**Dos tipos:**

| Tipo | URI |
|---|---|
| **Directo** | Estático — `docs://documents` |
| **Plantilla** | Parametrizado — `docs://documents/{doc_id}` |

**URI** = dirección o identificador para acceder a un recurso concreto; se define al crearlo.

**Flujo:** el cliente envía una petición de lectura con la URI → el servidor la empareja con una función → la ejecuta → devuelve los datos en el resultado.

**Implementación:** decorador **`@mcp.resource`** con los parámetros de URI y **MIME type**.

**MIME types** = pista para el cliente sobre el formato devuelto: `application/json` para datos estructurados, `text/plain` para texto plano.

**Recursos con plantilla:** el SDK **parsea automáticamente** los parámetros de la URI y los pasa como argumentos con nombre a la función.

> ### Resources vs. tools
>
> **Los resources aportan datos de forma proactiva** — por ejemplo, traer el contenido de un documento cuando se menciona con @.
>
> **Las tools ejecutan acciones de forma reactiva** — cuando Claude decide llamarlas.

**Serialización:** el SDK convierte automáticamente los datos devueltos a cadenas; **el cliente es responsable de deserializar**.

## Acceder a resources desde el cliente

**Pasos:**

1. Importa `json` y `AnyURL` de pydantic.
2. Llama a `await self.session.read_resource(AnyURL(uri))`.
3. Extrae el primer elemento de `result.contents[0]`.
4. Comprueba `resource.mime_type` para decidir cómo parsear.

**Lógica de parseo:**

- Si `mime_type == "application/json"` → `json.loads(resource.text)`
- Si no → devolver `resource.text` tal cual

**Resultado final:** el contenido de los documentos se incluye automáticamente en los prompts de Claude **sin necesidad de llamadas a herramienta**.

## Definir prompts

**MCP Prompts** = **plantillas de prompt predefinidas y probadas** que los servidores MCP exponen a las aplicaciones cliente.

**Para qué:** en vez de que los usuarios escriban prompts improvisados, **los autores del servidor crean prompts de alta calidad, ya evaluados**, adaptados al dominio de su servidor.

**Implementación:** decorador `@mcpserver.prompt` con nombre y descripción, sobre una función que **devuelve una lista de mensajes** (de usuario o asistente) lista para enviar a Claude.

**Ejemplo:** un prompt de formateo de documentos que recibe un ID, instruye a Claude a leer el documento con las herramientas, reformatearlo a markdown y guardar los cambios.

**Beneficios:** experiencia específica del servidor, calidad ya probada, reutilizable entre aplicaciones cliente, y **mejores resultados que los prompts que escribiría el usuario**.

**Estructura:** devuelve objetos `base.UserMessage` con el texto del prompt y los parámetros interpolados.

**Integración en el cliente:** los prompts aparecen como **opciones de autocompletado (slash commands)**, piden al usuario los parámetros necesarios y ejecutan el flujo predefinido.

## Prompts en el cliente

```python
async def list_prompts(self):
    result = await self.session.list_prompts()
    return result.prompts

async def get_prompt(self, prompt_name, arguments):
    result = await self.session.get_prompt(prompt_name, arguments)
    return result.messages
```

**El flujo:**

1. Defines el prompt en el servidor MCP con los argumentos que espera (p. ej. `document_id`).
2. El cliente llama a `get_prompt` con el nombre + un diccionario de argumentos.
3. Los argumentos se pasan como argumentos con nombre a la función del prompt.
4. La función los interpola en el texto.
5. Devuelve el array de mensajes, listo para el LLM.

> **La idea:** los prompts son **plantillas definidas por el servidor** que los clientes invocan con argumentos concretos para generar instrucciones contextualizadas. Los argumentos fluyen: llamada del cliente → función del prompt → texto interpolado → consumo por el LLM.
