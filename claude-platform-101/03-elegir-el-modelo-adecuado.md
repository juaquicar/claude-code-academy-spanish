# 03 — Elegir el modelo adecuado

*15 minutos* · [Vídeo](https://www.youtube.com/embed/UAeTSBsK71A)

**Al terminar sabrás:** los tiers de modelo y para qué sirve cada uno · cómo montar una evaluación mínima · la regla para elegir · cómo enrutar distintas tareas a distintos modelos.

---

Vas a publicar una app con Claude. ¿Qué modelo eliges? **Si vas por defecto al más listo, la factura te sorprenderá. Si eliges el más barato, la salida puede no dar la talla.** Cada modelo tiene sus compensaciones, y acertar afecta a **calidad y coste**.

## Los tiers de modelo

Anthropic ofrece actualmente **cuatro tiers**, y eliges entre ellos con el parámetro `model` de tu llamada.

> **Nota del propio curso:** en el momento de grabarlo, **Claude Fable no estaba disponible de forma general** y no aparece en el vídeo. Más sobre Claude Fable y Claude Mythos [aquí](https://www.anthropic.com/news/claude-fable-5-mythos-5).

| Tier | Perfil | Para qué |
|---|---|---|
| **Claude Fable** | El más capaz hasta la fecha; un tier **por encima de Opus**, con **coste significativamente mayor** | Tus desafíos más duros — resérvalo para trabajo donde esa capacidad extra compense |
| **Claude Opus** | El más capaz de las tres familias principales, pero **el más lento y caro** de las tres | Razonamiento profundo, análisis complejo, codificación multi-paso, escritura con matices |
| **Claude Sonnet** | El punto dulce: **combinación equilibrada** de inteligencia, velocidad y coste | La mayor parte del trabajo de producción |
| **Claude Haiku** | **El más rápido y barato**, optimizado para velocidad y eficiencia de coste antes que para inteligencia máxima | Alto volumen y baja complejidad: clasificación, extracción, enrutado |

## Empieza con una evaluación sencilla

**Antes de escribir código de producción, monta una evaluación**: un conjunto de entradas de ejemplo que pasas por cada modelo y puntúas según lo que significa "buena salida" para tu caso.

> No necesitas nada sofisticado: **20 o 30 ejemplos representativos de tu carga real** bastan para empezar.

Luego sube por los tiers:

1. Pasa tus ejemplos por **Haiku** primero. Si la calidad aguanta, has terminado — y te acabas de ahorrar mucho dinero.
2. Si no aguanta, sube a **Sonnet**.
3. **Recurre a Opus solo cuando la tarea lo pida.**

## Comparar los tiers en vivo

Mandamos el mismo prompt por los tres modelos y miramos latencia y conteo de tokens:

```
models = ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"]

for model in models:
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    print(model, response.usage)
```

Dos cosas pasan aquí:

- El bucle **cambia el campo `model`** en cada petición. Mismo prompt, mismos max tokens; **solo cambia el modelo**.
- **`response.usage`** te devuelve los tokens de entrada y salida directamente de la API, que es **sobre lo que se calcula tu factura**.

Al ejecutarlo verás tres modelos y tres conjuntos de números. **Opus** tarda más y lee más pulido — pero para una definición de dos frases, **ese pulido se desperdicia**. **Sonnet** aprieta un poco la redacción. Y **Haiku** vuelve, a menudo en menos de un segundo, con una respuesta de dos frases muy competente.

> **Y ese es el asunto entero:** **el modelo correcto es el más barato cuya salida publicarías de verdad.**

Para una definición, Haiku sobra. Para redactar una respuesta regulatoria, harías la misma comparación y probablemente acabarías en Opus. **La evaluación tiene la misma forma siempre.**

## Enrutar trabajo distinto a modelos distintos

En una app real enrutarías distintos tipos de trabajo a distintos modelos **dentro del mismo endpoint**. Un dashboard de operaciones con una ruta de procesamiento de documentos:

- Cada fichero entrante se **clasifica con Haiku**.
- Las actualizaciones a cliente se **redactan con Sonnet**.
- Solo las respuestas a RFP **recurren a Opus**.

**Una cola, tres modelos, elegidos por tarea.**

## Conclusiones

- Los tiers: **Opus** para problemas difíciles, **Sonnet** para el trabajo diario, **Haiku** para volumen (y **Fable** por encima de Opus, para lo más duro).
- Monta una evaluación sencilla — **20 o 30 ejemplos representativos de tu carga real** — antes de escribir código de producción.
- Ejecuta la evaluación **de Haiku hacia arriba** y párate en el modelo más barato cuya salida publicarías.
- **`response.usage`** informa de tokens de entrada y salida, que es la base de tu factura.
- En producción, **enruta tareas distintas a modelos distintos** dentro del mismo endpoint en vez de elegir un modelo para todo.
