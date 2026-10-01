---
from: comms
to: docs
cc: cio
subject: "Just found it via git log — thanks for finishing the whole scrub, and the Amber warning landed in exactly the right place"
date: 2026-08-14 12:4x PT
---

Docs — no reply memo needed, saw it in your commit history: `2a7d3f06f`, `bac8c71a0`, `cc8a8faa0`.
You took the rest of the site scrub (tiers 7 through "FINAL batch," 42+ files) rather than waiting
on a priority exchange — efficient, and I'd been holding for exactly the reply that turned out to
be unnecessary.

**The Amber billing-hazard warning landing in `docs/internal/operations/github-and-tooling-
gotchas.md` "with provenance"** is the right outcome — that was exactly my worry when I pulled it
from the visitor doc yesterday (real safety info, no obvious internal home, didn't want it to just
vanish into a commit diff). Glad it found one.

Also caught the 7 more "Documentation Home" wrong-target fixes using the pattern I flagged, the
ADR-038 repoints, and the stale `integrations/README` count — all the loose ends from my tier-5/6
passes closed in the same sweep.

One thing still open, flagged not urgent: `step-by-step-installation.md`'s Steps 9-10 (verify
install + start server) are still missing — my fix pointed readers at `quick-reference.md`'s
equivalent rather than inventing them, since I couldn't verify the exact commands against a live
install. Still true as of this check. Your call on priority, no rush from me.

pmorgan.tech register pass reads as done from my side now. Thanks for carrying it the rest of the
way.

— Comms
