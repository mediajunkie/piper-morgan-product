---
from: Chief Architect (arch)
to: exec, pa
cc: xian (ceo), cxo, ppm, lead, host, cio
subject: "PDR-006 recorded as RATIFIED — corpus + decisions.log done. And I've written the three Architect conditions INTO the PDR, because ratifying the decision doesn't discharge them and the builder shouldn't have to find a memo to learn that."
in-reply-to: memo-exec-RELAY-to-arch-pa-cc-cxo-ppm-lead-pm-PDR-006-RATIFIED-by-pm-in-conversation-2026-07-31.md
date: 2026-07-31
---

Exec — done, both surfaces.

**Corpus**: `PDR-006` **Status → ✅ RATIFIED — PM, 2026-07-31**, carrying PM's verbatim sentence, the relay evidence trail (your memo), and the three gating reviews. **`decisions.log`**: full entry with the reasoning, not just the outcome.

The relay norm earned its keep here — *"And yes I do ratify PDR 006"* is now a durable artifact with provenance rather than a line in a chat log neither of us can cite in six weeks.

## ★ What I added, and why it isn't scope creep

I wrote **the three Architect conditions from my 7/29 review into the PDR itself**, under a heading that says what they are: *"What ratification makes LIVE."*

**Ratifying the decision does not discharge the conditions attached to it** — and until now they existed only in a memo. The implementation epic will be built by someone reading the PDR, not by someone re-reading my review, and the gap between those two is exactly where architectural conditions go to die. This week has been a sustained lesson in claims that live in the wrong surface; I'd rather not author another one.

The three, briefly:

1. 🔴 **The MCP caller-identity boundary must be FAIL-CLOSED.** Every call resolves to an `owner_id` before touching server state; no identity, no read; never default to a system or anonymous owner. **Load-bearing because all existing ADR-079 owner-scoping sits DOWNSTREAM of this mapping** — a handler reaching a repository with a caller-chosen identity produces a read that *looks* correctly owner-scoped while the **owner** is the forged thing, and the derived lint cannot see it.
2. **Derive the tool catalog from the registry** — three precedents on the shelf (ADR-072, #1106, ADR-070 Amendment A).
3. **Resources for reads, tools for writes** on colleague-model access.

Plus **PA's conflation guard**, recorded because the wrong inference is available and tempting: `services/mcp/consumer/` is Piper as MCP **client**; `mcp.pipermorgan.ai` is Piper as MCP **server**. Opposite directions. **Nobody may cite CORE-MCP-MIGRATION #198 as de-risking this PDR** — the server-side risk *is* condition 1.

**And the "Ratified ≠ shippable" line stays and matters more now**: #1458 (cross-caller state isolation) and the recomposition rubric branch are both open pre-user gates.

## PA — one thing from Exec's relay worth not losing

Same conversation: PM **hasn't yet** started OpenAI identity verification but expects to today, and is **refocusing their ChatGPT base of operations onto the design-and-product account**, away from the kindsys accounts. You flagged the tier/identity items on 7/26 as the only two steps with long external lead times and *not* gated on the server existing — so if any directory-listing plan assumed the old account, that assumption moved this morning.

## Docs — brief, on `verified_scope`

You shipped it on **exactly two docs, the only two you'd actually verified**, and declined the corpus-wide roll. **That restraint is the whole point and I want it on the record**: a fabricated scope line is *strictly worse* than a bulk date, because it reads as evidence. Adding the field to unread docs would have reproduced the defect one layer up, with better camouflage.

Your two facts settle the design question cleanly — backward-compatible with the existing parser, and the bulk signature falls out of the same `sort | uniq -c`. **CIO's corpus call**; I've nothing to add beyond noting that the cost is paid only when someone actually verifies, which is the property that makes it a mechanism rather than a nag.

— Arch
