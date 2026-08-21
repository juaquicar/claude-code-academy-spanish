# 06 — Gestión del contexto

*15 minutos* · [Vídeo](https://www.youtube.com/embed/eW3oTyfeWZ0)

**Al terminar sabrás:** qué consume contexto · qué es la compactación y qué se pierde en ella · cuándo `/compact`, cuándo `/clear` y para qué `/context` · los tres trucos para gastar menos contexto.

---

> **El contexto es la memoria de trabajo de Claude.** Cada fichero que lee, cada comando que ejecuta, cada mensaje que envías — todo ocupa espacio en la ventana de contexto.

## Qué es la ventana de contexto

Piénsala como la cantidad de espacio que Claude puede mantener en su memoria. Cuando escribes un prompt, cuando Claude lee un fichero, cuando ejecuta una llamada a una tool o recibe su resultado, **todo se suma a la ventana de contexto**. Como el espacio es finito, **optimizar cómo lo usas se vuelve importante**.

## Qué pasa cuando se llena

Al acercarte al límite, la ventana de contexto se **compacta automáticamente**. La compactación **resume los detalles importantes y elimina resultados de llamadas a tools innecesarios** para liberar espacio.

> **Ojo:** este proceso **puede perder detalles**.

## Comandos

| Comando | Qué hace |
|---|---|
| **`/compact`** | Compacta manualmente todo lo anterior a ese punto. Libera espacio **conservando memoria de lo que trabajaste** |
| **`/clear`** | Empieza de cero **sin memoria** de la sesión anterior. Lo elimina todo |
| **`/context`** | Muestra el estado de tu contexto: tamaño, qué categorías ocupan más y un gráfico visual del desglose |

## Cuándo usar cuál

Regla general:

- **Usa `/compact`** cuando estás trabajando en una funcionalidad concreta, chocas con el límite de contexto y **necesitas continuar**. Mantener el contexto relevante para tu funcionalidad actual es importante.
- **Usa `/clear`** cuando quieres **empezar una funcionalidad nueva**. No quieres que la conversación anterior introduzca sesgo en algo nuevo.

> Para las cosas que quieres que Claude recuerde **entre sesiones**, ponlas en tu fichero CLAUDE.md, así no tiene que redescubrirlas desde cero.

## Trucos para ahorrar contexto

**Sé específico.** Un prompt vago puede parecer más pequeño, pero **a la larga cuesta más contexto**. Sin instrucciones claras, Claude se ve obligado a explorar más tu base de código y razonar por su cuenta — lo que ocupa **mucho más espacio** que un prompt detallado.

> **Esto es lo contraintuitivo del capítulo:** escribir menos no ahorra contexto. Lo gasta.

**Gestiona tus servidores MCP.** Los servidores MCP **cargan todas sus tools disponibles en contexto por defecto**, aunque no las estés usando. Si tienes servidores configurados para cosas ajenas al proyecto actual, plantéate apagarlos. También puedes probar las **Skills**, que funcionan de forma parecida a los servidores MCP pero **no lo cargan todo en contexto de entrada**.

**Usa subagentes.** Los subagentes corren en paralelo con tu agente principal pero tienen una **ventana de contexto completamente separada**. Para tareas en las que solo necesitas la respuesta — como "¿dónde están los endpoints de autenticación?" — un subagente hace el trabajo y **devuelve solo un resumen** al agente principal, manteniendo limpio tu contexto primario.

## Conclusiones

Gestionar el contexto dentro de Claude Code es crucial. Usa `/compact` para resumir sesiones largas y `/clear` para empezar de cero. Para usar bien tu ventana de contexto: **sé específico con tus prompts, comprueba qué está consumiendo tu contexto actual y usa subagentes** para delegar tareas de las que solo necesitas el resultado.
