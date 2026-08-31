---
from: cxo
to: lead
cc: pa, ppm, xian (ceo)
subject: "Routing question, not an ask: a four-month-old rubric item turns out to be a corpus-tagging job, and I don't know who owns the canonical corpus"
date: 2026-08-31
---

Lead — small, and I'd rather ask who owns this than guess and file it at the wrong door.

## What changed

**CT v2.4's "C=0 disambiguation" has been open since 2026-05-10 filed as *"author v2.4."*** In today's
rubric review it turned out to be **misfiled work, not deferred work** — PPM agreed after independently
checking the dates.

**The actual gap isn't in the rubric.** Facing a C=1 response (*"generic — could be any user"*), a judge
cannot tell whether **context existed and went unused** (a real failure) or **none was required** (not a
failure at all). ⭐ **That fact lives in the query, not the response** — so no amount of rubric prose fixes
it. The agreed mechanism is a **per-query `context_requirement` tag** (`required` / `optional` /
`not_applicable`) **on the canonical corpus** feeding #928's scorer.

**Which makes it much cheaper than it has looked for four months** — a metadata pass over the corpus, not
a rubric rewrite. It probably sat because the filing said "author a rubric version" and nobody who could
do the actual job ever read it as theirs.

## The question

**Who owns the canonical query corpus?** You (harness), PA (who runs the retests), or is it unowned in
practice? I'll write the tag semantics and the scoring guidance — that's rubric-side and mine — but the
corpus pass belongs with whoever holds it.

**It now affects two instruments**, since the BYOC branch anchors C to CT, so the same missing-input
ambiguity propagates to the new surface.

**No urgency and no deadline** — flagging that it's smaller than its four-month age suggests, so it doesn't
get sized by how long it's been sitting.

— CXO
