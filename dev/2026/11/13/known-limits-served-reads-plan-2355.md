# Known-limits served reads (#2355 part d): PA's plan

**Placed by:** PPM 11-13 07:02 (`01M7APWPZV0MEVG8KA01TA3C61`), on Arch's ruling. Rows: `docs/known-limits.md` (draft, 11-13). Row-to-issue map: `d-known-limits` in `docs/internal/design/tier1-corpus-manifest.csv`.
**Account:** web-seed-1386 (PA's test account) on beta.
**Blocked:** the sign-in has been down since 11-10 18:25 (the credential file's format, classifier-refused). The decision is with xian via Exec (`01M79Q8226TJGVZ9XK9FAC0K1X`). This plan is written now so the reads run the hour it clears.
**Build:** read on whatever beta serves after the 11-13 morning promotion. Record the `/health` sha on every quote.

Each row gets one result: **still fails as worded** (quote), **fails differently** (quote; Docs rewords), or **passes** (Docs deletes the row in a commit that has the fix as an ancestor). Quotes are the exact replies, untrimmed.

| # | Row (issue) | Surface | The read |
|---|---|---|---|
| 1 | Deleting several todos (#2025), shape A | chat | Add 3 throwaway todos. "show my todos", then "delete the first two". Then "show my todos" to see what's actually left. |
| 1b | Same, shape B | chat | Fresh chat with no list shown: "delete todo 1 and 2", then "show my todos". Keep only the half that fails (Arch). |
| 2 | Deleting or archiving a chat (#1516) | browser | Open History and record every control offered on a conversation (screenshot plus the control labels). Compare with the tester page's "Hide or delete a chat" line. |
| 3 | Private session (#1164) | browser + chat | Turn on "Start private session" in History, send one distinctive message, turn it off. Does History list that conversation? Does a later "what did I tell you about <word>" recall it? This shows only what the page shows; whether the server stores it is a Lead or Arch read. |
| 4 | Counting issues (#2185) | chat | "how many issues do I have open?" Compare with GitHub's count for the account's repos. Then "show my most recent issues", checking the date order. |
| 5 | Milestones (#2184) | chat | "what issues are in milestone <X>?" Compare with the GitHub milestone page. Needs a repo with a milestone on the test account; if none, mark "not read" with that reason. |
| 6 | Overdue todos (#1961) | browser | A todo with a past due date, still open. Is it shown struck through on the todo list? |
| 7 | Sharing (#2166) | browser | Share a todo, a list and a project from the screen. Quote the error or the success. |
| 8 | Several requests in one message (#2041, #2030) | chat | One message with two asks, one of which makes an offer or asks a question (e.g. "add a todo to call Sam and what's on my calendar tomorrow"). Is the offer or question kept, and rendered as buttons rather than plain text? |
| 9 | A failed action that looks like a success (#2208) | chat | The learned-pattern action. Needs #2208's repro steps; read the issue first. |
| 10 | Preferences on a repeated question (#2056) | chat | Ask X, set a preference that changes X's answer, ask X again within the cache window. |
| 11 | iPad in portrait (#1907) | device | No iPad reachable from PA. Mark "not read: needs a device" unless Web or xian has one. |
| 12 | The Claude and MCP connection (no issue) | connector | No single repro. This is a judgment row for CXO, not a read. PA can quote the current connector state (#2342 rows) as context. |

Chat rows run through the existing driver (`twoturn.py` or `turn.py`) once the sign-in works. Browser rows (2, 3, 6, 7) need a signed-in browser on the same account, which hits the same credential wall. If those go to Web, Web needs the same unblock.

Clean up after: delete the throwaway todos from rows 1 and 6, and leave the account as found (8 open, listed in the carry-forward).
