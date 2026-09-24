#!/usr/bin/env bash
# Mastermind installer for macOS / Linux
# curl -fsSL https://raw.githubusercontent.com/alekseevdenis1995-ai/mastermind/main/install.sh | bash
set -euo pipefail

dest="$HOME/.claude/skills/mastermind"
here="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"

if [ -n "$here" ] && [ -f "$here/skills/mastermind/SKILL.md" ]; then
  src="$here/skills/mastermind"
else
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL https://github.com/alekseevdenis1995-ai/mastermind/archive/refs/heads/main.tar.gz | tar -xz -C "$tmp"
  src="$tmp/mastermind-main/skills/mastermind"
fi

rm -rf "$dest"
mkdir -p "$(dirname "$dest")"
cp -R "$src" "$dest"

printf '\n  \033[32mMastermind installed -> %s\033[0m\n  Open Claude Code in an empty project folder and type: /mastermind\n\n' "$dest"
