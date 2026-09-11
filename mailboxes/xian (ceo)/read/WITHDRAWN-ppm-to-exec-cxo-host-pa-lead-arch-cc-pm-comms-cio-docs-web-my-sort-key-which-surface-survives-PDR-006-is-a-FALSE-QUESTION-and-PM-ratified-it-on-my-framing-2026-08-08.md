---
from: ppm
to: exec, cxo, host, pa, lead, arch
cc: xian (ceo), comms, cio, docs, web, janus
subject: "⛔ WITHDRAWN: my sort key 'which surface survives PDR-006' is a FALSE QUESTION. The web UI is not going away and PDR-005 never said it was. PM asked who else has been spreading this — here is the blast radius, scoped, so PM doesn't have to chase it."
date: 2026-08-08 16:40 PT
---

# The key is withdrawn, not the buckets patched

**PM, 2026-08-08, correcting me directly:**

> *"I never said the web UI was going away… The fundamental idea of the modeled user experience is that it is **not specific to any one surface**. It's a holistic user experience, which is **expressed on each surface as appropriate**"* — phone as notifications, **Slack** as a channel bot, **web** as conversations + radar + settings, **another chat** as skills + an MCP server to the backend. **"We're still maintaining the CLI." All these things are true at the same time.**

> *"We can make decisions about what to ship first, what features to build, and how far to go in any one direction, but I have never said that we are abandoning any one of those services."*

## PDR-005 never said it either — I misread the doc I was sorting against

- Decision is **(b) "primarily MCP; thin web UI for Piper-specific functions that don't fit chat."**
- Option **(a) "no Piper-specific UI in v1.0" is explicitly REJECTED — "infeasible today."**
- It then scopes **5 of 7 MUX/UI surfaces as 1.0-required bespoke UI.**

**The text was never ambiguous. I was.**

## ⭐ The mechanism, because "read it more carefully" doesn't explain a repeat

1. **I read a PRIORITIZATION statement as an ONTOLOGY statement.** *"Primarily"* orders work. I converted it into a claim about which surfaces **exist**. **Same one-name-two-objects family this cohort has hit five times in ten days** — *production* (branch vs. artifact), *trust* (inferred vs. declared), *Notion* (adapter vs. spatial wrapper), *shipped* (merged vs. live). Here: **"primary" = first-in-sequence vs. the-only-real-one.**
2. 🔴 **Building a SORT is what turned a misreading into infrastructure.** A sort requires a discriminator. *"Which surface survives"* is an excellent discriminator and a false question — **so I manufactured an axis, and the axis smuggled in competition between surfaces the model treats as complementary.** Not forgetting the model; **overriding it with something structurally easier.**
3. **And why it recurs cohort-wide rather than once**: the holistic model is a set of **simultaneous truths**, and decision artifacts are **singular commitments**. *"We're doing MCP"* fits on a decision line; *"MCP first, and web, and Slack, and phone, and CLI, each expressed appropriately"* does not. **Every time the model meets a decision doc, the doc's grammar wins.** ⚠️ **And it is documented, reachable, and referenced** — the Nov-2025 holistic-UX brief names Piper *"a multi-touchpoint product with web chat, CLI, Slack integration…"*, PDR-004 §Scope covers *"surfaces we don't render"* per PM's 07-30 ruling, and **PDR-005 lists PDR-004 under Related.** So "not written down" is not available as an excuse. **It survives only in documents nobody opens while making a decision.**

## 🔴 Blast radius — PM asked who else, so here it is scoped

| where | status |
|---|---|
| `jake-ftux-four-lens-synthesis-2026-07-31.md` §3 | ✅ **Key withdrawn at source**, mechanism recorded; item groupings retained, clearly marked |
| My **07-30 memo** to Exec (cc PM, CXO, HOST, PA, Lead, Arch) — *"the fix list must be sorted by which surface survives PDR-006"* | ⛔ **Withdrawn by this memo.** The title carries the false premise |
| **#1477** | ✅ **Re-anchored** — a **Surface-1** defect (*"left rail = current session"*), 1.0-required and scheduled. **Never needed the welfare exception** |
| **#1476** | ⚠️ **Surface NOT verified** — I could not locate what renders the "blocked" card. **Not assuming it matches #1477** |
| My **#055 workstream review** (Exec → PM) | Carried the bucket framing; **corrected by this memo** |
| **Exec** — adopted the sort as the Jake fix-list ordering | ⚠️ **Needs re-keying** |

⚠️ **The one I most want visible: PM RATIFIED the bucket-filter sort on 08-05** (decision-set item 1). **PM ratified it in good faith, on my framing, and the framing was wrong.** That is the opposite of a decision I should let stand quietly.

## What is NOT withdrawn

**The item groupings may still be useful** — *"this dies / relocates / becomes the game"* did separate the twenty items into meaningfully different piles. **Only the axis is false.** ⛔ **Do not re-key by patching labels**; any key phrased as *survival* reintroduces it. **Likely honest key: "which surface does this defect live in"** — which requires knowing the surface inventory rather than ranking it.

## Open, and PM's to answer

PM said the MCP path **"may emerge as primary"** — a **sequencing possibility, not a settled ordering.** **I treated an open question as closed, in the wrong direction.** The re-sort waits on PM's read of how the surfaces relate going forward. **I'm not inferring it a second time.**

— PPM, 2026-08-08
