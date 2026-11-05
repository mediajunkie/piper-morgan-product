---
from: pa
to: cxo, exec
cc: lead, web
date: 2026-11-04 18:49 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Served on alpha 9824d7d5b2 as web-seed-1386: the not-found close keeps the ruled sentence and is stored for reload; the card reads 'Connected as dinp-machine.'; the degrade shown alone is not run. Exec: the MCP deploy did not land, still v19"
---

CXO, Exec (cc Lead, Web),

**CXO, two of your three quotes, on alpha `9824d7d5b2` at 18:48 PT, as web-seed-1386, a non-xian Piper account.**

**1. The card.** `GET /api/v1/integrations/health`, GitHub entry, quoted in full:
- status `connected`
- status_message: `Connected as dinp-machine. Not the right account? Disconnect, then connect again.`
- status_detail: `Not checked yet. Press Test.`

That is the account's own GitHub login, not mediajunkie. This is the data the card renders, read through the API. I did not see the rendered card. Web's box 5 is the browser read.

**2. A not-found write turn, then what a reload reads.** In a fresh session I sent `Close issue #9995 in dinp-machine/piper-test-activity`. #9995 does not exist. It routed to `execution/close_issue_query` and Piper answered:

> I couldn't find issue #9995 in dinp-machine/piper-test-activity, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.

Then I read `GET /api/v1/conversations/{id}/turns`, which the page reads to restore a conversation on reload. It holds turn 1 with that user message and that exact sentence as `assistant_response`. So the reply stays in the conversation after a reload, in the stored data. The turn record carries no error field. Whether the bubble looks ordinary is a render question I can't see through the API, so Web's browser is the place to judge it.

**3. A GitHub degrade shown alone: not run.** It needs an account whose grant is stale or unreadable. web-seed-1386's grant is good, and I won't break it to make one. The 1-of-8 rejected grant in xian's census is another account's, and not mine to use. Blocker: a fixture account with a revoked grant. Lead or HOST can say whether one exists.

**Exec, item 6: the MCP deploy did not land.** The MCP server still serves `53685c4601`, and `fly releases -a piper-morgan-mcp` shows v19 (11-03 21:08) as the newest. xian's run in my session after the 15:47 fire was refused before anything deployed: `deploy-mcp: REFUSED: tracked files differ from origin/main … Sync first.` My worktree was behind other seats' log pushes. I synced right after, and the dry run is clean on current main. One more `! scripts/deploy-mcp.sh` in my session will do it, ideally right after I sync, since any push in between can trip the same check. When it lands I'll check `/health` and re-read `piper://me/github/issues`.

Verified how: `dev/2026/11/04/served-2188-reload-and-card.py` and its transcript `served-2188-reload-and-card-9824d7d5b2-2026-11-04.txt` (alpha `/health` read before and after: `9824d7d5b2`); `fly releases -a piper-morgan-mcp` and mcp `/health` at 18:47. Layer: the served API (intent, the turns store, the integrations card data), not the render. Denominator: 2 of CXO's 3 asks; the degrade is not run.

-- PA
