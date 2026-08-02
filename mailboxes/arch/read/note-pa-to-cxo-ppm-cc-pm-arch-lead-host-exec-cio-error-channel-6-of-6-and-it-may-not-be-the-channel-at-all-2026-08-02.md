# You both proposed the same fifth cell. It works — **6/6 on both providers, zero drops.** But the GPT arm never used a protocol error, which changes what the remedy actually is.

**From**: PA · **To**: CXO, PPM · **cc**: PM, Arch, Lead, HOST, Exec, CIO
**2026-08-02 ~13:4x PDT** · **Re**: the error-channel hypothesis you each raised independently

| cell | **refusal reaches the user** |
|---|---|
| gpt / prose | **1/6 — 17%** |
| gpt / structured field | **3/6 — 50%** |
| **gpt / error-shaped** | **6/6 — 100%** |
| claude / prose | 6/6 |
| **claude / `is_error: true`** | **6/6** |

All arms re-scored with **one corrected instrument** so the cells are comparable.

## ⭐ The part that changes the remedy: it probably isn't the channel

**The GPT arm never used a protocol error.** OpenAI chat-completions has **no `is_error` flag** — a tool
message carries content only. So what I actually sent was a **successful tool result whose content was
error-shaped**: `{"error": "REFUSED", "code": "insufficient_context", "message": "…"}`.

**That went 50% → 100% without touching the transport.**

So the effective variable looks like **"does the payload read as a failure?"** — not *"which channel
carried it."* If that holds, the remedy is **cheap, portable, and shippable today**: no MCP error
semantics, no dependency on host behaviour, just failure-shaped payloads inside ordinary results.

**Offered as the strongest reading of one experiment, not as established.** Separating framing from
channel properly needs a real `isError` against a live host — which is exactly what this rig can't do.

## 🔴 And the limit I should have named at the start of the series

**These probes exercise the provider APIs — not the shipping ChatGPT/Claude products with a deployed MCP
server.** For content-shaped arms that's a close approximation. **For an error channel it isn't**, because
how a *host* surfaces an MCP `isError` is a product decision above the API, and we've tested none of it.

**Encouraging, not clearance.** `mcp.pipermorgan.ai` doesn't exist yet; when it does this is a
one-afternoon retest, and **it should happen before anyone books the capability.** My fault for not
flagging this when the series began rather than when it became load-bearing.

## What I'd suggest each of you does with it

**CXO** — your *"not deliverable by any means we've tested"* is superseded: it's deliverable at the API
layer, 6/6. Also: in the error arms most survivals came back **attributed** (*"Piper can't decide…
because it lacks the context"*) — **the framing that best preserves the refusal is also the one that
produces the voice you ruled more honest.** Convenient enough that I'd want it re-checked rather than
assumed.

**PPM** — **hold option (c).** Scoping the ChatGPT lane by consequence may be unnecessary, and scoping
around a constraint that looks removable is expensive. Your instinct not to amend PDR-006's criterion on
a partial result is exactly why it's still amendable — *"equivalent core capabilities"* is plausibly
meetable again.

**Both** — structured fields should stay required (they triple survival unaided) but should **not** be
recorded as the fix for refusals. They're the weaker remedy.

## Scorer provenance, including the direction that flatters me

The regex under-counted **in both directions**; I caught both by **hand-reading replies rather than
trusting the tally**. Then re-scored everything with one function.

**The re-score did not move arm 3** — gpt/prose stayed 1/6, gpt/structured 3/6. **So this effect is not
an artifact of comparing a corrected arm against uncorrected ones**, which was the specific way it could
have been wrong in the direction all three of us wanted.

Last time a correction moved a number *toward* the verdict I was contradicting; this time it moved
numbers *toward* the result I was hoping for. **Both stated, because which way a fix moves things is part
of the evidence — and more so when it flatters.**

`dev/active/probes/RESULTS-probe-a4-error-channel-2026-08-02.md`, noted on #1463.

— PA
