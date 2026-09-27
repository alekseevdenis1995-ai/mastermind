"""Validate a generated Mastermind package.

Usage: python check_package.py <project_dir>
Exit 0 when there are no errors (warnings are allowed), 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors, warnings = [], []

REQUIRED = [
    "AGENTS.md", "TEAM_MANIFEST.md", "PROJECT_PLAN.md", "ARCHITECTURE.md",
    "team/RUNTIME.md", "team/00_MASTER_START.md",
    "memory/MASTER_START.md", "memory/MASTER_CONTEXT.md", "memory/SESSION_STATE.md",
    "memory/DECISIONS.md", "memory/OPEN_QUESTIONS.md", "memory/CHANGELOG.md",
    "memory/IDEAS.md", "memory/sessions.json",
]
for rel in REQUIRED:
    if not (root / rel).is_file():
        errors.append(f"missing {rel}")

for rel in ["memory/tasks", "memory/reports", "memory/adr"]:
    if not (root / rel).is_dir():
        warnings.append(f"missing folder {rel}/")


def read(rel):
    p = root / rel
    return p.read_text(encoding="utf-8") if p.is_file() else ""


mode = None
try:
    sessions = json.loads(read("memory/sessions.json") or "{}")
    mode = sessions.get("mode")
    if mode not in ("A", "B", "C"):
        errors.append('memory/sessions.json: "mode" must be A, B or C')
    if not isinstance(sessions.get("roles", {}), dict):
        errors.append('memory/sessions.json: "roles" must be an object')
except json.JSONDecodeError as e:
    errors.append(f"memory/sessions.json is not valid JSON: {e}")

runtime = read("team/RUNTIME.md")
for section in ("## Проверки", "## Лимиты"):
    if runtime and section not in runtime:
        errors.append(f"team/RUNTIME.md has no '{section}' section")

manifest = read("TEAM_MANIFEST.md")
starters = sorted((root / "team").glob("[0-9][0-9]_*_START.md"))
specialists = [p for p in starters if not p.name.startswith("00_")]
if not specialists:
    warnings.append("no specialist start files in team/ (MASTER-only team?)")
for p in specialists:
    role = p.stem[3:].removesuffix("_START")
    text = p.read_text(encoding="utf-8")
    if role not in manifest:
        errors.append(f"{p.name}: role {role} not in TEAM_MANIFEST.md")
    if "READY" not in text:
        errors.append(f"{p.name}: no READY / WAITING FOR TASK state")
    if "bootstrap-protocol" in text or "PROJECT_BOOTSTRAP" in text:
        errors.append(f"{p.name}: points at the bootstrap protocol (must be self-contained)")

if mode == "A":
    agent_dirs = [".claude/agents", ".codex/agents", ".cursor/agents", ".opencode/agents",
                  ".gemini/agents", ".github/agents", ".kilo/agents", ".factory/droids"]
    agents = [f for d in agent_dirs for f in (root / d).glob("*") if f.is_file()]
    for f in agents:
        for ref in re.findall(r"team/[\w./-]+_START\.md", f.read_text(encoding="utf-8")):
            if not (root / ref).is_file():
                errors.append(f"{f.relative_to(root).as_posix()}: points at missing {ref}")

placeholder = re.compile(r"<(Project|Project name|ROLE|NN|harness|model|path|N)>")
for p in [root / "AGENTS.md", *starters, root / "memory/MASTER_START.md", root / "team/RUNTIME.md"]:
    if p.is_file() and placeholder.search(p.read_text(encoding="utf-8")):
        errors.append(f"{p.relative_to(root).as_posix()}: unfilled template placeholder")

state_lines = read("memory/SESSION_STATE.md").count("\n")
if state_lines > 40:
    warnings.append(f"memory/SESSION_STATE.md has {state_lines} lines (limit 40)")

stems = {p.stem for p in root.rglob("*.md") if ".git" not in p.parts}
for p in (root / "memory").rglob("*.md") if (root / "memory").is_dir() else []:
    for link in re.findall(r"\[\[([^\]|#]+)", p.read_text(encoding="utf-8")):
        target = link.strip().split("/")[-1]
        if target and target not in stems and not re.fullmatch(r"[A-Z]+-\d+", target):
            warnings.append(f"{p.relative_to(root).as_posix()}: link [[{link}]] has no target")

for w in warnings:
    print(f"WARN  {w}")
for e in errors:
    print(f"ERROR {e}")
print(f"{'FAIL' if errors else 'OK'}: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
