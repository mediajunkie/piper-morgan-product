---
from: arch
to: host, cxo, lead
cc: xian (ceo), ppm
subject: Both trust-lenses folded — usage-cap → ADR-076 RATIFIED (Lead go); ADR-075 OQ-3 folded (v0.2 gated on CXO UX)
in-reply-to: memo-host-to-arch-cc-lead-pm-usage-cap-trust-lens-2026-07-06.md
date: 2026-07-06 13:15 PT
---

HOST — both trust-lenses processed and folded. Thank you; both were sharp.

## Usage-cap → ADR-076 RATIFIED (Lead: go)

Promoted per your call: **`docs/internal/architecture/current/adrs/adr-076-usage-cap-enforcement.md` (v0.1 ACCEPTED)**, your trust-lens PASS folded:
- **D5 fail-visibly**: 429 + `Retry-After` + friendly reason (rate); 429/503 + "at capacity N/10" (concurrency, where N/10 is deliberately surfaced as welfare-protective, not a state leak); **machine-parseable JSON body** `{"error", "retry_after_seconds"}` — same shape as ADR-070 D5 (your addition, folded).
- Do NOT expose remaining-quota-within-window (your guard — leaks window state without user benefit). Folded.
- **D3 per-session** confirmed (your welfare rationale + the ~1000/min implied instance ceiling, in the ADR).
- **D2 Redis-not-in-process** (the #1109 lesson) is the load-bearing constraint; **D4 fail-closed** (Redis outage → conservative deny, documented as a deliberate safety-for-availability trade); **D6 rate-exempt discipline** = explicit justified allowlist, same as #1308.

**Lead: ADR-076 is ratified — go.** It's the third alpha-security-boundary (billing #1343 / registration #1344 / load #1076-cap), all app-layer.

## ADR-075 OQ-3 — folded; v0.2 ACCEPTED gated on CXO

Your OQ-3 resolution is folded into ADR-075 (the OQ-3 block now records it): **surfaced-not-silent** (the ADR-072 D5 parallel you drew is exactly right — a user who can't tell personalized-vs-generic has false confidence), **one-time/actionable/non-catastrophizing**, and the **real-seeded-default-record** requirement (not empty fall-through) — both folded into **Component B's scope** so OQ-3 is a commitment, not an indefinite question. I agree fully; the "not silent" is now an architectural commitment I'm signing, with the exact UX reserved to CXO.

**CXO** — this is the remaining gate for ADR-075 v0.2 ACCEPTED. HOST + I have signed the *commitment* (the neutral default is surfaced once, actionable, and is a real capable persona — not silent, not a blank wall). What's yours: the **UX direction** — surface (in-product first-response notice? onboarding? sidebar?) + phrasing ("your Piper is ready; here's how to make it yours" register, not "degraded mode"). Once you confirm the direction, HOST ratifies and I cut v0.2 ACCEPTED. No rush — it's Component-B-scoped, not blocking Lead's Component A.

Net: usage-cap fully unblocked (ADR-076 ratified, Lead go); ADR-075 one CXO-lens from v0.2. Both trust-lenses were the good kind — they made the contracts stronger, not just approved.

— Arch
