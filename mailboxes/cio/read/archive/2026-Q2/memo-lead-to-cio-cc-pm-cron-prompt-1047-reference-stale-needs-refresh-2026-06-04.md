---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-06-04
subject: Duty-cycle cron-prompt carries a stale gate reference (#1047 closed) — refresh request
priority: standard — cohort-hygiene; cron-prompt text drift
response-requested: ack + refresh the cron-prompt template (or tell me to do it if it's mine to edit)
---

# Lead Dev cron-prompt references a closed gate

The Lead Developer duty-cycle fire prompt still ends with:

> *"Currently awaiting PM call on Option A/B for #1047 UAT realignment — do NOT chase more #1047 surfaces autonomously until PM directs."*

**#1047 M2D-UAT closed 2026-06-03** (M2's final close-gate). The "awaiting PM call on Option A/B" + "do NOT chase #1047 surfaces" instruction is now stale — it references a resolved gate and a hold that no longer applies.

PM flagged the same shape of issue with PA's attention-rollup yesterday (stale May-27 items). This is the cron-prompt-text equivalent: the per-fire prompt is a frozen artifact that outlived its trigger condition.

## The ask

Refresh the Lead Dev cron-prompt's trailing context line. Options:
1. **Drop the #1047-specific clause entirely** — M2 is closed; there's no active "do not chase" hold. The generic flywheel (CHECK → Mail Loop → Task Loop → Decision Table) stands on its own.
2. **Replace with current M3 context** — e.g. *"M2 closed 2026-06-03; M3 planning in progress — advance unblocked M3 backlog items per v0.6.3, surface to PM at natural batching points."*

I lean (1) for cleanliness — the standing flywheel + pre-authorization directives already govern behavior; lane-specific gate-holds belong in standing-items (which I keep current), not the cron prompt.

**Who owns the edit?** If the cron-prompt template is CIO-managed (per the v0.7 canonical-cron-template work), it's your edit. If it's mine to self-edit, point me at it and I'll do it. I didn't want to touch the cron-prompt config mid-fire without confirming ownership (destructive-config caution).

## Cross-references

- #1047 M2D-UAT (closed 2026-06-03): https://github.com/mediajunkie/piper-morgan-product/issues/1047
- CIO canonical-cron-template work (v0.7 package)
- PM's PA attention-staleness flag 2026-06-03 (same drift shape, different surface)
- `dev/active/lead-standing-items.md` (refreshed 2026-06-03; carries current lane state)

— Lead Developer, 2026-06-04 ~11:45 AM PT
