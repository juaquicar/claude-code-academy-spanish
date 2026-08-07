# 10 — Quiz del curso

Sección: *Quiz* · Página: https://anthropic.skilljar.com/claude-code-in-action/487234

**Resultado: 8 de 8 correctas (100%) · 5 minutos. Curso superado.**

Estructura real: de las **11 preguntas**, **8 son puntuadas** y **3 son encuesta** (satisfacción, recomendación, comentario libre). Una pregunta por lección, salvo CLAUDE.md y hooks que se funden en la de "regla dura → hook".

---

## Las 8 preguntas reales

Todas son de escenario: te plantean una situación y eliges la herramienta. No preguntan datos sueltos, preguntan **decisiones**.

### 1 · Sabes describir el "hecho" mejor que los pasos

> Puedes describir exactamente qué significa "terminado" (todos los tests de un paquete pasan, el type checker da cero errores) mejor que enumerar los pasos para llegar. ¿Qué enfoque encaja?

✅ **Usar `/goal`** para fijar una condición de finalización, de modo que Claude siga trabajando hasta que un evaluador rápido la confirme.

> *Feedback oficial:* `/goal` fija una condición comprobable y mantiene a Claude trabajando entre turnos hasta cumplirla, en vez de parar la primera vez que cree haber terminado.

Distractores: plan mode (acota, no persigue una condición) · loop (reintervalo fijo, no condición de fin) · `/compact` dirigido (gestiona contexto, no finalización).

### 2 · Regla dura del equipo

> Vuestra regla dura: nunca hacer push a main. ¿Dónde vive para que Claude no pueda saltársela?

✅ **En un hook pre-tool-use que pare el push.**

> *Feedback oficial:* CLAUDE.md son instrucciones que Claude sigue, no configuración obligatoria; una regla dura pertenece a un hook, que detiene la acción incluso cuando Claude lo intenta.

Distractor fino: ponerla en CLAUDE.md **con `IMPORTANT`** sigue siendo mal — el énfasis sube prioridad, no garantiza nada.

### 3 · Procedimiento repetido con material pesado

> Has tecleado el mismo procedimiento multipaso más de una vez, e incluye material de referencia largo y un script auxiliar. ¿Cómo lo empaquetas?

✅ **Una skill, con `skill.md` magro**, empujando la profundidad a `reference.md` y a scripts que Claude ejecuta cuando hacen falta.

> *Feedback oficial:* un procedimiento repetido es una skill; la carpeta puede llevar ficheros de referencia que se leen solo cuando se necesitan y scripts que Claude ejecuta, así `skill.md` se queda magro.

Distractor fino: meterlo **todo inline en `skill.md`** "para que no se pierda nada" también es incorrecto.

### 4 · Auto mode escribe autenticación rota

> Pides en auto mode refactorizar la autenticación y escribe una autenticación rota. ¿Qué pasa realmente y qué añades?

✅ **El clasificador la deja pasar porque roto no es peligroso**; empareja auto mode con un **stop hook que lance tus tests**.

> *Feedback oficial:* el clasificador de auto mode guarda la intención (peligro), no la corrección, así que permite código roto-pero-seguro; un stop hook que corre los tests confirma que el código funciona de verdad.

### 5 · Auditoría diaria sin infraestructura tuya

> Quieres una auditoría de dependencias cada mañana a las 9, sin ninguna máquina tuya encendida y sin fichero de workflow que mantener.

✅ **Un routine con trigger cron**, corriendo en infraestructura de Anthropic.

> *Feedback oficial:* los routines corren con trigger cron en infraestructura de Anthropic, así que nada tuyo se queda encendido y no hay workflow que mantener.

Distractores: headless `-p` lanzado a mano · Agent SDK embebido en tu app · una sesión con bypass permissions toda la noche.

### 6 · Revisión de todos los PRs sin construir nada

> El equipo quiere que Claude revise cada pull request con comentarios inline, sin nada que construir ni hospedar, y no necesitáis que apruebe o bloquee el PR.

✅ **Code review gestionado a través de la Claude GitHub app.**

> *Feedback oficial:* el code review gestionado está hospedado por Anthropic, publica hallazgos inline rankeados a través de la GitHub app y nunca aprueba ni bloquea; la action es para trabajos que van más allá de revisar.

### 7 · Un job de CI corrió solo y dice que fue bien

> Un job corrió desatendido en CI y reporta éxito. ¿Cuál es el primer movimiento más fiable antes de enviarlo?

✅ **Empezar por el diff y `git diff`**, y confirmar que los tests pasaron de verdad en vez de que se afirme que pasaron.

> *Feedback oficial:* un resumen ordenado puede leerse bien mientras el diff tocó ficheros inesperados; la verificación arranca desde el diff y desde la evidencia de que los tests realmente pasaron, dimensionada a lo no supervisado que fue el run.

### 8 · Un plugin de la comunidad con una skill que quieres

> Un plugin de la comunidad te da una skill que quieres. ¿Qué haces antes de activarlo?

✅ **Inspeccionar cada hook, agente y servidor MCP que añade**, porque un plugin ejecuta código con tus privilegios y sus hooks disparan en cada llamada que haga match.

> *Feedback oficial:* un plugin ejecuta código con tus privilegios y sus hooks se apilan con los tuyos en cada llamada que haga match; revisado no es lo mismo que confiable, así que lee qué hace antes de activarlo.

Distractores, todos falsos: "los plugins no pueden cambiar el comportamiento por defecto" (sí pueden, vía la clave `agent`) · "pasó la revisión automatizada, luego es confiable" · "el namespacing me protege, un plugin no puede traer settings.json" (sí puede, aunque solo se honran 2 claves).

---

## Patrón para el próximo intento

Las 8 comparten forma: **escenario → elige la herramienta**. El distractor siempre es una herramienta *real y adyacente* usada en el sitio equivocado. Si sabes para qué existe cada pieza y qué la distingue de la de al lado, están todas.

---

## Chuleta de hechos "de examen"

Son los datos concretos y contraintuitivos que un quiz suele atacar.

### Sesiones largas

- Plan mode = **solo lectura**, investiga y propone.
- `/compact` **a secas es un error**: añade instrucciones detrás para dirigir el resumen.
- **Cada prompt del usuario crea un checkpoint.** Menú rewind: **doble `Esc`** con el prompt vacío.
- Rewind ofrece 5 opciones: restore code+conversation / restore conversation / restore code / **summarize from here** (lo posterior) / **summarize up to here** (lo anterior).
- `/goal` = condición de finalización; se cancela con `/goal clear`. **El evaluador solo lee el transcript** → la condición debe ser comprobable desde la salida.
- `loop` corre un prompt a intervalos entre turnos; se para con `Esc`.
- **`.worktreeinclude`** (raíz del repo) = lista de ficheros git-ignored a copiar en cada worktree. Un worktree limpio se borra solo al salir.

### CLAUDE.md

- Es **guía, no configuración obligatoria**. Cada línea compite con las demás.
- **4 ubicaciones, todas se cargan y se apilan**: managed policy (org, no excluible) / user / project / local (no versionado).
- Imports `@ruta/fichero.md` **se expanden inline al arrancar** → organizan, **NO reducen contexto**.
- Regla vaga vs. específica; **nombra el reemplazo** ("use named exports, not default exports").
- El **énfasis es un presupuesto**: `IMPORTANT`/`YOU MUST` solo funcionan por contraste.
- Regla dura ("never push to main") → **hook PreToolUse**, no CLAUDE.md.

### Skills

- Skill = carpeta con `skill.md` (nombre + **description que la dispara** + procedimiento).
- **Solo las descriptions se cargan en contexto** hasta que la skill se necesita → empaquetar sale gratis.
- La carpeta puede llevar `reference.md` (se lee bajo demanda) y **scripts que Claude ejecuta** (no se cargan en contexto).
- La skill de verificación debe comprobar **que no se debilitó ningún test para que pase**.
- Umbral: **si has tecleado la misma instrucción multipaso dos veces, es una skill.**

### Reparto de superficies

| Regla | Superficie |
|---|---|
| Convención permanente | `CLAUDE.md` |
| Procedimiento de un tipo de tarea | Skill |
| No se puede saltar | **Hook** |

### Modos de permisos (6)

| Modo | Clave |
|---|---|
| Manual | solo lee sin preguntar |
| Accept edits | lecturas + edits + bash común de FS |
| Plan | solo lectura, propone |
| **Auto** | acepta todo, **clasificador aparte revisa cada acción** |
| Don't ask | solo herramientas pre-aprobadas, resto auto-denegado sin prompt |
| Bypass permissions | sin chequeos = `dangerously-skip-permissions`, **solo en contenedor/VM** |

- `shift-tab` cicla manual → accept edits → plan → auto. Modo actual en la **barra de estado**.
- El clasificador **vigila intención, NO corrección**. Autenticación rota pasa, porque roto ≠ peligroso.
- Emparejamiento canónico: **auto mode (intención, antes) + stop hook con tests (corrección, después)**.
- **Don't ask** = pipelines desatendidos (CI, cron, lotes nocturnos).

### Hooks

- ~**30 eventos**. Los clave: **PreToolUse** (única que bloquea *antes*), PostToolUse (formateo/lint), **Stop** (+SubagentStop), PreCompact/PostCompact, InstructionsLoaded, SessionStart.
- **Re-inyectar contexto tras compactar → `SessionStart` con matcher `compact`, NO PostCompact.**
- `permissionDecision`: `allow` / `deny` / `ask` (+ `defer`, solo en runs `-p` no interactivos).
- **`updatedInput` reemplaza el objeto de input COMPLETO** → hay que devolver los campos no modificados.
- Códigos de salida: **0** éxito (JSON se parsea; texto plano solo entra en contexto en `SessionStart`, `UserPromptSubmit`, `UserPromptExpansion`) · **2** error **bloqueante** (stderr vuelve a Claude) · **cualquier otro** no bloquea.
- **Trampa: exit 1 NO bloquea.** Para bloquear, **exit 2**.
- `exit 2` puede bloquear `Stop`. PostToolUse ya es tarde para impedir la llamada. `Notification` y `SessionStart` ignoran el bloqueo.
- Patrón estrella: **redactar en vez de bloquear** (detectar `sk_live_` y sustituir por placeholder con `updatedInput`).

### Routines y headless

- Routine = **prompt + repo + connectors**, corre en infraestructura de Anthropic.
- Triggers: **cron**, **HTTP POST** a su endpoint, **evento de GitHub**.
- Crear: web `claude.ai/code/routines` o **`/schedule`** desde el terminal.
- Límites: **research preview** · **frecuencia máxima horaria** · **clon fresco de la rama por defecto y push solo a ramas `claude/`**.
- **`-p` / `--print`** = one-shot sin UI. **Se salta el auto-descubrimiento de hooks, skills, plugins, MCP y CLAUDE.md** → arranque más rápido.
- Salida estructurada: `--output-format json --json-schema '...'` → el objeto aterriza en **`structured_output`**.
- Multipaso: capturar `session_id` y `claude --resume`.
- **`--bare`** = modo determinista para CI.
- **Agent SDK** (TypeScript/Python): función **`query`**, opciones `allowedTools`, system prompt, permission mode.

### GitHub

- **Code Review** (gestionado): Claude GitHub app, corre en infra de Anthropic, analiza el diff **contra el codebase completo**, comentarios inline por severidad + tabla resumen, **deduplica y rankea**.
- Timing: al abrir el PR / en cada push / solo con `@claude review`.
- **Nunca aprueba ni bloquea el PR. No hay autofix gestionado. Research preview, planes team y enterprise.**
- Arreglar en local: **`/code-review --fix`**.
- **GitHub Action** `anthropics/claude-code-action@v1`; setup con **`/install-github-app`** (requiere admin del repo).
- Inputs: `anthropic_api_key`, `github_token`, `trigger_phrase` (default `@claude`), `use_bedrock`/`use_vertex`, `prompt`, **`claude_args`**.
- Ajuste en `claude_args`: `--max-turns 5`, permission mode que no pregunte, allowed tools mínimos.

### Verificación

- **Verifica en proporción a la cuerda que diste.**
- Desatendido → **auto mode**, no bypass.
- **Empieza por el diff, no por el resumen.** `/code-review` y luego `git diff` con tus ojos.
- Tests como **puerta** vía stop hook con **`exit 2`** (el fallo vuelve a Claude y lo arregla).
- Runs headless se verifican por su **resultado JSON y exit code**.
- **Segunda opinión en frío**: sesión/subagente fresco sin memoria de cómo se construyó.

### Plugins

- Unidad instalable: skills, subagentes, hooks, configs MCP, LSP, monitores, temas, porción de `settings.json`.
- `/plugin install org-name@plugin-name` → luego **`/reload-plugins`**.
- `/plugin marketplace add your-org/claude-plugins`. Pestaña **Discover**.
- **Ejecuta código con tus privilegios; los hooks se apilan, no reemplazan.**
- Skills/agentes/comandos van con **namespace**; del `settings.json` del plugin solo se honran **2 claves** (agent y subagent status line).
- La clave **agent promueve un subagente del plugin al hilo principal** (system prompt, tools, modelo) → cambia el comportamiento por defecto.
- Empaquetar: misma forma `.claude`. Manifiesto **opcional** en **`.claude-plugin/plugin.json`**; **`name` es el único campo obligatorio**.
- Marketplace comunidad (revisión automatizada) ≠ marketplace oficial (curado). **Revisado ≠ confiable.**

---

## Autotest rápido

Tapa las respuestas.

1. ¿Por qué `/compact` sin argumentos es mala idea?
2. ¿Qué hace exactamente un import `@fichero.md` en CLAUDE.md respecto al contexto?
3. Regla "nunca hagas push a main": ¿CLAUDE.md, skill o hook? ¿Por qué?
4. ¿Qué exit code bloquea en un hook, y cuál es el que engaña?
5. Quieres re-inyectar contexto justo después de una compactación. ¿Qué evento y qué matcher?
6. ¿Qué NO detecta el clasificador del modo auto, y con qué se compensa?
7. ¿Qué se pierde al usar `-p`?
8. ¿A qué ramas puede hacer push un routine por defecto?
9. ¿Code Review puede bloquear un PR o aplicar autofix?
10. Instalas un plugin solo por sus skills. ¿Qué más te llevas?
11. ¿Cuál es el único campo obligatorio de `plugin.json`?

<details>
<summary>Respuestas</summary>

1. El resumen puede tirar lo importante y Claude deriva. Lo que escribes tras el comando dirige qué conserva.
2. Se **expande inline al arrancar**: organiza, pero no reduce nada el contexto cargado.
3. **Hook PreToolUse.** CLAUDE.md es guía ("normalmente hará caso"); un hook es código que bloquea la acción de verdad.
4. Bloquea **exit 2**. El engañoso es **exit 1**: parece error pero NO bloquea, el comando corre igual.
5. **SessionStart** con matcher **`compact`** (no PostCompact).
6. No detecta si el **código es correcto** — solo intención peligrosa. Se compensa con un **stop hook que lance los tests**.
7. El auto-descubrimiento de **hooks, skills, plugins, servidores MCP y CLAUDE.md**. A cambio, arranque mucho más rápido.
8. Solo a ramas con prefijo **`claude/`** (y arranca desde un clon fresco de la rama por defecto), salvo que lo relajes por repo.
9. **No** a ambas. Solo publica hallazgos; el juicio queda en el humano. El fix se aplica en local con `/code-review --fix`.
10. Sus **hooks** (PreToolUse, Stop...), que se apilan sobre los tuyos y corren con tus privilegios. Y potencialmente un `agent` que promueve un subagente suyo al hilo principal.
11. **`name`** (da namespace `company-name:skill-name`).

</details>
