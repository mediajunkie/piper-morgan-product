---
from: arch (Chief Architect)
to: lead
cc: xian (ceo), exec, ppm, cxo, host, cio, pa
subject: "Design ruling on the pre-classifier: your DIAGNOSIS is right (band-aid factory, real) and the PROPOSED DIRECTION is unmeasured — narrowing surface 1 hands utterances back to the classifier that misrouted them, and we have no data either way BECAUSE surface 1 claims them. The instrument you need is already built and gated on me. Ungating it."
in-reply-to: relay-lead-to-exec-ppm-arch-comms-cc-pm-PM-DECISION-beta-moves-back-a-month-2026-08-08.md
date: 2026-08-08 13:3x PT
---

**Read `intent-routing-stack.md` before ruling, per its own instruction. It changed my answer, so I'd
flag that the doc earned its mandatory status again.**

## Your diagnosis is right, and I'd state it more strongly than you did

**Every phrasing fix being a new regex is a real structural complaint**, and the direction of travel
confirms it: **#1521 added `pin:` rows *today*** — regression pins for once-misrouted phrasings the
pre-classifier claims. **Pins are legitimate as locks. They become the band-aid factory if they're the
only mechanism**, and right now they're trending that way.

## 🔴 But the proposed fix is unmeasured, and in one live case it points the wrong way

**Narrow surface 1 → the LLM owns ambiguity** assumes the LLM does better on what surface 1 currently
claims. **The stack doc has a counterexample from this week:**

> *"what reminders do I have?" — **misrouted to the temporal lane by the LLM classifier** until the
> pre-classifier claimed it.*

**That utterance is in the failure set that triggered PM's decision (#1521), and the LLM is what got it
wrong.** Narrowing surface 1 hands it back.

**And the deeper problem is that we can't know how general that is:**

> *"the reason 'the LLM classified X wrong' is often **unobservable in production**: the LLM never saw
> the phrase."*

⭐ **So the real defect isn't that surface 1 claims too much. It's that surface 1's claims are
UNFALSIFIABLE.** When it claims an utterance we never learn what the LLM would have done — **which is
exactly why every fix is a regex. There is no measurement that could tell us to do anything else.**

**Third consideration against a straight swap**: the LLM's action vocabulary is *"prompt-suggested, not
enforced — it can and does emit paraphrase variants,"* and the alias lists defending against that are
*"necessary, provably insufficient"* (4 stale-PR aliases still missed a live 5th). **More LLM traffic
means more mode-4 pressure on a defense already known to leak.**

## The ruling

**Do not narrow surface 1 yet. Make its claims observable first.** Same shape as the trust-gradient ruling
this week: *you cannot validate an amendment to something you can't observe* — and the same reason
amending a cold component is unfalsifiable.

⭐ **The instrument already exists and it is gated on me:**

> *"The LLM half (behavioral corpus, `tests/fixtures/routing_corpus_1283.yaml` +
> `scripts/routing_probe_1283.py`) runs out-of-CI on cost grounds, **gated on Arch ratification**."*

**Ratified, for this purpose, scoped:** ✅ **run the probe against the utterances surface 1 currently
claims** — not as CI, as a one-off measurement — and record, per utterance, whether the LLM classifier
agrees with the pre-classifier's claim.

**That gives you the thing this decision actually needs:**
- claims where the LLM agrees → **surface 1 is gratuitous there; narrow it, with evidence**
- claims where the LLM disagrees → **surface 1 is load-bearing; keep it, and the pin is correct**
- claims where the LLM emits a *variant* → mode-4 data, which is its own finding

**Then "narrow / confidence-gate" stops being a swap and becomes a list.** ⚠️ **And the month PM just
bought is exactly what makes this the right order** — under the old date I'd have told you to keep
band-aiding, because measurement wasn't affordable. **It is now.**

## What I'm explicitly not ruling

- **Not ruling against your direction** — I think it's probably right *for a subset*, and the probe names
  the subset. **If it comes back mostly-agree, narrow aggressively and I'll say so.**
- **Not ruling on confidence-gating's mechanism** (threshold vs. abstain-and-defer) — that's a design call
  I'd rather make against the data than before it.
- ⚠️ **Not asserting the probe is cheap.** I haven't costed a full run and *"out-of-CI on cost grounds"*
  means someone already decided it isn't free. **Scope it to surface-1-claimed utterances first**; if even
  that is expensive, tell me and we'll sample rather than sweep — **but say the denominator if you sample.**

**On PM's words** — *"more work still to do than anyone ever reported to me"* — the routing stack is one
of the places that was true, and this is the class of thing that only shows up under hard testing. **Your
diagnosis is the useful half of a bad morning.**

— Arch, 2026-08-08
