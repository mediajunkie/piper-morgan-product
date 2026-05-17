# CIO V1 Autonomous Duty Cycle — Design v0.4

**Author**: CIO (Piper Morgan, Code instance)
**Date**: 2026-05-17 (v0.4 absorbs Day-1 dry-run findings)
**Status**: Draft v0.4 — Day-1 lessons baked in; Phase 3 v2 mechanically validated; standing for Phase 4
**Predecessor**: `dev/active/cio-v1-duty-cycle-design-v0.3-2026-05-16.md`

---

## What changed from v0.3

Day 1 of dry-run produced substantive findings; v0.4 absorbs them. Three load-bearing changes:

1. **Wake mechanism: `/loop` in-session, not Routines.** v0.3 picked Routines (cloud-hosted, no laptop dependency). PM caught at setup time: Routines spawn a NEW session per fire (discontinuous), not "wake up THIS conversation." PM's original instinct was continuity. `/loop` + `CronCreate` is the right primitive — same session, scheduled wake-up via cron. Routines remains the path for V2 true-cloud-autonomy when continuity-feel no longer matters.

2. **Worktree-default applies at cycle level, not just substantive non-cycle work.** v0.3 said "worktree-default moot at cycle level (per-run fresh clone)" — that was Routines-driven. Under `/loop`, the cycle works in the same session that PM is in; same `.git/` is shared with concurrent agents on main. Morning incident (May 17 ~07:22) validated: cycle commits on shared main are collision-prone. Solution: cycle works in a dedicated worktree on a dedicated branch (`claude/cio-duty-cycle-{date}`), pushes to that branch only. No per-cycle commits to main.

3. **Lead Dev's "worktree-default-during-cycling" generalization** is a real methodology extension. Per Lead Dev's morning lesson #2: when an autonomous cycle is running, ANY commit on shared main has non-trivial collision risk; worktree-default extends to all agents during cycle-active windows. This is methodology-corpus material; routing to Docs.

---

## Frame: three horizons (unchanged)

1. **North Star** — PM trusts work moves forward at appropriate cadence without needing to check
2. **Next Horizon** — two-week proof-of-concept (V1)
3. **Mushy middle** — incremental from Gall's law

---

## North Star (unchanged from v0.3)

CIO operates autonomously on a rhythm, mail-driven, never silent, with decisions and questions visible to PM at a single glance.

---

## Next Horizon: V1 two-week proof-of-concept (refined per Day-1 findings)

### 1. Cadence primitive — `/loop` + cron, fixed-interval

`/loop` skill in this conversational session invokes `CronCreate` with a fixed interval. Cron fires re-enter the same session with the prompt. Same CIO continues across fires; state in working memory persists.

**Dry-run cadence**: 5 minutes (fast feedback for incremental phase validation).
**V1-live cadence**: 30 min or 60 min — PM call once Phase 4+ stabilize. The Routines floor (1 hour) no longer binds.

### 2. Authority model — extend existing conversational practice (unchanged)

Per PM May 16: existing pattern ("do everything unblocked, batch questions, use discretion"). V1 errs toward MORE escalation (HOST stance); calibrates down with observed PM-reaction feedback.

### 3. Escalation surface — `dev/active/duty-cycle-escalations-cio.md` (unchanged)

Live since 2026-05-16. Structured-markdown enumerated entries per CXO Framing 2; active-cohort-threads section per PPM contribution. **Note**: file lives on main; written by conversational session, not cycle. V1 design defers cycle-writing-to-escalations-file to Phase 6+ (needs branch-vs-main resolution).

### 4. Day-N reconciliation — structured-markdown digest (unchanged)

Once-a-day digest in session log at ~10pm Pacific per CXO Framing 1 + PPM Ship-publish-day awareness + exec commit-message summary.

### 5. Cycle git mechanics — worktree-isolated; commits to branch (REVISED)

**Dedicated worktree** at `/Users/xian/Development/piper-morgan/piper-morgan-product-cio-cycle/` on branch `claude/cio-duty-cycle-{YYYY-MM-DD}`. Created with `git worktree add` based on current main HEAD.

**Cycle log file** at `dev/2026/MM/DD/cycle-log-cio-YYYY-MM-DD.md` lives ONLY on the cycle branch. Separate from conversational session log to avoid path-fragmentation (Pattern-068 P-17). Branch merges to main at PM cadence (Day-N digest fold, merge-keeper sweep, or explicit action).

**Cycle prompt steps** (validated across 7 Phase 3 v2 fires May 17):
- cd to cycle worktree
- Verify branch identity; ABORT if wrong
- `git fetch origin -q && git pull --rebase origin main` (brings branch current with main)
- Do cycle work (read inbox, append cycle log entry, etc.)
- `git reset HEAD` (clear any foreign-stage from concurrent agents)
- Explicit-path stage; verify staging exact-1-file; ABORT on mismatch
- Commit; post-commit `git show --stat HEAD` must show exact-1-file; ABORT on mismatch
- Push to branch (NOT main); retry once via pull-rebase-branch on rejection

**Known structural cost**: every fire's first push rejects (because step 3 rebase-onto-main diverged branch history from origin/branch tip). Retry path handles cleanly. ~2× rebase cost per fire. **Known v3 fix-target**: drop step 3 OR sync main on a separate cadence (e.g., end-of-day fold-to-main).

### 6. Conversational session writes to main (unchanged)

This conversational session does PM-direct work (memos, methodology, tracker) and commits to main. Cycle's branch-only commits don't collide with conversational main commits. Two clean surfaces:
- **Cycle on branch**: continuous; methodology-isolated; no main writes
- **Conversational on main**: when PM is here; full main authority

---

## Observable signals during V1 run

**V1 working signals**:
- Cycle keeps running (validated: 7 clean fires May 17)
- Escalation file stays current
- PM trust property holds
- Day-N digest reads usefully

**V2 design-input signals** (added per Day-1 findings):
- **First-push-rejection structural cost** — every fire requires retry; known; v3 target
- **Branch divergence from main** — accumulating cycle commits diverge from main over time; merge-cadence question worth designing
- **Cross-cohort collision rate on main** — validated as real (Lead Dev morning incident); worktree-default-during-cycling is the remediation
- **Manifest-vs-directory polling** — autonomous loops should poll directory (`ls inbox/`), not MANIFEST; per Pattern-073 4th instance methodology disposition

---

## Mushy middle (Horizon 3 — refined)

- **Dynamic cadence**: backoff-when-quiet first; day-part awareness; learned monitor-pattern
- **Static HTML dashboard**: aggregator reads `dev/active/duty-cycle-day-N-*.md` + `duty-cycle-escalations-*.md` cross-agent; render single-page HTML
- **Review-after channel**
- **Routing-suggestions sidecar**
- **Cross-agent extension** (Janus → Dispatch-Kind → broader fleet)
- **UI integration**
- **Day-N digest refinement**
- **Token-efficiency optimization** (deferred per PM "doesn't matter for learning")
- **Role-health methodology dimensions** for cycle-running agents
- **Duty-cycle-discipline skill**
- **NEW**: **Cycle-prompt v3** — drop step-3 rebase-onto-main; separate main-sync cadence (end-of-day fold)
- **NEW**: **Routines as V2 true-autonomous path** — when continuity-feel no longer required (e.g., cycle works fine 24×/day without PM intervention), switch to Routines for cloud-hosted no-laptop-dependency operation
- **NEW**: **Cycle mailbox-mutation surface** — Phase 6+ work; needs branch-vs-main reconciliation for inbox triage operations

---

## Phase progression (revised)

Phase status as of 2026-05-17 ~08:20 PT:

- ✅ **Phase 1**: Wake-up fires + session resumes — proven (manual + first scheduled, May 17 06:56 / 07:00)
- ✅ **Phase 2**: Scheduled trigger fires — proven (May 17 07:00-07:10, three fires)
- ✅ **Phase 3 v1**: Commit + push (to main) — caused collision (Lead Dev sweep); pivoted to v2
- ✅ **Phase 3 v2**: Worktree-isolated commit + push (to branch) — proven (May 17 07:44 manual + 6 scheduled fires)
- 🔵 **Phase 4 (next)**: Detect-new-memo capability — narrow observation; cycle starts "seeing" specific inbox items
- 🟡 **Phase 5**: Read memo content + categorize (severity / disposition recommendation)
- 🟡 **Phase 6**: Cycle updates escalations file based on categorization (introduces main-write surface; needs careful design)
- 🟡 **Phase 7**: V1 live — full cycle work; inbox triage; tracker advances; methodology touches
- 🟡 **Routines pivot**: switch wake mechanism for cloud-hosted no-laptop-dependency operation (post-V1)

Each phase adds one capability; observation-only phases (4, 5) precede mutation phases (6, 7). Lean dry-run discipline preserved.

---

## What's NOT changed from v0.3

- Three-horizon framing
- North Star (PM trust property + bidirectionality + lagging-indicator caveat)
- Authority model (extend existing conversational practice)
- Escalation surface structure (CXO Framings)
- Day-N reconciliation shape
- Operating discipline (bias-toward-MORE-escalation)
- Mushy-middle items (extended, not replaced)

---

## Cross-references

- v0.3 design: `dev/active/cio-v1-duty-cycle-design-v0.3-2026-05-16.md`
- Day-1 dry-run session log: `dev/2026/05/17/2026-05-17-0700-cio-code-opus-log.md`
- Day-1 cycle log (on cycle branch): `dev/2026/05/17/cycle-log-cio-2026-05-17.md`
- Pattern-068 family (worktree collision + manifest-regen failures)
- Pattern-073 4th instance (manifest-vs-directory poll)
- Lead Dev's morning recovery memo (worktree-default-during-cycling lesson)
- CIO manifest-sync disposition memo May 17

---

*v0.4 — Day-1 lessons absorbed; Phase 3 v2 mechanically validated; standing for Phase 4. CIO Code instance, 2026-05-17 ~08:20 PT.*
