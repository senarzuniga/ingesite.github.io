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
import unicodedata
import re
import html

SOURCE_DEFAULT = Path(r"C:\Users\Inaki Senar\OneDrive\INGECART\VIDEOS web")
REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_VIDEOS = REPO_ROOT / 'assets' / 'videos'
PUBLIC_VIDEOS = REPO_ROOT / 'public' / 'videos'
ALLOWED_EXT = {'.mp4', '.webm', '.ogg', '.mov', '.mkv'}
MEDIA_BASE_URL = 'https://media.githubusercontent.com/media/senarzuniga/ingesite.github.io/main/assets/videos'
SITE_BASE_URL = 'https://senarzuniga.github.io/ingesite.github.io'


def ensure_dirs():
    ASSETS_VIDEOS.mkdir(parents=True, exist_ok=True)
    PUBLIC_VIDEOS.mkdir(parents=True, exist_ok=True)


def build_video_catalog():
    videos = []
    seen = set()

    def slugify(value):
        s = str(value)
        s = unicodedata.normalize('NFKD', s)
        s = s.encode('ascii', 'ignore').decode('ascii')
        s = re.sub(r"[^\w\s-]", '', s).strip().lower()
        s = re.sub(r"[-\s]+", '-', s)
        return s[:120]

    for p in sorted(ASSETS_VIDEOS.iterdir()):
        if p.is_file() and p.suffix.lower() in ALLOWED_EXT:
            stat = p.stat()
            title = p.stem
            base_slug = slugify(title) or slugify(p.name)
            slug = base_slug
            i = 1
            while slug in seen:
                slug = f"{base_slug}-{i}"
                i += 1
            seen.add(slug)
            share_path = f'{SITE_BASE_URL}/public/videos/{slug}.html'
            media_url = f'{MEDIA_BASE_URL}/{urllib.parse.quote(p.name)}'
            videos.append({
                'filename': p.name,
                'title': title,
                'url': media_url,
                'share_url': share_path,
                'slug': slug,
                'size': stat.st_size,
                'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

    return videos


def write_video_catalog(videos):
    json_path = PUBLIC_VIDEOS / 'videos.json'
    try:
        with json_path.open('w', encoding='utf-8') as fh:
            json.dump(videos, fh, indent=2, ensure_ascii=False)
        print(f"Wrote {json_path}")
    except Exception as e:
        print(f"Failed to write videos.json: {e}")

    index_html = PUBLIC_VIDEOS / 'index.html'
    try:
        with index_html.open('w', encoding='utf-8') as fh:
            fh.write(generate_public_index(videos))
        print(f"Wrote {index_html}")
    except Exception as e:
        print(f"Failed to write index.html: {e}")

    for v in videos:
        write_video_page(v)


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
                except PermissionError as e:
                    print(f"Skipped removal of {existing}: {e}")
                except OSError as e:
                    if getattr(e, 'winerror', None) == 32:
                        print(f"Skipped removal of {existing}: file is in use")
                    else:
                        print(f"Failed to remove {existing}: {e}")
                except Exception as e:
                    print(f"Failed to remove {existing}: {e}")

    videos = build_video_catalog()
    write_video_catalog(videos)

    return videos


def write_video_page(video):
    # write an individual landing page for a single video (using placeholder template to avoid f-string brace conflicts)
    try:
        title_escaped = html.escape(video.get('title', video.get('filename', '')))
        safe_url = html.escape(video['url'], quote=True)
        share_basename = f"{video.get('slug', 'video')}.html"
        tpl = '''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>%%TITLE%%</title>
    <link rel="stylesheet" href="../../css/styles.css">
</head>
<body>
    <div class="site-shell" style="padding:1rem">
        <h1>%%TITLE%%</h1>
        <video controls preload="metadata" width="100%" style="max-height:70vh;">
            <source src="%%SAFE_URL%%" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <p style="color:var(--text-muted);">%%HUMAN_SIZE%% · %%MTIME%%</p>
        <p><a class="button button-primary" href="%%SAFE_URL%%" download>Descargar</a> <a class="button" href="index.html">Volver al listado</a></p>
        <p><button id="copy-share" class="button">🔗 Copiar enlace compartible</button></p>
    </div>

    <script>
        function copyText(t){ if(navigator.clipboard && navigator.clipboard.writeText){ return navigator.clipboard.writeText(t); } var ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); return Promise.resolve(); }
        document.getElementById('copy-share').addEventListener('click', function(){
            var label = prompt('Etiqueta para personalizar el enlace (opcional)');
            var target = new URL('%%SHARE_BASENAME%%', location.href);
            if(label){ target.searchParams.set('ref', label); }
            var url = target.toString();
            copyText(url).then(function(){ alert('Enlace copiado:\\n'+url); try{ fetch('/.netlify/functions/notify_event',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'share',file:'%%VIDEO_URL%%',timestamp:new Date().toISOString(),ref:label||''})}); }catch(e){} });
        });
        var vid = document.querySelector('video'); if(vid){ vid.addEventListener('play', function(){ try{ fetch('/.netlify/functions/notify_event',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'play',file:'%%VIDEO_URL%%',timestamp:new Date().toISOString()})}); }catch(e){} }); }
    </script>
</body>
</html>
'''
        page = tpl.replace('%%TITLE%%', title_escaped).replace('%%SAFE_URL%%', safe_url).replace('%%SHARE_BASENAME%%', share_basename).replace('%%VIDEO_URL%%', video['url']).replace('%%HUMAN_SIZE%%', human_size(video.get('size',0))).replace('%%MTIME%%', video.get('mtime',''))
        out = PUBLIC_VIDEOS / f"{video['slug']}.html"
        with out.open('w', encoding='utf-8') as fh:
            fh.write(page)
        print(f"Wrote per-video page {out}")
    except Exception as e:
        print(f"Failed to write per-video page for {video.get('filename')}: {e}")


def generate_public_index(videos):
    # build items with percent-encoded URLs to avoid spaces/non-ASCII issues
    items = []
    for v in videos:
        safe_url = html.escape(v['url'], quote=True)
        item_html = f"""
        <article class=\"card\">\n          <h2 class=\"card-title\">{v['title']}</h2>\n          <video controls preload=\"metadata\" width=\"100%\" poster=\"\">\n            <source src=\"{safe_url}\" type=\"video/mp4\">\n            Your browser does not support the video tag.\n          </video>\n          <p style=\"color:var(--text-muted);\">{human_size(v['size'])} · {v['mtime']}</p>\n          <a class=\"button button-primary\" href=\"{safe_url}\" download>Descargar</a>\n        </article>\n        """
        items.append(item_html)

        index_html = f"""
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Video library</title>
            <link rel="stylesheet" href="../../css/styles.css">
        </head>
        <body>
            <div class="site-shell">
                <h1>Video library</h1>
                <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px;">{''.join(items)}</div>
            </div>
        </body>
        </html>
        """
    return index_html


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
