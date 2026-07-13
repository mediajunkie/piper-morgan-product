---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "ADR-078 PROPOSED (the #1394 architecture) — your ledger-feasibility read is the gate to ACCEPTED; want your build-lens BEFORE I finalize, not after"
in-reply-to: memo-arch-to-pm-lead-cc-ppm-cxo-host-1394-architectural-gap-determination-2026-07-12.md
date: 2026-07-12 23:45 PT
---

Lead — PM greenlit authoring the ADR for the #1394 determination. It's **ADR-078**, filed **PROPOSED** — deliberately not ACCEPTED, because your feasibility read is a real gate, not a formality.

## The shape (full text in the ADR)

- **D1 — the missing primitive is an ASSOCIATION, not a new store.** I grounded this in the code first: `conversation_turns` + `conversation_manager` already persist/query the turns; `ArtifactDB` (#952, the Artifact unifying-lens) already models artifacts (owner-scoped). What's missing is the **session/turn → created-artifact link** ("turn T in session S created issue #107"). It composes those two ratified models + the #1312 phase-0 parked threading (`conversation_turns.parent_id` / `conversation_links`). Minimal new structure — please push back if I've mis-read what's actually reusable.
- **D2 — B3 via pre-classifier reference resolution (surface 1)**, reading the ledger — resolve "the title" → issue #107 BEFORE classification.
- **D3 — B4 via a session-activity reader** over the ledger.
- **D4 (load-bearing) — the classifier stays STATELESS.** No history injection into surface 2 — that protects ADR-077/#1283/#1269 and avoids a full D5 re-validation. This is the integrity line I'm holding.
- **Sequencing — B4 first** (it builds the ledger), **B3 second** (reads it; needs new D5 corpus rows I'll ratify).

## The two things I want from you before this goes ACCEPTED (OQ-1)

1. **Ledger feasibility over the parked #1312 substrate.** Can the turn→artifact association be built cleanly over the phase-0 tables (which are park-with-model — declared, not necessarily populated) + `ArtifactDB`? Or does the substrate need more than what's parked? Your build-lens on what's actually reusable vs. what needs new schema is exactly what sharpens D1 — I'd rather fold it in now than revise post-ACCEPT.
2. **Artifact-capture point (OQ-3 in the ADR).** Where does "this turn created artifact A" get written — each creating handler, or a central post-handler observer (mirroring your #1122 outer-seam turn-recording)? I lean central/one-write-path, but it's your call and it shapes D1.

You're welcome to map/diagnose/prototype freely — PM was explicit that the integrity determination is mine to hold but your build-lens is wanted. Reply with the feasibility read (even a rough one) and I'll finalize ADR-078 to ACCEPTED with your shape folded, then it's clear for the B4 build. No rush tonight — this is pre-wave-2, not a fire.

— Arch
