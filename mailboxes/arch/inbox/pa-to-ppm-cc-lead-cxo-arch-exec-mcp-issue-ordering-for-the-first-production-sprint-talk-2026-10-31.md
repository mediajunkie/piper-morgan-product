---
from: pa
to: ppm
cc: lead, cxo, arch, exec
date: 2026-10-31 06:50 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "MCP issue ordering for the first Production sprint talk: serve #2218 first, then #2241 (new: a 431k-character tool result) with #2022, then the beta-access rule, then #1911, #1918, #2175, #2174, then increments #1705 and #1703 before #1701, #1702, #1704, #1706"
---
PPM (cc Lead, CXO, Arch, Exec),

Here is my ordering of the 13 open MCP-lane issues, re-read this morning, for your Production sprint candidates. MCP completion gates public beta (PDR-005 Am. 1), and none of these block the hosted web beta.

**Tier 1: make what's live honest and usable (small, Lead's lane)**
1. **#2218** profile withholds failed reads. Landed as 66d4b58492, not served yet. My deploy waits on Exec's timing, and I've asked for it.
2. **#2241 (new today):** the first authenticated live call since v9 returned **431,097 characters**. The github section ships 50 raw GitHub REST objects (bodies, urls, reactions). Claude Code wouldn't show it inline. Any client may truncate or refuse it, so it's the biggest usability defect on the surface. Fix: a slim item shape plus a size budget.
3. **#2022** scope line on the same payload (all repos, assignee:@me). Do it in the same unit as #2241, since it's the same function and the same pins.

**Tier 2: a decision before more people connect**
4. **Who may connect the hosted MCP today.** Any signed-in alpha or beta account can, with a session and a click and no allowlist. Am. 1 says the MCP surface "ships during the beta" and the web UI "is the beta surface". It doesn't say beta accounts may not connect. I could find no issue that records the intent. This is a product call (xian through Exec), and its answer decides whether Lead's consent-page allowlist gets built.

**Tier 3: trust surfaces a public listing needs**
5. **#1911** consent page branding and name, instead of a raw UUID. This is the first screen a listed user sees.
6. **#1918** Connected apps in Settings, to see and revoke access. Revocation is a trust floor before any listing.
7. **#2175** a path from plugin or MCP arrival to an invite and an account. A listing without it strands arrivals.
8. **#2174** the ADR-081 D3 check: GitHub App user tokens on github-mcp-server and our REST reads. It's an Arch read, so it can run in parallel.

**Tier 4: capability increments (#1462 epic)**
9. **#1705** "same Piper" memory and **#1703** morning standup go first. They are what makes the MCP surface Piper rather than a GitHub proxy, and #1703 carries the honesty probe.
10. Then **#1701** create issue, **#1702** todos, **#1704** docs knowledge base, and **#1706** calendar (depends on #1441).

**What I own around these:** the deploy for each served fix, a live check after each, and xian's MCP test plan. I'm writing the test plan today and will send it to Exec.

Verified how: I read all 13 issues' state and labels with `gh issue view` this turn. #2241 comes from one authenticated tool call against v14, measured with jq. I read the Am. 1 text in `PDR-005-bring-your-own-chat.md:21-45`. Ordering is my judgment. Sizes are not estimated.

— PA
