# 13 — Construir con Claude Code

*10 minutos* · [Vídeo](https://www.youtube.com/embed/Zq_c7xMbxto)

**Al terminar sabrás:** qué es la skill **Claude API** y cómo se invoca · cómo añadirla desde el marketplace (y la errata que todo el mundo comete) · las tres cosas que hace un buen prompt · el patrón de tres pasos que se repite siempre.

---

Escribir a mano el código que llama a la Claude API funciona bien, pero **hay un camino más rápido: que lo escriba Claude**. Aquí usamos **Claude Code** para rellenar una integración de la API a partir de un fichero con stubs — con los mismos primitivos del curso.

## Partiendo de un stub

El proyecto es simple: un fichero TypeScript que obtiene el tiempo. Contiene **dos stubs**:

- **`getWeather`** — acepta una ciudad y devuelve temperatura y condiciones.
- **`run`** — una función que debe usar el **tool runner** y el SDK de TypeScript de Claude.

El **tool runner** es la pieza que se encarga del tool calling y del bucle de agente por ti, para no tener que cablearlo a mano.

## La skill Claude API

Claude Code viene con una skill integrada llamada **Claude API**. Puedes invocarla directamente con **`/claude-api`**, o **Claude Code la invoca automáticamente** cuando detecta que estás usando el SDK de TypeScript.

> **Trampa de examen.** El slash command es **`/claude-api`** — no `/anthropic-api`, ni `/claude-sdk`, ni `/api-tools`. Es la pregunta 5 del quiz oficial.

Si no ves la skill, puedes añadirla desde el marketplace:

```
/plugin marketplace add AnthropicsSkills
```

> **Fíjate en la `s` al final de Anthropics** — se pasa por alto con facilidad.

## Un prompt, código funcionando

Abre la carpeta del proyecto en tu terminal y lanza Claude Code. A partir de ahí basta **un solo prompt**. Un buen prompt hace **tres cosas**:

1. **Nombra el fichero** que quieres cambiar.
2. **Nombra el patrón** que quieres que se use.
3. **Nombra el estado final** que esperas.

Claude Code entonces rellena `getWeather` y `run` contra los tipos, añade una llamada al final del fichero, **ejecuta el script y reporta la salida**. Si algo falla, **lee el mensaje de error y parchea el código in situ**.

## Qué produjo Claude Code

En esta ejecución, Claude Code creó una **tool con Zod** que parseaba la entrada y devolvía la salida según el tipo de ciudad. También creó el tool runner y la función `run` que pedimos, e imprimió los resultados finales del bucle de agente.

## El patrón a recordar

Casi todo lo que escribes contra la Claude API tiene la misma forma:

1. **Define una tool.**
2. **Pásasela a un runner.**
3. **Devuelve el resultado.**

> No hace falta que lo teclees de memoria cada vez. **Deja el fichero con stubs, pásaselo a Claude Code y revisa el diff.**

## Conclusiones

- **Claude Code** es un agente que edita ficheros y ejecuta comandos dentro de tu terminal.
- La skill integrada **Claude API** se carga automáticamente cuando Claude Code detecta el SDK de TypeScript, o la invocas con **`/claude-api`**.
- Dale un prompt que nombre **el fichero, el patrón y el estado final** — escribe el código, lo ejecuta y **arregla los errores in situ**.
- El código de la Claude API sigue una forma familiar: **define una tool, pásasela a un runner, devuelve el resultado.** Stub, delega, revisa el diff.

> **¿Quieres profundizar?** Los cursos dedicados: [Claude Code 101](../claude-code-101/README.md) y [Claude Code in Action](../claude-code-in-action/README.md).
