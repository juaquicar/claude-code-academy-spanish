# 06 — Solución de problemas

*15 minutos* · [Vídeo](https://www.youtube.com/embed/YBa1cwaG7is)

**Al terminar sabrás:** usar el validador de skills para detectar problemas estructurales antes de depurar · diagnosticar fallos de disparo y de carga · resolver conflictos de prioridad · depurar errores de ejecución (dependencias, permisos, rutas).

---

> Cuando las skills no funcionan, el problema **cae casi siempre en una de unas pocas categorías**: no se dispara, no se carga, tiene conflictos, o falla en ejecución. La buena noticia es que **la mayoría de arreglos son directos**.

## Empieza por el validador

Lo primero que hay que probar es el **comando verificador de agent skills**. Los pasos de instalación varían según el sistema operativo, pero **usar `uv` es la forma más rápida**.

Una vez instalado, navega al directorio de tu skill o ejecuta el comando desde cualquier sitio.

> **El validador detecta problemas estructurales antes de que pierdas tiempo depurando otras cosas.**

---

## Diagnóstico por síntoma

### ✗ La skill no se dispara

Existe y pasa la validación, pero Claude no la usa cuando lo esperas.

> **La causa es casi siempre la descripción.**

Claude usa **coincidencia semántica**: tu petición necesita solaparse con el significado de la descripción. Si no hay suficiente solape, no hay coincidencia.

**Qué hacer:**

- Contrasta tu descripción con **cómo formulas realmente las peticiones**.
- Añade **frases de disparo que los usuarios dirían de verdad**.
- **Prueba con variaciones:** *"help me profile this"*, *"why is this slow?"*, *"make this faster"*.
- **Si alguna variación no dispara, añade esas palabras clave a la descripción.**

### ✗ La skill no se carga

Si no aparece al preguntarle a Claude qué skills hay disponibles, comprueba los **requisitos estructurales**:

- El fichero **`SKILL.md` debe estar dentro de un directorio con nombre**, no en la raíz de skills.
- El nombre del fichero debe ser **exactamente `SKILL.md`** — **`SKILL` en mayúsculas, `md` en minúsculas**.

Ejecuta **`claude --debug`** para ver errores de carga. Busca mensajes que mencionen el nombre de tu skill: a veces eso solo ya te lleva directo al problema.

### ✗ Se usa la skill equivocada

Si Claude usa la que no es o parece confundido entre varias, **tus descripciones son demasiado parecidas**. Hazlas distintas.

> Ser lo más específico posible no solo ayuda a Claude a decidir cuándo usar tu skill: **también evita conflictos con otras de nombre parecido**.

### ✗ Conflictos de prioridad

Si tu skill personal se está ignorando, es posible que una **enterprise o de mayor prioridad tenga el mismo nombre**.

> Si hay una skill enterprise `code-review` y tú tienes una personal `code-review`, **gana la enterprise siempre**.

**Tus opciones:**

1. **Renombrar la tuya** a algo más distintivo — normalmente el camino más fácil.
2. Hablar con tu administrador sobre la skill enterprise.

### ✗ Las skills de un plugin no aparecen

**Limpia la caché, reinicia Claude Code y reinstala.**

Si aun así no aparecen, la estructura del plugin puede estar mal. **Aquí es donde el validador se gana el sueldo.**

### ✗ Errores de ejecución

La skill carga pero falla al ejecutarse. Causas habituales:

| Causa | Arreglo |
|---|---|
| **Dependencias que faltan** | Si tu skill usa paquetes externos, deben estar instalados. **Añade la información de dependencias a la descripción** para que Claude sepa qué hace falta |
| **Permisos** | Los scripts necesitan permiso de ejecución: **`chmod +x`** sobre los que la skill referencie |
| **Separadores de ruta** | **Usa barras normales (`/`) en todas partes, incluso en Windows** |

---

## Checklist rápida

| Síntoma | Arreglo |
|---|---|
| **¿No se dispara?** | Mejora la descripción y añade frases de disparo |
| **¿No se carga?** | Comprueba ruta, nombre de fichero y sintaxis YAML |
| **¿Se usa la skill equivocada?** | Haz las descripciones más distintas entre sí |
| **¿La están tapando?** | Revisa la jerarquía de prioridad y renombra si hace falta |
| **¿Faltan skills de plugin?** | Limpia caché y reinstala |
| **¿Falla en ejecución?** | Comprueba dependencias, permisos y rutas |

## Reflexión

- ¿Te has encontrado alguno de estos escenarios? ¿Qué arreglo te habría ahorrado más tiempo?
- ¿Cómo montarías un proceso para validar las skills antes de compartirlas con tu equipo?

---

## Cierre del curso

> Las mejores skills salen de **puntos de dolor reales**. Empieza por las instrucciones que más te encuentras repitiendo.
