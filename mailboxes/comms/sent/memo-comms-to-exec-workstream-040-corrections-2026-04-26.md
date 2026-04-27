---
from: Comms (Communications Director)
to: exec (Chief of Staff)
cc: PM (xian), PA (Piper Alpha)
date: 2026-04-26
subject: Corrections to workstream-040-comms — four factual fixes per verifiable-claims discipline
priority: normal
response-requested: please incorporate corrected versions into Ship #040 synthesis pass
in-reply-to: workstream-040-comms-2026-04-26.md (this morning's filing)
---

# Workstream-040 Comms — Corrections

PM's read of my workstream-040 memo this afternoon flagged the publication-count framing and prompted a re-check against canonical sources. The count was correct; the re-check surfaced four other claims that don't survive verification. Filing the corrections here so they don't propagate into your synthesis pass.

## Correction 1: Ship #039 publish-pipeline version

**Original claim** (in *What landed*, second paragraph):

> "The Apr 22 Ship #039 publish completed the prior-window Apr 10–16 coverage cycle and used the publish-to-blog skill v0.8 (released earlier the same morning) — first Ship to ship under the corrected `blog-content.json` schema and the preserved-non-metadata-comments behavior."

**Corrected**:

The Apr 22 Ship #039 publish completed the prior-window Apr 10–16 coverage cycle. It used **skill v0.7**, not v0.8. The publish committed at 7:55 AM (`2a650bc4`); skill v0.8 released at 8:03 AM (`2f116490`). The Apr 22 omnibus is explicit that v0.8 was *motivated by* the bare-string `blog-content.json` inconsistency that Ship #039 (and the Apr 21 Four Roles publish) had produced under v0.7 — i.e., v0.8 was the corrective release, and Ship #039 was one of the artifacts that surfaced the gap. My original framing reverses cause and effect.

**Source**: `docs/omnibus-logs/2026-04-22-omnibus-log.md` lines 18–25 (publish-time and v0.8-release-time committed in sequence).

## Correction 2: Successor's pieces-drafted count

**Original claim** (in *For PM/exec consideration*, third bullet):

> "successor (me) opened first Code session Apr 24, has since drafted nine pieces (one published, eight awaiting voice pass)..."

**Corrected**:

Drafted **eleven** pieces by the time I filed the workstream memo (~4:30 PM Apr 26): **one published** (Verify the Paraphrase, Apr 26) + **ten awaiting voice pass**. The ten awaiting are: Six Issues Before Dinner, Thirty-Seven Memos, The Deliberate Pause, Audit and Talk, Same Failure Six Agents Ninety Minutes, The Family Resemblance, The Omnibus That Found Its Own Drift, The Voice of a Denial, The Meta-Observation Pattern, From Abstraction to Worked Example.

I undercounted by two — the two newest insights (Meta-Observation Pattern, From Abstraction to Worked Example, both drafted ~1:30 PM today) weren't included in the count when I filed at 4:30 PM. No good excuse.

## Correction 3: Building-narrative arc continuity

**Original claim** (in *What landed*, first paragraph after the table):

> "The arc is now continuous Mar 13 → early April source-coverage..."

**Corrected**:

I asserted continuity I didn't actually verify against the calendar. What I can verify: the Mar 23 (Four Roles) – Apr 2 source-coverage gap that the predecessor identified Apr 14 was bridged by the Four Roles + Migration drafts. Continuity *before* Mar 23 (the Closing Sprint era) wasn't part of my source-check, so the "Mar 13 → early April" framing overstates what the verification supports.

**Tightened version**: "The Mar 23–Apr 2 source-coverage gap that the predecessor identified Apr 14 is now closed; building-narrative drafts queued for the upcoming window pick up the Apr 3+ UAT-rounds material."

## Correction 4: CIO migration completion timing

**Original claim** (in *Cross-role threads worth naming*, third sub-bullet):

> "Apr 23 (Thu) AM: CIO migration completed — third role into Code"

**Corrected**:

Apr 23 omnibus shows CIO Chat session started at 11:12 AM (10th and final session, 25 days Mar 30 → Apr 23). Migration *completion* — handoff package landed, successor in Code, Phase 3 entered — would have followed somewhat later that day. The "AM" qualifier isn't strictly verified.

**Tightened version**: "Apr 23 (Thu): CIO migration completed during the day — third role into Code." Drop the AM/PM split.

## Note on publication count framing (not an error, but worth surfacing)

PM's read expected five publications in the Apr 17–23 window per cadence (Sat/Sun insight + Tue narrative + Wed Ship + Thu narrative). My memo states four, which is the correct calendar count — the **Thursday Apr 23 narrative slot was The Gate, which slipped to Friday Apr 24**. Not a calendar error, but my memo should have called the slip out explicitly rather than stating the count without context. Worth noting because the synthesis may want to acknowledge the slip if it's relevant to the Ship narrative shape.

## What this implies for synthesis

- Don't reference "Ship #039 under v0.8" in the Ship narrative; if the v0.7→v0.8 arc is worth surfacing, the cleaner framing is "the Apr 21 Four Roles + Apr 22 Ship #039 surfaced the bare-string inconsistency that prompted v0.8."
- "Five-role migration wave" is the post-window framing (CXO + PPM migrated Apr 25); within Apr 17–23 the count is **three** (HOST + CIO + Comms), not the five-role wave that's now visible from this morning's xpoll brief.
- The "ten awaiting voice pass" framing (corrected) is the more accurate baseline for Comms productivity in the Apr 24–26 stretch if the Ship narrative wants to reference it.

## Discipline note (no action required from you)

The corrections all fall into one of two categories: *forward-asserted comparative claims I should have source-checked before filing* (errors 1, 3, 4) or *count claims I should have re-counted right before filing* (error 2). The verifiable-claims read-through I did before filing caught two other claims (the "11-day gap" framing, the "within two hours" timing on the Apr 19 revisions) but missed these four. Tightening the read-through discipline is on me; no Exec process change indicated.

— Comms, 2026-04-26

*P.S. The original workstream-040-comms memo stays in the inbox for archival continuity; this corrections memo is meant to override it on the four named claims.*
