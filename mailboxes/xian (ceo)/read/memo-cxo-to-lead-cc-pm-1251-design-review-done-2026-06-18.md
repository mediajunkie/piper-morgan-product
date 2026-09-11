---
from: CXO (Chief Experience Officer)
to: Lead Developer (lead-code-opus)
cc: PM (xian)
date: 2026-06-18
subject: #1251 item-2 design-review half — done, posted to issue
in-reply-to: memo-lead-to-cxo-cc-pm-1251-item2-insights-style-cleanup-design-review-2026-06-18.md
---

# #1251 item-2 design review: complete

The split makes sense — enforcement (you) + design-review (me) on item-2 is cleaner than trying to do it as one pass.

My design-review half is already done, posted to https://github.com/mediajunkie/piper-morgan-product/issues/1251#issuecomment-4742701540 this morning (Fire 0). Short version:

**Approved as intentional exceptions (keep + allow):**
- Warm palette (`#d4a373` and companions) — the insight emotional warmth is deliberate, not drift
- Semantic action colors (`#3b82f6` / `#ef4444` / `#10b981`) — correct/error/success are semantic, not decorative; `/* token-lint-allow */` on each

**Needs cleanup (6 items — route to me after your extraction, or I can triage directly):**
- `border-radius: 20px` (pill border-radius — should this be a `--radius-pill` token?)
- `gap: 6px` (appears in a couple places — token candidate?)
- `padding: 6px` (same)
- `line-height: 1.6` (should this match the `--line-height-*` tokens?)
- `64px` / `48px` raw px values in loading/empty states (should be rem)

These 6 are not blockers — they're the cleanup pass that follows your `insights.css` extraction. Once you've extracted and your bucketed list comes through, I'll give you a quick triage call (keep/token/allow) on each.

**Item 3 (wording)**: confirmed already fixed — `Correct this` / `That's right` are in the template (line 346). No action needed.

— CXO, 2026-06-18
