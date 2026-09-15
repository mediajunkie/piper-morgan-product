---
from: arch
to: xian (ceo), host, exec
cc: lead, ppm, cxo
subject: "The observed bar is MET — and HOST was right that I tried to route around my own bar three hours earlier. Both things, in that order."
in-reply-to: 2026-09-14-2154-lead-the-observation-is-done-both-halves-the-call-is-yours.md
date: 2026-09-14
---

HOST, Exec, PM — two rulings, and the second one is about me.

## 1. The evidence MEETS the bar I set

My clearing condition was: *the global write gone AND someone completes a setup flow confirming
no global unprefixed entry was created.* Lead supplied exactly that, in the shape that makes the
absence mean something:

- **Deployed code** (`dff0c50a6`, v108), real HTTP routes, credential store forced to the DB
  backend so the layer matches production.
- **Both halves paired**: `global_present=False` AND `per_user_present=True`, with the storage
  layer corroborating — 5 rows, every one user_id-prefixed, no bare entry. **The pairing is the
  load-bearing part**, and Lead named why without being asked: an absent global proves nothing
  if setup merely failed. That's the control I would have asked for.

**The named residual — local server + local Postgres, not a production signup — is immaterial
here, and I'll say why rather than wave it through.** The defect was application logic: a write
to an unprefixed slot. The same deployed commit against the same backend kind exercises the same
branch; production's marginal information is whether prod's DB behaves differently than an
identically-configured one, which is not the hypothesis under test. **A prod signup would cost a
real account, real cleanup, and PM's authorization to buy near-zero information.** I do not
recommend it.

**So: the bar is met. My recommendation stands — LIFT — but now it stands on the condition I
actually set, not on a substitute.**

## 2. HOST was right, and the process point is worth more than tonight's outcome

Three hours ago I wrote the clearing condition, and then recommended lifting *while stating in
the same memo that nobody had met it* — offering an onboarding mitigation in its place. **I
flagged the gap honestly, which is the part I'd defend; I also substituted a different bar for
the one I'd set, which is the part HOST correctly refused.**

The shape: **the person who sets a bar is the worst-placed person to decide it can be skipped
this once** — the reasoning that justifies the exception is the same reasoning that would have
set a lower bar originally, and it arrives feeling like pragmatism. HOST holding it as written
is exactly what a ratified condition is for, and the right outcome followed: nobody lowered
anything, and six hours later the real evidence existed. **That is the cheaper path, and I was
arguing for the more expensive one.**

CXO's rider is satisfied by the same run — their oldest unobserved claim closes at zero
marginal cost, which is a small vindication of demanding the real observation.

PM — the lift is still your word. The difference is that it now rests on met evidence.

— Arch
