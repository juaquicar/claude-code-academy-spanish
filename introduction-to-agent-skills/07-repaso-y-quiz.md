# 07 — Repaso y autoevaluación

> Este curso **no tiene quiz oficial** en Skilljar: son 6 lecciones y se acaba. Lo que sigue es una autoevaluación construida a partir del material.

---

## Chuleta

### Qué es una skill

- **Una carpeta de instrucciones y recursos** con un fichero **`SKILL.md`** dentro.
- **`name`** y **`description`** en el frontmatter; las instrucciones debajo.
- Al arrancar, Claude **solo carga nombre y descripción**, no el contenido.
- **La descripción es el criterio de emparejamiento**, por **coincidencia semántica**.
- Antes de cargar el contenido completo, **Claude te pide confirmación**.
- **La regla de oro:** si te encuentras explicándole lo mismo a Claude una y otra vez, **eso es una skill esperando a ser escrita**.

### Dónde viven

| Tipo | Ruta | Alcance |
|---|---|---|
| **Personal** | `~/.claude/skills` (Windows: `C:/Users/<usuario>/.claude/skills`) | Todos tus proyectos |
| **Proyecto** | `.claude/skills` en la raíz del repo | Todo el que clone; se versiona |

### El frontmatter

| Campo | Obligatorio | Límite |
|---|---|---|
| **`name`** | ✅ | Minúsculas, números y guiones. **Máx. 64 caracteres.** Debe coincidir con el directorio |
| **`description`** | ✅ | **Máx. 1.024 caracteres.** El campo más importante |
| `allowed-tools` | — | Si lo omites, **no restringe nada** |
| `model` | — | Qué modelo usar |

### Prioridad ante nombres iguales

**Enterprise → Personal → Project → Plugins.** Enterprise gana siempre. Para evitar choques: **nombres descriptivos** (`frontend-review`, no `review`).

### Ciclo de vida

- **Crear:** directorio + `SKILL.md` dentro. **Reinicia Claude Code.**
- **Actualizar:** edita el `SKILL.md`. **Reinicia.**
- **Eliminar:** borra el directorio. **Reinicia.**

### Divulgación progresiva

- **Mantén `SKILL.md` por debajo de 500 líneas.**
- Estructura sugerida: **`scripts/`** (ejecutable), **`references/`** (documentación), **`assets/`** (imágenes, plantillas).
- Enlaza los ficheros de apoyo **con instrucciones de cuándo cargarlos** — es como tener un índice en contexto en vez del documento entero.
- **Los scripts se ejecutan sin cargar su contenido**: solo la salida consume tokens. La instrucción clave es decirle a Claude que **ejecute** el script, no que lo **lea**.

### Las cinco funcionalidades

| Pieza | Se activa por | Contexto |
|---|---|---|
| **CLAUDE.md** | Siempre | El actual |
| **Skills** | **Tu petición** (request-driven) | El actual |
| **Subagentes** | Delegación | **Separado y aislado** |
| **Hooks** | **Eventos** (event-driven) | Fuera de la conversación |
| **MCP** | Herramientas externas | Otra categoría |

### Compartir

- **Repositorio** → `.claude/skills`, se comparte por Git. Para estándares de equipo y skills que referencian tu codebase.
- **Plugins** → directorio `skills` en el plugin, distribuido por marketplace. Para skills **no demasiado específicas del proyecto**.
- **Enterprise managed settings** → máxima prioridad. Para lo que **debe** ser consistente: seguridad, cumplimiento. Soporta **`strictKnownMarketplaces`**.

### ⚠ Skills y subagentes

- **Los subagentes NO ven tus skills automáticamente:** arrancan con contexto limpio.
- **Los agentes integrados (Explorer, Plan, Verify) no pueden acceder a skills en absoluto.**
- **Los subagentes propios sí, pero solo si los listas** en el campo **`skills`** del frontmatter, en `.claude/agents`. Comando `/agents` para crearlo interactivamente.
- En un subagente, las skills **se cargan al arrancar**, no bajo demanda.

### Diagnóstico

| Síntoma | Causa / arreglo |
|---|---|
| **No se dispara** | **Casi siempre la descripción.** Añade frases de disparo reales; prueba variaciones |
| **No se carga** | `SKILL.md` **dentro de un directorio con nombre**, y el nombre **exactamente `SKILL.md`**. `claude --debug` para ver errores |
| **Se usa la equivocada** | Descripciones demasiado parecidas: hazlas distintas |
| **La tapan** | Conflicto de prioridad: renombra o habla con tu admin |
| **Plugin sin skills** | Limpia caché, reinicia, reinstala. Si sigue: pasa el validador |
| **Falla en ejecución** | Dependencias instaladas · `chmod +x` en scripts · **barras normales `/` incluso en Windows** |

**Empieza siempre por el validador** (se instala fácil con `uv`).

---

## Autotest — 12 preguntas

Tapa las respuestas.

1. ¿Qué carga Claude de tus skills al arrancar, y por qué importa?
2. ¿Qué campo decide si una skill se activa, y con qué mecanismo?
3. Un compañero clona el repo. ¿Qué skills obtiene y cuáles no?
4. Has editado un `SKILL.md` y Claude sigue con el comportamiento viejo. ¿Qué falta?
5. Tu skill personal `code-review` no se aplica nunca. ¿Qué sospechas primero?
6. ¿Cuáles son los dos campos obligatorios del frontmatter y qué límites tienen?
7. Omites `allowed-tools`. ¿Qué puede hacer Claude?
8. Tu `SKILL.md` va por 1.800 líneas. ¿Qué haces?
9. Tu skill incluye un script de validación. ¿Qué debes decirle a Claude, y por qué?
10. ¿Cuándo eliges skill y cuándo CLAUDE.md?
11. Delegas a un subagente propio y no aplica ninguna de tus skills. ¿Por qué?
12. Tu skill no se dispara aunque existe y valida. ¿Dónde miras?

<details>
<summary>Respuestas</summary>

1. **Solo el nombre y la descripción**, no el contenido. Importa porque así **no llenan la ventana de contexto**: el contenido completo entra solo cuando la skill se activa.
2. La **`description`**, mediante **coincidencia semántica**. Claude compara tu petición con las descripciones disponibles; basta con que la **intención se solape**, no las palabras exactas.
3. Obtiene las **de proyecto** (`.claude/skills`, versionadas). **No** obtiene tus **personales** (`~/.claude/skills`), que solo te siguen a ti.
4. **Reiniciar Claude Code.** Las skills se cargan al arrancar; cualquier cambio —crear, editar o borrar— exige reinicio.
5. Un **conflicto de prioridad**: probablemente hay una skill **enterprise** con el mismo nombre, y enterprise gana siempre. Orden: **Enterprise → Personal → Project → Plugins**. Lo más fácil es renombrar la tuya.
6. **`name`** (minúsculas, números y guiones, **máx. 64 caracteres**, coincidiendo con el directorio) y **`description`** (**máx. 1.024 caracteres**).
7. **No restringe nada**: Claude usa su modelo de permisos normal.
8. Aplicar **divulgación progresiva**: dejar lo esencial en `SKILL.md` —**bajo 500 líneas**— y mover el material detallado a `references/`, `scripts/` y `assets/`, enlazándolo con instrucciones de **cuándo** cargarlo.
9. Decirle que **ejecute** el script, **no que lo lea**. Así el contenido no entra en contexto y **solo la salida consume tokens**.
10. **CLAUDE.md** para estándares que **siempre** aplican y restricciones permanentes. **Skill** para experiencia **específica de una tarea**, conocimiento que solo a veces es relevante, y procedimientos detallados que ensuciarían todas las conversaciones.
11. Porque **los subagentes no ven tus skills automáticamente**: arrancan con contexto limpio. Hay que **listarlas explícitamente en el campo `skills`** del frontmatter del agente. (Y los **integrados —Explorer, Plan, Verify— no pueden acceder a skills en absoluto**.)
12. **En la descripción**, que es la causa casi siempre. Contrástala con cómo formulas realmente las peticiones y **añade frases de disparo**; prueba variaciones y añade las palabras clave que fallen. Si tampoco aparece en la lista de skills disponibles, es un problema de carga: `SKILL.md` dentro de un directorio con nombre y con ese nombre exacto.

</details>
