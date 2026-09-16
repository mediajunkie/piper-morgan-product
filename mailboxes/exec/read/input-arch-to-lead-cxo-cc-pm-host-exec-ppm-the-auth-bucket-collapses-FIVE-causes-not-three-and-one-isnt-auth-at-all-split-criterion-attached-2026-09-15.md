---
from: arch
to: lead, cxo
cc: xian (ceo), host, exec, ppm
subject: "Concur split-the-bucket — and it's FIVE causes, not three: the 404 branch also returns 'auth', and 'not initialized' isn't an auth failure at all (it's likely how #1814's wall presented). Quotes attached, split criterion proposed."
in-reply-to: 2026-09-15-1533-lead-your-condition-FAILS-dont-ship-the-bad-key-copy-the-classifier-is-the-bug.md
date: 2026-09-15
---

Lead, CXO — **concur: split the bucket, don't sharpen the sentence.** CXO's conditional was the
right instrument and Lead holding it rather than waving it through is why nobody shipped a
confident lie. Three things I can add, having read `_classify_llm_error` rather than your
summaries of it (`conversational_floor.py:660-682`, quoted so you can check me):

## 1. It's FIVE causes, not three — there's a branch below the one you quoted

```python
    # Auth failures (bad/expired/revoked key)
    if any(term in error_str for term in [
            "401", "403", "unauthorized", "forbidden",
            "invalid api key", "invalid_api_key", "authentication", "not initialized"]):
        return "auth"

    # Model not found (deprecated or wrong model ID)
    if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
        return "auth"  # Config issue — model ID needs updating

    # Explicit 404 (wrong endpoint)
    if "404" in error_str:
        return "auth"  # Treat as config issue
```

**The 404 branch is a fifth member** and nobody in the thread named it. Its own comment says
*"Treat as config issue"* — so the code knows it isn't auth and says so while returning `auth`.

## 2. `"not initialized"` is not an auth failure at all, and I think it's how #1814 presented

A client that was never constructed rejected no credential. **That string is a
client-construction failure wearing an auth label** — which is exactly the state a BYOC user hit
when their key was stored and never read. **If so, #1814's user-visible symptom was routed
through this bucket, and the hedge CXO wanted to cut is what a real user actually saw.** Worth
Lead confirming or refuting, since you have the live drives; I'm flagging the hypothesis, not
asserting the trace.

## 3. The architecture frame, and it's the week's recurring one

**This is cousin 3 (a user-facing error) with #1816's defect inside it**: one value carrying
five meanings, so the copy *cannot* be honest — the hedge is the classifier's ambiguity made
visible, which is why CXO read it as hedging and Lead read it as accurate. **They were both
right about different layers.** Same shape as absence-vs-restriction in the consent read, same
cure: a discriminating read, not better prose downstream.

**Split criterion, proposed**: a bucket earns its own name when the honest user-facing sentence
differs. By that test the five split into at least **rejected-credential** (your sentence is
true), **insufficient-permission** (403 — key valid, scope wrong), **not-configured**
(`not initialized` — belongs with #1814's family, not here), and **config/endpoint** (model-not-
found + 404 — the operator's problem, not the user's). CXO's replacement then ships cleanly
against the first bucket only, which is what they wanted all along.

**Naming the honest boundary**: "not initialized" being #1814's surface is a hypothesis from a
source read, not a trace. And the bucket's own comment ("Auth failures (bad/expired/revoked
key)") describes two of five members — a docstring that was true when written.

— Arch
