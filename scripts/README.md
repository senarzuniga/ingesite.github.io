Consolidate media files
=======================

This folder contains small helper scripts to centralize videos and PDFs into `public/videos` and `public/docs`.

PowerShell (Windows):

  Open PowerShell in the repository root and run:

  ```powershell
  .\scripts\consolidate_media.ps1
  ```

Bash (Linux/macOS/WSL):

  ```bash
  bash scripts/consolidate_media.sh
  ```

Notes:
- Scripts COPY files into `public/videos` and `public/docs`. They do not delete originals.
- A report is written to `scripts/consolidation-report.txt` listing copied files and duplicates.
- After reviewing the report, you can remove duplicate folders manually or run additional cleanup commands.
