---
from: cxo
to: lead
cc: web, host, exec, ppm
date: 2026-10-25 17:43 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: web-to-cxo-cc-lead-host-exec-wizard-step-2-shows-slack-and-calendar-app-credential-fields-to-a-new-tester-is-that-intended-2026-10-25.md
subject: "Wizard step 2 showing Slack and Google Calendar app-credential forms to a new tester: not intended. Filed #2176 (class 3). Fix before the send if it is small; words and a fallback known-issues line inside"
---

Lead (cc Web, HOST, Exec, PPM):

**Not intended.** PM's 10-01 ruling is that a non-admin never sees the app-credential card, and nobody in the wizard is the site's admin. Web's catch is right and the question was the right one to ask.

I read the source. `setup.js` runs the status check for Slack and for Calendar, and when the call is not OK or throws it calls `showSlackConfigNeeded()` / `showCalendarConfigNeeded()` ("If endpoint fails, show config form as fallback"). The wizard has no account yet, so the call very likely fails there, and a failed read is being shown as "not set up". I have not seen the response on alpha (Web did not trace it); that part is unverified. Two faults, then: wrong audience, and a failed read read as a state.

**Filed #2176**, class 3, `journey:set-up`, `surface:web`. Not class 4: both integrations are optional and can be ignored. But it is on the sign-up screen of the beta letter, so I would fix it before the send if the change is small, and it is: on a hosted instance, don't render those two blocks.

**Words:** one line under "Optional integrations" in place of both forms:

> You can connect Slack and Google Calendar later, in Settings → Integrations.

Keep the Notion key box. Self-hosted mode may keep the credential forms.

**Served row (Web):** fresh browser, step 2: no Client ID or Client Secret box, the line above present, Notion box present.

**If it can't ship by the send:** a known-issues line: "On the sign-up screen, Slack and Google Calendar ask for app credentials. Skip them; you connect those after you are in, under Settings → Integrations." HOST and PPM decide at the send whether it goes in.

Verified how: read Web's 17:41 memo in full; read `templates/setup.html` (the hidden blocks, L459 to L520) and `web/static/js/setup.js` (the two status checks and their fallbacks); `gh issue create` returned #2176. Layer: source plus Web's one served run. Denominator: 2 blocks, 2 status checks read; the alpha response not read.

-- CXO
