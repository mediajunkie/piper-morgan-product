# Append-Only Autonomous-Cycle Architecture

## Overview

**Append-Only Autonomous-Cycle Architecture** names the design discipline for autonomous loops that share a working tree (and `.git/` metadata) with concurrent agents. The discipline eliminates a family of race conditions by structurally constraining the cycle's mutation surface to a single append-only file, and by reading external state via cross-branch git operations rather than working-tree access. Concretely:

1. The cycle operates on a dedicated branch (e.g., `claude/cio-duty-cycle-YYYY-MM-DD`) that has exactly one mutable file (the cycle log).
2. The cycle reads external state (e.g., inbox files on main) via `git ls-tree origin/main <path>` and `git show origin/main:<path>` — never via working-tree access. Foreign-state isolation by construction.
3. The cycle branch never rebases or merges main in. Push is always fast-forward from the cycle's own commits.
4. End-of-day fold to main happens once, via `git merge --squash`, producing one summary commit on main regardless of fire count.
5. Stage-verification at commit time (`git diff --cached --name-only` must show exactly the cycle log path; ABORT otherwise) is the structural guard that prevents foreign state from reaching commits even if hooks dirty the working tree.

The architecture is the cheapest known way to compose autonomous loops with mailbox-discipline hooks, concurrent agent activity, and shared `.git/` metadata without race conditions.

## Why This Methodology

### The hook-race failure mode (Phase 5 dry-run fire #3, May 17, 2026)

CIO's Phase 5 V2 cycle prompt followed the pattern V1 design v0.4 documented: per-fire `git pull --rebase origin main` to keep the cycle branch current; commit the cycle-log entry; push; retry once via branch-rebase on rejection.

V1's experience was that the retry always succeeded. V2's fire #3 (~19:23 PT May 17) surfaced a failure path V1 hadn't hit:

1. **Step 3 rebase-onto-main** rewrites prior cycle commit hashes (the branch's history is replayed onto a newer main tip).
2. **A mailbox MANIFEST-regen hook fires** during or after the rebase, modifying ~21 working-tree files. (Same hook the Pattern-073 4th instance disposition flagged: derived-index regen that lags reality.)
3. The cycle commits and pushes its cycle-log entry. **First push rejects** (expected — branch tip diverged from origin/branch due to the rebase).
4. **Step 14 retry** runs `git pull --rebase origin <branch>`. This fails immediately with `error: please commit or stash them` because of the uncommitted MANIFEST mods.
5. Discarding the MANIFEST mods lets the rebase proceed, but it hits a conflict on the cycle log file (origin's branch has original-hash fire commits; local has rebased-hash equivalents — same content, different ancestry, git can't auto-resolve).
6. `git rebase --abort` leaves the cycle in a state where the latest fire's commit is orphaned. The fire's data point is lost from the cycle log.

PM directive: "we can't accept data loss." Append-only architecture is the structural fix.

### The two-mode contrast

| Mode | Rebase-onto-main per fire | Append-only |
|---|---|---|
| Cycle branch's relationship to main | Continually re-rebased; branch history changes on every fire | Static base; cycle branch never re-bases |
| Working-tree access for external state | Yes — relies on rebase pulling main's state into working tree | No — uses `git ls-tree` + `git show` against origin/main ref |
| Push semantics | First push rejects every fire (structural cost); retry via branch-rebase | Always fast-forward; no first-push-rejection |
| Hook-firing surface | High (every rebase fires post-rebase hooks; merges fire post-merge hooks) | Minimal (only commit + push events) |
| Conflict surface at fold time | High (per-fire rebases compound divergence) | Zero (cycle branch only modifies the cycle log; main never modifies that file) |
| Recovery path on failure | Manual intervention (reset or force-push) | Structural ABORT; no recovery needed because failures don't compose |

## When to apply this framing

### Apply this framing when

- Designing any autonomous-loop work that runs in a session sharing `.git/` with concurrent agents (the common case for Code-instance roles).
- Hooks in the repo regenerate derived state in the working tree (MANIFESTs, INDEXes, generated docs) that the loop didn't author.
- The loop's mutation surface is narrow enough to constrain to a single append-only file (true for observation-only phases; trickier for mutation phases).
- The fold cadence is daily (or per-Ship, weekly) — a single squash-merge handles arbitrary divergence cheaply.

### This framing does not apply when

- The autonomous loop must mutate many files per fire (e.g., Phase 6+ in the CIO duty-cycle where the cycle updates the escalations file AND triages inbox AND writes outbound memos). For multi-file mutation surfaces, a different architecture is needed (see Phase 6+ pre-design open).
- The loop runs in true cloud isolation (Routines-style, no shared `.git/`) — the race conditions this architecture prevents don't exist there.
- The hook landscape is fully under the loop-author's control and proven not to dirty the working tree.

## What it predicts

If append-only architecture is genuine, the following downstream signals should appear:

- **First-push-rejection structural cost drops to zero** — no rebase-onto-main means no branch-tip divergence at push time. (Validated: 5 fires in Phase 5 V3 dry-run May 17, all fast-forward; 0 fires in May 17 V2 dry-run failed similarly.)
- **Hook-driven working-tree dirt becomes harmless** — even if a hook fires and modifies MANIFESTs, the stage-verification step ABORTs before any foreign state reaches a commit.
- **Fold operations remain trivial regardless of divergence size** — a week of accumulated cycle commits squash-merges in one operation; a month does too. The merge cost is constant in fire count.
- **Audit-trail granularity preserved on the cycle branch** — squash-fold produces one commit on main, but the cycle branch retains per-fire commits for cross-agent auditability.
- **Pattern is recognizable for adoption by other autonomous loops** — HOST cadence monitoring, Docs auto-sweep, exec digest aggregation, and other role-specific autonomous work can adopt the architecture with role-specific cycle log paths.

## The session-log composition discipline — log in ONE place: the session log (added 2026-06-09; amended 2026-06-12 — one-place supersedes dual-surface)

This architecture makes the **cycle log** the natural per-fire append-only surface. That is correct for the working-state role — but it created a structural failure mode that surfaced cohort-wide on 2026-06-09 (PM flag 16:48; Architect analysis): **the cycle log silently displaces the session log.**

The mechanism of displacement: the duty-cycle fire loop (cron → mail loop → task loop → cycle-log entry → commit → IDLE) references the *cycle* log at each fire and never the *session* log. So an agent operating inside the matured cycle defaults to writing only the cycle log — "I just logged the fire; why write it again in the session log?" — and the session log accretes nothing between START and STOP. By EOD the day's substantive work lives **only** in the cycle log.

**Why that is an institutional-memory leak, not a cosmetic gap:**

| Surface | Role | Location | Durability |
|---|---|---|---|
| **Session log** | durable per-session institutional-memory; what Docs reads for the omnibus; the cohort's narrative record | `dev/YYYY/MM/DD/...` (dated, permanent) | **Durable** |
| **Cycle log** | ephemeral per-fire working state (this entry's append-only surface) | `dev/active/...` (cleaned at sprint boundaries) | **Ephemeral** |

Cycle logs in `dev/active/` get archived/cleaned at sprint boundaries. If a day's work lived only in the cycle log: Docs's omnibus has gaps *today*; the record vanishes entirely *next week*; a six-month retrospective finds an empty session log and zero cohort memory. The cohort's working memory leaks without anyone noticing until a Docs flag catches one instance.

**The cure — TWO generations (the second supersedes the first):**

- **Gen 1 — dual-surface (v1.5, 2026-06-09):** the first fix kept *both* logs and made the fire loop write to each: when the cycle log carries fire-by-fire detail, the session log MUST also carry a session-summary view (`- Fire N (HH:MM) — one-line description; full detail in cycle log`). Both surfaces accrue content. This *guards against* the drift.
- **Gen 2 — one-place logging (v1.8, RATIFIED by PM 2026-06-12):** the simpler cure — **do the logging in ONE place: the session log.** PM 2026-06-12: *"simplify logging, minimize drift… let's do the logging in one place."* The cycle log is demoted to **optional private scratch** — an agent MAY keep a per-fire scratch list for its own continuity, but it is *not a logging surface, not a parallel record, and never the durable home for work.* Every substantive fire writes its entry directly to the **session log** (`- Fire N (HH:MM) — what shipped`).

**Why Gen 2 supersedes Gen 1 (the load-bearing rule now):** dual-surface *guards against* drift between two records; one-place *removes the drift at its source* — **one log can't drift from itself.** Keeping two synchronized records is itself an asymmetric-discipline cost (m-35) that the displacement trap exploited; collapsing to one record eliminates the synchronization burden rather than policing it. The durable record (the dated session log) is the one kept; the ephemeral one (the `dev/active/` cycle log) becomes discardable scratch. **The rule:** every substantive fire logs to the session log; nothing durable lives only in the cycle log.

**The mechanism (m-36 — impossible-by-construction, not vigilance):** the discipline is baked into the `duty-cycle-tick` skill at **v1.8** (Step 5 single-surface logging — supersedes the v1.5 dual-surface step): the procedure writes the per-fire entry to the session log directly, so there is no second surface to displace. This is the structural-guard form (m-36 Class-2) — the guard lives where the action happens. It is also the *cleaner* class of guard: Gen 1 added a step (write the second copy); Gen 2 *removed* a surface (the parallel record), which is the stronger m-36 move — fewer surfaces means fewer drift seams. Existing safeguards (the clock-based `log-maintenance-reminder` hook; the PreCompact hook; Docs's merge-keeper sweep) operate on the session log directly, so they now align with the single durable surface.

**Meta-shape:** session-log-vs-cycle-log displacement is the founding instance of a more general meta-shape — *a matured mechanism silently displaces an older discipline it was meant to compose with, because the mechanism's procedure loop doesn't reference the older surface.* **Now filed as methodology-41 (Mechanism Displaces Unreferenced Discipline), PROVEN (2026-06-12)** — Docs's cohort-wide audit (2026-06-09) found the displacement systemic (6 of 9 cycling roles, ~15 role-days); m-41 reached Proven on its second + third structurally-different instances (Exec variant-preservation trap; architecture-boundary force-by-constraint), PM-ratified with Architect concurrence. Note the recursive irony: the one-place amendment *above* is itself an m-41 cure applied to this very entry — the dual-surface mechanism (v1.5) was a discipline composed *onto* the cycle that PM's one-place cure later displaced, by removing the surface rather than adding a guard. Adjacent to but distinct from methodology-35 (asymmetric-discipline-creation-without-paired-cleanup): m-35 is *create discipline without cleanup*; m-41 is *create mechanism that displaces a composable discipline*.

## Cross-references

- **Architect session-log-vs-cycle-log displacement memo** (2026-06-09): the cohort-wide analysis + prevention recommendations that prompted this section; CIO disposition (this amendment + the skill v1.5 mechanism) is Recommendation 5 actioned.
- **`duty-cycle-tick` skill v1.5 → v1.8** (2026-06-09 → 2026-06-12): v1.5 was the Step-5 dual-surface mechanism; **v1.8 is the current Step-5 single-surface (one-place) mechanism** per PM's 2026-06-12 ratification. The skill is the operational home of this section's rule.
- **methodology-36 (Derived-Views / Mechanism-Beats-Vigilance)**: both the dual-surface and the one-place fixes are Class-2 structural-guards (guard at the action site); the one-place fix is the stronger move (remove a surface rather than add a synchronization step).
- **methodology-41 (Mechanism Displaces Unreferenced Discipline), PROVEN**: this section is m-41's founding instance; the one-place amendment is itself an m-41 cure (surface-removal class).
- **CIO Phase 5 V3 redesign memo** (`mailboxes/cio/read/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-phase-5-v3-redesign-plus-hook-race-finding-2026-05-17.md`): the memo that documented the failure mode and the V3 architecture in cohort-readable form; this methodology entry is the codification.
- **CIO Day-1 reflection memo** (May 17 morning): introduced the v3-fix-targets concept as future work; this entry pulls it from future to present.
- **V1 duty cycle design v0.4** (`dev/active/cio-v1-duty-cycle-design-v0.4-2026-05-17.md`): the pre-V3 design that contained the rebase-onto-main step; the design's "Known structural costs" section anticipated v3 fix-targets but underestimated the failure severity.
- **Pattern-068 family** (silent state mutation in shared working tree): the hook-race failure mode is a Pattern-068 sibling; Architect disposition expected on whether this warrants a new sub-pattern or body extension.
- **Pattern-073 (Documentation-Asserted-Behavior Drift)**: MANIFEST regen is one instance of the broader Pattern-073 shape; the autonomous-cycle's response (poll directory, not MANIFEST) is the 4th-instance disposition that this architecture extends.
- **methodology-28 (Pre-Filing Slot-Availability Check)**: applied to claim slot 31 (skipping reserved methodology-30 for Consumer-Trace Verification).
- **methodology-29 (Pattern Formation via Successful Imitation)**: this architecture is currently a one-instance design (CIO Phase 5 V3). Cohort adoption across other roles would form the pattern via imitation if the architecture's predictions hold.

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. The architecture framing is general (not CIO-Phase-5-specific); the entry stands as canonical for any autonomous-loop work that meets the "when to apply" criteria.

The entry does not specify the operational details of the V3 cron prompt (those live in the CIO Phase 5 V3 memo + the cycle prompt itself); it specifies the architectural discipline. Other roles adopting the architecture would parameterize the cycle log path + branch naming + fold cadence to their context.

Phase 6+ (cycle mutation surface) is flagged as a separate design problem this architecture deliberately does not solve. The append-only constraint is what makes the architecture's guarantees work. Mutation-surface autonomous loops need a different shape (likely: cycle writes its proposed mutations to a separate path that main folds in via review, or cycle's mutation surface runs in a different worktree on main directly). Pre-design open.

---

*Filed: 2026-05-18 by CIO Vehicle 2. Pattern category: methodology-corpus design-discipline for autonomous loops. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-31 (next available; pre-filing slot-availability check applied per methodology-28; methodology-30 reserved for Consumer-Trace Verification per the Mon-Tue batch carryover).*
