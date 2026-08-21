# 2 · Dominio 1 — Agentic Architecture & Orchestration

**Peso: 27 %** · ~16 de los 60 ítems. **El dominio que más pesa.** Siete task statements.

Escenarios que lo tocan: *Customer Support Resolution Agent*, *Multi-Agent Research System*, *Developer Productivity with Claude*.

---

## 1.1 · Diseñar e implementar bucles agénticos para ejecución autónoma

### Conocimiento

- El **ciclo de vida del bucle agéntico**: mandar la petición a Claude, inspeccionar `stop_reason` (`"tool_use"` frente a `"end_turn"`), ejecutar las herramientas pedidas y devolver los resultados para la siguiente iteración.
- Cómo los **resultados de herramienta se añaden al historial de conversación** para que el modelo pueda razonar sobre la siguiente acción.
- La distinción entre **decisión dirigida por el modelo** (Claude razona qué herramienta llamar según el contexto) y **árboles de decisión o secuencias de herramientas preconfigurados**.

### Habilidades

- Implementar el control de flujo que **continúa cuando `stop_reason` es `"tool_use"`** y **termina cuando es `"end_turn"`**.
- Añadir los resultados de herramienta al contexto **entre iteraciones**, para que el modelo incorpore la información nueva a su razonamiento.

### Antipatrones que el examen castiga

| Antipatrón | Por qué está mal |
|---|---|
| Parsear señales en lenguaje natural para decidir si terminar | El indicador correcto y determinista es `stop_reason`, no el texto |
| Poner un tope arbitrario de iteraciones **como mecanismo principal** de parada | Es una red de seguridad, no la condición de terminación |
| Mirar si hay contenido de texto del asistente como indicador de que acabó | Un turno puede traer texto **y** `tool_use` a la vez |

> **Trampa.** El tope de iteraciones no es "malo": es malo **como mecanismo primario**. Lee siempre el matiz de la opción.

---

## 1.2 · Orquestar sistemas multiagente con patrones coordinador–subagente

### Conocimiento

- Arquitectura **hub-and-spoke**: un coordinador gestiona toda la comunicación entre subagentes, el manejo de errores y el enrutado de información.
- Los subagentes operan con **contexto aislado** — **no heredan automáticamente** el historial del coordinador.
- El papel del coordinador: descomposición de la tarea, delegación, **agregación de resultados** y decidir **qué subagentes invocar** según la complejidad de la consulta.
- El riesgo de una **descomposición demasiado estrecha** por parte del coordinador: cobertura incompleta de temas de investigación amplios.

### Habilidades

- Coordinadores que **analizan los requisitos de la consulta y eligen dinámicamente** qué subagentes invocar, en vez de pasar siempre por el pipeline completo.
- **Particionar el alcance** entre subagentes para minimizar duplicación (subtemas distintos, tipos de fuente distintos).
- Bucles de **refinamiento iterativo**: el coordinador evalúa la síntesis buscando huecos, re-delega a búsqueda y análisis con consultas dirigidas, y vuelve a invocar la síntesis hasta que la cobertura basta.
- Enrutar **toda** la comunicación de subagentes por el coordinador: observabilidad, manejo de errores consistente y flujo de información controlado.

> **Trampa.** Cuando el informe final cubre solo una parte del tema y **cada subagente hizo bien su trabajo**, la causa raíz está en la **descomposición del coordinador**, no en los agentes de aguas abajo. Sale literalmente en las preguntas de muestra.

---

## 1.3 · Configurar invocación de subagentes, paso de contexto y spawning

### Conocimiento

- La **`Task` tool** es el mecanismo para lanzar subagentes, y `allowedTools` **debe incluir `"Task"`** para que un coordinador pueda invocarlos.
- El contexto del subagente **hay que dárselo explícitamente en el prompt**: no hereda el contexto del padre ni comparte memoria entre invocaciones.
- La configuración **`AgentDefinition`**: descripciones, system prompts y restricciones de herramientas por tipo de subagente.
- **Gestión de sesión basada en fork** para explorar enfoques divergentes desde una misma línea base de análisis.

### Habilidades

- Incluir **los hallazgos completos** de agentes previos directamente en el prompt del subagente (por ejemplo, pasar los resultados de búsqueda web y el análisis de documentos al subagente de síntesis).
- Usar **formatos de datos estructurados que separan contenido de metadatos** (URLs de origen, nombres de documento, números de página) al pasar contexto entre agentes, para preservar la atribución.
- Lanzar **subagentes en paralelo emitiendo varias llamadas a `Task` en una sola respuesta** del coordinador, no repartidas en turnos separados.
- Escribir prompts de coordinador que especifican **objetivos y criterios de calidad**, no instrucciones procedimentales paso a paso, para que el subagente pueda adaptarse.

---

## 1.4 · Workflows multipaso con enforcement y patrones de handoff

### Conocimiento

- La diferencia entre **enforcement programático** (hooks, puertas de prerrequisito) y **guía basada en prompt** para ordenar un workflow.
- Cuando hace falta **cumplimiento determinista** —verificar identidad antes de una operación financiera—, las instrucciones de prompt tienen una **tasa de fallo distinta de cero**.
- Protocolos de **handoff estructurado** para escalado a mitad de proceso, que incluyen datos del cliente, análisis de causa raíz y acciones recomendadas.

### Habilidades

- Implementar **prerrequisitos programáticos que bloquean llamadas posteriores** hasta que los pasos previos hayan terminado (bloquear `process_refund` hasta que `get_customer` haya devuelto un ID verificado).
- Descomponer peticiones de cliente con varios asuntos en items distintos, investigar cada uno **en paralelo con contexto compartido** y sintetizar una resolución unificada.
- Compilar **resúmenes de handoff estructurados** (ID de cliente, causa raíz, importe del reembolso, acción recomendada) al escalar a un agente humano que **no tiene acceso a la transcripción**.

> **Regla de oro del dominio.** Consecuencias financieras o de cumplimiento → **enforcement programático**. Prompt, few-shot y system prompt son probabilísticos.

---

## 1.5 · Hooks del Agent SDK para interceptar llamadas y normalizar datos

### Conocimiento

- Patrones de hook —por ejemplo **`PostToolUse`**— que interceptan **resultados** de herramienta para transformarlos antes de que el modelo los procese.
- Patrones de hook que interceptan **llamadas salientes** para hacer cumplir reglas (bloquear reembolsos por encima de un umbral).
- La distinción entre usar hooks para **garantías deterministas** y depender de instrucciones de prompt para **cumplimiento probabilístico**.

### Habilidades

- `PostToolUse` para **normalizar formatos heterogéneos** —timestamps Unix, ISO 8601, códigos de estado numéricos— procedentes de distintas tools MCP, antes de que el agente los procese.
- Hooks de intercepción que **bloquean acciones que violan política** (reembolsos por encima de 500 $) y **redirigen a un workflow alternativo** (escalado a humano).
- Elegir hooks sobre prompt cuando las reglas de negocio requieren cumplimiento garantizado.

---

## 1.6 · Estrategias de descomposición de tareas

### Conocimiento

- Cuándo usar **pipelines secuenciales fijos** (*prompt chaining*) y cuándo **descomposición dinámica adaptativa** basada en hallazgos intermedios.
- Patrones de prompt chaining que parten una revisión en pasos secuenciales: analizar cada fichero por separado y después una **pasada de integración entre ficheros**.
- El valor de los **planes de investigación adaptativos** que generan subtareas según lo que se descubre en cada paso.

### Habilidades

- Elegir el patrón según el workflow: **prompt chaining** para revisiones multiaspecto predecibles; **descomposición dinámica** para investigación abierta.
- Partir revisiones grandes en **pasadas locales por fichero + una pasada de integración aparte** para evitar la **dilución de atención**.
- Descomponer tareas abiertas ("añade tests exhaustivos a este código legacy") mapeando primero la estructura, identificando zonas de alto impacto y creando un plan priorizado que se adapta según aparecen dependencias.

---

## 1.7 · Estado de sesión, reanudación y forking

### Conocimiento

- Reanudación de sesión con nombre: **`--resume <session-name>`**.
- **`fork_session`** para crear ramas independientes desde una línea base compartida y explorar enfoques divergentes.
- La importancia de **avisar al agente de los cambios en ficheros ya analizados** al reanudar tras modificar código.
- Por qué **arrancar sesión nueva con un resumen estructurado es más fiable** que reanudar con resultados de herramienta obsoletos.

### Habilidades

- `--resume` con nombres de sesión para continuar investigaciones entre jornadas.
- `fork_session` para ramas de exploración paralelas (comparar dos estrategias de testing o dos enfoques de refactor partiendo del mismo análisis).
- **Elegir** entre reanudar (cuando el contexto previo sigue siendo válido en su mayoría) y empezar de cero inyectando un resumen (cuando los resultados previos están **stale**).
- Informar a una sesión reanudada de los cambios concretos para un re-análisis **dirigido**, en lugar de forzar una re-exploración completa.

---

## Conclusiones del dominio

- El bucle se controla con **`stop_reason`**, no con heurísticas sobre el texto.
- **Hub-and-spoke:** todo pasa por el coordinador. Los subagentes **no heredan contexto**; se lo pasas tú en el prompt.
- Paralelismo = **varias llamadas a `Task` en una misma respuesta**.
- Cuando el resultado exige garantía, **hook**; cuando admite margen, **prompt**.
- Cobertura incompleta con subagentes correctos ⇒ **la descomposición del coordinador es la culpable**.
- Contexto stale ⇒ **sesión nueva con resumen**, no `--resume`.

---

**Anterior:** [1 · La certificación](01-la-certificacion.md) · **Siguiente:** [3 · Dominio 2 — Herramientas y MCP](03-dominio-2-herramientas-y-mcp.md)
