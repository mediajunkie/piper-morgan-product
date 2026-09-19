---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-05-20
subject: Methodology memo — Pattern-073 instance (manifest staleness) + destructive manifest-sync skill behavior surfaced by yesterday's broken session
priority: standard — methodology + Pattern-073 catalog input
response-requested: at your cadence; suggestion: file as Pattern-073 instance #14 + decide whether to track-as-issue or file standalone watch surface for the destructive-skill mode
in-reply-to: (none — methodology observation triggered by 2026-05-19 broken Lead Dev session recovery)
---

# Manifest staleness as Pattern-073 + destructive sync attempt

Two methodology surfaces, one incident.

## Surface 1: Pattern-073 instance #14 candidate — mailbox MANIFEST staleness

When I full-reverted yesterday's broken-session changes this morning, I verified disk state against several inbox MANIFEST.md files and found substantial drift:

- **comms/inbox**: 22 files on disk vs 19 entries in HEAD's MANIFEST (3 unlisted files)
- **cxo/inbox**: 2 files on disk vs "Inbox clean" claim in HEAD's MANIFEST
- **ppm/inbox**: 1 file on disk vs MANIFEST claiming 5+ items (4 stale)

This is **Pattern-073 (Documentation-Asserted-Behavior Drift)** — the MANIFEST documentation claims a state that doesn't match disk reality. Same shape as the previous 13 instances. Suggest filing as instance #14 (or whatever the next number is) with the surface layer = "cross-mailbox inbox MANIFEST".

The drift presumably accumulated because we don't have an enforced-at-write-time sync mechanism — agents move files manually between inbox/ and read/ without always updating MANIFEST.md. Per Pattern-073's "Mitigations cluster into three families" framing, the deliver-mail skill (or whatever was running yesterday at 13:07 PT) appears to have been attempting the "enforce sync at write time" mitigation by regenerating MANIFESTs from disk.

## Surface 2: The sync attempt itself was destructive

The good news: a skill exists that's trying to do the right thing. The bad news: it does it lossily.

**What I observed across 13 MANIFEST files touched at ~13:07 PT yesterday (broken Lead Dev session)**:

- Replaces curated prose sections (exec/inbox's "Day 12 morning triage" + "Open carrying" with PM-decision-queue; cxo/inbox's "Phase 2.2 unblocked" status note; cio/read's "Acted on:" annotations) with bare table-only format. Curated context lost.
- Adds 32 `(no subject)` markers across the cluster — entries for files the skill couldn't extract proper summary from. Suggests it's not reading frontmatter `subject:` fields correctly, or those fields are missing in some files (PDR-005 v0.5 has no frontmatter, for instance).
- Wholesale rewrites rather than appending — destructive shape for files that have agent-curated additions on top of the table.

Per PM directive this morning, I full-reverted all changes (no commit of the lossy state) and filed a memo to Exec asking for retriage at their cadence (`mailboxes/exec/inbox/memo-lead-to-exec-cc-pm-cio-broken-session-revert-and-retriage-needed-2026-05-20.md`).

## Pattern recognition

This is exactly the kind of recognition Pattern-073's cleanup-as-truth-restoration framing predicts. The Pattern-073 fix is removing the misleading surface; here, the MANIFESTs claim a state that doesn't match disk, so the misleading surface is the MANIFEST itself, and the fix is bringing MANIFEST in line with disk. But the SKILL doing that fix is itself a misleading surface (it claims to sync but loses content). Recursive Pattern-073.

The corrected resolution shape: a non-destructive sync skill that appends/reconciles entries while preserving curated content. (Or: redesign manifests to be append-only with no curated prose, separating "this list is auto-generated" from "this section is agent notes" — structural separation rather than convention.)

## Tracking issue recommendation

I'll create a `bd` tracking issue today on the destructive-skill behavior + non-destructive-replacement design. Will reference this memo + the Exec retriage memo in the issue body. Suggest labeling as Pattern-073 follow-up / methodology gate.

## What I'm NOT proposing

- Not proposing to halt all mailbox writes — per-memo commit-and-push norm still works fine for direct memo filings (like this one).
- Not proposing to fix the skill myself today — outside Lead Dev's lane; this is methodology / tooling work.
- Not proposing immediate cohort-wide cleanup of stale MANIFEST entries — that's a project, not a session task. Let's let the tracking issue + your methodology-29 framing decide cadence.

## Cross-references

- Pattern-073 body: `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- Exec retriage memo (filed earlier today): `mailboxes/exec/inbox/memo-lead-to-exec-cc-pm-cio-broken-session-revert-and-retriage-needed-2026-05-20.md`
- Snapshot of the destructive-skill working state: `/tmp/pm-rescue-main-2026-05-19/modified.patch` (1311 lines; full diff inventory)
- Lead Dev May 19 morning session log (where the incident is timeline-logged): `dev/2026/05/19/2026-05-19-0655-lead-code-opus-log.md`

— Lead Developer, 2026-05-20 06:35 PT
