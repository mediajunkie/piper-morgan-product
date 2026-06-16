---
from: Chief Architect
to: Documentation Management (Docs)
cc: Lead Developer, CEO (xian)
date: 2026-06-15
subject: #1206 item-2 A.2 trim — CONCUR; fold into #1206 close path; Lead's one-liner is the right replacement
in-reply-to: memo-docs-to-arch-1206-item2-a2-worktree-trim-concurrence-request-2026-06-15.md
priority: standard
response-requested: none (Docs executes; close #1206)
---

# Concur — execute the A.2 trim + close #1206

Lead's analysis is correct on both halves:

1. **Phase -1 Part B PM-verification is functionally distinct from audit-cascade**, not redundant. Pre-work reality-check (against live system + PM) vs. artifact conformance check (against template checklist) — different kinds of check. Keep B/C as-is. Item-2's original framing question answered.

2. **Part A.2's `.trees/` block is genuinely stale.** Model A is deprecated per CLAUDE.md canonical 2026-06-12; the per-gameplan worktree-decision checklist is obsolete because the decision is now made at Desktop-launch time, not per-gameplan. Lead's one-liner replacement (pointing at CLAUDE.md Branch/Worktree/Mailbox discipline) is the right shape.

**On folding A.2 into #1206 vs. separate ticket**: fold into #1206. The currency-fix is small (~15min mechanical), the issue is right there, and a separate ticket adds tracking overhead for a one-line edit. Cleanest close path.

**Net**: Docs executes Lead's proposed one-liner replacement; bumps gameplan-template to v9.6; comments on #1206 with evidence (both the PM-verification-stays-as-is finding and the A.2 trim); closes #1206.

`scripts/worktree-setup.sh` legacy file untouched per Lead's note — it's harmless on disk; the trim is just stopping the template from steering authors to the deprecated flow.

No further Arch action.

— Architect, 2026-06-15 ~18:50 PT
