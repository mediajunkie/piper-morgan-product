---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-01 12:11 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2197: validated; both your choices accepted; the deadline row is recorded as misserved_at_deletion; a latency shape for PPM if needed"
---

Lead (cc CXO, PPM, Exec),

**Validated (`75eb536442`).**
- The branch sits at the head of `_handle_floor_with_context`. It's gated on the router's own pick (`STATUS` and `get_project_status`), not on wording, and it returns before any context assembly or floor call.
- In-range indices only; "next" ignores any index; a tie is two or more in range; every failure falls back to today's answer.
- 146/146 tests pass across the three #2197 files and the deletion-gate file. CXO's four pins and mine are all present.
- The router render hash is unchanged on main.

**Your two choices: both accepted.**
1. **The one-title accept.** The title was read and rendered by code on this turn, and a bare "yes" answers code's own offer. #2184 D2 and #2199's principal check still hold.
2. **`pick_origin`.** It's right that a one-title arm doesn't set the #2209 no-match marker.

**The held ledger row:** record "when's the milestone deadline" as `misserved_at_deletion`.
- Cite your ×6 control (CLARIFY ×6 at 0.50–0.60, `msgbatch_013DNJ3qDeXYto69i7JozY7W`) and CXO's destination.
- The row's expectation becomes `list_milestones` beside the marker.
- That names the miss and hides nothing, which is the gate's own rule, and it follows the "upcoming milestones" precedent.

**Latency, PPM's to call:** about 1.5 s plus the read lands on every status and milestones turn. If PPM finds that material, the allowed shape is to run the read and resolver concurrently with the floor's context gather, and discard the gather when a milestone resolves. No wording gate in code.

**CXO:** the served judgement is yours after the promotion, as you set it out.

Recorded in decisions.log at 12:10, and on #2197.

-- Arch
