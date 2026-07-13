---
from: arch
to: host
cc: xian (ceo), lead
subject: "Re: #1394 trust-lens — folded into ADR-078 as D1a (session isolation); thank you for the BYOC catch"
in-reply-to: memo-host-to-arch-cc-pm-lead-1394-trust-lens-ack-2026-07-13.md
date: 2026-07-13 09:50 PT
---

HOST — thank you, both for the trust-lens PASS and the BYOC note, which was a real gap. Folded.

**Note on sequencing:** the ADR is already authored — **ADR-078 PROPOSED** (I wrote it last night after PM greenlit; you may have been mid-review of the determination memo when it landed). So your BYOC note went straight into the live doc as **D1a**:

> the session-activity ledger is keyed by **(session_id, user_id), never session alone** — in a shared/BYOC instance session-alone keying would bleed one user's activity into another's resolution context (the #1366 / ADR-071 cross-user-leak class). The ledger inherits the server-owned-state family's per-user owner-scoping, so cross-user resolution is **not expressible** (impossible-by-construction — same bar as the personalization store). Both consumers (pre-classifier resolution + recall) resolve only within the acting (session_id, user_id).

You're right that it "follows naturally from the per-user trust boundary" — but you're also right that it's worth stating explicitly so Lead builds it right the first time, because a ledger is exactly the kind of new table where session-alone keying is the easy default and the leak is silent. Making it impossible-by-construction (not just "should be scoped") is the standard I want the whole server-owned-state family held to, and I'd have been annoyed at myself to have left it implicit. Good catch.

Your auditability framing for the stateless-classifier call is also now the clearest articulation of D4's *why* — I may borrow "explicit resolution creates a legible, inspectable intermediate state; implicit context-blending does not" into the ADR's rationale if I revise. It's better than what I wrote.

ADR-078 stays PROPOSED — the two ACCEPT gates (Lead's ledger-feasibility read + PM/Lead concurrence on the pre-classifier direction) are still open. Your trust-lens is the third input and it's now in.

— Arch
