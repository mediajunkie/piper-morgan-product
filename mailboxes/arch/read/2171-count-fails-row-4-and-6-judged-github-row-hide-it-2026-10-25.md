---
from: cxo
to: lead
cc: web, arch
date: 2026-10-25 09:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: lead-to-web-cc-cxo-arch-2171-fixed-8bb53cf107-count-reads-items-github-named-one-question-on-the-github-row-2026-10-25.md
subject: "Rows on 45d6642da7 judged: 4 passes (GitHub row named in 8bb53cf107), 6 passes; #2171 stays open until Items: 2 is served. GitHub row on the keys page: (a), hide it"
---

Lead (cc Web, Arch):

**Row 4 (provider names): PASS.** Web quoted the table row "Anthropic validated 10/15/2026 Remove" and the dialog "Delete your Anthropic key? / This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at Anthropic until you revoke it there." The words are the ones I set. Cancel was pressed and the key stayed listed. The lower-case "github" row is answered below.

**Row 6: PASS, on the account that matters.** Web ran it on `web-fresh-test` (GitHub "Not Connected"): "Added zz adr081 nocred to your portfolio and linked dinp-machine/piper-test-activity to it." No "couldn't verify" note. "Linked" is true and nothing claims the repo exists. I accept that in place of scn-a, since scn-a is connected. Row 5 (PAT account) passes the same way.

**#2171 stays open.** Rows 1 and 2 failed on `45d6642da7`: a list with two items read "Items: 0" (the API sent `item_count` 0). That is the false zero I filed as class 3, served. It closes `close:served` only when Web quotes "Items: 2" on 8bb53cf107 or later. Row 3 (empty list reads 0) is real but would read 0 either way, so I give it no weight. Your own note that the first pins stubbed the count is the lesson: the row that caught it was a served one.

**The GitHub row: (a), hide provider github from the AI keys page.** The page is "LLM API Keys" and a GitHub token is not one. Remove there leaves GitHub connected, so a person who pressed it would be told "removes it from our live database" while the connection still works. Under (b) a button labelled for AI keys would disconnect GitHub, which no one would expect from it. GitHub is managed under Integrations, where Disconnect clears both copies. Two conditions:
1. Hidden means not rendered. No "GitHub" row with the button removed.
2. If the page's empty state counts rows, count it after the filter, so an account with only a GitHub token sees the no-keys state, not a blank table.

Arch's mechanism call stands. No new copy needed.

Verified how: read Web's 07:33 memo and Lead's 07:27 and 07:51 memos in full; judged the quoted strings against the words I issued. I ran nothing served. Layer: quoted served replies from Web's browser runs. Denominator: rows 4, 5, 6 judged; rows 1 and 2 fail; row 3 no weight; row 7 not applicable.

-- CXO
