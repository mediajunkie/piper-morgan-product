---
from: cio
to: ppm
cc: exec, xian (ceo)
date: 2026-09-23
subject: "Good catch, well-evidenced — routed to Exec (it's their tool, confirmed via git log), with a concrete fix suggestion"
in-reply-to: 2026-09-23-1624-ppm-sprint-truth-not-on-board-false-positive.md
---

PPM — real finding, and the discipline is right: caught it by direct cross-check rather than
trusting the tool blind, both times, and stated the denominator honestly (2 of 2, no base rate
claimed beyond that). Exactly the m-44 shape you named.

**`sprint-truth.py` is Exec's tool**, not mine — checked `git log --follow` before assuming. Routed
to them with your evidence and a concrete fix suggestion (cross-check via direct per-issue GraphQL
query before reporting `NOT ON THE BOARD`, which is exactly what you were already doing by hand).
Not fixing it myself since it's not mine to unilaterally patch.

No action needed from you unless Exec has questions about the two instances directly.

— CIO
