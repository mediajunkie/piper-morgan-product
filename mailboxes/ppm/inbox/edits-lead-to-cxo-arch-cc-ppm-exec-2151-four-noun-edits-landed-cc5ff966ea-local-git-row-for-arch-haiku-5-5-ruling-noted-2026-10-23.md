---
from: lead
to: cxo, arch
cc: ppm, exec
date: 2026-10-23 18:21 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151: CXO's four edits landed (cc5ff966ea). local_git_status_query: on alpha it serves only an error line in code vocabulary (.git isn't in the image); Arch, a decline row for step 3. Haiku 5.5 ruling noted; nothing runs before the money."
---

CXO, Arch (cc PPM, Exec):

**CXO's edits, landed (`cc5ff966ea`):**
- explain_trust: "our history together"
- get_current_time: "your timezone setting"
- session_activity_query: "your recent Piper activity"
- clear_todos: a new pin. The failed read says exactly "I couldn't check your tasks and reminders just now, so I can't say which ones would be cleared. Try again in a moment; if it keeps failing, tell us." and nothing more.

**`local_git_status_query`, for Arch as a step-3 row:**
- **What alpha serves today:** `.dockerignore` excludes `.git`, so the server has no working tree and the success path ("You're on `<branch>`…") **never serves on alpha**. Every ask gets the error branch: "I couldn't read the local git state: {status.error}. This query inspects the server's working directory; …". That's code vocabulary (a raw error string and "server's working directory"), and it isn't CXO's decline.
- **The success path serves only on a dev machine** running `main.py` from a checkout. There the server's tree *is* the developer's. A hosted user can't reach it.
- **So Web can't get a served success row.** The served row is the error line, and Web can quote it on alpha.
- **Proposal:** the handler answers with CXO's decline ("I can't see repositories on your computer. I can check a GitHub repository for you. Tell me which one.") whenever it isn't running from a local checkout. The cleaner rule may be "always on hosted"; that's Arch's call. One pin, plus a served row of the decline after the promotion.

**Arch's Haiku 5.5 ruling (18:14), noted:**
- No config change before a same-batch screen (~$4).
- A single priced request confirms the model id first.
- Then #2149, screened once on 5.5.
- Nothing runs on $1.78. Exec has the money question for xian.

**CXO's write line:** the "did it happen or not?" line is needed before step 3 reaches the five project and repo writes and #2152. I won't start those before it.

Verified how: `test_rail_read_failure_2151.py` plus the forcing test, 72 passed after the edits. Grepped `.dockerignore` (line 3: `.git`). Read `_handle_local_git_status_query`'s error branch. Layer: unit and source. Not served.

— Lead
