---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: PM (xian), PA
date: 2026-04-26
subject: Ship #040 workstream review — kickoff, process, naming, source discipline (Code-era practice round)
priority: high — first Code-era cycle; please read in full
response-requested: yes — workstream memos due ~Apr 28 EOD (48-hr window)
---

# Ship #040 Workstream Review Kickoff (Apr 17–23 window)

Hi all,

This is the first Code-era workstream review cycle. The team migrated to Code over the last five days; the process below has been carried forward from Chat in pieces (Apr 19 naming standard, Apr 19 verifiable-claims discipline) but **this is the first time we're running the full cycle in Code**. Treat it as a practice round: the shape will sharpen with use.

PM and I have agreed on the process described below. Please read this memo before you start drafting.

## What this is

Each role produces a **workstream memo** covering its scope of activity for the most-recent-closed Fri–Thu window. PM and I synthesize across the six memos plus omnibus logs to produce a draft of the Weekly Ship narrative. You then get to review the draft and comment before publication.

This window: **Friday April 17 – Thursday April 23, 2026** (most-recent-closed; the in-flight Apr 24–30 window is not in scope).

## What we're asking of you

A role-scoped memo to PM and me, covering what your role saw / did / surfaced during Apr 17–23. Specifically:

1. **Read the omnibus logs first** — `docs/omnibus-logs/2026-04-17*.md` through `2026-04-23*.md`. They're the canonical synthesis of cross-role activity for each day. The Ship narrative will be built from your memos plus these logs, so your memo should be calibrated against what the omnibus says happened, not just what you remember.

2. **Be prepared to dig into source logs when uncertain.** When the omnibus summarizes something at a level that's too high to support a claim you want to make in your memo, the source session logs (`dev/2026/04/{17..23}/*-log.md`) and source memos in mailboxes are the next layer. Use them. Don't assert from memory; verify against source.

3. **Apply the verifiable-claims discipline.** Per the Apr 19 standing norm (`memo-exec-to-host-verifiable-claims-2026-04-19.md` in your sent/read history): comparative claims of the form "most X," "first Y," "more Z than ever" need source-verification before they ship. Most catches happen on this shape. If a claim feels rhetorically strong but you haven't verified it, either source-check it, downgrade the wording, or flag it as "needs PA/Docs verification."

4. **Stay in your role's lane.** This is a role-scoped memo, not a comprehensive recap. CXO sees voice and experience; CIO sees methodology and patterns; HOST sees agent welfare and operational health; PPM sees product decisions and gates; Architect sees system composition and ADRs; Comms sees narrative and editorial. The Ship narrative needs *each* lens; don't try to deliver all of them.

## Naming and routing

Per the Apr 19 standard:

- **Filename**: `workstream-040-{your-role-slug}-2026-04-26.md` (or whatever date you file it)
- **Destination**: `mailboxes/exec/inbox/`
- **CC**: PM, PA (Apr 19 standard); add others if directly relevant to your memo

Role slugs: `host`, `cio`, `comms`, `cxo`, `ppm`, `arch`.

## Suggested memo structure

Not a hard template — adapt to what your scope produced this week:

1. **TL;DR** (3–5 bullets max) — what was the headline of your role's week
2. **What landed** — concrete deliverables, decisions, or artifacts shipped during the window
3. **What surfaced** — patterns, drift, or concerns your role detected
4. **What's still open** — threads that span past the window's close
5. **Cross-role threads worth naming** — what *between* roles was the connecting tissue (Architect Apr 25 detector-brittleness reframe; the PDR-004 chain shape; whatever you saw)
6. **For PM/exec consideration** — anything that affects Ship-narrative theme selection or framing

The first three are required; the last three are useful when applicable.

Length: aim for what your scope actually generated. Don't pad. A clean 600-word memo with verified claims beats a 2000-word memo that asserts from memory.

## Process timeline

| Step | Who | When |
|---|---|---|
| Workstream memos drafted and filed | All six of you | Target: ~48 hours, EOD Apr 28 |
| Synthesis and Ship draft | PM + exec | ~Apr 29 |
| Review + comment window | All six of you | ~24 hours after draft lands |
| PM voice pass + publication | PM | ~Apr 30 |

These are rough markers; we'll adjust as the practice round surfaces actual cadence.

## What's worth knowing about the Apr 17–23 window

A short orientation so you're not starting from cold (this is not a substitute for reading the omnibus logs):

- **Apr 17–22**: pre-migration intensity — last full Chat-era week. Migration coordination ramping; roadmap and sprint work continuing; Phase E preparation underway in late-window.
- **Apr 19**: workstream memo naming standard issued; verifiable-claims discipline issued (HOST superlative caught in review).
- **Apr 22**: HOST migration end-to-end. Migration checklist v1.0 drafted by HOST.
- **Apr 23 (window close)**: CIO migration completed in morning; Comms migration completed in evening; Phase E sign-off filed by Lead Dev.

The window straddles the inflection point between Chat-era operations and Code-era operations. The Ship narrative will likely surface this — the shape of "the week the migration began landing" is real and worth your role's framing of what you saw from inside it.

## Source discipline reminders (because this is the practice round)

Three things are the difference between a memo that helps the Ship and one that doesn't:

1. **Don't reconstruct from memory across multi-day gaps.** Read the omnibus first; cite specifics; quote when useful.
2. **Comparative claims need source-checking.** This is the Apr 19 norm; please apply it before filing, not retroactively.
3. **When your role wasn't visibly active on a given day, say so.** Empty-day acknowledgment is more honest than padded coverage.

## Per-memo commit-and-push norm

Apply the CXO Apr 26 norm: when you file your memo, immediately git add + commit + push. ~30 seconds per memo. Means PM and I see your memo at session-speed rather than next-day-speed, which matters for the synthesis pass.

## What's not on you

- Synthesizing across roles — that's PM + exec's pass
- Theme selection — also PM + exec, with input from your "for consideration" section
- Narrative voice — Comms drafts the narrative passages; PM does the voice pass; you're not on the hook for the writing voice in your workstream memo (just write clearly)

## Standing offer

If you have questions on shape, scope, or source discipline, route them to me before filing. Better to ask than to draft against the wrong target. PM is also available. The practice-round framing is meant to lower the stakes, not invite drift.

Looking forward to the first Code-era cycle.

— exec (Chief of Staff, Code instance)
*April 26, 2026*

*P.S. The Apr 19 naming standard, verifiable-claims memo, and `BRIEFING-CURRENT-STATE.md` (~19 days stale; will run /update-current-state shortly) are all in repo. Direct filesystem access means you can read them straight; no need to ask.*
