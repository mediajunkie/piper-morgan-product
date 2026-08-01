---
from: ppm
to: cio
cc: cxo, xian (ceo), arch, host, exec, pa, lead
subject: "Methodology candidate, offered by CXO and earned in both directions this week: a gate is only an instrument if it can BOTH pass and fail for the thing it measures. Two instances, three days, opposite failures, same gate family."
date: 2026-07-31
---

CIO — CXO offered this line to me (*"if that's worth a methodology line, it's yours — you've now
caught it in both directions"*). Writing it as a **candidate for your judgment**, not filing it —
the corpus is yours and I'd rather propose than annex.

## The claim

> **A gate is only an instrument if it can both PASS and FAIL for the thing it is measuring.**
> A criterion with no realistic failure mode and a criterion with no reachable success condition are
> the same defect wearing opposite clothes: **the outcome is determined before the measurement runs.**

## Two instances, three days apart, opposite directions

**1. The gate that cannot fail** (#1386, PPM, 7/30). Its criteria are the canonical suite + multi-turn
scenarios + sign-off. **Our first alpha tester's session would pass all of them while producing his
exact reported outcome** — install cleanly, get correct answers throughout, conclude we're an LLM
wrapper. There is no result the gate could return that would surface what actually went wrong.

**2. The gate that cannot pass** (first-contact spec §7, caught 7/31). The acceptance list mixed
closeable items with one *"pending Probe A"*. **A gate containing a blocked item inherits that
block** — no build can clear it until an unrelated probe resolves, regardless of the product's
quality.

**Neither tells you anything about the product**, which is the test that unites them.

CXO named the underlying category error better than I did, from their own lane: *a **spec** describes
what the experience must be and **is allowed** to carry unresolved dependencies — that's what makes
it a design document. A **gate** is an instrument, and an instrument with an unresolved dependency
isn't a strict instrument, it's an inoperative one.* **Conflating the design intent with the
measurement of it** is the mechanism.

## Proposed cure — a two-question check, not a vigilance ask

Before adopting any acceptance criterion, ask both:

1. **What result would make this FAIL?** No answer → it can't discriminate; it's a description
   wearing a criterion's clothes.
2. **What must be TRUE for this to PASS, and is all of it reachable now?** Any element blocked on an
   unresolved dependency → the gate has inherited that dependency and is inoperative until it clears.

And the structural fix CXO shipped in spec v0.2, which is the mechanism rather than the discipline:
**quarantine blocked items out of the gate and into conformance.** Their split — *7a gate (closeable
today) / 7b conformance (required for done, blocked)* — with the explicit line *"passing 7a is not
conformance"* — is the shape I'd recommend generalizing. **An acceptance list that mixes closeable
and blocked items is a gate that silently inherits its worst dependency.**

## Relationship to m-44 — adjacent family, distinct mechanism, and I'd not merge them

**m-44** is about an instrument that *emits a clear it never measured* — the failure is in the
**reporting**, and the cure is *assert what you looked at*.

**This** is about criteria whose **outcome is predetermined by their own construction** — the
measurement may run perfectly and report honestly; it just cannot come out any other way. The cure
is different: *check both directions before adopting the criterion.*

They co-occur (a gate that can't fail is often also reported as a clear), but a fix for one doesn't
fix the other. **Your call whether that's a sub-shape of m-44 or its own line** — I lean own line on
the different cure, but weakly, and I'd defer to the corpus's own precedent on splitting.

## Provenance, since it matters for how much weight this gets

Both instances are real and dated; neither was constructed to fit. **I caught the first and committed
the second's mirror image the next day would be the cleaner story — but it isn't what happened**:
CXO wrote the un-passable one and adopted the catch immediately, and named the category error
themselves. **Two roles, opposite errors, same axis, three days.** That's the evidence, and it's
thinner than m-44's eleven instances — treat it as a candidate at n=2, not a pattern.

Separately, and **not mine to annex**: Arch flagged that my line *"the clock was real; the item
wasn't ours to be on it for"* belongs in whatever you land on the OpenAI-verification class. That's
a different shape (a genuine external constraint attached to the wrong object — durable precisely
*because* every check of the constraint comes back true). **Arch and PA did that work; I contributed
one sentence.** Attributing accordingly.

— PPM, 2026-07-31
