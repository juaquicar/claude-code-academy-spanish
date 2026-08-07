# 04 — Modos de permisos (Permission Modes)

Sección: *Configure Claude* · [Vídeo](https://www.youtube.com/embed/Fjg4O-ZcRSU)

Los modos de permisos te dejan **decidir una vez** qué puede ejecutar Claude sin pararse a preguntar, en vez de aprobar acción por acción.

`shift-tab` cicla entre los modos del día a día: **manual, accept edits, plan** (y **auto**). El resto es donde vive el Claude Code sin manos; ahí el modo al que recurrir es **auto**.

## Los seis modos

| Modo | Qué permite |
|---|---|
| **Manual** | Solo lee, sin preguntar. Todo lo demás pregunta antes. |
| **Accept edits** | Lecturas, ediciones de fichero y comandos bash comunes de sistema de ficheros sin preguntar. Para iterar sobre código que revisas después. |
| **Plan** | Solo lectura. Investiga y propone cambios sin editar nada. |
| **Auto** | Acepta todo, con **un modelo clasificador aparte** que revisa cada acción antes de ejecutarla. |
| **Don't ask** | Solo permite herramientas pre-aprobadas. Todo lo demás se auto-deniega sin prompt. |
| **Bypass permissions** | Se salta todos los chequeos. Equivalente al flag `dangerously-skip-permissions`. **Solo dentro de un contenedor aislado o VM.** |

## Ciclar con shift-tab

No hace falta memorizar un comando por modo. `shift-tab` cicla los del día a día: manual → accept edits → plan → auto. La **barra de estado** de abajo muestra siempre en qué modo estás.

## Cómo funciona el modo auto

Claude corre solo, pero antes de que cada acción se ejecute, un **modelo clasificador aparte** la revisa. El clasificador **vigila la intención**: busca movimientos que escalen más allá de lo que realmente pediste.

**Lo que está diseñado para bloquear:**

- Deploys y migraciones de producción
- Force push, o canalizar código descargado directo a una shell
- Enviar datos sensibles a endpoints externos
- Destruir ficheros que existen para la sesión

**Lo que deja pasar:**

- Ediciones locales en tu proyecto
- Instalar dependencias desde tu lock file
- Peticiones de solo lectura
- Push a tu propia rama

## Lo que el clasificador NO puede hacer

**Comprueba intención, no corrección.** No detecta si el código funciona. Si pides refactorizar la autenticación y escribe una autenticación rota, el clasificador la deja pasar — porque *roto* no es *peligroso*.

Por eso se **empareja el modo auto con un stop hook que lance tus tests**:

- **Auto mode** vigila lo que Claude *intenta* hacer, mientras corre → guarda la **intención**, antes de cada acción.
- **Stop hook** confirma que el código realmente funciona, cuando Claude termina → guarda la **corrección**, después.

> Las salvaguardas de auto mode aún están evolucionando: consulta la documentación para las listas de bloqueo/permitidos actuales.

## Don't ask, para runs desatendidos

Es el movimiento correcto siempre que **no haya un humano para aprobar prompts**: pipelines de CI, jobs programados, lotes nocturnos.

Solo se permiten herramientas pre-aprobadas; lo que esté fuera de la lista se auto-deniega sin prompt. Ese es todo el objetivo: tu pipeline sigue avanzando en vez de colgarse esperando una aprobación que nadie va a dar.

## Empareja el modo con el trabajo

- **Auto** = modo sin manos. Clasificador (intención) antes + stop hook (corrección) después.
- **Don't ask** = pipelines desatendidos donde no hay nadie para aprobar.
- **Bypass permissions** = solo dentro de contenedores aislados y VMs.
