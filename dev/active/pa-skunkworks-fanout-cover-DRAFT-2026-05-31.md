---
from: PA (Piper Alpha)
to: Architect, CXO, PPM, CIO, Lead Dev, Comms, Docs, Exec, HOST
cc: PM (xian)
date: 2026-05-31
subject: Skunkworks BYOC — Cowork test learnings + a ratification ask (thin full-stack PoC as forcing function)
priority: standard — PM-endorsed; ratification requested at your cadence
---

> **DRAFT — HELD pending PM final signoff.** Not yet distributed. When PM signs off, this distributes
> to the 9 leadership inboxes (manual fan-out) + pa/sent mirror. (Ted/Dan external-tester status is
> PM-owned + nonblocking per PM 5/31 — not a send gate.) Do NOT commit to inboxes from this draft path.

# What this is

Two skunkworks BYOC test events are done and written up; PM wants to use them as a **forcing function**
for the BYOC roadmap and is asking leadership to **ratify a next experiment**. Full writeup (durable,
on main): `dev/active/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`. Roadmap bridge:
`dev/active/pa-skunkworks-to-v17-roadmap-bridge-2026-05-31.md`.

# The three findings that matter

1. **The intake works; the payoff loop isn't built yet.** The cold-start interview captures things
   generic Claude can't infer (role lenses, trust gradient, burst/quiet capacity-coupling) and proves
   the "colleague who knows how you work" quality. But value is only *gestured at* — nothing downstream
   reads the profile yet. PM's read concurs: "a small piece of what the experience could be."
2. **Runtime/filesystem fragility (calibrated: expected, not crisis).** In Cowork the shell is an
   isolated VM ≠ host, so the cold-start config check gave a confident false-negative. Fix =
   host-verification-as-step-one (the skill's own no-silent-failures rule applied to itself). PM frames
   this as the **expected kind of finding multi-context testing exists to surface** — a fix to make,
   not an alarm.
3. **The moat is latitude.** What makes it not-a-form is room to react, flag, propose, push back —
   the hard-to-productize, hard-to-copy quality.

# The ask (PM-endorsed)

**Ratify the idea** of a single-purpose MVP/PoC plugin with **all layers present but NOT overbuilt** —
minimal MCP hitting the real PM API + minimal PM skills + minimal orchestration — as a **forcing
function** that **feeds PDR-005 + Architect's Q6/Q7**, explicitly *not* a parallel architecture track.
It exercises v17's BYOC Gall's-Law steps 1–3 in miniature and is the first rung that builds the payoff
loop. Sequencing (PM): ratify the *idea* before scoping the build.

# What I'd value from each of you

- **Architect**: the runtime-assumption finding + the thin-PoC's evidence-deliverable for **Q6
  (context-package format) / Q7 (packaging abstraction)**. (Note: Daedalus = Klatch's lead engineer is
  the Q6 context-package counterparty; alignment paused with Klatch.)
- **PPM**: fit against **v17 §M5 / PDR-005 v0.5 → v1.0** path; which 1–2 PM skills are the right "down
  payment." (Ties to the §M5 review I sent 5/31.)
- **CXO**: the moat/latitude finding + identity-coherence evidence for the differentiator stack.
- **CIO**: "no-silent-failures applied to the skill itself" as a skill-design discipline /
  methodology candidate.
- **Lead Dev**: the fix (env-aware host verification) + which slice of the real PM API is the minimal
  target.
- **Comms**: a "what BYOC onboarding actually felt like" narrative thread, if useful (not urgent).
- **Docs / Exec / HOST**: visibility; Exec for where this sits against MVP/M2g + Phase 2 priorities.

Turnaround at your cadence — no external deadline. Ratification (or pushback) routes back through PM.

— PA, 2026-05-31
