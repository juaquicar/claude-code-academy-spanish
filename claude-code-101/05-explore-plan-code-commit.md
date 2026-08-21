# 05 — El flujo explore → plan → code → commit

*15 minutos* · [Vídeo](https://www.youtube.com/embed/xJQuF02NAK8)

**Al terminar sabrás:** las cuatro fases del flujo y qué aporta cada una · por qué Plan Mode es el mejor sitio para corregir el rumbo · los tres consejos para que la fase de código vaya suave · por qué el revisor debe ser un subagente.

---

> **Si te llevas una sola cosa de este curso, que sea este flujo: Explore, Plan, Code y Commit.**

Sin él, la mayoría de la gente salta directamente a pedirle a Claude que escriba código — lo que significa **más correcciones de rumbo después**.

## Explore y Plan

La forma más rápida de resolver estos dos primeros pasos es con **Plan Mode**. En plan mode, Claude **no puede editar ficheros**: solo lee para reunir información sobre cómo va a abordar la implementación.

Para entrar en plan mode, pulsa `Shift + Tab` hasta que veas "Plan Mode" bajo el campo de texto. Luego escribe un prompt como:

```
I need to add WebP conversion to our image upload pipeline. Figure out where in the pipeline it should happen, whether we need new dependencies, and how to approach it.
```

Claude leerá los ficheros relevantes, hará algunas búsquedas web y te dará un plan de acción. Revísalo y decide si cumple tus criterios. Si no, **pídele que revise áreas concretas**.

> **Este es el mejor sitio para corregir el rumbo, porque es antes de que se escriba ningún código.**

También puedes ejecutar el **subagente de explore sin estar en plan mode** si solo quieres un resumen general de tu base de código sin intención de cambiar nada después.

## Code

Cuando el plan tiene buena pinta, selecciona "approve" para aceptarlo y deja que Claude vaya recorriendo los puntos de la lista. Puedes elegir si Claude auto-acepta las ediciones de fichero o te pregunta cada vez.

Claude hará lo posible por depurar antes de dar el plan por "terminado", pero **a veces tendrás que intervenir**. Ese es el beneficio de trabajar con Plan Mode: después de la ejecución también tienes **el contexto de cómo llegaste a los resultados**, lo que ayuda a guiar las siguientes decisiones de Claude.

Tres consejos para que esta fase vaya suave:

- **Define un criterio de éxito.** Para que Claude tenga confianza en sus resultados, necesita tener claro qué significa "correcto". Hazlo explícito al escribir tu plan.
- **Añade tools.** Las tools que ayudan a Claude a completar sus objetivos eliminan mucho ida y vuelta. Por ejemplo, si construyes interfaces web, instala la extensión **Claude in Chrome** para que Claude Code pueda controlar una pestaña del navegador y probar la UI directamente.
- **Incluye una suite de tests.** Dale a Claude una suite contra la que validar continuamente. Claude incluso puede escribirte los tests. **Antes de delegar esto, asegúrate de que los tests son una fuente de verdad fiable**, para evitar falsos positivos.

> **Truco rápido:** si ves que Claude tropieza una y otra vez con los mismos problemas, **pídele que guarde la solución en su fichero CLAUDE.md**.

## Commit

Una vez que has probado los cambios tú mismo y estás contento con el resultado, toca subir el código. Antes de hacer commit, **ejecuta un subagente revisor de código** para que mire tu trabajo.

> **Por qué un subagente y no el agente principal:** un subagente aporta **un par de ojos frescos** sobre la base de código — **no arrastra el sesgo** que el agente principal puede haber acumulado durante la sesión.

Luego pídele a Claude que genere un mensaje de commit **en tu estilo**. Enjuaga y repite.

## Conclusiones

Para ser efectivo con Claude Code, sigue el flujo Explore, Plan, Code y Commit:

- **Explore** le da a Claude el contexto relevante que necesita de tu proyecto.
- **Plan** crea un plan de acción que Claude usa para medir el éxito.
- **Code** es el ida y vuelta entre tú y Claude antes de fijar el resultado final.
- **Commit** te ayuda a revisar y subir tu código para que empieces con la siguiente funcionalidad.

> **Trampa de examen.** El flujo recomendado es **Explore → Plan → Code → Commit**. Los distractores del quiz oficial son variantes que suenan igual de razonables: *Code → Test → Deploy → Monitor*, *Write → Review → Merge → Ship*, *Prompt → Accept → Push → Repeat*. Ninguno es el del curso.
