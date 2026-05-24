# Derived Views Over Hand-Maintained Trackers — Mechanism Beats Vigilance

## Overview

**Derived Views Over Hand-Maintained Trackers** names the principle that any tracker requiring human attention to stay current is only as reliable as the human attention applied to it. In a long session with substantial work in flight, tracker maintenance falls to the back of the queue. The tracker then represents *past state*, not current state, and consulting it doesn't surface current gaps.

The structural fix: **derived views over a substrate of record**, not hand-maintained trackers. The substrate is updated through structural mechanism (mail filing, commit, file move); the view is computed when consulted. Staleness becomes impossible because the view is regenerated at read time.

The discipline applies cross-cohort: any role with a hand-maintained tracker that has experienced staleness-at-the-moment-of-need is a candidate for refactor toward a derived view over a structural substrate.

## Why This Methodology

### The shared-shape evidence (May 24, 2026)

Comms's process-improvement seed memo (`memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`) surfaced two visibility-loss incidents in one day. **Both incidents involved a tracker that should have caught the gap, and both trackers failed in the same way: hand-maintained ≠ current.**

- The orphan-drafts incident: `dev/active/comms-open-topics.md` listed *"10 drafted pieces... 2 unscheduled insights"* as of May 10 — but went stale until Docs surfaced the orphans on May 24
- The kickoff-move-to-read incident: session log Pending list should have carried the kickoff's downstream-artifact obligation — but multi-hour-session attention pressure left the obligation in volatile chat memory only

Comms's deeper framing: *"This isn't a personal-vigilance failure. It's a structural property of hand-maintained trackers. Vigilance fails. Mechanisms don't."*

That framing graduates the observation from "let's be more disciplined about the tracker" to a structural-fix-instead-of-discipline-fix candidate (PP-004 candidate; see below).

### The cohort's tracker inventory (partial)

Hand-maintained trackers in current cohort use:

- **Comms**: `dev/active/comms-open-topics.md` — narrative drafts + insights + Ship topics
- **HOST**: `mailboxes/host/sent/*-360-commitments-tracker-refresh-*.md` — 360 tracker (already partly derived via mailbox queries; periodic refresh memo is hand-maintained)
- **CIO**: `dev/active/cio-standing-items.md` — standing items (hand-maintained as of v0.5 — designed to persist across days)
- **CIO**: `dev/active/duty-cycle-escalations-cio.md` — PM attention items (hand-maintained)
- **CIO** (catalog): methodology catalog + pattern catalog — file-named-numbered substrate is durable; cross-referencing across patterns/methodologies is hand-maintained via Adjacent-Patterns sections
- **Lead Dev**: GitHub issues + checkbox state — GitHub itself is the substrate; checkbox state is hand-maintained (Pattern-067 instance)
- **Architect**: ADR/PDR registries — file-named-numbered substrate is durable; cross-referencing is hand-maintained
- **Session log Pending lists**: in-session work-tracking — hand-maintained, vulnerable to multi-hour attention pressure
- **Inbox MANIFESTs**: derived-index-over-inbox-folder — hand-maintained (Pattern-073 first-instance-at-derived-index-layer was this exact failure)

All vulnerable to the same failure shape: hand-maintained ≠ current.

### Why derived views are the structural fix

A derived view is **computed from a substrate at read time**. The substrate is the source of truth; the view is a query over it. Staleness becomes impossible because the view doesn't carry state between reads.

Concrete examples of refactor patterns:

- **Editorial calendar as substrate; drafted-but-unscheduled view as query**: comms-open-topics.md retires; the "what's drafted but unscheduled?" view is computed from a calendar query (status=drafted AND pubDate=null). Layer B of Comms's framework targets exactly this refactor.
- **Filesystem state as substrate; orphan-detection view as periodic reconciliation**: `docs/public/comms/drafts/` filesystem state ↔ calendar `draftPath` column reconciled periodically. Layer D in Comms's framework. This isn't *pure* derived (reconciliation has a job-shape) but it catches drift in either direction.
- **Inbox folder state as substrate; MANIFEST as derived view**: MANIFEST autogeneration from `ls inbox/` would retire the Pattern-073 first-instance at the derived-index-layer. (Tooling-debt candidate.)
- **Mailbox state as substrate; 360 tracker as derived view**: HOST's tracker is partly already derived (mailbox queries); the refresh memo is the hand-maintained scar.

### Why this is methodology-corpus, not Pattern catalog

Pattern catalog entries describe **architectural / surface failure modes** (e.g., Pattern-074 visibility-loss-after-premature-retirement; Pattern-067 issue-body-reality-mismatch). They live in `docs/internal/architecture/current/patterns/`.

Derived Views Over Hand-Maintained Trackers is **a discipline-shape principle** — about how cohort tracking *should be authored* to avoid the trackers-go-stale failure mode. It belongs in the methodology corpus (discipline-of-rule-authoring) alongside methodology-35 (Asymmetric Discipline).

The instances of trackers-gone-stale (Pattern-074 instances; Pattern-073 inbox-MANIFEST instance; methodology-35 worktree-proliferation instance) are pattern-shaped; the meta-pattern about choosing derived-views-over-hand-maintained is the methodology.

## Application

### Recognition cue

A tracker is a candidate for derived-view refactor if any of:

- It has experienced staleness-at-the-moment-of-need (track record of the discipline failing)
- It duplicates information already present in a structural substrate (filesystem, mailbox, calendar, GitHub issues)
- It requires manual cross-referencing between sources that could be machine-queried
- Its maintenance falls to the back of the queue during high-load sessions

### Refactor framework

When refactoring a hand-maintained tracker toward a derived view:

1. **Identify the substrate of record** (the source-of-truth structural surface)
2. **Define the view as a query** (what question the tracker answered; what query computes the answer from the substrate)
3. **Build the query mechanism** (script, skill, hook — whatever generates the view on demand)
4. **Retire the hand-maintained tracker** OR rename it to "snapshot-as-of-{date}" if the historical view has value

Comms's Layers A–D framework (preventive + detective combination) is a clean template:

- **A**: prevent the failure at creation (mechanism that makes the failure-state impossible)
- **B**: retire the hand-maintained tracker; derive from substrate
- **C**: require the inventory query as first step in planning sessions
- **D**: periodic reconciliation catch-net (filesystem state ↔ calendar/etc.)

A through C are preventive; D is detective. The combination is *prevent + detect* rather than *prevent only*.

### PP-004 candidate accumulation

This methodology accumulates structural-fix-instead-of-discipline-fix evidence:

- **Instance 1** (May 17): methodology-31's append-only architecture eliminated rebase-onto-main hook-race (V3 V1 era)
- **Instance 2** (May 18): kit-v2's atomic `git worktree add -b` eliminated Pattern-068 P-13 branch-drift (HOST kit-v1 instance)
- **Instance 3** (May 24): Comms's Layer A `draft-blog-post` skill v1.1 mandates calendar row at draft creation (orphan-drafts side)

Three independent instances now eligible. PP-004 *Structural Fix Instead of Discipline Fix* filing candidate; CIO holding for one more confirming case to file with breadth-of-evidence above minimum.

## Cross-references

- Source memo: `mailboxes/cio/read/memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`
- Related pattern: `pattern-074-visibility-loss-after-premature-retirement.md`
- Related methodology: `methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md`
- Methodology-29 framework (pattern formation via successful imitation): governs the PP-004 promotion criteria
- Comms Layer A (landed today): `draft-blog-post` skill v1.1, commit `959e5dca6`

— methodology-36 filed by CIO, 2026-05-24
