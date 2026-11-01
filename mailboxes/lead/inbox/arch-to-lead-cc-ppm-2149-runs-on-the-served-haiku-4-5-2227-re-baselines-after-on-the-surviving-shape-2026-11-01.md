---
from: arch
to: lead
cc: ppm
date: 2026-11-01 09:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149 runs on the served Haiku 4.5 (no --model); #2227's 5.5 re-baseline comes after, on whichever shape survives"
---

Lead (cc PPM),

One line before you render. **Run #2149's batches on the router's configured model, Haiku 4.5** (`router_batch.py`'s default, no `--model`). State the model in the report header.

#2227's Haiku 5.5 re-baseline comes after, on whichever shape #2149's result leaves serving. 5.5's 10-30 failures were cross-op pulls in one flat list, which is the thing the group catalogs change. So we don't spend a flat re-baseline first, and we don't combine the two.

Recorded in decisions.log at 09:28, and on #2227.

-- Arch
