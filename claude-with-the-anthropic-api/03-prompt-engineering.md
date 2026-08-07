# 03 — Prompt engineering

Mejorar los prompts para conseguir salidas más fiables y de mayor calidad.

**Estructura del módulo:** partir de un prompt inicial malo → aplicar las técnicas paso a paso → **evaluar la mejora después de cada una** → observar las ganancias acumuladas.

**El ejemplo:** generar un plan de comidas de un día para un atleta, a partir de altura, peso, objetivo físico y restricciones dietéticas.

## Las puntuaciones reales del curso

Esto es lo que hace valioso este capítulo: **cada técnica se mide**.

| Estado | Puntuación |
|---|---|
| Prompt inicial básico | **2,32** |
| + Ser claro y directo | **3,92** |
| + Ser específico (guidelines) | **7,86** |

> Espera puntuaciones malas al principio, sobre todo con modelos menos capaces. Suben conforme se aplican las técnicas.

## Montaje técnico

- Pipeline de eval actualizado con una **clase evaluadora flexible**.
- Soporta **concurrencia** — ajusta `max_concurrent_tasks` según tus límites de rate.
- `generate_dataset()` crea los casos de prueba con las entradas especificadas.
- `run_prompt()` procesa cada caso individualmente.
- **`prompt_input_spec`** — diccionario que define las entradas que el prompt necesita.
- **`extra_criteria`** — requisitos de validación adicionales para el grading por modelo.
- **`output.html`** — informe de evaluación formateado con los resultados y puntuaciones de cada caso.

**Proceso:** escribe el prompt inicial → interpola las entradas del caso → ejecuta la eval → aplica una técnica → vuelve a evaluar → repite hasta que el rendimiento te convenza.

---

## Técnica 1 · Ser claro y directo

Usa **lenguaje simple y directo con verbos de acción en la primera línea** del prompt para especificar la tarea exacta.

> **La primera línea es la parte más crítica del prompt**: sienta la base de toda la respuesta.

**Estructura:** verbo de acción + descripción clara de la tarea + especificación de la salida.

Ejemplos:

- *"**Write** three paragraphs about how solar panels work"*
- *"**Identify** three countries that use geothermal energy and for each include generation stats"*
- *"**Generate** a one day meal plan for an athlete that meets their dietary restrictions"*

**Componentes:** verbo de acción al principio + enunciado directo de la tarea + detalles de la salida esperada.

**Resultado medido: 2,32 → 3,92.**

## Técnica 2 · Ser específico

Añadir **guidelines o pasos** que dirijan la salida del modelo en una dirección concreta. Hay dos tipos:

| Tipo | Qué es | Qué controla |
|---|---|---|
| **A · Atributos** | Lista de cualidades deseadas en la salida: longitud, estructura, formato | **Las características de la salida** |
| **B · Pasos** | Pasos concretos que el modelo debe seguir en su razonamiento | **Cómo llega el modelo a la respuesta** |

**Cuándo usar cada uno:**

- **Tipo A (atributos)** — recomendable en **casi todos** los prompts.
- **Tipo B (pasos)** — para problemas complejos donde quieres que el modelo considere una perspectiva más amplia o puntos de vista adicionales que no consideraría por su cuenta.

En prompts profesionales **se combinan a menudo**.

**Resultado medido: 3,92 → 7,86.** Es el salto más grande de todo el capítulo.

## Técnica 3 · Estructurar con etiquetas XML

Usar etiquetas XML para **organizar y delimitar** las distintas secciones de contenido dentro del prompt.

**Para qué:** cuando interpolas grandes cantidades de contenido, las etiquetas ayudan al modelo a **distinguir entre tipos de información** y a entender cómo se agrupa el texto.

**Implementación:** envuelve las secciones en etiquetas descriptivas —`<sales_records></sales_records>`, `<my_code></my_code>`— en vez de volcar texto sin estructura.

> **Nombra las etiquetas de forma descriptiva y específica.** `sales_records` es mejor que `data`: aporta contexto sobre la naturaleza del contenido.

**Caso de uso:** un prompt de depuración que mezcla código y documentación se vuelve mucho más claro separado en `<my_code>` y `<docs>`.

**Beneficios:** hace obvia la estructura del prompt, reduce la confusión sobre dónde empieza y acaba cada cosa, y mejora la salida **incluso con bloques de contenido pequeños**.

> Puedes envolver cualquier contenido interpolado —`<athlete_information>`— aunque sea corto, solo para dejar claro que es una entrada externa a considerar.

## Técnica 4 · Dar ejemplos

**One-shot / multi-shot prompting** = incluir ejemplos en el prompt para guiar el comportamiento del modelo. *One-shot* = un ejemplo; *multi-shot* = varios.

**Implementación:** estructura los ejemplos con **etiquetas XML** que contengan la entrada de muestra y la salida ideal. **Envuélvelos siempre** con claridad para distinguirlos del contenido real del prompt.

**Dónde son más útiles:**

- **Casos límite** — detección de sarcasmo, escenarios raros.
- **Formatos de salida complejos** — estructuras JSON, formatos específicos.
- **Aclarar la calidad o el estilo** de respuesta esperados.

**Buenas prácticas:**

- Añade contexto para los casos límite: *"be especially careful with sarcasm"*.
- **Incluye el razonamiento** que explica por qué esa salida es la ideal.
- **Usa como plantilla los ejemplos con mejor puntuación de tus evals.** Es el bucle que cierra este bloque con el anterior.
- Coloca los ejemplos **después** de las instrucciones y guidelines principales.

> **Refuerzo:** combinar los ejemplos con una explicación de qué los hace ideales refuerza las características de salida que buscas.
