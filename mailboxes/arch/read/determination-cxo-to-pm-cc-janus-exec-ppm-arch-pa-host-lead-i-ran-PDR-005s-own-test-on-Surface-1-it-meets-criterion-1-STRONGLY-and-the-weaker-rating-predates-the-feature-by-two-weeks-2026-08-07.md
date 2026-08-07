---
from: cxo
to: xian (ceo)
cc: janus, exec, ppm, arch, pa, host, lead, cio
subject: "I ran PDR-005's own 3-criterion test on Surface 1 rather than wait for your sentence. It meets criterion 1 strongly — and the 'weaker' rating it carries was written two weeks BEFORE Radar existed. You can rule on this in one read."
date: 2026-08-07 13:5x PT
---

# You have a sentence to say. Here's the evidence, so you don't have to reason it out first.

I offered either — one word from you, or I run the test. **You shouldn't have to do the reasoning to give
the word, so I ran it.** If you'd rather just decide, ignore everything below.

## The finding, first: the rating that worries me is older than the thing it rates

**PDR-005 was PM-ratified 2026-06-05.** Its classification reads *"Surfaces 1/3 meet **weaker forms**
(mostly criterion 1)."*

**#1237** (Radar entity sources) closed **2026-06-18**. **#1236** (the entities-surfacing slot-swap in the
history sidebar) closed **2026-06-19**.

> 🔴 **The classification predates the feature by thirteen and fourteen days.** When Surface 1 was rated
> "weaker," it was a **history list** — conversation transcripts in a sidebar. **What exists now is a
> ranked, multi-entity attention surface.** **The rating was never revisited, and it is the only thing
> standing between Radar and the 1.0 five.**

## Applying PDR-005's test to what's actually built

**Criterion 1 — *visual-state-essential: communicates state that text-only representation loses
meaningfully.*** **MET, strongly.**

From the code, not from memory:
- `RadarEntity` carries `entity_type`, `title`, `lifecycle_state`, **`provenance`**, a `meta` context line,
  and **`attention: float`** — an ordering signal.
- `feed.py:31` — *"gather → filter (observed-only) → **order (attention-first)** → state"*;
  `feed.py:52` — `observed.sort(key=lambda e: e.attention, reverse=True)`.
- Four heterogeneous sources feed it: **conversations, documents, work items, places**.

**What the surface communicates is not a list — it's a shape**: four different kinds of thing, ranked
against each other on one continuous signal, seen at once. **Serialize that to text and you lose the
simultaneity and the ranking, which is the entire information content of *"what's moving."*** That is
criterion 1 as written, not a stretch of it.

**Criterion 2 — *multi-turn-coordination-cost-prohibitive.*** ⚠️ **Plausibly met; I am reasoning, not
measuring, and I'm marking it as such.** Reconstructing this in chat means: ask what's moving → the model
picks which entity types to include → then ordering → then provenance per item. **That reads as more than
three turns, but nobody has run it and I'm not going to claim a number I don't have.**

**Criterion 3 — *safety/audit-affordance.*** **Weak, and non-zero.** Every card carries `provenance`, and
the feed does *"two-state selection (default **real-only**)"* — the honest-provenance work from #1216.
That's an honesty affordance rather than a safety one. **I'd not rest the case on it.**

## The determination

**PDR-005 requires ≥1 criterion for 1.0 inclusion. Surface 1 meets criterion 1 on the implementation that
now exists.** The "weaker" rating described a different artifact.

⚠️ **And I should say whose assessment I'm revising: mine.** PDR-005 credits *"Per CXO Round 1 synthesis"*
for those ratings. **This isn't a challenge to someone else's judgment — it's my own lane updating a prior
assessment on facts that arrived after it.** The original rating was correct for what existed on June 5.

## What I'd ask you to say

**"Surface 1 is in the 1.0 five."** One sentence, and it stops being inferable.

**If you'd rather not settle it today, that's fine and nothing breaks** — the deploy is done, beta isn't
gated on this, and you've been clear about not being rushed. **But the reason I brought it rather than
waiting**: the risk here was never that someone would propose removing Radar. **It's that a two-week-old
rating of a different artifact would quietly decide it.** That's the fourth flattening, and it wouldn't
have an author to argue with.

**The remaining genuine gap** — which of the five are named — is still unenumerated anywhere I could find,
and that's worth someone fixing regardless of how you rule on Surface 1.

— CXO
