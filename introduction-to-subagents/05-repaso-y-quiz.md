# 05 — Repaso y autoevaluación

> Este curso **no tiene quiz oficial** en Skilljar: son 4 lecciones y se acaba. Lo que sigue es una autoevaluación construida a partir del material, con el mismo estilo de escenario que usa Anthropic en sus otros cursos.

---

## Chuleta

### Qué es un subagente

- **Una ventana de contexto separada.** Recibe **dos cosas**: un **system prompt** (de tu fichero de config) y una **descripción de tarea** (escrita por el agente padre).
- Trabaja solo y **devuelve únicamente un resumen**. **Su conversación completa se descarta.**
- **El trato:** ganas contexto principal limpio; **pierdes visibilidad** de cómo llegó ahí.

### Los tres integrados

| Subagente | Para qué |
|---|---|
| **General purpose** | Multipaso, con exploración **y** acción |
| **Explore** | Búsqueda y navegación rápidas |
| **Plan** | Investigación y análisis en plan mode, antes de presentar el plan |

### Crear uno

- Comando **`/agents`** → **Create new agent**.
- **Ámbito:** project-level (solo este proyecto) o user-level (todos los proyectos de la máquina).
- **Recomendado: que lo genere Claude** a partir de tu descripción, no escribirlo a mano.
- Categorías de herramientas: read-only, edit, execution, MCP, other.
- Se guarda en **`.claude/agents/nombre.md`**.
- **Modelos:** `haiku` (rápido/ligero) · `sonnet` (término medio) · `opus` (análisis complejo) · `inherit` (el de la conversación principal).

### Los campos del frontmatter

| Campo | Clave |
|---|---|
| `name` | Identificador. Lo invocas con **`@agent nombre`** |
| `description` | **Una sola línea** (`\n` escapado para saltos). Controla **cuándo** se usa **y moldea el prompt de entrada** |
| `tools` | Editable a mano en cualquier momento |
| `model` | `sonnet` / `opus` / `haiku` / `inherit` |
| `color` | Identificación visual en la interfaz |

- **El cuerpo del markdown, bajo el frontmatter, es el system prompt.**
- Para que Claude delegue solo: incluye **`proactively`** en la description.
- Si no se dispara cuando esperas: **el problema está en la description** — añade ejemplos y escenarios de disparo más específicos.

### El doble papel de la description

1. `name` + `description` de **todos** los subagentes disponibles van **en el system prompt del agente principal** → deciden **cuándo** se lanza.
2. El agente principal **usa la description como guía para escribir el prompt de entrada** → decide **qué se le manda hacer**.

Ejemplos de esta técnica:
- *"You must tell the agent precisely which files you want it to review"* → el prompt de entrada listará ficheros concretos en vez de un vago "usa git diff".
- *"return sources that can be cited"* en un subagente de búsqueda web → el principal incluye esa instrucción al delegar.

### Las 4 características de un subagente eficaz

1. **Description específica** — dirige el cuándo y el qué.
2. **Formato de salida definido** — *la mejora individual más importante*. Da **puntos de parada naturales** y **evita que corra de más**.
3. **Sección de obstáculos** — setup, workarounds, flags especiales, dependencias problemáticas. Si no lo pides en el formato, **el hilo principal lo redescubre gastando tiempo y tokens**.
4. **Herramientas limitadas** — evita efectos secundarios y clarifica roles.

| Tipo | Herramientas |
|---|---|
| Investigación / solo lectura | `Glob`, `Grep`, `Read` |
| Revisor de código | + `Bash` (para `git diff`), **sin `Edit`/`Write`** |
| Estilos / modificación | + `Edit`, `Write` |

### Cuándo sí

- **Investigación** — el principal necesita *dónde* está el JWT, no los 30 ficheros leídos.
- **Revisión de código** — Claude revisa mejor cuando el código **se le presenta como escrito por otro**. Un hilo que construyó la feature da feedback flojo sobre ella.
- **System prompt a medida** — copywriting (tono/audiencia, frente al sesgo técnico conciso del prompt por defecto) y estilos (apuntarlo a los ficheros del design system, que se cargan solos en su contexto).

### Cuándo no — los tres antipatrones

| Antipatrón | Por qué falla |
|---|---|
| **Reclamos de experto** | *"You are a Python expert"* no aporta nada: Claude **ya** tiene ese conocimiento |
| **Pipelines secuenciales** | Funcionan solo si las tareas son **realmente independientes**. Reproducir→depurar→arreglar falla porque cada paso depende del anterior; **la información se pierde en el traspaso** |
| **Test runners** | **Ocultan la salida que necesitas** para diagnosticar. Devolver *"tests failed"* te obliga a scripts de depuración extra. **Fue la configuración con peor rendimiento de todas las probadas** |

### La regla de decisión

> **¿Importa el trabajo intermedio?** No → delega. Sí → hilo principal.

---

## Quiz de autoevaluación — 10 preguntas

Tapa las respuestas.

1. Un subagente recibe exactamente dos cosas al arrancar. ¿Cuáles?
2. ¿Qué pasa con la conversación de un subagente cuando termina?
3. ¿Cuál es el precio que pagas por delegar a un subagente?
4. ¿Cuál de los integrados usarías para navegar rápido por un codebase desconocido?
5. Tu subagente revisor no se dispara nunca solo. ¿Qué campo tocas y qué palabra añades?
6. Además de decidir *cuándo* se lanza un subagente, ¿qué otra cosa hace la `description`?
7. ¿Cuál es la mejora individual más importante que puedes hacerle a un subagente, y qué dos problemas resuelve?
8. Un subagente descubrió que cierto comando necesitaba un flag raro. ¿Cómo te aseguras de enterarte?
9. ¿Qué herramientas le das a un revisor de código, y cuáles le niegas?
10. Quieres tres subagentes encadenados: reproducir bug → depurar → arreglar. ¿Buena idea?

<details>
<summary>Respuestas</summary>

1. **Un system prompt** (de su fichero de configuración) y **una descripción de tarea** escrita por el agente padre a partir de lo que pediste.
2. **Se descarta entera.** Solo vuelve el resumen al hilo principal.
3. **Visibilidad.** Pierdes ver cómo llegó a sus conclusiones; los hallazgos vienen comprimidos en un resumen.
4. **Explore** — búsqueda y navegación rápidas. (*General purpose* es para multipaso con exploración y acción; *Plan* es el de plan mode.)
5. La **`description`**, añadiendo **`proactively`**. Y si sigue sin dispararse, más **ejemplos concretos y escenarios de disparo**.
6. **Moldea el prompt de entrada** que el agente principal escribe al lanzarlo. Controla el *cuándo* **y** el *qué se le manda hacer*.
7. **Definir un formato de salida** en el system prompt. Resuelve: (a) le da **puntos de parada naturales** — sabe que terminó al rellenar cada sección; (b) **evita que corra demasiado tiempo**, que es el fallo típico sin salida definida.
8. **Pidiéndolo explícitamente en el formato de salida**, con una sección **"Obstacles Encountered"**: setup, workarounds, comandos con flags especiales, dependencias problemáticas. Si no lo pides, el hilo principal lo redescubre.
9. Le das **`Bash`** (para `git diff` y ver qué cambió) más las de lectura. Le niegas **`Edit` y `Write`**: su trabajo es analizar, no cambiar.
10. **No.** Antipatrón de pipeline secuencial: solo funciona si las tareas son realmente independientes, y arreglar bugs casi nunca lo es — cada paso depende de lo que descubrió el anterior y **la información se pierde en el traspaso**. Ese trabajo va en el hilo principal.

</details>
