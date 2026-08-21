# 3 · Dominio 2 — Tool Design & MCP Integration

**Peso: 18 %** · ~11 de los 60 ítems. Cinco task statements.

Escenarios que lo tocan: *Customer Support Resolution Agent*, *Multi-Agent Research System*, *Developer Productivity with Claude*.

---

## 2.1 · Diseñar interfaces de herramienta con descripciones y fronteras claras

### Conocimiento

- **La descripción de la tool es el mecanismo principal que usa el LLM para seleccionarla.** Descripciones mínimas → selección poco fiable entre herramientas parecidas.
- Hay que incluir en la descripción: **formatos de entrada, consultas de ejemplo, casos límite y explicación de fronteras**.
- Descripciones ambiguas o solapadas provocan **enrutado incorrecto** (`analyze_content` frente a `analyze_document` con descripciones casi idénticas).
- El **system prompt influye en la selección**: instrucciones sensibles a palabras clave pueden crear asociaciones no deseadas con ciertas tools.

### Habilidades

- Escribir descripciones que diferencian claramente **propósito, entradas esperadas, salidas y cuándo usarla frente a alternativas parecidas**.
- **Renombrar** herramientas y actualizar descripciones para eliminar solapamiento funcional (renombrar `analyze_content` a `extract_web_results` con una descripción específica de web).
- **Partir** tools genéricas en tools específicas con contratos de entrada/salida definidos (partir un `analyze_document` genérico en `extract_data_points`, `summarize_content` y `verify_claim_against_source`).
- Revisar el system prompt buscando **instrucciones sensibles a palabras clave** que puedan pisar descripciones bien escritas.

> **Trampa.** Ante mala selección de tool con descripciones mínimas, la respuesta correcta como **primer paso** es **mejorar las descripciones**, no añadir few-shot ni montar una capa de routing ni consolidar tools. Las tres son válidas en abstracto pero desproporcionadas o fuera de la causa raíz.

---

## 2.2 · Respuestas de error estructuradas para tools MCP

### Conocimiento

- El patrón del flag **`isError`** de MCP para comunicar fallos al agente.
- Los cuatro tipos: **transient** (timeouts, servicio caído), **validation** (entrada inválida), **business** (violación de política) y **permission**.
- Por qué las respuestas uniformes (`"Operation failed"` genérico) **impiden al agente decidir cómo recuperarse**.
- La diferencia entre errores **reintentables y no reintentables**, y cómo devolver metadatos estructurados **evita reintentos desperdiciados**.

### Habilidades

- Devolver metadatos con **`errorCategory`** (`transient`/`validation`/`permission`), **`isRetryable`** booleano y descripción legible.
- Incluir **`retriable: false`** y explicaciones aptas para el cliente en violaciones de regla de negocio, para que el agente sepa comunicarlo.
- Recuperación **local dentro del subagente** para fallos transitorios; propagar al coordinador **solo lo que no se puede resolver localmente**, junto con resultados parciales y qué se intentó.
- Distinguir **fallo de acceso** (necesita decisión de reintento) de **resultado vacío válido** (consulta correcta sin coincidencias).

---

## 2.3 · Repartir herramientas entre agentes y configurar `tool_choice`

### Conocimiento

- Dar demasiadas tools a un agente —**18 en vez de 4-5**— **degrada la fiabilidad de selección** al aumentar la complejidad de decisión.
- Los agentes con herramientas **fuera de su especialización tienden a usarlas mal** (un agente de síntesis intentando búsquedas web).
- **Acceso con alcance:** solo las tools que su rol necesita, con tools cruzadas limitadas para necesidades concretas de alta frecuencia.
- Opciones de **`tool_choice`**: `"auto"`, `"any"` y selección forzada `{"type": "tool", "name": "..."}`.

### Habilidades

- Restringir el set de cada subagente a lo relevante para su rol, evitando el mal uso cruzado.
- Sustituir tools genéricas por alternativas restringidas (cambiar `fetch_url` por `load_document`, que valida URLs de documento).
- Dar **tools cruzadas con alcance** para necesidades de alta frecuencia (un `verify_fact` para el agente de síntesis) y **enrutar los casos complejos por el coordinador**.
- Usar selección forzada para garantizar que una tool concreta se llama primero (forzar `extract_metadata` antes de las tools de enriquecimiento) y procesar los pasos siguientes en turnos posteriores.
- Poner **`tool_choice: "any"`** para garantizar que el modelo llama a *alguna* tool en vez de devolver texto conversacional.

| Valor de `tool_choice` | Qué garantiza |
|---|---|
| `"auto"` | El modelo **puede** devolver texto en vez de llamar a una tool |
| `"any"` | **Debe** llamar a una tool, pero elige cuál |
| `{"type":"tool","name":"..."}` | Debe llamar **a esa tool concreta** |

> **Trampa.** El principio es **mínimo privilegio**: al agente de síntesis se le da un `verify_fact` acotado para el 85 % de casos simples, **no** acceso completo a las tools de búsqueda web. Sobreaprovisionar viola la separación de responsabilidades.

---

## 2.4 · Integrar servidores MCP en Claude Code y en workflows de agente

### Conocimiento

- **Alcance de servidor MCP:** `.mcp.json` a nivel de proyecto para tooling compartido del equipo; `~/.claude.json` a nivel de usuario para servidores personales o experimentales.
- **Expansión de variables de entorno** en `.mcp.json` (por ejemplo `${GITHUB_TOKEN}`) para gestionar credenciales **sin commitear secretos**.
- Las tools de **todos** los servidores MCP configurados se descubren al conectar y quedan **disponibles simultáneamente** para el agente.
- **MCP resources** como mecanismo para exponer **catálogos de contenido** (resúmenes de issues, jerarquías de documentación, esquemas de base de datos) y **reducir llamadas exploratorias**.

### Habilidades

- Configurar servidores compartidos en `.mcp.json` con expansión de variables para los tokens de autenticación.
- Configurar servidores personales/experimentales en `~/.claude.json`.
- **Mejorar las descripciones de las tools MCP** explicando capacidades y salidas en detalle, para **evitar que el agente prefiera tools integradas** (como `Grep`) sobre tools MCP más capaces.
- Elegir **servidores MCP de la comunidad** frente a implementaciones propias para integraciones estándar (Jira), reservando los servidores a medida para flujos específicos del equipo.
- Exponer catálogos de contenido como **resources** para dar visibilidad de los datos disponibles sin llamadas exploratorias.

---

## 2.5 · Elegir y aplicar las tools integradas

`Read` · `Write` · `Edit` · `Bash` · `Grep` · `Glob`

| Tool | Para qué |
|---|---|
| **`Grep`** | Buscar **contenido**: nombres de función, mensajes de error, sentencias de import |
| **`Glob`** | Buscar **rutas** por patrón de nombre o extensión (`**/*.test.tsx`) |
| **`Read` / `Write`** | Operaciones de fichero completo |
| **`Edit`** | Modificación dirigida mediante **coincidencia de texto única** |

### Conocimiento y habilidades

- Cuando **`Edit` falla porque el texto no es único**, el fallback fiable es **`Read` + `Write`**.
- Construir entendimiento del codebase **de forma incremental**: empezar con `Grep` para encontrar puntos de entrada, luego `Read` para seguir imports y trazar flujos — **en vez de leer todos los ficheros de golpe**.
- Trazar el uso de una función a través de módulos wrapper: identificar primero todos los nombres exportados y luego buscar cada nombre por el codebase.

---

## Conclusiones del dominio

- **La descripción es la interfaz.** Si el modelo elige mal, la primera hipótesis es la descripción.
- Errores MCP: **estructurados y categorizados**, con `isRetryable`. Genérico = el agente no puede recuperarse.
- **Menos tools por agente = mejor selección.** 4-5, no 18.
- `.mcp.json` = equipo · `~/.claude.json` = tú. Ambos activos a la vez.
- `Grep` contenido · `Glob` rutas · `Edit` falla ⇒ `Read` + `Write`.

---

**Anterior:** [2 · Dominio 1](02-dominio-1-arquitectura-agentica.md) · **Siguiente:** [4 · Dominio 3 — Claude Code](04-dominio-3-claude-code.md)
