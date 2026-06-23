#!/usr/bin/env bash
# Install Piper Morgan PM skills for Claude Code
# Usage: curl -sSL https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/main/scripts/install-skills.sh | bash

set -euo pipefail

REPO="mediajunkie/piper-morgan-product"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}/.claude/skills"
SKILLS_DIR="${HOME}/.claude/skills"

# PM-facing skills (alpha set — audited for external use)
SKILLS=(
  "piper-sprint-plan"
  "piper-stakeholder-update"
  "piper-draft-issue"
  "piper-draft-spec"
  "piper-synthesize-feedback"
)

echo "Installing Piper Morgan PM skills..."
echo ""

mkdir -p "${SKILLS_DIR}"

installed=0
skipped=0

for skill in "${SKILLS[@]}"; do
  skill_dir="${SKILLS_DIR}/${skill}"
  skill_file="${skill_dir}/SKILL.md"
  url="${BASE_URL}/${skill}/SKILL.md"

  mkdir -p "${skill_dir}"

  if curl -sSfL "${url}" -o "${skill_file}" 2>/dev/null; then
    echo "  ✓ /${skill}"
    ((installed++))
  else
    echo "  ✗ /${skill} (fetch failed — skipped)"
    rm -rf "${skill_dir}"
    ((skipped++))
  fi
done

echo ""
echo "Done. ${installed} skills installed to ${SKILLS_DIR}/"

if [[ $skipped -gt 0 ]]; then
  echo "  (${skipped} skipped — check your connection or try again)"
fi

echo ""
echo "Restart Claude Code to pick them up as slash commands."
echo "Try: /piper-sprint-plan, /piper-draft-issue, /piper-synthesize-feedback"
echo ""
echo "Questions? https://github.com/${REPO}"
