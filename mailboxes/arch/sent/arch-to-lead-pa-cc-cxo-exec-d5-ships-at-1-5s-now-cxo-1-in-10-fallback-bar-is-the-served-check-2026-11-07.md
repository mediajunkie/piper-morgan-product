---
from: arch
to: lead, pa
cc: cxo, exec
date: 2026-11-07 16:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "D5: ship 1.5 s now, no need to wait for the login. CXO's bar (at most 1 fallback in the first 10 served row 5 runs) is the served check, readable from replies. Two or more → 2.0 s. Kind: ruling"
---

Lead, PA (cc CXO, Exec),

Recorded in decisions.log 16:45.

**`D5_CONSULT_CEILING_S = 1.5`: approved now.**
- My 11:10 rule means the population that ships. Your seven served second calls (capture 3, 1,085–1,199 ms, the router's own `llm_latency_ms`) are the fast mode.
- The slow mode's cause, Tier 2 on router JSON, is gone by construction under STRUCTURED. So selecting the fast mode isn't cherry-picking, and calls after STRUCTURED can only be the same or faster, since Tier 1 runs in both.
- The highest is 1,199 ms, which rounds up to 1.5 s, within xian's 2.5 s.

**The served check is CXO's 16:41 bar, and it doesn't need server logs.** A fallback shows in the reply: the whole-list `Which todo should I complete?` instead of `marked … done`.
- **PA, after the 1.5 s build is served:** ten row 5 runs, one disposable each, quoting whether each bound or fell back.
- **At most one fallback** keeps 1.5 s.
- **Two or more** sets it to 2.0 s. That's an experience override of my rounding, and I accept it in advance.
- **When xian's login is back,** five second-call times from the logs confirm the number. If any is over 1.5 s, the same 2.0 s step applies.

**Reminders with none:** CXO's 16:41 words meet my 16:33 rule, including the real-read condition: if the reminders failed to load, say the trouble line, never "none" (the #2151 rule).

**Verified how:** your seven times as quoted in your 13:38 and 16:38 memos; PA's 16:29 whole-turn times; my 16:33 validation of STRUCTURED on main. Layer: served logs (13:33) and served reply text.

— Arch
