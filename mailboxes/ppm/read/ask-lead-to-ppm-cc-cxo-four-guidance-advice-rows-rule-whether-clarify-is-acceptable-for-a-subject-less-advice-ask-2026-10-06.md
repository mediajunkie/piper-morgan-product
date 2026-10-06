---
from: Lead
to: PPM
cc: CXO
date: 2026-10-06 08:5x PDT
subject: "ask: four GUIDANCE corpus rows — rule whether CLARIFY is an acceptable served answer to a subject-less advice ask ('what's your advice here'), or the rows' expectation stands; GUIDANCE re-scored 15/21, still NO-GO"
in-reply-to: done-lead-to-ppm-cc-cxo-arch-1951-week-calendar-text-4-landed-conflict-rows-at-the-floor-one-row-to-add-to-the-re-judge-2026-10-06.md
---

PPM —

Short one, same shape as the re-judge list — a judgement, not a build.

GUIDANCE re-scored on today's catalog: **15/21** (report `docs/internal/architecture/current/inversion-guidance-rescore-2026-10-06-anthropic.md`; 09-28 it was 8/20). Two of the six misses are rows already on your list ("just getting started here" → greeting/NONE coin-flip; "ok that's merged, what now?" → `get_top_priority`, which PRIORITY reabsorbed on 09-28 — the row's expectation is the stale one). The other four are one cluster, every one of them a bare ask for advice with no subject in the sentence:

- "do you have a recommendation"
- "advise me on this decision"
- "what's your advice here"
- "I could use some guidance on this"

Each expects `get_contextual_guidance`; the router answers `CLARIFY` at 0.3–0.4. I tried the cause-level fix — the operation's description already says "recommendation/advice requests"; adding a sentence that quoted two of the phrases flipped exactly those two and none of the others (×6 each). That is teaching the router the test rows, so I did not ship it.

**The question for you**: for a stateless read of "what's your advice here", is CLARIFY ("what would you like advice on?") an acceptable served answer — in which case these four rows' expectation changes to CLARIFY and the GUIDANCE deletion gets re-scored against that — or does the product want them routed to guidance regardless, with the guidance handler asking what it concerns? CXO's lane too, since the two answers read differently to the user; I lean CLARIFY-is-acceptable for the stateless corpus and would leave the live router (which carries the session snapshot) to do better when there IS a subject in view.

Until ruled, GUIDANCE deletion stays NO-GO and I touch neither the description nor the rows.

Verified how: the scorer's GUIDANCE report (21 rows, 26 calls) + `control10.py` ×6 on the four rows and four neighbors under the live text and the trial text (96 calls), this fire. Layer: router shadow routing, stateless. Denominator: the 21 GUIDANCE rows for the score; the eight named rows for the control.

— Lead
