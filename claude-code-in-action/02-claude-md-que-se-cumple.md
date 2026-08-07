# 02 — Un CLAUDE.md que se cumple (A CLAUDE.md That Follows)

Sección: *Configure Claude* · [Vídeo](https://www.youtube.com/embed/sfE5UQEumdM)

**La trampa:** el CLAUDE.md crece sin parar. Problema → añades regla. Otro problema → otra regla. Acabas con un fichero gigante y Claude empieza a ignorar partes. No es un bug: es cómo funciona el fichero.

**Clave:** CLAUDE.md **no es configuración obligatoria, es guía**. Cada línea compite con todas las demás por la atención de Claude. Cuanto más largo, más compite consigo mismo y menos fiablemente se sigue cualquier regla concreta.

> El objetivo no es escribirlo todo. Es mantener el fichero apretado. Cuanto más magro, más lo cumple Claude.

## Primero: ¿es CLAUDE.md la herramienta correcta?

Hay reglas que son **guía** y reglas que son **líneas rojas**. Son dos trabajos distintos.

Ejemplo: *"nunca hagas push a main"*. En CLAUDE.md estás *esperando* que Claude lo lea y lo respete. La mayoría de las veces lo hará. Pero "la mayoría de las veces" no basta para algo tan peligroso.

Eso va en un **hook PreToolUse**. Un hook es código que corre antes de la acción y **puede bloquearla**. Cumplimiento real, no una petición educada.

→ Mueve las reglas duras a hooks; deja a CLAUDE.md las convenciones blandas.

## Las cuatro ubicaciones

CLAUDE.md no es un único fichero. Hay cuatro sitios, y Claude **carga todos al arrancar**. Nada se descarta; se apilan.

| Ubicación | Para qué |
|---|---|
| **Managed policy** | Fichero de organización que controla tu equipo de plataforma. No se puede excluir: la política corporativa siempre está en juego. |
| **User** | Tus preferencias personales, te siguen en todos los proyectos de tu máquina. |
| **Project** | Compartido con el equipo, versionado en el repo. |
| **Local** | Ignorado por git. Tus notas personales solo para ese repositorio. |

**Local** se pasa por alto y es muy útil: estás refactorizando en tu rama y quieres que Claude tenga presentes ciertas decisiones arquitectónicas. Eso no va en el fichero compartido del equipo.

## Partir un fichero grande con imports

Sintaxis path-to-file:

```
@.claude/conventions/code-style.md
@.claude/conventions/testing.md
@.claude/conventions/workflow.md
```

**Ojo con la idea equivocada:** al arrancar, Claude **expande los ficheros importados inline**, justo donde los referenciaste. Los imports ayudan a **organizar**, pero **todo se carga igual por adelantado**. No reducen el contexto que Claude debe leer.

> Usa imports para organizar, no para adelgazar la carga.

## La redacción es lo que hace que una regla pegue

La mayoría de reglas fallan por vagas.

### Sé específico y comprobable

- ❌ Vago: *"Follow best practices for API routes."* — si tú no puedes comprobar si se cumplió, Claude tampoco.
- ✅ Específico: *"Put new API routes in `src/api/handlers`, one per file."*

Debes poder mirar el resultado y saber al instante si se hizo bien.

### Nombra el reemplazo, no solo prohíbas

- ❌ Deja la puerta abierta: *"Don't use default exports."* — vale, ¿y entonces qué?
- ✅ La cierra: *"Use named exports, not default exports."*

### El énfasis es un presupuesto

`IMPORTANT`, `YOU MUST` sí suben la prioridad de una regla — **pero solo en relación a lo que hay alrededor**. Si todas las reglas gritan, ninguna destaca y el énfasis no significa nada.

→ Gástalo en las 2-3 reglas que de verdad duelen cuando se rompen. El resto, volumen normal.

## Mantén el fichero bajo revisión

El CLAUDE.md nunca está terminado. Trátalo como código vivo.

Cuando Claude haga algo mal, no suspires y lo arregles a mano: **trátalo como un bug report contra tu CLAUDE.md**. Puedes decirle directamente *"add that to the CLAUDE.md file"* y escribe la regla por ti. Así el fichero mejora cada vez que algo sale mal.

## Conclusión

Trata tu CLAUDE.md como código de producción. Si no puedes justificar una línea, bórrala.

1. Mueve las reglas duras a hooks, donde sí se aplican.
2. Organiza ficheros largos con imports (recordando que no reducen contexto).
3. Haz cada regla específica y comprobable, y nombra el reemplazo.
4. Gasta el presupuesto de énfasis en las pocas reglas que importan.
5. Revisa el fichero cada vez que Claude se equivoque.
