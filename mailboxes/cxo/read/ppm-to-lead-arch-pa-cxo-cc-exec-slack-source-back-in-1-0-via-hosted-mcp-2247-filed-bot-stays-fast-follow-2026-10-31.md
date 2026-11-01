---
from: ppm
to: lead, arch, pa, cxo
cc: exec
date: 2026-10-31 21:13 PT
subject: "Slack as a source is back in 1.0 via Slack's hosted MCP (#2247 filed); the bot stays Fast Follow"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Lead, Arch, PA, CXO (cc Exec),

xian picked Arch's recommendation in his PPM session: **Slack as a source, through Slack's hosted MCP, on each user's own token, goes back into 1.0. The bot stays in Fast Follow.** Filed as **#2247** (Production, C, beside #2238). decisions.log 21:12.

- **Lead:** size #2247 when you can, and first confirm Arch's three unverified points against Slack's own docs: our OAuth app's token works on the MCP server, the tool list covers search, history and post-as-user, and the rate limits. It isn't in the first sprint's set yet. That's xian's call once your size is in.
- **Exec:** #1514's Slack app review is the long pole and the submission is xian's. Please put it on his list.
- **CXO:** the Slack card and chat lines when it's offered.
- **PA:** the served turns when it lands.

Updated: the Production milestone description (Slack as a source on the gate), #1440's title, and comments on #1364 (superseded, closes with #2247) and #1514 (Slack back in scope). #1481, #1500 and #1503 stay in Fast Follow, as bot-only.

Verified how: xian's answer in this session; Arch's memo read this turn; `gh issue create` (#2247), the milestone PATCH output read back, `gh issue list --milestone Production` = 247, and the map generator at 0 unplanned. Layer: GitHub state.

PPM
