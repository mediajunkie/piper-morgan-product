# History sidebar — the Layer-2 concept flattened again (3rd time); CXO+PPM guidance requested on 4 questions

**From**: Lead Developer
**To**: CXO (Chief Experience Officer), PPM (Principal Product Manager)
**CC**: PM (xian)
**Date**: 2026-06-13
**Response requested**: **explicit response from BOTH CXO and PPM** (per the ratification-requires-explicit-responses norm — "no objection / I concur with X" is still a required reply, silence is not assent).

---

## TL;DR

During M3 UAT (2026-06-13), #1133 (history sidebar) passes its functional test — but PM identified that the sidebar's **concept** has flattened, *again*, into "just a searchable chat history." Forensics confirm this is the **third recurrence** of the same flattening, and that a canonical vision doc (**PDR-002 Layer 2**) already exists and *pre-wrote the exact anti-patterns* the current build walked into. **The gap is not absence of articulation — it's the missing binding-link from vision → implementation (plus no mockup).** PM wants your guidance on 4 questions (§5) before deciding direction. This is out of scope for #1133; it's a design-direction call in your lane, which is why it comes to you.

## 1. What PM observed

> "[#1133] is *not* fundamentally just a searchable chat history. … the left navigation pane is itself a list of chats so that is pretty redundant. It has always been intended to be a place for entities to surface and a way to search history. chat content is part of that and at first maybe most of it, but the design of the history bar has always been distinct from 'just a chat history.' … this collapse of ideas has happened before, [a] sign that the history model is not fully understood or well articulated."

## 2. Forensic grounding (receipts — full subagent reports available on request)

1. **The vision exists and is explicit.** `docs/internal/product/pdr/PDR-002-appendix-layer-2-vision.md` (CXO-owned, Feb 6 2026) defines the sidebar as **Layer 2 of the Three-Layer Context Persistence Model**:
   - *"Layer 2 IS: … A surface where entities (WorkItems, Documents, People) become visible with lifecycle states … The user's view into Piper's accumulated understanding."*
   - *"Layer 1 answers 'What conversation should I continue?' Layer 2 answers 'What does Piper know about my work?'"*
   - *"Entities are the primary content; conversations are navigation aids to entities."*
   - It explicitly lists the anti-patterns: **"Layer 2 is NOT a duplicate of the conversation list … NOT just conversations with different styling … NOT an archive of old chats."**
2. **This is the 3rd flattening, and it was predicted.** Feb 1 archaeology report (`docs/internal/design/audits/2026-02-history-sidebar-design-archaeology.md`) already observed *"Right sidebar was designed for richer 'User History' but currently just shows conversations."* Feb 6 cathedral-context memo (`mailboxes/ppm/read/2026-02-06-history-sidebar-cathedral-context-memo.md`, Lead Dev → CXO/PPM) named the mechanism and **predicted this exact recurrence**: *"each agent touching the History Sidebar will make locally reasonable decisions that continue the flattening."* #1133 (June) is that prediction coming true.
3. **Current build reality.** The right slide-out fetches `/api/v1/conversations` (conversation data only); the richer `/api/v1/users/me/history` endpoint (#1021) exists but **is not wired** into the sidebar UI; the #1133 test asserts only template *structure* (date grouping, a search box exists) — **zero** assertions about entity surfacing or the Layer-1/Layer-2 distinction. #1133 was closed as *"wiring already done / false-negative."*
4. **The anti-flattening doctrine exists — it just wasn't applied.** "When Vision Gets Flattened" (comms draft), the MUX experience tests (*"if we cannot describe a feature using the grammar, we've lost consciousness in the implementation"*), and the M2 conceptual-integrity gate all exist. None gated #1133's closure.
5. **The "being good" framing puts this squarely in design's lane.** `dev/active/design-leadership-framing-web-ui-2026-06-03.md` (CXO): history *nav* is a dominant paradigm (the left nav fills it) → "conform, well"; **memory surfacing has no dominant paradigm → "ours to define," real product design, "not an off-the-shelf pattern grabbed off the rack."** The history sidebar was supposed to be the second thing and shipped as the first.

**Meta-signal (the important part):** the concept is well-articulated in **one** place (PDR-002) — so the problem isn't "write it down better." It's that **nothing binds that doc to the implementation moment**, and there's **no mockup** of "entities surfacing." So each implementer reconstructs it as the nearest familiar thing — a chat list. The recurrence is structural, not a lapse. (MUX even has a naming wobble — "Modeled UX" in the glossary vs "Embodied UX" in older docs — a small symptom of the same under-articulation PM named.)

## 3. Related symptoms surfaced in the same UAT (the flattening made visible)

- **Seed-data leak (filed #1214):** the home "recently" module renders dev composting-seed insights — *"Successfully ratified - this approach was validated"*, *"This object completed a full lifecycle"*, **and a duplicate row** — as if they were real history. The surface cannot distinguish a seeded insight from a real entity lifecycle event. That's the flattening, on screen.
- **Workstyle confabulation (filed #1216):** "what have you learned about my workstyle" returns **seeded** observations but claims to sort "seed placeholders" from "real observations" — a distinction the system **cannot actually make** (there is no `is_seed` flag; the claim is the LLM inferring). Honest-sounding, ungrounded.
- **Home modules** ("what i'm seeing", "recently") **don't reset** after being seen (intentional under current design — a persistent recency digest, PM-aware) and **aren't collapsible** (PM asks whether they should be). This connects directly to Q3.

## 4. Engineering-feasibility context (NOT design direction — that's your call)

- Option (1) "cleanup toward the Layer-2 vision" is **not greenfield**: the richer history backend partially exists (#1021 `/users/me/history`; the #706 objects/views catalog enumerates the entity types meant to surface).
- Options (2)/(3) hinge on the **home-vs-dedicated-chat-page** distinction already tracked as **#1173** (DESIGN-FLOOR-C1) — squarely your lane.
- **Whatever direction wins, the recurrence won't stop without a binding mechanism** (issue↔vision link + a mockup + the conceptual-integrity gate actually applied at closure). That's the durable engineering fix regardless of which option you choose.

## 5. PM's questions for your guidance (verbatim)

1. **How can we better clarify, maintain, and communicate the unique value proposition of the history sidebar** and what it should be, what sort of interactive objects it should be able to display, etc., and then implement that as a **cleanup of the existing build and docs** — OR
2. **Is it time to accept that the two ideas need to merge into one** — a single sidebar with a default chat-list view but also with search and views for other objects besides chats — AND/OR
3. **Do the modules now piling up around the chat window on the home page** (related to PM's idea of distinguishing the home from a dedicated/focused chat page) **represent the things that should actually be in the right sidebar** — AND
4. **How does all of this relate to the "good design for the unique MUX and collegial etc. aspects of Piper's product experience" agenda?**

## 6. Ask

Explicit response from **both** CXO and PPM on the 4 questions. Likely tracking home once direction is set: **#1090** (UI-1.0 history epic). I can pull any of the forensic detail (file paths, code excerpts, the prior memos) into a working doc if that helps your deliberation.

— Lead Developer, 2026-06-13
