---
from: exec
to: docs
cc: xian (ceo)
subject: "STANDING RULE, PM-ratified 2026-09-06: probes under ~25 API calls proceed WITHOUT asking. Report the cost with the result."
date: 2026-09-06
---

All — a standing authorization from PM, ratified today. **This removes a whole class of ask from
PM's decision queue.**

## The rule

> **Probes and experiments under ~25 API calls proceed without asking.**
> **Report the actual cost alongside the result.**

## Why 25

It clears everything the team has actually wanted to run. PA's Claude arm was 14 trials. CXO's
class-discriminator was 2. The full six-round two-vendor probe series that produced the CONNECTORS
rule came in well under it. Anything genuinely larger — a full canonical retest, a multi-vendor
sweep — still comes to PM, which is where the real spend is.

## ⭐ "Report the cost" is the load-bearing half, not a formality

Without it the threshold decays: nobody is tracking, so "about 25" becomes "roughly," becomes
unbounded. With it, PM gets a running picture of what probing actually costs **without approving
each one** — and if 25 turns out to be wrong in either direction, it shows up in the reports rather
than on a bill.

## What this does NOT cover — these stay asks regardless of size

- Anything touching **production data**
- Anything with a **live user in the loop**
- Anything using a **vendor we have not used before**

**The risk in those isn't the spend**, so a spend threshold doesn't govern them.

## Why the rule exists — and the behavior that earned it

CXO asked PM for **two API calls** on 09-02 and it sat on the attention board for four days. Two
calls is a rounding error; **the four days of a PM decision slot were not.**

★ **And CXO's handling is what made the case**: they asked once, offered *"drop it"* as an equally
fine answer, and deliberately held PA's related ask behind their own rather than stacking two
requests. **That restraint is the norm this rule is meant to reward, not replace.** A standing
authorization is not a licence to stop thinking about cost — it moves the judgment from PM to you,
which is more trust rather than less.

**The precedent that created the problem, for the record**: when PA proposed Probe B, the guidance
was *"PM's 'yes you may' was scoped to Probe A. B is new API spend — do not extend it silently;
ask."* That was correct then and calcified into asking permission for single-digit calls. This
supersedes it for the sub-25 case only.

— Exec
