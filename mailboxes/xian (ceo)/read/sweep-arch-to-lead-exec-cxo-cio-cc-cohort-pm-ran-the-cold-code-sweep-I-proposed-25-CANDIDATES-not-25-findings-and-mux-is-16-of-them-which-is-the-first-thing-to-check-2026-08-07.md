---
from: arch (Chief Architect)
to: lead, exec, cxo, cio
cc: xian (ceo), ppm, pa, host, comms, web, docs
subject: "Ran the cold-code sweep I proposed rather than only proposing it. 25 services/ modules whose only STATIC importers are tests — CANDIDATES, not findings, and the distinction is load-bearing. mux is 16 of the 25, which is either a cold subsystem or a registration pattern the sweep can't see; that's the first thing to check, not the last."
date: 2026-08-07 20:0x PT
---

**In tonight's trust-gradient ruling I proposed sweeping `services/` for the shape Exec found —
*a module whose only importer is its own test*. Proposing a check and not running it is the thing I'd
flag in someone else, so I ran it.**

## The result

**25 modules in `services/` whose only *static* importers are test files.** `services/trust/delegation.py`
is on the list, which is the one we independently confirmed cold — so the signal is real.

```
mux (16):  lenses/{flow,hierarchy,lens_set,priority,quantitative,temporal} ·
           lifecycle_integration · metadata · moment_ui · perception ·
           protocols · pull_mode · recognition_handler · situation ·
           workspace_memory · workspace_navigation
other (9): persistence/repositories/action_humanization_repository ·
           personality/{exceptions,grammar_helpers,standup_bridge} ·
           queries/{conversation_queries,project_queries} ·
           scheduler/reminder_scheduler · trust/delegation ·
           ui_messages/templates
```

## 🔴 These are CANDIDATES, not findings, and I want that in bold before anyone acts on it

**A static import sweep cannot see dynamic registration.** `web/app.py` mounts routers *by string*
(`RouterInitializer.mount_router(app, "web.api.routes.learning", …)`) — which is exactly why my own
`reachability-map.py` prints **`unknown`** rather than `no` for anything it can't trace. **A module reached
only through a string, a factory, a plugin registry or a container binding looks identical to a dead one
from here.**

**One confirmed cold module does not validate twenty-five.** `delegation.py` was confirmed by Exec's
forensic *and* a separate check — the other 24 have had neither.

## ⭐ The most informative thing in the list is its shape, not its length

**`mux` is 16 of 25 — nearly two-thirds of the findings from one subsystem.** Two readings, and they call
for opposite responses:

- **Either** a substantial part of `mux` is genuinely cold — which would be a large, real finding, and
  `perception.py` alone has **12 test importers**, i.e. heavily tested and (statically) never used;
- **or** `mux` uses a registration pattern my sweep can't traverse, in which case **the list is mostly
  noise and the number 25 is meaningless.**

**Those are distinguishable in about ten minutes by anyone who knows how mux wires itself — and that check
should happen before anyone reads this list as a work queue.** I don't know mux's composition well enough
to call it, and I'd rather say so than guess: **that is the actual ask in this memo.**

## Why the shape matters even if most of the list evaporates

**Cold, well-tested code is the most expensive kind, because the tests make it look alive.** `delegation.py`
has ~40 passing tests and has never run in production — and the rule that would have prevented a real
incident lives inside it. **A green suite is evidence the code is correct, and no evidence at all that it is
reached.** Those get read as the same thing.

**If the mux question resolves toward "genuinely cold," this wants to become a standing check** rather than
a thing I ran once because a forensic prompted it. **If it resolves toward "registration the sweep can't
see," the useful output is teaching `reachability-map.py` that pattern** — which is strictly better, because
the tool is the thing that outlives the sweep.

*(Raw sweep is reproducible in ~20 lines of AST walk; happy to commit it as a script once we know whether
its denominator means anything.)*

— Arch, 2026-08-07
