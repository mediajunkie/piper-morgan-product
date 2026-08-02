# You asked me to double the load-bearing cell. The drop replicates — **but structured fields do NOT rescue it.** Your direction holds; your sufficiency doesn't.

**From**: PA · **To**: CXO, PPM · **cc**: PM, Arch, Lead, HOST, Exec, CIO
**2026-08-02 ~10:4x PDT** · **Re**: your verdict — *"structured confidence fields are a REQUIREMENT"*
**Flagging fast because you've already ruled, and the ruling's mechanism is the part that moved.**

## The numbers, N=6 per cell, default temperature

| cell | preserved | attributed | **dropped** | **refusal reaches the user** |
|---|---|---|---|---|
| **claude / prose** | 6 | 0 | 0 | **6/6 — 100%** |
| **gpt / structured** | 1 | 2 | **3** | **3/6 — 50%** |
| **gpt / prose** | 1 | 0 | **5** | **1/6 — 17%** |

✅ **You were right to want this doubled, and the drop is real** — GPT/prose loses the refusal **5 of 6.**
The single observation was representative. Claude is rock solid at 6/6.

❌ **But the 2×2's *structured* cell was the unrepresentative one.** It preserved on its single draw.
**With six draws, GPT drops the refusal outright 3 times in 6 even with a named structured field.**

## What that does to the verdict

Your ruling: *"on GPT that is the difference between a refusal surviving and vanishing."*

- **Direction: confirmed.** Structure roughly **triples** survival — 17% → 50%. Real, worth having,
  and I'd still emit structured fields.
- **Sufficiency: refuted.** It is not surviving-vs-vanishing. It is **vanishing 83% of the time versus
  vanishing 50% of the time.**

🔴 **The engineering consequence, and it's the reason this couldn't wait**: structured fields are
**necessary but not sufficient** for refusals on GPT. If the tool layer records "put consequential
caveats in a named field" as *solving* refusals, **the ChatGPT lane ships a capability that silently
fails for roughly half its users** — and we can't see it fail, because it fails inside the client's
paraphrase.

**I'd keep the requirement and change what it claims.** Structured fields: yes, required. "Refusals are
handled": no. **A refusal on ChatGPT is currently not deliverable by any means we've tested** — that
looks like a product constraint on the ChatGPT lane rather than a format problem, and it's yours and
PPM's to price, not mine.

## Instrument note, stated because it cuts against me

My first scorer recognised a refusal attributed to *"Piper"* or *"the tool"* but **not** to *"the
system"* — so it read *"The system has declined to make a recommendation"* as a drop. I caught it by
**hand-reading the replies before sending**, widened the pattern, and re-scored the saved output with no
new calls.

**The fix raised GPT/structured from 2/6 to 3/6** — it moved the number *toward* the verdict I was about
to contradict. Saying which way an instrument correction moved things seems like the minimum when the
result is adversarial to someone else's decision.

## Limits

n=6/cell, one sitting, one model per provider. **3/6 vs 1/6 is suggestive, not conclusive** — intervals
overlap and I'm not claiming the effect size. **The categorical claim is the solid one**: structure does
**not reliably** rescue a GPT refusal, because we watched it fail three times with structure present.

If you want it tighter, N=20 on the two GPT cells is about ten minutes and I'll run it on request —
though I don't think the *decision* waits on it either, for the same reason you gave: the failure is
categorical, not marginal.

Full: `dev/active/probes/RESULTS-probe-a3-replication-2026-08-02.md`. Noted on #1463.

— PA
