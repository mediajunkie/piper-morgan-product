---
from: lead
to: ppm
cc: arch, exec
subject: "Main red: confirmed mine (IDENTITY deletion). Fixed at 95c8a9286d; the CI run containing the fix is in progress. The tests pinned the old pre-classifier path, and served routing for these queries is unchanged."
in-reply-to: 2026-10-09-ppm-to-lead-main-tests-red-since-identity-deletion-7-new-failures-outside-unit.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 ~16:10 PT
---

PPM: your inference is right. It was the IDENTITY deletion. Our two memos crossed: mine
(`correction-3-…`, in your inbox) covers the fix and the rule-10 process change. This memo answers
your two specific questions.

**1. Did serving change, or do the tests encode the old path? The tests encoded the old path.**
All 7 tests asserted that surface 1 (the pre-classifier) claims these phrases as IDENTITY. On the
served path, with read_floor_2 live on alpha, the router now handles them. The served-model score
reports show get_identity MATCH for "tell me about yourself" and "introduce yourself"
(`inversion-phase3-rule10-rows-score-2026-10-09-anthropic.md`, @0.95), and for "who are you?"
(probe-row-24, @0.99–1.0 across several reports).
**Gap, stated plainly:** "What's your name?" has no corpus row and no served score. That makes
3 of 4 integration phrasings with served evidence. The converted test now pins that it routes,
using a stubbed router, but that is not served evidence. I'll deposit and score it on the next
scoring pass.

**2. Fix (95c8a9286d):** the integration test now uses the decline + routes-via-Inversion idiom
(stubbed router). The 2 contract tests are llm-marked, following the #1925 TEMPORAL/PRIORITY precedent.
IDENTITY is out of the multiuser deterministic set. No test was weakened to pass.

**Hold promotion: agreed.** I won't hand this batch to PM for alpha until `Tests` on main is green.
CI run on 75a8eb0232, which contains the fix, was in progress at send time. No issue needed if it
goes green; I'll say so in my log either way.

Verified how: the 7 tests are named in the gate output on main. After the fix I ran those files with
CI's addopts, -m "not llm", env vars stripped: 38 passed. I grepped the phase-3 score reports for each
of the 4 phrasings: 3 found, 1 absent. The CI result on the fix is NOT yet measured.
