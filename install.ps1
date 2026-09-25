# Mastermind installer for Windows: installs into every agent harness found on this machine
# irm https://raw.githubusercontent.com/alekseevdenis1995-ai/mastermind/main/install.ps1 | iex
$ErrorActionPreference = 'Stop'

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

# harness home -> its global skills folder
$h = $HOME
$map = [ordered]@{
    "$h\.claude"          = "$h\.claude\skills"           # Claude Code
    "$h\.codex"           = "$h\.agents\skills"           # Codex CLI
    "$h\.cursor"          = "$h\.agents\skills"           # Cursor
    "$h\.gemini"          = "$h\.agents\skills"           # Gemini CLI
    "$h\.config\opencode" = "$h\.agents\skills"           # OpenCode
    "$h\.copilot"         = "$h\.agents\skills"           # GitHub Copilot
    "$h\.codeium"         = "$h\.agents\skills"           # Windsurf / Devin
    "$h\.config\agents"   = "$h\.config\agents\skills"    # Amp
    "$h\.config\goose"    = "$h\.config\goose\skills"     # Goose
    "$h\.kiro"            = "$h\.kiro\skills"             # Kiro
    "$h\.factory"         = "$h\.factory\skills"          # Factory Droid
    "$h\.cline"           = "$h\.cline\skills"            # Cline
    "$h\.kilo"            = "$h\.kilo\skills"             # Kilo Code
    "$h\.roo"             = "$h\.roo\skills"              # Roo Code
}
$targets = @($map.Keys | Where-Object { Test-Path $_ } | ForEach-Object { $map[$_] } | Select-Object -Unique)
if (-not $targets) { $targets = @("$h\.claude\skills", "$h\.agents\skills") }

foreach ($t in $targets) {
    $dest = Join-Path $t 'mastermind'
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    New-Item -ItemType Directory -Force $t | Out-Null
    Copy-Item $src $dest -Recurse
    Write-Host "  + $dest" -ForegroundColor Green
}
if ($tmp) { Remove-Item $tmp -Recurse -Force }

Write-Host ""
Write-Host "  Mastermind installed. Open your agent in an empty project folder and type: /mastermind"
Write-Host "  (or just say: 'I have a project idea, build me a team')"
Write-Host ""
