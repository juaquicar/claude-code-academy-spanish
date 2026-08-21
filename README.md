# Claude Code Academy — resúmenes en español

Resúmenes completos, en español, de los cursos de la [Anthropic Academy](https://www.anthropic.com/learn) sobre Claude Code — y una guía de la certificación **[Claude Certified Architect – Foundations](certificacion-ccar-f/)** hacia la que apuntan.

Cada curso trae **un `.md` por lección** para leer en el editor, y **un `curso-interactivo.html`** autocontenido —sin dependencias ni conexión— con diagramas interactivos, flashcards, quiz con corrección al momento, seguimiento de progreso, buscador y tema claro/oscuro. Se abre con doble clic.

## Cursos

| Curso | Lecciones | Contenido |
|---|---|---|
| **[Claude Code 101](claude-code-101/)** | 13 | Qué es y cómo funciona · Instalación · Tu primer prompt y Plan Mode · Explore → Plan → Code → Commit · Gestión del contexto · Revisión de código · CLAUDE.md · Subagentes · Skills · MCP · Hooks |
| **[Claude Platform 101](claude-platform-101/)** | 14 | La plataforma y sus tres capas · Tu primera llamada · Elegir el modelo · El bucle del agente · Tool use y tool runner · Thinking · Tools integradas · Skills · MCP · Gestión del contexto · Agentes gestionados · Construir con Claude Code |
| **[Claude Code in Action](claude-code-in-action/)** | 9 | Dirigir sesiones largas · CLAUDE.md · Skills de verificación · Modos de permisos · Hooks · Routines y headless · GitHub Actions y Code Review · Verificar runs no supervisados · Plugins |
| **[Introduction to Subagents](introduction-to-subagents/)** | 4 | Qué son · Crearlos · Diseñarlos bien · Usarlos con criterio |
| **[MCP: Advanced Topics](model-context-protocol-advanced-topics/)** | 8 | Sampling · Log y progreso · Roots · Mensajes JSON · STDIO · StreamableHTTP · SSE en profundidad · stateless_http y json_response |
| **[Claude with the Anthropic API](claude-with-the-anthropic-api/)** | 85 | API y modelos · Evals · Prompt engineering · Tool use · RAG · Funcionalidades · Prompt caching · MCP · Claude Code · Agentes y workflows |
| **[Introduction to Agent Skills](introduction-to-agent-skills/)** | 6 | Qué son · Crearlas · Configuración y multi-fichero · Vs. otras funcionalidades · Compartir · Diagnóstico |
| **[Introduction to Model Context Protocol](introduction-to-model-context-protocol/)** | 11 | Qué es MCP · Clientes · Tools e inspector · Implementar un cliente · Resources · Prompts · Las tres primitivas |

> **[▶ index.html](index.html)** — página de inicio: navega entre los cursos, busca con `⌘/Ctrl+K`, y ve tu progreso y tu cobertura por dominio del examen. Ábrela con doble clic.

## La certificación

| | Contenido |
|---|---|
| **[Claude Certified Architect – Foundations (CCAR-F)](certificacion-ccar-f/)** | Ficha y políticas · los 5 dominios con sus 30 task statements · los 6 escenarios · las 12 preguntas oficiales de muestra · plan de estudio, mapa curso↔dominio y temas dentro y fuera de alcance |

La credencial hacia la que apuntan estos cursos. **No pregunta sintaxis: pregunta criterio de arquitectura** — un problema de producción con síntomas concretos y cuatro arreglos plausibles, y hay que elegir el que ataca la causa raíz con el esfuerzo proporcionado. Premia el arreglo más simple que funciona, el determinismo donde el resultado lo exige, y diagnosticar dónde falla de verdad. Castiga la sobreingeniería.

**60 ítems · 120 minutos · 4 escenarios de un banco de 6 · corte en 720 sobre 1000 · 125 USD · válida 12 meses.** Pesos por dominio: **27 / 18 / 20 / 20 / 15 %**.

La guía interactiva trae **blueprint navegable, simulacro de 60 preguntas con modo por dominio, flashcards y un panel de preparación** que estima tu nota ponderando por los pesos reales. Todo se guarda en tu navegador; el índice del repo lee ese resumen y te muestra la cobertura por dominio.

> Elaborada a partir del **Exam Guide oficial v1.0** (efectiva julio 2026). La guía oficial es la única referencia autoritativa y puede cambiar sin previo aviso. Este proyecto **no está afiliado ni respaldado por Anthropic PBC**, y aquí no hay preguntas reales del examen: solo las 12 de muestra que la propia guía publica.

### Claude Code 101

[Curso original](https://anthropic.skilljar.com/claude-code-101) · **quiz oficial superado 5/5**

La puerta de entrada. Claude Code no es un chat que te sugiere código: es **un agente que entra en tu repositorio y hace el trabajo**. Y sacarle partido son dos cosas — el flujo **Explore → Plan → Code → Commit** («si te llevas una sola cosa de este curso, que sea este flujo») y **saber qué ocupa tu ventana de contexto**.

Lo contraintuitivo que deja: un prompt vago **no ahorra contexto, lo gasta**; conviene **empezar sin CLAUDE.md** para que lo escriba la experiencia; y si algo tiene que pasar siempre y sin fallo, **no va en un prompt, va en un hook**.

El quiz oficial tiene 7 preguntas, de las que **4 son evaluables**; el repo recoge las reales con sus distractores más un banco extra de 24. La lección **Skills** no tiene texto en la plataforma — solo vídeo y enlace al curso dedicado — y el capítulo lo dice explícitamente en vez de rellenar el hueco.

> **Orden sugerido:** este curso primero, y luego [Claude Code in Action](claude-code-in-action/) para autonomía y verificación.

### Claude Platform 101

[Curso original](https://anthropic.skilljar.com/claude-platform-101) · **quiz oficial superado 6/6**

El salto de **chatear con Claude** a **publicar algo con Claude dentro**. En línea recta: una llamada `messages.create` → un bucle de agente con tools → delegar ese bucle, primero al **tool runner**, después entero a los **managed agents** de Anthropic.

Dos ideas ordenan el curso. La delegación es un espectro: **tú eres dueño del bucle y de las tools, Claude es dueño del razonamiento** — hasta que decides no serlo. Y la elección entre funcionalidades es una regla de tres: **las tools son para tus cosas, las skills para tus procesos, y MCP para las cosas de todos los demás.**

El quiz oficial tiene 8 preguntas, de las que **5 son evaluables**; el repo recoge las reales más un banco extra de 28.

> **Orden sugerido:** después de este, [Claude with the Anthropic API](claude-with-the-anthropic-api/) para evals, prompt engineering y RAG en profundidad.

### Claude Code in Action

[Curso original](https://anthropic.skilljar.com/claude-code-in-action) · **quiz oficial superado 8/8**

Llevar Claude Code más allá de la tarea rápida y poder *confiar* en el resultado. El eje: cuanta más autonomía le des, más deliberadas tienen que ser dos cosas — **qué le permites hacer antes** (permisos, hooks, instrucciones) y **cómo compruebas lo que hizo después** (diff, tests como puerta, segunda opinión).

Incluye las **8 preguntas reales del quiz oficial** con su feedback, más 15 de repaso.

### Introduction to Subagents

[Curso original](https://anthropic.skilljar.com/introduction-to-subagents)

Usar y crear subagentes para gestionar el contexto y delegar tareas. El eje: un subagente es **una ventana de contexto aparte** que devuelve solo un resumen y descarta el resto. La regla de decisión — **¿importa el trabajo intermedio?** No → delega. Sí → hilo principal.

Este curso no tiene quiz oficial; el repo incluye una autoevaluación de 12 preguntas construida a partir del material.

### MCP: Advanced Topics

[Curso original](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)

Las capacidades de MCP que van más allá de exponer herramientas. El eje: **sampling, notificaciones y roots son la misma cosa vista desde tres ángulos** — el servidor pidiéndole algo al cliente. STDIO da esa dirección gratis; HTTP no, y la rescata con un apaño de SSE que dos flags desmontan.

Los tres walkthroughs de código de la plataforma están integrados: en el HTML se navegan paso a paso, con las líneas exactas resaltadas. La evaluación oficial de 10 preguntas está pendiente de hacer.

### Claude with the Anthropic API

[Curso original](https://anthropic.skilljar.com/claude-with-the-anthropic-api)

El más grande de la academia: 85 lecciones desde la primera llamada al API hasta construir agentes. Enseña **una disciplina, no una lista de funcionalidades** — pide, mide antes de retocar, mejora con técnicas medidas (el curso puntúa cada una: **2,32 → 3,92 → 7,86**), extiende, optimiza, integra y elige la arquitectura.

Cierra con un consejo que va a contracorriente: **prioriza workflows.** Los usuarios quieren productos que funcionen al 100%, no agentes vistosos.

Las **8 evaluaciones oficiales** (7 quizzes de bloque + evaluación final) están pendientes de hacer.

### Introduction to Agent Skills

[Curso original](https://anthropic.skilljar.com/introduction-to-agent-skills)

Una skill es un fichero markdown que le enseña a Claude cómo hacer algo **una vez**, y que aplica **automáticamente** cuando viene al caso. La regla de oro: *si te encuentras explicándole lo mismo a Claude una y otra vez, eso es una skill esperando a ser escrita*.

Todo el curso gravita sobre un campo, la **`description`**: decide si la skill se activa —por coincidencia semántica— y es donde está el problema cuando algo falla.

Este curso no tiene quiz oficial; el repo incluye una autoevaluación de 14 preguntas.

### Introduction to Model Context Protocol

[Curso original](https://anthropic.skilljar.com/introduction-to-model-context-protocol)

MCP traslada el trabajo de escribir esquemas y funciones de herramienta **del desarrollador de la aplicación al mantenedor del servidor MCP**. Un servidor tiene tres primitivas, y la lección final las ordena con una idea que lo aclara todo: **se distinguen por quién decide cuándo se usan** — el modelo (tools), la aplicación (resources) o el usuario (prompts).

La **evaluación final oficial** está pendiente de hacer.

> **Orden sugerido:** este curso primero, y luego [MCP: Advanced Topics](model-context-protocol-advanced-topics/) para sampling, roots, transportes y los flags que rompen el despliegue.

## Estructura

```
CLAUDE.md                     cómo se elabora un curso, de principio a fin
index.html                    página de inicio: cursos, progreso y certificación
scripts/
├── extraer_curso.py          descarga un curso de Skilljar → markdown crudo
└── validar_html.py           valida un curso-interactivo.html antes de publicarlo
<nombre-del-curso>/
├── README.md                 índice y hilo conductor del curso
├── 01-....md ... NN-....md   una lección por fichero
└── curso-interactivo.html    el curso entero en una página
certificacion-ccar-f/
├── README.md                 índice y hilo conductor de la certificación
├── 01-la-certificacion.md    ficha, blueprint, registro, políticas, renovación
├── 02-....md ... 06-....md   un fichero por dominio del examen
├── 07-los-seis-escenarios.md los 6 escenarios y el mapa escenario↔dominio
├── 08-preguntas-oficiales.md las 12 preguntas de muestra de la guía oficial
├── 09-plan-de-estudio.md     preparación, mapa curso↔dominio, huecos, alcance
└── certificacion-interactiva.html
```

## Añadir un curso nuevo

```bash
python3 scripts/extraer_curso.py <slug-del-curso>     # → /tmp/<slug>/raw_*.md
# leer los raw_*.md, escribir los resúmenes y el HTML
python3 scripts/validar_html.py <slug>/curso-interactivo.html
```

El procedimiento completo y las convenciones de redacción están en [CLAUDE.md](CLAUDE.md).

## Aviso

Resúmenes de estudio derivados del material del curso, redactados en español para uso personal. Los cursos originales, sus vídeos y su contenido son de Anthropic. Si te interesa el tema, haz el curso: es gratuito.
