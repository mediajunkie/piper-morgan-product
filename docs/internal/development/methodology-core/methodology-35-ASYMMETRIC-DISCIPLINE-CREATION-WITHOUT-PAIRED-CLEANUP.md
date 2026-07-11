# Asymmetric Discipline — Operational Rules with Creation Without Paired Cleanup

## Overview

**Asymmetric Discipline** names the failure mode where an operational rule ratchets up cumulative state without a paired cleanup mechanism, producing accumulating overhead the rule's authors didn't anticipate. The shape:

1. A rule is introduced that requires creating a new artifact (file, branch, worktree, memo, etc.) under specified conditions
2. The rule explicitly governs *when to create* but is silent or under-specified on *when to remove*
3. Over time, the artifact-count accumulates with no proportional removal
4. The accumulation eventually becomes its own cleanup burden, often surfaced via PM-direct ask or audit rather than self-correction

The discipline asymmetry — creation-half well-specified, cleanup-half unspecified — is the structural failure shape. Pair this with a cleanup-when-{condition} sub-rule to close the asymmetry.

## Why This Methodology

### The worktree-proliferation instance (May 20, 2026)

Lead Dev's May 20 audit memo (commit `ac222b49f`) surfaced the pattern:

PM-directed audit found 15 sibling worktrees + 6 random-slug worktrees in `.claude/worktrees/` accumulated since May 15. Lead Dev cleaned 6 fully-merged ones + filed cohort triage for the 9 unmerged. The structural finding: CLAUDE.md's "Worktree-default for substantive sessions" (PM directive 2026-05-15) specifies *when to create* but is silent on *when to remove*.

The cleanup half wasn't built into the discipline at adoption. Over five days, the accumulation became its own operational burden requiring a PM-directed audit to surface.

CIO disposition (May 20 response, commit `3e7c39eb5`):
- Worktree-proliferation is NOT a Pattern-073 instance (different shape — Pattern-073 is asserted-behavior-drift; this is creation-without-cleanup)
- File as methodology-corpus candidate covering the broader asymmetric-discipline shape
- Pair the worktree-default discipline with a cleanup-when-merged sub-rule
- Routing to Docs's daily merge-keeper sweep for the cohort-wide cleanup mechanism

This methodology entry formalizes that disposition.

### Why this is methodology-corpus, not Pattern catalog

Pattern catalog entries describe **architectural failure modes** (e.g., Pattern-073 documentation-asserted-behavior-drift; Pattern-068 family silent-state-mutation). They live in `docs/internal/architecture/current/patterns/`.

Asymmetric Discipline is **a discipline-shape failure mode** — about how operational rules are authored + maintained. It belongs in the methodology corpus (discipline-of-rule-authoring) rather than the pattern catalog (discipline-of-architecture).

The instances of Asymmetric Discipline (worktree-proliferation; potentially others) ARE pattern-shaped (recurring failure modes), but the meta-pattern is about discipline asymmetry itself.

### Candidate additional instances (watch surface)

The pattern needs ≥2 more independent instances to graduate Emerging → Proven (per methodology-29 framework). Watch surface candidates:

- **Cycle-log branches** (claude/{role}-duty-cycle-YYYY-MM-DD) — V1 era pattern that piled branches without cleanup; retired but illustrative
- **Session log graveyard** — daily session logs accumulate; dated directories impose organization but no removal/archival discipline
- **`dev/active/` accumulation** — designed as living working-state; the `cleanup-dev-active` skill is the paired-cleanup mechanism (asymmetric originally; symmetrified retroactively)
- **Inbox-without-triage** — memos accumulate without disposition; the Session-Start Inbox Triage Gate (filed May 18) is the paired-cleanup mechanism (asymmetric originally; symmetrified)
- **Memory pin accumulation** — feedback memories accumulate over time; consolidation pass is the paired-cleanup mechanism (asymmetric originally; consolidate-memory skill provides cleanup)

Several existing disciplines retroactively grew their cleanup-half via skills or process amendments. The pattern of "create-rule-first; cleanup-rule-added-later-when-pain-surfaces" is itself the asymmetric-discipline shape.

## When to apply this framing

### Apply this framing when

- Authoring a new operational rule that requires artifact creation — explicitly design the cleanup-when-{condition} pair at the same time
- Auditing existing operational rules — check whether each rule's cleanup-half is specified
- Investigating cumulative-state pain (worktree pile-up, inbox depth, branch graveyard, etc.) — likely an asymmetric-discipline instance; surface the missing cleanup half
- Reviewing methodology corpus entries — ensure each operational discipline has paired-cleanup specified

### This framing does not apply when

- The rule is genuinely create-only by intent (e.g., commit history is append-only by design; we don't want a "delete old commits" discipline)
- The accumulating state IS the value (e.g., session logs preserve institutional memory; the dating organizes; "cleanup" would lose information)
- The rule is one-shot or context-bounded (e.g., per-session housekeeping; doesn't compound across sessions)

## What it predicts

If Asymmetric Discipline is applied as a watch lens, the following downstream signals should appear:

- **PM-directed audits surface accumulation pain** as the dominant symptom (rather than agents self-correcting) — same shape as the worktree-proliferation discovery
- **Retroactive cleanup-half additions** to existing disciplines follow recurring pain (cleanup-dev-active skill; consolidate-memory skill; Inbox Triage Gate) — pattern of cleanup-as-afterthought
- **New disciplines authored after this framing lands carry their cleanup-half from inception** — the rule-authoring discipline shifts from create-only to create-with-cleanup
- **Cohort's operational overhead decreases over time** as accumulated state stops compounding

## Cross-references

- **Lead Dev worktree-proliferation memo** (May 20, commit `ac222b49f`): the originating instance + PM-audit-surfaced finding
- **CIO disposition response** (May 20, commit `3e7c39eb5`): named the Asymmetric Discipline framing as methodology candidate; proposed pairing worktree-default with cleanup-when-merged
- **CLAUDE.md "Worktree-default for substantive sessions"** (PM directive 2026-05-15): the creation-half discipline; cleanup-half forthcoming
- **methodology-29 (Pattern Formation via Successful Imitation)**: the framework for graduating Emerging → Proven via additional instances
- **methodology-31 (Append-Only Autonomous-Cycle Architecture)**: NOT this pattern shape — methodology-31 is structural-fix-of-architectural-failure-mode; this entry is rule-authoring-discipline
- **`cleanup-dev-active` skill**: example of retroactive cleanup-half addition to an asymmetric discipline
- **`consolidate-memory` skill**: example of retroactive cleanup-half addition to memory accumulation
- **Session-Start Inbox Triage Gate** (May 18 CIO proposal, Docs queue): example of paired-cleanup design (the gate IS the cleanup half of inbox-write discipline)

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Status: **Proven** (promoted 2026-07-10, criterion met — see below). Originally filed **Emerging** — one well-evidenced instance (worktree-proliferation) + several candidate-additional instances on watch.

**Promotion-to-Proven criterion**: ≥2 more independent instances of Asymmetric Discipline surfacing in cohort operation, each paired with a cleanup-half addition that resolves the pain. **Met 2026-07-10** by two independent cron-lifecycle instances, diagnosed the same day with PM:

1. **`duty-cycle-tick`'s STOP re-arm** — the STOP procedure said "re-CronCreate same expr as the final action" without ever specifying a check-and-delete of the existing job first; any agent following it literally while idle at STOP (the normal case) produced a duplicate. Cleanup-half added: `duty-cycle-tick/SKILL.md` fixed at all 4 places using the ambiguous phrasing to require `CronList` → `CronDelete` existing → `CronCreate` → verify-exactly-one; **tested live** against a real session's cron (`772e045e` → `8094d7db`), not simulated.
2. **Docs's `f33227b7`** — migrating from an ephemeral cron to a `scheduled-tasks` entry (to satisfy a PM schedule-change request) created the new job but never deleted the old mechanism's. Cleanup-half added: `docs/operations/duty-cycle design/procedures/cron-lifecycle.md` § "Cron-mechanism migration — the orphaned-predecessor gap" — the explicit self-delete-as-part-of-the-same-migration discipline, plus a detection-and-nudge backstop (`list_sessions` + `send_message`) for when the discipline is missed and the visibility window has already closed.

The retroactive-cleanup pattern (Inbox Gate, cleanup-dev-active, consolidate-memory) suggested the framing already operated implicitly before this promotion; these two instances are the first *cron-lifecycle* confirmations, and the first where the cleanup-half was both written down and verified rather than just proposed.

Slot 35 per pre-filing slot-availability check (methodology-28); filed in the May 24 methodology batch.

The cleanup-half discipline this entry recommends is **simpler than the create-half** in most cases — pair every creation rule with "remove when {merged / processed / cohort-resolved / N-days-stale / etc.}" Asymmetric-discipline-aware authoring is a low-cost upgrade to rule-authoring practice.

---

*Filed: 2026-05-24 by CIO Vehicle 2. Pattern category: methodology-corpus discipline-authoring observation. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-35 (pre-filing slot-availability check applied per methodology-28; slots 30-34 filed prior).*
