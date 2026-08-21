# 03 — Instalar Claude Code

*10 minutos* · [Vídeo](https://www.youtube.com/embed/0kILa02vKuI)

**Al terminar sabrás:** cómo instalarlo en terminal, VS Code, JetBrains, escritorio y web · qué método no soporta auto-actualizaciones · qué alcance tiene sobre tus ficheros · cuál elegir según lo que busques.

---

## Terminal

En **macOS, Linux o WSL**, se instala de una vez con el comando `curl`. Si prefieres Homebrew, también puedes usar `brew install`, pero **ese método no soporta auto-actualizaciones**.

En **Windows** hay varias opciones. En PowerShell, el comando `Invoke-RestMethod`. En CMD, el comando `curl`. También hay un comando `winget` disponible, aunque **igual que Homebrew, no se auto-actualiza**.

Tras la instalación deberías poder ejecutar el comando `claude`. Si no, reinicia el terminal. Ve al directorio de tu proyecto y ejecuta:

```
claude
```

Pasarás por unos pasos iniciales: elegir el tema de color e iniciar sesión con tu cuenta de Claude (Pro, Max o Enterprise) o con una API key. **Si tu organización tiene una cuenta Claude Enterprise, asegúrate de seleccionar esa opción.**

> **El alcance lo marca el directorio.** En el directorio en el que ejecutes `claude`, tendrá acceso a **ese directorio y a todas sus subcarpetas**.

## Visual Studio Code

Abre el panel de Extensions y busca "Claude Code". Busca la extensión **de Anthropic con el check azul de verificación**. Instálala.

Puede que tengas que reiniciar VS Code. Una vez arrancado, abre la paleta de comandos con `Ctrl/Cmd + Shift + P` y busca **"Claude Code Open in New Tab"**. También puedes hacer clic en el logo de Claude si lo ves en la barra lateral.

La extensión de VS Code ofrece una experiencia muy parecida a la del terminal. También puedes **renunciar a la interfaz** y usar la experiencia de terminal directamente desde los settings.

## JetBrains

Instala el plugin de Claude Code desde el **JetBrains Marketplace**. Después de instalarlo, reinicia el IDE. Al reabrirlo verás el logo de Claude; al pulsarlo se abre un panel con la experiencia de terminal funcionando junto a tu editor.

## Desktop

Tras instalar Claude Desktop e iniciar sesión, verás arriba un toggle etiquetado **"Code"**. El aspecto es similar al del chat, pero te permite trabajar en una carpeta concreta, cambiar permisos e incluso trabajar en un entorno en la nube.

## Web

En la web, accedes a Claude Code yendo a `claude.ai/code`, o pulsando la etiqueta **"Code"** en la barra lateral de la app de chat. Funciona de forma parecida a la app de escritorio, pero **estás restringido a repositorios de GitHub**.

## ¿Cuál debería usar?

| Si quieres… | Usa |
|---|---|
| **Estar en la cresta de la ola** | El **terminal** — las novedades llegan ahí primero |
| Que Claude Code se sienta entrelazado con tu editor | Las **integraciones de IDE** (experiencia casi idéntica) |
| Dejar a Claude corriendo en segundo plano mientras haces otras cosas | **Desktop** |
| Trabajar en remoto sobre un repositorio de GitHub | **Claude Code en la web** |

Cómo quieras usar Claude Code es cosa tuya.
