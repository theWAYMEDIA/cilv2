# cilv2.com

Sitio en español (es-MX) para las 41 casas del Condominio Ignacio L. Vallarta II, Puerto Vallarta.
No es un sitio oficial y los autores no son abogados.

## Versión de Hugo

**Hugo 0.123.7** (no se necesita la edición extended). La misma versión está fijada en
`.github/workflows/pages.yml` (`HUGO_VERSION`). Si se cambia una, cambiar la otra.

## Construir y revisar

```bash
hugo server        # ver el sitio en http://localhost:1313/
hugo --minify      # construir en public/
python3 scripts/check-links.py public   # falla si hay enlaces rotos, anclas faltantes o peticiones externas
```

## Lanzamiento (un solo paso)

Mientras `launched = false` en `hugo.toml`, todas las páginas llevan `noindex, nofollow`, `robots.txt`
dice `Disallow: /` y el sitemap está vacío. Cuando el abogado haya revisado el sitio, cambiar en
`hugo.toml`:

```toml
launched = true
```

y publicar. Eso quita el `noindex`, abre `robots.txt` y llena el sitemap.

## Contenido

- `content/`: textos terminados. No reescribir; los errores se reportan, no se corrigen.
- `static/pdf/`: escaneo oficial de la escritura en tres partes (A, B, C), enlazado desde `/escritura-24693/`.
- Las páginas `antecedentes`, `somos-distintos` y `nuestra-opinion` aparecen en el menú sólo cuando existen y no están en borrador.

## Dominio y DNS (GitHub Pages)

Dominio: `cilv2.com` (`static/CNAME`). En el proveedor del dominio, para el dominio raíz:

| Tipo | Nombre | Valor |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | `<usuario-de-github>.github.io` |

Después, en GitHub: Settings → Pages → Source: *GitHub Actions*, dominio personalizado `cilv2.com`,
y activar *Enforce HTTPS* cuando el certificado esté listo. No usar comodines (`*`) en el DNS.

## Privacidad

El sitio no publica dirección, teléfono ni correo, ni etiquetas de autor o generador, ni analítica.
Los commits usan el correo `noreply` de GitHub. Si el repositorio es público, el repositorio y su
historial son visibles para cualquiera.
