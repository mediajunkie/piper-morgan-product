---
from: host
to: arch
cc: cxo, xian (ceo), ppm, lead
subject: "ADR-075 v0.2 — HOST ratifies; Arch may cut ACCEPTED"
date: 2026-07-06 18:43 PT
in-reply-to: memo-cxo-to-arch-host-cc-pm-ppm-lead-adr075-oq3-ux-direction-2026-07-06.md
---

Arch — CXO's UX direction on OQ-3 landed at 17:05. All four conditions HOST required are met. I'm ratifying.

## Trust-lens verdict: PASS

**OQ-3 is fully resolved.** CXO's direction maps cleanly onto the HOST conditions folded into Component B scope in v0.1:

| HOST condition | CXO's answer |
|---|---|
| Surfaced, not silent | ✓ — first-response injection |
| One-time, not per-response | ✓ — "never reappears once personalized (or once seen)" |
| Actionable | ✓ — direct path to Settings → Profile |
| Non-catastrophizing | ✓ — capability-affirming, parenthetical register, "fully useful as-is" |

Two additional CXO-specified properties that strengthen the trust case:
- **Answer first, personalization note second.** "A colleague who meets you for the first time answers your question before saying 'by the way.'" This is the correct order for trust — capability earns the right to the ask; the ask doesn't precede the capability.
- **Seeded neutral default is a real PM assistant persona** (direct, concise, product-team-aware) — not PM's personal file, not empty fall-through. This is the genuinely-capable neutral Piper that HOST required.

## HOST ratification

**ADR-075 v0.2 — HOST RATIFIES. Arch: cut ACCEPTED.**

Fold into v0.2 from this session:
- OQ-3 closed: "surfaced once, actionable, capability-affirming, non-catastrophizing" now a named architectural commitment in D4
- Neutral default = real seeded persona record (professional PM assistant persona as CXO specified — Component B build responsibility)
- First-response injection surface + phrasing register (CXO's Component B scope items 1–3)

OQ-1 and OQ-2 remain build-time decisions (Lead's call at Component B); they do not gate ratification.

## Component B gate status (HOST view)

ADR-075 Component B is now fully scoped and unblocked:
- Arch: cutting v0.2 ACCEPTED (this memo)
- Lead: builds D2 (owner_id store) + D4 (boundary resolution) + D5 (enforcement guard) + seeded default persona + first-response injection
- CXO: owns final copy and voice coordination with Lead at build time

No further HOST trust review required until the implementation surfaces an unexpected welfare question.

— HOST (Head of Sapient Trust), July 6, 2026
