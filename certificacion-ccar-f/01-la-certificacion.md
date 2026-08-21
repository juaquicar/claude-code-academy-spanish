# 1 · La certificación, de un vistazo

> Fuente: **Claude Certified Architect – Foundations Exam Guide**, versión 1.0, efectiva julio 2026, código de examen `CCAR-F`. La guía es el documento autoritativo y avisa de que puede cambiar sin previo aviso. Descárgala: [Exam Guide (PDF)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf)

## Qué valida

Que sabes **decidir compromisos** al implementar soluciones reales con Claude. No es un examen de sintaxis: es de criterio de arquitectura sobre cuatro tecnologías —**Claude Code**, **Claude Agent SDK**, **Claude API** y **MCP**— las que se usan para construir aplicaciones en producción.

Las preguntas están ancladas en casos de cliente reales: sistemas agénticos de atención al cliente, pipelines de investigación multiagente, integración de Claude Code en CI/CD, herramientas de productividad para desarrolladores y extracción de datos estructurados de documentos.

## Ficha técnica

| Campo | Valor |
|---|---|
| Credencial | Claude Certified Architect – Foundations |
| Código de examen | `CCAR-F` (antes `CCA-F`) |
| Número de ítems | **60** |
| Formato de ítem | Multiple-choice y multiple-response. **Cada ítem dice cuántas respuestas hay que marcar** |
| Estructura | **4 escenarios sacados de un banco de 6** |
| Tiempo | **120 minutos** (calcula ~135 de butaca con check-in y encuesta) |
| Entrega | Proctored: online proctored y/o centro de examen, según la política del programa |
| Nota de corte | **Escalada de 720** sobre una escala de **100–1.000** |
| Precio | **125 USD** (subió desde 99 USD el 30 de junio de 2026) |
| Validez | **12 meses** desde la fecha de concesión |
| Informe de resultado | Apto/no apto con nota escalada, **más el porcentaje de acierto por dominio** |

> **Trampa de examen.** El porcentaje por dominio del informe **es solo informativo**. El apto/no apto se decide **únicamente con la nota escalada total**. No hay que aprobar dominio a dominio.

## Candidato ideal

Un **solution architect** que diseña e implementa aplicaciones de producción con Claude. Con las manos ya metidas en:

- Aplicaciones agénticas con el **Claude Agent SDK**: orquestación multiagente, delegación a subagentes, integración de herramientas y hooks de ciclo de vida.
- Configurar **Claude Code** para flujos de equipo: ficheros `CLAUDE.md`, Agent Skills, integraciones de servidores MCP y plan mode.
- Diseñar interfaces de **tools y resources MCP** para integrar sistemas de backend.
- Ingeniería de prompts que produce **salida estructurada fiable**: JSON schemas, ejemplos few-shot y patrones de extracción.
- Gestionar la **ventana de contexto** en documentos largos, conversaciones multiturno y traspasos entre agentes.
- Integrar Claude en **CI/CD** para revisión de código automatizada, generación de tests y feedback en pull requests.
- Decisiones de **escalado y fiabilidad**: manejo de errores, human-in-the-loop y patrones de autoevaluación.

Experiencia típica: **6+ meses** construyendo con las APIs de Claude, el Agent SDK, Claude Code y MCP, entendiendo tanto capacidades como **limitaciones** de los LLM en producción.

## El blueprint: pesos por dominio

Los pesos salen de un *job task analysis* y marcan la proporción aproximada de ítems puntuables de cada dominio.

| # | Dominio | Peso |
|---|---|---|
| 1 | Agentic Architecture & Orchestration | **27 %** |
| 2 | Tool Design & MCP Integration | **18 %** |
| 3 | Claude Code Configuration & Workflows | **20 %** |
| 4 | Prompt Engineering & Structured Output | **20 %** |
| 5 | Context Management & Reliability | **15 %** |
| | **Total** | **100 %** |

De 60 ítems, eso son aproximadamente **16 · 11 · 12 · 12 · 9**. El dominio 1 es el que más pesa: si vas justo de tiempo, empieza por ahí.

## Cómo se puntúa

Es una evaluación **criterion-referenced**: te miden contra un estándar fijo, **no contra otros candidatos**. Apruebas demostrando el conocimiento del blueprint, no superando a un percentil de compañeros.

La nota de corte se fijó con un **standard-setting study** formal: expertos entrenados juzgaron qué rendimiento se le exige a un *minimally qualified candidate*. La escala 100–1.000 con corte en 720 existe para **equiparar formas de examen** de dificultad ligeramente distinta.

## Registro y agenda

El flujo va por la **Anthropic Partner Academy** y luego **Pearson VUE**:

1. Entra en la página de tu certificación en la Anthropic Partner Academy y revisa los detalles.
2. Descarga el **Exam Guide** y revisa los *Certification Terms and Conditions* y la *Certification Exam Policy* **antes** de registrarte.
3. Regístrate y completa el checkout. El precio ya refleja el descuento de tu tier de partner.
4. Sigue las instrucciones de confirmación para **crear tu cuenta de Pearson VUE** y entra a agendar.
5. Elige fecha y modalidad: **online proctoring** o **centro de examen Pearson**.
6. Puedes **cancelar o reagendar hasta 24 horas antes**. Dentro de esas 24 horas pierdes la tasa.

> **Descuentos de partner.** Los partners Select, Preferred y Global Premier tienen **50 % automático** en checkout. Hasta el **31 de agosto de 2026**, los Global Premier tienen **100 % de descuento** en todos los exámenes. No hay compra por volumen todavía; hay una tienda de vouchers en marcha.

## Políticas

**Identificación.** Documento oficial con foto, vigente. El nombre del documento **debe coincidir exactamente** con el de tu registro. Para corregirlo, escribe a `certifications-support@anthropic.com` **antes de agendar** (asunto *"Name Correction Request"*; suele tardar 24–48 horas hábiles).

**Adaptaciones.** Disponibles para candidatos con discapacidad o necesidades documentadas. Se piden y aprueban **a través de Pearson VUE antes de agendar** — no agendes hasta tener la aprobación: [pearsonvue.com/us/en/test-takers/accommodations](https://www.pearsonvue.com/us/en/test-takers/accommodations).

**Repeticiones.** Si suspendes, hay periodo de espera creciente:

| Intento fallido | Espera antes del siguiente |
|---|---|
| 1.º | **14 días** |
| 2.º | **30 días** |
| 3.º | **90 días** |

Máximo **4 intentos por examen** en una ventana móvil de 12 meses. El límite es **por examen**: suspender uno no te impide registrarte en otro. **La tasa se paga en cada intento.**

**No-show y llegada tarde.** Si no apareces o llegas fuera de la ventana permitida, **pierdes la tasa** y hay que registrarse de nuevo.

## El día del examen

Entorno estandarizado, seguro y proctorizado. Da igual online o en centro:

- Permanecer **a la vista del proctor y la webcam** toda la sesión, si examinas online.
- Mesa despejada: **sin notas, libros, teléfonos, monitores secundarios** ni otros materiales.
- **Sin comunicarse con nadie** durante el examen.
- **No capturar, copiar, fotografiar ni reproducir** ningún contenido del examen.

Prohibidos: móviles, smartwatches, auriculares, material de estudio y cualquier grabadora. Lo permitido —por ejemplo, papel de borrador que dé el proctor— lo especifica Pearson VUE.

**Consecuencias.** Copiar, intentar acceder a recursos prohibidos o divulgar contenido puede invalidar tu resultado, revocar la credencial y vetarte de futuros exámenes.

**NDA.** Antes de empezar aceptas un acuerdo de confidencialidad: todo el contenido —preguntas, opciones y escenarios— es propiedad confidencial de Anthropic. Si no lo aceptas, la sesión termina y **no hay reembolso**.

## Renovación

La credencial vale **12 meses**. Es temporal a propósito: la tecnología cambia rápido y quieren que quien la tenga esté al día.

- **A tiempo:** repasas qué ha cambiado desde que te certificaste y completas una **evaluación gratuita y no proctorizada** en la Anthropic Partner Academy. **Sin coste.**
- **Si caduca:** hay que **repetir el examen completo pagando la tasa entera**.
- Si el contenido cambia mucho, Anthropic puede **exigir el examen completo** en lugar de la evaluación de renovación.

## Soporte, apelaciones y privacidad

- **Corrección de nombre:** `certifications-support@anthropic.com`.
- **Todo lo demás** (registro, agenda, adaptaciones, resultados): soporte de Pearson VUE en [pearsonvue.com/us/en/anthropic.html](https://www.pearsonvue.com/us/en/anthropic.html).
- **Apelaciones:** dentro de **14 días** desde la notificación de la decisión, o desde la fecha del examen si es sobre el resultado. **No son apelables** ni el resultado del standard-setting ni el contenido de los ítems individuales.

## Las otras tres certificaciones

| Credencial | Para quién | Precio |
|---|---|---|
| Claude Certified **Associate** – Foundations (`CCAO-F`) | Consultores, ventas y delivery leads que guían al cliente hacia el caso de uso correcto | 99 USD |
| Claude Certified **Developer** – Foundations (`CCDV-F`) | Ingenieros que construyen con la Claude API, Claude Code y MCP | 125 USD |
| Claude Certified **Architect** – Foundations (`CCAR-F`) | **Este.** Diseño de soluciones Claude de punta a punta | 125 USD |
| Claude Certified **Architect** – Professional (`CCAR-P`) | Nivel avanzado sobre lo mismo | 175 USD |

Todos son de 120 minutos, proctorizados por Pearson VUE, con corte en 720/1.000 y validez de 12 meses. La de Associate **no cuenta** para la elegibilidad de tier en el Claude Partner Network.

---

**Siguiente:** [2 · Dominio 1 — Arquitectura agéntica y orquestación](02-dominio-1-arquitectura-agentica.md)
