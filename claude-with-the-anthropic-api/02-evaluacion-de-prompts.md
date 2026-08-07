# 02 — Evaluación de prompts

**Prompt engineering** = técnicas para escribir y editar prompts que ayuden a Claude a entender la petición y la respuesta deseada.

**Prompt evaluation** = **pruebas automatizadas** de prompts con métricas objetivas para medir su eficacia.

## Las tres salidas después de escribir un prompt

1. Probarlo una o dos veces y desplegarlo a producción. → **trampa**
2. Probarlo con entradas propias y hacer ajustes menores para casos límite. → **trampa**
3. Pasarlo por un **pipeline de evaluación** para obtener una puntuación objetiva. → **recomendado**

> **La idea del capítulo:** los ingenieros **infra-prueban los prompts** de forma sistemática. Usa un pipeline de evaluación para tener puntuaciones objetivas **antes** de iterar y desplegar.

## El workflow típico de eval

Proceso iterativo de **6 pasos**:

| Paso | Qué haces |
|---|---|
| **1 · Prompt inicial** | Escribe un borrador de referencia que optimizar |
| **2 · Dataset de evaluación** | Colección de entradas de prueba. Pueden ser **3 ejemplos o miles**, escritos a mano o generados por LLM |
| **3 · Variaciones del prompt** | Interpola cada entrada del dataset en la plantilla del prompt |
| **4 · Respuestas del LLM** | Pasa cada variación por Claude y recoge las salidas |
| **5 · Puntuar** | Un grader puntúa cada respuesta (p. ej. de 1 a 10) y se promedia para el rendimiento global |
| **6 · Iterar** | Modifica el prompt según las puntuaciones, repite el proceso, compara versiones |

> **No existe una metodología estándar.** Hay muchas herramientas open-source y de pago, pero puedes empezar simple con una implementación propia. La complejidad del grading varía. Lo que importa es que la puntuación objetiva permite mejorar el prompt de forma sistemática, comparando A/B.

## Generar datasets de prueba

**Objetivo del ejemplo del curso:** un prompt de asistencia con AWS que devuelva **solo** Python, configuración JSON o una regex, sin explicaciones.

**Cómo montar el dataset:** a mano, o automatizado con Claude — **usa modelos rápidos como Haiku** para generarlo.

**Estructura:** array de objetos JSON con una propiedad `task` que describe la petición del usuario.

**Proceso de generación:**

1. Pide a Claude que cree los casos de prueba.
2. Usa **pre-fill** con el mensaje de asistente ` ```json `.
3. Fija la **stop sequence** ` ``` `.
4. Parsea la respuesta como JSON.
5. Guárdalo en fichero.

La función `generate_dataset()` hace todo eso y deja un `dataset.json` para usar después.

## Ejecutar la eval

**Caso de prueba** = un registro individual del dataset, un objeto JSON.

**Tres funciones núcleo:**

| Función | Qué hace |
|---|---|
| `run_prompt` | Fusiona el caso de prueba con el prompt, lo envía a Claude, devuelve la salida |
| `run_test_case` | Llama a `run_prompt`, puntúa el resultado, devuelve un diccionario resumen |
| `run_eval` | Recorre el dataset, llama a `run_test_case` por cada caso, ensambla los resultados |

**Estructura del prompt v1** (punto de partida): *"Please solve the following task: [test_case_task]"*.

**Limitaciones de esa v1:** sin instrucciones de formato de salida, puntuación fija a 10 codificada a mano, respuestas de Claude demasiado verbosas.

**Tiempo de ejecución:** ~31 segundos con Haiku para el dataset completo.

**Formato de salida:** array de objetos con la salida de Claude, el caso de prueba original y la puntuación.

> **El núcleo del pipeline de eval es: dataset + prompt + LLM + grader.** Con muy poco código.

## Grading por modelo

Sistema de evaluación que toma las salidas del modelo y les asigna **puntuaciones objetivas** — típicamente escala 1-10, donde 10 es la máxima calidad.

### Los tres tipos de grader

| Tipo | Qué es | Ventajas / límites |
|---|---|---|
| **Code graders** | Comprobaciones programáticas: longitud, presencia de palabras, validación de sintaxis, índices de legibilidad | Rápidos y deterministas |
| **Model graders** | **Una llamada adicional al API** que evalúa la salida original | Muy flexibles para calidad y seguimiento de instrucciones |
| **Human graders** | Una persona evalúa las respuestas | Los más flexibles, pero lentos y tediosos |

**Requisitos:** debe devolver una **señal objetiva** —normalmente una puntuación numérica— y hay que **definir los criterios por adelantado**.

### Patrón de implementación de un model grader

- Crea un prompt detallado que pida **fortalezas, debilidades, razonamiento y puntuación** — no solo la puntuación.

> ⚠ Pedir solo la puntuación hace que el modelo tienda a dar valores mediocres por defecto. Pedirle que razone primero lo evita.

- Usa formato de respuesta JSON con pre-fill y stop sequences.
- Parsea el JSON para sacar puntuación y razonamiento.
- Calcula la media entre casos de prueba para la métrica final.

> Los model graders son muy flexibles pero **pueden ser inconsistentes**. Aun así dan una referencia objetiva para optimizar.

## Grading por código

Validación automatizada de salidas que contienen código, JSON o regex.

```python
validate_json()    # intenta parsear JSON      → 10 si válido, 0 si error
validate_python()  # intenta parsear el AST    → 10 si válido, 0 si error
validate_regex()   # intenta compilar la regex → 10 si válido, 0 si error
```

**Requisito del dataset:** debe incluir una clave **`format`** que especifique el tipo de salida esperado (JSON / Python / RegEx). Se añade modificando la plantilla del prompt de generación automática del dataset.

**Prompt engineering asociado:**

- Indica al modelo que responda **solo** con el código, JSON o regex crudo.
- Sin comentarios, explicaciones ni comentarios adicionales.
- Pre-fill del mensaje de asistente con el bloque de código y stop sequences para extraer la salida limpia.

**Sistema de puntuación:**

```
puntuación final = (puntuación_del_modelo + puntuación_de_sintaxis) / 2
```

Combina la **evaluación semántica** con la **validación sintáctica**: mide a la vez que sea correcto y que sea técnicamente válido.

> ⚠ **Limitación:** requiere conocer el formato esperado para elegir el validador correcto.
