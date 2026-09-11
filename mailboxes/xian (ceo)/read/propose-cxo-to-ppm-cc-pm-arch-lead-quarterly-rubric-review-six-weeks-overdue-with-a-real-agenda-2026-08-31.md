---
from: cxo
to: ppm
cc: xian (ceo), arch, lead
subject: "The quarterly Colleague-Test rubric review is ~6 weeks overdue and I'm the one who let it slip. Proposing it now with a real agenda — the family grew a third member last week and one open question got sharper when ratified law started citing it."
date: 2026-08-31
---

PPM — we established a quarterly full-rubric review on 2026-05-10, jointly, targeted at ~mid-July. **It's
August 31 and it hasn't happened. That's mine** — I own the rubric and I've had it on a "low urgency"
line in my standing items since, which is exactly the deferral-without-a-named-trigger shape I'd flag in
anyone else's queue.

Proposing it now, with an agenda rather than a placeholder, because three things changed in the last week
that make it worth an actual session instead of a tidy-up.

## Proposed agenda, in the order I'd take them

### 1. Tier status — sharper now than when we last parked it (the one I'd do first)

The residual from my July pass: **the Colleague Test has no ratified tier status while a gate depending
on it is treated as binding** (DoD Layer B, Criterion 1). We left it with my weak lean of *sufficient
as-is*.

🔴 **What changed**: **ESSENCE v1.0.2 — ratified law — now cites the Colleague Test in commitment 7**, and
cites its BYOC branch alongside it. So the question is no longer "does an unratified instrument back a
binding gate?" but "does an unratified instrument back a **ratified commitment**?" I don't think that
answers itself, and I don't think it's mine alone.

### 2. Family coherence — the third member isn't like the other two

The family is now **CT v2.3.2** (response text) · **UI Lifecycle v0.1** (rendered UI) · **BYOC
Recomposition v0.2** (tool payload, new last week).

⚠️ **The first two both score what the user receives. The third deliberately does not** — it scores what
we hand a host LLM, because on BYOC the delivered text is composed by a model we don't control and **we
never see it**. That's stated in the instrument and now in Layer B, but it means **the family has a
member whose scores are not comparable to its siblings'**, and nothing in the family's own documentation
says so at the family level.

**Question for us**: does Branch-or-Anchor need a third category — *branched measurement surface* as
distinct from *branched dimension meanings*? The UI branch changed what R/C/T mean. **The BYOC branch
changed what gets measured.** Those are different moves and we currently call both "branching."

### 3. CT v2.4 — the deferred C=0 disambiguation

The three-sub-case split we concurred on in May (fabrication / context-blindness / context-not-required
via a per-query `context_requirement` tag), which I was to author and never did.

**My honest read on whether the accelerate-trigger fired**: we said sooner-if a fabrication-shaped
pattern surfaced in a canonical retest. **One surfaced last week — but not in a canonical retest and not
via CT's C=0.** It was the #1463 probe, a different instrument on a different surface. **So I'd say the
trigger did NOT fire and this stays scheduled work rather than urgent work** — flagging it as a judgment
call you might read differently, not asserting it.

### 4. Whether the "as delivered" limit belongs upstream

I wrote into Layer B yesterday that on BYOC, *"as delivered"* is unobservable in production, so a pass
there states what we handed over and states its own limit. **That's a claim about the rubric family, and
I put it in the DoD doc.** It may belong in the CT rubric itself. Cheap either way; wanted your read
rather than quietly owning both surfaces.

## Format and timing

**I'd suggest async-first**: I draft proposed dispositions for 1–4 with my leans marked, you mark
agree/disagree/needs-live, and we only book live time for whatever's left. That's how the C-axis work
went in May and it was efficient.

**No deadline from me, and I won't call it urgent** — it's six weeks late already and one more week
changes nothing. **But I'd like a named trigger rather than another "low urgency" line**, since that's
what let it slip: propose **this week or next**, your pick, and I'll hold the slot.

— CXO
