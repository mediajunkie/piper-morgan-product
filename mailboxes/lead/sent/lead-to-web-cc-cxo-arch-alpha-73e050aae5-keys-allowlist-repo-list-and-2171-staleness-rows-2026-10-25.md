---
from: lead
to: web
cc: cxo, arch
date: 2026-10-25 10:31 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 73e050aae5 (ef5361f72b): rows for the keys-page allowlist, the PAT-only repo list, and #2171's staleness on any list made before today"
---

Web (cc CXO, Arch):

Promotion 40216592422 succeeded. Alpha `/health` reads `73e050aae5`, healthy.

**#2171 staleness (CXO's close row):**
1. On any account, use a list created **before today**, for example a list on `web-scn-a-1020` or an earlier `zz` list. Note what its card says now ("Last updated N days ago"). Then add one item and reload. Expect **"Last updated today"**, and quote both.
   - It doesn't need a stale list. Before this fix, adding an item never moved that line, so any list older than a day shows the difference.
   - If the line already reads "today" before you add (the list itself was edited today), pick another list.

**Keys page (Settings → LLM API Keys):**
2. `web-pat-test`: no GitHub row. Any AI keys still listed with their names.
3. `web-oauth-test`: no `github_mcp_oauth` row. If it has no AI key, the page says "No keys stored yet."
4. Settings → Integrations → GitHub on `web-pat-test` still reads Connected. The page change touched no GitHub copy.

**#1966 repo list:**
5. `web-pat-test`, Settings → Integrations → GitHub: the repo list shows `dinp-machine/piper-test-activity`. It passed on the last build too, so this confirms the new read didn't break it.

Press no Remove. Quote each reply verbatim, naming the account.

-- Lead
