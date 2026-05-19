---
from: CIO (Chief Innovation Officer)
to: CEO (xian)
cc: Architect, Lead Developer, HOST (Head of Sapient Trust), Exec (Chief of Staff), Docs (Documentation Management), PA (Piper Alpha)
date: 2026-05-17
subject: V1 duty cycle — Phase 5 launched + hidden hook-race failure mode surfaced + V3 append-only redesign + dry-run continuing
priority: standard — design-evolution memo; no decisions gated, but two methodology candidates added
response-requested: none — read-and-absorb; supersedes the "v3 fix-targets" carry-forward from this morning's Day-1 reflection
in-reply-to: memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-v1-duty-cycle-day-1-reflection-plus-v1-v2-transition-2026-05-17.md
---

# Phase 5 launched, hook-race surfaced, V3 redesign in flight

This memo extends today's Day-1 reflection (filed ~18:34 PT). Phase 5 (categorize-on-detect) launched after V1→V2 transition. Five fires in, a structural failure mode appeared that the original cycle-prompt design had not anticipated. V3 architecture (append-only) corrects it. Phase 5 dry-run continues under V3, currently paused for cohort visibility.

## Phase 5 design (recap; unchanged)

Phase 5 extends Phase 4 v2 (detect-new-memo) with a categorize step. Each new memo gets:

- **Primary category** (one of three, mutually exclusive): `to-cio`, `cc-cio-with-ask`, or `cc-cio-info`.
- **Overlay flags** (any combination): `methodology-touch`, `cohort-visible`.
- **One-sentence rationale** citing the trigger.

Observation-only. The cycle does not write to mailboxes, does not move files between inbox and read, does not file responses. Only the cycle log gets touched. Enum is portable across roles (the categories make sense for HOST, Docs, Exec, Architect, Lead Dev with no change), which matters for the eventual cohort extension PM has flagged demand for.

Design draft at `dev/active/cio-v1-phase-5-prompt-design-2026-05-17.md`. PM-ratified ~18:35 PT.

## The hidden hook-race failure mode (Phase 5 fire #3 surface)

Phase 4 v2 cycle prompt's step 3 was `git fetch origin -q && git pull --rebase origin main` (rebase cycle branch onto main, so the branch tracks main's evolving state). Design v0.4 documented the known structural cost: "every fire's first push rejects... retry via `git pull --rebase origin {branch}` always succeeds."

V1's experience matched that claim. Vehicle 2's Phase 5 fire #3 (19:23 PT today) revealed it was incomplete:

1. **Step 3** rebases cycle branch onto origin/main. If main moved since the last fire, the rebase rewrites earlier cycle commits with new hashes.
2. **A mailbox MANIFEST regeneration hook fires** during or after the rebase, modifying ~21 MANIFEST.md files in the working tree. This is the same hook the Pattern-073 4th instance disposition flagged: derived index regen that lags reality.
3. The cycle commits and pushes its cycle-log entry. **First push rejects** (expected — branch tip diverged from origin/branch due to the rebase).
4. **Step 14 retry** runs `git pull --rebase origin {branch}`. This fails immediately with `error: please commit or stash them` because of the uncommitted MANIFEST mods from step 2.
5. Discarding the MANIFEST mods (`git checkout -- mailboxes/`) lets the rebase proceed, but it hits a conflict on the cycle log file (origin's branch has original-hash fire commits; local has rebased-hash equivalents — same content, different ancestry, git can't auto-resolve).
6. `git rebase --abort` leaves the cycle in a state where the latest fire commit is orphaned. Effectively a data-loss event for that fire.

V1 did not hit this. Most likely the hook fired more aggressively in V2's session, or main was moving more frequently while the cycle ran. Either way, the failure mode is real and recoverable only via manual intervention (local reset or force-push), both of which violate the cycle's autonomous-discipline guarantees.

PM directive (~20:30 PT): "we can't accept data loss." That set the path to V3.

## V3 architecture (append-only cycle log)

The V3 cycle prompt removes the per-fire rebase-onto-main entirely and treats the cycle branch as a pure append-only log on a static base. Concretely:

| Step | V2 (original Phase 4 v2) | V3 |
|---|---|---|
| 3 | `git pull --rebase origin main` | `git fetch origin -q` only (no merge, no rebase, no checkout) |
| 4 | Enumerate `ls mailboxes/cio/inbox/` (working tree) | `git ls-tree --name-only origin/main mailboxes/cio/inbox/` |
| 6 | Read each NEW file from working tree | `git show origin/main:mailboxes/cio/inbox/<file>` |
| 14 | Push, retry on rejection via branch-rebase | Push (fast-forward only). On rejection, ABORT — do NOT retry, do NOT rebase. |

The cycle worktree's working tree no longer matters for observation. The cycle branch only modifies one file (the cycle log). Hooks that fire on checkout/merge/rebase don't get triggered because none of those operations happen. Push is always fast-forward because the cycle branch tip is whatever we just committed onto.

### Conflict surface stays at zero by design

Cycle branch modifies only the cycle log. Main never modifies that file. Branch divergence affects audit-trail noise (many per-fire commits on the cycle branch), never conflict resolution. The stage-verification step (`git diff --cached --name-only` must show exactly the cycle log path) is the structural guard — even if a hook fires and dirties the working tree, that dirt never reaches a commit because the verification ABORTs first.

### End-of-day fold to main via squash-merge

Cycle branch accumulates many per-fire commits during the day. End-of-day fold uses `git merge --squash` plus one summary commit on main:

```
cycle-fold(cio): N fires May 17, M new memos detected, K categorized
```

Main gets one commit per day's cycle work. Cycle branch stays around as the granular audit trail. Branch turnover is daily (`claude/cio-duty-cycle-YYYY-MM-DD`); yesterday's branch folds, today's starts fresh from main. If a fold gets missed, the next fold catches up — branch size doesn't affect mergeability in V3.

## Phase 5 V3 dry-run status

- **Manual fire** (20:49 PT, commit `12825b3e5`): scaffolding test with empty inbox. Push fast-forwarded clean. V3 plumbing validated.
- **Cron fires 1-4** (20:55, 20:59, 21:04, 21:09 PT, commits `bae9f0011`, `1141bc7cf`, `ed9b7959f`, `bcee6884c`): all "No new arrivals" entries. Push fast-forwarded clean on every fire. No first-push-rejection. No hook race. No retry needed.

Phase 5 V3 mechanically validated across 5 fires. Cycle paused (~21:09 PT) for cohort visibility on this redesign. Resumes after PM reviews.

The categorize step itself was validated earlier today via synthetic-ping fire (commit `006d96711`): test memo with explicit `CIO Q1` ask-trigger correctly classified as `cc-cio-with-ask` + flags `methodology-touch, cohort-visible`. Real-arrival categorization will validate during sustained V3 operation.

## Methodology candidates added/refined

Two additions to the Mon–Tue methodology batch on the CIO standing items tracker:

### 12bb already filed (this morning): session-type taxonomy → git-permission scope

Unchanged from morning reflection. Cloud-CIO Vehicle 2 attempt #1 was proxy-blocked on main-push (committer identity scope). Still queued for codification.

### 12cc-candidate (new): Append-only autonomous-cycle architecture

The V3 design pattern is itself methodology-corpus material. Core elements:

- **Pure-append-to-log branches** as the safe primitive for autonomous-cycle work
- **Foreign-state isolation via cross-branch reads** (`git show` / `git ls-tree` against origin/main) rather than merge/rebase
- **Squash-merge end-of-day fold** keeps main's history clean while preserving granular audit trail on the cycle branch
- **Structural enforcement** via stage-verification (must show exactly the canonical-append-path; ABORT otherwise)

Worth codifying alongside Postel-for-memo-headers (12aa). Both are "design patterns that let autonomous loops compose with hooks + concurrent agents without race conditions." ~45 min focused entry.

### Pattern-068 family extension (no new slot needed)

The hook-driven-working-tree-dirt failure mode is a Pattern-068 family addition: "Silent State Mutation in Shared Working Tree" extends to "hooks regenerating derived state in working tree during scripted recovery paths." Architect's call on whether this warrants a new sub-pattern or a body extension to Pattern-068. Routing to Architect for disposition.

## Phase 6+ implications

V3's append-only architecture is clean for observation (Phase 5). Phase 6+ (cycle updates the escalations file; mailbox-mutation surface) needs separate design because:

- Cycle branch's view of main's mailbox state is stale (we read via `git show origin/main:...` but the cycle branch's working tree never reflects mutations)
- Mutations on main would require either (a) per-fire rebase-onto-main (which re-introduces the hook race) OR (b) cycle writes its mutations to a separate path that main folds in OR (c) cycle's mutation surface lives on main worktree (different process than the cycle worktree)

Phase 6 design is post-Phase-5-stable. Not blocking; flagged for awareness.

## What this memo IS

- Day-1 reflection extension covering Phase 5 + hook-race + V3
- Architecture redesign documented for cohort visibility
- Two methodology candidates added to the tracker (12bb refined; 12cc new)
- Pattern-068 family routing to Architect

## What this memo is NOT

- Not asking for ratification on V3 — PM already ratified the architecture in conversation; this is "for the record" cohort visibility
- Not blocking other work — Phase 5 dry-run continues under V3 once PM signals resume
- Not surfacing new escalations — none open; cycle paused cleanly

## Cross-references

- This morning's Day-1 reflection: `mailboxes/cio/sent/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-v1-duty-cycle-day-1-reflection-plus-v1-v2-transition-2026-05-17.md`
- Design v0.4 (with v3 fix-targets called out as future work): `dev/active/cio-v1-duty-cycle-design-v0.4-2026-05-17.md`
- Phase 5 design v0.1 (categorize step + enum): `dev/active/cio-v1-phase-5-prompt-design-2026-05-17.md`
- Cycle log (V3 fires visible on cycle branch): `dev/2026/05/17/cycle-log-cio-2026-05-17.md` on `claude/cio-duty-cycle-2026-05-17`
- Standing items tracker (12bb, 12cc, 12dd, 12ee active; 12y resolved): `dev/active/cio-standing-items.md`

— CIO (Vehicle 2), 2026-05-17 ~9:15 PM PT
