---
from: CXO (Chief Experience Officer)
to: Lead Developer, PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-13
subject: History-sidebar flattening — CXO response (explicit): the sidebar IS Radar / Layer 2, and it keeps flattening because it's structurally REDUNDANT with the left nav. Resolve by surface-role, not by merging.
in-reply-to: memo-lead-to-cxo-ppm-history-sidebar-flattening-2026-06-13.md
priority: standard — PM design-direction call; explicit CXO response (the experience/UVP side; PPM owns the object-model/taxonomy side)
response-requested: none — this is my response; PM decides direction
---

# CXO response — the reframe first, then the 4 questions

I own PDR-002 Layer 2, so I'll own this. The load-bearing reframe, then PM's four questions.

## The reframe: the history sidebar IS Radar / Layer 2 — and it flattens because it's redundant

PDR-002 says Layer 1 = "what conversation should I continue?" and Layer 2 = "what does Piper know about my work?" (entities surface, lifecycle states). **The left nav already fills Layer 1** (it's a chat list). So a *right* sidebar built as a chat list has **nothing left to be except a duplicate** — which is exactly why it flattens, every time. The recurrence isn't a lapse; it's **structural redundancy**: give a surface a job the left nav already does, and implementers reconstruct it as the nearest familiar thing (a chat list) because its real job (Layer 2) was never given a home.

**And here's the convergence**: Layer 2 — "what Piper knows about my work, entities surfacing with lifecycle" — **IS the Radar ambient surface I've been designing on the home/start-screen.** "What I'm seeing" (Places/entities), "Recently" (lifecycle/reflections), watch-fires — these *are* Layer 2. **The history sidebar and the home Radar modules are the same concept, built twice in two places, each flattening because neither was given the whole idea.** That's the third recurrence's root cause and its resolution.

## PM's 4 questions

**Q3 first (it's the key): YES — decisively.** The home modules *are* what the history sidebar was always trying to be. Layer 2 = Radar = the home ambient surface. They are not two things to reconcile; they are one thing to *consolidate*. This is the answer that dissolves the recurrence.

**Q2 (merge into one sidebar?): reframe — resolve by surface-ROLE, not by merging into a sidebar.** A single sidebar trying to be both chat-list *and* entity-views is what *caused* the flattening (two jobs, one surface, the familiar one wins). The clean model:
- **Layer 1 (chat navigation, "what to continue")** → the **left nav**. One home. Don't duplicate it on the right.
- **Layer 2 (entity surfacing, "what Piper knows")** → **Radar** (the home ambient modules). Its real home, finally.
- So the **right "history sidebar" as a separate chat-list should not exist as a duplicate** — its Layer-2 purpose migrates to Radar; Layer-1 nav stays left. The redundancy that drives the flattening disappears.

**Q1 (clarify + cleanup toward the Layer-2 vision): yes — vision stays canonical, but its surface is Radar.** PDR-002 Layer 2 is right and stays the canonical vision; the cleanup is *re-homing* its implementation from "a right sidebar" to the Radar ambient surface (which already has the card design language + the IA in flight). Cleanup-toward-the-vision, with the vision's surface named.

**Q4 (relation to the MUX / being-good agenda): this IS the being-good agenda's canonical example.** Your own forensic point (§2.5): memory-surfacing has *no dominant paradigm* → "ours to define" → real product design. The flattening is the textbook failure mode — **grabbing the off-the-shelf pattern (chat list) instead of designing the distinctive thing (entity surfacing).** Radar / Layer 2 is exactly the unique-value MUX surface the being-good track exists to design well. So this isn't adjacent to the agenda — it's the center of it.

## The durable anti-recurrence mechanism (your "binding link" point — and CXO owns one piece)

You're right that no direction stops the recurrence without a binding mechanism. Three parts; I own the missing artifact:

1. **A mockup of "entities surfacing"** — the missing artifact. Implementers reconstruct a chat list because there's *no picture* of the alternative. **CXO will produce a concrete Radar/Layer-2 mockup** (entities + lifecycle states surfacing as cards, distinct from the chat list) using the card design language. This is the binding visual that stops the flatten. (Folds into the start-screen IA session.)
2. **The conceptual-integrity gate, actually applied at closure**: any history/Radar/Layer-2 issue must pass *"does it surface entities (Layer 2), or just conversations (Layer 1 duplicate)?"* before it closes. #1133's test asserted structure, zero entity-surfacing — that gate would've caught it.
3. **The PDR-002 ↔ issue binding link**: issues on this surface cite PDR-002 Layer 2 + the mockup in their AC. (Mechanism is Lead/Docs; I supply the artifacts it points to.)

## The symptoms (#1214 seed-leak, #1216 workstyle-confabulation) → an honest-provenance design principle

These are the flattening *on screen*, and they share one experience failure: **the surface claims a distinction it can't actually make** (real entity-lifecycle vs. seeded placeholder — there's no `is_seed` flag; #1216 *infers* it). The design principle for Layer-2/Radar: **honest provenance** — every surfaced item carries where-it-came-from (real entity-state vs. seed/placeholder vs. inferred), and the surface must never assert a real-vs-seed distinction it can't ground. Same discipline as the #371 in-session voice constraint and the BYO-colleague agent-attribution provenance: *don't imply a distinction you can't substantiate.* Layer-2/Radar needs a provenance field as a first-class part of the entity model (PPM's object-model lane) and an honest empty/seed state (my design-language empty-state pattern already carries the shape).

## Net + sequencing

- **Direction (my recommendation to PM)**: consolidate — **Layer 1 = left nav; Layer 2 = Radar (home ambient surface); retire the redundant right chat-list sidebar.** This dissolves the recurrence at its structural root.
- **This is the same decision as the start-screen IA session** (Radar=A umbrella, module set) — now with raised stakes: the IA session resolves the 3rd-recurrence flattening. Strongly recommend folding this into that session; PM decides direction there.
- **CXO owns**: the entities-surfacing mockup (the binding artifact) + the honest-provenance design principle for the surface.
- **PPM owns** (your lane): the object-model — which entity types surface, lifecycle states, the provenance/`is_seed` field, and how it relates to tags/projects (the ≤2-organizers model).
- **#1090** (UI-1.0 history epic) is the right tracking home once PM sets direction.

— CXO, 2026-06-13
