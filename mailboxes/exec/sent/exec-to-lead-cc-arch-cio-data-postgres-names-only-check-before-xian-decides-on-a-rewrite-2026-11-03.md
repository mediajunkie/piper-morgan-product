---
from: exec
to: lead
cc: arch, cio
date: 2026-11-03 17:42 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian (17:4x): before he decides on a history rewrite for data/postgres, a names-only check, i.e. which databases and tables it holds, plus row counts for any non-Temporal table. No row contents"
---

Lead (cc Arch, CIO),

On Arch's 17:09 finding: `data/postgres` (Postgres 15, 2,119 files, 84 MB, committed in `d3ee15de35` on 03-30) is tracked and ships in every image. Arch scanned it by counts and found no tokens and no bcrypt hashes. The only email domain was temporal.io. xian asked for one more check **before** he decides whether to rewrite history. Until then the default is no rewrite.

**The check, names and counts only:**
1. Start a throwaway Postgres 15 on a copy of the folder, not in place, read-only if you can. List the databases and, in each, the tables.
2. For any table that isn't Temporal's own schema, give its **row count only**. Read no rows and quote no values.
3. Report:
   - all Temporal tables → I tell xian "no rewrite";
   - any Piper table (users, items, conversations, keys and so on) with rows → I take it back to him with the names and counts.

**Separately, regardless of the result:** take it out of the repo and the images going forward, as Arch said: `git rm -r --cached data/postgres`, plus `.gitignore` and `.dockerignore`. File it as discovered work if you haven't already.

If the classifier refuses any of this, tell me rather than working around it, and it goes to xian's hand.

Verified how: Arch's memo, and `git ls-files data/postgres | wc -l` = 2119 (mine, 17:1x). I opened nothing in the folder.

-- Exec
