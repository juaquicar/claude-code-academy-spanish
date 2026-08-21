# 11 — ¿Qué son los agentes gestionados?

*20 minutos* · [Vídeo](https://www.youtube.com/embed/haeslvB0zpg)

**Al terminar sabrás:** qué te quita de encima un agente gestionado · tres formas reales de usarlos · qué son las rúbricas y los graders · los ocho bloques de construcción.

---

**Claude Managed Agents** es un conjunto de APIs para **construir y desplegar agentes a escala**. Defines agentes con tools, personas y capacidades concretas. Configuras entornos sandbox con los paquetes y controles de red adecuados. Luego **lanzas sesiones desde tu propia aplicación**, y Claude hace el trabajo **dentro de un contenedor aislado** con acceso completo al sistema de ficheros, ejecución de bash y búsqueda web.

## El bucle del agente, alojado por ti… o por ellos

Por dentro esto es **un bucle de agente**: Claude razona, llama a una tool, lee el resultado y repite hasta que el trabajo está hecho. Si ya has construido agentes, probablemente has escrito ese bucle tú mismo.

> **Managed agents coge ese mismo bucle y lo aloja en la infraestructura de Anthropic, para que no tengas que ejecutarlo tú.**

Managed Agents tiene su propia sección en la **Claude Console**.

## Ejemplo 1 · Un tablero Kanban que hace el trabajo

Imagina un tablero Kanban montado sobre managed agents. **Arrastras un ticket a la columna "in progress" y eso dispara una sesión** automáticamente. Digamos que el ticket dice "optimize website performance":

1. Tu backend **crea una sesión**.
2. La sesión apunta a un **entorno** que configuraste con **Lighthouse y Puppeteer preinstalados**.
3. **Tu repositorio de GitHub se monta** en el contenedor.

Ahora Claude tiene el código, las tools y una **rúbrica** que define qué significa "hecho":

- Puntuación de Lighthouse **por encima de 90**
- **Sin recursos que bloqueen el renderizado**
- **Todas las imágenes con lazy load**

Claude ejecuta la auditoría y empieza a comprimir imágenes, meter CSS inline y diferir scripts. **Cada llamada a tool vuelve al tablero en tiempo real por el event stream**, así que ves el trabajo mientras ocurre.

Entonces entra la rúbrica. **Un grader separado, corriendo en su propia ventana de contexto**, evalúa la salida contra tus criterios. Claude lee ese feedback, **vuelve a entrar, arregla lo que se dejó y reenvía**. En la demo, ese bucle sube la puntuación de Lighthouse **hasta 96**.

Una cosa más: **puedes arrastrar un segundo ticket mientras el primero sigue corriendo**. Dos sesiones, dos contenedores, dos tareas en paralelo.

## Ejemplo 2 · Un agente de investigación recurrente con memoria

Otra forma de agente: uno cuyo trabajo es **seguir precios y cambios de plan** en cada herramienta SaaS que paga tu empresa, con un informe listo antes del stand-up.

En cada ejecución, el agente:

- Busca en la web las páginas de precios actuales, comprueba cambios de tier y **señala funcionalidades nuevas** que puedan afectar a tus contratos
- Ejecuta un **análisis de costes en Python** dentro del sandbox
- Usa una **skill de hoja Excel** y escribe un resumen ejecutivo
- **Publica un enlace en Slack y crea una tarea de revisión en Asana**, ambas vía **servidores MCP**

El agente además **lee y escribe en un almacén de memoria**. Antes de empezar, consulta qué encontró la semana pasada. Al terminar, guarda qué cambió. Así el informe del lunes siguiente puede decir **"los costes de cómputo son un 15 % más bajos que la semana pasada"** en vez de listar los mismos precios estáticos cada vez.

## Ejemplo 3 · Respuesta a incidentes con varios agentes

Salta una alerta de tu stack de monitorización. Una **tool personalizada** en tu backend recibe el payload y lo mete en una sesión nueva **como un tool result**. Esta sesión usa **coordinación multi-agente**:

- Un **agente coordinador** recibe la alerta y **delega en tres especialistas**.
- **Cada especialista corre en su propia ventana de contexto**, sobre **el mismo sistema de ficheros compartido**.
- Los especialistas reportan de vuelta y el coordinador **sintetiza sus hallazgos** en un único resumen de incidente.

Antes de que el resumen llegue a Slack, se dispara la **política de permisos**: ves el borrador en pantalla, lo apruebas y el mensaje sale. **Las acciones sensibles esperan a un humano.**

**La memoria lo ata todo.** El coordinador consulta incidentes pasados y señala un patrón: *"esto se parece al problema de resolución de DNS de hace dos semanas, causado por un TTL mal configurado."* La próxima vez que salte una alerta parecida, el agente **arranca con ese contexto** en vez de diagnosticar de cero.

## Los bloques de construcción

| Bloque | Qué es |
|---|---|
| **Agents** | Definiciones con tools, personas y capacidades concretas |
| **Sessions** | Ejecuciones individuales que lanzas desde tu aplicación |
| **Environments** | Sandboxes con los paquetes y controles de red adecuados |
| **Tools** | Incluidas **tools personalizadas en tu backend** |
| **MCP** | Conexiones a servicios como Slack y Asana |
| **Memory** | Un almacén que el agente **lee antes de empezar y escribe al terminar** |
| **Outcomes** | **Rúbricas y graders** que definen y comprueban qué es "hecho" |
| **Multi-agent coordination** | Coordinadores delegando en especialistas |

## Conclusiones

- **Claude Managed Agents** es un conjunto de APIs para construir y desplegar agentes a escala, **alojados en la infraestructura de Anthropic**.
- Ejecuta el bucle de agente de siempre — razonar, llamar a una tool, leer el resultado, repetir — **dentro de un contenedor aislado** con sistema de ficheros, bash y búsqueda web.
- Las sesiones corren en **entornos que tú configuras**, **funcionan en paralelo** y **transmiten las llamadas a tools a tu app en tiempo real**.
- **Rúbricas y graders separados** te dejan definir criterios de éxito; **Claude itera hasta cumplirlos**.
- Memoria, servidores MCP, tools personalizadas, políticas de permisos y coordinación multi-agente completan la experiencia de agente con estado.
- **Tú defines qué significa "hecho". Claude trabaja hasta llegar ahí.**
