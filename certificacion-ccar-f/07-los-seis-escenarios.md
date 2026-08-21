# 7 · Los seis escenarios

El examen es **basado en escenarios**. Cada escenario presenta un contexto de producción realista que enmarca un conjunto de preguntas. En tu sesión te salen **4 escenarios elegidos al azar de estos 6**.

Los seis están publicados literalmente en la guía oficial. Saberlos de memoria es media batalla: cuando reconoces el escenario, sabes qué dominios van a preguntarte.

---

## Escenario 1 · Customer Support Resolution Agent

> Estás construyendo un agente de resolución de atención al cliente con el Claude Agent SDK. El agente maneja peticiones de alta ambigüedad como devoluciones, disputas de facturación y problemas de cuenta. Tiene acceso a tus sistemas de backend a través de tools MCP a medida (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Tu objetivo es **80 %+ de resolución en el primer contacto**, sabiendo cuándo escalar.

**Dominios principales:** Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| El agente salta `get_customer` y llama a `lookup_order` con el nombre | **Prerrequisito programático**, no prompt |
| Confunde `get_customer` con `lookup_order` (descripciones mínimas) | **Ampliar las descripciones** con formatos, ejemplos, casos límite y fronteras |
| Escalado mal calibrado (55 % de resolución) | **Criterios explícitos + few-shot**, no confianza autoinformada ni sentimiento |
| Reembolsos por encima de 500 $ | **Hook** que intercepta y redirige a escalado |
| Formatos de fecha heterogéneos entre tools | **`PostToolUse`** que normaliza |
| Contexto largo perdiendo importes y fechas | Bloque **"case facts"** persistente |
| Traspaso a humano | **Handoff estructurado**: ID, causa raíz, importe, acción recomendada |

---

## Escenario 2 · Code Generation with Claude Code

> Estás usando Claude Code para acelerar el desarrollo. Tu equipo lo usa para generación de código, refactor, depuración y documentación. Necesitas integrarlo en el flujo de desarrollo con **slash commands** a medida, configuraciones de **`CLAUDE.md`**, y entender **cuándo usar plan mode frente a ejecución directa**.

**Dominios principales:** Claude Code Configuration & Workflows · Context Management & Reliability

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| Comando `/review` disponible al clonar el repo | **`.claude/commands/`** en el proyecto |
| Monolito → microservicios, decenas de ficheros | **Plan mode desde el principio** |
| Convenciones por tipo de fichero disperso (tests) | **`.claude/rules/`** con globs en el frontmatter |
| Un compañero nuevo no recibe las instrucciones | Están en **nivel usuario**, deben ir a **nivel proyecto**. Verifica con **`/memory`** |
| Skill de análisis que llena la conversación | **`context: fork`** |
| Sesión larga que degrada | **scratchpad**, **`/compact`**, subagentes, `Explore` |

---

## Escenario 3 · Multi-Agent Research System

> Estás construyendo un sistema de investigación multiagente con el Claude Agent SDK. Un agente coordinador delega en subagentes especializados: uno busca en la web, otro analiza documentos, otro sintetiza hallazgos y otro genera informes. El sistema investiga temas y produce **informes exhaustivos y citados**.

**Dominios principales:** Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| Informe que cubre solo una parte del tema, subagentes correctos | **Descomposición del coordinador demasiado estrecha** |
| El subagente de búsqueda hace timeout | **Contexto de error estructurado** al coordinador |
| Síntesis que necesita verificar hechos constantemente | **`verify_fact` acotado** para el 85 % simple; lo complejo sigue por el coordinador |
| Se pierden las citas al sintetizar | **Mapeos claim–source estructurados** preservados aguas abajo |
| Dos fuentes creíbles con cifras distintas | **Anotar el conflicto con atribución**, no elegir |
| Latencia de subagentes secuenciales | **Varias llamadas a `Task` en una sola respuesta** |
| El subagente de síntesis no ve lo que encontró el de búsqueda | Hay que **pasárselo explícitamente en el prompt** |

---

## Escenario 4 · Developer Productivity with Claude

> Estás construyendo herramientas de productividad para desarrolladores con el Claude Agent SDK. El agente ayuda a los ingenieros a explorar codebases desconocidos, entender sistemas legacy, generar boilerplate y automatizar tareas repetitivas. Usa las tools integradas (`Read`, `Write`, `Bash`, `Grep`, `Glob`) e integra servidores MCP.

**Dominios principales:** Tool Design & MCP Integration · Claude Code Configuration & Workflows · Agentic Architecture & Orchestration

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| Buscar quién llama a una función | **`Grep`** (contenido) |
| Encontrar `**/*.test.tsx` | **`Glob`** (rutas) |
| `Edit` falla por texto no único | **`Read` + `Write`** como fallback |
| Entender un codebase enorme | **Incremental**: `Grep` para entradas, `Read` para seguir imports. No leerlo todo |
| MCP compartido del equipo con token | **`.mcp.json`** + `${VAR}` |
| MCP personal experimental | **`~/.claude.json`** |
| El agente prefiere `Grep` a una tool MCP mejor | **Mejorar la descripción de la tool MCP** |
| Integración estándar tipo Jira | **Servidor MCP de la comunidad**, no uno propio |
| Tarea abierta ("añade tests al legacy") | **Descomposición adaptativa**: mapear, priorizar, adaptar |

---

## Escenario 5 · Claude Code for Continuous Integration

> Estás integrando Claude Code en tu pipeline de CI/CD. El sistema ejecuta revisiones de código automatizadas, genera casos de test y da feedback en pull requests. Necesitas diseñar prompts que den **feedback accionable y minimicen falsos positivos**.

**Dominios principales:** Claude Code Configuration & Workflows · Prompt Engineering & Structured Output

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| El job se cuelga esperando entrada | **`-p`** / `--print` |
| Publicar hallazgos como comentarios inline | **`--output-format json`** + **`--json-schema`** |
| Falsos positivos que hunden la confianza | **Criterios categóricos explícitos**, no "sé conservador" |
| Formato de hallazgo inconsistente | **Few-shot** con ubicación, problema, severidad, arreglo |
| PR de 14 ficheros, revisión contradictoria | **Pasada por fichero + pasada de integración** |
| Revisar el código que él mismo generó | **Instancia independiente** |
| Comentarios duplicados al re-ejecutar | Incluir hallazgos previos e instruir "solo lo nuevo o no resuelto" |
| Tests generados de bajo valor | Documentar estándares y fixtures en **`CLAUDE.md`**; aportar los tests existentes |
| Pre-merge bloqueante frente a informe nocturno | **Síncrono** el primero, **batch** el segundo |

---

## Escenario 6 · Structured Data Extraction

> Estás construyendo un sistema de extracción de datos estructurados con Claude. El sistema extrae información de documentos no estructurados, valida la salida con JSON schemas y mantiene alta precisión. Debe manejar casos límite con elegancia e integrarse con sistemas de aguas abajo.

**Dominios principales:** Prompt Engineering & Structured Output · Context Management & Reliability

**Qué te van a preguntar aquí**

| Tema | Respuesta que espera el examen |
|---|---|
| Salida que a veces no es JSON válido | **`tool_use` con JSON schema** |
| Tipo de documento desconocido, varios esquemas | **`tool_choice: "any"`** |
| Forzar que la extracción de metadatos vaya primero | **`{"type":"tool","name":"extract_metadata"}`** |
| El modelo inventa valores ausentes | Campos **opcionales / nullable** |
| Categorías que no caben en el enum | **`"other"` + campo de detalle**; `"unclear"` para lo ambiguo |
| Las líneas no suman el total | **Validación semántica**: `calculated_total` junto a `stated_total` |
| El reintento no arregla el fallo | La información **no está en el documento** |
| 100 documentos, sin prisa | **Message Batches API**, fallos por `custom_id` |
| 97 % de precisión global | **Estratifica por tipo de documento y campo** |
| Priorizar revisores | **Confianza por campo calibrada** con conjunto etiquetado |

---

## Mapa escenario ↔ dominio

| Escenario | D1 | D2 | D3 | D4 | D5 |
|---|:-:|:-:|:-:|:-:|:-:|
| 1 · Customer Support | ● | ● | | | ● |
| 2 · Code Generation | | | ● | | ● |
| 3 · Multi-Agent Research | ● | ● | | | ● |
| 4 · Developer Productivity | ● | ● | ● | | |
| 5 · CI | | | ● | ● | |
| 6 · Structured Extraction | | | | ● | ● |

**Lectura:** el **dominio 5 aparece en cuatro de los seis** escenarios pese a pesar solo un 15 %. Y el **dominio 4 solo aparece en dos**: si te tocan los escenarios 1, 2, 3 y 4, apenas verás prompting. La suerte del sorteo importa.

---

**Anterior:** [6 · Dominio 5](06-dominio-5-contexto-y-fiabilidad.md) · **Siguiente:** [8 · Las 12 preguntas oficiales de muestra](08-preguntas-oficiales.md)
