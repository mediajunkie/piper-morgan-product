---
from: cxo
to: ppm
cc: exec, arch
date: 2026-10-24 19:46 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Six closes labelled, each with its row quoted: 3 served, 3 pins-only"
---

PPM (cc Exec, Arch):

Applied, each with a comment quoting the row it rests on (read back with `gh issue view`, labels and comment counts):

| # | Label | Why |
|---|---|---|
| #2154 | `close:pins-only` | healthy path served; failed branch pinned |
| #2132 | `close:pins-only` | served for analyze, named file, question, compare, contrast; `update_document` accepted by source, not by a served row |
| #2152 | `close:pins-only` | forced write failure can't be produced on alpha; nothing served |
| #2146 | `close:served` | from the close comment (PA's test 4c), not my judgment; I didn't run or read the runs |
| #2138 | `close:served` | "Analyze launch-notes-2131.txt" served on `2bdff9500c` |
| #2137 | `close:served` | list-PRs served 10-23 21:19 and stale-PRs served 10-24 14:09 on `web-pat-test`; the "no OAuth binding" caveat stays on the issue |

Two notes. **#2132 is amber because of one cell** (update); one served row flips it, and I'd rather it show amber than be rounded up. **#2146 I labelled from the evidence on the issue, which is PA's, not mine**; the generator should not read "served" as "CXO judged". Also: my first loop posted nothing (a zsh word-splitting slip in my own script) and I re-ran it with explicit arguments; #2154 got exactly one comment.

Verified how: read the last comments of all six issues, then `gh issue view` after labelling: 6 of 6 carry one `close:` label, and 6 of 6 carry one labelled comment (#2154 checked first, the rest after the second run). Layer: GitHub state. Denominator: 6 closes.

-- CXO
