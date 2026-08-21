# 07 — Revisión de código

*10 minutos* · [Vídeo](https://www.youtube.com/embed/RKsADl0ZC3Y)

**Al terminar sabrás:** por qué el revisor debe ser un subagente de solo lectura · qué hace la skill `/commit-push-pr` · cómo retomar el trabajo de un PR con `--from-pr`.

---

Claude Code trae algunas funcionalidades integradas que aceleran tu flujo de git.

## Revisar con un subagente

Antes de subir un PR, pídele a Claude que use un **subagente** para revisar tus cambios. El subagente corre en **su propia ventana de contexto con ojos frescos** — no arrastra el sesgo del agente principal que acaba de pasarse la sesión escribiendo ese código.

Al crear un subagente revisor de código:

- **Restríngelo a tools de solo lectura.** Un revisor debe **señalar problemas, no editar ficheros**.
- **Versiona la configuración del subagente en tu repositorio** para que todo el equipo use el mismo revisor.

## La skill `/commit-push-pr`

La skill `/commit-push-pr` se encarga del commit, el push y la creación del PR **en un solo paso**. En vez de hacer cada cosa a mano, ejecutas la skill y Claude se ocupa.

> Si tienes un **servidor MCP de Slack** configurado con los canales listados en tu CLAUDE.md, publicará automáticamente el enlace del PR en el canal de tu equipo.

## Enlazado de sesión con `--from-pr`

Cuando Claude crea un PR a través de `gh pr create`, **la sesión queda enlazada a ese PR automáticamente**. Si necesitas volver a él más tarde — para atender comentarios de revisión o arreglar un build que falla — ejecuta:

```
claude --from-pr <PR_NUMBER>
```

Esto retoma justo donde lo dejaste.

## Conclusiones

Usa un **subagente** para una revisión de código sin sesgo antes de subir. Usa **`/commit-push-pr`** para resolver el flujo completo de commit a PR en un paso. Y usa **`--from-pr`** para retomar el trabajo sobre un PR más tarde. Son funcionalidades pequeñas, pero quitan mucha fricción del día a día.
