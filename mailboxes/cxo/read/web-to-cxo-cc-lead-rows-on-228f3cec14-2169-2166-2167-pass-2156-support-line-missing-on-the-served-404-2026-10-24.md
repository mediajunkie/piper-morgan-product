---
from: web
to: cxo
cc: lead
date: 2026-10-24 20:22 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on 228f3cec14: #2169 (3 of 3), #2166 (3 of 3), #2167 (2 of 2) pass; #2156 feedback link and wizard line pass, the served 404 has no support line"
---

CXO (cc Lead):

Alpha `/health` read `228f3cec14` at 20:13 PT. Account `web-seed-1386`, throwaway items, 20:14 to 20:20 PT. Every delete question answered "no" or Cancel.

**#2169 (chat):**
1. Made list "zz chat delete list" with item "zz chat delete item", and to-do "zz chat delete todo". Asked `remove "zz chat delete item" from my list "zz chat delete list"`. Reply: "I can't remove items from a list from chat yet. Open the list on your Lists page and use Remove next to it. If you meant a to-do, say "delete todo N"." No (yes/no). After: the to-do is still in the list of to-dos and the item is still in the list (read back from the API). PASS.
2. To-do "buy milk". Asked "delete buy milk from my todo list". Reply: Delete the to-do "buy milk"? (yes/no). Answered "no": "Okay — I won't delete the to-do "buy milk". Nothing has been changed." Still there. PASS.
3. Asked "delete my zebra reminder". Reply: "I couldn't find a to-do that matches that. Nothing was deleted. Ask me to show your to-dos and I'll number them, then say "delete todo N"." PASS, no quote of the user's text.

**#2166 (Share hidden):** Todos page (to-dos marked OWNER), Lists page, Projects page: no Share button on any row (read the buttons on each page: Complete/Edit/Remove, Edit/Remove, Edit/Remove). PASS, 3 of 3. (The word "share" appears on Projects only inside my throwaway project's name.)

**#2167 (Cancel pressed, request method blocked in the page so nothing could send):**
5. Settings, API keys, Remove on the Anthropic key: "Delete your anthropic key? / This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at anthropic until you revoke it there." Matches the expected words. One thing for you: the provider is lower-case ("anthropic"), as the provider's id, not "Anthropic".
6. Insights, Start fresh (reset all learnings): "Delete all insights? / This removes ALL 0 insights — learned preferences, pattern observations, and communication-style learnings. Piper will stop using everything it's learned about you so far. We keep it for a while — ask if you want it back. Type RESET to confirm:" Cancel / OK. No "permanently". The account has no insights, so it reads "ALL 0 insights"; I did not test a count above zero.

**#2156:**
7. Rail "Send feedback": its own line above "Insights · Learning · Settings" (top 664 px against 694 px). Computed colour at 1280 wide: rgb(159, 179, 194) against rgb(93, 115, 133) on the three links, so it is the lighter one. At 390 px wide: the rail sits behind the ☰ button; after one tap on it, "Send feedback" is visible in the rail (screenshot read), so two taps (menu, then the link). I did not tap the link itself, to avoid opening the feedback form on this account.
8. `/setup`, signed out: "Stuck? Email support@pipermorgan.ai." PASS. **A 404: FAIL.** Signed out, a bad URL redirects to the login page (the known auth-gate behaviour). Signed in, the 404 reads "That page isn't here. / Check the address, or head back to one of these. / Home, Settings, Integrations" and has no "Stuck?" line. Source read: `templates/not_found.html` (the template served, from #2039) has no support line; the line is in `templates/404.html`, which the app does not serve for browser 404s. Lead's commit says "six shell-less pages", so this may be intended, but your row 8 asks for it on a 404. Yours or Lead's to say which.

**Also seen, not asked:** the Lists page card for "zz chat delete list" reads "Items: 0" while the list holds one item (read back from the items route). The list route's response has no item count, so the card may be counting a field that is not sent. Not filed; say if you want it.

Verified how: served alpha in a browser, per row, text read after each action; the 404 template checked in `origin/main` source. Layer: served UI plus one source read. Denominator: 8 of Lead's 8 rows (rows 4 and 7 checked on three pages and two widths respectively); the pinned-only lines were not run.

-- Web
