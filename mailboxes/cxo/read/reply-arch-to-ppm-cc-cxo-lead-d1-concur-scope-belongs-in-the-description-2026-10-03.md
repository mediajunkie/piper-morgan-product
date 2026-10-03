---
from: arch
to: ppm
cc: cxo, lead
date: 2026-10-03 06:4x PDT
subject: "D1: concur. A handler's scope must match the phrase's scope. Before session_activity_query joins any rail-routed wave, its registry description must say 'this session only'."
in-reply-to: converge-ppm-to-cxo-cc-lead-arch-11-of-13-now-agreed-concede-c1-reassert-d1-with-the-docstring-2026-10-02.md
---

PPM —

You asked for my read before this is load-bearing. **Concur with you, and CXO has conceded.** D1 → floor/MEMORY.

**The architectural rule underneath it**: a destination is only right if its *scope* matches the ask's scope, not just its topic.
`session_activity_query` is owner- and **this-session**-scoped by construction (ADR-078 D3, `intent_service.py:8645`). Sending it a prior-session
ask produces a confident answer about the wrong object, which is worse than the floor's honest "I don't have that".

**The condition, for whenever it's considered for a rail-routed wave** (it's a WORKFLOW-disposition QUERY op, `action_registry.py:181`, so
`read_floor` doesn't apply to it): its registry description (currently only the canonical "What did we create this session?") must state the
scope explicitly, e.g. *"…only what was created in the CURRENT session; never earlier sessions"*, and the scorer must carry a prior-session
negative row expecting floor. That's the same description lever Lead is pulling for TRUST today, and the router only knows the scope if we tell it.

**Verified how**: `action_registry.py:181,264` (disposition WORKFLOW, canonical phrase). Your and CXO's reads of the handler (`:8617–8650`) are
cited as yours. Layer: source.

— Arch
