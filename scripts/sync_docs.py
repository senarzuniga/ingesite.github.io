#!/usr/bin/env python3
"""
Sync documents from a local OneDrive folder into the repository's assets and public folders.
Generates `public/docs/docs.json` and a simple `public/docs/index.html` listing.
"""
import sys
from pathlib import Path
import shutil
import json
import subprocess
import datetime
import os
import urllib.parse

SOURCE_DEFAULT = Path(r"C:\Users\Inaki Senar\OneDrive\INGECART\Documentos web")
REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DOCS = REPO_ROOT / 'assets' / 'docs'
PUBLIC_DOCS = REPO_ROOT / 'public' / 'docs'
ALLOWED_EXT = {'.pdf', '.pptx', '.ppt', '.docx', '.doc', '.xlsx', '.xls', '.zip', '.txt', '.md', '.html', '.htm'}

# Maximum file size to copy (bytes). Files with size >= this will be skipped
# to avoid Git hosting pre-receive hook failures (GitHub hard limit ~100 MB).
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


def ensure_dirs():
    ASSETS_DOCS.mkdir(parents=True, exist_ok=True)
    PUBLIC_DOCS.mkdir(parents=True, exist_ok=True)


def list_source(src_dir: Path):
    if not src_dir.exists():
        return []
    files = []
    for p in src_dir.iterdir():
        try:
            if not p.is_file():
                continue
            if p.suffix.lower() not in ALLOWED_EXT:
                continue
            size = p.stat().st_size
            if size >= MAX_FILE_SIZE:
                print(f"Skipping {p.name}: file too large ({size} bytes)")
                continue
            files.append(p)
        except Exception as e:
            print(f"Skipping {p}: could not stat file: {e}")
            continue
    return sorted(files, key=lambda p: p.name)


def sync_from_source(src_dir: Path):
    print(f"Syncing docs from {src_dir}")
    ensure_dirs()
    src_files = list_source(src_dir)
    src_names = {p.name for p in src_files}

    for p in src_files:
        target_asset = ASSETS_DOCS / p.name
        target_public = PUBLIC_DOCS / p.name
        try:
            shutil.copy2(p, target_asset)
            shutil.copy2(p, target_public)
            print(f"Copied {p.name}")
        except Exception as e:
            print(f"Failed to copy {p}: {e}")

    # remove files in targets not present in source
    for folder in (ASSETS_DOCS, PUBLIC_DOCS):
        for existing in list(folder.iterdir()):
            if existing.is_file() and existing.name not in src_names:
                try:
                    existing.unlink()
                    print(f"Removed {existing}")
                except Exception as e:
                    print(f"Failed to remove {existing}: {e}")

    docs = []
    for p in sorted(ASSETS_DOCS.iterdir()):
        if p.is_file() and p.suffix.lower() in ALLOWED_EXT:
            stat = p.stat()
            title = p.stem
            docs.append({
                'filename': p.name,
                'title': title,
                'url': f'/public/docs/{p.name}',
                'size': stat.st_size,
                'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'ext': p.suffix.lower(),
            })

    # write JSON
    json_path = PUBLIC_DOCS / 'docs.json'
    try:
        with json_path.open('w', encoding='utf-8') as fh:
            json.dump(docs, fh, indent=2, ensure_ascii=False)
        print(f"Wrote {json_path}")
    except Exception as e:
        print(f"Failed to write docs.json: {e}")

    # write a simple index.html
    index_html = PUBLIC_DOCS / 'index.html'
    try:
        with index_html.open('w', encoding='utf-8') as fh:
            fh.write(generate_public_index(docs))
        print(f"Wrote {index_html}")
    except Exception as e:
        print(f"Failed to write index.html: {e}")

    return docs


def generate_public_index(docs):
    items = []
    for d in docs:
        safe_url = urllib.parse.quote(d['url'], safe='/')
        title = html_escape(d.get('title') or d.get('filename'))
        items.append(f"<li style=\"margin-bottom:10px;\"><strong>{title}</strong> — <a href=\"{safe_url}\" target=\"_blank\">Abrir</a> <a class=\"button\" href=\"{safe_url}\" download>Descargar</a></li>")

    # Build a simple HTML page
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


def html_escape(s):
    try:
        return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    except Exception:
        return s


def human_size(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


def git_commit_and_push(message='Sync docs from OneDrive'):
    try:
        subprocess.run(['git', 'add', '-A'], check=False)
        subprocess.run(['git', 'commit', '-m', message], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=False)
        print('Git operations completed (add/commit/push).')
    except Exception as e:
        print('Git operation failed:', e)


def main():
    src = SOURCE_DEFAULT
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    if not src.exists():
        print(f"Source folder {src} does not exist.")
        sys.exit(1)

    docs = sync_from_source(src)
    try:
        git_commit_and_push()
    except Exception:
        pass


if __name__ == '__main__':
    main()
