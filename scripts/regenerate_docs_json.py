#!/usr/bin/env python3
"""
Regenerate public/docs/docs.json and public/docs/index.html from files in assets/docs.
"""
import json
import datetime
from pathlib import Path
import urllib.parse

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DOCS = REPO_ROOT / 'assets' / 'docs'
PUBLIC_DOCS = REPO_ROOT / 'public' / 'docs'

PUBLIC_DOCS.mkdir(parents=True, exist_ok=True)


def html_escape(s):
    try:
        return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    except Exception:
        return s


def generate_public_index(docs):
    items = []
    for d in docs:
        safe_url = urllib.parse.quote(d['url'], safe='/')
        title = html_escape(d.get('title') or d.get('filename'))
        if d.get('ext', '').lower() in ('.pdf', '.ppt', '.pptx', '.doc', '.docx', '.xlsx', '.xls'):
            items.append(f"<li style=\"margin-bottom:10px;\"><strong>{title}</strong> — <a href=\"{safe_url}\" target=\"_blank\">Abrir</a> <a class=\"button\" href=\"{safe_url}\" download>Descargar</a></li>")
        else:
            items.append(f"<li style=\"margin-bottom:10px;\"><strong>{title}</strong> — <a href=\"{safe_url}\" target=\"_blank\">Abrir</a></li>")

    html_text = f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\"> 
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"> 
  <title>Documentación pública</title>
  <link rel=\"stylesheet\" href=\"/css/styles.css\"> 
</head>
<body>
  <div class=\"site-shell\" style=\"padding:1rem;\"> 
    <h1>Documentación pública</h1>
    <p>Materiales comerciales y técnicos disponibles para descarga.</p>
    <ul>
      {''.join(items)}
    </ul>
  </div>
</body>
</html>"""
    return html_text


# Build docs list from assets/docs
entries = []
for p in sorted(ASSETS_DOCS.iterdir()):
    if not p.is_file():
        continue
    if p.name in ('docs.json', 'index.html'):
        continue
    stat = p.stat()
    entries.append({
        'filename': p.name,
        'title': p.stem,
        'url': f'/public/docs/{p.name}',
        'size': stat.st_size,
        'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'ext': p.suffix.lower(),
    })

# Write JSON
json_path = PUBLIC_DOCS / 'docs.json'
with json_path.open('w', encoding='utf-8') as fh:
    json.dump(entries, fh, indent=2, ensure_ascii=False)
print(f'Wrote {json_path}')

# Write index.html
index_html = PUBLIC_DOCS / 'index.html'
with index_html.open('w', encoding='utf-8') as fh:
    fh.write(generate_public_index(entries))
print(f'Wrote {index_html}')
