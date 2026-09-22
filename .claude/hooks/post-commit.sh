#!/usr/bin/env bash
# post-commit.sh — git-native post-commit hook, common-dir install (see docs/internal/operations/
# amber-hooks-investigation-2026-07.md for how the common-dir/PreToolUse split works; this is the
# post-commit sibling of check-branch.sh's pre-commit).
#
# Runs TWO independent, advisory (never-block) checks after every commit, in every worktree that
# shares this common .git dir. Both are approved-in-design, GO'd for pilot 2026-09-21 (Pard):
#   1. Heartbeat auto-fire — closes the "forgot to call duty-cycle-heartbeat.sh" failure mode
#      (Web's finding, 2026-09-20: a busy role that commits all day but never runs Step 5b reads
#      BELT-INVISIBLE despite being alive). A commit already proves liveness; this just makes the
#      heartbeat surface record it without depending on the agent remembering the separate call.
#   2. Ruff advisory check — Lead's proposal, 2026-09-20 (no ruff pre-commit mechanism existed;
#      format drift was pure "everyone remembers"). Runs the pinned ruff (0.6.9, the CI pin) against
#      the files the commit actually touched, WARN-ONLY. Promotion to blocking is Lead's call, not
#      wired here.
#
# 🔴 PILOT GATE — READ BEFORE EDITING, READ BEFORE REMOVING. Both checks below run ONLY for the
# `cio` role during the single-seat pilot (Pard's GO, 2026-09-21: "the single-seat pilot on your own
# seat, a full day, tomorrow 09-22"). This file lives in the COMMON .git dir's hooks/, which every
# worktree shares by construction (same reason check-branch.sh's pre-commit protects every seat with
# one install) — so without this gate, installing it today would be a fleet-wide flip on day one,
# exactly what the pilot exists to avoid. Fleet rollout is a DELIBERATE follow-up: once the pilot
# holds (CIO's own telemetry read against Pard's independent belt/watchdog comparison), remove the
# `[ "$ROLE" = "cio" ]` guards below — nothing else in this file needs to change.
#
# Exit code is always 0 — a post-commit hook cannot block (the commit already happened), and both
# checks are advisory by design; a nonzero exit here would only make git print a spurious warning.

set -uo pipefail

# ── RE-ENTRY GUARD — CRITICAL, added 2026-09-22 after the fire-zero recursion incident ─────────
# (Pard's INCIDENT mail, 2026-09-21 23:2x, INCIDENT-pard-to-cio-...-2026-09-21.md). This hook calls
# duty-cycle-heartbeat.sh, which — on the suppressed path — itself runs `git commit` for the
# last-invoked marker. THAT commit also fires this same post-commit hook (git fires post-commit on
# every commit on the branch; it has no notion of "a commit this hook's own subprocess just made"
# vs. a real one). Unguarded, that is unbounded recursion: hook -> heartbeat -> commit -> hook ->
# heartbeat -> ... Real incident: ~2,882 nested processes, 967 marker commits pushed to
# origin/main before Pard disarmed the shim and killed the chain by hand. No code or data was
# touched — every one of those commits changed only the one-line marker file — but it was a real
# production incident on shared trunk history, not a close call to wave off.
#
# Guard: an exported env var, checked FIRST, before any other work. A recursive child inherits its
# parent's exported environment, so this is airtight against the actual failure mode (process-tree
# depth) rather than a heuristic on commit-message text, which the incident report also asked for
# as cheap defense-in-depth (see the marker-message check inside duty-cycle-heartbeat.sh's own
# --no-push path, added the same day) — belt and suspenders, per Pard's own framing.
if [ -n "${PIPER_IN_POST_COMMIT_HOOK:-}" ]; then
  exit 0
fi
export PIPER_IN_POST_COMMIT_HOOK=1

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
BRANCH="$(git branch --show-current 2>/dev/null)"

# Role inference: claude/{role}-cycle is this repo's Model-A branch convention (CLAUDE.md
# §"Worktree model"). Anything that doesn't match (main, a non-agent feature branch, detached HEAD)
# is not a duty-cycle seat — silently exit, nothing to do.
case "$BRANCH" in
  claude/*-cycle) ROLE="${BRANCH#claude/}"; ROLE="${ROLE%-cycle}" ;;
  *) exit 0 ;;
esac

# ── 1. Heartbeat auto-fire — PILOT: cio only ──────────────────────────────────────────────────
# ⚠️ RUNS SYNCHRONOUSLY, not backgrounded — found live during pilot-prep testing, 2026-09-21.
# A first draft backgrounded this call (`&` + `disown`) to avoid adding commit latency. Tested it
# directly rather than trusting the design: the marker on origin/main never updated after the
# backgrounded call "succeeded." Almost certainly the managed/sandboxed shell this hook's parent
# process (git commit, itself a child of the agent's own Bash tool call) runs inside tears down the
# process tree once the parent exits — a background+disown that would survive in a real persistent
# terminal does not survive here. Running synchronously trades a small latency cost (this script's
# --if-quiet path is a fast local check; the rare non-suppressed path costs a few seconds for
# fetch+commit+push) for actually completing — the same "don't strand it, verify it landed"
# discipline as everything else this hook exists to close.
if [ "$ROLE" = "cio" ]; then
  # --no-push (added 2026-09-22, second incident fix): a hook that pushes races every real push on
  # the belt, and was also what let the recursion's damage reach origin/main (967 commits) instead
  # of staying a local-only mess Pard could have cleaned with a reset. The marker commit still gets
  # made locally — the surface still becomes observable — but delivery to origin/main now rides the
  # agent's own next real push (which happens routinely per CLAUDE.md's "push to main routinely"
  # standing order), not a push initiated from inside a hook.
  "$REPO_ROOT/scripts/duty-cycle-heartbeat.sh" "$ROLE" WORK --if-quiet --no-push >/dev/null 2>&1
fi

# ── 2. Ruff advisory check — PILOT: cio only, same gate, same reasoning ──────────────────────────
if [ "$ROLE" = "cio" ]; then
  CHANGED_PY="$(git diff-tree --no-commit-id --name-only -r HEAD -- '*.py' 2>/dev/null)"
  if [ -n "$CHANGED_PY" ]; then
    RUFF_BIN="$REPO_ROOT/ruffenv2/bin/ruff"
    [ -x "$RUFF_BIN" ] || RUFF_BIN="ruff"   # fall back to PATH if the pinned venv isn't present
    if command -v "$RUFF_BIN" >/dev/null 2>&1 || [ -x "$RUFF_BIN" ]; then
      OUT="$(cd "$REPO_ROOT" && printf '%s\n' "$CHANGED_PY" | xargs -I{} "$RUFF_BIN" format --check {} 2>&1; \
             printf '%s\n' "$CHANGED_PY" | xargs -I{} "$RUFF_BIN" check {} 2>&1)"
      if [ -n "$OUT" ]; then
        echo "post-commit(ruff, advisory — not blocking): format/lint drift on $(printf '%s' "$CHANGED_PY" | wc -l | tr -d ' ') file(s) just committed:" >&2
        echo "$OUT" | sed 's/^/  /' >&2
      fi
    fi
  fi
fi

exit 0
