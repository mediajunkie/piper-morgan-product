#!/usr/bin/env bash
# last-real-commit.sh — print the most recent commit on HEAD that is NOT a heartbeat marker.
#
# Why (2026-10-04): with the post-commit heartbeat hook live (stage 2: cio, lead, cxo, docs), a marker
# commit (`hb(<role>): …` or `hb-last-invoked(<role>): …`) lands right after each real commit, so
# `git log -1` / `git rev-parse HEAD` returns the marker, not your work. Lead cited two marker shas
# as their real commits on 10-04. Use this whenever you quote "the commit I just made".
# Usage: scripts/last-real-commit.sh [--short]      (prints "<sha> <subject>")
fmt='%H %s'; [ "${1:-}" = "--short" ] && fmt='%h %s'
git log -1 --format="$fmt" --invert-grep -E --grep='^hb(-last-invoked)?\(' HEAD
