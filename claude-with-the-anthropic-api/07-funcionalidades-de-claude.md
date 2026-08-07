# 07 — Funcionalidades de Claude

Cinco capacidades que vienen dadas y no hay que construir.

---

## Extended thinking

Permite a Claude **razonar antes de generar la respuesta final**.

**Mecánica:**

- Muestra un **proceso de pensamiento separado**, visible para el usuario.
- **Aumenta la precisión** en tareas complejas, pero **añade coste** (se cobran los tokens de pensamiento) **y latencia**.
- **Thinking budget** = mínimo **1024 tokens** asignados a la fase de pensamiento.
- ⚠ **`max_tokens` debe superar el thinking budget**: con budget 1024, `max_tokens` ≥ 1025.

**Cuándo activarlo:**

> Actívalo **cuando optimizar el prompt no haya conseguido la precisión que buscas**. Usa evals para decidir si hace falta.

**Estructura de la respuesta:**

- **Bloque de pensamiento** — el texto de razonamiento + una **firma criptográfica**.
- **Bloque de texto** — la respuesta final.
- **La firma impide manipular el texto de pensamiento**. Es una medida de seguridad.

**Casos especiales — bloques de pensamiento redactados:** texto de pensamiento cifrado que los sistemas de seguridad han marcado. Se entregan igualmente para mantener la continuidad de la conversación sin perder contexto.

**Implementación:** `thinking=true` + el parámetro de budget, asegurando `max_tokens` > budget para que quede capacidad de respuesta.

---

## Soporte de imágenes

Claude puede procesar imágenes dentro de los mensajes de usuario: analizar, comparar, contar y describir.

**Límites:**

- Máximo **100 imágenes por petición**.
- Restricciones de tamaño y dimensiones.
- **Las imágenes consumen tokens**, calculados según alto y ancho en píxeles.

**Bloque de imagen** = tipo de bloque especial dentro del mensaje de usuario, que contiene **datos crudos en base64** o **una URL** a una imagen online. Se permiten varios bloques por mensaje.

> ⚠ **El factor crítico de éxito: la calidad del prompt.** Los prompts simples fallan a menudo. La precisión con imágenes **depende enteramente de lo sofisticado que sea el prompt, no de la calidad de la imagen**.

**Técnicas de prompting para imágenes:**

- Instrucciones de análisis **paso a paso**.
- Ejemplos one-shot / multi-shot, **alternando pares de imagen y texto**.
- Guidelines claras y pasos de verificación.
- Marcos de análisis estructurados.

**Ejemplo de caso de uso:** evaluación automática de riesgo de incendio a partir de imágenes de satélite, analizando densidad arbórea, acceso a la propiedad y voladizo del tejado, y asignando una puntuación numérica de riesgo.

**Implementación:** codifica la imagen en base64, crea el mensaje con el bloque de imagen (`type: image`, `source: base64`, `media_type`, `data`) seguido del bloque de texto con las instrucciones detalladas.

---

## Soporte de PDF

Claude lee ficheros PDF **directamente**, con código muy parecido al de imágenes.

Los cambios de implementación:

| | Imagen | PDF |
|---|---|---|
| Tipo de fichero | `"image"` | **`"document"`** |
| Media type | `"image/png"` | **`"application/pdf"`** |
| Variable | `image_bytes` | `file_bytes` |

**Qué extrae:** texto + imágenes + gráficas + tablas + contenido mixto.

> Es una solución **integral** para análisis documental: mismo patrón de uso que con imágenes, pero con parámetros de documento.

---

## Citations

Permite a Claude **referenciar los documentos fuente** y mostrar de dónde sale la información.

**Tipos de cita:**

| Tipo | Para qué | Qué muestra |
|---|---|---|
| `citation_page_location` | Documentos **PDF** | Índice del documento, título, página inicial, página final, texto citado |
| `citation_char_location` | **Texto plano** | Posición de caracteres dentro del bloque de texto |

**Implementación:**

- Añade `"citations": {"enabled": true}` a la petición.
- Añade un campo **`title`** para identificar el documento fuente.
- Funciona tanto con PDF como con texto plano.

**Estructura de la respuesta:** el contenido pasa a ser una **lista de bloques de texto**, algunos con un array `citations` con los datos de ubicación.

> **Para qué sirve de verdad:** transparencia. El usuario puede **verificar las fuentes** y comprobar si la interpretación de Claude es correcta, en vez de que parezca que habla de memoria.

**Beneficio de interfaz:** permite mostrar popups o superposiciones con el documento fuente, los números de página y el texto exacto citado al pasar el ratón por el contenido referenciado.

---

## Code execution y la Files API

### Files API

Permite **subir ficheros por adelantado** y referenciarlos después por **ID**, en vez de incluir los datos crudos en cada petición.

Flujo: subes el fichero → recibes un objeto de metadatos con el **ID** → usas el ID en peticiones futuras.

### Code execution

Herramienta **del lado del servidor** donde Claude **ejecuta código Python en contenedores Docker aislados**.

- **No hace falta implementación**: basta con incluir el esquema de herramienta predefinido.
- Claude puede ejecutar código **varias veces**, interpretar resultados y generar la respuesta final.

> ⚠ **Restricción clave: los contenedores Docker no tienen acceso a red.** La entrada y salida de datos depende de la integración con la Files API.

### El flujo combinado

1. Subes el fichero por la Files API.
2. Recibes el ID.
3. Incluyes el ID en un bloque de subida al contenedor.
4. Pides a Claude que lo analice.
5. Claude escribe y ejecuta código **con acceso al fichero subido**.
6. Devuelve el análisis y los resultados.

Claude también puede **generar ficheros** dentro del contenedor —gráficas, informes— que se descargan con los IDs devueltos en la respuesta.

**Casos de uso:** análisis de datos, procesamiento de ficheros, generación automática de código para tareas complejas. La respuesta contiene bloques de código, resultados de ejecución y el análisis final.
