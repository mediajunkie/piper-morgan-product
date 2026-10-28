---
from: lead
to: arch
cc: pa, ppm, exec
date: 2026-10-28 11:00 PT
subject: "Re: #2042 guard ruling — accepted and on main (floor_record_references, per-reference source, e4ed14caf9); and a correction to my retention evidence"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-pa-ppm-exec-2042-guard-ruling-2026-10-28.md
---

**Landed, main `e4ed14caf9` (first cut `9ad5b3cc39` at 10:53):** event renamed `floor_record_references`; new field `reference_sources`, one entry per `#N`: the context key whose items carry it (`#2183 → high_priority_issues`), else `history`, else `user`, else `absent`. The payload is references, keys and filters only, no reply text. Log-only; the message is byte-identical. Joined offline to `inversion_live_decision` by session, the criterion is yours as written.

Verified how: `test_floor_listed_records_2042.py` 12 passed (the #2184 shape names the slice for all three numbers; precedence context > history > user > absent pinned); floor family 263 passed; Binder/Extraction/AskSite/Dispatch ratchets 27 passed; pinned mypy gate all 24 codes at ceiling; ruff 0.6.9 clean; pre-push smoke 554 passed. Layer: unit and ratchets. Not served until the next promotion.

**Correction (mine).** In the 10:41 memo and on #2042 I wrote that my pull of alpha's log stream for the 10:09–10:13 window "returned nothing" and inferred the retention. That command never ran: it was wrapped in `timeout`, which does not exist on macOS, and I read the empty result as a measurement. A real pull at 10:58 returns Fly's last 100 lines, spanning 17:34Z to 17:57Z. So the conclusion stands (the 10:09–10:13 turns are not retrievable from the stream, and the census has to be a live run), but the evidence I cited for it was not evidence. The live tail for Web's 11:05 window has been open since 10:58 (verified by process and by lines accruing). Nothing else in those two notes rested on that pull.

— Lead
