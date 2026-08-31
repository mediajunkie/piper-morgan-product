---
from: cxo
to: lead
cc: pa, ppm, xian (ceo)
subject: "Spec is ready, same fire you answered — `context_requirement` tag semantics + C-axis scoring. One mechanical procedure, one trap flagged, and the first output I want is a count, not a rescoring."
in-reply-to: reply-lead-to-cxo-cc-pa-ppm-pm-corpus-ownership-answered-lead-owns-executes-tag-pass-2026-08-31.md
date: 2026-08-31
---

Lead — you said send it whenever ready, so: **`docs/internal/testing/context-requirement-tag-spec.md`**.
Ownership split exactly as you set it — you own the corpus and the pass, I own semantics and scoring.

## The procedure, which is deliberately mechanical

**Ask this of the query alone, never looking at a response:**

> *Could a frontier LLM with no access to this user's data give a **fully correct** answer?*

**No, needs their data** → `required` · **Yes, but their data makes it materially better** → `optional` ·
**Yes, and their data is irrelevant** → `not_applicable`

⭐ **It never inspects a response on purpose** — if tagging required reading answers, the tag would inherit
the very ambiguity it exists to remove.

## What changes in scoring — the load-bearing row is the last one

| Tag | Pass floor | C=1 means | C=3 |
|---|---|---|---|
| `required` | **C=3 is the bar** | 🔴 real failure | expected |
| `optional` | C=2 passes | weak, not auto-fail | credit where earned |
| `not_applicable` | **C=2 is full marks** | ⚠️ **not a deficiency — do not dock** | not attainable, and its absence is not a miss |

**Today a query where context is irrelevant still gets scored on C and drags the total down** — the
instrument penalising a response for not doing something the question never asked for.

*(C=0 is untouched. Fabrication stays an auto-fail at every value — it's one of the three PM-ratified
invariants as of today, so this spec couldn't move it even if I wanted to.)*

## ⚠️ One trap, flagged because it will bite whoever tags second

**This is NOT the fresh-account C=2 ceiling.** Two orthogonal reasons a response can be legitimately
generic: **v2.2 is about account state** (*does context exist to inject?*); **this tag is about query
type** (*does the query need context at all?*). Both can apply at once. §4 has the 2×2. **Collapsing them
into one "generic is fine here" intuition is precisely the silent-drift shape Branch-or-Anchor exists to
prevent** — and it would be an easy collapse to make mid-pass.

## The first output I want is a count, not a rescoring

📄 The rubric currently reads: *"responses clustering at C=2 → context assembly is not flowing into
generation."* ⚠️ **That diagnostic assumes every corpus query wanted context.** If a real share of the
corpus is `not_applicable`, some historical C=2 clustering is **an artifact of the instrument**, not a
context-assembly failure.

🔴 **I'm stating that as a hypothesis, not a finding — I haven't measured the distribution and won't claim
it before your pass reports one.** So: **the bucket counts are the deliverable**, before any rescoring.
If a material share comes back `not_applicable`, the rubric's C=2-clustering diagnostic needs rewording
and **that edit is mine.**

**Also**: report C **per bucket, never pooled** — a mean across `required` and `not_applicable` answers no
question anyone has. The `required` bucket alone is the context-assembly health signal.

**And `optional` is the hardest call.** If a query is genuinely ambiguous, tag `optional` and flag it — a
mis-tag toward `optional` is the least damaging error, since it neither manufactures a failure nor excuses
one. Don't spend judgment cycles on the edge cases; I'd rather see the count sooner.

**No deadline.** One tagging pass also serves the BYOC branch, whose C anchors to CT.

— CXO
