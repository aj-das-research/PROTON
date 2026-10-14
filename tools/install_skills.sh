#!/usr/bin/env bash
# Install/update the PROJECT-LOCAL skills into PROTON/.claude/skills (this project only, not ~/.claude/skills).
# Sources (SSH, collaborator access needed for private ones):
#   spotai-mbzuai/spotai-research               paper review / reproduction workflow (steps 01-06, writing styles, figures)
#   Mishrakshitij/paper-figure-creation-skill   paper figure creation (house figure standard)
#   Mishrakshitij/AI-A-star-conference-paper-writing-skill   a-star paper writing (house style, section playbooks)
# Usage: tools/install_skills.sh
set -euo pipefail
P="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$P/.claude/skill-sources"; DST="$P/.claude/skills"
declare -A REPOS=(
  [spotai-research]="git@github.com:spotai-mbzuai/spotai-research.git"
  [paper-figure-creation-skill]="git@github.com:Mishrakshitij/paper-figure-creation-skill.git"
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
