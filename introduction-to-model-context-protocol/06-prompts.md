# 06 — Prompts

**Prompts** = **instrucciones ya escritas y probadas** que los servidores MCP exponen a los clientes para tareas especializadas.

## Para qué

- Los **autores del servidor** definen prompts de alta calidad **adaptados a su dominio**.
- Los **clientes** los invocan mediante **slash commands** — p. ej. `/format`.
- Es una **alternativa a que el usuario escriba sus propios prompts**.

> **El beneficio:** los autores del servidor crean prompts **optimizados y probados**, en vez de dejar la calidad del prompt en manos del usuario final.

## Definirlos en el servidor

- Decorador **`@prompt`** con **nombre y descripción**.
- La función **recibe argumentos** — p. ej. un ID de documento.
- **Devuelve una lista de mensajes** en formato usuario/asistente.
- Esos mensajes **se envían directamente a Claude**.

```python
@prompt(name="format", description="rewrites document in markdown")
def format_document(doc_id: str) -> list[messages]:
    return [base.user_message(prompt_text)]
```

## Invocarlos desde el cliente

```python
async def list_prompts(self):
    result = await self.session.list_prompts()
    return result.prompts

async def get_prompt(self, prompt_name, arguments):
    result = await self.session.get_prompt(prompt_name, arguments)
    return result.messages
```

**El flujo de los argumentos:**

> Argumentos del cliente → **argumentos con nombre** de la función del prompt → **interpolados en el texto** de la plantilla → **array de mensajes** que forma la entrada para el modelo.

## El flujo completo, de punta a punta

1. El usuario escribe **`/format`**.
2. Selecciona un documento.
3. El **servidor devuelve el prompt especializado** con el ID interpolado.
4. El **cliente lo envía a Claude**.
5. **Claude usa las herramientas** para leer, reformatear y guardar el documento.

> **La idea:** los prompts son **plantillas definidas por el servidor** que los clientes invocan con parámetros, permitiendo **instrucciones reutilizables con contenido dinámico**.
>
> **El propósito:** encapsular la **experiencia en prompt engineering del dominio** dentro de servidores MCP especializados.
