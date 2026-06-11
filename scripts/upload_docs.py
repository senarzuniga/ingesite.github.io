#!/usr/bin/env python3
"""
upload_docs.py

Copies document files (PDF/HTML) from a local source folder into the site's
`public/docs/` directory and regenerates `public/docs/index.html` listing.

Usage examples:
  python scripts/upload_docs.py
  python scripts/upload_docs.py --source "C:\\path\\to\\docs" --force
"""

import argparse
import shutil
import re
import sys
from pathlib import Path
import html

# Default source requested by the user
DEFAULT_SOURCE = r"C:\Users\Inaki Senar\Documents\INGECART\MARKETING\ARTWORK\DOCUMENTOS COMERCIALES WEB"

ALLOWED_EXTS = ['.pdf', '.html', '.htm']

def list_docs_in_dir(d: Path):
    if not d.exists():
        return []
    return sorted([p.name for p in d.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTS])

def copy_docs(src: Path, dst: Path, force: bool = False):
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    for p in sorted(src.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in ALLOWED_EXTS:
            continue
        target = dst / p.name
        if target.exists():
            if force:
                shutil.copy2(p, target)
                copied.append(p.name)
            else:
                print(f"Skipping existing file: {p.name}")
        else:
            shutil.copy2(p, target)
            copied.append(p.name)
    return copied

def prettify_title(fn: str) -> str:
    name = Path(fn).stem
    name = re.sub(r'[_\-]+', ' ', name)
    name = ' '.join(w.capitalize() for w in name.split()).strip()
    return name or fn

def regenerate_index(index_path: Path, docs_files):
    text = index_path.read_text(encoding='utf-8')
    # backup
    backup = index_path.with_name(index_path.name + '.bak')
    if not backup.exists():
        backup.write_bytes(index_path.read_bytes())

    items = []
    for fn in docs_files:
        ext = Path(fn).suffix.lower()
        title = prettify_title(fn)
        if ext == '.pdf':
            item = f'<li><a href="{html.escape(fn)}" target="_blank">{html.escape(title)} (PDF)</a> — <a class="button" href="{html.escape(fn)}" download>Download</a></li>'
        else:
            item = f'<li><a href="{html.escape(fn)}">{html.escape(title)}</a></li>'
        items.append(item)

    new_ul = '<ul>\n  ' + '\n  '.join(items) + '\n</ul>'
    new_text, n = re.subn(r'<ul>[\s\S]*?<\/ul>', new_ul, text, count=1)
    if n:
        text = new_text
        # update iframe preview to first pdf (if any)
        pdfs = [f for f in docs_files if Path(f).suffix.lower() == '.pdf']
        if pdfs:
            # replace existing iframe src attribute (simple heuristic)
            text = re.sub(r'<iframe[^>]*src="[^"]*"[^>]*>', f'<iframe src="{html.escape(pdfs[0])}" width="100%" height="640" style="border:1px solid #ddd">', text, count=1)
        index_path.write_text(text, encoding='utf-8')
        print(f"Updated {index_path} with {len(docs_files)} documents")
    else:
        print("Could not find <ul> block in index.html — skipping update")

def main():
    parser = argparse.ArgumentParser(description='Copy docs into public/docs and regenerate index.html')
    parser.add_argument('--source', default=DEFAULT_SOURCE, help='Source folder with documents')
    parser.add_argument('--target', default=None, help='Target folder inside the repo (defaults to public/docs)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    target_dir = Path(args.target) if args.target else repo_root / 'public' / 'docs'
    source_dir = Path(args.source)

    if not source_dir.exists():
        print(f"Source folder does not exist: {source_dir}")
        sys.exit(2)

    print(f"Copying documents from {source_dir} -> {target_dir} (force={args.force})")
    copied = copy_docs(source_dir, target_dir, force=args.force)
    if copied:
        print('Copied files:')
        for f in copied:
            print(' -', f)
    else:
        print('No files were copied.')

    docs_files = list_docs_in_dir(target_dir)
    index_html = target_dir / 'index.html'
    if index_html.exists():
        regenerate_index(index_html, docs_files)
    else:
        print('index.html not found at', index_html)

if __name__ == '__main__':
    main()
