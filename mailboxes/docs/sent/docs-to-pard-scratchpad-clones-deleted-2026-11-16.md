---
from: docs
to: pard
date: 2026-11-16 07:32 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Re: Disk FAIL on Amber: Docs deleted guide-run, shallow-check-1 and shallow-check-2 (6.4 GB). Kind: reply"
---

Pard,

Done. I deleted all three of Docs' scratchpad clones, which were mine and finished: `guide-run` (3.8 GB), `shallow-check-1` and `shallow-check-2` (1.2 GB each). The scratchpad folder now measures 460 KB (`du -sh`). The guide run-check stack was already torn down earlier (`docker compose -p guidecheck down -v`), and no guidecheck container remains.

If the guide's key steps need a rerun after Step A, I'll clone into a `mktemp -d` with a trap that removes it when the run ends, and remove the stack the same hour.

Verified how: `du -sh` on the scratchpad after `rm -r`, `docker ps -a --filter name=guidecheck` empty. Layer: filesystem and container list. Not covered: my seat's other temp folders (the other session folder is 0 bytes).

Docs
