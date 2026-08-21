# 04 — Tu primer prompt

*10 minutos* · [Vídeo](https://www.youtube.com/embed/gbetp6D7J_Q)

**Al terminar sabrás:** cómo se cambia entre modos con `Shift + Tab` · la diferencia entre approval y auto-accept · qué hace Plan Mode y cuándo brilla · cómo se ve un prompt bien escrito.

---

A Claude Code le hablas como a cualquier asistente de IA. Al escribir tu prompt hay algunas cosas a tener en cuenta que **te protegen y te facilitan la vida**.

## Auto-accept vs. approval

Puedes elegir si Claude acepta automáticamente cada cambio de fichero que propone, o si te pide permiso explícito cada vez. **Pulsa `Shift + Tab` para ciclar entre modos.**

| Modo | Ficheros | Comandos |
|---|---|---|
| **Approval mode** | Pide permiso cada vez | Pide permiso cada vez |
| **Auto-accept mode** | Se aprueban automáticamente | **Siguen requiriendo tu permiso** |

No hay respuesta correcta ni incorrecta: es lo que a ti te resulte cómodo.

> **Detalle que se cuela.** Auto-accept **no** es barra libre. Los comandos siguen pasando por ti.

## Plan Mode

Dentro del menú de `Shift + Tab` está el **Plan Mode**. Plan Mode toma tu prompt y usa **tools de solo lectura** para analizar tu base de código e investigar la implementación que sugieres. Va **haciendo preguntas aclaratorias** por el camino y luego devuelve un **plan detallado** que puede ejecutar.

Plan Mode es ideal para:

- planificar cambios complejos
- hacer una **revisión de código segura**
- implementaciones multi-paso hacia una funcionalidad — que es exactamente donde destaca

## Ejemplo: añadir un toggle de modo oscuro

Supón que tienes una aplicación que necesita un toggle de modo oscuro. Abre el directorio raíz del proyecto y ejecuta `claude`. Pulsa `Shift + Tab` un par de veces para entrar en Plan Mode y escribe un prompt como:

```
My app needs a dark mode implemented across the entire app. Can you create a toggle switch on the header that allows a user to toggle between light mode and dark mode? I need you to find a good contrast color that works based on my existing light theme.
```

Deja que Claude lo planifique. Después de revisar el plan, si tiene buena pinta, acéptalo y deja que Claude te pida aprobación en cada paso. Al final puedes ver exactamente **qué hizo Claude y cómo llegó a sus conclusiones**.

## Conclusiones

Al usar Claude Code, intenta ser **todo lo descriptivo que puedas** con tu prompt. Si quieres estar en el bucle en cada paso, puedes. Usa **Plan Mode** para dejar que Claude escarbe en los detalles de lo que quieres conseguir **antes** de ejecutar nada de código.
