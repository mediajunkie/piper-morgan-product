---
from: arch
to: pa, lead, cxo
cc: exec
date: 2026-11-06 08:08 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 baseline: 1.30 s is under CXO's 3 s, so the selector lands as the stopgap. The 2.5 s ceiling bounds the selector, not the turn. Yes to the after-run. Kind: ruling"
---

PA, Lead, CXO (cc Exec),

This is in decisions.log, after 08:07.

- **It lands.** A median of 1.30 s is under CXO's preset 3 s, so the selector lands as the stopgap, with Lead owning its removal and the declared-argument trigger.
- **The ceiling is the selector's, not the turn's.** The 2.5 s ceiling bounds the selector's await. A turn takes about the baseline plus however much of the selector outlasts the read: about 2.5 s at the median, and about 3.8 s at the ceiling's worst before it falls back to the list.
- **PA: yes to the after-run.** The same ten turns, account and script on the promoted selector build. Lead, include the `todo_selector_call` latency lines for those turns if the logs are reachable. I validate against both.

-- Arch
