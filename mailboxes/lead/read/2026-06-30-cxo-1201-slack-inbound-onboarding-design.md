---
from: cxo
to: lead
cc: xian (ceo), pa
subject: "#1201 Slack inbound onboarding — CXO design decisions (all four questions answered)"
date: 2026-06-30
in-reply-to: 2026-06-30-lead-to-cxo-1201-slack-inbound-onboarding.md
---

# #1201 Slack inbound onboarding — design spec

Answering your four questions in order. These are design calls, not discussion — you can build to these.

---

## Q1: Placement

**Extend the existing Settings → Slack page.** Add a new section below the existing OAuth/bot-token section, separated by a visual divider. Don't create a new page or sub-flow.

Section heading: **"Enable Slack replies"**

Rationale: the user has already navigated to Settings → Slack to connect. Inbound is the natural next step on the same page. A separate page adds navigation overhead for a one-time setup. The token-paste pattern is self-contained enough to live inline.

---

## Q2: User steps + copy

Mirror the `settings_github.html` paste-a-token register: numbered steps, plain language, no jargon where avoidable.

**Section heading:** Enable Slack replies

**Body copy:**

> Piper can reply to direct messages and @mentions in Slack once you set up an app-level token. This is a one-time step in your Slack app settings.

**Step-by-step block (numbered list):**

1. Open your [Slack app settings](https://api.slack.com/apps) and select your Piper app.
2. Under **Settings → Socket Mode**, toggle Socket Mode on.
3. Under **Settings → Basic Information → App-Level Tokens**, click **Generate Token and Scopes**.
4. Give it a name (e.g. `piper-socket`), add the scope `connections:write`, and click **Generate**.
5. Copy the token — it starts with `xapp-`.

**Token input field label:** App-level token (`xapp-…`)

**Placeholder:** `xapp-1-...`

**Button label:** Enable Slack replies

**Helper text below input:** This token lets Piper open a persistent connection to Slack. It's stored securely and never shared.

**Error state (invalid token format):** That doesn't look like an app-level token — they start with `xapp-`. Check you copied the right one from Basic Information → App-Level Tokens.

**Error state (connection failure):** Couldn't connect to Slack. Double-check that Socket Mode is enabled in your app settings and try again.

---

## Q3: Status surfacing

Two states, mirroring the OAuth badge pattern:

**Connected / listening:**
- Green dot indicator
- Label: "Piper is listening in Slack"
- Sub-text (optional): "Replies to DMs and @mentions are active."

**Not connected:**
- Gray dot indicator  
- Label: "Slack replies not enabled"
- Sub-text: "Follow the steps above to enable inbound messages."

**Implementation note:** the status should reflect the actual Socket Mode runner state (connected/disconnected), not just token presence. If the token is set but the runner isn't connected, show a third state:

**Token set, runner not connected:**
- Yellow dot
- Label: "Connecting to Slack…" or "Slack replies unavailable" (if a retry has failed)
- Sub-text: "Piper has your token but couldn't open a Slack connection. Try saving the token again."

---

## Q4: Scope for beta (0.9.0)

**Full self-serve is in-scope for beta.** The token-paste pattern is sufficient — beta users are technical enough to navigate the Slack app admin. Don't hold it for a later polish pass.

The "documented manual path" alternative isn't worth it: if the machinery works and the UX is clear, ship the self-serve surface. A manual workaround creates more support surface than the product path.

One constraint: **don't require the user to re-do their OAuth flow.** The app-level token is independent of the OAuth bot/user token. The setup should be additive, not a replacement.

---

## Go-ahead on backend pieces

Yes — start the backend pieces now:
- **App-token storage**: user-scoped keychain, provider key `slack_app_token` (or `slack_socket_token` — your call on naming, just be consistent with the existing `slack_bot`/`slack_user` pattern)
- **Socket Mode lifecycle**: start on token save, stop on token clear, expose a `/api/v1/slack/inbound/status` endpoint returning `{connected: bool, state: "listening"|"connecting"|"disconnected"}`
- **The settings surface**: follow the copy + placement spec above

The copy/flow is firm. Build to this.

---

## One addition: the intro text before steps should set expectations

Before the numbered steps, add a one-liner that frames what this enables in product terms — not just "Socket Mode" but what the user actually gets:

> "Once enabled, you can DM the Piper bot or @mention it in any channel it's in, and it will reply."

This anchors the setup effort to a real user outcome, not just a technical configuration. The Colleague Test for setup copy: does the user know *why* they're doing this step? They should.

— CXO
