#!/usr/bin/env python3
"""Descarga un curso de anthropic.skilljar.com y lo extrae a markdown crudo.

Uso:  python3 scripts/extraer_curso.py <slug-del-curso> [directorio-salida]
Ej.:  python3 scripts/extraer_curso.py introduction-to-subagents /tmp/curso

Usa la sesión de Chrome ya logueada: descifra las cookies de Skilljar del
perfil por defecto con la clave "Chrome Safe Storage" del keyring del sistema.
No pide credenciales ni las ve nunca en claro.

Salida en <directorio-salida>/:
  curso.html          la página índice del curso
  L<id>.html          cada lección, HTML crudo
  raw_<id>.md         cada lección convertida a markdown
  indice.txt          id | título, en orden de currículo

Requiere: python3-cryptography, python3-secretstorage, python3-bs4, curl.
"""
import html
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time

BASE = "https://anthropic.skilljar.com"
CHROME_COOKIES = "~/.config/google-chrome/Default/Cookies"


# ─────────────────────────── cookies ───────────────────────────
def cookies_skilljar(tmpdir):
    """Devuelve la cabecera Cookie para anthropic.skilljar.com."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    import secretstorage

    col = secretstorage.get_default_collection(secretstorage.dbus_init())
    if col.is_locked():
        col.unlock()
    pw = next((i.get_secret() for i in col.get_all_items()
               if i.get_label() == "Chrome Safe Storage"), None)
    if pw is None:
        sys.exit("No se encuentra 'Chrome Safe Storage' en el keyring. "
                 "¿Chrome instalado y el keyring desbloqueado?")

    key = PBKDF2HMAC(algorithm=hashes.SHA1(), length=16,
                     salt=b"saltysalt", iterations=1).derive(pw)

    def dec(v):
        if not v or v[:3] not in (b"v10", b"v11"):
            return ""
        d = Cipher(algorithms.AES(key), modes.CBC(b" " * 16)).decryptor()
        out = d.update(v[3:]) + d.finalize()
        out = out[: -out[-1]]
        try:
            return out.decode("utf8")
        except UnicodeDecodeError:
            return out[32:].decode("utf8", "replace")  # prefijo sha256 del dominio

    src = os.path.expanduser(CHROME_COOKIES)
    dst = os.path.join(tmpdir, "Cookies")
    shutil.copy2(src, dst)  # copiar: Chrome mantiene el fichero bloqueado
    con = sqlite3.connect(dst)
    rows = con.execute(
        "select name, encrypted_value from cookies "
        "where host_key='anthropic.skilljar.com'"
    ).fetchall()
    if not rows:
        sys.exit("Sin cookies de anthropic.skilljar.com. Inicia sesión en Chrome primero.")
    return "; ".join(f"{n}={dec(v)}" for n, v in rows)


def get(url, cookie, dest):
    subprocess.run(
        ["curl", "-sS", "-b", cookie, "-A", "Mozilla/5.0", url, "-o", dest],
        check=True,
    )
    return open(dest, encoding="utf8").read()


# ─────────────────────────── html → markdown ───────────────────────────
def _conv(node, out, depth=0):
    from bs4.element import NavigableString, Tag

    if isinstance(node, NavigableString):
        out.append(str(node))
        return
    if not isinstance(node, Tag):
        return
    n = node.name
    if n in ("script", "style", "svg", "button"):
        return
    if n == "iframe":
        if node.get("src"):
            out.append(f"\n[VIDEO] {node['src']}\n")
        return
    if n in ("h1", "h2", "h3", "h4", "h5", "h6"):
        out.append("\n\n" + "#" * int(n[1]) + " ")
        for c in node.children:
            _conv(c, out, depth)
        out.append("\n")
        return
    if n == "p":
        out.append("\n\n")
        for c in node.children:
            _conv(c, out, depth)
        return
    if n == "br":
        out.append("\n")
        return
    if n in ("strong", "b"):
        out.append("**")
        for c in node.children:
            _conv(c, out, depth)
        out.append("**")
        return
    if n in ("em", "i"):
        out.append("_")
        for c in node.children:
            _conv(c, out, depth)
        out.append("_")
        return
    if n == "code" and node.parent and node.parent.name != "pre":
        out.append("`" + node.get_text() + "`")
        return
    if n == "pre":
        out.append("\n\n```\n" + node.get_text().strip("\n") + "\n```\n")
        return
    if n in ("ul", "ol"):
        out.append("\n")
        items = [c for c in node.children if isinstance(c, Tag) and c.name == "li"]
        for i, li in enumerate(items):
            out.append("\n" + "  " * depth + ("- " if n == "ul" else f"{i + 1}. "))
            for c in li.children:
                _conv(c, out, depth + 1)
        out.append("\n")
        return
    if n == "li":
        for c in node.children:
            _conv(c, out, depth)
        return
    if n == "table":
        out.append("\n")
        for tr in node.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            out.append("| " + " | ".join(cells) + " |\n")
        out.append("\n")
        return
    for c in node.children:
        _conv(c, out, depth)


def leccion_a_markdown(path):
    """(titulo, markdown) de una página de lección de Skilljar."""
    from bs4 import BeautifulSoup
    from bs4.element import NavigableString

    soup = BeautifulSoup(open(path, encoding="utf8").read(), "html.parser")
    top = soup.find("div", class_="lesson-top")
    titulo = top.get_text(strip=True) if top else ""
    main = soup.find(id="lesson-main-content")
    if main is None:
        return titulo, ""
    for a in main.find_all("a"):
        href, txt = str(a.get("href") or ""), a.get_text(strip=True)
        if href.startswith("http") and txt:
            a.replace_with(NavigableString(f"[{txt}]({href})"))
    out = []
    _conv(main, out)
    txt = html.unescape("".join(out))
    txt = re.sub(r"[ \t]+\n", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return titulo, txt.strip()


# ─────────────────────────── main ───────────────────────────
def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1].strip("/")
    outdir = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{slug}"
    os.makedirs(outdir, exist_ok=True)

    cookie = cookies_skilljar(outdir)
    idx = get(f"{BASE}/{slug}", cookie, os.path.join(outdir, "curso.html"))
    if "juanma" not in idx and "sign-out" not in idx.lower():
        print("AVISO: la página no parece autenticada; puede faltar contenido.",
              file=sys.stderr)

    # el orden de aparición en el HTML es el orden del currículo
    ids, vistos = [], set()
    for m in re.finditer(rf'href="/{re.escape(slug)}/(\d+)"', idx):
        if m.group(1) not in vistos:
            vistos.add(m.group(1))
            ids.append(m.group(1))
    if not ids:
        sys.exit("No se encontraron lecciones. ¿Estás matriculado en el curso?")
    print(f"{len(ids)} lecciones: {', '.join(ids)}")

    lineas = []
    for i, lid in enumerate(ids):
        lp = os.path.join(outdir, f"L{lid}.html")
        get(f"{BASE}/{slug}/{lid}", cookie, lp)
        titulo, md = leccion_a_markdown(lp)
        with open(os.path.join(outdir, f"raw_{lid}.md"), "w", encoding="utf8") as f:
            f.write(f"# {titulo}\n\n{md}")
        lineas.append(f"{lid} | {titulo} | {len(md)} chars")
        print(f"  {lineas[-1]}")
        if i < len(ids) - 1:
            time.sleep(1)  # cortesía con el servidor

    with open(os.path.join(outdir, "indice.txt"), "w", encoding="utf8") as f:
        f.write("\n".join(lineas) + "\n")

    # las cookies no se quedan en disco
    os.remove(os.path.join(outdir, "Cookies"))
    print(f"\nListo en {outdir}/ — lee los raw_*.md y escribe los resúmenes.")
    print("Si algún raw_*.md sale casi vacío, esa lección se renderiza por JS "
          "(p. ej. un quiz): míralo aparte.")


if __name__ == "__main__":
    main()
