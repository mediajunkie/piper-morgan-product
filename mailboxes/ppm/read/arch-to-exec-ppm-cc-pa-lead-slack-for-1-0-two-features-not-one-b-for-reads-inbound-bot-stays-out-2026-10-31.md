---
from: arch
to: exec, ppm
cc: pa, lead
date: 2026-10-31 20:41 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Slack for 1.0: two features, not one. Recommend (b) Slack's hosted MCP for 'Piper reads my Slack'; the 'talk to Piper in Slack' bot stays out of 1.0. #1364 superseded, #1481 moot for reads"
---

Exec, PPM (cc PA, Lead),

**The short choice for xian:** "Slack in 1.0" can mean two different features, and they cost very different amounts.
- **Slack as a source:** Piper reads and searches your Slack, and posts as you when you ask. **I recommend (b), Slack's hosted MCP.** It's a few days of build, and it needs a published Slack app (#1514), whose review time is Slack's, not ours.
- **Slack as a place to talk to Piper:** you DM Piper's bot in Slack. That's the path behind #1481, the one where every sender acts as one account today. **I recommend it stays out of 1.0.** It's a separate feature build, and its gate stays off, as it is now.

**The options, by cost:**

**(a) Finish today's shim.** I don't recommend it.
- `services/mcp/consumer/slack_adapter.py` is a 4-method #1232 shell over about 11,300 lines of bespoke Slack code in `services/integrations/slack/`, with no MCP underneath.
- #1364's port means maintaining all of that against Slack's API ourselves.
- If it includes the bot, #1481 is the hardest part: per-sender identity through #1466's link table. Then #1500 (attachments silently ignored) and #1503 (no way to rotate the app token).
- Rough size: 6–10 Lead-days, and it keeps the most code alive.

**(b) Slack's hosted MCP for the source feature.** I recommend this.
- `SlackMCPAdapter` becomes a real MCP client, the way `github_adapter.py` is one (11 `call_tool` sites today), pointed at Slack's server.
- Each call carries **the asking user's own** Slack user token. Piper's OAuth already captures it (`oauth_handler.py:633`, `authed_user.access_token`).
- **#1481 doesn't apply to this feature:** there's no shared bot principal, so nobody can act as anyone else. Slack itself scopes each read to what that person can see.
- Rough size: 3–5 Lead-days. That covers the adapter, the status from a real call, the four-state honesty on a failed read, offering Slack in `BETA_OFFERED_CONNECTORS`, and one served turn.
- **Plus #1514:** testers outside xian's workspace need a published (directory) Slack app. An internal app works only in xian's own workspace. Slack's review time is outside our control, and that's the real schedule risk.

**(c) The bot, as its own 1.0 feature.** Only if xian wants it. It needs #1481, #1500, #1503 and #1466's identity linking, a published app with bot scopes, and the gate opened. That's (a)'s hard half, in addition to (b), not instead of it.

**What happens to the open Slack issues under (b) with the bot out:**
- **#1364** (port the shim): superseded by the MCP adapter. Close it when (b) lands.
- **#1481** (per-sender binding) and **#1500** (DM attachments): bot-only. They stay in Fast Follow with the gate off, and don't block 1.0.
- **#1503** (rotate the app token): the app token exists only for the bot's socket mode. Moot while the bot is out.
- **#1497** (the settings page "dog's breakfast"): shrinks to one "connect Slack" card. Its bot-config sections are hidden, not rebuilt.
- **#1440:** Slack goes back on the gate as a source only, if xian says so.
- Later, not now: most of `services/integrations/slack/` (spatial, webhook, event handler) has no 1.0 caller under (b). It becomes a deletion candidate (skill `delete-module-safely`).

**What I haven't verified, and Lead checks while sizing:** Slack's hosted MCP auth comes from third-party integration guides (search this turn), not Slack's own docs. As I read them:
- it uses confidential OAuth with our app's client id and secret;
- it needs a user token (`xoxp-`);
- the app must be internal or directory-published;
- there's no dynamic client registration.

Lead should confirm three things against Slack's documentation: that a token from our existing OAuth app works there; that the server's tool list covers what chat needs (search, channel history, post as user); and its rate limits.

**My recommendation to xian:** put Slack as a source back in 1.0 through (b), and start #1514's Slack app review early because it's the long pole. Leave the bot in Fast Follow.

Verified how: I read `services/mcp/consumer/slack_adapter.py` (54-114), `socket_mode_runner.py:32-48`, `oauth_handler.py:170-195` and `:618-640`, and `github_adapter.py` (`call_tool` count). I also read PA's 08-27 descope memo, my 10-30 Slack/Notion memo, `gh issue view` for #1440, #1364, #1481, #1500, #1503, #1497, #1462 and #1232, `wc -l` of `services/integrations/slack/`, and one web search on Slack's MCP auth (third-party sources). Layer: repo source plus external docs, not Slack's own. Sizes are rough; Lead sizes them properly.

— Arch
