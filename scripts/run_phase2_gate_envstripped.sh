#!/bin/bash
# #1595 Phase 2.1 — one-shot wrapper: the canonical env-strip (CLAUDE.md
# "restarting the server" block) around the gate runner, so the LLM keys
# resolve via Keychain instead of Claude Code's empty inherited vars.
cd "$(dirname "$0")/.." || exit 1
exec env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
  -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
  /Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python \
  scripts/inversion_phase2_gate.py "$@"
