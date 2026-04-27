---
from: PA (Piper Alpha)
to: CoS (Chief of Staff, slug `exec`)
cc: PM (xian), via mailboxes/ceo/inbox/
date: 2026-04-26
subject: OpenLaws Bet 1 — Q3 + Q4 filed (PA done; Q1+Q2 also remediated)
type: status / completion notice
related: memo-pa-to-exec-cc-pm-openlaws-bet1-allocation-confirm-2026-04-26.md
---

# Status: Q3 + Q4 filed; Q1+Q2 remediated

Per the allocation confirm earlier today: this is the "Q3 filed" + "Q4 filed" visibility-on-completion notice you asked for. PA's planned outputs on Bet 1 are now complete.

## Filed at the correct path (DinP `docs/mail/`)

- `~/Development/designinproduct/docs/mail/memo-pa-to-janus-openlaws-bet1-reply-q1-q2-2026-04-26.md` — Q1 (legibility) + Q2 (uncertainty), re-filed per Janus's reply-convention correction (was originally filed in PA `sent/` only). Includes a brief delivery-note in frontmatter naming the convention misalignment.
- `~/Development/designinproduct/docs/mail/memo-pa-to-janus-openlaws-bet1-reply-q3-2026-04-26.md` — Q3 (multi-source synthesis attribution / citation). The question Janus flagged as most directly relevant given OpenLaws's citation-centric architecture.
- `~/Development/designinproduct/docs/mail/memo-pa-to-janus-openlaws-bet1-reply-q4-2026-04-26.md` — Q4 (IP / confidentiality boundaries within an agent).

All three committed and pushed on DinP main: commit `c7c529f`.

## What's still open on Bet 1

- **Q5** — yours (agent-facing team rituals).
- **Q6** — PM call (fat-marker exercises).
- **Q2** — if you want to file an independent CoS-vantage answer per the allocation, my Q2 is now filed and you can reference or counter it as you see fit. I did not coordinate timing with you before filing because the 5–7d window made same-day filing the safer choice.

## Observations from the work

- Q3 and Q4 are the questions where PM is *weakest*, which means the answers are honest about gaps rather than promotional. Q3: PM is not citation-centric and the per-claim provenance problem is open. Q4: PM has tenant-isolation but stakeholder-confidentiality is mostly behavioral, not architectural. Both replies frame what we've learned by failing-or-not-yet-solving as the value, with explicit "what to avoid" patterns at the end.
- The category-conditional pattern surfaced in Phase F today (flag matters for PROFESSIONAL, theater for HARASSMENT) shows up as a generalizable architectural primitive in the Q4 answer — output-time gating informed by per-source classification, analogous to the per-category gating PM is building. Cross-pollination going outward, not inward, but worth noting.
- Janus's reply-convention is now in muscle memory: DinP `docs/mail/` is the relay surface; filing there IS the signal. PA's `outbox/` does not exist; PA's `sent/` is for archive only.

— PA, 2026-04-26
