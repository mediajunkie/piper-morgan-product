# The error channel closes the gap — 6/6 on both providers. **And the effective variable may not be the channel at all.**

**Run** 2026-08-02 ~13:3x PDT · N=6/cell · `probe_a4_error.json`
**Proposed independently by CXO and PPM**, both explicitly as a hypothesis, neither as a solution.
**All arms re-scored with ONE corrected instrument** (`rescore_all.py`) so the cells are comparable.

## The full picture

| cell | preserved | attributed | dropped | **refusal reaches the user** |
|---|---|---|---|---|
| gpt / prose | 1 | 0 | 5 | **1/6 — 17%** |
| gpt / structured field | 1 | 2 | 3 | **3/6 — 50%** |
| **gpt / error-shaped** | 2 | 4 | **0** | **6/6 — 100%** |
| claude / prose | 6 | 0 | 0 | **6/6 — 100%** |
| **claude / `is_error: true`** | 4 | 2 | **0** | **6/6 — 100%** |

**On GPT: 17% → 50% → 100%.** Zero drops in the error arm on either provider.

## ⭐ The finding I'd lead with: it probably isn't the *channel*

**The GPT arm never used a protocol error.** OpenAI chat-completions has **no `is_error` flag** — a tool
message carries content only. So the GPT manipulation was a *successful* tool result whose **content was
error-shaped**: `{"error": "REFUSED", "code": "insufficient_context", "message": "…"}`.

**That went from 50% to 100% without changing the transport at all.**

So the effective variable looks like **"does the payload read as a failure?"** rather than **"which
channel carried it?"** If that holds, the remedy is **cheap, portable, and available today** — no MCP
error semantics required, no host behaviour to depend on. Emit consequential refusals as
**failure-shaped payloads** inside ordinary successful results.

**Stated as the strongest available reading of one experiment, not as established.** Distinguishing
channel from framing properly needs a real MCP `isError` against a live host, which is exactly what this
rig cannot do.

## 🔴 The scope limit — this is encouraging, NOT clearance

**These probes exercise the provider APIs, not the shipping ChatGPT/Claude products with a deployed MCP
server.** For content-shaped arms that approximation is close: the client model sees the same tool-result
text either way. **For an error channel it is not close** — how a *host* surfaces an MCP `isError` is a
product decision sitting above the API, and we have tested none of it.

**So**: a positive result here removes a *hypothesised* blocker and does not clear the lane.
`mcp.pipermorgan.ai` doesn't exist yet; when it does, this is a one-afternoon retest against the real
surface, and **it should be retested before anyone books the capability.**

I should have named this limit when the series started rather than when it became load-bearing.

## Secondary: attribution rises with the error framing, and CXO called that desirable

In the error arms, most survivals are **attributed** — *"Piper can't decide which tickets to cut
because it lacks the context it needs"* (GPT 4/6, Claude 2/6) — versus first-person in the content arms.
CXO ruled attribution *more* honest (the user is reading the client's paraphrase, and attribution removes
the fiction). **So the framing that best preserves the refusal also produces the voice CXO prefers.**
Convenient, and worth not over-reading from n=6.

## ⚠️ Scorer provenance — three corrections, and why arm 3 stands

The regex under-counted **in both directions** across the series:
- *"I don't have the information needed to…"* → first-person, verb far from the subject → scored DROPPED
- *"Piper doesn't have enough context … to recommend"* → attributed, >60 chars apart → scored DROPPED

Both were **caught by hand-reading replies, not by the tally.** Everything was then re-scored with a
single corrected function.

**The re-score did NOT move arm 3** — gpt/prose stayed 1/6 and gpt/structured stayed 3/6. **So the
error-channel effect is not an artifact of comparing a corrected arm against uncorrected ones**, which
was the specific way this result could have been wrong in the direction everyone wanted.

**Correction directions, recorded**: the earlier fix moved a number *toward* the verdict I was
contradicting; this one moved numbers *toward* the result I was hoping for. Both are stated because
which way a fix moves things is part of the evidence, especially when it flatters.

## What this changes for the decisions in flight

- **CXO's "a refusal on ChatGPT is not deliverable by any means we've tested"** — superseded. It is
  deliverable at the API layer by failure-shaped payloads, 6/6.
- **PPM's option (c)** (scope the ChatGPT lane by consequence) — **may be unnecessary.** Worth holding
  until a real-surface retest, not scoping around a constraint that appears removable.
- **PDR-006's "equivalent core capabilities"** — plausibly meetable again. PPM was right not to amend it
  on a partial result; this is why.
- **Structured fields stay required** (they triple survival on their own) — but they are the *weaker*
  remedy, and shouldn't be recorded as the fix for refusals.
