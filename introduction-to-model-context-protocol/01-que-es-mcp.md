# 01 — Qué es MCP

**MCP** = *Model Context Protocol*, una **capa de comunicación** que aporta a Claude **contexto y herramientas** sin obligar al desarrollador a escribir código tedioso.

## Arquitectura

```
Tu servidor  ──►  Cliente MCP  ──►  Servidor MCP
                                     ├── tools
                                     ├── resources
                                     └── prompts
```

Un **cliente MCP** conecta con un **servidor MCP**. El servidor contiene **tools, resources y prompts** como componentes internos.

## El problema que resuelve

El enfoque tradicional obliga al desarrollador a **escribir a mano los esquemas y las funciones de cada integración**.

> Un chatbot de GitHub exigiría implementar herramientas para repositorios, pull requests, issues y proyectos. **Eso crea una carga de mantenimiento** en servicios complejos con muchas funcionalidades.

## La solución

MCP **traslada la definición y la ejecución de herramientas del servidor del desarrollador a un servidor MCP dedicado**.

Un **servidor MCP es una interfaz a un servicio externo**, que envuelve su funcionalidad en **herramientas ya construidas**.

**El beneficio:** elimina la necesidad de que escribas y mantengas esquemas e implementaciones. **Otro las escribe y las empaqueta en el servidor MCP.**

## Preguntas frecuentes

| Pregunta | Respuesta |
|---|---|
| **¿Quién escribe los servidores MCP?** | **Cualquiera** — pero a menudo los propios proveedores del servicio crean implementaciones oficiales |
| **¿En qué se diferencia de llamar al API directamente?** | Te **ahorra tiempo**: te da esquemas y funciones ya hechos en vez de tener que escribirlos |
| **¿Y de tool use?** | **Son complementarios, no lo mismo.** MCP se centra en **quién hace el trabajo** de crear las herramientas |

## El valor central

> **Reduce la carga del desarrollador externalizando la creación de herramientas a las implementaciones de servidor MCP**, en vez de exigir desarrollo propio para cada integración.
