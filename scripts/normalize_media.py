#!/usr/bin/env python3
"""
Normalize media filenames (slugify) under public/videos and public/docs,
update references in HTML/JS/MD and other text files, and produce a report.

Run from repository root:
  py -3 scripts\normalize_media.py
or
  python scripts/normalize_media.py
"""
from __future__ import annotations
import os
import re
import sys
import unicodedata
import shutil
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent

def slugify(text: str) -> str:
    text = text.strip()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[\(\)\[\]{}]', ' ', text)
    text = re.sub(r"[^a-z0-9]+", '-', text)
    text = re.sub(r'-{2,}', '-', text)
    text = text.strip('-')
    return text or 'file'

def find_media(root: Path, exts: set[str]):
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            yield p

def main():
    videos_dir = REPO_ROOT / 'public' / 'videos'
    docs_dir = REPO_ROOT / 'public' / 'docs'
    mapping: dict[str, str] = {}

    # Ensure target dirs exist
    for d in (videos_dir, docs_dir):
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)

    # Rename media files under public/videos
    for media in find_media(videos_dir, {'.mp4', '.webm', '.ogg'}):
        rel = media.relative_to(REPO_ROOT)
        stem = media.stem
        ext = media.suffix.lower()
        new_stem = slugify(stem)
        new_name = f"{new_stem}{ext}"
        new_path = media.with_name(new_name)
        i = 1
        while new_path.exists() and new_path.resolve() != media.resolve():
            new_path = media.with_name(f"{new_stem}-{i}{ext}")
            i += 1
        if new_path.resolve() != media.resolve():
            media.rename(new_path)
            mapping[str(rel)] = str(new_path.relative_to(REPO_ROOT))

    # Rename PDFs in public/docs
    for media in find_media(docs_dir, {'.pdf'}):
        rel = media.relative_to(REPO_ROOT)
        stem = media.stem
        ext = media.suffix.lower()
        new_stem = slugify(stem)
        new_name = f"{new_stem}{ext}"
        new_path = media.with_name(new_name)
        i = 1
        while new_path.exists() and new_path.resolve() != media.resolve():
            new_path = media.with_name(f"{new_stem}-{i}{ext}")
            i += 1
        if new_path.resolve() != media.resolve():
            media.rename(new_path)
            mapping[str(rel)] = str(new_path.relative_to(REPO_ROOT))

    report_lines = []
    report_lines.append('Rename mapping:')
    for k, v in mapping.items():
        report_lines.append(f"{k} -> {v}")

    # Update references in repository text files
    text_exts = {'.html', '.htm', '.js', '.css', '.md', '.txt', '.json', '.svg'}
    updated_files = []
    for path in REPO_ROOT.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in text_exts:
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except Exception:
            try:
                content = path.read_text(encoding='latin-1')
            except Exception:
                continue

        original = content

        # Replace filename occurrences and URL-encoded variants
        for old_rel, new_rel in mapping.items():
            old_name = os.path.basename(old_rel)
            new_name = os.path.basename(new_rel)

            # raw replacement of filename
            content = content.replace(old_name, new_name)
            # URL encoded replacement
            content = content.replace(quote(old_name, safe=''), quote(new_name, safe=''))

            # if old path used nested Videos folder, normalize to /public/videos/
            content = content.replace('/videos/Videos ingecart web 2026/', '/public/videos/')
            content = content.replace('/videos/Videos%20ingecart%20web%202026/', '/public/videos/')

        # Normalize any remaining /videos/ or /docs/ references to public paths
        content = content.replace('/videos/', '/public/videos/')
        content = content.replace('/docs/', '/public/docs/')

        if content != original:
            path.write_text(content, encoding='utf-8')
            updated_files.append(str(path.relative_to(REPO_ROOT)))

    report_lines.append('')
    report_lines.append('Updated files:')
    report_lines.extend(updated_files)

    report_path = REPO_ROOT / 'scripts' / 'normalize-report.txt'
    report_path.write_text('\n'.join(report_lines), encoding='utf-8')

    print('Normalization complete.')
    print(f'Report written to: {report_path}')

if __name__ == '__main__':
    main()
