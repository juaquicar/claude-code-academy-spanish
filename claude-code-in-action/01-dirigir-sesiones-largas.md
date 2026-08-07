# 01 — Dirigir sesiones largas (Steering Long Sessions)

Sección: *Steer the Work* · [Vídeo](https://www.youtube.com/embed/l_4ZYAiyP7U)

Tarea corta = fácil. Tarea larga (refactor de 12 ficheros, feature nueva, horas) = otro juego. Cuanto más tienes que corregir sobre la marcha, más se alarga.

Dos hábitos: **acotar antes de empezar** y **dirigir mientras corre**.

## 1. Acotar primero con plan mode

Antes de escribir una línea, que Claude presente un plan. En plan mode investiga en **solo lectura**: lee código, decide qué cambiar, te entrega un plan.

- Léelo de verdad, no lo hojees.
- Cuanto más completo el plan, menos sorpresas en ejecución.
- Si falta algo, pídele que lo añada donde quieras.
- Iterar sobre el plan es **mucho más rápido** que dejarlo correr y limpiar el destrozo.

## 2. Dirigir mientras trabaja

### Compact

Resume la conversación, usa el resumen como contexto nuevo y borra los mensajes viejos. Libera ventana de contexto.

**Riesgo:** que el resumen tire algo importante y Claude se desvíe.

Por eso: nunca `/compact` a secas. Añade instrucciones detrás para decirle qué conservar.

```
/compact Focus on the --version flag implementation
```

Lo que escribas tras el comando moldea el resumen. Ese es tu volante del contexto.

### Rewind

Cuando Claude coge el camino equivocado, no hace falta prompt-earse la salida. Rewind vuelve al último checkpoint. **Cada prompt del usuario crea un checkpoint.** Abrir menú: doble toque a `Esc` con el prompt vacío.

Opciones del menú:

- **Restore code and conversation** — revierte ambos a la vez.
- **Restore conversation** — solo el chat.
- **Restore code** — solo los ficheros.
- **Summarize from here** — resume todo lo *posterior* al checkpoint. Útil si hubo una conversación lateral y quieres liberar espacio.
- **Summarize up to here** — resume todo lo *anterior*. Útil cuando hubo una fase larga de preparación que quieres comprimir, manteniendo intacta la implementación.

## 3. Dejarlo correr más autónomo

### Goal

Fija una **condición de finalización**. Describes qué es "hecho" y Claude sigue trabajando entre turnos hasta que un evaluador rápido confirma que se cumple. No para la primera vez que cree haber terminado.

```
/goal all tests in src/billing pass, and the type checker reports zero errors
```

Cancelar: `/goal clear`.

**Restricción clave:** el evaluador **solo lee el transcript**. La condición tiene que ser comprobable desde la salida que Claude realmente produce (p. ej. resultados de un test run).

### Loop

Ejecuta un prompt a intervalos entre turnos, fijo o autoregulado. Sirve para *sondear* algo externo (un run de CI, un deploy) y actuar cuando cambia el estado.

Parar un loop: `Esc`.

## 4. Trabajo en paralelo con worktrees

Metáfora: un volante por coche. Varios agentes sobre el mismo repo = dos volantes en un coche = conflictos peleando por los mismos ficheros.

**Worktrees:** cada sesión recibe su propio árbol de ficheros independiente. No se pisan. Al salir de una sesión, un worktree limpio se elimina automáticamente.

Fichero útil: **`.worktreeinclude`** en la raíz del repo. Lista ficheros ignorados por git que se deben copiar a cada worktree — p. ej. fichero de variables de entorno o config local que necesitas en todos los worktrees pero no quieres versionar.

## Resumen ejecutable

1. Acota el trabajo primero, luego dirige.
2. Dirige la compactación para que el resumen conserve lo que importa.
3. Usa el menú rewind para corregir el rumbo cuando derive.
4. Fija un `goal` cuando sepas describir mejor el "hecho" que los pasos.
5. Ejecuta trabajo paralelo en worktrees.
