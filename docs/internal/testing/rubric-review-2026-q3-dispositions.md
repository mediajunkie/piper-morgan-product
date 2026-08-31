---
type: review-dispositions
review: Quarterly Colleague-Test rubric review, Q3 2026 (~6 weeks late; cadence set 2026-05-10)
participants: CXO (author), PPM (co-owner)
status: ✅ ALL FOUR AGREED by PPM 2026-08-31 (Arch concurred on item 1). Items 2 and 4 EXECUTED same day
  (CT rubric v2.3.3). Item 1 needs PM ratification; item 3 needs a corpus owner.
date: 2026-08-31
due: PPM's named trigger — Thursday 2026-09-03
last_updated: 2026-08-31
currency_claim: static once the review closes
max_age_days: 14
---

# Quarterly rubric review — dispositions

> ### ✅ OUTCOME, 2026-08-31 — all four agreed, two already executed
> **PPM agreed all four**, having read this doc in full and **independently verified item 3's date claim**
> (`git log -S"v2.2"` → v2.2 landed **2026-04-26**, genuinely before the 05-10 concurrence). Arch concurred
> on item 1. **No live time needed.**
>
> - **Items 2 and 4 — DONE same day**: CT rubric **v2.3.3** carries the third branch case (measurement
>   surface) and the canonical "as delivered" statement; DoD Layer B now points rather than restates.
> - **Item 1 — needs PM.** Ratification isn't mine or PPM's to grant.
> - **Item 3 — needs a corpus owner.** The `context_requirement` tag is corpus work, not rubric work.
>
> ⚠️ **PPM's noted edge on item 1, recorded here because a property named only in a memo is a property
> that disappears**: under the invariants/criteria split I can still freely rewrite dimension *criteria* —
> exactly the T=3 change I made on 08-30. **That is not "moving the bar" in the ratified sense, but it
> changes what earns points beneath a fixed bar, which has similar practical effect.** PPM explicitly did
> not want this fixed (gating criteria edits reintroduces the freeze problem) and notes git history gives
> the paper trail. **Known property of the split, not a silent gap in it.**

**Four items, my lean marked on each, in the order PPM agreed.** Async-first: mark each
agree / disagree / needs-live. Nothing here is decided.

---

## 1. Tier status — **PROPOSE: ratify the invariants, NOT the criteria**

**The question, restated with what changed**: the Colleague Test has no ratified tier status, while
things that *are* ratified depend on it — DoD Layer B Criterion 1 (a binding Done-gate) and now
📄 **ESSENCE v1.0.2 commitment 7**, which cashes "colleague" via the Colleague Test and its BYOC branch.
In July we left this with my weak lean of *sufficient as-is*.

🔴 **What makes it no longer sufficient, and it's a concrete thing I did:** on 2026-08-30 **I revised a
scoring criterion unilaterally** — falsified and rewrote T=3 in the BYOC branch on probe evidence. That
was good practice and I'd do it again. **But it means the bar for a ratified commitment is currently mine
to move, silently, on my own authority.** If commitment 7's meaning is "passes the Colleague Test," and I
can redefine passing, then I hold the pen on ratified law. **That is the gap — not a paperwork gap.**

⚠️ **And full ratification is the wrong fix.** Ratifying a 382-line rubric would freeze an instrument
whose whole value is that it improves when evidence contradicts it. Yesterday's falsification would have
needed a PM decision. That trades a real capability for a governance comfort.

**PROPOSED, and it is the smallest thing that closes the gap** — split the instrument the way ESSENCE
splits the repo:

| Ratified (PM; changes need PM) | CXO-editable (evidence-driven, no gate) |
|---|---|
| **The question**: *"Would a smart, capable PM colleague respond this way?"* | Dimension criteria and score bands |
| **The verdict shape**: three dimensions 0–3, **≥7/9 PASS**, **any single 0 auto-fails** | Worked examples, calibration notes |
| **The fabrication auto-fail** (C=0 for made-up data) | Branches, and their dimension meanings |

**Surface**: a `decisions.log` entry naming those three invariants — **not a PDR, not full-rubric
ratification.** Cheap, sufficient, reversible.

**Why these three specifically**: they are what a *citation* of the Colleague Test means. Everything else
is how we measure it, which should move with evidence.

---

## 2. Family coherence — **PROPOSE: yes, "branched measurement surface" is a distinct category**

PPM's early lean was that this is a difference in kind, not degree. **Agreed, and here is the sharper
reason**, which is about report legibility rather than taxonomy.

| Branch | Artifact measured | Comparable to CT's verdict? |
|---|---|---|
| **UI Lifecycle v0.1** | rendered UI — **still what the user perceives** | ✅ yes — both say "this is/isn't good for the user" |
| **BYOC Recomposition v0.2** | **the tool payload we hand a host** — *not* what the user perceives | 🔴 **no** |

⚠️ **The hazard is a sentence, and it is exactly the Apr 26 C-axis shape**: a Layer-B report reading
*"passed the Colleague Test family rubric, 9/9"* looks **identical** in both cases — while in one it means
the user's experience was good and in the other it means *we handed the host good material and never saw
what the user read.* Same vocabulary, different claim, converging on PASS.

**PROPOSED — two requirements that attach to this category and to no other:**

1. **A measurement-surface branch must state what its score does NOT claim**, in the instrument *and* in
   any report citing it. (My BYOC rubric §5 already does this — *"a 9/9 here means we handed the host
   everything it needed… not that the reply was good."* **Make that a requirement of the category, not a
   courtesy I happened to include.**)
2. **It must name its companion verification** — how the un-measured artifact gets checked. For BYOC
   that's the probe harness. **Without this the family silently loses coverage of the user's actual
   experience on that surface**, while every report still reads PASS.

**Note the asymmetry**: the UI branch needs neither, because rendered UI *is* user-perceived. The
requirements attach to proxies, not to branches generally.

---

## 3. CT v2.4 — C=0 disambiguation: **PROPOSE keep, reframed. ⚠️ I talked myself out of this and was wrong.**

**Recording the reasoning error, because it changes what the work is.** My first pass concluded v2.4 was
already solved by existing rubric text — the three sub-cases map cleanly onto current scores:

- fabrication → **C=0** · context-blindness (*"generic — could be any user"*) → **C=1** ·
  context-not-required → the **v2.2 fresh-account C=2 ceiling**

**That looked airtight, and it is wrong for a checkable reason: v2.2 predates our May 10 concurrence.**
We agreed v2.4 was needed *with the fresh-account ceiling already in the rubric.* So either we both missed
it, or the concern was never about rubric text. **It's the second** — the agreed mechanism was a
**per-query `context_requirement` tag** (`required` / `optional` / `not_applicable`) **on the corpus**,
not a rubric edit.

⭐ **The distinction matters and it's the whole item**: the rubric text distinguishes *response shapes*;
the tag supplies *query metadata a judge lacks*. Facing a C=1 response, a judge cannot tell whether
context existed and went unused (a real failure) or none was required (not a failure at all) — **because
that fact lives in the query, not the response.** No amount of rubric prose fixes a missing input.

**PROPOSED**: keep the item, **reframed as corpus-metadata work rather than a rubric rewrite** — which
makes it cheaper than it has looked for four months, and probably explains why it never got picked up:
it was filed as "author v2.4," and the actual job is tagging a corpus.

**One thing it now also affects**: the BYOC branch **anchors C to CT**, so the same missing-input
ambiguity propagates to the new surface. Two instruments, one fix.

**Accelerate-trigger check**: we said *sooner if* a fabrication-shaped pattern surfaced in a canonical
retest. One surfaced last week — **but in the #1463 probe, a different instrument on a different surface,
not CT's C=0 in a canonical retest.** 🔴 **My read: the trigger did NOT fire.** Flagging it as a judgment
call you may read differently rather than asserting it.

---

## 4. Where the "as delivered" limit lives — **PROPOSE: canonical in the CT family doc, pointer in Layer B**

Yesterday I wrote into DoD Layer B that on BYOC, *"as delivered"* is unobservable in production, so a pass
there scores the payload and must state its own limit.

⚠️ **That is a claim about the rubric family, and I put it in the DoD doc** — the surface that *consumes*
the family. It should be canonical in `development/colleague-test.md` with Layer B pointing at it.

**Reason, and it's a ratified standing rule rather than my preference**: 📄 ESSENCE — *"Derive, don't
hand-maintain: registries, catalogs, prompts, and manifests are generated from one source; **hand-maintained
copies are the documented failure mode.**"* Two prose statements of the same limit in two docs is the
hand-maintained-copy shape, and the copy in the consuming doc is the one that goes stale unnoticed.

**Cheap either way. I flagged it rather than quietly owning both surfaces.**

---

## What I am NOT proposing

- **No change to R/C/T dimension meanings in CT itself.** Nothing this quarter argued for one.
- **No new instrument.** Three is the right number; #2 exists to keep the third legible, not to add a fourth.
- **No PDR.** Every disposition above fits in `decisions.log` plus edits to docs we already own.

## Denominator

I re-read the C-axis and the branching discipline in full, and the DoD Layer B routing section. **I did
not re-read all 382 rubric lines this pass**, nor the worked examples, nor the UI Lifecycle rubric — so a
drift finding could be sitting in any of those and this review would not have caught it.
