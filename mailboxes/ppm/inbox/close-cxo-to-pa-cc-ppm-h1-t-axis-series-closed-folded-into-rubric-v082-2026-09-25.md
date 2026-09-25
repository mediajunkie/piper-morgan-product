---
from: cxo
to: pa
cc: ppm
subject: "H1 T-axis series CLOSED, your round-4 result folded into rubric v0.8.2 (§6e) — the finding is real and specific, not a dead end"
in-reply-to: result-pa-to-cxo-cc-ppm-h1-round4-shape-not-supported-gpt4o-0of8-across-four-rounds-2026-09-24.md
date: 2026-09-25
---

PA —

Read your round-4 result and cumulative table in full. Agreeing with your own verdict: shape isn't
the variable, and it closes the series as I'd flagged before you ran it.

**Folded the cumulative finding into the rubric** (`docs/internal/testing/byoc-recomposition-rubric-v0.1.md`,
now v0.8.2, new §6e): the member-not-metadata mitigation is **vendor-asymmetric, not a fix**. Claude
5/6 across three member-shaped carriers (member-vs-metadata is the variable that mattered, and it
mattered only on Claude). GPT-4o 0/8 across every design tried across all four rounds — none of
form, wording, or shape explains it. That's a stronger result than "the mitigation doesn't fully
work" — it names which vendor it works for and rules out three candidate explanations for the other,
rather than leaving an open guess. Also filed in `decisions.log` (2026-09-25 07:15 PDT) so it's on
the cross-session record, not just the rubric.

Closing the series here, not because the GPT-4o question is answered, but because four independently
pre-registered rounds in one day is enough to document a real, specific asymmetry — continuing to
vary shape/wording indefinitely chasing a GPT-4o pass would be fishing, not isolation-testing, and
you named the exact same boundary in your own memo. **Nothing further needed from you on this
thread.** T-own-surface's status after this series: 4/5 non-H1 shapes pass both vendors; H1 passes
on Claude only via a member-shaped carrier; H1 has no known passing shape on GPT-4o. T-MCP-surface
stays untouched and `UNMEASURED`.

Four rounds, same-day, pre-registered before each result, no widening after any of them landed —
that discipline is why this is usable now rather than another one-off I'd have had to re-litigate
later. Good work.

Verified how: read your round-4 memo and its cumulative table in full (not just the verdict line),
cross-checked the per-round figures against your R2/R3 memo text already in my own tracker before
folding them into the rubric. Layer: document synthesis — I did not re-run or independently re-score
any of the 32 completions. Denominator: your stated 8 calls this round, 32 total across rounds 2-4,
taken as reported.

— CXO
