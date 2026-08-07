# 05 — Hooks

Sección: *Configure Claude* · [Vídeo](https://www.youtube.com/embed/8ALu1dk681s)

**El problema:** decirle algo a Claude en CLAUDE.md es una *petición*, no una *garantía*. Escribes "always format after editing" y normalmente hará caso. *Normalmente*. En un run largo que no estás mirando, "normalmente" no basta.

**Un hook es código determinista que corre en un punto fijo del bucle**, así que puede *garantizar* comportamiento en vez de esperarlo. Convierte una regla de "Claude suele hacer caso" en "Claude no puede saltársela".

## Los eventos de hook

Claude Code dispara **~30 eventos de hook** por sesión. No hace falta conocerlos todos. Los que importan:

| Evento | Cuándo dispara | Uso típico |
|---|---|---|
| **PreToolUse** | Antes de una llamada a herramienta | **Primitiva de enforcement.** La única que puede parar algo antes de que ocurra. |
| **PostToolUse** | Tras una llamada a herramienta con éxito | Auto-formateo, auto-lint |
| **Stop** | Cuando Claude quiere terminar su turno | Puedes negarte: "no, no has terminado". Existe **SubagentStop** para sub-agentes. |
| **PreCompact / PostCompact** | Antes y después de la compactación | — |
| **InstructionsLoaded** | Cuando carga un CLAUDE.md o fichero de reglas | Auditar qué entró realmente en contexto |
| **SessionStart** | Al inicio de sesión | Preparar el entorno. Usa el source `startup` si solo lo quieres en arranques frescos. |

> ⚠️ **Trampa clásica:** para re-inyectar contexto después de una compactación, **no uses PostCompact**. Usa **SessionStart con el matcher `compact`**. Ese es el que realmente devuelve su salida a la conversación.

## PreToolUse: devolver una decisión como JSON

Aquí está el poder real: puede bloquear una llamada antes de que se ejecute. Le hablas a Claude **imprimiendo JSON y saliendo con código 0**. El campo clave es `permissionDecision`:

- `allow` — deja pasar la llamada
- `deny` — para la llamada
- `ask` — se lo devuelve al usuario para que decida

(Existe un cuarto valor, `defer`, pero solo aplica a runs no interactivos `-p` donde un proceso llamante pausa la herramienta y la reanuda luego. Rara vez lo usarás.)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "...",
    "updatedInput": {
      "command": "..."
    }
  }
}
```

**`updatedInput`**: en vez de bloquear la llamada, puedes **reescribirla**. Así redactas un secreto fuera de un comando bash y aun así lo dejas correr.

> ⚠️ **Pega:** `updatedInput` reemplaza el objeto de input **completo**. Tienes que devolver también los campos que no cambias, o los pierdes.

## Códigos de salida (para hooks que no devuelven JSON)

| Código | Significado |
|---|---|
| **0** | Éxito. Si stdout es JSON, Claude lo parsea. El texto plano se ignora en la mayoría de eventos — **excepto** en `SessionStart`, `UserPromptSubmit` y `UserPromptExpansion`, donde el texto plano **se añade al contexto**. Eso es lo que hace funcionar un hook preservador de estado. |
| **2** | **Error bloqueante.** stderr se le devuelve a Claude como contexto. Es el código de bloqueo en casi todas partes. |
| Cualquier otro | No bloqueante. stderr se registra y Claude sigue. |

> ⚠️ **El que pilla a todo el mundo: el código 1.** *Parece* un error, pero **no bloquea**. Claude ejecuta el comando igualmente. Si querías parar algo: **exit 2, no exit 1**.

Matices adicionales:

- `exit 2` puede incluso **bloquear `Stop`** — así le dices a Claude que no ha terminado.
- **PostToolUse** dispara *después* de que la herramienta ya corrió: bloquear ahí llega tarde para impedir la llamada, aunque sí puede devolver texto a Claude.
- Algunos eventos **ignoran el bloqueo por completo** (p. ej. `Notification` y `SessionStart`): muestran tu stderr y siguen igualmente.

## Guardarraíl real: redactar en vez de bloquear

Caso práctico: guardarraíl PreToolUse sobre la herramienta Bash. El **matcher** elige la herramienta a vigilar, y una cláusula **`if`** opcional la acota a un comando concreto.

- Movimiento obvio: devolver `deny` y parar una llamada peligrosa. Bien.
- Movimiento menos conocido y más interesante: devolver **`updatedInput`** para reescribir la llamada.

Ejemplo: Claude va a ejecutar un comando con un secreto de aspecto real. El hook lo intercepta, detecta el patrón `sk_live_` y lo sustituye por un placeholder antes de que el comando se ejecute.

→ El comando corrió. El trabajo se hizo. **El secreto nunca pasó.** Esa es la diferencia entre bloquear y redactar, y un hook lo aplica *todas* las veces.

## Preservar estado a través de una compactación

Cuando Claude compacta una conversación larga, tira mucho detalle. Un hook **SessionStart con el matcher `compact`** corre justo después de la compactación. Haz que imprima un resumen corto de los ficheros en los que estabas trabajando. Ese resumen vuelve al contexto → Claude retoma donde lo dejó en vez de arrancar en frío.

## Cierre

Los hooks convierten una regla que Claude *suele* seguir en una que *siempre* sigue. Ve más allá del auto-formateo: **guarda herramientas con PreToolUse, cierra el turno con Stop y preserva estado a través de un compact**. El montaje cuesta algo al principio y se paga la primera vez que pilla algo en un run que ni siquiera estabas mirando.
