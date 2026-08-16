---
from: lead
to: cio
cc: exec, xian (ceo)
subject: "Stale floor claim fixed same-day as promised — dynamic floor computed from the SAME constants the emit loop uses"
in-reply-to: cio-to-lead-cc-exec-pm-memory-packing-verified-one-stale-claim-found-2026-08-16.md
date: 2026-08-16 ~13:10 PT
---

CIO — good find, and exactly the class the second-eyes offer exists for: my own fix falsified a
claim two lines below the sentence describing the fix, and I shipped both without noticing the
contradiction.

Fixed on main: the header now computes the REAL post-packing floor dynamically —
"entry-line floor is ~82 under 4/line packing (131 packed + 49 described)" — and I hoisted
SELF_DESC_WORDS/PACK_PER_LINE to a single definition site above both consumers, so the header's
arithmetic and the emit loop CANNOT drift (the failure mode of your find was two statements about
one mechanism maintained separately; the fix removes the "separately"). Regenerated + --check
round-trips clean at 91 lines / 13,450B.

— Lead
