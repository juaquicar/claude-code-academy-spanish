# 8 · Las 12 preguntas oficiales de muestra

La sección 9 del **Exam Guide** publica 12 preguntas de muestra "sacadas del test de práctica", con su explicación, para ilustrar el formato y el nivel de dificultad. Aquí están traducidas, con el enunciado y las opciones íntegras y la explicación oficial.

> **Aviso.** Son las preguntas de **muestra publicadas por Anthropic en la guía**, no contenido del examen real (que está bajo NDA). Cubren 4 de los 6 escenarios: no hay muestras de *Developer Productivity* ni de *Structured Data Extraction*.

---

## Escenario · Customer Support Resolution Agent

### Pregunta 1

Los datos de producción muestran que en el **12 % de los casos** tu agente se salta `get_customer` por completo y llama a `lookup_order` usando solo el nombre que dice el cliente, lo que ocasionalmente lleva a cuentas mal identificadas y reembolsos incorrectos. ¿Qué cambio abordaría de forma más eficaz este problema de fiabilidad?

- **A.** Añadir un prerrequisito programático que bloquee las llamadas a `lookup_order` y `process_refund` hasta que `get_customer` haya devuelto un ID de cliente verificado.
- **B.** Mejorar el system prompt para indicar que la verificación del cliente vía `get_customer` es obligatoria antes de cualquier operación sobre pedidos.
- **C.** Añadir ejemplos few-shot que muestren al agente llamando siempre a `get_customer` primero, incluso cuando el cliente aporta detalles del pedido.
- **D.** Implementar un clasificador de enrutado que analice cada petición y habilite solo el subconjunto de tools apropiado para ese tipo de petición.

**Correcta: A.** Cuando se requiere una secuencia de herramientas concreta para lógica de negocio crítica (como verificar la identidad del cliente antes de procesar reembolsos), **el enforcement programático da garantías deterministas que los enfoques basados en prompt no pueden dar**. Las opciones B y C dependen del cumplimiento probabilístico del LLM, insuficiente cuando los errores tienen consecuencias financieras. La opción D aborda la **disponibilidad** de herramientas, no su **orden**, que es el problema real.

---

### Pregunta 2

Los logs de producción muestran que el agente llama con frecuencia a `get_customer` cuando los usuarios preguntan por pedidos (por ejemplo, *"mira mi pedido #12345"*), en vez de llamar a `lookup_order`. Ambas tools tienen descripciones mínimas (*"Retrieves customer information"* / *"Retrieves order details"*) y aceptan formatos de identificador similares. ¿Cuál es el **primer paso** más eficaz para mejorar la fiabilidad de selección?

- **A.** Añadir ejemplos few-shot al system prompt demostrando la selección correcta, con 5-8 ejemplos de consultas de pedido enrutadas a `lookup_order`.
- **B.** Ampliar la descripción de cada tool para incluir los formatos de entrada que maneja, consultas de ejemplo, casos límite y fronteras que expliquen cuándo usarla frente a tools similares.
- **C.** Implementar una capa de enrutado que parsee la entrada del usuario antes de cada turno y preseleccione la tool según palabras clave y patrones de identificador detectados.
- **D.** Consolidar ambas tools en una sola `lookup_entity` que acepte cualquier identificador y decida internamente a qué backend consultar.

**Correcta: B.** **Las descripciones de tool son el mecanismo principal que usan los LLM para seleccionarlas.** Cuando son mínimas, al modelo le falta contexto para diferenciar entre tools parecidas. La opción B ataca la causa raíz con un arreglo de poco esfuerzo y mucho apalancamiento. Los ejemplos few-shot (A) añaden coste de tokens sin arreglar el problema de fondo. Una capa de enrutado (C) está sobreingenierizada y esquiva la comprensión de lenguaje natural del LLM. Consolidar tools (D) es una decisión arquitectónica válida pero **requiere más esfuerzo del que justifica un "primer paso"** cuando el problema inmediato son descripciones inadecuadas.

---

### Pregunta 3

Tu agente consigue un **55 % de resolución en primer contacto**, muy por debajo del objetivo del 80 %. Los logs muestran que escala casos sencillos (reemplazos estándar por daño con evidencia fotográfica) mientras intenta manejar de forma autónoma situaciones complejas que requieren excepciones de política. ¿Cuál es la forma más eficaz de mejorar la calibración del escalado?

- **A.** Añadir criterios de escalado explícitos al system prompt con ejemplos few-shot que demuestren cuándo escalar y cuándo resolver de forma autónoma.
- **B.** Hacer que el agente autoinforme una puntuación de confianza (1-10) antes de cada respuesta y enrutar automáticamente a humanos cuando caiga por debajo de un umbral.
- **C.** Desplegar un modelo clasificador aparte, entrenado con tickets históricos, que prediga qué peticiones necesitan escalado antes de que el agente principal empiece.
- **D.** Implementar análisis de sentimiento para detectar el nivel de frustración del cliente y escalar automáticamente cuando el sentimiento negativo supere un umbral.

**Correcta: A.** Añadir criterios explícitos con few-shot ataca directamente la causa raíz: **fronteras de decisión poco claras**. Es la respuesta proporcionada antes de añadir infraestructura. La B falla porque **la confianza autoinformada por un LLM está mal calibrada** — el agente ya es incorrectamente confiado en los casos difíciles. La C está sobreingenierizada: requiere datos etiquetados e infraestructura de ML cuando no se ha probado optimizar el prompt. La D resuelve un problema distinto: **el sentimiento no correlaciona con la complejidad del caso**, que es el problema real.

---

## Escenario · Code Generation with Claude Code

### Pregunta 4

Quieres crear un slash command `/review` a medida que ejecute el checklist de revisión estándar de tu equipo. Debe estar disponible para **todos los desarrolladores** cuando clonen o hagan pull del repositorio. ¿Dónde creas el fichero del comando?

- **A.** En el directorio `.claude/commands/` del repositorio del proyecto.
- **B.** En `~/.claude/commands/` en el directorio home de cada desarrollador.
- **C.** En el fichero `CLAUDE.md` de la raíz del proyecto.
- **D.** En un fichero `.claude/config.json` con un array `commands`.

**Correcta: A.** Los slash commands de ámbito de proyecto van en **`.claude/commands/`** dentro del repositorio. Quedan bajo control de versiones y disponibles automáticamente para todos al clonar o hacer pull. La opción B (`~/.claude/commands/`) es para comandos personales que **no** se comparten por control de versiones. La C (`CLAUDE.md`) es para instrucciones y contexto del proyecto, no para definiciones de comando. **La opción D describe un mecanismo de configuración que no existe en Claude Code.**

---

### Pregunta 5

Te han asignado reestructurar la aplicación monolítica del equipo en microservicios. Implica cambios en decenas de ficheros y requiere decisiones sobre fronteras de servicio y dependencias entre módulos. ¿Qué enfoque tomas?

- **A.** Entrar en plan mode para explorar el codebase, entender las dependencias y diseñar un enfoque de implementación antes de hacer cambios.
- **B.** Empezar con ejecución directa y hacer cambios incrementales, dejando que la implementación revele las fronteras naturales de servicio.
- **C.** Usar ejecución directa con instrucciones exhaustivas por adelantado que detallen exactamente cómo debe estructurarse cada servicio.
- **D.** Empezar en modo de ejecución directa y cambiar a plan mode solo si aparece complejidad inesperada durante la implementación.

**Correcta: A.** Plan mode está diseñado para tareas complejas con cambios a gran escala, múltiples enfoques válidos y decisiones arquitectónicas — exactamente lo que exige pasar de monolito a microservicios. Permite explorar el codebase y diseñar de forma segura antes de comprometerse a cambios. La B arriesga retrabajo caro cuando las dependencias se descubren tarde. La C asume que ya conoces la estructura correcta sin haber explorado el código. **La D ignora que la complejidad ya está enunciada en los requisitos**, no es algo que pueda emerger más tarde.

---

### Pregunta 6

Tu codebase tiene áreas con convenciones distintas: los componentes React usan estilo funcional con hooks, los handlers de API usan `async/await` con manejo de errores específico, y los modelos de base de datos siguen el patrón repositorio. Los ficheros de test están **repartidos por todo el codebase junto al código que testean** (por ejemplo `Button.test.tsx` junto a `Button.tsx`), y quieres que todos los tests sigan las mismas convenciones **independientemente de su ubicación**. ¿Cuál es la forma más mantenible de que Claude aplique automáticamente las convenciones correctas al generar código?

- **A.** Crear ficheros de regla en `.claude/rules/` con frontmatter YAML que especifique patrones glob para aplicar convenciones condicionalmente según la ruta del fichero.
- **B.** Consolidar todas las convenciones en el `CLAUDE.md` raíz bajo cabeceras por área, confiando en que Claude infiera qué sección aplica.
- **C.** Crear skills en `.claude/skills/` para cada tipo de código, con las convenciones relevantes en sus ficheros `SKILL.md`.
- **D.** Poner un `CLAUDE.md` separado en cada subdirectorio con las convenciones específicas de esa área.

**Correcta: A.** `.claude/rules/` con patrones glob (por ejemplo `**/*.test.tsx`) permite aplicar convenciones según la ruta **independientemente del directorio**, esencial para ficheros de test repartidos por el codebase. La B depende de inferencia en vez de coincidencia explícita, lo que la hace poco fiable. La C requiere invocación manual de la skill o confiar en que Claude decida cargarla, lo que **contradice la necesidad de aplicación "automática"** basada en rutas. La D no maneja bien ficheros dispersos por muchos directorios, porque **los `CLAUDE.md` están atados a un directorio**.

---

## Escenario · Multi-Agent Research System

### Pregunta 7

Tras ejecutar el sistema sobre el tema *"impacto de la IA en las industrias creativas"*, observas que **cada subagente termina con éxito**: el de búsqueda web encuentra artículos relevantes, el de análisis de documentos resume los papers correctamente, y el de síntesis produce salida coherente. Sin embargo, los informes finales cubren **solo artes visuales**, y omiten por completo música, escritura y producción cinematográfica. Al examinar los logs del coordinador ves que descompuso el tema en tres subtareas: *"IA en creación de arte digital"*, *"IA en diseño gráfico"* e *"IA en fotografía"*. ¿Cuál es la causa raíz más probable?

- **A.** Al agente de síntesis le faltan instrucciones para identificar huecos de cobertura en los hallazgos que recibe.
- **B.** La descomposición de tareas del coordinador es demasiado estrecha, produciendo asignaciones que no cubren todos los dominios relevantes del tema.
- **C.** Las consultas del agente de búsqueda web no son suficientemente exhaustivas y hay que ampliarlas a más sectores creativos.
- **D.** El agente de análisis de documentos está filtrando fuentes de industrias creativas no visuales por criterios de relevancia demasiado restrictivos.

**Correcta: B.** Los logs del coordinador revelan la causa raíz directamente: descompuso "industrias creativas" en subtareas **solo de artes visuales**, omitiendo música, escritura y cine. **Los subagentes ejecutaron correctamente sus tareas asignadas — el problema es qué se les asignó.** Las opciones A, C y D culpan incorrectamente a agentes de aguas abajo que están funcionando bien dentro del alcance que se les dio.

---

### Pregunta 8

El subagente de búsqueda web hace **timeout** investigando un tema complejo. Necesitas diseñar cómo fluye esa información de fallo de vuelta al coordinador. ¿Qué enfoque de propagación de errores permite mejor una recuperación inteligente?

- **A.** Devolver al coordinador contexto de error estructurado que incluya el tipo de fallo, la consulta intentada, cualquier resultado parcial y posibles enfoques alternativos.
- **B.** Implementar lógica de reintento automático con backoff exponencial dentro del subagente, devolviendo un estado genérico *"search unavailable"* solo tras agotar los reintentos.
- **C.** Capturar el timeout dentro del subagente y devolver un conjunto de resultados vacío marcado como exitoso.
- **D.** Propagar la excepción de timeout directamente a un handler de nivel superior que termine el workflow de investigación completo.

**Correcta: A.** El contexto de error estructurado le da al coordinador la información que necesita para decidir con criterio: reintentar con una consulta modificada, probar un enfoque alternativo, o seguir con resultados parciales. El estado genérico de la B **esconde contexto valioso** e impide decisiones informadas. La C **suprime el error marcando el fallo como éxito**, lo que impide cualquier recuperación y arriesga resultados incompletos. La D termina el workflow entero innecesariamente cuando había estrategias de recuperación que podían funcionar.

---

### Pregunta 9

Durante las pruebas observas que el agente de síntesis necesita con frecuencia verificar afirmaciones concretas mientras combina hallazgos. Ahora mismo, cuando hace falta verificar, devuelve el control al coordinador, que invoca al agente de búsqueda web y luego re-invoca la síntesis con los resultados. Eso añade 2-3 viajes de ida y vuelta por tarea y **aumenta la latencia un 40 %**. Tu evaluación muestra que el **85 %** de esas verificaciones son comprobaciones simples (fechas, nombres, estadísticas) y el **15 %** requiere investigación más profunda. ¿Cuál es el enfoque más eficaz para reducir la sobrecarga manteniendo la fiabilidad?

- **A.** Dar al agente de síntesis una tool `verify_fact` acotada para consultas simples, mientras las verificaciones complejas siguen delegándose al agente de búsqueda a través del coordinador.
- **B.** Hacer que el agente de síntesis acumule todas sus necesidades de verificación y las devuelva en lote al coordinador al final de su pasada, que las manda todas de golpe al agente de búsqueda.
- **C.** Dar al agente de síntesis acceso a todas las tools de búsqueda web para que maneje cualquier verificación directamente sin viajes por el coordinador.
- **D.** Hacer que el agente de búsqueda cachee proactivamente contexto extra alrededor de cada fuente durante la investigación inicial, anticipando lo que la síntesis podría querer verificar.

**Correcta: A.** La opción A aplica el **principio de mínimo privilegio**: le da al agente de síntesis solo lo que necesita para el 85 % de casos comunes, preservando el patrón de coordinación para los complejos. El batching de la B **crea dependencias bloqueantes**, porque los pasos de síntesis pueden depender de hechos verificados anteriormente. La C **sobreaprovisiona** al agente de síntesis, violando la separación de responsabilidades. La D depende de un cacheo especulativo que **no puede predecir de forma fiable** qué necesitará verificar la síntesis.

---

## Escenario · Claude Code for Continuous Integration

### Pregunta 10

Tu script de pipeline ejecuta `claude "Analyze this pull request for security issues"` pero el job **se cuelga indefinidamente**. Los logs indican que Claude Code está esperando entrada interactiva. ¿Cuál es el enfoque correcto para ejecutar Claude Code en un pipeline automatizado?

- **A.** Añadir el flag `-p`: `claude -p "Analyze this pull request for security issues"`
- **B.** Definir la variable de entorno `CLAUDE_HEADLESS=true` antes de ejecutar el comando.
- **C.** Redirigir stdin desde `/dev/null`: `claude "Analyze this pull request for security issues" < /dev/null`
- **D.** Añadir el flag `--batch`: `claude --batch "Analyze this pull request for security issues"`

**Correcta: A.** El flag **`-p`** (o `--print`) es la forma documentada de ejecutar Claude Code en modo no interactivo. Procesa el prompt, escribe el resultado a stdout y sale sin esperar entrada del usuario — exactamente lo que necesita un pipeline de CI/CD. Las demás opciones referencian **funcionalidades que no existen** (la variable `CLAUDE_HEADLESS`, el flag `--batch`) o usan apaños de Unix que no abordan correctamente la sintaxis del comando.

---

### Pregunta 11

Tu equipo quiere reducir costes de API. Ahora mismo dos workflows usan llamadas en tiempo real: (1) una comprobación **pre-merge bloqueante** que debe terminar antes de que los desarrolladores puedan mergear, y (2) un **informe de deuda técnica generado de noche** para revisar a la mañana siguiente. Tu manager propone pasar los dos a la Message Batches API por su 50 % de ahorro. ¿Cómo evalúas la propuesta?

- **A.** Usar batch solo para los informes de deuda técnica; mantener llamadas en tiempo real para las comprobaciones pre-merge.
- **B.** Pasar ambos a batch con polling de estado para comprobar la finalización.
- **C.** Mantener tiempo real en ambos para evitar problemas de ordenación de resultados del batch.
- **D.** Pasar ambos a batch con un fallback por timeout a tiempo real si los lotes tardan demasiado.

**Correcta: A.** La Message Batches API ofrece **50 % de ahorro pero con tiempos de hasta 24 horas y sin SLA de latencia garantizado**. Eso la hace **inadecuada para comprobaciones pre-merge bloqueantes** donde el desarrollador está esperando, e ideal para trabajos nocturnos como informes de deuda técnica. La B es incorrecta porque confiar en que "suele ser más rápido" no es aceptable para un workflow bloqueante. **La C refleja un malentendido: los resultados de batch se correlacionan con `custom_id`.** La D añade complejidad innecesaria cuando la solución simple es emparejar cada API con su caso de uso.

---

### Pregunta 12

Un pull request modifica **14 ficheros** del módulo de seguimiento de stock. Tu revisión de una sola pasada analizando todos los ficheros juntos produce resultados inconsistentes: feedback detallado para algunos ficheros y comentarios superficiales para otros, bugs obvios que se pasan, y **feedback contradictorio** — marcando un patrón como problemático en un fichero mientras aprueba código idéntico en otro del mismo PR. ¿Cómo reestructuras la revisión?

- **A.** Partirla en pasadas enfocadas: analizar cada fichero individualmente para problemas locales, y luego una pasada separada centrada en integración que examine el flujo de datos entre ficheros.
- **B.** Exigir a los desarrolladores que partan los PRs grandes en envíos de 3-4 ficheros antes de que corra la revisión automática.
- **C.** Cambiar a un modelo de tier superior con ventana de contexto mayor para dar atención adecuada a los 14 ficheros en una sola pasada.
- **D.** Ejecutar tres pasadas de revisión independientes sobre el PR completo y marcar solo los problemas que aparezcan en al menos dos de las tres.

**Correcta: A.** Partir la revisión en pasadas enfocadas ataca la causa raíz: **dilución de atención** al procesar muchos ficheros a la vez. El análisis fichero a fichero garantiza profundidad consistente, y una pasada de integración aparte captura los problemas entre ficheros. La B traslada la carga a los desarrolladores sin mejorar el sistema. **La C malinterpreta que una ventana de contexto mayor no resuelve la calidad de atención.** La D **suprimiría la detección de bugs reales**, al exigir consenso sobre problemas que quizá solo se detectan de forma intermitente.

---

## El patrón que se repite en las 12

Léelas juntas y sale un sesgo consistente. **El examen premia el arreglo más simple que funciona y que ataca la causa raíz**, y castiga tres cosas:

| Sesgo | Ejemplo |
|---|---|
| **Sobreingeniería** | Clasificador ML entrenado (P3-C), capa de routing por keywords (P2-C), modelo de tier superior (P12-C) |
| **Confiar en lo probabilístico cuando se exige determinismo** | Prompt o few-shot para forzar orden de tools (P1-B, P1-C) |
| **Culpar a quien funciona bien** | Los subagentes de aguas abajo cuando el fallo es del coordinador (P7-A/C/D) |

Y aparecen **opciones que citan funcionalidades inexistentes**: `.claude/config.json` con array `commands` (P4-D), `CLAUDE_HEADLESS` y `--batch` (P10-B/D). Si una opción menciona algo que no reconoces del producto, sospecha.

---

**Anterior:** [7 · Los seis escenarios](07-los-seis-escenarios.md) · **Siguiente:** [9 · Plan de estudio](09-plan-de-estudio.md)
