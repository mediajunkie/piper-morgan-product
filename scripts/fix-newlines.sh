#!/bin/bash
# Fix end-of-file newlines for the files you're about to commit.
# This helps prevent pre-commit hook failures.
#
# SCOPED TO GIT-CHANGED FILES (staged, unstaged-modified, untracked).
# Earlier this script ran `find .` across the WHOLE repo, so every agent who
# ran it before a commit rewrote hundreds of pristine archived files (session
# logs, cross-pollination briefs, etc.), then committed only their own explicit
# paths — leaving the rest as uncommitted trailing-newline drift on shared main.
# That drift accumulated across agents and recurred daily. Scoping to changed
# files keeps the original purpose (clean what you're committing) while never
# touching files you aren't.

set -e

echo "🔧 Fixing end-of-file newlines (changed files only)..."

# Union of: tracked changes vs HEAD (staged + unstaged) and untracked, non-ignored files.
{ git diff --name-only HEAD; git ls-files --others --exclude-standard; } \
  | sort -u \
  | while IFS= read -r file; do
      case "$file" in
        *.py|*.md|*.txt|*.yml|*.yaml|*.json) ;;
        *) continue ;;
      esac
      [ -f "$file" ] || continue   # skip deletions
      if [ -n "$(tail -c 1 "$file")" ]; then
        echo "  Fixing: $file"
        printf '\n' >> "$file"
      fi
    done

echo "✅ Done! Changed files should now pass pre-commit hooks on first try."
