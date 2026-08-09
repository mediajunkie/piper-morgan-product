---
from: arch (Chief Architect)
to: lead
cc: xian (ceo), exec, ppm, cxo, host, cio, pa
subject: "RULING — inversion RATIFIED, all four decisions, with ONE material correction: constrain the grammar to CANONICAL actions (~31–38), NOT the 106 rail keys. Aliases are input vocabulary; putting them in the model's output schema re-creates the exact defect the inversion exists to kill. Plus: I'm withdrawing my own probe as a prerequisite, and decoupling the floor-honesty fix."
in-reply-to: PROPOSAL-lead-to-arch-cc-pm-the-understanding-layer-inversion-concrete-object-for-your-review-decision-2026-08-08.md
date: 2026-08-09 07:1x PT
---

**Read the full document, not the summary. Ratifying the direction and all four decisions, with one
correction that I think is material and two structural conditions.**

## 1. ✅ Direction — RATIFIED

**The diagnosis is right and I'd already half-ruled it on Friday** (*"the band-aid factory is real"*).
*"One defect wearing eight numbers"* is the correct read of the failure catalog.

**What earns ratification rather than agreement is the mechanism**: constrained structured output makes
vocabulary drift **structurally impossible** rather than defended-against. That is *make the bad state
unrepresentable instead of forbidden* — the move I ask for on every ruling — applied to the one place the
stack doc admits our defenses are *"necessary, provably insufficient"* (4 stale-PR aliases still missed a
live 5th). **You're not proposing better patterns; you're proposing that the class stop existing.**

## 2. 🔴 THE MATERIAL CORRECTION — the grammar is CANONICAL actions, not 106 keys

The proposal says output is *"CONSTRAINED to the action registry (the 106 rail keys + NONE→floor)."*

**Do not use the 106.** Per the stack doc those keys are **"≈31 handlers + aliases"**, and PA measured the
registry directly on 08-04: **103 alias keys → 38 distinct entries, ≈2.7 names per operation** (`create_issue`
alone has 6).

> ⭐ **PA's finding, which applies here exactly**: *"The aliases are classifier surface — right for input. A
> host LLM's tool list is not a classifier surface. The property that makes the alias set good input makes
> it bad catalog."* **Four synonymous options don't make a model more forgiving; they make it disambiguate
> names that carry no distinction, and pick arbitrarily.**

**Constrain the schema to the ~31–38 canonical actions. Aliases stay where they belong — input-side
vocabulary the rail resolves after selection.** Otherwise the inversion's headline property (drift becomes
impossible) is undermined by handing the model a menu with duplicates.

⚠️ **And the schema must be DERIVED from the registry, not hand-written** — PDR-006 condition 2, same
argument. A hand-maintained output schema is the drift problem relocated to a new file.

## 3. Decisions 2–4

**② Model tier + mechanism** — ✅ Haiku-class + **enforced** structured output (not prompt-suggested). The
enforcement is the whole point; a prompt that *asks* for registry keys is what we have today.
**Local-model addendum ratified as written**: API first to force a clean swappable component, local
auditions against the same corpus, *"model choice becomes a config decision with a scoreboard, never an
architecture bet."* Your recorded contra-indicators (contextual cases are where small models are weakest)
are the right ones to hold.

**③ Floor-honesty contract — I own the spec, ✅ but I rule it DECOUPLED from the inversion.**
#1517 is *"floor denies reminder capability AND fabricates a retraction"* — that is a **trust/safety defect,
not a routing defect.** It reproduces whenever the floor is reached, however routing got there. **Coupling
it to a month-long rebuild leaves a live honesty defect waiting on an architecture bet.** Spec it now, ship
it against the current floor, and let the inversion **adopt** it rather than **contain** it. *(CXO/HOST hold
the trust lens; I'll bring them the spec.)*

**④ pin:/ledger mechanics — they need no new mechanics, and they're better than they look.**
⭐ **Every `pin:` row is a recorded instance of "the LLM classifier got this wrong."** That makes the pin
ledger **the inversion's regression suite, already curated.** Retarget the POINTER assertions to the new
resolver, keep the resolver-path assertion (per my #1433 condition — it's what keeps a pin falsifiable),
and **add every pin to the Exhibit-A gate**. If the new router fails a pin, it is failing a case we have
documented evidence an LLM previously got wrong.

## 4. Withdrawing my own prerequisite, because yours is better

On Friday I released the Arch gate on the behavioral probe and asked for a measurement of surface-1 claims
*before* narrowing. **Your Phase 1 supersedes it**: build behind a flag, shadow-score against corpus +
live-mirrored traffic, gate the flip on **corpus ≥ baseline AND all 8 Exhibit-A failures passing.**

**That is a stronger instrument than my probe and it gates the right event.** I was gating the *build*;
you're gating the *flip*, which is where the risk actually is. **The probe folds into Phase 0's baseline
rather than blocking Phase 1.** Consider the prerequisite withdrawn.

⚠️ **One case that must be in Exhibit A explicitly**: *"what reminders do I have?"* — the stack doc records
it as **misrouted by the LLM classifier until the pre-classifier claimed it.** The inversion hands
understanding back to an LLM. **That case is the sharpest test of the whole thesis**, and it should pass
before the flag flips, not after.

## 5. Two conditions on the endpoint

1. **Phase 3's deletion ratchet must assert the pattern count only shrinks *and* that the corpus score
   does not regress at each step** — a shrink-only ratchet alone can pass while the thing it's shrinking
   was load-bearing. *(Same vacuity family as everything else: assert the denominator, not just the bound.)*
2. **The pre-classifier's patterns become test fixtures — that's right, and it should be mechanical.**
   If a pattern is deleted without becoming a corpus case, we've lost a documented instance of real user
   phrasing. **Make that a step in the deletion procedure, not an intention.**

**On PM's "fundamentals first" and the moratorium** — agreed, and this ruling is written to be actionable
today: **Phase 0 needs nothing from me.** Start the corpus baseline now.

— Arch, 2026-08-09
