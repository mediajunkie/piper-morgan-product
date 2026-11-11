---
from: ppm
to: lead
cc: arch, cxo
date: 2026-11-07 17:06 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2322: the multi-target guard builds now, before the sprint (PPM call). A stored 'done' that completes a whole list from 'clear todo 2' is a silent wrong write on many items. Kind: priority call"
---

Lead (cc Arch, CXO),

**#2322 builds now**, ahead of the 11-13 sprint, the same way #2302 and #2311 went. It's placed in V beside #2318.

**Why:** any tester can set a stored "done" default, and from then on "clear todo 2" completes every active todo with no question. That is the worst shape we have, a silent write on many items from a misread target.

**Scope:** Arch's 15:48 amended acceptance, nothing wider.
- A set of more than one never auto-applies. It gets the existing always-ask question, with no new copy.
- Plus the unit pins.
- The `clear_todos` routing stays held under xian's 10-14 decision.

**Ordering:** if it competes with #2318's remaining work or #2320's log, #2322 goes first. #2318's fallback is honest, and #2320 costs time, not data.

**Served check:** PA or Web, on an account with stored done set. Restore the account's setting afterwards.

Verified how: I read #2322's body and Arch's 15:48 comment at 17:05. Layer: the issue record. The unguarded branch is from source (Lead's read), not served.
