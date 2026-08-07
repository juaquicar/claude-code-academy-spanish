# 11 — Agentes y workflows

**Workflows y agentes** = dos estrategias para tareas que Claude no puede completar en una sola petición.

## La regla de decisión

> **Usa workflows cuando entiendas la tarea con precisión y sepas la secuencia exacta de pasos.**
> **Usa agentes cuando los detalles de la tarea no estén claros.**

**Workflow** = una serie de llamadas a Claude para un problema concreto, **con los pasos predeterminados**.

### El ejemplo: conversor de imagen a modelo 3D

| Paso | Qué hace |
|---|---|
| 1 | Claude describe la imagen subida en detalle |
| 2 | Claude usa la librería CADQuery de Python para modelar el objeto desde la descripción |
| 3 | Se genera un render del modelo |
| 4 | Claude compara el render con la imagen original |
| 5 | Si no es preciso, **vuelve al paso 2 con el feedback** |

Eso es el **patrón evaluador-optimizador**:

- **Productor** — genera la salida (Claude + modelado CADQuery).
- **Evaluador** — valora la calidad (el paso de comparación).
- El bucle continúa hasta que el evaluador acepta.

> ⚠ **Ojo:** los workflows son **patrones de implementación** que otros ingenieros han usado con éxito. Identificar el patrón **no lo implementa por ti** — sigues teniendo que escribir el código.

---

## Los tres patrones de workflow

### Paralelización

Partir una tarea compleja en **varias subtareas simultáneas** y luego agregar los resultados.

**Ejemplo — selección de material para una pieza:**

- ❌ **En vez de:** un prompt grande pidiendo a Claude que elija entre metal, polímero, cerámica y compuesto con todos los criterios a la vez.
- ✅ **Haz:** peticiones paralelas separadas, cada una evaluando la idoneidad de **un material**, y un paso final de agregación que compare resultados.

**Estructura:** entrada → múltiples subtareas en paralelo → agregador → salida final.

**Beneficios:**

| | Por qué |
|---|---|
| **Foco** | Cada subtarea hace un análisis específico en vez de malabares con varias consideraciones |
| **Modularidad** | Cada prompt se puede mejorar y evaluar por separado |
| **Escalabilidad** | Añadir subtareas nuevas no afecta a las existentes |
| **Calidad** | Reduce la confusión de los prompts únicos demasiado complejos |

### Encadenado (chaining)

Partir una tarea grande en una **serie de pasos secuenciales** distintos, en vez de un prompt complejo único.

**Ejemplo:** el usuario introduce un tema → buscar temas en tendencia → Claude elige el más interesante → Claude investiga → Claude escribe el guion → generar el vídeo → publicar en redes.

**El caso de uso principal, que es menos obvio:**

> Cuando **Claude ignora sistemáticamente restricciones** en prompts complejos por mucho que las repitas. Pasa a menudo con prompts largos llenos de *"no hagas X"*.

**Escenario problema:** un prompt largo con restricciones —no menciones la IA, sin emojis, tono profesional— y Claude viola algunas pase lo que pase.

**Solución:**

1. Envía el prompt inicial y **acepta la salida imperfecta**.
2. Envía un prompt de seguimiento pidiéndole que reescriba **según las violaciones concretas encontradas**.

> **La idea:** incluso un workflow que parece trivial se vuelve imprescindible con prompts cargados de restricciones que la IA no consigue cumplir de una pasada.

### Enrutado (routing)

**Categorizar la entrada del usuario** para decidir qué pipeline de procesamiento aplicar.

**Mecanismo:** una primera petición a Claude clasifica la entrada en categorías predefinidas. Según esa clasificación, el sistema enruta a un pipeline especializado con prompts y herramientas propios.

**Ejemplo:**

1. El usuario introduce un tema — *"funciones de Python"*.
2. Claude lo categoriza — *"educativo"*.
3. El sistema usa la plantilla específica de temas educativos.
4. Claude genera el guion con el tono y la estructura adecuados.

**Beneficio:** la salida encaja con la naturaleza del tema. Los temas de programación reciben tratamiento educativo con definiciones y explicaciones; los de entretenimiento, lenguaje de tendencia y ganchos.

**Estructura:** un paso de enrutado → múltiples pipelines especializados → cada uno con sus prompts y herramientas.

---

## Agentes y herramientas

**Agentes** = sistemas de IA que **crean un plan** para completar la tarea usando las herramientas que les das. Eficaces cuando **no se conocen los pasos exactos**.

**Ventajas:** flexibilidad para resolver tareas variadas con el mismo conjunto de herramientas, y capacidad de **combinarlas de formas inesperadas**.

### El principio de abstracción de herramientas

> **Da herramientas genéricas y abstractas, no hiperespecializadas.**

| ✅ Abstractas | ❌ Especializadas |
|---|---|
| `bash` | `refactor_tool` |
| `web_fetch` | `install_dependencies` |
| `file_write` | |

Es lo que hace Claude Code: pocas herramientas flexibles.

**Ejemplo de combinación:** `get_current_datetime` + `add_duration` + `set_reminder` resuelven multitud de tareas relacionadas con el tiempo mediante combinaciones distintas.

**Comportamiento del agente:** puede pedir información adicional cuando la necesita, combina herramientas de forma creativa, y **funciona mejor con un conjunto pequeño de herramientas flexibles**.

## Inspección del entorno

**Environment inspection** = que el agente **evalúe su entorno y el resultado de sus acciones** para entender el progreso y manejar errores.

> **La idea:** tras cada acción, el agente necesita mecanismos de feedback **más allá del valor que devuelve la herramienta**, para entender el nuevo estado del entorno.

**Ejemplos:**

- **Computer use** — Claude toma una **captura después de cada acción** (escribir, hacer clic) para ver cómo cambió el entorno, porque no puede predecir el resultado exacto de pulsar un botón.
- **Edición de código** — antes de modificar un fichero, el agente debe **leer su contenido actual** para conocer el estado existente.
- **Agente de vídeo para redes** — usar Whisper CPP vía bash para generar subtítulos con marcas de tiempo y verificar la colocación del diálogo; usar FFmpeg para extraer capturas del vídeo a intervalos e inspeccionar el resultado visual; validar que el vídeo cumple lo esperado antes de publicar.

**El beneficio:** permite al agente **medir su progreso, detectar errores y adaptarse** a resultados inesperados, en vez de operar a ciegas.

---

## Workflows vs. agentes — la comparación final

| | Workflows | Agentes |
|---|---|---|
| **Qué son** | Serie predefinida de llamadas, con los pasos exactos conocidos | Enfoque flexible con herramientas básicas que Claude combina |
| **División de la tarea** | En subtareas pequeñas y específicas → **más foco y precisión** | Afrontan retos variados de forma creativa, sin pasos predeterminados |
| **Pruebas y evaluación** | **Más fáciles de probar**, la secuencia se conoce | **Más difíciles**, la ruta de ejecución es impredecible |
| **Experiencia de usuario** | Requieren entradas específicas | Crean sus propias entradas a partir de la consulta y **pueden pedir más** |
| **Tasa de éxito** | **Más alta**, por el enfoque estructurado | **Más baja**, por la complejidad delegada |

### La recomendación del curso

> **Prioriza los workflows por fiabilidad. Usa agentes solo cuando la flexibilidad haga falta de verdad.**
>
> **Los usuarios quieren productos que funcionen al 100%, no agentes vistosos.**

**El principio de cierre:**

> ### Resuelve los problemas de forma fiable primero. Innova después.
