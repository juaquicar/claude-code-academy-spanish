# 08 — Skills

*15 minutos* · [Vídeo](https://www.youtube.com/embed/3fGaS8mcD9Q)

**Al terminar sabrás:** la diferencia entre tools y skills en una frase · cómo se carga una skill (y por qué eso mantiene el contexto ligero) · cómo se sube y cómo se adjunta a una petición · por qué se emparejan con code execution.

---

Las **Skills** son **carpetas de instrucciones, scripts y recursos** que Claude carga dinámicamente para rendir mejor en tareas especializadas. En el núcleo de toda Skill hay un fichero **`SKILL.md`**: un conjunto empaquetado de instrucciones que **subes una vez** y luego **adjuntas a cualquier llamada `messages.create`**.

Estás enseñándole a Claude cómo lo haces **tú**: tu formato de informe de estado, tu checklist de revisión, tus notas de versión. Claude lee la Skill, sigue el procedimiento y produce salida **con tu forma**.

## Skills vs. tools

Conviene tenerlo claro, porque resuelven problemas distintos:

- **Las tools conectan a Claude con datos y acciones.** "Consulta esta sección del código", "envía este correo" — Claude llama a la tool y **algo más lo ejecuta**.
- **Las skills le enseñan a Claude un procedimiento.** "Genera el informe diario de estado siguiendo esta plantilla" — es un **playbook** que Claude lee y sigue, lo que a veces implica **ejecutar scripts incluidos**.

> **La forma de recordarlo: las tools son sobre *qué* puede hacer Claude; las skills, sobre *cómo* quieres que se haga.**

## Carga progresiva

Las Skills **no se cargan enteras en contexto al arrancar**. Al principio **solo se cargan el nombre y la descripción**. Cuando tu agente decide que una Skill es relevante, **entonces carga la Skill completa** en contexto.

> Eso mantiene tu contexto ligero **aunque tengas muchas Skills disponibles**.

## Subir una Skill

Las Skills **se suben una vez a tu workspace** y luego se referencian **por ID**. Puedes subirlas directamente en la Claude Platform o programáticamente:

```
skill = client.beta.skills.create(
    display_title="Status Report Generator",
    files=files_from_dir("status-report-skill"),  # folder containing SKILL.md
)

print(skill.id)  # reference this ID in future requests
```

Para el ejemplo queremos un **generador de informes de estado**. Todas las reglas sobre qué hace bueno a un informe — secciones, tono, cómo resumir, cómo tratar los bloqueos — **viven en una Skill empaquetada de antemano**. El registro de actividad en sí es solo una cadena que se pasa en tiempo de petición.

## Adjuntar una Skill a una petición

Las Skills se adjuntan a través de la **configuración del container**: un array **`skills`** dentro del container, donde cada entrada nombra un **`skill_id`** y una **`version`**.

```
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    betas=["skills-2025-10-02", "code-execution-2025-08-25"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": skill.id,
                "version": "latest",
            }
        ]
    },
    tools=[
        {
            "type": "code_execution_20250825",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": f"Generate the daily status report from this activity log:\n\n{activity_log}",
        }
    ],
)
```

Tres cosas que señalar:

- Llamamos a **`client.beta.messages.create`**, no a la estándar, y pasamos la funcionalidad de skills vía **beta header**. A fecha del vídeo, las Skills siguen **en beta**.
- **`container.skills`** es donde se adjunta la Skill. Es una **lista**, así que **puedes apilar varias Skills en una llamada**.
- **Code execution** también está activado. Las Skills **encajan bien con code execution**, porque los procedimientos de una Skill pueden hacer trabajo real — como ejecutar scripts en un terminal.

## Ejecutándolo

La salida es un informe de estado formateado **exactamente como dice la Skill**. Secciones, tono, tratamiento de bloqueos — todo viene del `SKILL.md` que subiste. **El prompt del usuario es una línea; el procedimiento vive en la Skill.**

En producción, así es como un equipo **estandariza la salida de una funcionalidad entera**: en un endpoint de informe diario, todos los PM reciben la misma estructura, el mismo tono, las mismas secciones y en el mismo orden — **sin que nadie copie y pegue una plantilla en un prompt**.

## Conclusiones

- **Las Skills empaquetan tus procedimientos.** Un fichero `SKILL.md` (más scripts y recursos) le enseña a Claude cómo quieres que se haga algo.
- **Tools vs. Skills:** las tools son sobre **qué** puede hacer Claude; las Skills, sobre **cómo** quieres que se haga.
- **Las Skills cargan progresivamente.** Solo nombre y descripción al arrancar; la Skill completa cuando el agente decide usarla.
- **Sube una vez** con `client.beta.skills.create` y **adjunta** con `container.skills` en cualquier `messages.create` — es una lista, así que puedes apilarlas.
- **Emparéjalas con code execution** cuando el procedimiento de la Skill tenga que hacer trabajo real.
- Recurre a una Skill cuando **el *cómo* importa tanto como el *qué***.

> **¿Quieres profundizar?** El curso dedicado: [Introduction to agent skills](../introduction-to-agent-skills/README.md).
