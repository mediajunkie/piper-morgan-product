#!/usr/bin/env bash
# ensure-ruff.sh — print the path to a ruff pinned to CI's version, creating it once per host.
#
# Why (2026-10-01, CIO, on Docs's datum): four format-only reds on main in one day. The advisory
# check could not find a binary. Only 1 of 13 Amber worktrees had venv/bin/ruff, the main checkout
# had none, and there was no ruff on PATH. Per-seat "remember to format" promises don't hold.
#
# The pin is READ from requirements.txt (the same `ruff==X` CI installs via lint.yml), never
# hardcoded here. The env lives OUTSIDE the repo in a shared per-host cache, so every worktree
# reuses one install. First use costs one pip install (~10-20s); after that it's a stat.
# Prints the binary path on stdout and exits 0, or prints nothing and exits 1. Never fails loudly.
set -u
top="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 1
ver="$(grep -E '^ruff==' "$top/requirements.txt" 2>/dev/null | head -1 | cut -d= -f3)"
[ -n "$ver" ] || exit 1
base="${XDG_CACHE_HOME:-$HOME/.cache}/piper-morgan"
env="$base/ruff-$ver"
bin="$env/bin/ruff"
if [ -x "$bin" ]; then echo "$bin"; exit 0; fi
mkdir -p "$base" 2>/dev/null || exit 1
lock="$env.lock"
# mkdir is atomic: only one concurrent caller builds; others wait briefly, then use or give up.
if mkdir "$lock" 2>/dev/null; then
  echo "ensure-ruff: creating pinned ruff $ver at $env (one-time, per host)..." >&2
  { python3 -m venv "$env" && "$env/bin/pip" install -q "ruff==$ver"; } >/dev/null 2>&1
  rmdir "$lock" 2>/dev/null
else
  for _ in $(seq 1 30); do [ -x "$bin" ] && break; sleep 1; done
fi
[ -x "$bin" ] && { echo "$bin"; exit 0; }
exit 1
