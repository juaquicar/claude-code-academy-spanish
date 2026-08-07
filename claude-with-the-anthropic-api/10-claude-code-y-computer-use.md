# 10 — Claude Code y computer use

**Anthropic Apps** = dos aplicaciones desplegadas por Anthropic: **Claude Code** y **Computer Use**.

- **Claude Code** — asistente de programación en terminal, que sirve de **ejemplo de arquitectura de agente**.
- **Computer Use** — conjunto de herramientas que amplía las capacidades de Claude más allá de generar texto.

> Ambas ejemplifican cómo funcionan los agentes, y sirven de modelo de aprendizaje para construir agentes eficaces. Por eso están justo antes del capítulo de arquitectura.

---

## Claude Code · montaje

Asistente de programación en terminal.

**Capacidades base:** buscar, leer y editar ficheros + herramientas avanzadas (fetch web, acceso al terminal) + **soporte de cliente MCP** para ampliar funcionalidad vía servidores MCP.

**Instalación:**

1. Instala **Node.js** — compruébalo con `npm help`.
2. `npm install` para instalar Claude Code.
3. Ejecuta `claude` en el terminal para iniciar sesión en tu cuenta de Anthropic.

Guía completa en `docs.anthropic.com`.

## Claude Code en acción

> **No es un generador de código: es un ingeniero colaborador en el proyecto.**

**Capacidades:** montaje del proyecto, diseño de funcionalidades, escritura de código, pruebas, despliegue y corrección de errores en producción.

**Flujo de arranque:**

1. Descarga el proyecto y ábrelo en el editor.
2. Ejecuta `claude`.
3. Pídele que lea el README y ejecute las instrucciones de montaje.
4. Ejecuta **`init`** → Claude escanea el codebase buscando arquitectura y estilo de código, y crea el fichero **`claude.md`**.
5. `claude.md` se **incluye automáticamente como contexto** en las peticiones futuras.

**Tipos de memoria:** de proyecto (compartida), local y de usuario.

**Gestión del contexto:**

- Usa el símbolo **`#`** para añadir notas concretas a la memoria.
- Puedes editar `claude.md` a mano o volver a ejecutar `init` para actualizarlo.
- Claude puede encargarse de operaciones de Git: stage, commit.

### Dos estrategias de prompting

**Método 1 · Flujo de tres pasos**

1. Identifica los ficheros relevantes y pide a Claude que los analice.
2. Describe la funcionalidad y pídele que **planifique la solución, sin escribir código todavía**.
3. Pídele que implemente el plan.

**Método 2 · Desarrollo guiado por tests**

1. Aporta el contexto relevante.
2. Pídele que **sugiera tests** para la funcionalidad.
3. Selecciona e implementa los elegidos.
4. Pídele que escriba código **hasta que los tests pasen**.

> **El principio:** Claude Code es un **multiplicador de esfuerzo**. Instrucciones más detalladas = resultados significativamente mejores. Trátalo como un ingeniero colaborador, no como un generador de código.

## Ampliar con servidores MCP

Claude Code lleva un **cliente MCP embebido** que puede conectarse a servidores MCP.

```bash
claude mcp add [nombre-servidor] [comando-de-arranque]
```

**Ejemplo:** un servidor de procesamiento de documentos que expone la herramienta *"Document Path to Markdown"*, permitiendo a Claude Code leer PDF y Word ejecutando `uv run main.py`.

**Ampliación dinámica:** los servidores MCP **añaden funciones a Claude Code en tiempo real**, sin modificar el núcleo.

**Casos de uso habituales:** monitorización de producción (Sentry), gestión de proyectos (Jira), comunicación (Slack), herramientas propias del flujo de desarrollo.

**Montaje:** 1) crea un servidor MCP con tus herramientas, 2) añádelo a Claude Code con nombre y comando de arranque, 3) reinicia Claude Code para acceder a las nuevas capacidades.

## Paralelizar Claude Code

Ejecutar **varias instancias de Claude a la vez** para tareas distintas.

**El problema:** varias instancias modificando los mismos ficheros a la vez generan conflictos y código inválido.

**La solución: git work trees** — espacios de trabajo aislados por instancia.

**Git work trees** = copias completas del proyecto en directorios separados, cada una asociada a una rama distinta.

**Flujo:** crear el work tree → asignar la tarea a una instancia → trabajar en aislamiento → hacer commit → fusionar de vuelta a la rama principal.

**Comandos personalizados:** automatiza la creación y gestión de work trees con ficheros markdown en el directorio **`.claude/commands`**.

**Estructura:** `.claude/commands/nombre.md`, con el marcador **`$ARGUMENTS`** para los valores dinámicos.

> **El beneficio:** un solo desarrollador comandando un **equipo virtual de ingenieros de software**. El escalado solo está limitado por tu capacidad de gestionar tareas simultáneas.

**Conflictos de merge:** Claude los resuelve automáticamente al fusionar ramas. **Limpieza:** Claude se encarga de eliminar el work tree cuando la funcionalidad está terminada.

## Depuración automatizada

Usar Claude para **detectar, analizar y corregir errores de producción sin intervención manual**.

**El flujo:**

1. Una **GitHub Action** corre a diario para revisar el entorno de producción.
2. Recupera los **logs de CloudWatch** de las últimas 24 horas.
3. Claude identifica los errores y los **deduplica**.
4. Claude analiza cada uno y **genera correcciones**.
5. Crea un **pull request** con las soluciones propuestas.

**Componentes:** GitHub Actions para programar, AWS CLI para recuperar logs, Claude Code para analizar y corregir, CloudWatch para monitorizar.

**Beneficios:** **captura errores que solo pasan en producción**, reduce el tiempo de buscar en logs, aporta correcciones con contexto y explicación, y genera pull requests revisables.

> **Caso de uso típico:** errores de configuración entre entornos —IDs de modelo inválidos, claves de API— que funcionan en local y fallan en producción.

---

## Computer use

Capacidad de Claude para **interactuar con interfaces de ordenador mediante observación visual y acciones de control**.

**Qué puede hacer:**

- Tomar capturas de pantalla de aplicaciones y navegadores.
- Hacer clic en botones, escribir texto, navegar interfaces.
- Seguir instrucciones multipaso de forma autónoma.
- Ejecutar pruebas de QA y tareas de automatización.

**Cómo funciona:** corre en un **contenedor Docker aislado**. El usuario da instrucciones por chat, Claude **observa la pantalla visualmente** y ejecuta acciones, y genera un informe de resultados.

**Casos de uso:** QA automatizado de aplicaciones web, pruebas de interacción con la interfaz en distintos escenarios, ahorro de tiempo en tareas repetitivas, identificación de bugs mediante pruebas sistemáticas.

**Ejemplo de flujo:** el usuario describe los requisitos de prueba → Claude navega a la aplicación → ejecuta los casos → informa de pass/fail con hallazgos detallados.

## Cómo funciona computer use por dentro

> **Es exactamente el mismo flujo de tool use del capítulo 4.**

**Recordatorio del flujo:** usuario envía mensaje + esquema → Claude responde con una petición de tool use (ID, nombre, entrada) → tu servidor ejecuta código → el resultado vuelve a Claude como tool result.

**Computer use sigue ese flujo idéntico:**

- Se envía un **esquema especial** a Claude; un esquema pequeño **se expande a una estructura mayor** por detrás.
- El esquema expandido incluye una función de acción con argumentos: mover ratón, clic izquierdo, captura de pantalla…
- Claude envía la petición de tool use.
- **El desarrollador debe cumplirla** mediante un entorno de computación, normalmente un contenedor Docker.
- El contenedor ejecuta las pulsaciones y movimientos de ratón programáticamente.
- La respuesta vuelve a Claude.

> ⚠ **Claude no manipula directamente ningún ordenador.** Computer use = el sistema de herramientas + un entorno de computación que aportas tú.

Anthropic ofrece una **implementación de referencia**: un contenedor Docker con el código de ejecución de ratón y teclado ya hecho. Solo hace falta Docker y ejecutar un comando.

> **Computer use es una capa de abstracción**: el sistema de herramientas gestiona la comunicación con Claude, y el contenedor Docker gestiona la interacción real con el ordenador.
