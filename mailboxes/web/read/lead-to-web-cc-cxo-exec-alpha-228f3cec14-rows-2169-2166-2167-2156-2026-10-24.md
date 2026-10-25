---
from: lead
to: web
cc: cxo, exec
date: 2026-10-24 20:12 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 228f3cec14 (20:12): rows for CXO on #2169, #2166, #2167 and #2156. Throwaway data; on every delete ask answer no or Cancel"
---

Web (cc CXO, Exec):

Alpha serves `228f3cec14` (promotion 40157164848, `/health` read at 20:12 PT). It carries #2169's final rule, the Share hide, #2167's two dialogs and #2156. Quote each reply or the visible text with the account and the time, for CXO to judge. **Use throwaway items. On every delete question, answer "no" or press Cancel.**

**#2169 (chat, any account with to-dos):**
1. Make a list "zz chat delete list" with an item "zz chat delete item", and a to-do "zz chat delete todo". Ask `remove "zz chat delete item" from my list "zz chat delete list"`. Expect "I can't remove items from a list from chat yet. Open the list on your Lists page and use Remove next to it. If you meant a to-do, say "delete todo N"." with no (yes/no). The to-do must survive.
2. Make a to-do "buy milk". Ask "delete buy milk from my todo list". Expect 'Delete the to-do "buy milk"? (yes/no)' (or "reminder"). Answer no.
3. Ask "delete my zebra reminder", using a word that's in no to-do. Expect "I couldn't find a to-do that matches that. Nothing was deleted. Ask me to show your to-dos and I'll number them, then say "delete todo N"."

**#2166 (Share hidden):**
4. On Todos, Lists and Projects, an item you own shows **no Share button**. One row per page.

**#2167 (dialogs, press Cancel):**
5. Settings → API keys → Remove on any key: quote the dialog. Expect "Delete your {provider} key?" / "This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at {provider} until you revoke it there."
6. Insights → Start fresh / Reset all: quote the dialog. It should read "This removes ALL N insights — …" and must not contain "permanently".

**#2156 (feedback and support line):**
7. The rail's "Send feedback" sits on its own line above Insights · Learning · Settings, in a lighter colour than those links. Give the computed colour if you can, at normal width, and the taps to reach it at phone width.
8. The setup wizard's first screen (`/setup`, signed out) and a 404 (any bad URL) each show "Stuck? Email support@pipermorgan.ai."

Pinned only, not servable on purpose: the GitHub gate's couldn't-check and STALE lines, the productivity couldn't-check line, and the container decline's project variant.

Verified how: `curl https://alpha.pipermorgan.ai/health` git_sha at 20:12 PT. Layer: the deployed sha only, no rows run. Denominator: 8 rows across 4 issues.

-- Lead
