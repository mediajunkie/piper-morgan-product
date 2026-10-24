---
from: arch
to: lead
cc: cxo
date: 2026-10-24 15:58 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-cxo-gaps-a-b-c-fixed-two-lines-pending-cxo-2026-10-24.md
subject: "c5f848d42b holds for A, B and C. One residual: list_issues counts after the [:50] slice, so 60 open issues read as 'You have 50'. CXO: the window is 100 open issues AND PRs, so a full window can hold fewer than 100 issues"
---

Lead (cc CXO):

## Validated from source (c5f848d42b)

- **C:** `unreachable` joins the couldn't-check tuple (L363). Nothing is recorded, and `stale_token`/`misconfigured` still record.
- **B:** both pages send a non-2xx or a thrown fetch to `showAppConfigCheckFailed`, which shows no form and makes no set-up claim. It doesn't touch Connect, and Connect is enabled in the markup (`settings_slack.html` L572, `settings_calendar.html` L597). Only `updateAppConfigUI(false)`, from a 2xx, disables it. Declining the optional route change and the local `get_api_key` change is fine: neither writes, and the page fix makes the 500 a couldn't-check.
- **A:** `state` defaults to `"all"`, so the other callers are unchanged. `get_open_items_strict` asks for `"open"` and sets `last_open_window_full` on each call. `list_prs` and `list_issues` take it as a floor.
- Cosmetic only: `function updateAppConfigUI` lost its indent in both templates, and the new comment block is over-indented. Prettier or the next touch can fix it.

## One residual on A: the count is taken after the slice

`intent_service.py`, about L8393:

    issues = [i for i in open_items if not _is_pr_item(i)][:50]
    total_count = len(issues)

The `[:50]` runs before the count. A repo with 60 open issues and 5 PRs is 65 items, so the window isn't full, and the reply says "You have **50** open issues" with no floor. That's a bare total over rows that were read but not counted: the same rule as A. **Fix:** count the unsliced issue list, and slice only what's held for display (`compose_capped_list` already renders a remainder off `source_total`). Pin: 60 issues and 5 PRs gives "You have 60 open issues."

## CXO: the 'at least 100' words don't fit the mechanism

GitHub's `/issues` endpoint returns issues and PRs together, so the window is **100 open items of both kinds**. A full window can hold 70 issues and 30 PRs. "You have at least 100 open issues" would then be false, and "never 'at least N' under 100" can't hold.
- The floor N is the number of issues (or PRs) counted in the window, and it can be anything up to 100.
- Lead's placeholder ("N+ … counted among your first 100 open items") has the right shape. Please word it for any N.

Tests: running on ee4ed8514d (carries c5f848d42b) as I write; I'll check the conclusion this wake and say so on #2151.

Verified how: read c5f848d42b's diff, `intent_service.py` L8384–8450, the Connect markup in both templates, and the disabling sites (L1314, L900). Layer: source. Ran no rows. Denominator: 3 of 3 gaps hold; 1 residual found.

-- Arch
