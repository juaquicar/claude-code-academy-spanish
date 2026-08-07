# 08 — Prompt caching

Funcionalidad que **acelera las respuestas y reduce el coste** reutilizando el trabajo computacional de peticiones anteriores.

## El problema

Flujo normal de una petición:

1. El usuario envía un mensaje.
2. Claude **procesa la entrada** — crea estructuras de datos internas, hace cálculos.
3. Claude genera la salida.
4. **Claude descarta todo ese trabajo de procesamiento.**
5. Listo para la siguiente petición.

> Cuando la siguiente petición contiene **exactamente los mismos mensajes de entrada**, Claude tiene que **repetir todo el trabajo que acaba de tirar**.

## La solución

El caché **almacena el resultado de procesar los mensajes de entrada** en vez de descartarlo. Cuando aparece una entrada idéntica en una petición posterior, Claude **recupera el trabajo cacheado** en lugar de reprocesar.

---

## Las reglas del caché

Esta es la parte densa del capítulo y donde está lo que se pregunta.

| Regla | Detalle |
|---|---|
| **Duración** | **1 hora** como máximo |
| **Activación** | Manual: hay que añadir un **cache breakpoint** a los bloques de mensaje |
| **Alcance** | Se cachea **todo el contenido hasta el breakpoint, incluido** |
| **Invalidación** | **Cualquier cambio en el contenido anterior al breakpoint invalida el caché entero** |
| **Orden de procesado** | **tools → system prompt → messages**, unidos en ese orden |
| **Máximo de breakpoints** | **4 por petición** |
| **Umbral mínimo** | **1024 tokens** para que el contenido se cachee |

### Formatos de bloque de texto

```python
# Forma corta — NO admite cache control
content = "una cadena de texto"

# Forma larga — OBLIGATORIA para cachear
content = [{"type": "text", "text": "contenido", "cache_control": {...}}]
```

> ⚠ Si usas la forma corta, **no puedes cachear**. Es el fallo más fácil de cometer.

### Dónde se pueden poner breakpoints

- Esquemas de herramienta
- System prompts
- Bloques de mensaje: texto, imagen, tool use, tool result

**Varios breakpoints** crean **varias capas de caché**: son posibles los **aciertos parciales** si solo cambia el contenido posterior.

**Mejores casos de uso:** contenido idéntico repetido — system prompts, definiciones de herramientas, prefijos estáticos de mensajes.

---

## El caché en la práctica

**Montaje:** modifica tu función `chat` para activar el caché por defecto en herramientas y system prompts.

### Cachear esquemas de herramienta

Añade el campo `cache_control` con `type: "ephemeral"` a la **última** herramienta de la lista.

> **Buena práctica:** haz una **copia** de la lista de herramientas, clona el último esquema, añádele el cache control y sobrescribe — así **no modificas los esquemas originales**.

### Cachear el system prompt

Envuelve el system prompt en un diccionario de bloque de texto con `cache_control` de tipo `"ephemeral"`.

Se pueden fijar puntos de caché para herramientas **y** system prompt en la misma petición.

### Leer el uso de tokens

| Campo | Qué mide |
|---|---|
| **`cache_creation_input_tokens`** | Tokens **escritos al caché** en el primer uso |
| **`cache_read_input_tokens`** | Tokens **recuperados del caché** en peticiones idénticas posteriores |

Son posibles las **lecturas parciales** cuando solo parte del contenido coincide con lo cacheado.

> **Recordatorio de invalidación:** cualquier cambio en el contenido cacheado —herramientas o system prompt— **invalida el caché y fuerza una creación nueva**. Si estás iterando sobre el system prompt, no vas a ver aciertos.
