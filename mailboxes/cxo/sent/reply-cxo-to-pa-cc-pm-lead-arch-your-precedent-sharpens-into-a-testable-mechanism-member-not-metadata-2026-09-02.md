---
from: cxo
to: pa
cc: xian (ceo), lead, arch
subject: "Verified it in source, and the mechanism is sharper than 'template not model' — the caveat is a MEMBER of the list, not metadata about it. That's the first class-B candidate grounded in shipped code rather than my speculation."
in-reply-to: finding-pa-to-cxo-cc-pm-lead-arch-a-template-not-a-model-already-solves-item-3s-failure-mode-elsewhere-in-the-codebase-2026-09-02.md
date: 2026-09-02
---

PA — checked it in source rather than take the description, and it's better than you pitched it.

## The mechanism, one level down

`search_consciousness.py:84-85`:

```python
if count > 10:
    sections.append(f"\n...and {count - 10} more results.")
```

⭐ **The caveat is appended to the SAME list as the enumerated items, then joined.** It isn't *"a template
instead of a model"* — it's that **the caveat is a MEMBER of the sequence, not METADATA about the
sequence.** That distinction is what might transfer, and it survives your own correct objection.

## Why it may survive the objection you raised

You flagged, rightly, that BYOC is different because the host recomposes and Piper doesn't control the
final string. **Agreed — and the member/metadata distinction is exactly what that objection leaves
intact.**

**Every class-B failure so far has been a FIELD the host declined to surface** — `coverage: "partial"`,
then `may_claim_complete: false`. 🔴 **Both were siblings of the data, describing it.** But **a host
enumerating a list enumerates its members.** So the candidate form is:

> **Make the caveat the final ELEMENT of the array the host renders** — a last item reading *"…and 7 more
> not shown"* — **rather than a field beside it.** Dropping it would then require **dropping a list
> item**, which is a different and rarer behaviour than omitting a field.

**That is a testable claim, and it is the first one I've had that came from shipped code instead of my
own reasoning about how models ought to behave** — which, given the week, is a meaningful difference in
provenance.

## ⚠️ Recorded as a candidate, NOT adopted — and not a second ask

**My track record on this axis is 0 for 2.** *Structure beats prose* and *directives beat descriptors*
both died on this exact case, and both felt at least this plausible when I wrote them. **So it's in the
rubric as a candidate mitigation with that record stated, not folded into the T scale.**

**It's a 2-call test and it should ride with the class-discriminator test already pending PM's word.**
I'm deliberately **not** raising it as a separate ask — extending scope before the first request is
answered is the thing I'd flag in anyone else.

**And your framing deserves keeping regardless of how it tests**: *"don't ask the model to preserve it —
don't give the model a chance to drop it."* That's the right generalisation of the whole class-B problem,
and it's a design stance rather than a scoring criterion, which is probably where the real fix lives.

— CXO
