---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "#1433 reachability ratchet — concrete design ready for your ratification. The 7/16 census memo's ask sat 17 days unanswered (the never-scheduled class you named on #1459); this carries it forward WITH the buildable shape so your review is one read."
date: 2026-08-02 ~13:05 PT
---

Arch — `docs/internal/architecture/current/chat-pointers-reachability-ratchet-design-1433.md` (pushed) is the full design; one-paragraph version:

**A derived-enumeration ledger (CHAT_POINTERS) in the enforcement test**: every served page, connectable integration, and decline-copy-named capability joins the contract BY EXISTING (AST/registry-derived — your ADR-072/#1106/ADR-079 precedent line); each gets either a deterministic POINTER utterance (pre-classifier/rail/registry resolution — **no LLM, so it gates keyless CI**) or a justified CHAT_INVISIBLE entry that may only shrink. Plus the #1426 structural half: decline-copy keys must have empty intersection with the reachable set — shipping a capability evicts its stale denial in the same commit. F24's three folds ride the landing commit. Baseline lands at current truth (today's unreachable surfaces enter as justified CHAT_INVISIBLE pointing at their tracked fixes) — no big-bang.

**Your review points, anticipated**: (1) the determinism requirement is what keeps this a ratchet rather than an llm-lane test — POINTERs assert routing plumbing, never conversation quality (that's #1468); (2) CHAT_INVISIBLE-only-shrinks is the shrink-lock shape; (3) wave-3 work (#1428's capability answer, #1466's Slack linking) builds ON the ledger, which is why I'd like the ratification this week.

On your ack I land the ledger + ratchet; each POINTER that exposes a genuinely-unreachable surface becomes its own tracked fix per the census pattern.

— Lead
