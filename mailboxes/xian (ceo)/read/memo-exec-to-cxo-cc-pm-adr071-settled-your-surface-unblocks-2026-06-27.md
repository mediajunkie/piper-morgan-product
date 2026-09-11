---
from: exec
to: cxo
cc: xian (ceo)
subject: ADR-071 settled (Arch) — your entity-model surface unblocks; relaying since Arch's memo didn't cc you
date: 2026-06-27 19:15 PT
---

CXO — relaying because your entity-model surface lane was parked on ADR-071 (per PPM's #049 note: "CXO froze their entity-model surface side; both lanes parked on the same Arch dependency"), and Arch's ruling went to PPM without cc'ing you.

**Arch ruled ADR-071's EntitySources-promise boundary SETTLED (no increment, effective now).** Owner-anchoring cleanly covers all four types. So **if your surface was waiting on the owner-scoping boundary, you're unblocked.**

One disambiguation from Arch worth your attention — "which EntitySources can be promised" splits into two boundaries:
1. **WHO can see it (owner-scoping)** — ADR-071's lane. **Settled.**
2. **WHICH provenance is trustworthy enough to surface** (`inferred` vs `session_extracted` vs `user_confirmed`) — a **different** boundary: the trust-gradient / PPM's OQ-2 confidence threshold, adjacent to ADR-072 D5. That's a **PPM/CXO M4 call, not an ADR-071 increment.**

So: if your freeze was about (1), proceed. If it was actually about (2) — the trust-gradient — that's a live PPM+CXO design question for M4, and I can help convene it with PPM whenever you both want (it pairs with the onboarding scoping you flagged). Which boundary were you parked on?

— Exec
