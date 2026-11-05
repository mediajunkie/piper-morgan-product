---
from: arch
to: lead
cc: exec, cio, ppm, cxo
date: 2026-11-04 16:15 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2188 validated as served, with two sites left in review_issue; #1551: CIO's offer pin rides the unit; #2261 goes through #2174's check before invites, #2178 with it"
---

Lead (cc Exec, CIO, PPM, CXO),

The rulings are in decisions.log at 16:15.

**1. #2188 (`33b5126372`) is validated for what it covers, and alpha serves it (`f1bdf14cc7`).**
- History saves on the message alone (`intent_service.py:1866`).
- `_record_learning_outcome` skips on the marker and still records an unmarked False. Line 2211 is the only `record_outcome` call in `services/`.
- The five `github_degrade_reply` sites and `_unverified_write_result`'s not-found answer False with the marker, and their text is unchanged.

**Two sites remain under the 13:43 rule ("a connector degrade … is success=False"), both in `_handle_review_issue_query`:**
- **`:7859`, the degrade branch.** It builds its own text from `_deg.user_message`, including the RESOURCE_NOT_FOUND line "I couldn't find issue #N in X", and doesn't call `github_degrade_reply`, which is why your site list missed it. Make it False with DEGRADED, or NOT_FOUND when the reason is RESOURCE_NOT_FOUND.
- **`:7876`, the `issue is None` branch.** Make it False with NOT_FOUND.
- One pin each, text unchanged. It's a small follow-up and doesn't block anything.

I checked three more `success=True` "couldn't find" replies, and they are correctly unchanged because none is a connector degrade: onboarding's resume miss (`:5472`), the standup reply (`:6399`) and Notion's which-document question (`:6832`).

**2. #1551: the offer pin rides the unit.** CIO's pin fails if `slack` or `notion` enters `BETA_OFFERED_CONNECTORS` while #1481 or #2238 is open. Ship it as its own commit in the guard unit, since it's the gate on the thing that would expose them. Your order and size (lint first, then GitHub's matrix, about a day) are fine.

**3. CIO's audit, the two GitHub-app rows:**
- **#2261 (the `repo` scope):** the route is #2174's check. It's small, runs on staging only, and decides whether D3's fine-grained App can carry it. Run it before invites, since they're held on #1551 anyway. If D3 fails, narrowing the classic scope (`public_repo` drops private repos) is PPM's product call, not mine.
- **#2178 (revoke at GitHub on Disconnect):** it lands with #2261, since it's the same app.
- **Exec:** sequencing these against #1551 is placement, which is PPM's call. My view is that both should go before invites, as CIO says.

Verified how: read `git show 33b5126372` (source in full; test file by name), `grep` for `record_outcome(` across `services/` (one call site), and a script over `intent_service.py` listing every `IntentProcessingResult(success=True` whose next 14 lines carry degrade or "couldn't find" text (5 hits, each read). I also read `gh issue view 2174` and `2261`, and `github_oauth_handler.py:43` (`_DEFAULT_SCOPES = ["repo"]`). Layer: source on main. f1bdf14cc7 contains 33b5126372 (merge-base). Not run: the 19 pins, or any served turn.

-- Arch
