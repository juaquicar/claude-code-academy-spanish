# 5 · Dominio 4 — Prompt Engineering & Structured Output

**Peso: 20 %** · ~12 de los 60 ítems. Seis task statements.

Escenarios que lo tocan: *Claude Code for Continuous Integration*, *Structured Data Extraction*.

---

## 4.1 · Criterios explícitos para ganar precisión y bajar falsos positivos

### Conocimiento

- **Criterios explícitos por encima de instrucciones vagas.** Ejemplo del propio material: *"marca un comentario solo cuando el comportamiento que afirma contradice el comportamiento real del código"* frente a *"comprueba que los comentarios son precisos"*.
- Instrucciones generales como *"sé conservador"* o *"reporta solo hallazgos de alta confianza"* **no mejoran la precisión** comparadas con criterios categóricos específicos.
- El impacto de la tasa de falsos positivos en la **confianza del desarrollador**: una categoría con muchos falsos positivos **socava la confianza en las categorías que sí aciertan**.

### Habilidades

- Escribir criterios de revisión específicos que definen **qué reportar** (bugs, seguridad) y **qué saltar** (estilo menor, patrones locales), en vez de filtrar por confianza.
- **Desactivar temporalmente** las categorías con muchos falsos positivos para recuperar la confianza del equipo mientras se mejora el prompt de esas categorías.
- Definir criterios de severidad explícitos **con ejemplos de código concretos por nivel** para lograr clasificación consistente.

---

## 4.2 · Few-shot para consistencia y calidad

### Conocimiento

- Los ejemplos few-shot son **la técnica más eficaz** para conseguir salida consistentemente formateada y accionable cuando las instrucciones detalladas por sí solas dan resultados inconsistentes.
- Su papel al **demostrar el manejo de casos ambiguos** (selección de tool para peticiones ambiguas, huecos de cobertura de test a nivel de rama).
- Permiten al modelo **generalizar el criterio a patrones nuevos**, no solo casar los casos preespecificados.
- Son eficaces para **reducir alucinación en tareas de extracción** (medidas informales, estructuras de documento variadas).

### Habilidades

- Crear **2-4 ejemplos dirigidos** para escenarios ambiguos que **muestran el razonamiento** de por qué se eligió una acción sobre otra plausible.
- Incluir ejemplos que demuestran el formato de salida deseado (ubicación, problema, severidad, arreglo sugerido).
- Dar ejemplos que **distinguen patrones de código aceptables de problemas reales**, reduciendo falsos positivos **sin perder generalización**.
- Demostrar el manejo correcto de estructuras variadas (citas inline frente a bibliografía; secciones de metodología frente a detalles embebidos).
- Añadir ejemplos de extracción correcta en documentos con formatos distintos para corregir extracciones vacías o nulas de campos obligatorios.

---

## 4.3 · Forzar salida estructurada con tool use y JSON schemas

### Conocimiento

- **`tool_use` con JSON schema es el enfoque más fiable** para salida garantizada conforme al esquema: **elimina los errores de sintaxis JSON**.
- Los tres modos de `tool_choice`:

  | Valor | Comportamiento |
  |---|---|
  | `"auto"` | El modelo **puede devolver texto** en vez de llamar a una tool |
  | `"any"` | **Debe** llamar a una tool, pero elige cuál |
  | `{"type":"tool","name":"..."}` | Debe llamar **a esa tool concreta** |

- Los esquemas estrictos **eliminan errores de sintaxis pero no errores semánticos**: líneas de detalle que no suman el total, valores en el campo equivocado.
- Diseño del esquema: campos obligatorios frente a opcionales, y **enums con patrón `"other"` + campo de detalle** para categorías extensibles.

### Habilidades

- Definir tools de extracción con el JSON schema como parámetros de entrada y sacar los datos de la respuesta `tool_use`.
- Poner **`tool_choice: "any"`** para garantizar salida estructurada cuando hay **varios esquemas de extracción** y el tipo de documento es desconocido.
- **Forzar** una tool concreta con `{"type": "tool", "name": "extract_metadata"}` para asegurar que esa extracción corre antes de los pasos de enriquecimiento.
- Diseñar campos como **opcionales (nullable)** cuando el documento origen puede no contener la información: **evita que el modelo invente valores** para satisfacer campos obligatorios.
- Añadir valores de enum como `"unclear"` para casos ambiguos, y `"other"` + campo de detalle para categorización extensible.
- Incluir **reglas de normalización de formato en el prompt** junto al esquema estricto, para manejar formatos de origen inconsistentes.

> **Trampa.** El esquema estricto no valida semántica. Si el problema es "las líneas no suman el total", la solución **no** es un esquema más estricto: es validación semántica (ver 4.4).

---

## 4.4 · Validación, reintentos y bucles de feedback

### Conocimiento

- **Retry-with-error-feedback:** añadir los errores de validación concretos al prompt del reintento para guiar la corrección.
- **Los límites del reintento:** son inútiles cuando la información sencillamente **no está en el documento origen** (a diferencia de errores de formato o estructura).
- Diseño del bucle de feedback: registrar qué construcciones disparan hallazgos (campo **`detected_pattern`**) para poder analizar sistemáticamente los patrones de descarte.
- La diferencia entre **errores semánticos de validación** (los valores no suman, campo equivocado) y **errores de sintaxis de esquema** (eliminados por tool use).

### Habilidades

- Implementar peticiones de seguimiento que incluyen **el documento original, la extracción fallida y los errores de validación concretos** para autocorrección.
- **Identificar cuándo el reintento no va a servir** (la información solo existe en un documento externo no aportado) frente a cuándo sí (desajustes de formato, errores estructurales de salida).
- Añadir `detected_pattern` a los hallazgos estructurados para analizar patrones de falso positivo cuando los desarrolladores los descartan.
- Diseñar flujos de autovalidación: extraer **`calculated_total` junto a `stated_total`** para marcar discrepancias; añadir booleanos **`conflict_detected`** para datos de origen inconsistentes.

---

## 4.5 · Procesamiento por lotes

### La Message Batches API

| Propiedad | Valor |
|---|---|
| Ahorro de coste | **50 %** |
| Ventana de procesamiento | Hasta **24 horas** |
| SLA de latencia | **Ninguno garantizado** |
| Tool calling multiturno dentro de una petición | **No soportado** |
| Correlación petición↔respuesta | Campo **`custom_id`** |

### Conocimiento y habilidades

- **Apropiado** para cargas no bloqueantes y tolerantes a latencia: informes nocturnos, auditorías semanales, generación de tests de madrugada.
- **Inapropiado** para workflows bloqueantes: comprobaciones pre-merge donde el desarrollador está esperando.
- Emparejar el enfoque de API con el requisito de latencia: **API síncrona para pre-merge bloqueante, batch para análisis nocturno/semanal**.
- **Calcular la frecuencia de envío** según el SLA: por ejemplo, ventanas de 4 horas para garantizar un SLA de 30 horas con 24 horas de procesamiento batch.
- Manejar fallos: **reenviar solo los documentos fallidos**, identificados por `custom_id`, con las modificaciones oportunas (trocear los que excedieron el límite de contexto).
- Refinar el prompt **sobre una muestra** antes de procesar grandes volúmenes, para maximizar el acierto en la primera pasada y reducir el coste de reenvíos.

---

## 4.6 · Arquitecturas de revisión multi-instancia y multi-pasada

### Conocimiento

- **Límites de la autorrevisión:** el modelo conserva el contexto de razonamiento de cuando generó, lo que le hace **menos propenso a cuestionar sus propias decisiones** en la misma sesión.
- Las **instancias de revisión independientes** —sin el razonamiento previo— son más eficaces que las instrucciones de "revísate a ti mismo" o que el extended thinking.
- **Revisión multipasada:** partir revisiones grandes en pasadas locales por fichero **más** pasadas de integración entre ficheros, para evitar **dilución de atención** y hallazgos contradictorios.

### Habilidades

- Usar una **segunda instancia independiente** de Claude para revisar el código generado, sin el contexto de razonamiento del generador.
- Partir revisiones multi-fichero grandes en pasadas por fichero (problemas locales) más pasadas de integración (flujo de datos entre ficheros).
- Ejecutar pasadas de verificación donde el modelo **autoinforma confianza junto a cada hallazgo**, para enrutar la revisión de forma calibrada.

> **Trampa.** Ante una revisión inconsistente de 14 ficheros, **un modelo con ventana de contexto mayor no arregla la calidad de atención**, y exigir consenso entre tres pasadas independientes **suprimiría bugs reales** que solo se detectan de forma intermitente. La respuesta es **partir en pasadas**.

---

## Conclusiones del dominio

- **Criterios categóricos, no filtros de confianza.** "Sé conservador" no hace nada.
- **Few-shot** es la técnica de mayor impacto para consistencia de formato y casos ambiguos: 2-4 ejemplos **con razonamiento**.
- `tool_use` + JSON schema **elimina sintaxis, no semántica**.
- Campos **nullable** para lo que puede no existir: es lo que evita la invención.
- El reintento arregla **formato**, no **ausencia de información**.
- Batch = 50 % más barato, 24 h, sin SLA, `custom_id`. **Nunca en un camino bloqueante.**
- **Quien escribe no revisa bien.** Instancia independiente.

---

**Anterior:** [4 · Dominio 3](04-dominio-3-claude-code.md) · **Siguiente:** [6 · Dominio 5 — Contexto y fiabilidad](06-dominio-5-contexto-y-fiabilidad.md)
