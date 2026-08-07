# 06 — Routines y modo headless (Routines and Headless)

Sección: *Automate Repeat Work* · [Vídeo](https://www.youtube.com/embed/b9TCW-pdzDA)

Cuando ya confías en Claude para una tarea, el siguiente paso es dejar de hacerla a mano. Si es el mismo prompt sobre un disparador recurrente, no deberías tener que lanzarlo tú cada vez.

**Espectro:** en un extremo, **routines** sobre infraestructura gestionada de Anthropic (no construyes nada). En el otro, **modo headless** y **Agent SDK**, que ejecutan Claude Code desde tu propio código (control total).

## Routines: un prompt guardado que corre en la nube

Un routine es la forma más directa de automatizar. Sin script y sin servidor. Empaqueta tres cosas y las ejecuta en la nube cuando se dispara:

1. Un **prompt**
2. El **repositorio** sobre el que trabaja
3. Los **connectors** que necesite

La infraestructura es de Anthropic: no hay máquina tuya encendida toda la noche ni fichero de workflow que mantener.

### Disparadores

- **Cron**, p. ej. cada mañana a las 9:00
- **HTTP POST** a su endpoint de API, para que tu propio código lo lance
- **Evento de GitHub**, p. ej. un pull request nuevo

Buenos candidatos: auditoría matinal de dependencias, un triador de PRs que se dispara al llegar un PR nuevo, un escaneo diario de tickets de Sentry para saber qué es más urgente.

### Dos formas de crearlo

Desde la web en `claude.ai/code/routines`: nombre, instrucciones de qué debe hacer Claude en cada sesión, repositorio y disparador.

O desde dentro de Claude Code sin salir del terminal:

```
/schedule daily dependency audit at 9am
```

Misma idea, dos puertas de entrada.

### Tres límites que debes conocer antes de depender de routines

1. **Son research preview.** El comportamiento y los límites van a seguir moviéndose.
2. **Un horario recurrente corre como mucho cada hora.** Si necesitas más frecuencia, routines no es la herramienta.
3. **Cada run arranca desde un clon fresco de tu rama por defecto y solo puede hacer push a ramas con prefijo `claude/`** (salvo que lo relajes por repo). Ese es el guardarraíl que impide que un run autónomo reescriba main.

## Modo headless: cuando necesitas tu propio entorno

Cuando el trabajo necesita *tu* entorno, o lógica envolviendo el run.

El núcleo es el flag **`-p`** (abreviatura de `--print`). Ejecuta Claude Code como comando one-shot sin UI interactiva. Lee de stdin y escribe a stdout, así que se canaliza como cualquier herramienta de shell:

```bash
claude -p "summarize the changes in this diff"
```

> ⚠️ **Importante:** `-p` **se salta el auto-descubrimiento** de hooks, skills, plugins, servidores MCP y el fichero CLAUDE.md. Obtienes Claude más las herramientas que permitas explícitamente, y nada de lo que el entorno local cargue por su cuenta. **A cambio, el arranque es mucho más rápido.**

### Salida estructurada

Empareja un **JSON schema** con el formato de salida JSON y Claude restringe su salida a tu esquema. El objeto aterriza en el campo **`structured_output`** de la respuesta JSON, así que lo sacas con `jq`:

```bash
claude -p "Extract the exported function names from src/core/style.js" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output.functions'
```

### Automatización multipaso con sesiones

No hay que meterlo todo en un comando. Captura el `session_id` de la salida JSON y reanuda después:

```bash
claude --resume "$(jq -r .session_id /tmp/plan.json)"
```

Un script arranca el trabajo, otro lo reanuda más tarde con contexto completo. Útil cuando la primera pasada produce un plan y la segunda lo ejecuta.

### Runs deterministas para CI

El flag **`--bare`** da modo determinista. Es la elección correcta cuando ejecutas Claude Code dentro de un pipeline y quieres salida repetible y predecible en vez de algo que varíe entre runs.

## El Agent SDK: Claude Code dentro de tu app

Último escalón del espectro: una librería que embebe Claude Code en tus aplicaciones **TypeScript o Python**.

Ambos lenguajes exponen una función **`query`** y las mismas primitivas que la CLI. Le pasas un prompt más opciones:

- `allowedTools` para controlar qué puede hacer Claude
- un system prompt
- un permission mode

Luego iteras sobre los mensajes que Claude devuelve en streaming y los manejas como tu app necesite. Mismo motor que la CLI, invocable desde dentro de tu producto.

## Guía rápida de decisión

| Necesidad | Herramienta |
|---|---|
| Trabajo repetitivo, por defecto | **Routines** — infraestructura de Anthropic, nada que hospedar |
| El job necesita tu pipeline y quieres canalizar datos por un script | **Headless con `-p`** |
| CI necesita los mismos resultados cada run | **`--bare`** |
| El trabajo pertenece dentro de tu propio producto | **Agent SDK** |

**Empieza por routines. Baja por el espectro solo cuando el trabajo realmente necesite el control extra.**
