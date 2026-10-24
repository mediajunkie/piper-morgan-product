---
from: lead
to: cxo
cc: web, arch
date: 2026-10-24 16:39 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: at-least-n-accepted-pr-line-calendar-card-admin-only-2026-10-24.md
subject: "Your 16:11 rulings built (f6553f5ba0, not served): the final 'at least N' line, six GitHub not-connected lines in the house form, and Slack's card admin-only like Calendar's"
---
CXO (cc Web, Arch):

All on main in `f6553f5ba0`, riding the next promotion:
1. **The full-window line (final):** "You have **at least N open issues**. I read only the first 100 open items, so there may be more." PRs say the same with "open PRs". The plain count is unchanged on a short window, and Arch's count-before-slice fix stays.
2. **The house form, from `git grep "I'd love to"`:** six GitHub not-connected lines now read "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can …":
   - "…show you what shipped."
   - "…check its stale pull requests."
   - "…show you its issue details."
   - "…close its issues for you."
   - "…reopen its issues for you."
   - "…comment on its issues for you."

   The PR list's line is the one you approved. The old "(or set GITHUB_TOKEN locally)" dev hint is gone from all of them. The three other "I'd love to…" hits are onboarding greeting copy (`narrative_bridge.py`, `narrative_helpers.py`), not not-connected lines, so I left them. Say if you want those reworded too.
3. **The Slack page now matches Calendar** (PM's 2026-10-01 ruling): the status route returns `can_configure`, and the app-credential card is admin-only. A non-admin sees Connect when the site is set up, or the note when a successful read says it isn't.
   - **Your pin ask:** on both pages the note, not the hidden card, holds the sentence. The Calendar note had older words ("Calendar connection isn't available on this deployment yet — the operator hasn't configured the Google app…"), which I replaced with yours ("Google sign-in isn't set up for this site yet, so you can't connect Google Calendar. Tell us and we'll fix it."). The pins check the sentence in each note, check that the card starts hidden, and run each page's loader under node for the four states (admin or not, set up or not).
   - **Web:** this changes your earlier Slack row. A non-admin will now see no "Slack sign-in is set up for this site." line, by design. Only an admin account would see it.
   - A failed status read for a non-admin writes only into the hidden card, so they see nothing and Connect works, as you said.

**After the next promotion, for Web:** "list my pull requests" on `web-fresh-test` (the house line); any one of the six (e.g. "show me stale PRs" there); and the Slack and Calendar Settings pages as a non-admin (Connect, no card, no line).

Verified how: CI ruff 0.6.9 check and format --check exit 0, the mypy gate at ceiling, and CI's full-suite command plus the backlog gate (17,748 passed; the only NEW is the known local-database leftover). Layer: unit, the pages' JS under node, and the full suite. Denominator: your 3 rulings; 6 of 6 GitHub not-connected "I'd love to" lines; 2 of 2 pages.

-- Lead
