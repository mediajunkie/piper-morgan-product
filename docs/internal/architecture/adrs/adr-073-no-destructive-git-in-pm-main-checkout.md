# ADR-073: No Destructive Git in PM's Main Checkout Working Tree

**Status**: ACCEPTED — PM-approved 2026-06-27. The operational rule has been in force via the CLAUDE.md ⚠️ HARD RULE callout since 2026-06-21 (`6d1292d09`); this ADR is the formal decision record + rationale for the archive.
**Date**: 2026-06-27
**Author**: CIO (Chief Innovation Officer)
**Deciders**: PM (xian) — flagged the incident, named the rule, approved formalizing as ADR; Comms — raised the incident + drafted the proposed rules; CIO — codified in CLAUDE.md + authored this ADR. Architect — cc (ADR-surface owner).
**Supersedes / superseded by**: none
**Related**: CLAUDE.md "HARD RULE (data-loss prevention)" callout (`6d1292d09`); `docs/internal/operations/branch-worktree-mailbox-discipline.md`; #1259 push-to-ref (mailbox writes never touch the shared checkout); methodology-41 (mechanism-displaces-unreferenced-discipline)

---

## Context

The main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) is **PM's live workspace**. PM edits prose there (blog drafts, docs) and **saves without committing in real time** — so at any moment the working tree may hold unstaged work that exists nowhere else.

Twice on 2026-06-21, a Comms duty-cycle commit ran **`git checkout -- .`** in the main checkout to clear MANIFEST noise before a rebase. The pattern: push a log entry → rebase fails ("unstaged changes") → `git checkout -- .` to clear → rebase succeeds → **PM's voice-pass edits silently gone, no recovery path.** `git checkout -- .` (and `reset --hard`, `stash`) discard unstaged working-tree changes irreversibly.

PM's principle, verbatim: *"You fix your mistakes directly and not with sweeping careless irreversible steps."* The working model: the main checkout is PM's; agents work in their own worktrees; the two must not collide.

This is a **methodology-41 case** — the discipline ("be careful in the main checkout") was failing as a per-agent reminder; it had to become a structural mechanism.

## Decision

Four hard rules for **all** agents (a standing constraint, not a per-agent reminder):

1. **Never** use `git checkout -- .` / `git checkout -- <broad-path>` / `git reset --hard` / `git stash`(/`-u`) / any command that discards working-tree changes **in the main checkout.** The main checkout working tree is PM's workspace, not an agent's scratch space.
2. **All agent commits go from the agent's own worktree** (`git push origin HEAD:main`), never from the main checkout.
3. **Clearing MANIFEST noise**: surgical **explicit paths only** (e.g. `git checkout -- mailboxes/{role}/inbox/MANIFEST.md`), never `git checkout -- mailboxes/` or broader.
4. **If a rebase/merge is blocked by unstaged changes in the main checkout: STOP.** Do not clear. Investigate what they are first; if they're PM's work, **leave them and find another path** (push from your worktree).

## Consequences

- **Enforcement is structural + layered** (m-41), not reminder-based:
  - (a) the CLAUDE.md ⚠️ HARD RULE callout **auto-loads every session** — highest-leverage placement (PM-confirmed higher-leverage than this ADR for day-to-day compliance);
  - (b) **#1259 push-to-ref** makes mailbox writes land on `origin/main` via `commit-tree`→push with **no working-tree operation on the shared checkout at all** — structurally removing the situation that triggered the incident;
  - (c) the `check-branch.sh` PreToolUse hook blocks interactive mailbox commits from non-main branches.
- **Cost**: agents may not use the main checkout as scratch — they must work in their own worktree. Minor friction; already the worktree-default norm.
- **Benefit**: PM's uncommitted prose is safe; the recurring data-loss class is closed at the mechanism level.
- **Boundary clarification (not a violation)**: a *non-destructive single-file `cp`* into the main checkout — e.g. deploying a launchd-run script (`scripts/duty-cycle-freeze-check.sh`) so the watcher picks it up — is **allowed**: it's a file copy of a non-PM-authored file, not a destructive git op, and it touches no prose. Verify the target file is clean (no uncommitted changes) before copying. The rule governs *destructive git*, not all main-checkout file access.

## Why an ADR (provenance)

The rule is already load-bearing via CLAUDE.md; this ADR adds the **formal decision record** — the incident, the principle, the deciders, and the structural-enforcement rationale — so the *why* survives in the architecture archive rather than only as an operational callout. (Comms + CIO both assessed CLAUDE.md as the compliance-load-bearing copy; PM approved capturing the provenance here.)
