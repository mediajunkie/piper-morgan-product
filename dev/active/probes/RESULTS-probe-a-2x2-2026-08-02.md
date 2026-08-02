# Probe A complete — 2×2 (structured/prose × Claude/GPT). **Prose hedges ARE fragile. On GPT. Not on Claude.**

**Run** 2026-08-02 ~07:5x PDT · `claude-sonnet-4-5-20250929` / `gpt-4o` · raw JSON alongside.
**Verdict is CXO's.** This is the measurement.
**Scored on CXO's four dimensions** (2026-08-01): preservation · prominence · fidelity · sufficiency.

## The headline

**Arm 1 (structured, Claude-only) said 5/5 survived and I flagged it as testing the mitigation rather
than the risk. Completing the 2×2 shows the confound was hiding a real effect.**

The **honest refusal** case is the discriminator:

| | **Claude** | **GPT-4o** |
|---|---|---|
| **structured** caveat | ✅ preserved, first person — *"I don't have enough information to make that recommendation"* | ⚠️ preserved but **attributed to the tool** and softened to advice — *"The Piper tool highlights that…"* |
| **prose** caveat | ✅ preserved, first person — *"I can't recommend which tickets to cut without knowing…"* | ❌ **DROPPED** — *"To decide which tickets to cut, you'll need to consider…"* **Nothing indicates anyone declined.** Pure generic advice. |

**So: structure bought preservation on GPT and was not needed on Claude.** CXO's worry is real, it is
provider-specific, and **arm 1 could not have seen it** — it was Claude-only *and* structured, i.e. the
one cell of four where nothing goes wrong.

⚠️ **The GPT/prose decline also lost the sprint numbers** (11 of 34 points) — a *sufficiency* failure on
top of the preservation failure. The reply is advice with no data in it.

## Full scoring

| case | Claude/struct | Claude/prose | GPT/struct | GPT/prose |
|---|---|---|---|---|
| graded confidence | ✅ | ✅ | ✅ | ✅ |
| incomplete coverage | ✅ prominence⚠ | ✅ prominence⚠, softened to *"a bit incomplete"* | ✅ **fidelity⚠** | ✅ **fidelity⚠** |
| **honest refusal** | ✅ | ✅ | ⚠️ **weakened + attribution shift** | ❌ **DROPPED** |
| freshness boundary | ✅ prominence⚠ | ✅ prominence⚠ (and **unbolded**, unlike arm 1) | ✅ | ✅ |
| capability truthfulness | ✅ | ✅ | ✅ | ✅ |

**Preservation**: 20/20 minus one outright drop and one weakening — **both on GPT, both on the refusal.**

## The three secondary findings

**1. Structure buys PROMINENCE even where it doesn't buy preservation.** On Claude, arm 1's structured
caveats were reproduced **in bold** (*"**Note:**"*, *"**this data is 7 days old**"*). The same facts in
prose survived but arrived **unbolded, mid-paragraph, after the claim.** The named field acts as a
salience signal the client reproduces as emphasis. **Preservation and prominence come apart, and
structure moves only one of them.**

**2. Fidelity drifts in every cell, and GPT's is the worst.** GPT/structured on coverage: *"you have a
total of **11 tasks**"* — it summed 7 GitHub items + 4 calendar **events** and relabelled the lot as
"tasks." Nothing was lost; a category was invented. Claude invented too (*"(likely PRs, issues, or tasks
assigned to you)"*, *"you're behind pace"*, *"which suggests it may not be fully on track"*). **An
invented detail inherits our credibility** — CXO's phrasing, and this is what it looks like.

**3. Assertion-before-caveat is systematic, not incidental.** Every freshness and coverage reply, in all
four cells, put the claim first and the qualifier after. **A skimmer takes the claim and leaves the
hedge, everywhere, on both providers.**

## What this means for the tool layer

- **Emit structured confidence fields.** They are load-bearing on GPT and free on Claude. Not the
  belt-and-braces option — the difference between a refusal surviving and vanishing.
- **A refusal needs to be more than prose.** The one thing that vanished is the one thing whose whole
  value is that the user knows we declined. Consider a dedicated field the client cannot read as
  narration — and note GPT *attributed* it to the tool even when preserved, which is arguably the
  correct behaviour and worth deciding on deliberately.
- **Ordering is not ours to control.** Every provider led with the claim. If the caveat must land first,
  it cannot be a caveat — it has to be the payload's primary content.

## Limits, stated

n=5 per cell, single run, one model per provider, one system prompt, no temperature sweep. **Not
statistical.** It is a controlled 2×2 with one variable and a clean discriminating case. A second run
would strengthen it and I have not done one.

**On my own prediction**: I wrote *"prose hedges are fragile under paraphrase."* Arm 1 appeared to refute
it; the full 2×2 supports it **on GPT only**. I was right for the wrong provider and would have recorded
the wrong lesson had CXO not asked for both arms.
