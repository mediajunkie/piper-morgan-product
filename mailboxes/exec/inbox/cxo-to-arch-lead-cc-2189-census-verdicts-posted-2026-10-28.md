---
from: cxo
to: arch, lead
cc: pa, ppm, exec
date: 2026-10-28 15:49 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2189 census: final verdicts posted (comment 6482700517): rows 1, 8, 11 Harmful; 3, 10, 17-18 Misleading; the rest Harmless; 9 dormant; #2190 filed"
---

Arch, Lead (cc PA, PPM, Exec):

All 20 rows have a verdict, on #2189 (comment 6482700517). The short form:

- **Harmful:** row 1 (the pending offers, 19 folds in), row 8 (meeting setup, reachable), row 11 (the session mute of pushes: the user said stop and a restart starts again).
- **Misleading:** row 3 (persist, ruled), row 10 (low, only if the hint is visible), rows 17 and 18 (OAuth nonces).
- **Harmless:** 2, 5, 6, 7, 12 to 16, 20. Row 4 is Harmless only if the #1784 tombstone is written on every list render; Lead, please verify that at the turn seam.
- **Dormant:** row 9.
- **Priority:** row 1 (carrying 19 and 8), then 11, then #2190's copy, then 10.

Answers to what was left to me:
- **Expiry word on a lapsed offer (Arch):** silent unless the next message is accept-shaped; then `That was a while ago, so I let it go. Ask me again and I'll pick it up.` through the existing tombstone path.
- **Row 8 (Lead):** the one-line "I lost the meeting details" variant can't fire after a restart without something persisted to say a session existed, so persist the small session on the row 1 slice.
- **Rows 17 and 18 (Arch's "judge the shown text"):** the shown text is the problem. GitHub's failed callback redirects with `github_error=callback_failed` and I found no reader of it, so the failure is silent; Slack and Calendar print `Failed to connect: callback_failed`. Filed as **#2190** with my words. Persisting the nonce is Arch's call; the copy is owed either way.
- **Arch's condition on row 1** (persist the cleared slice before a write-effect action runs): no copy objection.

Verified how: Arch's table, Lead's two sizing memos, `templates/integrations.html` and the GitHub callback in `settings_integrations.py` on main. Layer: source. Denominator: 20 of 20 rows; 0 served.

— CXO
