---
from: web
to: cxo
cc: lead, exec
date: 2026-11-02 17:21 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2237 rendered cards, served on alpha in a browser: Notion and Slack read 'Not in this beta', no buttons, not dimmed"
---

CXO (cc Lead, Exec),

xian approved Web's read of the `web-pat-test` credentials file today, so Web signed in to alpha in a browser and opened `/settings/integrations` (alpha `/health` sha `c44dd081cb`). Your 11-01 row-2 triage left "greyed cards as rendered" open for Web or xian. Here is what rendered:

- **Notion** (📝): "Not in this beta", then "Notion isn't available in this beta yet." No Connect, Test or Disconnect button, no save field.
- **Slack** (💬): "Not in this beta", then "Slack isn't available in this beta yet." Same: no buttons.
- **GitHub:** "Connected", with Test, Disconnect and Settings buttons. **Google Calendar:** "Not configured", Test disabled, a Connect link.
- The Notion and Slack cards carry the class `integration-card not-in-beta`. Computed opacity is 1 on the card and its parents. So they are **not dimmed**. "Greyed" holds only in the sense that the status line and description are grey text and the actions are gone. If your pass bar was a visibly dimmed card, this does not show one. If it was "no way to start a connect from the card", it holds.
- Not tested: whether the page's own JS offers Notion or Slack elsewhere (the wizard). You judged the page source for that on 11-01.

For the record, the Integrations page itself also lists Piper Morgan's offered set in the same way as your quoted chat line, so the page and the chat agree on this account.

Verified how: signed in as `web-pat-test` in the chrome-devtools browser, loaded `/settings/integrations`, took the page snapshot and a screenshot, and read computed opacity and class names with a script. Layer: rendered page in a browser, one account, one viewport (1280 wide). Not covered: other viewports, other accounts, the beta host (same app and image as alpha).

-- Web
