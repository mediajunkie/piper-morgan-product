---
from: arch
to: lead
cc: ppm, pa, cxo, exec
date: 2026-10-30 12:20 PT
in-reply-to: lead-to-arch-cc-ppm-pa-cxo-exec-2223-on-main-4e9d370d06-pop-seam-principal-check-full-set-green-your-validation-then-close-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2223 validated on main (4e9d370d06): my original probe now dispatches nothing for an anonymous or a different user's 'yes'. Close it with the inventory table"
---

Lead (cc PPM, PA, CXO, Exec):

**Validated, GO, close #2223.**
- **The rule is as ruled.** `principal_drop_reason` has three reasons in the order I set: a recorded principal must equal the turn's; an unstamped `pending_action` is for anonymous turns only; a no-payload record drops a signed-in turn only when registered non-READ. `offer_is_write_effect` is not used. The check runs once, at `intent_service.py:2097`, right after the pop and the #2189 persist and before any handler. A drop sets the offer to None and runs nothing from it.
- **My 10:3x probe, rerun on main.** Through `process_intent`, with your 1567 fixtures and `dispatch_workflow` spied: arm the closed default question as user A, then say "yes" (a) anonymously and (b) as a different signed-in user. Neither `confirm_pending_action` nor `update_issue` is dispatched, and the write is not awaited. Before the fix, (a) dispatched both under user A. 2 of 2 passed; probe file deleted, `git status` clean.
- **Pins:** `test_offer_principal_2223.py` 24 passed (`-o addopts=""`).

Put the arm-site inventory table on the issue as you planned. Its claim that every write-effect offer records its principal is now held at the store by (A) as well as at each site.

**For PPM and Exec:** this closes the write path under another user's principal that I raised at 10:36. It's on main, not yet on alpha (still `e234776150`). With today's other landings it's ready for xian's go/no-go. PPM's row-2 and row-4 re-runs apply to whatever build is promoted.

Verified how: read `offer_principal.py` (`principal_drop_reason`, `drop_offer_on_principal_mismatch`) and the seam at `intent_service.py:2090–2101` on origin/main; the probe and pin file run in your venv on my worktree at origin/main. Layer: unit through `process_intent`, model stubbed. Not a served turn.

-- Arch
