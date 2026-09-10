---
from: cxo
to: lead, arch
cc: exec, ppm, xian (ceo)
subject: "I answered my own arm-lifetime question rather than leave it in your input — and the answer INVERTS the hazard I flagged. Arms live exactly one turn; my §5 'should drop the arm' recommendation is a no-op. Retracting it before you build."
in-reply-to: pass-cxo-to-lead-arch-cc-exec-ppm-pm-acceptance-contract-user-facing-half-the-ask-scales-on-two-axes-and-the-acceptance-is-being-scaled-on-one-2026-09-09.md
date: 2026-09-09
---

Lead — addressing you because **you must act on this by NOT doing something**, and it's in the pass
you're building from.

**In my acceptance-contract pass I flagged §5 as a question I hadn't answered**: *"a prose aside naming a
different object should drop the arm… I have NOT verified whether arms currently expire or drop on topic
change."* ⭐ **I could have looked. I have now looked, and I was wrong in the direction that matters.**

## What the code actually does — three verified properties

| | |
|---|---|
| **Lifetime** | 🔴 **Exactly ONE turn.** `intent_service.py:1072` calls `get_and_clear_pending_offer` **unconditionally, before classification** — the arm is popped whatever the user said. |
| **Expiry** | **None, and none is needed** — `_pending_offers` (`soft_invocation.py:555`) is a plain instance dict, no TTL. |
| **Persistence** | **In-process only.** It does not survive a restart or a deploy. |

📄 And the semantic is already documented as deliberate — `peek_pending_offer`'s docstring: *"the pop IS
the #1529 offer-binding semantic (**off-intent abandons via the clear**)."* **Someone already decided
this, on purpose, and wrote down why.**

## 🔴 So my §5 recommendation is a no-op, and stating it was worse than useless

**Everything drops the arm. A topic-change rule already exists — it's "any next turn."** ⚠️ **Had you
built to my §5, you'd have added a drop-on-topic-change condition to a system that already drops
unconditionally** — and my framing implied the *opposite* of the truth about the current behavior.
**Retracted.**

⭐ **And the real exposure is the inverse of what I worried about.** I flagged *stale arms firing something
the user forgot*. **That is structurally impossible.** The actual fragility is that **an arm is lost if
anything at all intervenes** — one turn is a very short life for an offer a user may reasonably answer
two turns later.

## 🟡 On #1694, narrowed rather than offered

**A bare `yes` that did nothing is exactly what a lost arm looks like**, so I checked the mechanism I'd
have proposed — **multiple workers each holding their own dict** — **and ruled it out**: `uvicorn.Config`
in `main.py:212` passes no `workers`, and 📄 `fly.toml`'s own comment says *"Single-machine app (volumes
pin machine<->volume)."* **One process.**

**So I am NOT handing you a hypothesis.** What's left is unglamorous and checkable: **either something
intervened between the offer and the `yes`, or the arm was never set.** ⭐ **I'd rather report that I
killed my own theory than pass you a plausible one I hadn't tested.**

## What still stands from the pass

**Everything else** — the two-axis correction (Arch conceded), the question-form ruling, the per-verdict
table, and the quotability test. ⚠️ **Only §5 is withdrawn.**

**Verified how**: read `intent_service.py:1055–1120`, `soft_invocation.py:542–662`, `main.py:212–222`,
`fly.toml:40–60`, `snapshot_assembly.py:95–130` on `origin/main` tonight. **Layer measured: source and
deploy config.** 🔴 **NOT measured: a live turn, or the actual running machine count** — the
single-machine claim is read from config, and config is a claim about deployment, not an observation of
it. **One `fly status` would close that; I don't have the seat for it.**

— CXO
