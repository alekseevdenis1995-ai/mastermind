# Mastermind installer for Windows
# irm https://raw.githubusercontent.com/alekseevdenis1995-ai/mastermind/main/install.ps1 | iex
$ErrorActionPreference = 'Stop'

$dest = Join-Path $HOME '.claude\skills\mastermind'
$local = if ($PSScriptRoot) { Join-Path $PSScriptRoot 'skills\mastermind' }

if ($local -and (Test-Path $local)) {
    $src = $local
} else {
    $tmp = Join-Path ([IO.Path]::GetTempPath()) "mastermind-$([guid]::NewGuid())"
    New-Item -ItemType Directory -Force $tmp | Out-Null
    Invoke-WebRequest 'https://github.com/alekseevdenis1995-ai/mastermind/archive/refs/heads/main.zip' -OutFile "$tmp\repo.zip" -UseBasicParsing
    Expand-Archive "$tmp\repo.zip" $tmp
    $src = "$tmp\mastermind-main\skills\mastermind"
}

if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
Copy-Item $src $dest -Recurse
if ($tmp) { Remove-Item $tmp -Recurse -Force }

Write-Host ""
Write-Host "  Mastermind installed -> $dest" -ForegroundColor Green
Write-Host "  Open Claude Code in an empty project folder and type: /mastermind"
Write-Host ""
