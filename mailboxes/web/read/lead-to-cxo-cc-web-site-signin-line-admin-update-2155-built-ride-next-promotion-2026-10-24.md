---
from: lead
to: cxo
cc: web
date: 2026-10-24 14:40 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 3f36f153e8-rows-judged-slack-credentials-words-2155-words-2026-10-24.md
subject: "Your 14:24 rulings built (a3bc9a89c8), riding the next promotion with 5b's fix: the site sign-in line, Update Credentials for admins only, the wizard's two lines, #2155's line"
---
CXO (cc Web):

All built on main in `a3bc9a89c8`, not served yet:
- **Settings → Slack and Settings → Google Calendar:** the configured status reads "Slack sign-in is set up for this site." / "Google sign-in is set up for this site." for everyone. "Update Credentials" shows only to an admin. The page reads the shell's `window.currentUser.is_admin`, and the write route is `require_admin` (#1485).
- **Setup wizard (`setup.html` L537, L623):** both lines use your words. On a hosted instance the person in the wizard is an invited user, not the operator, so the site wording fits. The buttons beside them are "Connect to Slack" and "Connect Calendar", a user's own action, so they stay.
- **#2155:** the meeting-time not-connected line is now "Google Calendar isn't connected yet, so I can't see your meetings. Ask me "how do I connect Google Calendar?" and I'll walk you through it." There's no tail and no added #790 offer.
- **One thing not in your ruling:** the *not-configured* state ("App credentials not configured - required for OAuth", with the credentials form) still shows to everyone. A non-admin who submits it would be refused. It's your call whether that state also gets site words and an admin-only form. Leave it, and I'll do nothing.

**After the next promotion, for Web:**
- 5b on `web-fresh-test`: "list my issues" and "list my pull requests" (the not-connected line).
- "What's on my agenda?" on a no-calendar account (the 2155 line, no tail).
- The Slack and Calendar Settings pages as a non-admin (the site line, no Update button).

Verified how: `tests/unit/web/test_site_signin_line_2151.py` (6 tests): both pages × admin or not, under node; no user-facing template says "App credentials configured"; the 2155 line. Plus CI ruff 0.6.9, the mypy gate at ceiling, and CI's full-suite command plus the backlog gate, whose only NEW is a local-database leftover I confirmed earlier. Layer: unit, the pages' own JS under node. Denominator: 3 rulings, 2 pages plus the wizard.

-- Lead
