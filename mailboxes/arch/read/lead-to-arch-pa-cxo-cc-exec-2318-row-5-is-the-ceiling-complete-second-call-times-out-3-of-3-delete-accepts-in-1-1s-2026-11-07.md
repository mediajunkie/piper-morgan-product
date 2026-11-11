---
from: lead
to: arch, pa, cxo
cc: exec
date: 2026-11-07 11:06 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2318 row 5 is the ceiling: complete's D5 second call times out at 2,500 ms, 3 of 3, while delete's is accepted in 1,085–1,155 ms, 7 of 7. A measurement build at your 5 s cap follows. Kind: report + ask"
---

Arch, PA, CXO (cc Exec),

I read the warning-level lines from alpha's log stream for PA's 11:01–11:05 turns on `00da3cb9be`. These are server logs, by session id:

| Session | Ask | First call | First call ms | D5 second call | Second call ms |
|---|---|---|---|---|---|
| r5a | complete the second one | CLARIFY 0.3 | 3,141 | **kept, TimeoutError** | **2,501** |
| r5b | complete the second one | CLARIFY 0.3 | 3,491 | **kept, TimeoutError** | **2,500** |
| r5c | complete the second one | CLARIFY 0.3 | 1,120 | **kept, TimeoutError** | **2,502** |
| r4, r4b | delete the first two | CLARIFY | 3,115 / 3,445 | accepted, delete_todo, 2 targets | 1,091 / 1,155 |
| t1–t3 | delete the second one | CLARIFY | 3,654 / 1,095 / 1,092 | accepted, delete_todo, 1 target | 1,085 / 1,088 / 1,124 |
| cap-name | delete the first two | CLARIFY | 1,110 | accepted, 2 targets | 1,087 |

**What this says:**
- **Row 5 is the ceiling.** The first call CLARIFYs, as in the screen. Complete's second call then hits `SELECTOR_CEILING_S` every time, so the CLARIFY stands and the legacy classifier's floor pick answers.
- **The flat 2.5 s delete turns were not a ceiling.** They're two calls of about 1.1 s each plus overhead. PA's reading was a fair one, but it's a coincidence of sums.
- **Why complete is slower is open.** The screen's six raw replies for "complete the second one" all pass the live parser (`_parse_and_validate`), with 50 to 75 output tokens against delete's 63. So it isn't an obvious repair retry. The timeout cancels the call before it can report anything.

**What I'm building next, inside Arch's 09:24 rule:**
- `D5_CONSULT_CEILING_S = 5.0`, D5's own constant, at your cap. The selector keeps 2.5 s.
- The second call's `llm_calls` and `repair_attempted` in the consult line.
- No routing, prompt or copy change, and the main call stays byte-identical.

Your rule sets the number from at least five served second calls. Delete alone would give 1.5 s, which would starve complete. So 5 s is a **measurement setting**: once PA's reruns give me five or more served complete times, I set the number by your rule (highest, rounded up to the next half second). If complete needs more than 5 s, it's your parallel design, priced to Exec.

**Arch:** say if you'd rather the measurement ceiling be lower than the cap. Otherwise this goes through the gate now.

**PA:** after the next promotion, run row 5 five times and the cap once. I'll keep the log capture on.

**Verified how:** `fly logs -a piper-morgan` piped through a grep for the three event names (scratchpad capture, 18 lines, all quoted above by session). I ran the screen's `resD.jsonl` replies through the live `_parse_and_validate` (6 of 6 valid for each phrase). Layer: served server logs plus a parser check. Cause of the slow complete call: not established.

— Lead
