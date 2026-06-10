#!/usr/bin/env python3
"""Normalize filenames in given folders to URL-safe slugs and update text references.

Usage:
  python scripts/slugify_and_update_refs.py public/videos public/docs

This script will attempt to `git mv` each file to a slugified filename,
then scan common text files (.html, .js, .md, .css, .txt) and replace
occurrences of the old filename (and its URL-encoded form) with the new one.
It stages the changes but does not commit them — commit/push is performed after.
"""

import sys
import os
import re
import unicodedata
import subprocess
import urllib.parse

TEXT_EXTS = ('.html', '.htm', '.js', '.css', '.md', '.txt')

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    # keep dots (for extensions) out of base transformation
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def git_mv(src, dst):
    try:
        subprocess.run(['git', 'mv', src, dst], check=True)
        return True
    except Exception:
        try:
            os.replace(src, dst)
            return True
        except Exception as e:
            print(f"ERROR moving {src} -> {dst}: {e}")
            return False

def main(args):
    if len(args) < 1:
        print('usage: slugify_and_update_refs.py <dir1> [dir2 ...]')
        return 1

    repo_root = os.getcwd()
    mapping = {}  # old_basename -> new_basename

    # Step 1: rename files
    for d in args:
        dpath = os.path.join(repo_root, d)
        if not os.path.isdir(dpath):
            print(f"Skipping missing folder: {dpath}")
            continue
        for name in os.listdir(dpath):
            old_full = os.path.join(dpath, name)
            if os.path.isdir(old_full):
                continue
            base, ext = os.path.splitext(name)
            new_base = slugify(base)
            if not new_base:
                continue
            new_name = new_base + ext.lower()
            if new_name == name:
                continue
            dst_full = os.path.join(dpath, new_name)
            # avoid collisions
            i = 1
            candidate = dst_full
            while os.path.exists(candidate):
                candidate = os.path.join(dpath, f"{new_base}-{i}{ext.lower()}")
                i += 1
            dst_full = candidate
            moved = git_mv(old_full, dst_full)
            if moved:
                mapping[name] = os.path.basename(dst_full)
                print(f"MOVED: {old_full} -> {dst_full}")

    if not mapping:
        print('No files renamed.')

    # Step 2: update references in repository text files
    updated_files = []
    for root, dirs, files in os.walk(repo_root):
        if '.git' in root.split(os.sep) or 'public/uploads' in root:
            continue
        for f in files:
            if not f.lower().endswith(TEXT_EXTS):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    txt = fh.read()
            except Exception:
                continue
            newtxt = txt
            for old, new in mapping.items():
                # raw occurrences
                newtxt = newtxt.replace(old, new)
                # URL-encoded occurrences
                newtxt = newtxt.replace(urllib.parse.quote(old, safe=''), urllib.parse.quote(new, safe=''))
                newtxt = newtxt.replace(urllib.parse.quote_plus(old, safe=''), urllib.parse.quote_plus(new, safe=''))
            if newtxt != txt:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(newtxt)
                updated_files.append(path)
                print(f"UPDATED: {path}")

    # Stage changes
    if mapping or updated_files:
        subprocess.run(['git', 'add', '-A'])
        print('\nStaged renamed files and updated references.')
        print('Renamed mapping:')
        for old, new in mapping.items():
            print(f'  {old} -> {new}')
        return 0
    else:
        print('No changes to stage.')
        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
