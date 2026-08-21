# 08 — El fichero CLAUDE.md

*15 minutos* · [Vídeo](https://www.youtube.com/embed/O0FGCxkHM-U)

**Al terminar sabrás:** qué problema resuelve CLAUDE.md · cuándo lo lee Claude Code · la jerarquía proyecto vs. usuario · cómo referenciar documentación con `@` · por qué conviene empezar **sin** él.

---

Una de las funcionalidades más útiles de Claude Code es el fichero **CLAUDE.md**. Le da a Claude Code **memoria persistente** sobre tu proyecto.

## El problema que resuelve

Cuando abres Claude Code sin un CLAUDE.md, **empieza de cero cada vez**. Tiene que reexplorar tu base de código, averiguar qué dependencias hacen falta y entender qué funcionalidades ya están implementadas. A veces hace suposiciones, y eso dificulta llevarlo en la dirección correcta.

CLAUDE.md resuelve esto. Es un fichero Markdown que añades **a la raíz de tu proyecto**, y **Claude Code lo lee automáticamente cada vez que arrancas una sesión**. Piénsalo como un **script de onboarding** para tu base de código. El contenido del fichero CLAUDE.md **se añade a tu prompt**.

> **Trampa de examen.** No se lee "solo después de ejecutar `/init`", ni "una vez al crear el proyecto", ni "solo cuando se lo pides explícitamente". **Se lee automáticamente al inicio de cada sesión.** Es la pregunta 4 del quiz oficial.

## Un ejemplo

Así es como se ve un CLAUDE.md típico:

```
# Project

This is a Next.js 15 app using the App Router, Tailwind, and Drizzle ORM.

# Commands
- Dev server: `pnpm dev`
- Run tests: `pnpm test`
- Lint: `pnpm lint`

# Code Style
- Use 2-space indentation
- Prefer named exports
- All API routes go in app/api/
- Use server actions instead of API routes where possible
```

Es directo. Ahora, si le pides a Claude Code que cree un componente de React, **ya sabe** que debe usar Tailwind para los estilos y seguir tus convenciones.

## CLAUDE.md es para equipos

Puedes (y deberías) **versionar tu CLAUDE.md** para que tu equipo se beneficie de él. Hay una **jerarquía de ficheros de memoria** según a quién van dirigidos:

| Nivel | Dónde vive | Para quién |
|---|---|---|
| **CLAUDE.md de proyecto** | Directorio raíz del proyecto | **Compartido con el equipo** |
| **CLAUDE.md de usuario** | Tu carpeta de configuración | **Solo para ti**, y aplica a **todos tus proyectos** — tus preferencias personales |

## Trucos

**Guarda las correcciones en memoria.** Si te ves corrigiendo a Claude repetidamente — por ejemplo, diciéndole que use siempre server actions en vez de API routes — **pídele explícitamente que guarde esa regla en memoria**. La próxima vez que abras el proyecto, ya lo sabrá.

**Referencia la documentación del proyecto.** Si tienes documentación en el proyecto que quieres que Claude consulte, usa el **símbolo `@`** con la ruta del fichero:

```
## README.md

Please read if you need more info: @README.md
```

**Empieza sin CLAUDE.md.** La recomendación es **arrancar un proyecto sin fichero CLAUDE.md** para ver dónde tienes que corregir el rumbo constantemente. Así tu CLAUDE.md queda **compacto y centrado solo en la información necesaria**. Cuando estés listo, ejecuta **`/init`** para que Claude te genere uno.

> **Contraintuitivo:** la tentación es escribir un CLAUDE.md enorme el día uno. El curso recomienda lo contrario — que el fichero lo escriba la experiencia.

## Conclusiones

La diferencia entre una sesión frustrante de Claude Code y una productiva suele reducirse al **contexto** — y el fichero CLAUDE.md es cómo se lo proporcionas. Empieza con tu stack, tus preferencias y tus comandos, y ve construyendo desde ahí.
