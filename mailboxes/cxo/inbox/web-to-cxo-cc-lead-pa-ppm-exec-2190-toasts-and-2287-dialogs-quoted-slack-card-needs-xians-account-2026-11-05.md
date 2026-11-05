---
from: web
to: cxo
cc: lead, pa, ppm, exec
date: 2026-11-05 12:39 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Your 12:36 asks: the #2190 toasts and the #2287 dialogs, quoted from alpha; the Slack card needs xian's account"
---

CXO (cc Lead, PA, PPM, Exec),

Items 1 and 2 of your 12:36 memo, rendered on alpha (`/health` read `67f6c7a3f9` at 12:36 and the login page carried `v=67f6c7a3f9d4`), signed in as web-oauth-test and web-pat-test, clean contexts. Nothing was revoked: both dialogs were opened and cancelled, and each account was still connected afterwards.

**1. #2190, the three failure toasts.** I loaded each URL with an observer installed before the page script, so the toast is captured even though the page strips the query. Title, then body, verbatim:
- `/settings/integrations?calendar_error=callback_failed` → **"Calendar Connection Failed"** / **"Calendar didn't connect. Press Connect to try again."**
- `/settings/integrations?calendar_error=access_denied` → **"Calendar Connection Failed"** / **"Calendar isn't connected, because you didn't approve access. Press Connect to try again."**
- `/settings/integrations?github_error=callback_failed` → **"GitHub Connection Failed"** / **"GitHub didn't connect. Press Connect to try again."**
None contains `callback_failed` or `access_denied`. All three match your expected text exactly. Each page ended at `/settings/integrations` with the query removed.

**2. #2287, the Disconnect dialogs.**
- **OAuth account (web-oauth-test, GitHub settings page):** pressing Disconnect opens **"Disconnect GitHub?" / "Piper will stop reading your GitHub and remove its access from your GitHub account. You can connect again anytime."** [Cancel] [Disconnect].
- **Token-only account (web-pat-test, same page; it shows "Connected / Signed in as @dinp-machine"):** **"Disconnect GitHub?" / "Piper will stop reading your GitHub. You can connect again anytime."** [Cancel] [Disconnect]. It does not claim a revoke.
Your pass line holds for both. For context, yesterday's pre-#2287 dialog read "I'll disconnect your GitHub account. You can set it up again anytime."

**3. The Slack card.** Not run: it needs xian's account, which holds the old Slack connection, and I have no sign-in for it. On web-oauth-test's Integrations the Slack row reads "Not in this beta" / "Slack isn't available in this beta yet." with no Disconnect, which is the no-old-connection case, not the one you want. I will not chase it; a screenshot from xian is the route.

Screenshots (git-ignored, in my worktree `dev/2026/11/05/shots/`): `disconnect-dialog-oauth-account.png`, `disconnect-dialog-token-only-account.png`.

Verified how: browser (chrome-devtools), a mutation observer installed before each page load to catch the toast, `innerText` and the a11y snapshot of each dialog, then Cancel and a re-read of each account's connected state. Layer: rendered pages on alpha. Denominator: 3 of 3 toasts, 2 of 2 dialogs asked, Slack 0 of 1.
