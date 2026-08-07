# 03 — Configuración y skills multi-fichero

*20 minutos* · [Vídeo](https://www.youtube.com/embed/98KaK_rn5rQ)

**Al terminar sabrás:** configurar los metadatos avanzados incluyendo `allowed-tools` y `model` · escribir descripciones que disparen de forma fiable · restringir lo que Claude puede hacer con una skill activa · organizar skills complejas con divulgación progresiva y múltiples ficheros.

---

## Los campos del frontmatter

El **estándar abierto de agent skills** soporta varios campos. **Dos son obligatorios**, el resto opcionales:

| Campo | Obligatorio | Detalle |
|---|---|---|
| **`name`** | ✅ | Identifica la skill. **Solo minúsculas, números y guiones. Máximo 64 caracteres.** Debe coincidir con el nombre del directorio |
| **`description`** | ✅ | Le dice a Claude cuándo usarla. **Máximo 1.024 caracteres.** **El campo más importante**, porque es el que usa para emparejar |
| **`allowed-tools`** | — | Restringe qué herramientas puede usar Claude con la skill activa |
| **`model`** | — | Especifica qué modelo de Claude usar para la skill |

## Escribir descripciones eficaces

> **Sé explícito.** Si alguien te dijera *"tu trabajo es ayudar con la documentación"*, no sabrías qué hacer — **Claude piensa igual**.

Una buena descripción responde **dos preguntas**:

1. **¿Qué hace la skill?**
2. **¿Cuándo debe usarla Claude?**

> Si tu skill no se dispara cuando lo esperas, **añade más palabras clave que coincidan con cómo formulas realmente tus peticiones**. La descripción es lo que Claude usa para decidir si una skill es relevante: **el lenguaje importa**.

## Restringir herramientas con `allowed-tools`

A veces quieres una skill que **solo pueda leer ficheros, no modificarlos**. Útil para flujos sensibles a la seguridad, tareas de solo lectura, o cualquier situación en la que quieras guardarraíles.

```yaml
---
name: codebase-onboarding
description: Helps new developers understand the system works.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---
```

Con esa skill activa, Claude **solo puede usar esas herramientas sin pedir permiso** — nada de editar, nada de escribir.

> Si **omites `allowed-tools`** por completo, la skill **no restringe nada**: Claude usa su modelo de permisos normal.

## Divulgación progresiva

Las skills **comparten la ventana de contexto** con tu conversación. Al activarse una, su `SKILL.md` entra en contexto. Pero a veces necesitas referencias, ejemplos o scripts de los que la skill depende.

**Meterlo todo en un fichero de 2.000 líneas tiene dos problemas:** ocupa mucho contexto y es incómodo de mantener.

**La divulgación progresiva lo resuelve:** deja las instrucciones esenciales en `SKILL.md` y pon el material de referencia detallado en ficheros aparte que Claude lee **solo cuando hacen falta**.

El estándar abierto sugiere organizar el directorio así:

```
mi-skill/
├── SKILL.md
├── scripts/      # código ejecutable
├── references/   # documentación adicional
└── assets/       # imágenes, plantillas u otros datos
```

Luego, en `SKILL.md`, enlazas los ficheros de apoyo **con instrucciones claras sobre cuándo cargarlos**.

> Ejemplo: Claude lee `architecture-guide.md` **solo cuando alguien pregunta por el diseño del sistema**. Si preguntan dónde añadir un componente, ese fichero nunca se carga.
>
> **Es como tener un índice en la ventana de contexto en vez del documento entero.**

**Regla del pulgar: mantén `SKILL.md` por debajo de 500 líneas.** Si lo superas, plantéate si el contenido debería partirse en ficheros de referencia.

## Usar scripts con eficiencia

> Los scripts del directorio de la skill **se ejecutan sin cargar su contenido en contexto**. El script corre y **solo la salida consume tokens**.

**La instrucción clave que debes incluir en tu `SKILL.md`** es decirle a Claude que **ejecute** el script, no que lo **lea**.

Es especialmente útil para:

- **Validación del entorno**
- **Transformaciones de datos** que necesitan ser consistentes
- **Operaciones que son más fiables como código probado** que como código generado

## Reflexión

- Piensa en una skill que te gustaría construir con varios ficheros. ¿Cómo estructurarías el `SKILL.md` frente a los ficheros de referencia?
- ¿Hay flujos en tu equipo donde restringir el acceso a herramientas con `allowed-tools` añadiría una capa de seguridad importante?
