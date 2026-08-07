# 05 — Resources

**Resources** = funcionalidad del servidor MCP que **expone datos a los clientes para operaciones de lectura**.

## Los dos tipos

| Tipo | URI | Ejemplo |
|---|---|---|
| **Directo / estático** | URI fija | `docs://documents` |
| **Con plantilla** | URI parametrizada con comodines | `documents/{doc_id}` |

## El flujo

1. El **cliente** envía una petición de lectura **con la URI**.
2. El **servidor MCP** empareja la URI con la función del resource.
3. El servidor **ejecuta la función** y devuelve el resultado.
4. El cliente **recibe los datos** en el mensaje de resultado.

## Definirlos en el servidor

- Decorador **`@mcp.resource`**
- Define la **URI** — una dirección tipo ruta
- Fija el **MIME type**: `application/json`, `text/plain`…
- En los **resources con plantilla**, los parámetros de la URI **se convierten en argumentos con nombre** de la función
- **El SDK de Python serializa automáticamente** los valores devueltos a cadenas

**MIME types** = **pistas para el cliente** sobre el formato devuelto, para que sepa cómo deserializarlo.

> **Patrón habitual: un resource por cada operación de lectura distinta** — listar elementos vs. traer uno solo.

## Accederlos desde el cliente

Función **`read_resource`**, que recibe una **URI** y pide el resource al servidor.

```python
async def read_resource(self, uri):
    result = await self.session.read_resource(AnyUrl(uri))
    resource = result.contents[0]
    if resource.mime_type == "application/json":
        return json.loads(resource.text)
    return resource.text
```

**Dependencias:** el módulo **`json`** y **`AnyUrl`** de pydantic para el tipado.

**Lógica de parseo:** se comprueba **`resource.mime_type`** para decidir cómo interpretar los datos — de ahí que el MIME type importe.

## Qué se consigue

- Las funciones del cliente MCP **las llaman otros componentes** de tu aplicación.
- Permite **seleccionar documentos desde la CLI** con las flechas y la barra espaciadora.
- **El contenido del resource seleccionado se incluye automáticamente en los prompts al LLM.**

> **El resultado clave:** ya **no hacen falta herramientas para leer el contenido de los documentos durante el chat**. Los datos llegan por otra vía.

Ese contraste —resources traen datos, tools ejecutan acciones— es el que ordena el [capítulo 07](07-las-tres-primitivas.md).
