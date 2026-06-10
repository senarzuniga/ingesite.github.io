#!/usr/bin/env bash
# Consolidate media and PDFs into public/videos and public/docs
# Usage: bash scripts/consolidate_media.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST_VIDEOS="$REPO_ROOT/public/videos"
DEST_DOCS="$REPO_ROOT/public/docs"

mkdir -p "$DEST_VIDEOS" "$DEST_DOCS"

hash_cmd=""
if command -v sha256sum >/dev/null 2>&1; then
  hash_cmd="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  hash_cmd="shasum -a 256"
else
  echo "No sha256 tool found (sha256sum or shasum). Exiting." >&2
  exit 1
fi

SOURCES=(
  "$REPO_ROOT/videos"
  "$REPO_ROOT/videos/Videos ingecart web 2026"
  "$REPO_ROOT/public/videos"
  "$REPO_ROOT/public/videos/Videos ingecart web 2026"
  "$REPO_ROOT/brochure"
  "$REPO_ROOT"
  "$REPO_ROOT/docs"
  "$REPO_ROOT/public/docs"
)

declare -A HASHMAP
REPORT_FILE="$REPO_ROOT/scripts/consolidation-report.txt"
rm -f "$REPORT_FILE"

copy_unique() {
  local pattern="$1" dest="$2"
  for src in "${SOURCES[@]}"; do
    [ -d "$src" ] || continue
    while IFS= read -r -d $'\0' file; do
      h="$($hash_cmd "$file" | awk '{print $1}')"
      if [[ -n "${HASHMAP[$h]:-}" ]]; then
        echo "SKIP duplicate: $file -> already copied as ${HASHMAP[$h]}" >> "$REPORT_FILE"
        continue
      fi
      base=$(basename "$file")
      destpath="$dest/$base"
      i=1
      while [[ -e "$destpath" ]]; do
        existingh="$($hash_cmd "$destpath" | awk '{print $1}')"
        if [[ "$existingh" == "$h" ]]; then
          HASHMAP[$h]="$destpath"
          echo "SKIP already present: $file -> $destpath" >> "$REPORT_FILE"
          continue 2
        fi
        name="${base%.*}"
        ext=".${base##*.}"
        destpath="$dest/${name}-$i$ext"
        ((i++))
      done
      cp -f "$file" "$destpath"
      HASHMAP[$h]="$destpath"
      echo "COPIED: $file -> $destpath" >> "$REPORT_FILE"
    done < <(find "$src" -type f -iname "$pattern" -print0 2>/dev/null)
  done
}

copy_unique "*.mp4" "$DEST_VIDEOS"
copy_unique "*.pdf" "$DEST_DOCS"

echo "Consolidation finished. See $REPORT_FILE"
