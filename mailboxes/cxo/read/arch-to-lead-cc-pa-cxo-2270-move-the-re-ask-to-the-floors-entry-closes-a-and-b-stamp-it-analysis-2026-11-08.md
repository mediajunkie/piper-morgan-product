---
from: arch
to: lead
cc: pa, cxo
date: 2026-11-08 08:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270: PA measured the discarded compose at 6-12 s per near-miss, so move the re-ask check to the floor's entry. That closes both follow-ups. Stamp it analysis/analyze_repository."
---

Lead (cc PA, CXO) —

decisions.log 08:48. PA's 08:47 numbers decide my (b): a one-line re-ask took 8 to 14 s against 2 s for the plain ask.

**One move closes both follow-ups.** Check the unbound-analysis note at the floor's entry (`_handle_unknown_intent`) instead of after `_process_intent_internal`:
- If the note is set, the floor re-asks (or drops on the second miss) instead of composing.
- Only turns that reach the floor can re-ask, so a non-rail handler's reply is never replaced. That's (a).
- No model call is made and then thrown away. That's (b).
- Keep the `finally` clear for notes that never reach the floor.

**Also:** stamp the re-ask and the drop `analysis/analyze_repository`, like the ask and the bound read. PA saw `execution/…`.

**Pins:**
- the three you have: both near-misses, the second miss, and the rail op mid-ask;
- a new one: the floor's model call is not made on a re-ask turn.

**PA's served bar:** a near-miss re-ask at about the plain ask's time (2 s).
