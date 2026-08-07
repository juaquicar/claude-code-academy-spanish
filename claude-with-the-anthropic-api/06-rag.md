# 06 — RAG (Retrieval Augmented Generation)

Técnica para **consultar documentos grandes** con modelos de lenguaje.

**El problema:** cómo extraer información concreta de un documento de 100-1000+ páginas sin chocar con los límites de contexto.

## Las dos opciones

| | Opción 1 · Directa | Opción 2 · RAG |
|---|---|---|
| Qué haces | Meter el documento entero en el prompt | Trocear el documento y meter solo los trozos relevantes |
| Límites de tokens | **Choca con ellos** | Los evita |
| Eficacia | **Baja con prompts largos** | El modelo se centra en lo relevante |
| Coste | Alto | **Bajo** |
| Velocidad | Lenta | **Rápida** |
| Escala | Un documento | **Muchos documentos** |

**Contrapartidas de RAG:** más complejidad, requiere preprocesado, necesita un mecanismo de búsqueda, **no garantiza que los trozos tengan el contexto completo**, y hay varias estrategias de troceado posibles.

> **RAG cambia simplicidad por escalabilidad y eficiencia.** El reto está en definir qué es "relevante" y cuál es la estrategia de troceado óptima para tu caso.

## Estrategias de troceado

> **La calidad del troceado impacta directamente en el rendimiento de RAG.** Un troceado malo recupera contexto irrelevante — el ejemplo del curso: texto médico sobre un "bug" recuperado para una consulta de ingeniería de software sobre bugs.

### 1 · Por tamaño

Dividir en cadenas de igual longitud.

- ✓ Fácil de implementar, **la más común en producción**.
- ✗ Corta palabras a la mitad, pierde contexto.
- **Solución: solapamiento** — incluir caracteres de los trozos vecinos.
- Contrapartida: duplica texto, pero mejora el significado de cada trozo.

### 2 · Por estructura

Dividir según la estructura del documento: encabezados, párrafos, secciones.

- Mejor para documentos estructurados: markdown, HTML.
- ✗ **Requiere que el formato esté garantizado.**
- Ejemplo: partir por encabezados markdown (`##`) para crear trozos por sección.

### 3 · Semántico

Usar NLP para agrupar frases y secciones relacionadas.

- La técnica más avanzada.
- Agrupa frases consecutivas según su similitud semántica.
- Implementación compleja.

### Cómo elegir

| Granularidad | Cuándo |
|---|---|
| **Por carácter** | El recurso más fiable: funciona con cualquier documento |
| **Por frase** | Buen término medio, si la detección de frases funciona bien |
| **Por sección** | Resultados óptimos, pero exige entrada estructurada |

> **No hay un método universalmente mejor.** Depende de qué garantías tengas sobre la estructura del documento y de tu caso de uso.

## Embeddings de texto

**Text embedding** = representación numérica del **significado** del texto, generada por un modelo de embeddings.

- El modelo recibe texto y devuelve una lista larga de números, en rango **-1 a +1**.
- Cada número es una puntuación que representa **cualidades desconocidas** del texto. En teoría cada uno puntúa un aspecto distinto —alegría, relevancia temática—, pero **su significado real es desconocido para quien los usa**.

**Búsqueda semántica** = usar embeddings para encontrar los trozos relacionados con la pregunta del usuario. Resuelve el problema de emparejar consultas con trozos relevantes.

> **La idea:** los embeddings permiten emparejar por **similitud semántica** en vez de por coincidencia de palabras clave.

**Implementación:** Anthropic recomienda **Voyage AI** para generar embeddings. Requiere cuenta y clave aparte; empezar es gratis y la integración por SDK es sencilla.

## El flujo RAG completo

Siete pasos que combinan troceado, embeddings y búsqueda vectorial.

**Preprocesado (1-4):**

| Paso | Qué pasa |
|---|---|
| **1 · Troceado** | Partir los documentos fuente en piezas |
| **2 · Embeddings** | Convertir cada trozo en un vector numérico |
| **3 · Normalización** | Escalar la magnitud de los vectores a 1.0 — **lo hacen las APIs de embeddings automáticamente** |
| **4 · Base de datos vectorial** | Guardar los embeddings en una base optimizada para operaciones con vectores |

**En tiempo real (5-7):**

| Paso | Qué pasa |
|---|---|
| **5 · Consulta** | Convertir la pregunta del usuario en embedding **con el mismo modelo** |
| **6 · Búsqueda por similitud** | Encontrar los embeddings más parecidos con **similitud coseno** |
| **7 · Ensamblar el prompt** | Combinar la pregunta con los trozos recuperados y enviarlo al LLM |

### Las matemáticas mínimas

- **Similitud coseno** = coseno del ángulo entre dos vectores. Devuelve de **-1 a 1**; **más cerca de 1 = más similar**.
- **Distancia coseno** = 1 menos la similitud. **Más cerca de 0 = más similar.**
- **Base de datos vectorial** = hace esos cálculos para encontrar los embeddings más cercanos.

## Implementarlo

| Paso | Código |
|---|---|
| **1 · Trocear** | `chunk_by_section` sobre el fichero `report.MD` |
| **2 · Embeddings** | `generate_embedding` — acepta una cadena o una lista |
| **3 · Poblar el store** | Crear la instancia del índice y, con `zip()`, recorrer los pares trozo-embedding: `store.add_vector(embedding, {content: chunk})` |
| **4 · Consulta** | Generar el embedding de la pregunta del usuario |
| **5 · Buscar** | `store.search(user_embedding, 2)` → los 2 trozos más relevantes con su distancia coseno |

> ⚠ **Guarda el texto original junto al embedding.** Sin los metadatos con el contenido, los resultados de la búsqueda no te sirven de nada.

En el ejemplo, distancias de 0,71 y 0,72 para la sección dos y la de metodología.

## BM25 · búsqueda léxica

**BM25** (*Best Match 25*) = algoritmo de búsqueda **léxica** que complementa a la semántica.

**El problema de la búsqueda semántica sola:** puede **pasar por alto coincidencias exactas de términos**, devolviendo resultados irrelevantes aunque un término específico aparezca muchas veces en ciertos documentos.

**Búsqueda híbrida** = combinar semántica (embeddings) y léxica (BM25) **en paralelo**, y luego fusionar los resultados.

**Los cuatro pasos de BM25:**

1. **Tokenizar** la consulta en términos separados: quitar puntuación, partir por espacios.
2. **Contar la frecuencia** de cada término en todos los trozos.
3. **Asignar importancia relativa** según esa frecuencia — **términos raros = más importancia**; comunes como "a" = menos.
4. **Rankear** los trozos según cuántos términos de alto peso contienen.

> **La idea:** los términos que aparecen mucho en todo el corpus son **menos** relevantes para la búsqueda que los términos raros y específicos.

**Ventajas:** encuentra mejor las coincidencias exactas y prioriza documentos con términos raros. Compensa las debilidades de la búsqueda semántica.

Ambos sistemas exponen APIs parecidas (`add_document`, `search`), lo que los hace fáciles de combinar.

## Pipeline RAG multi-índice

Sistema que combina **índice vectorial** (semántico) e **índice BM25** (léxico).

**Componentes:**

- **Vector Index** — búsqueda por similitud semántica.
- **BM25 Index** — búsqueda por palabras clave.
- **Retriever** — clase envoltorio que reenvía la consulta a ambos índices y fusiona resultados.

### Reciprocal Rank Fusion

Técnica para fusionar resultados de índices distintos:

```
RRF_score = Σ (1 / (rank + 1))   por cada método de búsqueda
```

Los documentos se ordenan por la puntuación combinada más alta.

> **Ejemplo:** vectorial devuelve `[doc2, doc7, doc6]`, BM25 devuelve `[doc6, doc2, doc7]`. Tras RRF el orden final es `[doc2, doc6, doc7]`, porque **doc2 salió alto en ambos**.

**Beneficios:** mejor precisión al combinar paradigmas distintos, diseño modular con API estandarizada (`search()` y `add_document()`), fácil de extender con más índices, y mejor manejo de los casos donde un método solo falla.

## Reranking

Paso de **postprocesado** que usa un LLM para **reordenar los resultados por relevancia** después de la recuperación inicial.

**Proceso:** búsqueda vectorial + BM25 → fusionar → pasar al LLM con un prompt que le pida ordenar por relevancia → resultados reordenados.

**Detalles de implementación:** usa **IDs de documento en vez del texto completo**, por eficiencia. El LLM recibe la consulta del usuario + los documentos candidatos + la instrucción de devolver los más relevantes en orden decreciente. Pre-fill del mensaje de asistente + stop sequence para asegurar salida JSON estructurada.

**Contrapartidas:** sube la precisión aprovechando la comprensión semántica del LLM, pero **añade latencia** por la llamada extra. Es especialmente eficaz cuando la recuperación inicial se pierde matices de la intención.

> **Ejemplo:** la consulta *"¿qué hizo el equipo de ingeniería con el incidente de 2023?"* priorizó correctamente la sección de ingeniería de software sobre la de ciberseguridad **tras el reranking**, pese a que la búsqueda híbrida la había puesto más abajo. El matiz era *"ENG team"* vs *"engineering team"*.

## Contextual retrieval

Técnica para mejorar la precisión **añadiendo contexto a cada trozo antes de generar su embedding**.

**El problema:** al partir el documento, **cada trozo pierde el contexto del original**, y eso reduce la precisión de recuperación.

**El proceso:**

1. Tomas el trozo individual + el documento fuente.
2. Los envías a Claude pidiéndole que genere **contexto de situación**.
3. El LLM genera un contexto breve que explica la relación del trozo con el documento completo.
4. Unes ese contexto con el trozo original = **trozo contextualizado**.
5. Usas el trozo contextualizado como entrada de los índices vectorial y BM25.

**Si el documento fuente no cabe en un solo prompt**, estrategia de contexto selectivo:

- Incluir los **trozos iniciales (1-3)** del documento, para el resumen o abstract.
- Incluir los trozos **inmediatamente anteriores** al objetivo, para contexto local.
- **Saltarse los trozos intermedios**, que aportan menos.

**Implementación:** `add_context` recibe el trozo + el texto fuente, genera el contexto vía LLM, lo concatena y devuelve la versión contextualizada.

> **Beneficio:** los trozos conservan sus vínculos con la estructura del documento y sus referencias cruzadas, lo que mejora la recuperación en documentos complejos con secciones interconectadas.
