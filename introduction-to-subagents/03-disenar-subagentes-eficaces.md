# 03 — Diseñar subagentes eficaces

[Vídeo](https://www.youtube.com/embed/WPxWKT_OaU4)

Un subagente mal configurado **divaga, corre demasiado tiempo o produce una salida que el agente principal no puede usar**. Los arreglos se reducen a cuatro cosas: **buenas descriptions, formato de salida definido, reporte de obstáculos y acceso limitado a herramientas**.

## Cómo se usa realmente el config de un subagente

Cuando envías un mensaje al agente de la ventana de contexto principal, **el `name` y la `description` de cada subagente disponible se incluyen en su system prompt**. Así es como el agente principal decide **qué subagente lanzar y cuándo**.

> Si quieres mejor control sobre cuándo se dispara un subagente automáticamente, **name y description son lo que hay que tocar**.

Y la description tiene un **segundo papel**, que es el que casi nadie ve:

> Cuando el agente principal lanza un subagente, **escribe un prompt de entrada** para arrancar la tarea. **Usa la description como guía para escribir ese prompt.**

Es decir: la description no controla solo **cuándo** corre un subagente — **moldea lo que se le dice que haga**.

## Escribir descriptions que moldean el prompt de entrada

Toma un subagente de revisión de código.

- **Description genérica** → el agente principal podría escribir un prompt de entrada como *"use git diff to find the current changes"*. Vago: el subagente tiene que averiguar por su cuenta qué ficheros importan.
- **Description mejorada** → si le añades algo como *"You must tell the agent precisely which files you want it to review"*, el agente principal **escribirá un prompt de entrada mucho más específico**, listando los ficheros reales a revisar.

La técnica se traslada a cualquier tipo de subagente. Ejemplo: añadir *"return sources that can be cited"* a la description de un subagente de búsqueda web hace que el agente principal **incluya esa instrucción al delegar la tarea**.

## Definir un formato de salida

> **La mejora individual más importante** que puedes hacerle a un subagente es **definir un formato de salida en su system prompt.**

Hace dos cosas:

1. **Crea puntos de parada naturales** — el subagente sabe que ha terminado cuando ha rellenado cada sección del formato.
2. **Evita que corra demasiado tiempo** — sin una salida definida, los subagentes tienen problemas para decidir cuánta investigación es suficiente y **tienden a correr mucho más de lo necesario**.

Ejemplo de formato estructurado para un subagente de revisión de código:

```
Provide your review in a structured format:

1. Summary: Brief overview of what you reviewed and overall assessment
2. Critical Issues: Any security vulnerabilities, data integrity risks,
   or logic errors that must be fixed immediately
3. Major Issues: Quality problems, architecture misalignment, or
   significant performance concerns
4. Minor Issues: Style inconsistencies, documentation gaps, or
   minor optimizations
5. Recommendations: Suggestions for improvement, refactoring
   opportunities, or best practices to apply
6. Approval Status: Clear statement of whether the code is ready
   to merge/deploy or requires changes
```

Este formato le da al subagente **una checklist clara**. Una vez rellenada cada sección, sabe que puede parar.

## Reportar obstáculos

Cuando un subagente descubre un workaround durante su trabajo —resolver un problema de dependencias, descubrir que cierto comando necesita flags concretos— **esos detalles tienen que aparecer en el resumen que devuelve**. Si no, **el hilo principal tiene que redescubrir las mismas soluciones por su cuenta**, lo que desperdicia tiempo y tokens.

Lo que quieres que salga a la superficie:

- Problemas de setup o rarezas del entorno
- Workarounds descubiertos durante la tarea
- Comandos que necesitaron flags o configuración especial
- Dependencias o imports que dieron problemas

**La forma de conseguirlo es pedirlo explícitamente en el formato de salida.** Añadir una sección *"Obstacles Encountered"* a tu plantilla lo hace aflorar de forma fiable:

```
7. Obstacles Encountered: Report any obstacles encountered during the
   review process. This can be: setup issues, workarounds discovered or
   environment quirks. Report commands that needed a special flag or
   configuration. Report dependencies or imports that caused problems.
```

## Limitar el acceso a herramientas

No todo subagente necesita todas las herramientas. Dale solo las que su trabajo requiere. Eso consigue dos cosas: **evita efectos secundarios no deseados** y **hace más claro el rol de cada subagente** cuando tienes varios.

| Tipo de subagente | Herramientas | Razón |
|---|---|---|
| **Investigación / solo lectura** | `Glob`, `Grep`, `Read` | **No puede modificar ficheros accidentalmente** |
| **Revisor de código** | + `Bash` | Necesita `Bash` para ejecutar `git diff` y ver qué cambió, pero **sigue sin necesitar `Edit` ni `Write`** |
| **Estilos / modificación de código** | + `Edit`, `Write` | Aquí sí: su trabajo *es* cambiar tu código |

## Juntándolo todo

Los subagentes eficaces comparten cuatro características:

1. **Descriptions específicas** — controlan cuándo se lanza el subagente **y qué instrucciones recibe**. Escríbelas para dirigir ambas cosas.
2. **Salida estructurada** — define un formato en el system prompt para que el subagente sepa cuándo ha terminado y devuelva información que el hilo principal pueda usar.
3. **Reporte de obstáculos** — incluye una sección para workarounds, rarezas y problemas, para que el hilo principal no tenga que redescubrirlos.
4. **Acceso limitado a herramientas** — solo lo necesario. Solo lectura para investigación, bash para revisores, edit/write solo para agentes que deban cambiar código.

> Cada patrón es simple por separado, pero juntos convierten un subagente de "algo que vagamente intenta ayudar" en **un trabajador enfocado y predecible que termina a tiempo y reporta con claridad**.
