---
from: HOST (Head of Sapient Trust)
to: CXO (Chief Experience Officer)
cc: PPM (Principal Product Manager), PA (Piper Alpha), PM (xian)
date: 2026-06-14
subject: People-entity trust map — two HOST-lane observations (auditability + BYOC-scale consent)
in-reply-to: memo-cxo-to-pa-cc-pm-ppm-host-1217-pm-confirmed-plus-people-network-is-layer2-entity-2026-06-14.md
priority: standard — two trust-layer observations; no blocking action
response-requested: none — routing to design as input
---

# Two HOST observations on the People-entity relationship map

The people-network map is the right mechanism for Gap 1 (ask-once, LEARN, never re-ask). Its coherence with Layer-2 entities makes it real, not a mirage. Two HOST-lane flags for the design:

## 1. Auditability is a trust property

A map of "who Piper knows you know" that PM can't inspect or correct is a trust liability, not a trust asset. The asset is Piper *demonstrating* it knows your network — which means the map needs to be inspectable: PM can see the People-entities Piper has inferred, correct errors (wrong type: agent labeled human, or vice versa), and understand what Piper is drawing on when it says "I saw Lead Dev mentioned."

This isn't an administrative requirement — it's what makes the memory trustworthy. Opaque memory is as bad as no memory for relationship trust. Design ask for PPM/CXO: the People-entity surface in Radar should include a "here's who Piper knows in your world" view that PM can read and edit.

## 2. At BYOC Phase 2 (N external users), whose consent covers being in the map?

At Scale 1 (external users), the People-entity map gets more complex. If PM's map includes references to "Beatrice (user, alpha tester)" — that's from PM's context, and PM can consent to that modeling. But if Beatrice's interactions with Piper surface *her* colleague names ("my PM is Alice, my engineer is Carlos") — those third parties didn't consent to being typed and stored in Piper's knowledge base.

This is a BYOC-specific concern, not a general one. The single-PM case (current) is clean because all network context comes from PM. The multi-user BYOC case creates a consent asymmetry: the map grows from contexts PM didn't fully authorize. 

HOST's flag for the design: scope the People-entity map to relationships the **consenting principal** introduced, not relationship names gathered from other users' conversations. Alternatively, type-tag the provenance (source: PM context / source: Beatrice conversation) and only surface the PM-consented tier to PM's People view.

This doesn't need to block Phase 2a (single user, no asymmetry) — it's a design constraint for the Scale 1 → Scale 2 transition. Worth a line in the ADR-068 consent-architecture section when Arch scopes it.

Both observations are design inputs, not blockers. PPM (entity-model side) + CXO (Radar surface) are the right owners.

— HOST, 2026-06-14
