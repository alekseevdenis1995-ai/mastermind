#!/usr/bin/env bash
# Mastermind installer for macOS / Linux: installs into every agent harness found on this machine
# curl -fsSL https://raw.githubusercontent.com/alekseevdenis1995-ai/mastermind/main/install.sh | bash
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$here" ] && [ -f "$here/skills/mastermind/SKILL.md" ]; then
  src="$here/skills/mastermind"
else
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL https://github.com/alekseevdenis1995-ai/mastermind/archive/refs/heads/main.tar.gz | tar -xz -C "$tmp"
  src="$tmp/mastermind-main/skills/mastermind"
fi

h="$HOME"
# "harness home|its global skills folder"
map=(
  "$h/.claude|$h/.claude/skills"                  # Claude Code
  "$h/.codex|$h/.agents/skills"                   # Codex CLI
  "$h/.cursor|$h/.agents/skills"                  # Cursor
  "$h/.gemini|$h/.agents/skills"                  # Gemini CLI
  "$h/.config/opencode|$h/.agents/skills"         # OpenCode
  "$h/.copilot|$h/.agents/skills"                 # GitHub Copilot
  "$h/.codeium|$h/.agents/skills"                 # Windsurf / Devin
  "$h/.config/agents|$h/.config/agents/skills"    # Amp
  "$h/.config/goose|$h/.config/goose/skills"      # Goose
  "$h/.kiro|$h/.kiro/skills"                      # Kiro
  "$h/.factory|$h/.factory/skills"                # Factory Droid
  "$h/.cline|$h/.cline/skills"                    # Cline
  "$h/.kilo|$h/.kilo/skills"                      # Kilo Code
  "$h/.roo|$h/.roo/skills"                        # Roo Code
)

targets=()
for pair in "${map[@]}"; do
  home="${pair%%|*}"; dir="${pair#*|}"
  if [ -d "$home" ] && [[ ! " ${targets[*]:-} " == *" $dir "* ]]; then targets+=("$dir"); fi
done
[ ${#targets[@]} -eq 0 ] && targets=("$h/.claude/skills" "$h/.agents/skills")

for t in "${targets[@]}"; do
  rm -rf "$t/mastermind"
  mkdir -p "$t"
  cp -R "$src" "$t/mastermind"
  printf '  \033[32m+ %s\033[0m\n' "$t/mastermind"
done

printf '\n  Mastermind installed. Open your agent in an empty project folder and type: /mastermind\n  (or just say: "I have a project idea, build me a team")\n\n'
