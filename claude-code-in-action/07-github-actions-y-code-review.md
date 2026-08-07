# 07 — GitHub Actions y Code Review

Sección: *Automate Repeat Work* · [Vídeo](https://www.youtube.com/embed/gIVt_iqmACw)

El mejor sitio para delegar trabajo repetitivo es el **pull request**. Dos caminos que resuelven problemas distintos: un **servicio gestionado** que activas, y una **GitHub Action** que cableas tú.

## Camino gestionado: Code Review

Servicio hospedado por Anthropic que revisa tus PRs mediante la **Claude GitHub app**. Nada que construir ni hospedar. Lo activas y empieza a publicar hallazgos como comentarios inline en las líneas que importan.

**Activación:** un admin de la organización lo habilita desde los ajustes de admin de Claude Code → sección *Code review* → botón *Configure*, que lo engancha a tus repositorios. Desde ahí el admin instala la Claude GitHub app, elige qué repos vigila y cuándo corre:

- Una vez, al abrir el PR
- En cada push al PR
- Solo cuando alguien comenta `@claude review`

**Cómo funciona:** todo corre en infraestructura de Anthropic. Un conjunto de agentes de revisión analiza el diff **contra tu codebase completo**, no solo las líneas cambiadas en aislamiento. Publica hallazgos como comentarios inline en las líneas concretas, **etiquetados por severidad**, con una **tabla resumen** en el check run.

Lo bueno: **deduplica y rankea** los hallazgos. En vez de un muro de nimiedades, lees un puñado de problemas reales.

### Qué hace y qué no

- **Nunca aprueba ni bloquea el PR.** El juicio se queda con un humano. Claude marca; tú decides.
- **No hay autofix gestionado.** El servicio solo publica hallazgos.
- Es **research preview**, disponible en planes **team y enterprise**. Espera que el comportamiento cambie.

Como no hay autofix en el servicio, aplicar un hallazgo es un movimiento local. Desde tu terminal:

```
/code-review          # revisa un diff
/code-review --fix    # aplica los hallazgos a tu working tree
```

**Flujo:** Claude lo encuentra en el PR → tú te lo bajas y lo arreglas en local.

## Camino DIY: la GitHub Action

Code Review cubre *revisión*. Cuando el trabajo va **más allá de revisar**, usas la GitHub Action: CI a medida — implementar cambios desde un comentario, informes programados, cualquier cosa que normalmente escribirías como workflow. Corre el agente sobre comentarios de PR, jobs programados y cualquier evento de GitHub.

**Setup:** desde dentro de Claude Code, ejecuta `/install-github-app` (necesitas admin del repo). El slash command te guía instalando la GitHub app y poniendo el secreto con la Anthropic API key en el repo.

La action es **`anthropics/claude-code-action@v1`**. Inputs que usarás de verdad:

| Input | Descripción |
|---|---|
| `anthropic_api_key` | Opcional |
| `github_token` | Por defecto `secrets.GITHUB_TOKEN` |
| `trigger_phrase` | Qué escucha la action en los comentarios. Por defecto `@claude` |
| `use_bedrock` / `use_vertex` | Cambiar a esos proveedores |
| `prompt` | La instrucción del run |
| `claude_args` | Cadena de argumentos CLI pasados directamente a Claude Code |

### Workflow que responde a @claude

En `.github/workflows/claude.yaml`, escucha `@claude` en comentarios de PR e issues:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}
    trigger_phrase: "@claude"
    prompt: "Your instructions here"
    claude_args: "--max-turns 5 --model claude-sonnet-5"
```

Alguien escribe `@claude implement the spec in the linked Linear issue` en un PR y la action lo recoge. Claude hace push de commits y publica comentarios describiendo lo que hizo.

### Workflow programado

La misma action sirve para un resumen diario: un trigger cron dispara p. ej. a las 9:00 UTC, la action corre y Claude publica los resultados. Añade también un trigger **`workflow_dispatch`** para poder lanzarlo a mano desde la pestaña Actions. Puedes ver el progreso paso a paso en Actions, como cualquier workflow.

### Ajustar el run con claude_args

- **`--max-turns 5`** — tope duro al bucle del agente, para que no corra eternamente.
- **Permission mode** — en un job desatendido quieres que no se pare a preguntar, porque no hay nadie para contestar.
- **Allowed tools** — dale exactamente lo que necesita y nada más. Para un informe, eso significa solo lectura.

## ¿Cuál usar?

- **Para revisiones de PR** → camino gestionado. Activa Code Review, deja que la GitHub app publique hallazgos inline, y aplica arreglos en local con `/code-review --fix`.
- **Cuando el trabajo es más que revisar** → la action. `/install-github-app` para el setup, un workflow para menciones `@claude`, otro para cron, y todo el ajuste fino en `claude_args`.

**Empieza por el servicio gestionado. Pasa a la action en cuanto necesites que Claude realmente *haga* algo en CI, no solo que comente.**
