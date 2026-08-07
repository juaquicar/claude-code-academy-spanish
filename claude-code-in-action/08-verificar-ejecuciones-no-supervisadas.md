# 08 — Confía: verificar ejecuciones no supervisadas (Trust It)

Sección: *Verify and Share* · [Vídeo](https://www.youtube.com/embed/lalGZSNhm8E)

Le diste una tarea a Claude y lo dejaste correr sin mirar cada paso. Ahora dice que ha terminado. Antes de enviar ese trabajo necesitas una forma de comprobar algo que ni siquiera supervisaste. **Esa comprobación es lo que hace seguro depender de Claude Code sin manos.**

## La idea rectora

> **Verifica en proporción a la cuerda que diste. Cuanto menos miraste, más verificas.**

Si viste los mensajes pasar en una sesión corta, un vistazo basta. Pero un run desatendido, o un job que se disparó en CI sin nadie en el bucle, necesita una comprobación real: nadie vio lo que pasó, así que tienes que reconstruirlo a posteriori.

## Mantén los runs desatendidos en auto mode

En el trabajo, cuando un run va desatendido, usa **auto mode**, no *bypass permissions*. En auto mode el clasificador sigue revisando cada acción en busca de peligro. Esa red de seguridad merece la pena.

Pero ten claro qué hace y qué no: **el clasificador nunca juzga si el código es correcto**. Solo marca acciones peligrosas. Tu listón de verificación se queda exactamente donde estaba, y lo fijas según lo no supervisado que fuera el run.

## Empieza por el diff, no por el resumen

**No empieces por el resumen de Claude sobre lo que hizo. Empieza por el diff.**

1. Ejecuta `/code-review` para recorrer los cambios y marcar problemas.
2. Después pon tus propios ojos sobre `git diff`.

**La trampa:** un resumen ordenado que se lee perfectamente, mientras el diff real tocó un fichero que sinceramente no esperabas que tocara. El resumen no te lo dirá. El diff sí.

Lee qué cambió. Lee primero los ficheros que estaban en el plan, luego busca cualquier cosa fuera de él. **Un informe limpio no es prueba de código limpio.**

## Convierte los tests en una puerta, no en una promesa

La puerta real de un run no supervisado es si los tests pasaron **y si Claude realmente los ejecutó o solo dijo que lo hizo**. No lo dejes a la confianza: cabléalo como hook para que Claude no pueda saltárselo.

- Un **stop hook** que ejecuta tus tests y **se niega a terminar el turno** si fallan.
- Un **post-tool-use hook** que hace lint y type check después de cada edición.

**El detalle clave es el código de salida.** Un hook que sale con **`exit 2`** devuelve el fallo directamente a Claude. Claude lee ese fallo y lo arregla sin que se lo pidas. Y mejor aún: la comprobación dispara en **cada** run, te acuerdes o no de pedirla.

## Consigue una segunda opinión en frío

La revisión de código por sub-agente que harías antes de un PR sirve también aquí. Apúntala a un run no supervisado.

Abre una **sesión o sub-agente fresco** y que revise el código cambiado **sin memoria de cómo se construyó**. Como no tiene interés en el enfoque, pilla las cosas de las que el run original se autoconvenció.

> Un segundo revisor con ojos frescos encuentra lo que el autor racionalizó.

## Juntándolo todo

Haz la comprobación tan seria como no supervisado fue el run:

- **Lee el diff tú mismo.**
- **Convierte los tests en un hook que cierre el turno.**
- **Verifica los runs headless por su resultado JSON y su exit code.**
- **Consigue una segunda opinión en frío** en cualquier cosa que importe.

Con eso, *"Claude lo hizo mientras yo no miraba"* deja de ser un acto de fe.
