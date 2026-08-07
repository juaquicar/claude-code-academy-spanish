# 04 — Usar subagentes con criterio

[Vídeo](https://www.youtube.com/embed/n5LoKZ8Oa-A)

Ya sabes crearlos y diseñarlos bien. La pregunta ahora es: **¿cuándo ayudan de verdad y cuándo estorban?** La diferencia se reduce a una cosa — **si el trabajo intermedio le importa o no a tu hilo principal**.

## Cuándo brillan

Los subagentes funcionan mejor **cuando la exploración está separada de la ejecución**.

- Si **cada paso depende de lo que descubrió el anterior**, quieres ese trabajo en tu hilo principal.
- Si **solo necesitas una respuesta y el viaje te da igual**, delégalo.

Destacan en tareas donde:

- Necesitas **un resultado**, no la narración jugada a jugada de cómo se encontró
- El trabajo exploratorio **ensuciaría el contexto** de tu hilo principal
- La tarea **se beneficia de una perspectiva fresca** o de un system prompt a medida

## Caso 1 · Investigación

El caso de uso clásico. Investigar cómo funciona la autenticación en un codebase desconocido: tu hilo principal necesita saber **dónde** se valida el JWT, pero **no necesita ver cada fichero que se buscó** por el camino.

Un subagente de investigación puede leer decenas de ficheros, rastrear llamadas a función y explorar rutas de código distintas. **Toda esa exploración se queda en el contexto del subagente.** Tu hilo principal recibe un resumen limpio:

```
JWT validation happens in middleware/auth.js line 42,
called from the Express router in route/api.js
```

El subagente hizo el trabajo pesado. Tu hilo principal obtiene exactamente lo que necesita para avanzar.

## Caso 2 · Revisiones de código

> **Claude revisa código de forma más eficaz cuando el código se le presenta como escrito por otra persona.**

Si construiste una feature a lo largo de muchos turnos con tu hilo principal, pedirle a ese mismo hilo que la revise **suele producir feedback flojo**: Claude estuvo implicado en crearlo, así que le cuesta verlo con ojos frescos.

Un subagente revisor ve los cambios **en un contexto separado**: ejecuta `git diff`, lee los ficheros modificados y aplica sus criterios de revisión **sin el historial de cómo se escribió el código**.

Esa separación además te permite **codificar los estándares de revisión propios del proyecto** en el system prompt del subagente, garantizando **criterios consistentes en todo el equipo**.

## Caso 3 · System prompts a medida

El system prompt por defecto de Claude Code **enfatiza respuestas concisas y centradas en código**. Perfecto para programar, no para todo.

Dos casos donde un system prompt propio hace al subagente **genuinamente mejor que el hilo principal**:

| Subagente | Por qué gana |
|---|---|
| **Copywriting** | Le das instrucciones de tono, audiencia y estilo. El prompt por defecto de Claude Code tiende a escritura técnica concisa, que **no es lo que quieres** para una landing page o una campaña de email. Un subagente de copy puede tener instrucciones completamente distintas sobre voz y estructura. |
| **Estilos** | Lo apuntas a los ficheros de tu design system. Al ejecutarse, **esos ficheros se cargan en su contexto automáticamente**, así que conoce tus variables de color, convenciones de espaciado y patrones de componentes **antes incluso de escribir una línea de CSS**. |

## Cuándo hacen daño

El coste de lanzar un subagente —**perder visibilidad** de su trabajo y **comprimir sus hallazgos en un resumen**— solo compensa cuando el subagente hace algo que el hilo principal **no puede**. Tres antipatrones:

### ✗ Antipatrón 1 · Reclamos de experto

Los subagentes que **proclaman expertise** rara vez ayudan. Prompts del tipo *"you are a Python expert"* o *"you are a Kubernetes specialist"* **no aportan valor porque Claude ya tiene ese conocimiento**. No hay nada que un supuesto subagente experto pueda hacer que tu hilo principal no pueda hacer directamente.

### ✗ Antipatrón 2 · Pipelines secuenciales

Los pipelines secuenciales de subagentes **crean problemas**. Piensa en un flujo de tres agentes: uno reproduce un bug, otro lo depura, otro lo arregla.

> Los pipelines funcionan **cuando las tareas son realmente independientes**. Fallan cuando **cada paso depende de descubrimientos del paso anterior** — y arreglar bugs casi siempre es así. **La información se pierde en el traspaso** entre agentes.

### ✗ Antipatrón 3 · Ejecutores de tests

Los subagentes que corren tests **tienden a ocultar información que necesitas**. Cuando los tests fallan, quieres **la salida completa** para diagnosticar. Un subagente que devuelve *"tests failed"* te obliga a crear scripts de depuración adicionales para conseguir detalles **que habrían estado visibles en la salida directa**.

> Las pruebas mostraron que **el patrón de test runner fue el que peor rendimiento dio de todas las configuraciones**.

## La regla de decisión

Al decidir si usar un subagente, hazte **una sola pregunta**:

> ### ¿Importa el trabajo intermedio?

- **No** — solo necesitas el resultado final → **delega a un subagente**.
- **Sí** — necesitas ver y reaccionar a lo que ocurre por el camino → **quédatelo en el hilo principal**.

| ✓ Usa subagentes para | ✗ Evítalos para |
|---|---|
| Investigación y exploración | Personas de "experto" que no añaden capacidad real |
| Revisiones de código | Pipelines multipaso donde cada paso depende del anterior |
| Tareas que necesitan un system prompt a medida | Ejecutar tests cuando necesitas la salida completa para depurar |
