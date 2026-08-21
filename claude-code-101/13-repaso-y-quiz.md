# 13 — Repaso y quiz

*15 minutos*

El curso **sí trae quiz oficial**: `Course quiz`, **7 preguntas** en la plataforma. De esas 7, solo **4 son de opción múltiple evaluables**; las otras 3 son una encuesta de satisfacción, un NPS y un campo de texto libre. El aprobado se calcula sobre las evaluables (aquí: **5 de 5, 100 %**).

---

## Parte 1 · Las preguntas oficiales

Están reproducidas literalmente, con **la respuesta correcta marcada** y los distractores tal cual aparecen. La plataforma no da explicación textual por pregunta: solo marca acierto o fallo, así que el «por qué» de abajo es del material del curso.

### 1. Claude Code works as an AI agent. What is an AI agent?

- A chatbot that responds to questions in real time
- A code editor with built-in autocomplete features
- A cloud service that hosts your development projects
- ✅ **AI that takes action to complete goals**

**Por qué.** Un agente es software que **interactúa con su entorno y ejecuta acciones** para completar un objetivo definido, con un modelo de lenguaje operando en un bucle. Los tres distractores describen herramientas que **no actúan**: responden, autocompletan o alojan. → [capítulo 01](01-que-es-claude-code.md)

### 2. What happens when Claude Code reaches its context window limit?

- It switches to a smaller, faster model to save memory
- It removes your oldest files to make room for new ones
- ✅ **It automatically compacts your conversation to free up space**
- It stops working and asks you to restart the session

**Por qué.** La compactación **resume los detalles importantes y elimina resultados de tools innecesarios**. No cambia de modelo ni borra por antigüedad, y **puede perder detalles** en el proceso. → [capítulo 06](06-gestion-del-contexto.md)

### 3. What is the recommended workflow for using Claude Code effectively?

- Code → Test → Deploy → Monitor
- ✅ **Explore → Plan → Code → Commit**
- Write → Review → Merge → Ship
- Prompt → Accept → Push → Repeat

**Por qué.** Es *la* idea del curso: «si te llevas una sola cosa, que sea este flujo». Los distractores son ciclos de despliegue o de git que suenan igual de plausibles pero no son el del curso. → [capítulo 05](05-explore-plan-code-commit.md)

### 4. How does Claude Code use the CLAUDE.md file?

- It reads it only after you run the `/init` command
- It reads it once when you first create the project
- ✅ **It reads it automatically at the start of every session**
- It only reads it when you explicitly ask it to

**Por qué.** El contenido de CLAUDE.md **se añade a tu prompt** en cada sesión: por eso es memoria persistente. `/init` solo sirve para **generarlo**, no para que se lea. → [capítulo 08](08-el-fichero-claude-md.md)

### 5–7. No evaluables

Encuesta de satisfacción (escala de 5), NPS (escala de 5) y un campo de texto libre («Is there any feedback you'd like to provide…»). El texto libre **es obligatorio** para poder enviar el quiz.

---

## Parte 2 · Banco extra

El quiz oficial solo toca 4 conceptos. Estas atacan lo que deja fuera.

**1.** En auto-accept mode, ¿qué sigue requiriendo tu aprobación?
<details><summary>Respuesta</summary>

**Los comandos.** Auto-accept aprueba automáticamente las **ediciones de fichero**, pero los comandos de shell siguen pasando por ti. → cap. 02 y 04
</details>

**2.** ¿Qué combinación de teclas cicla entre modos de permisos?
<details><summary>Respuesta</summary>

**`Shift + Tab`**. Plan Mode está dentro de ese mismo menú. → cap. 04
</details>

**3.** ¿Qué puede hacer Claude en Plan Mode y qué no?
<details><summary>Respuesta</summary>

**Puede leer** ficheros y hacer búsquedas web con tools de **solo lectura**, y hace preguntas aclaratorias. **No puede editar ficheros.** → cap. 04 y 05
</details>

**4.** ¿Cuál es la diferencia entre `/compact` y `/clear`?
<details><summary>Respuesta</summary>

`/compact` **resume** todo lo anterior y **conserva memoria** de lo trabajado — para seguir con la misma funcionalidad. `/clear` **lo elimina todo** — para empezar una funcionalidad nueva sin sesgo previo. → cap. 06
</details>

**5.** ¿Qué muestra `/context`?
<details><summary>Respuesta</summary>

Una vista general del **tamaño de tu contexto**, las **categorías que más ocupan** y un **gráfico visual** del desglose. → cap. 06
</details>

**6.** Un prompt vago, ¿ahorra o gasta contexto?
<details><summary>Respuesta</summary>

**Gasta más.** Sin instrucciones claras Claude explora más código y razona más por su cuenta, y eso ocupa mucho más que un prompt detallado. → cap. 06
</details>

**7.** ¿Por qué la revisión de código la debe hacer un subagente y no el agente principal?
<details><summary>Respuesta</summary>

Porque el subagente corre en **su propia ventana de contexto con ojos frescos** y **no arrastra el sesgo** del agente que acaba de escribir ese código. Además conviene **restringirlo a tools de solo lectura**: un revisor señala, no edita. → cap. 05 y 07
</details>

**8.** ¿Qué hace `claude --from-pr <PR_NUMBER>`?
<details><summary>Respuesta</summary>

**Retoma la sesión enlazada a ese PR.** Cuando Claude crea un PR con `gh pr create`, la sesión queda enlazada automáticamente. → cap. 07
</details>

**9.** ¿Cómo referencias un fichero de documentación desde CLAUDE.md?
<details><summary>Respuesta</summary>

Con el símbolo **`@`** y la ruta: `@README.md`. → cap. 08
</details>

**10.** ¿Dónde vive el CLAUDE.md de proyecto y dónde el de usuario, y para quién es cada uno?
<details><summary>Respuesta</summary>

**Proyecto:** en la raíz del repositorio, **compartido con el equipo**. **Usuario:** en tu carpeta de configuración, **solo para ti** y aplicando a **todos** tus proyectos. → cap. 08
</details>

**11.** El curso recomienda empezar un proyecto **sin** CLAUDE.md. ¿Por qué?
<details><summary>Respuesta</summary>

Para **ver dónde tienes que corregir el rumbo constantemente** y que el fichero salga **compacto y centrado** solo en lo necesario. Luego `/init` lo genera. → cap. 08
</details>

**12.** ¿Qué comando crea un subagente y qué clave precarga skills en él?
<details><summary>Respuesta</summary>

**`/agents`** → "Create new agent". La clave **`skill`**, listando las skills por nombre. Ahí **la skill entera se carga en contexto**, al contrario que en la conversación principal. → cap. 09
</details>

**13.** ¿Qué dos tipos de servidor MCP hay y qué distingue a cada uno?
<details><summary>Respuesta</summary>

**HTTP** para servicios **remotos** alojados por el proveedor, y **stdio** para **procesos locales** en tu máquina. → cap. 11
</details>

**14.** ¿Cuál de los tres alcances de MCP hace que todo tu equipo reciba los mismos servidores automáticamente?
<details><summary>Respuesta</summary>

**Project**, mediante un fichero **`.mcp.json`** versionado. Los otros dos son **local** (solo este proyecto, solo tú) y **user** (todos tus proyectos, solo tú). → cap. 11
</details>

**15.** ¿A partir de qué porcentaje de la ventana de contexto ocupado por tools de MCP cambia Claude Code a tool search mode?
<details><summary>Respuesta</summary>

**El 10 %.** Y el propio curso avisa de que ese modo **puede no funcionar de forma tan fiable**. → cap. 11
</details>

**16.** Tienes una tool de MCP para GitHub y también tienes `gh` instalado. ¿Qué es más eficiente en contexto?
<details><summary>Respuesta</summary>

**La CLI**, porque **no añade definiciones de tools persistentes** al contexto. → cap. 11
</details>

**17.** Enumera los cinco eventos de hooks.
<details><summary>Respuesta</summary>

**PreToolUse**, **PostToolUse**, **UserPromptSubmit**, **Stop** y **Notification**. → cap. 12
</details>

**18.** En un hook PreToolUse, ¿qué hace el código de salida 2 y dónde debe ir el mensaje?
<details><summary>Respuesta</summary>

**Bloquea la acción**, y el mensaje va a **stderr** — porque se le devuelve a Claude como feedback para que sepa por qué se le bloqueó. El 0 continúa; cualquier otro código es un **error no bloqueante**. → cap. 12
</details>

**19.** ¿Qué matcher se usa para que un hook de formateo se dispare en cualquier modificación de fichero?
<details><summary>Respuesta</summary>

`"Edit|MultiEdit|Write"`, sobre el evento **PostToolUse**. → cap. 12
</details>

**20.** ¿Qué variable de entorno usas en un hook para referenciar scripts de tu proyecto?
<details><summary>Respuesta</summary>

**`CLAUDE_PROJECT_DIR`**, para que funcionen independientemente del directorio de trabajo actual de Claude. → cap. 12
</details>

**21.** ¿Qué método de instalación en terminal **no** soporta auto-actualizaciones?
<details><summary>Respuesta</summary>

**Homebrew** (`brew install`) en macOS/Linux, y **winget** en Windows. El script de `curl` sí se auto-actualiza. → cap. 03
</details>

**22.** ¿Qué alcance de ficheros tiene Claude Code al arrancar?
<details><summary>Respuesta</summary>

**El directorio donde ejecutas `claude` y todas sus subcarpetas.** → cap. 03
</details>

**23.** ¿Qué limitación tiene Claude Code en la web frente al terminal?
<details><summary>Respuesta</summary>

Está **restringido a repositorios de GitHub**. Y las funcionalidades **llegan antes al terminal**. → cap. 03
</details>

**24.** Skill vs. servidor MCP: ¿qué se carga en contexto de cada uno al arrancar?
<details><summary>Respuesta</summary>

Del servidor MCP, **todas las definiciones de tools**. De la skill, **solo nombre y descripción**; el contenido completo se carga **cuando Claude decide que la necesita**. → cap. 10 y 11
</details>
