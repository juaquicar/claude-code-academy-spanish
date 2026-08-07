# 03 — Skills de verificación (Verification Skills)

Sección: *Configure Claude* · [Vídeo](https://www.youtube.com/embed/soLPOXXAc1w)

Las skills automatizan trabajo repetido. De todas las que puedes construir, **la de verificar tu propio trabajo es la primera que merece la pena**.

## Por qué esta skill va primero

Cómo compruebas normalmente el trabajo de Claude: le pides un refactor, termina, y **tú tienes que acordarte** de revisar. Quizá le pides que lance los tests. Quizá lees el diff. El problema: la comprobación depende de que tú te acuerdes de pedirla. Te lo saltas una vez y cuela código malo.

Una skill de verificación elimina esa dependencia. Forma:

1. Pides un refactor.
2. Al terminar, el cambio encaja con la **description** de la skill → **la skill se dispara sola**.
3. Ejecuta la suite de tests.
4. Lee el diff.
5. **Comprueba que ningún test fue debilitado solo para que pase.**
6. Reporta pass/fail **con la evidencia adjunta**.

Todo el flujo corre sin que lo pidas. La `description` es lo que la dispara; una vez disparada recorre los mismos pasos siempre.

> Fíjate en el paso 5. No basta con ver los tests en verde: un test se puede aflojar en silencio para que pase pase lo que pase. "Hecho" no es "el código parece correcto leyendo el diff". **Hecho es que las puertas se ejecutaron y se observaron, con los resultados declarados explícitamente.**

Esta misma forma sirve para cualquier procedimiento que tu equipo repita: checklist de release, receta de migración, chequeo pre-PR.

**Regla del pulgar: si has tecleado la misma instrucción multipaso dos veces, eso es una skill.**

## Una carpeta de skill guarda más que instrucciones

Una skill no es solo un `skill.md`. La carpeta puede llevar más cosas:

- **`reference.md`** al lado, con material detallado, enlazado desde `skill.md`. Claude solo lo lee cuando necesita esa profundidad → el fichero principal se queda corto.
- **Scripts** en la carpeta. Claude los **ejecuta** en vez de cargar su contenido en contexto. Así una skill lleva su propio utillaje, p. ej. un `check.sh` que corre todas las puertas.

> Mantén `skill.md` magro. Empuja el material pesado —explicaciones largas y scripts ejecutables— a ficheros laterales. El fichero magro describe qué hacer; los laterales guardan la profundidad y las herramientas.

## Qué superficie es dueña de qué regla

| Regla | Dónde va |
|---|---|
| Convenciones que aplican **siempre** (nombres, ubicación de ficheros) | `CLAUDE.md` |
| Procedimientos y material de referencia ligados a **un tipo de tarea** | Skill |
| Regla que Claude **no puede saltarse** | Hook |

Porque `CLAUDE.md` y skills son *instrucciones que Claude sigue*; un hook es *código que se ejecuta*. Si saltarse la regla no es aceptable, no lo dejes en manos del seguimiento de instrucciones.

## Recapitulación

Una skill es una carpeta con un `skill.md` dentro: un nombre, una **description que la dispara**, y el procedimiento.

**Solo las descriptions se cargan en contexto** hasta que una skill se necesita de verdad → no hay coste en empaquetar todos los procedimientos que repites.

Empieza por verificación. Constrúyela, súbela a `.claude/skills` de tu proyecto, y **todo el equipo hereda el mismo movimiento**: el trabajo de todos se comprueba igual, automáticamente, sin que nadie tenga que acordarse de pedirlo.
