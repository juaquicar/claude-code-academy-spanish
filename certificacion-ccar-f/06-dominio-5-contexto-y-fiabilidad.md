# 6 · Dominio 5 — Context Management & Reliability

**Peso: 15 %** · ~9 de los 60 ítems. Seis task statements. Es el dominio que menos pesa, pero **aparece como dominio secundario en cinco de los seis escenarios**.

---

## 5.1 · Preservar información crítica en interacciones largas

### Conocimiento

- **Riesgos de la summarización progresiva:** condensar valores numéricos, porcentajes, fechas y expectativas dichas por el cliente en resúmenes vagos.
- El efecto **"lost in the middle"**: los modelos procesan de forma fiable la información del **principio y del final** de entradas largas, pero pueden **omitir hallazgos de las secciones intermedias**.
- Los resultados de herramienta **se acumulan en contexto y consumen tokens de forma desproporcionada a su relevancia** (40+ campos por consulta de pedido cuando solo 5 son relevantes).
- Hay que **pasar el historial completo de conversación** en las peticiones siguientes para mantener coherencia conversacional.

### Habilidades

- Extraer los **hechos transaccionales** (importes, fechas, números de pedido, estados) a un bloque persistente de **"case facts"** que se incluye en cada prompt, **fuera del historial resumido**.
- Extraer y persistir datos estructurados de incidencia (IDs de pedido, importes, estados) en **una capa de contexto aparte** para sesiones con varios asuntos.
- **Recortar las salidas verbosas** a los campos relevantes **antes** de que se acumulen en contexto.
- **Colocar los resúmenes de hallazgos clave al principio** de las entradas agregadas y organizar el detalle con cabeceras de sección explícitas, para mitigar los efectos de posición.
- Exigir a los subagentes que **incluyan metadatos** (fechas, ubicación de la fuente, contexto metodológico) en sus salidas estructuradas, para que la síntesis de aguas abajo sea precisa.
- Modificar los agentes de aguas arriba para que devuelvan **datos estructurados** (hechos clave, citas, puntuaciones de relevancia) en lugar de contenido verboso y cadenas de razonamiento, cuando los de aguas abajo tienen presupuesto de contexto limitado.

---

## 5.2 · Escalado y resolución de ambigüedad

### Los tres disparadores válidos de escalado

1. **El cliente pide un humano** explícitamente.
2. **Excepción o hueco de política** — no simplemente "el caso es complejo".
3. **Incapacidad de progresar** de forma significativa.

### Conocimiento

- La distinción entre **escalar de inmediato cuando el cliente lo exige explícitamente** y **ofrecer resolverlo** cuando el asunto es sencillo.
- Por qué el **escalado por sentimiento** y las **puntuaciones de confianza autoinformadas** son proxies **poco fiables** de la complejidad real del caso.
- Cómo varias coincidencias de cliente exigen **pedir aclaración** (identificadores adicionales) en lugar de **elegir por heurística**.

### Habilidades

- Añadir criterios de escalado explícitos **con ejemplos few-shot** al system prompt, mostrando cuándo escalar y cuándo resolver de forma autónoma.
- **Honrar de inmediato** la petición explícita de un agente humano, sin investigar primero.
- Reconocer la frustración **y a la vez ofrecer resolución** cuando el asunto está dentro de la capacidad del agente, escalando solo si el cliente reitera su preferencia.
- Escalar cuando la política es **ambigua o guarda silencio** sobre la petición concreta (igualar el precio de un competidor cuando la política solo contempla ajustes de precio propios).
- Instruir al agente a **pedir identificadores adicionales** cuando la tool devuelve múltiples coincidencias.

> **Trampa.** La confianza autoinformada por el LLM está **mal calibrada**: si el agente ya es incorrectamente confiado en los casos difíciles, un umbral sobre esa confianza no arregla nada. Y el sentimiento **no correlaciona con la complejidad**.

---

## 5.3 · Propagación de errores en sistemas multiagente

### Conocimiento

- El **contexto de error estructurado** —tipo de fallo, consulta intentada, resultados parciales, enfoques alternativos— es lo que permite al coordinador **decidir la recuperación con criterio**.
- La distinción entre **fallo de acceso** (timeout: hay que decidir si reintentar) y **resultado vacío válido** (consulta correcta sin coincidencias).
- Por qué los estados de error genéricos (*"search unavailable"*) **esconden contexto valioso** al coordinador.
- Por qué **suprimir errores en silencio** (devolver vacío como éxito) y **terminar el workflow entero ante un solo fallo** son **ambos antipatrones**.

### Habilidades

- Devolver contexto de error estructurado que incluya tipo de fallo, qué se intentó, resultados parciales y alternativas posibles.
- Distinguir en el reporte los fallos de acceso de los resultados vacíos válidos.
- Que los subagentes hagan **recuperación local** de fallos transitorios y **solo propaguen** lo que no pueden resolver, incluyendo qué intentaron y qué resultados parciales tienen.
- Estructurar la salida de síntesis con **anotaciones de cobertura**: qué hallazgos están bien sustentados y qué áreas tienen **huecos por fuentes no disponibles**.

---

## 5.4 · Gestión de contexto en exploración de codebases grandes

### Conocimiento

- **Degradación del contexto en sesiones largas**: el modelo empieza a dar respuestas inconsistentes y a referirse a *"patrones típicos"* en vez de a las clases concretas que descubrió antes.
- El papel de los **ficheros scratchpad** para persistir hallazgos clave a través de las fronteras de contexto.
- **Delegación a subagentes** para aislar la salida verbosa de exploración mientras el agente principal coordina la comprensión de alto nivel.
- **Persistencia de estado estructurada para recuperación ante caídas**: cada agente exporta su estado a una ubicación conocida y el coordinador carga un **manifiesto** al reanudar.

### Habilidades

- Lanzar subagentes para investigar preguntas concretas ("encuentra todos los ficheros de test", "traza las dependencias del flujo de reembolso") mientras el principal conserva la coordinación de alto nivel.
- Mantener **ficheros scratchpad** con los hallazgos clave y consultarlos en preguntas posteriores, para contrarrestar la degradación.
- **Resumir los hallazgos de una fase antes de lanzar los subagentes de la siguiente**, inyectando esos resúmenes en el contexto inicial.
- Diseñar recuperación ante caídas mediante **exportaciones de estado estructuradas (manifiestos)** que el coordinador carga al reanudar e inyecta en los prompts.
- Usar **`/compact`** para reducir el uso de contexto en sesiones de exploración largas cuando el contexto se llena de descubrimiento verboso.

---

## 5.5 · Revisión humana y calibración de confianza

### Conocimiento

- El riesgo de que las **métricas agregadas** (por ejemplo, 97 % global) **enmascaren mal rendimiento** en tipos de documento o campos concretos.
- **Muestreo aleatorio estratificado** para medir tasas de error en extracciones de alta confianza y detectar patrones de error nuevos.
- Puntuaciones de confianza **a nivel de campo**, calibradas con **conjuntos de validación etiquetados**, para enrutar la atención de revisión.
- La importancia de **validar la precisión por tipo de documento y por segmento de campo** antes de automatizar las extracciones de alta confianza.

### Habilidades

- Implementar muestreo aleatorio estratificado de las extracciones de alta confianza para medir tasa de error de forma continua y detectar patrones nuevos.
- Analizar la precisión **por tipo de documento y por campo** para verificar rendimiento consistente en todos los segmentos **antes** de reducir la revisión humana.
- Hacer que el modelo emita confianza por campo y **calibrar los umbrales de revisión con conjuntos etiquetados**.
- Enrutar a revisión humana las extracciones de baja confianza o con documentos origen ambiguos/contradictorios, priorizando la capacidad limitada de los revisores.

---

## 5.6 · Procedencia de la información e incertidumbre en síntesis multi-fuente

### Conocimiento

- Cómo **se pierde la atribución de fuente durante los pasos de summarización**, cuando los hallazgos se comprimen sin preservar el mapeo afirmación↔fuente.
- La importancia de **mapeos claim–source estructurados** que el agente de síntesis debe **preservar y fusionar** al combinar hallazgos.
- Cómo tratar **estadísticas en conflicto de fuentes creíbles**: **anotar el conflicto con atribución**, no elegir un valor arbitrariamente.
- **Datos temporales:** exigir fechas de publicación o de recogida en las salidas estructuradas, para que las diferencias temporales **no se interpreten como contradicciones**.

### Habilidades

- Exigir a los subagentes que emitan mapeos claim–source estructurados (URLs, nombres de documento, extractos relevantes) que los agentes de aguas abajo **preserven a través de la síntesis**.
- Estructurar informes con secciones explícitas que **distinguen hallazgos bien establecidos de hallazgos contestados**, preservando la caracterización original de la fuente y el contexto metodológico.
- Completar el análisis del documento **incluyendo los valores en conflicto y anotándolos explícitamente**, dejando que el coordinador decida cómo reconciliar antes de pasar a síntesis.
- Exigir fechas de publicación o de recogida en las salidas estructuradas.
- **Renderizar cada tipo de contenido como toca** en la síntesis —datos financieros como tabla, noticias como prosa, hallazgos técnicos como listas estructuradas— en vez de convertirlo todo a un formato uniforme.

---

## Conclusiones del dominio

- Los hechos duros van a un bloque **"case facts" persistente**, fuera del resumen.
- **Lost in the middle:** lo importante al principio (o al final), nunca enterrado.
- **Recorta la salida de las tools** antes de que se acumule.
- Escalado: **petición explícita, hueco de política, incapacidad de progresar**. Ni sentimiento ni autoconfianza.
- Error genérico = coordinador ciego. **Estructurado, con parciales y alternativas.**
- Sesión larga ⇒ **scratchpad**, **subagentes**, **`/compact`**, **manifiestos** para recuperarse de caídas.
- El **97 % global esconde** un 60 % en un tipo de documento. **Estratifica.**
- **Los conflictos se anotan, no se resuelven** por tu cuenta.

---

**Anterior:** [5 · Dominio 4](05-dominio-4-prompting-y-salida-estructurada.md) · **Siguiente:** [7 · Los seis escenarios](07-los-seis-escenarios.md)
