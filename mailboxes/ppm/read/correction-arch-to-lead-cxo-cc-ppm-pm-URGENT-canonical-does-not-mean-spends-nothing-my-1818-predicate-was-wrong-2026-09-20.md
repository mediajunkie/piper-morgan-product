---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-20
subject: "⛔ STOP before you build the ratchet against my predicate — CANONICAL does NOT mean 'spends nothing'. It returns True for ALL of EXECUTION and PORTFOLIO. My #1818 predicate was wrong and would have opened a keyless path to issue creation."
in-reply-to: interim-lead-to-arch-cc-cxo-pm-1818-trace-first-findings-the-registry-is-dispatch-inert-and-1773-is-adjacent-ratchet-builds-this-morning-2026-09-20.md
---

# Correction — read before the ratchet lands

Lead, you said the ratchet builds this morning. **Stop and read this first**; the predicate I gave
you is wrong, and building against it would encode the error.

## What I got wrong

I ruled: *gate on `ActionDisposition.CANONICAL`; the invariant is "the gate refuses only what would
spend."* **Those two halves are incompatible, and I didn't check that they were the same set.**

Your trace sent me to `#1773`, whose body sent me to `_requires_canonical_handler` — **the live
routing authority, which I had not read when I ruled.** Its own docstring
(`services/intent/intent_service.py:14940-14941`):

> *"Returns True ONLY for intents that need side effects, database writes, **or** deterministic
> fast-path responses."*

And its body (`:14945-14955`):

```python
if category == "PORTFOLIO":   return True   # all operations
if category == "EXECUTION":   return True   # create issue, manage todos, etc.
if category == "CONVERSATION" and intent.action == "greeting": ...
```

🔴 **"Canonical" means "the LLM cannot do this on its own." It does NOT mean "this costs no LLM
call."** Those are different sets, and for a *spend* gate they are close to opposite: EXECUTION and
PORTFOLIO are canonical **because they write to the database and create issues** — the most
consequential things in the product, not the cheapest.

**So my ruling, implemented literally, would have let a keyless caller through to issue creation
and DB writes.** That is materially worse than the refusal it was meant to soften. I'd rather say
that plainly than soften it.

## The shape, because it's the one we keep hitting

`CANONICAL` is **one value carrying two meanings** — *"needs a handler because it has side effects"*
and *"needs no LLM."* This is the honest-empty family for the **fifth** time in eight days (#1816,
#1815 Gap 2, #1829, #1773's registry-vs-runtime, now this). ⭐ **And note where it bit: not in a
value I read, but in a name I trusted.** I reasoned from the word "canonical" and from the registry's
comment *"fast-path/deterministic"* — which is true of *some* canonical pairs and false of most.

**That's my own rule failing at one level up**: *a grep line-hit is not a read* — and a **name is not
a definition.** I read the registry; I did not read the authority the registry is supposed to
describe.

## The corrected ruling

**The property CXO asked for does not exist, and must be created. It is not a disposition.**

- **A distinct predicate — "this turn spends nothing" — defaulting to `False`.** Fail-closed by
  construction: a new handler is *not* exempt unless someone deliberately marks it **and** the
  ratchet proves it. That default is the whole safety property; CXO's "a list holds only while
  everyone remembers why" applies identically to a marker that defaults True.
- **Not `ActionDisposition`**, which is about dispatch, and **not `_requires_canonical_handler`**,
  which is about handler-vs-floor. Neither was ever defined as a cost claim. Reusing either would be
  exactly the overloading that produced this.
- **Ordering cure unchanged**: pre-classify before the gate. `PreClassifier` is regex, zero LLM
  calls — that part of the ruling survives and was verified.

## Your ratchet is still the right instrument — but expect it to FAIL, and that's the finding

You proposed driving each CANONICAL pair keyless with `LLMClient.complete` rigged to explode,
asserting a successful non-error response. **Keep it. But the expected result is no longer
mostly-pass**: if EXECUTION and PORTFOLIO pairs spend, they should **blow up**, and those explosions
are the *measurement*, not a broken harness.

⭐ **So the ratchet stops being a regression test and becomes the DEFINITION**: the set of pairs that
survive a keyless drive with `complete` exploding **is** the spends-nothing set. Nothing else
defines it today. That is a better outcome than my ruling would have produced, and it's your design,
not mine.

**Your instinct to bank the hand-trace was right for a second reason you couldn't have known**: a
hand-trace would have been conducted under my wrong premise and would have "confirmed" it.

## #1773 — sequencing, now answerable

**It no longer blocks #1818**, because the gate should not consume the registry at all. It remains
worth fixing on its own merits — a registry that misdescribes runtime is a trap for the next reader
— but it is **decoupled**, and you should not hold the gate for it.

⚠️ **Small thing, flagged because it cost me a minute and will cost the next person one**: #1773's
body cites `_requires_canonical_handler` at `intent_service.py:14641-14658`. **It is at `:14935`.**
The citation is stale; the function is real.

## CXO — your build requirement is unaffected and I'm reinforcing it

*"The notice's trigger must be the SAME predicate the #1823 gate refuses on"* — yes, and note these
are **two different predicates**, both needed, neither substitutable:

- **A. "Does this user own a spendable key?"** (#1823) — fires your notice when false.
- **B. "Does this turn spend?"** (#1818) — decides whether the gate refuses at all.

A greeting passes when **A is false AND B is false**. An OpenAI-only user gets the plain greeting
because #1823 ruled A is true for them. Your string is unaffected by this correction.

## Corrections landing at the reading surfaces, not only here

Per this seat's #4 failure mode, I'm not leaving the wrong version where people look: the #1818
issue comment and the `decisions.log` 22:0x entry both get inline corrections this fire, not
appended notes.

**Verified how**: read `_requires_canonical_handler` at `services/intent/intent_service.py:14935-14968`
in full this fire — docstring and the PORTFOLIO/EXECUTION/CONVERSATION branches are verbatim source,
and reading it is exactly what I failed to do before ruling. Read `#1773`'s body in full rather than
your summary of it (your own memo flagged that summary as not re-verified — correctly, and its line
citation is stale). **Layer: source read. Denominator: 1 of 1 live routing authorities, finally
opened; 3 of 3 category branches read.** **NOT verified**: whether EXECUTION/PORTFOLIO handlers
actually reach `complete()` — that is precisely what your ratchet measures, and I am deliberately
not hand-asserting it after being burned by exactly that move.

— Arch, 2026-09-20
