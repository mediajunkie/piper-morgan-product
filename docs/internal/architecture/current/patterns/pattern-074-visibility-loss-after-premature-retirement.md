# Pattern-074: Visibility Loss After Premature Retirement

## Status

**Emerging** — Filed 2026-05-24 by CIO per Comms's process-improvement seed memo (`memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`). **Two reference instances** logged within a single day (both Comms-side, May 24, 2026). Meets methodology-29 framework's minimum-for-Emerging threshold (≥2 independent instances within a bounded window); needs ≥1 more independent cross-role instance to graduate Emerging → Proven.

Slot 074 allocated per pre-filing slot-availability check; 073 occupied (Documentation-Asserted-Behavior Drift). CIO catalog-management authority per methodology-29 framework.

## Product Relevance

**Methodology / Discipline** — Recognition discipline for a specific failure shape in how teams manage active-vs-completed state of work artifacts (inbound mail, draft files, issue trackers, etc.). Users will not encounter this pattern directly; agents and engineers managing work-state transitions will reach for it when an artifact is moved to a "completed" location prematurely.

## Context

Work artifacts (inbound memos, draft files, issues, tasks) have an implicit *state* communicated by their **location**. An artifact in `inbox/` means *active; needs attention*. An artifact in `read/` or `done/` or equivalent means *handled; no further action needed*. The location IS the done-signal that other observers (PM, peer agents, the agent's own future self) read.

When an artifact is moved to its "completed" location BEFORE the downstream work the artifact required is actually complete, the implicit done-signal is wrong. The gap is silent: from outside the failing surface, the artifact looks handled.

### Where this surfaced

Two independent instances on May 24, 2026, both Comms-side:

1. **Orphan blog drafts** (uncovered ~12:19 PM PT) — 4 draft files sat in `docs/public/comms/drafts/` for weeks (workDates Mar 30 – Apr 22) without corresponding editorial-calendar rows. The drafts' presence in `drafts/` signaled "drafted, awaiting publish." But no calendar row meant no scheduling, no publish path, no PM-side visibility. By the time Docs's Group 3 cleanup pass surfaced them, 5 later-workDate narratives + 2 later-workDate insights had already published ahead — absolute-chronology drift unrecoverable.

2. **Ship #044 workstream kickoff prematurely moved to read/** (caught ~2:28 PM PT) — Comms triaged 4 inbox items including Exec's Ship #044 workstream-review kickoff. The kickoff was read, content noted in chat, **then moved to `comms/read/`** before the workstream review memo it required had been filed. The kickoff's downstream artifact (the Comms workstream memo, due Tue May 26 EOD) didn't yet exist; the move-to-read silenced the active-state signal. PM noticed the kickoff disappearing from inbox + flagged it; visibility was only restored by PM-side noticing.

### The recurring shape across both instances

The artifact's **"active" state ended before the downstream work was complete.** A tracker that *should* have caught the gap (the open-topics tracker for orphans; the session log Pending list for the kickoff) was stale, partial, or not consulted. The failure was invisible until an outside observer surfaced it (Docs for the orphans, PM for the kickoff). The cost was bounded only by *how soon someone outside the failing surface noticed*.

| Instance | Active artifact | Premature retirement signal | Downstream artifact missing |
|---|---|---|---|
| Orphan drafts | Draft files in `drafts/` | File creation without calendar row | Calendar row tracking the draft |
| Kickoff move-to-read | Inbound memo in `comms/inbox/` | Move to `comms/read/` post-read | Workstream review memo required by kickoff |

The asymmetry that makes this load-bearing:

- **The artifact's location is the done-signal observers consume.** Moving to "completed" location implicitly says "done."
- **The downstream work's existence is the actual completion criterion.** Whether the downstream work exists is invisible from the artifact's location.
- **Vigilance via hand-maintained trackers fails when needed most.** In a long session with substantial work in flight, tracker maintenance falls to the back of the queue. The tracker represents *past state*, not current state. Consulting it doesn't surface current gaps.

## Problem

### The failure mode

```
Artifact A is in active-location L_active (e.g., inbox/, drafts/, open-issues)
   → Agent processes A's content + extracts asks
   → Agent moves A from L_active to L_done (e.g., read/, archive/, closed)
   → Downstream artifact D required by A does not yet exist
   → A's location now signals "handled" to all observers
   → D's absence is invisible from outside the failing surface
   → Failure surfaces only when an outside observer notices (or never, until cost compounds)
```

### Why hand-maintained trackers don't save us

In both May 24 instances, a tracker designed to catch this kind of gap existed (`dev/active/comms-open-topics.md` for orphan drafts; session log Pending list for the kickoff). Both failed in the same way: **hand-maintained trackers require discipline to keep current, and the discipline broke at the exact moment when the catch was needed.**

A tracker that needs human attention to stay current is only as reliable as the human attention applied to it. This isn't a personal-vigilance failure. It's a structural property of hand-maintained trackers. Vigilance fails. Mechanisms don't.

(See methodology-36 *Derived Views Over Hand-Maintained Trackers* for the deeper structural treatment.)

### Recognition cue

The cue for this pattern's appearance:

- An artifact moved from active-location to completed-location
- The agent's mental model says "I read it / I processed the content"
- But the **downstream artifact the original artifact required** has not yet been produced

## Resolution

### Discipline shape

**Move to "completed" location only when ALL of:**
1. Content processed
2. Required downstream artifact exists OR no downstream artifact required

**Stay in "active" location when** (1) is true but (2) is not. **Annotate the active location** with explicit *"Active until {downstream artifact}"* naming the gating artifact.

This is the **annotation-in-active-queue** approach (alternative considered: add a third folder state like `pending/`; chose annotation for simplicity + 2-state preservation).

### Cohort-wide adoption (CIO ratified 2026-05-24)

The annotation-in-active-queue discipline generalizes beyond Comms. Any role that processes inbound work and produces downstream artifacts is subject to the same trap:

- **CIO**: methodology + pattern entries asked-for in inbound memos (this very memo as instance)
- **HOST**: 360-tracker items + per-role health-touch flags
- **PPM**: ratification asks + decision-rule sign-offs
- **Lead Dev**: issue work referenced in inbound + cross-role mail
- **Arch**: ADR/PDR review asks
- **Exec**: workstream-kickoff distributions awaiting return memos

Each role has its own version of *"this looks handled but the downstream artifact doesn't exist yet."* The annotation-in-active-queue rule applies cross-cohort.

### Memory pin sharpening (Comms, 2026-05-24)

The `feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately` memory pin was sharpened today to operationalize *"used"* as *"the downstream artifact required by the memo exists,"* not just *"the memo content has been processed."* CIO endorses this sharpening as cohort-wide; agents whose memory pins reference move-to-read discipline should update accordingly.

## Relationship to Adjacent Patterns

- **Pattern-066 (Stacked Silent Failures)**: same silent-failure family; Pattern-074 specifically about state-transition silence at the active/completed boundary
- **Pattern-067 (Issue Body Reality Mismatch)**: adjacent in that both involve a surface (issue body / artifact location) drifting from underlying truth (code state / downstream-artifact existence)
- **Pattern-073 (Documentation-Asserted-Behavior Drift)**: distinct — Pattern-073 is about claims about behavior; Pattern-074 is about implicit completion-signals via location
- **methodology-35 (Asymmetric Discipline)**: the orphan-drafts instance specifically has methodology-35 shape — the "draft-creation" rule was well-specified but the "register-in-calendar" cleanup-half was unspecified. The fix (draft-blog-post skill v1.1) symmetrified the create-rule by mandating calendar row at draft creation. Pattern-074 is the surface failure; methodology-35 is the discipline-authoring shape that produced it.

## Watch surface for additional instances (graduate to Proven)

Candidate places the pattern may surface next:

- **Issues moved to "closed" before merge** (issue body unchecked checkbox = Pattern-067; closing before merge = Pattern-074 candidate)
- **Branches deleted before merge-keeper sweep confirms merge** (stranded-work risk)
- **PRs marked "ready for review" before tests are green** (CI signal premature)
- **Calendar rows marked `drafted` before draft file exists** (reverse-orphan; calendar-side analog)
- **Mailbox CC memos triaged to read/ before action items are tracked** (CC implies info-only, but action items can still exist)

Three or more independent cross-role instances would graduate the pattern to Proven per methodology-29.

## Cross-references

- Source memo: `mailboxes/cio/read/memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`
- Layer A fix (orphan-drafts side): `draft-blog-post` skill v1.1, commit `959e5dca6`
- Memory pin (updated today): `feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately.md`
- Related methodology: `methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md`
- Related methodology: `methodology-36-DERIVED-VIEWS-OVER-HAND-MAINTAINED-TRACKERS.md` (filed same session)
- Pattern catalog discipline: `docs/internal/architecture/current/patterns/` slot allocation per pre-filing slot-availability check

— Pattern-074 filed by CIO, 2026-05-24
