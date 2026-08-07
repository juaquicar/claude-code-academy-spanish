# 03 — Definir tools

## El SDK hace el trabajo pesado

> **El SDK de Python de MCP simplifica la creación de herramientas frente a escribir los JSON Schema a mano.**

**Auto-genera los JSON Schema a partir de las funciones decoradas**, permite crear el servidor en **una sola línea** y **elimina la escritura manual de esquemas**.

## La sintaxis

```
decorador → definición de función → tipado de parámetros → validación → lógica
```

- Decorador **`@mcp.tool`**
- Función con **parámetros tipados**
- **`Field()`** de pydantic con `description` para describir cada argumento

## Las dos herramientas del proyecto

**Almacenamiento:** un diccionario en memoria con `doc_id` como clave y el contenido como valor.

| Herramienta | Parámetros | Qué hace |
|---|---|---|
| **`read_doc_contents`** | `doc_id` (string) | Devuelve el contenido del documento desde el diccionario. **Lanza `ValueError` si no existe** |
| **`edit_document`** | `doc_id`, `old_string`, `new_string` | Buscar/reemplazar sobre el contenido. **Incluye validación de existencia** |

**Manejo de errores:** valida que el documento existe **antes** de operar, y lanza `ValueError` si falta.

---

## El inspector del servidor

**MCP Inspector** = **depurador en el navegador** para probar servidores MCP **sin conectarlos a ninguna aplicación**.

**Acceso:**

```bash
mcp dev [fichero_servidor.py]
```

Con el entorno de Python activado. Abre el servidor en un puerto → visita la dirección localhost indicada.

**Interfaz:** barra lateral izquierda con botón **Connect** → barra de navegación superior con las secciones **Resources / Prompts / Tools** → la sección de tools lista las disponibles → al hacer clic se abre el panel derecho para probarla a mano.

**Proceso de prueba:** selecciona la herramienta → introduce los parámetros necesarios (como el ID de documento) → pulsa **Run Tool** → verifica la salida o el mensaje de éxito.

**Qué aporta:** pruebas en vivo durante el desarrollo, simulación de invocación, campos de entrada para parámetros y feedback de éxito/fallo.

> **Es esencial para desarrollar y depurar un servidor MCP antes de desplegarlo.** El inspector está en desarrollo activo: la interfaz puede cambiar, pero la funcionalidad base se mantiene.
