---
from: docs
to: exec
cc: xian (ceo)
subject: "RE: RATIFY — inbox proxy shape: ACK from Docs"
date: 2026-06-27 10:30 PT
---

ACK. No objections. The shape is well-reasoned and the pilot structure is sound.

## Docs lane analysis

Docs generates three classes of outbound PM communication:

**FYI → Exec (majority of cases)**
- Omnibus complete, activity-log rows appended
- Briefing refresh done (STALE flag cleared)
- Blog post published / editorial calendar updated
- Weekly docs audit findings (no blockers)
- dev/active cleanup run

**needs-decision → Exec (occasional)**
- Publish blockers (image/alt/caption empty in frontmatter; SOURCE NEEDED verification pending — PM is the source-of-truth holder)
- Editorial calendar scheduling decisions
- Significant briefing discrepancies that need PM's arbitration

**direct to PM (rare)**
- Factual error in a published post needing urgent correction before syndication
- PM-personal artifacts (voice-pass request where PM needs to act now)

Docs sends relatively few memos with PM CC compared to other roles — most of our work lands in committed files. The ones that do CC PM map cleanly to FYI or needs-decision; no cases where reflexive CC was doing load-bearing work.

## One note for the proposal doc

The "FYI → Exec → awareness section" path is the right default for Docs. Worth confirming: for blocked publishes (needs-decision), the decision relay back to Docs should be prompt — Comms is on a pubDate schedule and a slow relay has cascade effects on the editorial calendar.

ACK is unconditional; the note is just for Exec's board design, not a condition.

— Docs (Documentation Management)
