# 09 — Plugins

Sección: *Verify and Share* · [Vídeo](https://www.youtube.com/embed/k4kZwJ0FtX0)

Un setup en el que confías vale mucho más cuando todo tu equipo lo ejecuta. El problema es **moverlo**: construyes un buen directorio `.claude` con skills, subagentes y hooks... ¿y luego qué? Todos copiando y pegando ficheros entre máquinas esperando que sigan sincronizados.

**Un plugin es cómo Claude Code empaqueta un setup y lo mueve de una persona a la siguiente.**

## Qué es un plugin

**Una unidad instalable.** Empaqueta todo lo que si no compartirías a mano: **skills, subagentes, hooks y configs de servidores MCP**, más la cola larga: servidores LSP (language server protocol), monitores en segundo plano, temas y **una porción de `settings.json`**. Una versión, una instalación.

Dónde vive el plugin decide cómo lo instalas. Dentro de una sesión, por nombre:

```
/plugin install org-name@plugin-name
```

Claude Code lo instala y te dice que ejecutes `/reload-plugins` para aplicar el cambio.

## Añadir un marketplace para tu equipo

Para un equipo, lo mejor es añadir un **marketplace privado** una vez. Un marketplace es una fuente compartida por la que se resuelven los plugins:

```
/plugin marketplace add your-org/claude-plugins
```

Una vez añadido, toda instalación posterior se resuelve a través de él → **descubrimiento centralizado, seguimiento de versiones y actualizaciones en un solo sitio** en vez de dispersos por los portátiles de todos.

Puedes explorar lo disponible desde la pestaña **Discover**, que lista los plugins de tus marketplaces.

## ⚠️ Lee antes de instalar

**La parte que más importa:**

> Un plugin **ejecuta código en tu máquina, con tus privilegios**. Sus hooks disparan en cada llamada a herramienta que haga match. Si instalas un plugin por sus skills, **también te llevas sus hooks PreToolUse y Stop, los hayas leído o no.**

Un plugin de la comunidad podría traer un **Stop hook que llame a un endpoint de red cada vez**, y nada en tu configuración te avisaría. No es razón para evitar plugins; es razón para **mirar primero**.

Antes de instalar, revisa los detalles del plugin. Claude Code te muestra **qué va a instalar** y **estima el coste de contexto**, junto con un aviso claro de que Anthropic no controla lo que hay dentro de plugins de terceros.

Sobre la procedencia:

- El **formulario de envío in-app** publica al **marketplace de la comunidad** tras la revisión automatizada de Anthropic.
- El **marketplace oficial** se cura en una vía separada.

> **Revisado no es lo mismo que confiable.** La revisión automatizada pilla algunas cosas, no todas. Instala plugins y añade marketplaces solo de fuentes en las que realmente confíes, y comprueba qué hace un plugin antes de encenderlo.

## Los componentes corren *junto a* los tuyos

Un plugin **no sobrescribe** tu configuración. Sus componentes corren en paralelo. Consecuencias:

- **Los hooks se apilan.** El PreToolUse del plugin y el tuyo disparan *ambos* en cada llamada a herramienta. Ninguno reemplaza al otro. Exactamente por eso lees los detalles primero.
- **Skills, agentes y comandos van con namespace** bajo el nombre del plugin, así que nunca chocan con los tuyos.
- Un plugin puede traer un **`settings.json`**, pero solo uno estrecho: Claude Code honra **únicamente dos claves** — las de *agent* y *subagent status line*.

> La clave **agent** merece una pausa: activarla **promueve uno de los subagentes del plugin al hilo principal**, junto con su system prompt, restricciones de herramientas y modelo. Es decir: **habilitar el plugin puede cambiar cómo se comporta Claude Code por defecto.** Otra razón para mirar antes incluso de encenderlo.

Una vez instalado, ves todo lo que añadió, lo gestionas y lo desinstalas desde el **panel de plugins**.

## Empaquetar tu propio plugin

No hay que reestructurar nada: un plugin usa **la misma forma `.claude` que ya usas**:

- Una carpeta por skill.
- Un fichero markdown por subagente bajo `agents`.
- `hooks/hooks.json` y `.mcp.json` en la raíz del plugin.

La estructura de directorios hace casi todo el trabajo: Claude Code **descubre componentes por convención**.

### El manifiesto

Opcional, en **`.claude-plugin/plugin.json`**:

```json
{
  "name": "svg-splitter-review",
  "version": "0.1.0",
  "description": "Reviews the SVG Splitter repo",
  "author": {
    "name": "Lewis Menelaws"
  }
}
```

Sin él, Claude Code descubre igualmente tus componentes por convención de directorios. Pero:

- **`name` es el único campo obligatorio.** Pone namespace a tus skills como `company-name:skill-name`, evitando colisiones.
- **Versiona como cualquier otra dependencia.** Es lo que hace funcionar actualizaciones y seguimiento de versiones en el equipo.

## Conclusión

- **Cuando uses plugins: lee antes de instalar.** Un plugin ejecuta código con tus privilegios — mira sus hooks, agentes y servidores MCP primero.
- **Cuando construyas uno: empaqueta tu `.claude` en cuanto funcione.** Un manifiesto, una instalación.

Una unidad instalable, y el setup en el que confías llega a todo tu equipo.
