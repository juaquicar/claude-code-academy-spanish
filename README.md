# Claude Code Academy — resúmenes en español

Resúmenes completos, en español, de los cursos de la [Anthropic Academy](https://www.anthropic.com/learn) sobre Claude Code.

Cada curso trae **un `.md` por lección** para leer en el editor, y **un `curso-interactivo.html`** autocontenido —sin dependencias ni conexión— con diagramas interactivos, flashcards, quiz con corrección al momento, seguimiento de progreso, buscador y tema claro/oscuro. Se abre con doble clic.

## Cursos

| Curso | Lecciones | Contenido |
|---|---|---|
| **[Claude Code in Action](claude-code-in-action/)** | 9 | Dirigir sesiones largas · CLAUDE.md · Skills de verificación · Modos de permisos · Hooks · Routines y headless · GitHub Actions y Code Review · Verificar runs no supervisados · Plugins |
| **[Introduction to Subagents](introduction-to-subagents/)** | 4 | Qué son · Crearlos · Diseñarlos bien · Usarlos con criterio |

### Claude Code in Action

[Curso original](https://anthropic.skilljar.com/claude-code-in-action) · **quiz oficial superado 8/8**

Llevar Claude Code más allá de la tarea rápida y poder *confiar* en el resultado. El eje: cuanta más autonomía le des, más deliberadas tienen que ser dos cosas — **qué le permites hacer antes** (permisos, hooks, instrucciones) y **cómo compruebas lo que hizo después** (diff, tests como puerta, segunda opinión).

Incluye las **8 preguntas reales del quiz oficial** con su feedback, más 15 de repaso.

### Introduction to Subagents

[Curso original](https://anthropic.skilljar.com/introduction-to-subagents)

Usar y crear subagentes para gestionar el contexto y delegar tareas. El eje: un subagente es **una ventana de contexto aparte** que devuelve solo un resumen y descarta el resto. La regla de decisión — **¿importa el trabajo intermedio?** No → delega. Sí → hilo principal.

Este curso no tiene quiz oficial; el repo incluye una autoevaluación de 12 preguntas construida a partir del material.

## Estructura

```
CLAUDE.md                     cómo se elabora un curso, de principio a fin
scripts/
├── extraer_curso.py          descarga un curso de Skilljar → markdown crudo
└── validar_html.py           valida un curso-interactivo.html antes de publicarlo
<nombre-del-curso>/
├── README.md                 índice y hilo conductor del curso
├── 01-....md ... NN-....md   una lección por fichero
└── curso-interactivo.html    el curso entero en una página
```

## Añadir un curso nuevo

```bash
python3 scripts/extraer_curso.py <slug-del-curso>     # → /tmp/<slug>/raw_*.md
# leer los raw_*.md, escribir los resúmenes y el HTML
python3 scripts/validar_html.py <slug>/curso-interactivo.html
```

El procedimiento completo y las convenciones de redacción están en [CLAUDE.md](CLAUDE.md).

## Aviso

Resúmenes de estudio derivados del material del curso, redactados en español para uso personal. Los cursos originales, sus vídeos y su contenido son de Anthropic. Si te interesa el tema, haz el curso: es gratuito.
