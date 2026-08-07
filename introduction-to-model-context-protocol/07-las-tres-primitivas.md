# 07 — Las tres primitivas

La lección que ordena todo el curso de golpe.

> Un servidor MCP tiene **tres primitivas** — tools, resources y prompts — y **se distinguen por quién decide cuándo se usan**.

## La tabla que hay que memorizar

| Primitiva | Quién controla | A quién sirve |
|---|---|---|
| **Tools** | **El modelo** — Claude decide cuándo ejecutarlas | Al **modelo** |
| **Resources** | **El código de la aplicación** decide cuándo traer los datos | A la **aplicación** |
| **Prompts** | **El usuario**, con acciones como un clic o un slash command | Al **usuario** |

---

## Tools · controladas por el modelo

**Primitivas donde Claude decide cuándo ejecutarlas.**

Se usan para **añadir capacidades a Claude** — por ejemplo, ejecución de JavaScript para hacer cálculos.

> **Sirven al modelo.**

## Resources · controladas por la aplicación

**Primitivas donde el código de la aplicación decide cuándo traer los datos.**

Se usan para **meter datos en tu app**, ya sea para mostrarlos en la interfaz o para enriquecer el prompt — por ejemplo, opciones de autocompletado o el listado de documentos de Google Drive.

> **Sirven a la aplicación.**

## Prompts · controlados por el usuario

**Primitivas disparadas por acciones del usuario**: pulsar un botón, escribir un slash command.

Se usan para **flujos de trabajo predefinidos** — por ejemplo, los botones de inicio de conversación en la interfaz de Claude.

> **Sirven al usuario.**

---

## La regla de decisión

> **¿Necesitas capacidades para Claude? → implementa tools.**
>
> **¿Necesitas datos para tu app? → usa resources.**
>
> **¿Necesitas flujos para el usuario? → crea prompts.**

**El patrón de control determina el propósito.** No elijas por lo que la primitiva *hace técnicamente*, sino por **quién debe decidir cuándo pasa**.

## Ejemplos reales, del propio Claude

| Qué ves en Claude | Qué primitiva es |
|---|---|
| Los **botones de inicio de conversación** | **Prompts** — los pulsa el usuario |
| La **selección de documentos de Google Drive** | **Resources** — los trae la aplicación |
| La **ejecución de código** | **Tools** — la decide el modelo |
