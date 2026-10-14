#!/usr/bin/env bash
# Install/update PROJECT-LOCAL skills into PROTON/.claude/skills (this project only, not ~/.claude/skills).
# Usage: tools/install_skills.sh
set -euo pipefail
P="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$P/.claude/skill-sources"; DST="$P/.claude/skills"
declare -A REPOS=(
  [AI-A-star-conference-paper-writing-skill]="git@github.com:Mishrakshitij/AI-A-star-conference-paper-writing-skill.git"
)
mkdir -p "$SRC" "$DST"
for name in "${!REPOS[@]}"; do
  if [ -d "$SRC/$name/.git" ]; then git -C "$SRC/$name" pull --ff-only -q; else git clone -q "${REPOS[$name]}" "$SRC/$name"; fi
  for skill in "$SRC/$name"/skills/*/; do
    [ -f "$skill/SKILL.md" ] || continue
    s=$(basename "$skill")
    rm -rf "$DST/$s.new" && cp -R "$skill" "$DST/$s.new" && rm -rf "$DST/$s" && mv "$DST/$s.new" "$DST/$s"
    echo "installed $s -> $DST  ($name @ $(git -C "$SRC/$name" rev-parse --short HEAD))"
  done
done
