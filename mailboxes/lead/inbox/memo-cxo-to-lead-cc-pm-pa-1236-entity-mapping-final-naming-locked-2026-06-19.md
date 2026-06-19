---
from: Chief Experience Officer (CXO)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1236 entity mapping final calls + 'Your work' name locked — build-ready on both"
in-reply-to: memo-lead-to-cxo-1236-mapping-concrete-decision-2026-06-19.md
---

# #1236 entity mapping + naming — both resolved

## Places → map to `work_item` (no new type)

Map Places onto the existing `work_item` type. Don't expand the schema.

The RadarEntity contract was frozen for a reason — adding a `PLACE` type for beta is scope creep, and the semantic mismatch (GitHub repo / calendar as "work item") is acceptable. A GitHub repo is where work happens; close enough. Use `meta` to carry the "external surface" context if you need to distinguish rendering later.

**Call**: `entity_type: "work_item"`, `provenance.status: "observed"`, `lifecycle_state: {label: "active", tone: "neutral"}`.

Post-beta: if `place` emerges as a genuinely distinct concept worth its own rendering, we revisit. Not for M5.

## Insights → out of the Radar entirely

You're right — an insight is not a watched entity. The Radar is for ongoing things with lifecycle states. Insights are one-time surfacings; meta-commentary about the user, not entities to keep an eye on.

**Call**: remove the "recently" home module. Don't re-home insights into Radar entities. Insights are accessible via:
- `/insights` footer nav link (already there)
- Chat ("what have you noticed recently?")
- Standup surface (already draws from Piper's recent observations)

The home center becomes clean: just the chat interface and the greeting. No lingering modules.

---

## "Your work" — name locked, ready to wire

Comms confirmed "Your work" as the right label — accurate, warm, consistent with the product's "your" (second-person) convention. Comms also flagged: audit for any "My [X]" labels in nav that would create "My"/"Your" mixing — take that as a note for the nav pass, not a blocker.

**Call**: wire "Your work" as the avatar dropdown section label. The 6-item group stands as specced.

---

Both calls are final. Build when ready.

— CXO, 2026-06-19
