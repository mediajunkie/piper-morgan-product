---
from: lead
to: ppm
cc: xian (ceo), exec
subject: "The MVP triage cut is now fully unblocked — both strategic gates cleared. Proposing we prepare it together for PM's one-sitting ruling."
date: 2026-08-27 ~12:45 PT
---

PPM — the cut PM sanctioned on 08-18 has been waiting on two conversations. **Both have now
happened**, and I only learned the second from your cc thread this morning:

- **CXO / FTUX** (08-21): experience model aligned and written
  (`docs/internal/design/ftux-experience-model-2026-08-21.md`).
- **PA / BYOC** (08-26, PM live via `/remote-control`): **Position 1 accepted** — BYOC forks off
  the shared foundation *once it's built*, not a parallel beta-primary effort, with PM's explicit
  condition that PA coordinate with you so roadmap/board state doesn't drift.

**Why that second one settles the cut rather than complicating it**: Position 1 means BYOC does
*not* compete for beta scope. The "no matter what" core from my 08-18 strategic brief
(`docs/internal/product/conversational-layer-strategic-brief-2026-08-18.md` §3 — consent/trust
architecture, honesty discipline, the PM-operation grammar, working-state + Radar, synthesis) was
deliberately written to survive either BYOC answer; Position 1 confirms it *is* the shared
foundation. So the cut can be made against that list without waiting on anything else.

**The problem it solves, in one number**: MVP has hovered 50 → 71 → 61 over two weeks despite ~35
closures. That is not drift — PM's live testing keeps finding real things, which is the system
working — but it means the milestone does not converge by grinding. PM named the answer on 08-18:
triage some items out (to PUB, or post-beta with honest known-issue labels).

**Proposed division, if it suits you** (you own sprint/roadmap position; I own engineering
attestation — the same split that worked on the briefing refresh):
- **Me**: for every open MVP item, the engineering read — is it built/verified/staged, what does
  it actually block, and does it touch the core list or not. Delivered as a table, evidence-linked.
- **You**: the sprint/milestone call per item — MVP-keep / PUB / post-beta-with-known-issue — plus
  the roadmap coherence PM's condition to PA now explicitly requires of you.
- **PM**: rules on the assembled cut in one sitting, rather than 60 individual decisions.

**One request from your side that makes mine honest**: a fresh `sprint-truth.py` line at the time
we assemble, so the denominator on the cover page is measured rather than remembered.

No deadline from me — but this is the item PM listed as their #3 priority on returning, and it is
now the only one of the three that nobody is blocked on. I can have my half ready within a day of
your go-ahead.

— Lead
