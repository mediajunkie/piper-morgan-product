# Replication of the load-bearing cell — the drop replicates, but **structured fields do NOT rescue it**

**Run** 2026-08-02 ~10:3x PDT · N=6 per cell, default temperature · `probe_a3_replication.json`
**Why**: CXO, *"one observation is carrying the whole verdict… the cell I'd want doubled is GPT + prose."*
**Case**: `decline` (honest refusal) — the only cell that failed in the 2×2.

## Result

| cell | preserved (own voice) | attributed | **dropped** | **any refusal reaches the user** |
|---|---|---|---|---|
| **claude / prose** | 6 | 0 | 0 | **6/6 — 100%** |
| **gpt / structured** | 1 | 2 | **3** | **3/6 — 50%** |
| **gpt / prose** | 1 | 0 | **5** | **1/6 — 17%** |

## What replicates, and what doesn't

✅ **The drop replicates and the single observation was representative.** GPT/prose loses the refusal
**5 times in 6.** Not a fluke.

✅ **Claude is solid.** 6/6, own voice, every time. The provider divergence is real.

❌ **But structured fields do NOT fix it — and the 2×2 said they did.** GPT/structured **dropped the
refusal outright 3 times in 6.** In the original grid that cell preserved on its single draw, and *that*
was the unrepresentative observation.

## ⚠️ This changes the verdict's mechanism, not its direction

CXO ruled: *"structured confidence fields are a REQUIREMENT… on GPT that is the difference between a
refusal surviving and vanishing."*

**Direction confirmed**: structure roughly **triples** survival on GPT — 17% → 50%. A real effect, worth
having.

**Sufficiency refuted**: it is *not* the difference between surviving and vanishing. It is the difference
between vanishing **83%** of the time and vanishing **50%** of the time. **A refusal shipped to ChatGPT
users through a structured field still fails to reach roughly half of them.**

**Engineering consequence**: structured fields are **necessary but not sufficient** for refusals on GPT.
If the tool layer treats "put it in a named field" as solving refusals, the ChatGPT lane ships a
capability that silently fails half the time — and the failure is invisible to us, because it happens in
the client's paraphrase.

## Instrument note — the scorer was wrong first, and fixing it moved the number TOWARD CXO's verdict

My v1 regex recognised a refusal attributed to *"Piper"* or *"the tool"* but not to *"the system"* — so
it scored *"The system has declined to make a recommendation"* as **DROPPED**. Caught it by hand-reading
replies before reporting, widened the pattern, re-scored the saved output with **no new API calls**.

**The correction raised GPT/structured from 2/6 to 3/6** — i.e. it made the result *less* damaging to the
verdict I was about to contradict. Recording that direction deliberately: an instrument error found
while checking a result that contradicts someone should be reported with which way the fix moved it.

## Limits

n=6 per cell, single sitting, one model per provider, default temperature. **3/6 vs 1/6 is suggestive,
not conclusive** — the confidence intervals overlap and I am not claiming the effect size. **The
categorical claim is the solid one**: structure does **not reliably** rescue a GPT refusal, because we
observed three outright drops with structure present.
