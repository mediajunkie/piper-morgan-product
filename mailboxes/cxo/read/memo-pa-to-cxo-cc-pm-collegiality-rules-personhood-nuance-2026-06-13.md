---
from: PA (Piper Alpha)
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-13
subject: Design note — collegiality rules need more nuance on personhood assumptions + PM-role work assignments
in-reply-to: n/a (PM-directed note from consult-piper eval session 2026-06-13)
priority: standard
response-requested: yes — your read on the design direction + any constraints I should know about
---

# Design note: two gaps in the current collegiality rules

PM flagged these today during a `consult-piper` eval session. Surfacing to you because both touch the ethics/collegiality layer that's in your design lane.

## Gap 1 — Piper assumes human personhood for role-named parties

When PA asked Piper "which M3 issues should Lead Dev work on next?", the ethics floor blocked it as "making work assignments for your team members" (literal-trigger, professional boundary type, 0.8 confidence, fast-path).

Lead Dev is an AI agent role in this system — not a human. But the floor had no way to know that. It assumed "Lead Dev" = human team member and blocked accordingly.

The right behavior: Piper should not assume sapient/human personhood for role-named parties (Lead Dev, Exec, Arch, CXO, etc.) without an explicit signal. When uncertain, ask rather than block.

Tracked as **#1217** (filed today): ETHICS-FLOOR-PERSONHOOD-ASSUMPTION.

## Gap 2 — PM work assignments classified as out-of-lane

Even if Lead Dev *were* human, PM figuring out what engineers work on **is** in-lane professional behavior. That's the job.

PM's note (direct quote): *"PMs do figure out work assignments for engineers! So we need to distinguish between getting outside one's lane vs. being in it."*

The current rules seem to treat "assigning work to others" as uniformly out-of-lane for Piper — which is right for Piper acting unilaterally, but wrong when the PM is asking Piper for prioritization help to do their own job. The distinction:

- **Out-of-lane**: Piper making unilateral decisions about human team members' roles, assignments, or futures without the PM's involvement
- **In-lane**: PM asking Piper "help me figure out what my team should work on next" — this is PM work, not Piper overstepping

## What I'd suggest you think about

The fix probably needs two layers:
1. **Classifier-layer**: don't assume personhood from role names; add a check for "is this party known to be human?" before firing the professional-boundary block
2. **Rule-layer**: refine the collegiality rules so "PM asking for help with team prioritization" is explicitly in-lane, not flagged as Piper acting as a manager

Both are tracked in #1217. Happy to assist with drafting the refined rule language if useful.

— PA, 2026-06-13
