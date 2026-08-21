# 12 — Hooks

*15 minutos* · [Vídeo](https://www.youtube.com/embed/IkaPHiMDazM)

**Al terminar sabrás:** por qué un hook no es un prompt · los cinco eventos disponibles · cómo bloquear una tool con PreToolUse y qué significa cada código de salida · cómo compartirlos con tu equipo.

---

Los **hooks** te permiten ejecutar comandos en puntos concretos del ciclo de vida de Claude Code. La diferencia clave entre los hooks y todo lo demás que cubre este curso es que **los hooks son deterministas: siempre se ejecutan**.

## Por qué usar hooks

Puedes decirle a Claude en tu CLAUDE.md que ejecute Prettier después de cada edición de fichero. **La mayoría de las veces lo hará. Pero a veces no.** Un hook hace que ocurra **todas y cada una de las veces, sin excepciones**.

Casos de uso habituales:

- **Auto-formatear** después de editar ficheros
- **Registrar** todos los comandos ejecutados, para cumplimiento normativo
- **Bloquear operaciones peligrosas**, como modificar ficheros de producción
- **Enviarte notificaciones** cuando Claude termina una tarea

## Cómo funcionan

Los hooks se configuran en tu **`settings.json`**. Eliges un **evento**, opcionalmente pones un **matcher** para indicar a qué tools aplica, y das un **comando** a ejecutar.

Los eventos disponibles son:

| Evento | Cuándo se dispara |
|---|---|
| **PreToolUse** | Antes de una llamada a una tool |
| **PostToolUse** | Después de que una llamada a una tool se complete |
| **UserPromptSubmit** | Cuando envías un prompt, **antes de que Claude lo procese** |
| **Stop** | Cuando Claude termina de responder |
| **Notification** | Cuando Claude envía una notificación |

Se configuran con el comando **`/hooks`** dentro de Claude Code, o editando `settings.json` directamente.

## Un ejemplo práctico

El hook más común: **auto-formatear tras las ediciones**. Pon un hook **PostToolUse** con un matcher `"Edit|MultiEdit|Write"` para que se dispare siempre que Claude modifica un fichero. El comando comprueba la extensión del fichero y ejecuta el formateador adecuado — Prettier para TypeScript, gofmt para Go, lo que use tu proyecto.

## Bloquear con PreToolUse

Los hooks **PreToolUse pueden bloquear llamadas a tools antes de que se ejecuten**. Tu hook recibe **el nombre de la tool y su entrada como JSON por stdin**. El **código de salida** determina el comportamiento:

| Código de salida | Comportamiento |
|---|---|
| **0** | Continúa normalmente |
| **2** | **Bloquea la acción.** El mensaje de **stderr se le devuelve a Claude como feedback**, para que sepa por qué se le bloqueó y pueda ajustarse |
| **Cualquier otro** | Error **no bloqueante**: se te muestra, pero no detiene nada |

> **El detalle que se olvida:** el código de bloqueo es el **2**, no el 1. Y el mensaje útil va a **stderr**, porque es lo que Claude lee.

Así se imponen reglas duras. Bloquear escrituras en un directorio de configuración de producción. Bloquear comandos bash que contengan `rm -rf`. Bloquear commits a main. Lo que tu equipo necesite que esté **garantizado, no sugerido**.

## Compartir hooks con tu equipo

Los hooks configurados en **`.claude/settings.json`** son de **nivel proyecto** y se pueden versionar en tu repositorio. Así todo tu equipo obtiene los mismos hooks automáticamente.

Usa la variable de entorno **`CLAUDE_PROJECT_DIR`** en tus comandos para referenciar scripts guardados en tu proyecto, **de modo que funcionen independientemente del directorio de trabajo actual de Claude**.

## Conclusiones

Los hooks te dan control determinista sobre el comportamiento de Claude Code. Usa **PostToolUse** para auto-formateo y logging. Usa **PreToolUse** para bloquear operaciones peligrosas. Configúralos con `/hooks` o en `settings.json`. Y **versiónalos en tu repositorio** para que tu equipo los tenga también.

> **Si algo tiene que pasar siempre y sin fallo, no lo pongas en un prompt. Ponlo en un hook.**
