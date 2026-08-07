#!/usr/bin/env python3
"""Valida un curso-interactivo.html antes de darlo por bueno.

Uso:  python3 scripts/validar_html.py <curso>/curso-interactivo.html

Comprueba, en este orden:
  1. Anidamiento HTML — etiquetas sin cerrar o mal cerradas
  2. Sintaxis del JS embebido — via `node --check`
  3. Render real en Chrome headless — cuenta los elementos que genera el JS
     (si un widget devuelve 0, el JS reventó en tiempo de ejecución)
  4. Desbordamiento horizontal a 1360 / 900 / 700 px

Sale con código 1 si algo falla. Requiere: node, google-chrome, python3-bs4.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr"}
CHROME = next((p for p in ("/opt/google/chrome/chrome",
                           "/usr/bin/google-chrome",
                           "/usr/bin/chromium") if os.path.exists(p)), None)
# selector → nombre legible; 0 elementos = fallo
WIDGETS = [
    (".quiz-q", "preguntas del quiz"),
    (".opt", "opciones de respuesta"),
    ("#cardGrid .card", "flashcards"),
]


class _Nest(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila, self.err = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.pila.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        t = tag
        if t in VOID:
            return
        if not self.pila:
            self.err.append(f"cierre huérfano </{t}> en {self.getpos()}")
        elif self.pila[-1][0] != t:
            self.err.append(f"</{t}> en {self.getpos()} pero está abierto "
                            f"<{self.pila[-1][0]}> de {self.pila[-1][1]}")
            for i in range(len(self.pila) - 1, -1, -1):
                if self.pila[i][0] == t:
                    del self.pila[i:]
                    break
        else:
            self.pila.pop()


def chrome(args, url, tmp):
    assert CHROME
    return subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         f"--user-data-dir={tmp}/prof", "--virtual-time-budget=4000",
         *args, url],
        capture_output=True, text=True, timeout=120,
    )


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = os.path.abspath(sys.argv[1])
    src = open(path, encoding="utf8").read()
    fallos = []

    # 1 · anidamiento
    n = _Nest()
    n.feed(src)
    if n.err or n.pila:
        fallos.append("anidamiento HTML")
        for e in n.err[:6]:
            print("  ✗", e)
        for t, pos in n.pila[:6]:
            print(f"  ✗ <{t}> de {pos} nunca se cierra")
    else:
        print("✓ anidamiento HTML")

    with tempfile.TemporaryDirectory() as tmp:
        # 2 · sintaxis JS
        m = re.search(r"<script>\s*(.*?)</script>", src, re.S)
        if not m:
            fallos.append("no se encuentra el bloque <script>")
        else:
            js = os.path.join(tmp, "check.js")
            open(js, "w", encoding="utf8").write(m.group(1))
            r = subprocess.run(["node", "--check", js],
                               capture_output=True, text=True)
            if r.returncode:
                fallos.append("sintaxis JS")
                print("  ✗", r.stderr.strip().splitlines()[0])
            else:
                print("✓ sintaxis JS")

        if not CHROME:
            print("· Chrome no encontrado: se omiten render y desbordamiento")
            return sys.exit(1 if fallos else 0)

        url = "file://" + path

        # 3 · render real
        r = chrome(["--dump-dom"], url, tmp)
        try:
            from bs4 import BeautifulSoup
            dom = BeautifulSoup(r.stdout, "html.parser")
            vacios = []
            for sel, nombre in WIDGETS:
                c = len(dom.select(sel))
                print(f"{'✓' if c else '✗'} {nombre}: {c}")
                if not c:
                    vacios.append(nombre)
            if vacios:
                fallos.append("widgets sin renderizar: " + ", ".join(vacios))
        except ImportError:
            print("· bs4 no instalado: se omite el recuento de widgets")

        # 4 · desbordamiento horizontal
        sonda = """<script>addEventListener("load",()=>{setTimeout(()=>{
const W=document.documentElement.clientWidth,S=document.documentElement.scrollWidth,o=[];
document.querySelectorAll("*").forEach(e=>{const b=e.getBoundingClientRect();
 if(b.right>W+1&&e.closest("pre")===null)o.push(e.tagName+"."+(typeof e.className==="string"?e.className.split(" ")[0]:""));});
console.log("PROBE"+JSON.stringify({W:W,S:S,o:o.slice(0,6)}));},300);});</script></body>"""
        probe = os.path.join(tmp, "probe.html")
        open(probe, "w", encoding="utf8").write(src.replace("</body>", sonda))
        for w in (1360, 900, 700):
            r = chrome([f"--window-size={w},900", "--enable-logging=stderr",
                        "--dump-dom"], "file://" + probe, tmp)
            mm = re.search(r"PROBE(\{.*?\})", r.stderr)
            if not mm:
                print(f"· {w}px: sin lectura de la sonda")
                continue
            d = json.loads(mm.group(1))
            ok = d["S"] <= d["W"]
            print(f"{'✓' if ok else '✗'} {w}px: scrollWidth={d['S']} "
                  f"clientWidth={d['W']}" + ("" if ok else f" · {d['o']}"))
            if not ok:
                fallos.append(f"desbordamiento horizontal a {w}px")

    if fallos:
        print("\nFALLA: " + " · ".join(fallos))
        sys.exit(1)
    print("\nTodo correcto.")


if __name__ == "__main__":
    main()
