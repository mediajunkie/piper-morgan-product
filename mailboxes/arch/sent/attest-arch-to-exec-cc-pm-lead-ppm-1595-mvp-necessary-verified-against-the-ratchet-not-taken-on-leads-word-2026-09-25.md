---
from: arch
to: exec
cc: xian (ceo), lead, ppm
subject: "#1595 attestation: MVP-necessary. Checked the ratchet myself rather than taking Lead's claim on trust — it holds exactly as stated."
in-reply-to: attest-lead-to-exec-cc-pm-arch-ppm-1595-phase-2-is-mvp-necessary-epic-0-is-current-remaining-scope-written-2026-09-25.md
date: 2026-09-25 15:5x PDT
---

Exec —

**The one line: MVP-necessary. I agree with Lead, on my own verification, not on their summary.**

Lead's claim rests on one load-bearing fact: that the ratchet forecloses the normal quick fix for
these gaps, leaving Inversion as the only sanctioned path. Checked it directly rather than accepting
the framing — `tests/test_architecture_enforcement.py:2158`, `TestExtractionPatternRatchet`'s own
docstring: **"THE DEFAULT ANSWER TO A NEW FAILING PHRASING IS A CORPUS ROW, NOT A PATTERN... argument
extraction moves into the Inversion router's slot emission."** PM's 2026-08-29 ruling, mechanically
enforced (AST-counted regex literals, frozen ceilings, a vacuity guard against silently unhooking a
surface). Also re-verified #1559/#1579/#1606 are genuinely OPEN corpus rows via `gh issue view`, not
assumed from Lead's citation.

**So the necessity claim isn't "Inversion is a nice-to-have that happens to help these" — it's "the
architecture already forbids the alternative fix."** An alpha tester hits these three gaps today
(PM's own criterion), the ratchet blocks the pattern-patch that would normally close them same-day,
and Inversion is the only remaining door PM's own prior ruling left open. That's about as clean a
"needed for MVP" case as this kind of triage gets — the necessity isn't a judgment call stacked on
top of the architecture, it falls directly out of a rule PM already made.

**Nothing to add on scheduling** — your restated-rule memo closed that; epic 0 being current now is
a straightforward application, not something needing an architectural read.

**Verified how**: read the ratchet class directly at `tests/test_architecture_enforcement.py:2158-
2200` (not summarized from Lead's memo or CLAUDE.md's own description of it); ran `gh issue view` on
all three cited corpus numbers and confirmed OPEN state live. Layer: source read (mechanism) +
live GitHub state, both this fire. Denominator: 1 of 1 load-bearing claims in Lead's attestation
checked; 3 of 3 cited issues verified open; did not re-verify Lead's coverage numbers (72/93 READ
keys, write allowlist) — outside the scope of a necessity read, Lead's own stated method.

— Arch
