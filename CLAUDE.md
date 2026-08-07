# CLAUDE.md

Repo de resúmenes en español de los cursos de la Anthropic Academy (Skilljar).
Cada curso vive en `<slug-del-curso>/` con un `.md` por lección más un `curso-interactivo.html`.

## El procedimiento, de principio a fin

### 1 · Extraer

```bash
python3 scripts/extraer_curso.py <slug-del-curso>
```

Deja en `/tmp/<slug>/` un `raw_<id>.md` por lección más `indice.txt` con el orden del currículo. Usa la sesión de Chrome ya logueada de juanma.quijada@stratosgs.com; descifra las cookies de Skilljar con la clave del keyring y las borra al terminar.

Si un `raw_*.md` sale casi vacío, esa lección se renderiza por JavaScript (típicamente un quiz). Búscale el endpoint AJAX en el HTML de la lección en vez de dar la lección por perdida.

**No lances un quiz oficial sin permiso:** empezarlo registra un intento en la cuenta del usuario. Cargarlo en modo lectura (`load=true`) sí vale para saber cuántas preguntas tiene.

### 2 · Escribir los `.md`

Un fichero por lección: `NN-titulo-en-kebab-case.md`, numerado desde `01` en el orden del currículo. Más un `README.md` con índice y el hilo conductor del curso.

Convenciones:

- **Todo en español**, salvo lo que se teclea o se lee en pantalla: comandos, flags, nombres de campo, rutas, mensajes de error, nombres de los subagentes y modos. Esos van verbatim.
- **Enlaza el vídeo original** bajo el título de cada capítulo.
- **Conserva los datos concretos**: números, nombres exactos de eventos y flags, códigos de salida, límites. Son lo que después pregunta un quiz.
- **Marca lo contraintuitivo** con una caja de trampa. Si el material dice "esto despista a todo el mundo", eso es material de examen.
- **Tablas para lo enumerable** (modos, campos, eventos, comparativas). Prosa para el razonamiento.
- Cierra cada capítulo con la lista de conclusiones del propio material, no con una inventada.

Nunca añadas contenido que no esté en el curso. Reorganizar, condensar y traducir sí; extrapolar no. Si algo del material parece incompleto, dilo explícitamente en el fichero en vez de rellenarlo.

### 3 · Capítulo de quiz

- **Si el curso tiene quiz oficial**, se hace en la plataforma y luego se registran aquí las preguntas reales con su feedback textual y los distractores descartados, más un banco extra que ataque los detalles que el oficial no toca.
- **Si no lo tiene**, se construye una autoevaluación desde el material y se dice en la primera línea que el curso no trae quiz.

### 4 · El HTML interactivo

Copia el de un curso ya hecho y sustituye el contenido. Los tokens CSS, los widgets y el JS son comunes a propósito: los cursos deben leerse como un mismo producto.

Qué lleva siempre:

- Barra superior con progreso, buscador (`⌘/Ctrl+K`) y tema claro/oscuro, todo en `localStorage` bajo un prefijo propio del curso.
- Sidebar con scrollspy y marca de leído por capítulo.
- Flashcards y quiz con corrección al momento, explicando **por qué**.
- Un widget interactivo por cada concepto que cuesta entender leyendo: pestañas para comparaciones, línea de tiempo para procesos, dial para escalas, decisor de dos preguntas para reglas de elección, constructor en vivo para ficheros de configuración.

Reglas de estilo que no se negocian:

- **Un solo fichero, sin dependencias externas ni conexión.** Se abre con doble clic.
- **Texto con tokens de texto**, nunca con el color de un acento. Sobre fondo de acento usa `--on-accent`, que cambia en modo oscuro; blanco sobre salmón no tiene contraste.
- **Los items de grid llevan `min-width:0`.** Por defecto es `auto` y un `<pre>` largo revienta el ancho de la página. Ya ha pasado dos veces.

### 5 · Validar antes de darlo por bueno

```bash
python3 scripts/validar_html.py <curso>/curso-interactivo.html
```

Comprueba anidamiento HTML, sintaxis del JS, que los widgets generados por JavaScript renderizan de verdad, y que no hay desbordamiento horizontal a 1360 / 900 / 700 px. Tiene que salir "Todo correcto" antes de decir que está hecho.

Para mirar el resultado con los ojos, Chrome headless saca capturas:

```bash
/opt/google/chrome/chrome --headless --disable-gpu --no-sandbox \
  --user-data-dir=/tmp/prof --window-size=1360,1700 \
  --virtual-time-budget=4000 --screenshot=/tmp/x.png "file://$PWD/<curso>/curso-interactivo.html"
```

Ojo: headless captura desde el origen de la página, así que `#ancla` en la URL no sirve para ver una sección de más abajo. Para eso, inyecta un `<script>` en una copia temporal.

### 6 · Cerrar

Actualiza el `README.md` raíz con la fila del curso nuevo y su párrafo de resumen. Commit en español, con el cuerpo explicando qué cubre el curso.

## Detalles del entorno

- La extensión Claude-in-Chrome **no está instalada**. Para contenido tras login, el camino es el script de cookies; para renderizar, Chrome headless. No pierdas tiempo con `tabs_context_mcp`.
- `WebFetch` sirve para la página pública de un curso (currículo, descripción) pero **falla en todo lo que requiera sesión**.
- Herramientas disponibles: `python3` con `cryptography`, `secretstorage` y `bs4`; `node`; `curl`; Chrome en `/opt/google/chrome/chrome`. No hay `html2text` ni `markdownify` — el conversor propio está en `extraer_curso.py`.
- Remoto: `git@github.com:juaquicar/claude-code-academy-spanish.git`, rama `main`, SSH ya autenticado como `juaquicar`.
