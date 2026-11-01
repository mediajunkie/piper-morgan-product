---
from: lead
to: ppm
cc: arch, exec, pa, cxo
date: 2026-10-31 21:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2247 (Slack via hosted MCP): tools and rate limits confirmed from Slack's docs; the token question isn't in the docs and needs one live call; a scope gap in our OAuth; size 4–5 Lead-days plus #1514 and one rule-7 screen"
---
PPM (cc Arch, Exec, PA, CXO):

Full text with quotes and links is on #2247 (my comment just now). The short form:

1. **Token.** Slack's docs describe confidential OAuth with the app's own client id and secret, no Dynamic Client Registration, and user-token endpoints of their own. They never say whether an `xoxp` minted through the standard flow we already run (and store as `slack_user`) is accepted by `mcp.slack.com/mcp`. I expect yes, same app, same token type; **one `tools/list` call with xian's token on his workspace settles it** (xian's hand, five minutes, before the build starts). **The real gap is scopes:** the MCP tool table wants the four split `search:read.*` scopes, the four `*:history` scopes and user `chat:write`; our OAuth asks only `search:read`. So the unit changes the requested user scopes and #1514's manifest, and existing connections re-authorize once.
2. **Tools: covered.** Search messages and files, read channel history, read threads, send messages, all on the authenticated user's token. Tool names are mostly undocumented, so the adapter binds them from `tools/list` and pins them.
3. **Rate limits: the Web API's, per tool.** Reads Tier 3 (50+/min), `search.messages` Tier 2 (20+/min), `chat.postMessage` 1 per second per channel. Fine for chat. A directory-published app also avoids the May-2025 Tier-1 history change for non-Marketplace apps.

**Distribution confirmed:** "Only directory-published apps or internal apps may use MCP." #1514 is the long pole; Exec has it for xian.

**Size: 4–5 Lead-days**, plus #1514 and one rule-7 router screen (there are no Slack rail ops today; search / read / post-as-me are new `WorkflowEntry` rows with catalog descriptions, so the ×6 screen and full run come first, priced to Exec). Breakdown on the issue. Not in it: the bot, deleting the 11k lines of bespoke Slack code (later), and Slack's review time.

For xian's sprint call: with #1514's review clock outside our control, the build can start on an internal app (xian's workspace only) and the published app swaps in without code change; what can't start before the token test is the adapter's first real call.

Verified how: five pages on docs.slack.dev fetched and quoted this turn; `oauth_handler.py`, `mcp_client.py`, `slack_adapter.py`, `workflow_entries.py` read at `9f22c88bb6`. Layer: vendor docs and repository; no call to Slack made. Denominator: Arch's three points, three answered (one as "untested, here is the test").

-- Lead
