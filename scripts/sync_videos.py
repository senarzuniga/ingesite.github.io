#!/usr/bin/env python3
"""
Sync videos from a local OneDrive folder into the repository's assets and public folders.
Generates `public/videos/videos.json` and a simple `public/videos/index.html` gallery.
"""
import sys
from pathlib import Path
import shutil
import json
import subprocess
import datetime
import os
import urllib.parse

SOURCE_DEFAULT = Path(r"C:\Users\Inaki Senar\OneDrive\INGECART\VIDEOS web")
REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_VIDEOS = REPO_ROOT / 'assets' / 'videos'
PUBLIC_VIDEOS = REPO_ROOT / 'public' / 'videos'
ALLOWED_EXT = {'.mp4', '.webm', '.ogg', '.mov', '.mkv'}


def ensure_dirs():
    ASSETS_VIDEOS.mkdir(parents=True, exist_ok=True)
    PUBLIC_VIDEOS.mkdir(parents=True, exist_ok=True)


def list_source(src_dir: Path):
    if not src_dir.exists():
        return []
    files = [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXT]
    return sorted(files, key=lambda p: p.name)


def sync_from_source(src_dir: Path):
    print(f"Syncing from {src_dir}")
    ensure_dirs()
    src_files = list_source(src_dir)
    src_names = {p.name for p in src_files}

    # copy new and updated files
    for p in src_files:
        target_asset = ASSETS_VIDEOS / p.name
        target_public = PUBLIC_VIDEOS / p.name
        try:
            shutil.copy2(p, target_asset)
            shutil.copy2(p, target_public)
            print(f"Copied {p.name}")
        except Exception as e:
            print(f"Failed to copy {p}: {e}")

    # remove files in targets not present in source
    for folder in (ASSETS_VIDEOS, PUBLIC_VIDEOS):
        for existing in list(folder.iterdir()):
            if existing.is_file() and existing.name not in src_names:
                try:
                    existing.unlink()
                    print(f"Removed {existing}")
                except Exception as e:
                    print(f"Failed to remove {existing}: {e}")

    # build metadata
    videos = []
    for p in sorted((ASSETS_VIDEOS).iterdir()):
        if p.is_file() and p.suffix.lower() in ALLOWED_EXT:
            stat = p.stat()
            videos.append({
                'filename': p.name,
                'title': p.stem,
                'url': f'/assets/videos/{p.name}',
                'size': stat.st_size,
                'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

    # write JSON
    json_path = PUBLIC_VIDEOS / 'videos.json'
    try:
        with json_path.open('w', encoding='utf-8') as fh:
            json.dump(videos, fh, indent=2, ensure_ascii=False)
        print(f"Wrote {json_path}")
    except Exception as e:
        print(f"Failed to write videos.json: {e}")

    # write a simple index.html to public/videos for backwards compatibility
    index_html = PUBLIC_VIDEOS / 'index.html'
    try:
        with index_html.open('w', encoding='utf-8') as fh:
            fh.write(generate_public_index(videos))
        print(f"Wrote {index_html}")
    except Exception as e:
        print(f"Failed to write index.html: {e}")

    return videos


def generate_public_index(videos):
    # build items with percent-encoded URLs to avoid spaces/non-ASCII issues
    items = []
    for v in videos:
        safe_url = urllib.parse.quote(v['url'], safe='/')
        item_html = f"""
        <article class=\"card\">\n          <h2 class=\"card-title\">{v['title']}</h2>\n          <video controls preload=\"metadata\" width=\"100%\" poster=\"\">\n            <source src=\"{safe_url}\" type=\"video/mp4\">\n            Your browser does not support the video tag.\n          </video>\n          <p style=\"color:var(--text-muted);\">{human_size(v['size'])} · {v['mtime']}</p>\n          <a class=\"button button-primary\" href=\"{safe_url}\" download>Descargar</a>\n        </article>\n        """
        items.append(item_html)

    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset=\"utf-8\">\n      <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n+      <title>Video library</title>\n+      <link rel=\"stylesheet\" href=\"/css/styles.css\">\n+    </head>\n+    <body>\n+      <div class=\"site-shell\"> \n+        <h1>Video library</h1>\n+        <div style=\"display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px;\">{''.join(items)}</div>\n+      </div>\n+    </body>\n+    </html>\n+    """
    return html


def human_size(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


def git_commit_and_push(message='Sync videos from OneDrive'):
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

    videos = sync_from_source(src)
    # commit and push
    try:
        git_commit_and_push()
    except Exception:
        pass


if __name__ == '__main__':
    main()
