# 09 — Repaso y autoevaluación

El curso tiene una **evaluación oficial de 10 preguntas** en la plataforma: *Assessment on MCP Concepts*. Hacerla registra un intento en tu cuenta, así que este capítulo es la **preparación**: la chuleta y un autotest construido desde el material.

Cuando la hagas, vuelve aquí y registra las preguntas reales con su feedback, como en `claude-code-in-action/10-quiz.md`.

---

## Chuleta

### El esquema mental de todo el curso

Las tres capacidades del primer bloque **son la misma cosa vista desde tres ángulos**: el servidor pidiéndole algo al cliente.

| Capacidad | El servidor pide… | Método |
|---|---|---|
| **Sampling** | que genere texto con su LLM | `ctx.session.create_message()` |
| **Log / progreso** | que muestre un mensaje o el avance | `ctx.info()` · `ctx.report_progress()` |
| **Roots** | la lista de rutas permitidas | `ctx.session.list_roots()` |

Y el segundo bloque es qué pasa con esa dirección según el transporte.

### Sampling

- Traslada el acceso al LLM **del servidor al cliente**: sin claves de API, sin autenticación, sin coste de tokens en el servidor.
- Flujo: servidor crea la petición → cliente la recibe en su **sampling callback** → cliente llama al LLM → cliente devuelve el texto.
- Servidor: **`create_message()`**. Cliente: **sampling callback** que devuelve un **`CreateMessageResult`**.
- El callback se pasa a **`ClientSession`**.
- Los mensajes vienen **en formato MCP**, no en el de tu SDK: hay que **convertirlos**.
- Caso de uso principal: **servidores públicos** que necesitan un LLM sin tener acceso a uno.

### Notificaciones de log y progreso

- Es **opcional**, puramente **UX**: evita que el usuario crea que la llamada se ha colgado.
- Servidor: la función de herramienta recibe **`Context` como último argumento, automáticamente**. Métodos **`info()`, `warning()`, `debug()`, `error()`** y **`report_progress()`**.
- Cliente: **dos callbacks separados** y en **dos sitios distintos**:

| Callback | Se pasa a |
|---|---|
| logging | **`ClientSession`** |
| progreso | **`call_tool()`** |

### Roots

- **Root** = fichero o carpeta que el usuario autoriza **por adelantado**, normalmente por argumentos de línea de comandos al arrancar.
- La URI **debe empezar por `file://`**.
- El cliente **no manda los roots de entrada**: registra un **callback** (`list_roots_callback`) que responde cuando el servidor los pide.
- El servidor los pide con **`ctx.session.list_roots()`**.
- Tres herramientas del ejemplo: **ConvertVideo**, **ReadDirectory**, **ListRoots**.
- Dos beneficios: **control de permisos** y **descubrimiento autónomo** (Claude encuentra el fichero sin que le des la ruta).
- ⚠ **El SDK no impone las restricciones.** Tienes que implementar tú `is_path_allowed()` y llamarla en **todas** tus herramientas.
- **ListRoots es opcional**: alternativamente puedes meter la lista en el prompt.

### Tipos de mensaje JSON

- Dos categorías: **pares request/result** (siempre juntos) y **notifications** (sin respuesta).
- Formato **JSON-RPC** con `method`, `params`, `ID`.
- Esquema en **`schema.ts`** del repo de la especificación — **no es código ejecutable**, solo tipos.
- Clave: **los servidores pueden mandar mensajes al cliente**, y esa capacidad es la limitación crítica en StreamableHTTP.

### STDIO

- El cliente **lanza el servidor como proceso aparte** y hablan por **stdin/stdout**.
- **Bidireccional**: cualquiera de los dos puede iniciar una petición en cualquier momento.
- **Solo funciona en la misma máquina física.**
- Inicialización: **initialize request → initialize result → initialize notification** (esta última sin respuesta).

### StreamableHTTP

- Permite **alojamiento remoto**, servidores públicos en una URL.
- Limitación: **HTTP es unidireccional**. El servidor **no conoce la dirección del cliente** y el cliente **puede no ser accesible públicamente**.
- Afecta a: **sampling, listado de roots, notificaciones de progreso y de logging**.
- Apaño: **SSE**, manteniendo conexiones abiertas.
- **Session ID** aleatorio asignado en la inicialización, viaja como **cabecera HTTP**.
- **Dos conexiones SSE**:

| Conexión | Para |
|---|---|
| **larga** | peticiones iniciadas por el servidor · **notificaciones de progreso** |
| **corta** | respuesta a una llamada concreta · **logging + resultado de la herramienta** · se cierra sola |

### Los dos flags

| | `stateless_http = true` | `json_response = true` |
|---|---|---|
| Para qué | **escalado horizontal** con balanceador | desactivar el streaming en el POST |
| Session IDs | **no se asignan** | siguen |
| Inicialización | **se salta** | sigue |
| GET SSE | **desactivada** | sigue |
| Rompe | sampling, progreso, logging, suscripciones a recursos | progreso y logging |
| Extra | reduce el tráfico del servidor | el cliente espera al resultado completo |

> **Usa en desarrollo el mismo transporte que en producción.**

---

## Autotest — 12 preguntas

Tapa las respuestas.

1. ¿Qué tres problemas del servidor resuelve el sampling?
2. ¿Quién llama realmente al LLM en una operación de sampling?
3. Implementas un sampling callback y el servidor se queda colgado. ¿Qué se te ha olvidado?
4. ¿Por qué hay que escribir lógica de conversión de mensajes en el cliente?
5. ¿Cómo llega el objeto `Context` a tu función de herramienta?
6. El callback de logging y el de progreso se pasan a sitios distintos. ¿Cuáles?
7. ¿Con qué debe empezar la URI de un root, y quién decide la lista?
8. El servidor lee un fichero fuera de los roots concedidos. ¿Falla? ¿Por qué?
9. ¿Qué método usa el servidor para obtener los roots, y qué provoca en el cliente?
10. ¿Cuál es la ventaja de STDIO que HTTP no tiene, y cuál es su límite?
11. En StreamableHTTP hay dos conexiones SSE. ¿Qué viaja por cada una?
12. Pones `stateless_http = true` para escalar. ¿Qué cuatro cosas pierdes?

<details>
<summary>Respuestas</summary>

1. Manejar **claves de API**, manejar **autenticación** y pagar los **costes de tokens**. Sampling traslada esa responsabilidad al cliente.
2. **El cliente.** El servidor solo crea la petición; el cliente la recibe en su sampling callback, llama al LLM y devuelve el texto.
3. Pasar el callback a **`ClientSession`**. Sin eso, el servidor pide sampling y no hay nadie escuchando.
4. Porque los mensajes vienen **formateados para comunicación en MCP** y **no hay garantía de que sean compatibles** con el SDK de LLM que uses.
5. **Automáticamente, como último argumento** de la función de herramienta. No hay que registrarlo.
6. **Logging → `ClientSession`.** **Progreso → `call_tool()`.** El logging es de la sesión entera; el progreso, de una llamada concreta.
7. Por **`file://`**. La lista la decide **el usuario**, típicamente por argumentos de línea de comandos al arrancar el servidor.
8. **No falla por sí solo.** El **SDK de MCP no impone las restricciones de root**: si tú no implementas y llamas a algo como `is_path_allowed()`, la lectura sale adelante.
9. **`ctx.session.list_roots()`**. Manda un mensaje **de vuelta al cliente**, que ejecuta su callback de listado de roots.
10. Ventaja: **comunicación bidireccional** — cualquiera de los dos puede iniciar una petición en cualquier momento. Límite: **solo funciona si cliente y servidor están en la misma máquina física**.
11. **Larga:** peticiones iniciadas por el servidor (sampling) y **notificaciones de progreso**. **Corta:** **mensajes de logging y el resultado de la herramienta**, atada a esa petición y cerrada automáticamente después.
12. **Sampling**, **logging de progreso**, **suscripciones a recursos** y, en general, cualquier **petición del servidor al cliente** — porque se desactiva la vía GET SSE y no se asignan session IDs. Como extras: no hace falta inicialización y baja el tráfico.

</details>
