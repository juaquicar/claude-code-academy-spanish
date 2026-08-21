# 4 · Dominio 3 — Claude Code Configuration & Workflows

**Peso: 20 %** · ~12 de los 60 ítems. Seis task statements.

Escenarios que lo tocan: *Code Generation with Claude Code*, *Claude Code for Continuous Integration*, *Developer Productivity with Claude*.

---

## 3.1 · `CLAUDE.md`: jerarquía, alcance y organización modular

### La jerarquía

| Nivel | Ruta | Alcance |
|---|---|---|
| Usuario | `~/.claude/CLAUDE.md` | **Solo tú.** No se comparte por control de versiones |
| Proyecto | `.claude/CLAUDE.md` o `CLAUDE.md` en la raíz | Todo el equipo, vía repositorio |
| Directorio | `CLAUDE.md` dentro de un subdirectorio | Ese subárbol |

### Conocimiento

- Los ajustes de nivel usuario **aplican solo a ese usuario**: lo que pongas en `~/.claude/CLAUDE.md` **no llega a tus compañeros**.
- La sintaxis **`@import`** para referenciar ficheros externos y mantener `CLAUDE.md` modular (por ejemplo, importar en cada paquete solo los ficheros de estándares que le tocan).
- El directorio **`.claude/rules/`** para organizar reglas por tema, como alternativa a un `CLAUDE.md` monolítico.

### Habilidades

- **Diagnosticar problemas de jerarquía**: un miembro nuevo del equipo no recibe las instrucciones porque están en configuración **de usuario** y no **de proyecto**.
- Usar `@import` para incluir selectivamente los ficheros de estándares relevantes en el `CLAUDE.md` de cada paquete.
- Partir un `CLAUDE.md` grande en ficheros temáticos dentro de `.claude/rules/` (`testing.md`, `api-conventions.md`, `deployment.md`).
- Usar el comando **`/memory`** para verificar **qué ficheros de memoria están cargados** y diagnosticar comportamiento inconsistente entre sesiones.

---

## 3.2 · Slash commands y skills a medida

| Artefacto | Proyecto (compartido) | Usuario (personal) |
|---|---|---|
| Slash commands | `.claude/commands/` | `~/.claude/commands/` |
| Skills | `.claude/skills/` | `~/.claude/skills/` |

### Conocimiento

- Los comandos de proyecto van a control de versiones y **están disponibles para todo el que clone o haga pull**.
- Las skills viven en `.claude/skills/` con ficheros **`SKILL.md`** cuyo frontmatter admite **`context: fork`**, **`allowed-tools`** y **`argument-hint`**.
- **`context: fork`** ejecuta la skill en un contexto de subagente aislado, **evitando que su salida contamine la conversación principal**.
- Personalización personal: crear variantes en `~/.claude/skills/` **con otro nombre** para no afectar a los compañeros.

### Habilidades

- Crear comandos de proyecto en `.claude/commands/` para disponibilidad de equipo vía control de versiones.
- Usar `context: fork` para aislar skills de salida verbosa (análisis de codebase) o de contexto exploratorio (brainstorming de alternativas).
- Configurar `allowed-tools` en el frontmatter para restringir el acceso a herramientas durante la ejecución de la skill (limitar a escritura de ficheros para evitar acciones destructivas).
- Usar `argument-hint` para pedir los parámetros necesarios cuando el desarrollador invoca la skill sin argumentos.
- Elegir entre **skills** (invocación bajo demanda para flujos concretos) y **`CLAUDE.md`** (estándares universales siempre cargados).

> **Trampa.** "Disponible para todo el equipo al clonar el repo" ⇒ `.claude/commands/`. No `CLAUDE.md` (que es contexto e instrucciones, no definiciones de comando) y **no** `.claude/config.json` con un array `commands`: ese mecanismo **no existe** en Claude Code.

---

## 3.3 · Reglas por ruta para carga condicional de convenciones

### Conocimiento

- Ficheros en `.claude/rules/` con **frontmatter YAML** y un campo **`paths`** con **patrones glob** para activación condicional.
- Las reglas con alcance de ruta **se cargan solo al editar ficheros que casan**, reduciendo contexto irrelevante y **uso de tokens**.
- La ventaja de las reglas con glob sobre los `CLAUDE.md` por directorio: convenciones que **abarcan varios directorios** (ficheros de test repartidos por todo el codebase).

### Habilidades

- Crear ficheros en `.claude/rules/` con `paths: ["terraform/**/*"]` para que carguen solo al editar lo que corresponde.
- Aplicar convenciones **por tipo de fichero independientemente del directorio** (`**/*.test.tsx` para todos los tests).
- Elegir reglas por ruta sobre `CLAUDE.md` de subdirectorio cuando las convenciones aplican a ficheros dispersos por el codebase.

---

## 3.4 · Plan mode frente a ejecución directa

| Usa **plan mode** cuando | Usa **ejecución directa** cuando |
|---|---|
| Cambios a gran escala | Cambio simple y bien acotado |
| Varios enfoques válidos | Un solo enfoque obvio |
| Decisiones arquitectónicas | Sin implicación de arquitectura |
| Modificaciones multi-fichero | Un fichero, alcance claro |

### Conocimiento y habilidades

- Plan mode permite **explorar el codebase y diseñar antes de comprometerse a cambios**, evitando retrabajo caro.
- El **subagente `Explore`** aísla la salida verbosa de descubrimiento y devuelve resúmenes, **preservando el contexto de la conversación principal**.
- Ejemplos de plan mode: reestructurar un monolito en microservicios, migraciones de librería que tocan 45+ ficheros, elegir entre enfoques de integración con requisitos de infraestructura distintos.
- Ejemplos de ejecución directa: un bug de un solo fichero con stack trace claro, añadir un condicional de validación de fecha.
- **Combinar los dos**: plan mode para investigar, ejecución directa para implementar lo planificado.

> **Trampa.** "Empiezo en directo y cambio a plan mode si aparece complejidad" es incorrecto cuando **la complejidad ya está enunciada en el requisito**. No es algo que *pueda* surgir: ya está ahí.

---

## 3.5 · Refinamiento iterativo

### Conocimiento

- **Ejemplos concretos de entrada/salida** son la forma más eficaz de comunicar la transformación esperada cuando la prosa se interpreta de forma inconsistente.
- **Iteración dirigida por tests**: escribir la suite primero, luego iterar compartiendo los fallos.
- El **patrón entrevista**: hacer que Claude formule preguntas para sacar a la luz consideraciones que el desarrollador no anticipó, antes de implementar.
- Cuándo dar **todos los problemas en un solo mensaje** (problemas que interactúan) frente a arreglarlos **secuencialmente** (problemas independientes).

### Habilidades

- Dar **2-3 ejemplos** concretos de entrada/salida cuando la descripción en lenguaje natural produce resultados inconsistentes.
- Escribir suites que cubren comportamiento esperado, casos límite y requisitos de rendimiento **antes** de implementar, e iterar compartiendo los fallos.
- Usar el patrón entrevista para sacar consideraciones de diseño (estrategias de invalidación de caché, modos de fallo) en dominios desconocidos.
- Dar casos de test concretos con entrada de ejemplo y salida esperada para arreglar casos límite (valores nulos en scripts de migración).

---

## 3.6 · Integrar Claude Code en pipelines CI/CD

### Flags que hay que saberse

| Flag | Qué hace |
|---|---|
| **`-p`** / **`--print`** | Modo no interactivo: procesa el prompt, escribe a stdout y sale. **Sin esto el job se cuelga esperando entrada** |
| **`--output-format json`** | Salida parseable por máquina |
| **`--json-schema`** | Fuerza la estructura de esa salida |

### Conocimiento

- **`CLAUDE.md` es el mecanismo** para dar contexto de proyecto (estándares de testing, convenciones de fixtures, criterios de revisión) a un Claude Code invocado desde CI.
- **Aislamiento de contexto de sesión:** la misma sesión que generó el código es **menos eficaz revisando sus propios cambios** que una instancia de revisión independiente.

### Habilidades

- Ejecutar con `-p` para evitar que el pipeline se cuelgue.
- Combinar `--output-format json` con `--json-schema` para producir hallazgos estructurados que se publican como comentarios inline en el PR.
- Incluir **los hallazgos de revisiones previas** en el contexto al re-ejecutar tras nuevos commits, instruyendo a Claude a **reportar solo lo nuevo o lo aún sin resolver**, para no duplicar comentarios.
- Aportar los **ficheros de test existentes** en contexto para que la generación de tests no proponga escenarios ya cubiertos.
- Documentar en `CLAUDE.md` los estándares de testing, qué hace valioso a un test y qué fixtures existen, para mejorar la calidad y **reducir tests de bajo valor**.

> **Trampa.** `CLAUDE_HEADLESS=true` y el flag `--batch` **no existen**. Redirigir stdin desde `/dev/null` es un apaño de Unix que no aborda la sintaxis de Claude Code. La respuesta es **`-p`**.

---

## Conclusiones del dominio

- Jerarquía: usuario **no** se comparte; proyecto sí. Si el compañero no lo ve, está en el nivel equivocado. Verifica con **`/memory`**.
- Comandos y skills de equipo → `.claude/`. Personales → `~/.claude/`.
- **`context: fork`** aísla salida verbosa. **`allowed-tools`** limita el daño. **`argument-hint`** pide parámetros.
- Convenciones por tipo de fichero disperso → **`.claude/rules/` con globs**, no `CLAUDE.md` por directorio.
- Complejidad enunciada de antemano → **plan mode desde el principio**.
- CI → **`-p`**, y revisar con **una instancia distinta** de la que generó.

---

**Anterior:** [3 · Dominio 2](03-dominio-2-herramientas-y-mcp.md) · **Siguiente:** [5 · Dominio 4 — Prompting y salida estructurada](05-dominio-4-prompting-y-salida-estructurada.md)
