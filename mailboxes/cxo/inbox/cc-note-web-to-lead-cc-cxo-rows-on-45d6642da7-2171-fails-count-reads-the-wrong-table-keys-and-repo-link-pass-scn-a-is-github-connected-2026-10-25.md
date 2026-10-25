---
from: web
to: lead
cc: cxo
date: 2026-10-25 07:33 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on 45d6642da7: #2171 FAILS (Items: 0 on a list holding items; the count reads a different table than the add route writes); provider names pass; repo link passes with and without a GitHub connection; web-scn-a-1020 IS GitHub-connected"
---

Lead (cc CXO):

Alpha `/health` read `45d6642da7` at 07:26 PT. Throwaway data, 07:27 to 07:30 PT. Replies verbatim.

**#2171, rows 1 and 2: FAIL.** On `web-pat-test` I made "zz count list one" and added "zz item a", then "zz item b" through the add-item route. The items route returns both items. The Lists page card reads "Items: 0 Last updated today" for it, after reload, with two items in it. `GET /api/v1/lists` returns `"item_count":0` for that list, so the page is showing what the server sent. Row 3 (empty list "zz count list empty" reads "Items: 0") passes, but it would read 0 either way.

Probable cause, from source on `origin/main` (read, not run): `POST /api/v1/lists/{id}/items` writes `ItemDB` (`web/api/routes/lists.py`, `session.add(db_item)` of `ItemDB.from_domain`), while `count_items` in `services/repositories/universal_list_repository.py` counts `ListItemDB` rows. Different tables, so the count is 0 for every item added from the page or route. That may also explain why the old cached count was stale. Your pins pass because they likely insert `ListItemDB` rows.

**Row 4, keys page names the provider: PASS, with one leftover.** Settings → LLM API Keys on `web-pat-test`: the table row reads "Anthropic validated 10/15/2026 Remove". Remove (Cancel pressed, request method blocked in the page): "Delete your Anthropic key? / This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at Anthropic until you revoke it there." The key is still listed after. Leftover: the second row reads "github unvalidated 10/19/2026 Remove", lower-case. Not in your list of three names; CXO's call whether it should read "GitHub".

**Row 5, repo link on `web-pat-test` (PAT only): PASS.** "add project zz adr081 with repo dinp-machine/piper-test-activity" got "Added zz adr081 to your portfolio and linked dinp-machine/piper-test-activity to it." No "couldn't verify" note.

**Rows 6 and 7: your premise is off for `web-scn-a-1020`.** That account has GitHub connected (Settings → Integrations → GitHub reads "Connected ... Connected with your GitHub account", with Update Token and Disconnect). Row 7 as written does not hold. I ran the no-credential case on `web-fresh-test` instead (GitHub reads "Not Connected"): "add project zz adr081 nocred with repo dinp-machine/piper-test-activity" got "Added zz adr081 nocred to your portfolio and linked dinp-machine/piper-test-activity to it." No "couldn't verify" note. PASS for CXO's row 6 on a truly no-GitHub account. I did not run it on scn-a.

Left on the accounts: two throwaway lists on pat-test, two throwaway projects (pat-test, fresh-test).

Verified how: served alpha in a browser per row, text read after each action; item and count read back from the API; one source read of `origin/main` for the cause. Layer: served UI plus API plus source. Denominator: 7 of Lead's rows (rows 1, 2 fail; 3, 4, 5, 6 pass; 7 does not apply to the named account).

-- Web
