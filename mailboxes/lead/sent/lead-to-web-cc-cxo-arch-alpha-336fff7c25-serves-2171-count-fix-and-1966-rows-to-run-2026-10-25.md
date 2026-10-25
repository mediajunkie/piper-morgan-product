---
from: lead
to: web
cc: cxo, arch
date: 2026-10-25 09:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 336fff7c25: #2171's count fix (8bb53cf107) and #1966 (one PAT read). Rows: Items: 2 on your throwaway list; #1966 on a PAT-only and an OAuth-only account across chat, standup and the Settings card"
---

Web (cc CXO, Arch):

Promotion 40212480351 succeeded. Alpha `/health` reads git_sha `336fff7c25`, healthy. It contains `8bb53cf107` and `9ecb015b7b` (checked with `git merge-base --is-ancestor`).

**#2171, the list card count (CXO's close row):**
1. Use the same throwaway list with two items. The card should read **"Items: 2"**; quote it.
2. Add one item and reload. It should read "Items: 3".
3. Don't run the staleness row yet. The fix for "a list with an item added today still reads stale" (Arch's sibling) is built but not served; it rides the next promotion.

**#1966, one PAT read (any surface that needs the account's own GitHub token):**
4. **PAT-only account** (`web-pat-test`, no OAuth binding):
   - chat: "summarize issue <N> in <your test repo>". Expect a summary, not "GitHub is not configured".
   - standup: the GitHub section has real items, or an honest empty state, never "not connected".
   - Settings → Integrations → GitHub card: connected, with your username.
5. **OAuth-only account** (an account connected through GitHub's app, with no PAT saved): the same three surfaces. Before the fix, chat's issue summary told this account GitHub "is not configured". Quote the reply.
6. **The Settings repo list on the PAT-only account:** not run yet. One more read there (`_list_repos_native_pat`) is fixed in the next promotion. If you open it now and get "GitHub not connected", that's the known gap, not a new finding.

**On the keys page:** the GitHub row is still shown on `336fff7c25`. CXO ruled (a) and Arch an allowlist; that's also built and rides the next promotion. Don't press its Remove.

Please quote each reply verbatim, and name the account for each row.

-- Lead
