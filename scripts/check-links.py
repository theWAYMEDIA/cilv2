#!/usr/bin/env python3
"""Revisa public/ despues de `hugo --minify`.

Falla (codigo 1) si hay:
  - un enlace interno roto o un ancla (#...) que no existe,
  - un ancla obligatoria del Reglamento/Clausulas que falta,
  - una peticion externa (script, css, imagen, iframe, fuente).
Los enlaces externos <a href> (por ejemplo wa.me) se permiten.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

PUBLIC = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
BASE = "https://cilv2.com"

# Paginas que existen en el contenido pero aun no estan publicadas (draft u omitidas).
# Se reportan como aviso, no como error.
KNOWN_UNPUBLISHED = {"/antecedentes/", "/somos-distintos/", "/nuestra-opinion/"}

REQUIRED = {
    "/escritura-24693/04-reglamento/": [f"articulo-{n}" for n in
        (5, 21, 23, 36, 38, 45, 46, 47, 49, 50, 51, 54, 58, 60, 61, 62, 63, 64, 104, 105, 106)]
        + ["capitulo-v", "capitulo-viii"],
    "/escritura-24693/02-clausulas/": ["bienes-comunes"],
}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.external = set(), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        for key in ("src", "srcset", "data"):
            if a.get(key, "").startswith(("http://", "https://", "//")):
                self.external.append(f"<{tag} {key}={a[key]}>")
        if tag == "link" and a.get("href", "").startswith(("http://", "https://", "//")):
            if a.get("rel") not in ("canonical",):
                self.external.append(f"<link href={a['href']}>")
        if tag in ("script", "iframe", "embed", "object"):
            self.external.append(f"<{tag}>")


def url_for(path: Path) -> str:
    rel = "/" + path.relative_to(PUBLIC).as_posix()
    return rel[: -len("index.html")] if rel.endswith("index.html") else rel


pages, files = {}, set()
for f in PUBLIC.rglob("*"):
    if f.is_file():
        files.add("/" + f.relative_to(PUBLIC).as_posix())
        if f.suffix == ".html" and f.name != "404.html":
            p = P()
            p.feed(f.read_text(encoding="utf-8"))
            pages[url_for(f)] = p

errors, warnings = [], []
for url, p in pages.items():
    for e in p.external:
        errors.append(f"{url}: peticion externa {e}")
    for href in p.links:
        if href.startswith(("mailto:", "tel:")):
            continue
        absu = urljoin(BASE + url, href)
        u = urlparse(absu)
        if u.netloc != "cilv2.com":
            continue  # enlace externo normal
        target, frag = urldefrag(u.path)
        if u.query:
            target = u.path
        if target in pages:
            if frag and frag not in pages[target].ids:
                errors.append(f"{url}: ancla inexistente {target}#{frag}")
        elif target in files:
            pass
        elif target in KNOWN_UNPUBLISHED:
            warnings.append(f"{url}: enlaza a {target} (pagina aun no publicada)")
        else:
            errors.append(f"{url}: enlace roto {href} -> {target}")

for page, ids in REQUIRED.items():
    if page not in pages:
        errors.append(f"falta la pagina {page}")
        continue
    for i in ids:
        if i not in pages[page].ids:
            errors.append(f"{page}: falta el ancla obligatoria #{i}")

for w in sorted(set(warnings)):
    print("AVISO:", w)
for e in errors:
    print("ERROR:", e)
print(f"{len(pages)} paginas revisadas, {len(errors)} errores, {len(set(warnings))} avisos.")
sys.exit(1 if errors else 0)
