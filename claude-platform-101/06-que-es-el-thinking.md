# 06 — ¿Qué es el thinking?

*15 minutos* · [Vídeo](https://www.youtube.com/embed/4SunBsMGRwA)

**Al terminar sabrás:** qué es el extended thinking y por qué es visible · cómo se activa en Opus 4.7 · dónde va exactamente el parámetro `effort` y sus cinco niveles · cuándo **no** usarlo.

---

Algunas tareas necesitan más que una respuesta rápida. Claude puede **trabajar el problema antes de responder** — una funcionalidad llamada **extended thinking**.

El modo de fallo que intentamos evitar: haz a un modelo una pregunta multi-paso y que responda inmediatamente, y **puede equivocarse con toda seguridad**.

## Qué es el extended thinking

El extended thinking permite a Claude **razonar paso a paso antes de producir la respuesta final**. Cuando está activado, Claude genera **tokens de razonamiento internos** — lo que suele llamarse **chain of thought** — y luego entrega la respuesta.

> **El razonamiento no está oculto: lo ves en la respuesta, junto al texto final.**

## Thinking adaptativo en Opus 4.7

Con Opus 4.7, el thinking es **adaptativo**. **No eliges un presupuesto de tokens.** Lo activas y **Claude decide dinámicamente cuándo pensar y cuánto**.

Para controlar cuánto piensa, usas el parámetro **`effort`**.

> **La trampa, dicha por el propio curso:** `effort` va **dentro de `output_config`**, no al lado del bloque `thinking`.

Los niveles:

| Nivel | |
|---|---|
| `low` | |
| `medium` | |
| `high` | **el valor por defecto** |
| `xhigh` | extra high |
| `max` | |

## Cuándo usarlo (y cuándo saltárselo)

**Ayuda con:**

- Matemáticas y lógica multi-paso
- Depuración de código
- Análisis regulatorio
- Cualquier cosa con **compensaciones o comparación de opciones**

**Sáltatelo para** clasificación simple, extracción o boilerplate. Ahí **solo añade latencia y coste** sin mejorar realmente los resultados.

## El thinking en acción

Un bucle de agente con una tool de tiempo, pidiéndole a Claude que planifique un viaje por carretera saliendo de San Francisco — dos paradas, sopesando tiempo meteorológico y tiempo de conducción. **Eso sí es una compensación real**, el tipo de pregunta donde el thinking se gana el sueldo.

```
import anthropic

client = anthropic.Anthropic()

weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"],
    },
}

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # low | medium | high | xhigh | max
    tools=[weather_tool],
    messages=[
        {
            "role": "user",
            "content": "Plan a road trip out of San Francisco with two stops, "
                       "weighing weather and drive time.",
        }
    ],
)
```

Al ejecutarlo, la salida es más interesante de lo normal: verás **bloques de thinking** donde Claude trabaja las compensaciones, seguidos de llamadas a tools para consultar cada ciudad, y finalmente un bloque de texto con la recomendación.

**El razonamiento es visible — de eso se trata.**

## Por qué importa en producción

En una app de producción, esto es la diferencia entre un agente que encuentra problemas de uno en uno y **un agente que los conecta**. En una app de revisión de cumplimiento, activar el thinking adaptativo en la llamada de auto-revisión permite al agente razonar **a través de las secciones** del informe — pillando cosas como que una especificación de carga de viento en la sección tres **contradice** la especificación de material en otra parte del documento.

## Conclusiones

- El **extended thinking** le da a Claude margen para razonar antes de responder, y **el razonamiento es visible** en la respuesta.
- Con Opus 4.7 se activa con **`thinking: {"type": "adaptive"}`** — sin presupuesto de tokens; Claude decide cuándo y cuánto piensa.
- Ajusta la profundidad con el parámetro **`effort` dentro de `output_config`**: `low`, `medium`, `high` (por defecto), `xhigh` o `max`.
- Úsalo para problemas duros y cargados de compensaciones. **Sáltatelo en los simples**: ahí solo cuesta latencia y tokens.
