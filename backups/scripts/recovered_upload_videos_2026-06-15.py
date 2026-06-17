#!/usr/bin/env python3
"""
upload_videos.py

Copies video files from a local source folder into the site's `public/videos/`
directory and regenerates `public/videos/index.html` to include all videos found
in that directory. Designed to be run from the repository copy.

Usage examples:
  python scripts/upload_videos.py                # use default source path
  python scripts/upload_videos.py --source "C:\\path\\to\\videos" --force
  python scripts/upload_videos.py --target public/videos --force
"""

import argparse
import shutil
import re
import sys
from pathlib import Path
import html
import unicodedata

# Default source folder (from user's request)
DEFAULT_SOURCE = r"C:\Users\Inaki Senar\Documents\INGECART\MARKETING\ARTWORK\VIDEOS"

# Allowed video extensions (lowercase)
ALLOWED_EXTS = ['.mp4', '.webm', '.mov', '.mkv', '.ogv']

def list_videos_in_dir(d: Path):
    if not d.exists():
        return []
    return sorted([p.name for p in d.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTS])

def copy_videos(src: Path, dst: Path, force: bool = False):
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    def _slugify_filename(name: str) -> str:
        base = Path(name).stem
        ext = Path(name).suffix.lower()
        text = unicodedata.normalize('NFKD', base)
        text = text.encode('ascii', 'ignore').decode('ascii')
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = re.sub(r'-+', '-', text)
        text = text.strip('-')
        if not text:
            text = Path(name).stem
        return text + ext

    for p in sorted(src.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in ALLOWED_EXTS:
            continue
        slug_name = _slugify_filename(p.name)
        target = dst / slug_name
        if target.exists():
            if force:
                shutil.copy2(p, target)
                copied.append(target.name)
            else:
                print(f"Skipping existing file (slug exists): {slug_name}")
        else:
            shutil.copy2(p, target)
            copied.append(target.name)
    return copied

def prettify_title(filename: str) -> str:
    name = Path(filename).stem
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'\b(720p|1080p|hd)\b', '', name, flags=re.I)
    name = ' '.join(w.capitalize() for w in name.split()).strip()
    return name or filename

def mime_for_ext(ext: str) -> str:
    mapping = {
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska',
        '.ogv': 'video/ogg',
    }
    return mapping.get(ext.lower(), 'video/mp4')

def generate_card(fn: str) -> str:
    title = prettify_title(fn)
    ext = Path(fn).suffix
    mtype = mime_for_ext(ext)
    return f'''    <div class="card">
      <div class="video-wrap">
        <video controls preload="metadata" playsinline>
          <source src="{html.escape(fn)}" type="{mtype}" />
          Your browser does not support the video tag.
        </video>
      </div>
      <div class="card-body">
        <span class="card-tag">Uploaded</span>
        <h2 class="card-title">{html.escape(title)}</h2>
        <p class="card-desc">Uploaded automatically.</p>
        <div class="card-actions">
          <a class="btn btn-secondary" href="{html.escape(fn)}" download="{html.escape(fn)}">
            ↓ Download
          </a>
        </div>
      </div>
    </div>'''

def regenerate_index(index_path: Path, video_files):
    text = index_path.read_text(encoding='utf-8')
    # create backup if not present
    backup = index_path.with_name(index_path.name + '.bak')
    if not backup.exists():
        backup.write_bytes(index_path.read_bytes())
    # update badge count (use callable replacement to avoid ambiguous backreferences)
    def _replace_badge(m):
        return f"{m.group(1)}{len(video_files)} videos available{m.group(2)}"
    text = re.sub(r'(<span class="badge">)\s*\d+\s* videos available(</span>)', _replace_badge, text, count=1, flags=re.S)
    start_marker = '<div class="grid">'
    end_marker = '</div><!-- /.grid -->'
    if start_marker in text and end_marker in text:
        before, rest = text.split(start_marker, 1)
        _, after = rest.split(end_marker, 1)
        cards = '\n'.join(generate_card(fn) for fn in video_files)
        new_text = before + start_marker + '\n' + cards + '\n  ' + end_marker + after
        index_path.write_text(new_text, encoding='utf-8')
        print(f"Updated {index_path} with {len(video_files)} videos")
    else:
        print("Could not find grid markers in index.html — skipping update")

def main():
    parser = argparse.ArgumentParser(description='Copy videos into public/videos and regenerate index.html')
    parser.add_argument('--source', default=DEFAULT_SOURCE, help='Source folder with videos')
    parser.add_argument('--target', default=None, help='Target folder inside the repo (defaults to public/videos)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    target_dir = Path(args.target) if args.target else repo_root / 'public' / 'videos'
    source_dir = Path(args.source)

    if not source_dir.exists():
        print(f"Source folder does not exist: {source_dir}")
        sys.exit(2)

    print(f"Copying videos from {source_dir} -> {target_dir} (force={args.force})")
    copied = copy_videos(source_dir, target_dir, force=args.force)
    if copied:
        print('Copied files:')
        for f in copied:
            print(' -', f)
    else:
        print('No files were copied.')

    video_files = list_videos_in_dir(target_dir)
    index_html = target_dir / 'index.html'
    if index_html.exists():
        regenerate_index(index_html, video_files)
    else:
        print('index.html not found at', index_html)

if __name__ == '__main__':
    main()
