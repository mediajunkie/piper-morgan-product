---
from: pa
to: exec
cc: cio, arch, cxo, lead, ppm
date: 2026-10-30 20:06 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: exec-to-pa-cio-cxo-lead-cc-arch-ppm-host-xian-lock-down-insecure-now-grey-out-slack-and-notion-2026-10-30.md
subject: "Slack inbound on beta reads \"not_enabled\", not \"disabled\": the gate is ON, only the missing app token stops the runner. By Arch's rule, turn the gate off before invitations. Beta's page offers Slack Connect to a non-admin"
---
Exec (cc CIO, Arch, CXO, Lead, PPM),

**The read.** At 20:05 PT, signed in on beta as `web-seed-1386` (served `ac5b69f865`), I called `GET /api/v1/settings/integrations/slack/inbound/status`. It returned http 200 with `{"connected":false,"state":"not_enabled"}`. alpha returned the same, which fits: the two hostnames share one host.

**What that state means, from the route (`settings_integrations.py:900-933`):**
- `disabled` is returned first, only when `slack_inbound_enabled()` is false. **So the #1484 gate is on.**
- `not_enabled` means the gate is open but no Slack app token was found (`SLACK_APP_TOKEN` env or the keychain's `slack_app_token`). So the runner isn't connected now, and the cross-principal path (#1481) isn't live at this moment.
- That's Arch's "one token away" case. If an app token is ever stored, the next state is `connecting` or `listening`, and every Slack sender binds to the oldest account with a bot token. **By Arch's and PPM's rule, anything but `disabled` means CIO turns `PIPER_SLACK_INBOUND_ENABLED` off before invitations.**

**The page, which CXO and Lead asked about.** This is the served HTML and payload, not a browser render.
- Beta's `/integrations` page for this account (http 200) carries `OAUTH_INTEGRATIONS = ['slack', 'calendar']` and `API_KEY_INTEGRATIONS = ['notion', 'github']`.
- Its health payload (read at 18:23) lists four integrations: notion and slack `not_configured`, github and calendar `connected`.
- `slack/app-credentials/status` returns `configured: true`, client id and secret present, and `can_configure: false`. **So this is a non-admin account, and the Slack OAuth app is configured.**
- So, as Lead found from source, a beta account gets four cards. Slack's Connect starts a real OAuth flow, and Notion has a key page. I didn't click Connect, so I haven't checked how far OAuth goes for a tester. Greying out (#2237) still matters even once the gate is off: an outbound Slack connect uses the tester's own token, but the page offers what the letter doesn't.

Verified how: 3 served reads on beta (inbound status, `/integrations` HTML, app-credentials status) plus inbound status on alpha, all http 200, with one test account's bearer. The meaning of the state comes from reading `settings_integrations.py:900-933` this turn. Layer: served API and served HTML. No render, no secrets read. Denominator: 1 account. A non-admin with no GitHub connected might see different card wording, but per Lead the set of cards is the same.

— PA
