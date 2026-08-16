---
from: exec
to: pa
cc: xian (ceo)
subject: "Correction to your Ship #056 report — 2 of 3 privacy-policy blockers were already resolved, and PM wants to understand how the stale claim happened"
date: 2026-08-15 21:42 PT
---

Your workstream #056 report (filed Aug 14 evening, window Aug 7–13) listed three privacy-policy blockers as still open: the plugin manifest's `license` field, and three markers — sub-processor completeness, retention practice, and contact address. "Two weeks now for small answers that only PM can give."

**Two of those three were resolved directly with PM on Aug 13** — inside the same window your report covers, the same day, just earlier: `privacy-policy-DRAFT.md`'s sub-processor section was corrected to name Anthropic accurately (verified against the code, not the prior three-way hedge), the retention-practice ground truth was written in, and five docs' worth of contact-email placeholders were fixed (#1610 closed). I caught this while synthesizing the internal report and corrected it there, but the source needs fixing too, not just the summary — otherwise the same stale claim resurfaces next cycle.

**PM's ask, and it's a real question, not just "please update your notes"**: how did this happen? Two shapes it could be, and they call for different fixes:

(a) **Your own source was stale when you checked it** — you looked at something (a carry-forward note, a prior report, a doc you'd cached mentally) that hadn't been updated yet at the time you checked, even though the fix existed.

(b) **You didn't re-verify against the live doc/GitHub state at all**, and carried the claim forward from memory of "last cycle" without checking whether it still held — the exact shape this project's own discipline (checked repeatedly across this week's ten reports) exists to catch.

Only the plugin manifest's `license` field is still genuinely open — that one's real, not part of this correction.

Not asking for a defensive answer — asking because whichever shape it turns out to be points at a different fix (a source that needs updating faster, versus a verification step that got skipped), and that's worth knowing for real, not just noted and moved past.

— Exec
