# 10 — Gestión del contexto

*15 minutos* · [Vídeo](https://www.youtube.com/embed/jZQ6b_vVHRc)

**Al terminar sabrás:** qué cuenta como contexto · los **cuatro patrones** de Anthropic y cuál de ellos **no** es una funcionalidad de la API · qué modo de fallo ataca cada uno.

---

Cada petición que envías a Claude tiene una **ventana de contexto**. Un millón de tokens suena a mucho, pero **se acaba antes de lo que crees** cuando estás publicando un agente de verdad. Ahí entra la **gestión del contexto**: cómo mantenerte dentro de la ventana **sin perder lo que importa**.

## Qué cuenta como contexto

El contexto es **todo lo que Claude ve en un turno dado**:

- El system prompt
- El historial de mensajes
- Definiciones de tools y resultados de tools
- Ficheros y skills adjuntos
- Bloques de thinking

Es **la entrada de cada llamada a la API**. Lo pagas al entrar y lo pagas al salir. **Y cuando la ventana se llena, la petición falla.**

> **El objetivo no es meterlo todo. El objetivo es meter lo correcto.**

> **Trampa de examen.** El motivo por el que importa **no** es que Claude rechace peticiones que usen más de media ventana, ni que los mensajes viejos se borren solos a los diez turnos, ni que más contexto sea siempre mejor. Es que **la ventana es finita y pagas por lo que hay dentro**. Es la pregunta 3 del quiz oficial.

Anthropic publica **cuatro patrones** para gestionar el contexto en agentes de larga duración. **Tres son funcionalidades de primera clase de la API, y uno es un patrón de diseño.**

## Patrón 1 · Just-in-time context

**No cargues todo por adelantado.** Carga lo que el agente necesita **ahora**, y deja que traiga más vía tools cuando lo pida.

Piensa en un agente de revisión de cumplimiento: **no** recibe el libro entero del código de edificación metido en su system prompt — **llama a una tool `lookup_building_code`** cuando necesita una sección concreta.

> **Este es *el* patrón de diseño de los cuatro**: nada especial en la API, solo **una decisión deliberada** sobre qué cargas y cuándo.

## Patrón 2 · Compactación en servidor

Cuando una conversación se alarga, la **compactación en servidor** de Anthropic **resume los turnos antiguos en un solo bloque**. Te apuntas añadiendo una clave **`context_management`** a tu petición, con un edit y su tipo:

```
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    context_management={
        "edits": [
            {"type": "compact"}
        ]
    },
    messages=messages,
)
```

La API **auto-resume cuando la entrada cruza el umbral de disparo**. No tienes que llevar tú la cuenta de la longitud de la conversación.

## Patrón 3 · Prompt caching

El **prompt caching** te permite **marcar las partes estables** de una petición — el system prompt, las definiciones de tools, un documento largo — y **reutilizarlas entre llamadas a una fracción del coste**.

> **La aritmética importa más de lo que parece.** Si tu system prompt son 4.000 tokens y lo llamas 100 veces por hora, el caching es la diferencia entre una factura usable y **una llamada de teléfono de finanzas**.

## Patrón 4 · La memory tool

Parte del contexto necesita **sobrevivir entre sesiones**: preferencias del usuario, notas del agente, lo que se decidió la semana pasada. El primitivo recomendado es la **memory tool**.

Cómo funciona:

- Claude **lee y escribe en un directorio de memoria** vía llamadas a tools.
- **Tú implementas el backend de almacenamiento** en el cliente — un sistema de ficheros, una base de datos, un almacén cifrado, lo que quieras.
- Anthropic **auto-inyecta una instrucción de sistema** diciéndole a Claude que **consulte el directorio de memoria antes de empezar a trabajar**.

## Apilar los patrones

En producción normalmente **usarás los cuatro a la vez**. El agente de revisión de cumplimiento cachea su system prompt y sus definiciones de tools, y trae secciones del código de edificación **just in time** vía `lookup_building_code`.

> **Cada patrón ataca un modo de fallo distinto: coste, tamaño de ventana, ausencia de estado.** Elige los que encajen con lo que se te está rompiendo.

## Conclusiones

- El contexto es todo lo que Claude ve en un turno — **y no es gratis ni infinito**. Cuando la ventana se llena, **la petición falla**.
- **Just-in-time context**: carga lo necesario ahora y deja que las tools traigan el resto. **Es el patrón de diseño de los cuatro.**
- **Compactación en servidor**: añade una clave `context_management` y la API resume los turnos antiguos automáticamente al cruzar el umbral.
- **Prompt caching**: marca las partes estables de la petición y reutilízalas entre llamadas a una fracción del coste.
- **Memory tool**: Claude lee y escribe un directorio de memoria vía tools; **el backend es tuyo**, así que el contexto sobrevive entre sesiones.
- Cuatro patrones, un objetivo. Cablearlos a mano — **o usar los managed agents, que traen caching y compactación activados por defecto**.
