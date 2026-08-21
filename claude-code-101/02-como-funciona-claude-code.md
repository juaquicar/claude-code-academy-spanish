# 02 — Cómo funciona Claude Code

*10 minutos* · [Vídeo](https://www.youtube.com/embed/6bs5b4FltCU)

**Al terminar sabrás:** los cinco pasos del bucle agéntico · qué es la ventana de contexto y qué pasa cuando se llena · qué son las tools y por qué son la columna vertebral · los tres modos de permisos.

---

Claude Code es distinto de una aplicación de chat típica. Entender cómo funciona por dentro te permite usarlo mejor.

## El bucle agéntico

La mejor forma de explicar Claude Code es a través del **bucle agéntico**:

1. **Escribes un prompt** en Claude Code.
2. **Claude reúne el contexto que necesita** interactuando con el modelo, que devuelve texto o una llamada a una tool que Claude Code puede ejecutar.
3. **Actúa** — por ejemplo, editando un fichero o ejecutando un comando.
4. **Verifica los resultados** y determina si cumplen lo que tu prompt pedía.
5. Si lo cumplen, **Claude termina** y espera el siguiente prompt. Si no, **vuelve al bucle** y lo intenta de nuevo hasta que el resultado esté completo y sea verificable.

Durante todo el bucle **puedes añadir contexto, interrumpir o redirigir al modelo** para guiarlo hacia tu objetivo.

## Contexto

Claude tiene una **ventana de contexto** que determina cuánto puede almacenar y referenciar de tu conversación, el contenido de los ficheros, la salida de los comandos y demás.

Cuando alcanzas ese límite, **Claude Code compacta tu conversación**: determina automáticamente qué puede eliminar o resumir para devolver la ventana de contexto a un tamaño usable.

> **Trampa de examen.** Al llegar al límite **no** cambia a un modelo más pequeño, **ni** borra tus ficheros más antiguos, **ni** deja de funcionar pidiéndote reiniciar la sesión. **Compacta automáticamente la conversación.** Es la pregunta 2 del quiz oficial.

## Tools

**Las tools son la columna vertebral del funcionamiento de los agentes.** La mayoría de asistentes de IA sencillamente toman texto y devuelven texto. Las tools le permiten a Claude Code determinar **cuándo** ejecutar código para acercarse a completar una tarea.

Puede ser una tool de lectura de ficheros, una de búsqueda web o cualquier otra capacidad. Claude Code usa **comprensión semántica** para decidir cuándo llamar a una tool y cómo usar su salida.

## Permisos

Claude Code tiene varios modos de permisos:

| Modo | Qué hace |
|---|---|
| **Default behavior** | Claude pide **permiso explícito** antes de editar un fichero o ejecutar un comando de shell |
| **Auto-accept** | Los ficheros se editan sin preguntar, pero **los comandos siguen requiriendo aprobación** |
| **Plan mode** | Usa **tools de solo lectura** para elaborar un plan de acción antes de empezar el trabajo |

Todo esto se configura en tu fichero de settings.

> **Cuidado al saltarte los permisos.** Darle a Claude Code barra libre para ejecutar comandos significa que un error puede ser más difícil de pillar antes de que ocurra.

## Conclusiones

Claude Code combina varios conceptos agénticos: un **bucle agéntico**, una **ventana de contexto gestionada**, **tools** y **permisos configurables** — todo dentro de tu terminal. Puede leer tu base de código, actuar y verificar su propio trabajo. Eso es lo que lo hace fundamentalmente distinto de una ventana de chat.
