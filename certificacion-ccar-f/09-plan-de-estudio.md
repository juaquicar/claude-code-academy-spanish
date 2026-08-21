# 9 · Plan de estudio

Tres partes: **qué recomienda Anthropic**, **qué cubre este repo** y **qué hueco te queda**.

---

## 9.1 · Lo que dice la guía oficial (sección 7)

Siete líneas de preparación, todas de manos en el teclado:

1. **Construye un agente con el Claude Agent SDK**: bucle agéntico completo con tool calling, manejo de errores y gestión de sesión. Practica lanzar subagentes y pasarles contexto.
2. **Configura Claude Code para un proyecto real**: `CLAUDE.md` con jerarquía, reglas por ruta en `.claude/rules/`, skills con opciones de frontmatter (`context: fork`, `allowed-tools`) y **al menos un servidor MCP** integrado.
3. **Diseña y prueba tools MCP**: descripciones que diferencian tools parecidas. Respuestas de error estructuradas con categoría y flags de reintento. Prueba la fiabilidad de selección **con peticiones ambiguas**.
4. **Construye un pipeline de extracción estructurada**: `tool_use` con JSON schemas, bucles de validación-reintento, esquemas con campos opcionales/nullable, y batch con la Message Batches API.
5. **Practica técnicas de prompting**: few-shot para escenarios ambiguos, criterios explícitos de revisión para reducir falsos positivos, arquitecturas de revisión multipasada.
6. **Estudia patrones de gestión de contexto**: extraer hechos estructurados de salidas verbosas, ficheros scratchpad para sesiones largas, delegación a subagentes para gestionar los límites.
7. **Repasa escalado y human-in-the-loop**: cuándo escalar (huecos de política, petición del cliente, incapacidad de progresar) frente a resolver de forma autónoma. Diseña flujos de revisión humana con enrutado por confianza.

## 9.2 · Los cuatro ejercicios oficiales (sección 8)

### Ejercicio 1 · Agente multi-tool con lógica de escalado
**Refuerza:** D1, D2, D5

- Define 3-4 tools MCP con descripciones detalladas. **Incluye a propósito dos tools de funcionalidad parecida** que exijan descripciones cuidadosas para no confundir la selección.
- Implementa un bucle agéntico que consulta `stop_reason` para decidir si seguir ejecutando tools o presentar la respuesta final. Maneja `"tool_use"` y `"end_turn"` correctamente.
- Añade respuestas de error estructuradas: `errorCategory` (transient/validation/permission), `isRetryable` booleano y descripción legible. Comprueba que el agente maneja cada tipo (reintentar transitorios, explicar los de negocio al usuario).
- Implementa un **hook programático** que intercepte llamadas para hacer cumplir una regla de negocio (bloquear operaciones por encima de un umbral), redirigiendo a escalado.
- Prueba con mensajes de varios asuntos y verifica que el agente **descompone, atiende cada asunto y sintetiza** una respuesta unificada.

### Ejercicio 2 · Configurar Claude Code para un equipo
**Refuerza:** D3, D2

- `CLAUDE.md` de proyecto con estándares universales. Verifica que lo de nivel proyecto se aplica de forma consistente a todo el equipo.
- Ficheros `.claude/rules/` con globs en el frontmatter (`paths: ["src/api/**/*"]`, `paths: ["**/*.test.*"]`). **Comprueba que solo cargan al editar ficheros que casan.**
- Una skill de proyecto en `.claude/skills/` con `context: fork` y restricciones de `allowed-tools`. Verifica que corre aislada sin contaminar el contexto principal.
- Un servidor MCP en `.mcp.json` con expansión de variables de entorno para credenciales. Añade uno personal experimental en `~/.claude.json` y **verifica que ambos están disponibles a la vez**.
- Prueba plan mode frente a ejecución directa en tres tareas de complejidad distinta: bug de un fichero, migración de librería multi-fichero, y una feature nueva con varios enfoques válidos.

### Ejercicio 3 · Pipeline de extracción estructurada
**Refuerza:** D4, D5

- Tool de extracción con JSON schema: campos obligatorios y opcionales, un enum con patrón `"other"` + string de detalle, y campos nullable. Procesa documentos a los que les faltan campos y **verifica que el modelo devuelve `null` en vez de inventar**.
- Bucle validación-reintento: cuando falla la validación (Pydantic o JSON schema), manda un seguimiento con el documento, la extracción fallida y el error concreto. **Registra qué errores se resuelven con reintento (formato) y cuáles no (información ausente).**
- Añade few-shot con formatos variados (citas inline frente a bibliografía, descripción narrativa frente a tabla estructurada).
- Estrategia de batch: 100 documentos por la Message Batches API, manejo de fallos por `custom_id`, reenvío con modificaciones (trocear los que se pasaron de contexto), y cálculo del tiempo total frente al SLA.
- Enrutado de revisión humana: confianza por campo, baja confianza a humano, y **análisis de precisión por tipo de documento y campo**.

### Ejercicio 4 · Diseñar y depurar un pipeline de investigación multiagente
**Refuerza:** D1, D2, D5

- Coordinador que delega en al menos dos subagentes. Asegúrate de que su `allowedTools` incluye `"Task"` y de que **cada subagente recibe los hallazgos en su prompt**, sin confiar en herencia automática.
- Ejecución paralela: el coordinador emite **varias llamadas a `Task` en una sola respuesta**. Mide la mejora de latencia frente a secuencial.
- Salida estructurada que separa contenido de metadatos: cada hallazgo con afirmación, extracto de evidencia, URL/nombre de documento y fecha de publicación. **Verifica que la síntesis preserva la atribución.**
- Propagación de errores: simula un timeout de subagente y verifica que el coordinador recibe contexto estructurado (tipo de fallo, consulta intentada, resultados parciales). Prueba que puede continuar con parciales y **anotar los huecos de cobertura**.
- Prueba con datos en conflicto: dos fuentes creíbles con estadísticas distintas. Verifica que la síntesis **preserva ambos valores con atribución** en vez de elegir uno, y distingue lo bien establecido de lo contestado.

## 9.3 · Los cursos oficiales de preparación

La Anthropic Partner Academy lista este *prep path* para CCAR-F:

| Curso | Qué aporta |
|---|---|
| AI Fluency: Framework & Foundations | Colaborar con sistemas de IA de forma eficaz, eficiente, ética y segura |
| **Building with the Claude API** | El espectro completo de trabajar con los modelos vía Claude API |
| Claude on Google Cloud | Los modelos sobre Google Cloud |
| **Claude Code in Action** | Sesiones largas y sin supervisión en las que se puede confiar: dirigir, configurar, automatizar y verificar |
| Claude 101 | Claude para tareas rutinarias, funcionalidades básicas |
| Claude with Amazon Bedrock | Programa de acreditación creado por AWS |
| **Introduction to Model Context Protocol** | Construir servidores y clientes MCP desde cero con Python |

En **negrita** los tres que este repo tiene resumidos en español.

---

## 9.4 · Mapa curso ↔ dominio

Qué cubre cada curso de este repo, y con qué profundidad.

| Curso de este repo | D1 27 % | D2 18 % | D3 20 % | D4 20 % | D5 15 % |
|---|:-:|:-:|:-:|:-:|:-:|
| [Claude Code in Action](../claude-code-in-action/) | ◐ | | **●** | ◐ | ◐ |
| [Introduction to Subagents](../introduction-to-subagents/) | **●** | ◐ | | | ◐ |
| [Introduction to Model Context Protocol](../introduction-to-model-context-protocol/) | | **●** | | | |
| [MCP: Advanced Topics](../model-context-protocol-advanced-topics/) | | ◐ | | | |
| [Claude with the Anthropic API](../claude-with-the-anthropic-api/) | ◐ | ◐ | ◐ | **●** | ◐ |
| [Introduction to Agent Skills](../introduction-to-agent-skills/) | | | **●** | | |

**●** cubre el grueso del dominio · **◐** cubre una parte

### Qué aporta cada uno, en concreto

**Claude Code in Action** → D3 casi entero: `CLAUDE.md`, modos de permisos, hooks, headless y GitHub Actions (que es 3.6), y la disciplina de verificación. Toca D1 por los hooks y D5 por la gestión de sesiones largas.

**Introduction to Subagents** → D1.2 y D1.3 en su núcleo: aislamiento de contexto, que el subagente no hereda nada, la `description` como disparador, formato de salida estructurado, y los antipatrones (pipeline secuencial, test runner). La regla *"¿importa el trabajo intermedio?"* es exactamente el criterio de delegación que pregunta el examen.

**Introduction to Model Context Protocol** → D2.4 y D2.5: las tres primitivas, tools frente a resources, y **quién decide cuándo se usan**. El concepto de *resource como catálogo de contenido* que pregunta 2.4 sale de aquí.

**MCP: Advanced Topics** → **cuidado**: sampling, roots, transportes STDIO/StreamableHTTP/SSE y `stateless_http` son excelente material de MCP pero **caen en la lista de temas fuera de alcance** del examen ("Deploying or hosting MCP servers", "Streaming API implementation or server-sent events"). Es un curso que te hace mejor arquitecto, no que te aprueba el examen.

**Claude with the Anthropic API** → D4 casi entero: prompt engineering medido, tool use con esquemas, evals. Y aporta a D1 (agentes y workflows), D2 (tool use) y D5.

**Introduction to Agent Skills** → D3.2 al detalle: `SKILL.md`, `allowed-tools`, divulgación progresiva, skills frente a `CLAUDE.md` frente a hooks, y diagnóstico cuando no se dispara.

---

## 9.5 · Lo que este repo NO te cubre

Honestidad por delante: hay objetivos del blueprint que **ningún curso de los resumidos aquí toca**, o los toca de refilón. Si vas a examinarte, estos son tus deberes aparte.

| Hueco | Dominio | Dónde mirar |
|---|---|---|
| `AgentDefinition`, `allowedTools`, la `Task` tool, `fork_session` | 1.3, 1.7 | Documentación del **Claude Agent SDK** |
| Hooks `PostToolUse` para normalizar datos e interceptar llamadas | 1.5 | Agent SDK · el curso de Claude Code cubre hooks de Claude Code, que no es exactamente lo mismo |
| `.claude/rules/` con `paths` en el frontmatter YAML | 3.3 | Documentación de Claude Code |
| `context: fork` y `argument-hint` en `SKILL.md` | 3.2 | Documentación de Claude Code |
| `--output-format json` y `--json-schema` | 3.6 | `claude --help` |
| Message Batches API: ventana, `custom_id`, cálculo de SLA | 4.5 | Documentación de la Claude API |
| Calibración de confianza, muestreo estratificado, precisión por segmento | 5.5 | Sin cobertura en el repo |
| Mapeos claim–source, anotación de conflictos, datos temporales | 5.6 | Sin cobertura en el repo |
| Recuperación ante caídas con manifiestos de estado | 5.4 | Sin cobertura en el repo |

El **dominio 5** es donde el repo va más flojo — y es el que aparece como dominio secundario en **cuatro de los seis escenarios**.

---

## 9.6 · Apéndice de la guía: qué entra y qué no

### Tecnologías y conceptos que pueden aparecer

- **Claude Agent SDK** — agent definitions, bucles agénticos, manejo de `stop_reason`, hooks (`PostToolUse`, intercepción de llamadas), spawning de subagentes vía `Task` tool, configuración de `allowedTools`
- **Model Context Protocol (MCP)** — servidores, tools, resources, flag `isError`, descripciones de tool, distribución de tools, configuración de `.mcp.json`, expansión de variables de entorno
- **Claude Code** — jerarquía de `CLAUDE.md` (usuario/proyecto/directorio), `.claude/rules/` con path-scoping en frontmatter YAML, `.claude/commands/`, `.claude/skills/` con frontmatter de `SKILL.md` (`context: fork`, `allowed-tools`, `argument-hint`), plan mode, ejecución directa, `/memory`, `/compact`, `--resume`, `fork_session`, subagente `Explore`
- **Claude Code CLI** — `-p` / `--print`, `--output-format json`, `--json-schema`
- **Claude API** — `tool_use` con JSON schemas, opciones de `tool_choice`, valores de `stop_reason`, `max_tokens`, system prompts
- **Message Batches API** — 50 % de ahorro, ventana de hasta 24 horas, `custom_id`, polling, sin soporte de tool calling multiturno
- **JSON Schema** — campos obligatorios frente a opcionales, enums, nullable, patrón `"other"` + string de detalle, modo estricto
- **Pydantic** — validación de esquema, errores semánticos, bucles validación-reintento
- **Tools integradas** — `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`
- **Few-shot prompting**, **prompt chaining**, **gestión de ventana de contexto** (presupuestos de tokens, summarización progresiva, lost-in-the-middle, extracción de contexto, scratchpads), **gestión de sesión**, **confidence scoring**

### Temas **fuera de alcance** — no aparecen

- Fine-tuning de modelos Claude o entrenar modelos propios
- Autenticación, facturación o gestión de cuenta de la Claude API
- Implementación detallada de lenguajes o frameworks concretos (más allá de lo necesario para configurar tools y esquemas)
- **Desplegar u hospedar servidores MCP** (infraestructura, redes, orquestación de contenedores)
- Arquitectura interna de Claude, proceso de entrenamiento o pesos del modelo
- Constitutional AI, RLHF o metodologías de safety training
- Modelos de embedding o detalles de implementación de bases de datos vectoriales
- **Computer use** (automatización de navegador, interacción de escritorio)
- Capacidades de **visión / análisis de imagen**
- **Implementación de streaming API o server-sent events**
- Rate limiting, cuotas o cálculos de precio de API
- OAuth, rotación de API keys o detalles de protocolos de autenticación
- Configuraciones de proveedores cloud concretos (AWS, GCP, Azure)
- Benchmarking de rendimiento o métricas de comparación de modelos
- **Detalles de implementación de prompt caching** (más allá de saber que existe)
- Algoritmos de conteo de tokens o especificidades de tokenización

> **Esta lista vale oro.** Ahorra estudiar de más, pero sobre todo **descarta opciones**: si una respuesta se apoya en algo que está fuera de alcance, casi seguro es un distractor.

---

**Anterior:** [8 · Preguntas oficiales](08-preguntas-oficiales.md) · **Índice:** [README](README.md)
