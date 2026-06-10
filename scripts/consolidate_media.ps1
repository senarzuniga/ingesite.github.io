<#
Consolidate media and documents into public/videos and public/docs.

Usage (PowerShell):
  Open PowerShell in the repo root and run:
    .\scripts\consolidate_media.ps1

This script will COPY (not remove) files from common source folders into
`public/videos` and `public/docs`. Files are compared by SHA256 hash to
avoid duplicates. A report is written to `scripts/consolidation-report.txt`.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $repoRoot

Write-Host "Starting media consolidation..."

# Destination folders
$destVideos = Join-Path $repoRoot 'public\videos'
$destDocs   = Join-Path $repoRoot 'public\docs'

New-Item -ItemType Directory -Path $destVideos -Force | Out-Null
New-Item -ItemType Directory -Path $destDocs -Force | Out-Null

# Candidate source folders to scan (in order)
$sources = @( 
    (Join-Path $repoRoot 'videos'),
    (Join-Path $repoRoot 'videos\Videos ingecart web 2026'),
    (Join-Path $repoRoot 'public\videos'),
    (Join-Path $repoRoot 'public\videos\Videos ingecart web 2026'),
    (Join-Path $repoRoot 'brochure'),
    $repoRoot,
    (Join-Path $repoRoot 'docs'),
    (Join-Path $repoRoot 'public\docs')
)

$hashMap = @{}        # SHA256 -> destination filename
$report = [System.Collections.Generic.List[string]]::new()

function Copy-UniqueFiles {
    param(
        [string]$pattern,
        [string]$dest
    )

    foreach ($src in $sources) {
        if (-not (Test-Path $src)) { continue }
        Get-ChildItem -Path $src -File -Recurse -Include $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            $file = $_.FullName
            try {
                $h = (Get-FileHash -Algorithm SHA256 -Path $file).Hash
            } catch {
                Write-Warning "Failed hashing $file: $_"
                return
            }

            if ($hashMap.ContainsKey($h)) {
                $report.Add("SKIP duplicate: $file -> already copied as $($hashMap[$h])")
                return
            }

            $baseName = $_.Name
            $destPath = Join-Path $dest $baseName

            # If file exists but different content, add numeric suffix
            $i = 1
            while (Test-Path $destPath) {
                $existingHash = (Get-FileHash -Algorithm SHA256 -Path $destPath).Hash
                if ($existingHash -eq $h) {
                    # Already present identical file
                    $hashMap[$h] = $destPath
                    $report.Add("SKIP already present: $file -> $destPath")
                    return
                }
                $nameOnly = [System.IO.Path]::GetFileNameWithoutExtension($baseName)
                $ext = [System.IO.Path]::GetExtension($baseName)
                $destPath = Join-Path $dest ("{0}-{1}{2}" -f $nameOnly, $i, $ext)
                $i++
            }

            Copy-Item -Path $file -Destination $destPath -Force
            $hashMap[$h] = $destPath
            $report.Add("COPIED: $file -> $destPath")
        }
    }
}

# Copy video files
Copy-UniqueFiles -pattern '*.mp4' -dest $destVideos

# Copy PDF files
Copy-UniqueFiles -pattern '*.pdf' -dest $destDocs

$reportFile = Join-Path $repoRoot 'scripts' 'consolidation-report.txt'
$report | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "Consolidation finished. Report written to scripts/consolidation-report.txt"
Pop-Location
