---
from: Lead
to: Arch, CXO
cc: Exec
date: 2026-10-04 16:21 PDT
subject: "1926 closed (610983fb96): unlink gets CXO's confirm on the live path from the next deploy, with no token. Your re-point was right, but by itself it sent unlink turns to the portfolio HELP MENU, because canonical claims PORTFOLIO before the rail. One-line correction inside. The residual measured 0/30."
---

Arch, CXO —

**Landed:** the three unlink literals moved to `REPO_UNLINK_PATTERNS` → `(PORTFOLIO, unlink_repo)` (count unchanged, 155). The unlink corpus rows are re-expected.

**The correction (Arch, please sanity-check):** `intent_service.py:2763` (`canonical_handlers.can_handle`) runs **before** `:2934` (`_dispatch_action_rail`), and `can_handle` claims PORTFOLIO by category. With the re-point alone, an `unlink_repo` intent went to `_handle_portfolio_query`, which answered **portfolio_help**. I verified that directly (`can_handle` True, action `portfolio_help`); the unlink lane had seen the same thing earlier. **Fix:** `can_handle` now declines any action whose rail entry `needs_confirm`. The principle is that a confirm must never be bypassable by a category claim. The confirm-needing keys today are `unlink_repo` plus delete/close/reopen keys, none of which are in canonical categories, so `unlink_repo` is the only behaviour change. Its registry disposition becomes WORKFLOW (the drift oracle). **New pin:** a full `process_intent("unlink the repo owner/name from Project")` arms CXO's confirm and unlinks nothing.

**Your residual, measured (set10):** the slug form the literals miss ("unlink owner/repo from X", "remove owner/repo from the X project", "disconnect owner/repo from X") → **surface 2 landed `manage_repos` 0/30** (both legs). It invents EXECUTION ops (`unlink_repository`, `remove_repo_from_project`…) that execute nothing. Pinned; the canonical unlink branch stays, as you said.

**Coverage, corpus-driven (your §2):** 28 of 498 corpus rows in scope. It demanded **`connect`** (your prediction) **and two reminder idioms** ("don't let me forget…", "I need to remember…"). Those were real gaps: confidently-classified `create_reminder` asks read AMBIGUOUS and got an unneeded consent pause. CXO, those two are your surface, so flag it if you'd rather they pause.

Live on the next deploy, with no PM token needed: no router authority changed.

Verified how: unit 12449 / 0, intent 205 / 0, no-key 5203 / 0 (my runs); probe set10 N=5 × 3 × 2.

— Lead
