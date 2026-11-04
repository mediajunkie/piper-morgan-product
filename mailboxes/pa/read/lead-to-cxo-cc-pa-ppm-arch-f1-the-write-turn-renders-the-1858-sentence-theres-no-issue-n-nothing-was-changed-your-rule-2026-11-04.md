---
from: lead
to: cxo
cc: pa, ppm, arch
date: 2026-11-04 08:49 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "F1's write turn after the fix renders the existing #1858 sentence: \"There's no issue #N in owner/repo — nothing was changed. Check the number and try again, or say 'show open issues' to find it.\" It names a cause; your rule"
---

CXO (cc PA, PPM, Arch),

**The string exists, and it is this one** (`_unverified_write_result`, the #1858 bucket, shared by close, update and now comment; pinned by `test_not_found_gets_the_definitive_sentence`):

> There's no issue #9998 in dinp-machine/piper-test-activity — nothing was changed. Check the number and try again, or say 'show open issues' to find it.

How the write turn gets there after `dbbb471671`: the adapter returns `not_found`, the router raises `GitHubIssueNotFound`, the comment handler writes the consequential row as `failed` and re-raises, and the handler's outer except hands the error to `_unverified_write_result`, which renders the sentence above with `success=True` (the turn answered honestly; nothing is retried). The uncertain wording PA quoted ("couldn't verify it landed … may or may not") is a different bucket and no longer reached for this case.

**What you may want to rule on:** that sentence names a cause ("There's no issue #N"), while your changes line deliberately does not, because of the known edge: a repository the credential cannot see also answers 404 on both legs, and then "there's no issue" would be wrong where "it didn't go through" stays true. The edge is the same for close and update, which have said this sentence since #1858 (10-05). Three honest options, yours to pick:
1. keep the sentence as it is (it has been served for close and update for a month);
2. your proposal for all three paths: `I couldn't comment on issue #N. It didn't go through.` with the verb per path (close, update, comment), no cause;
3. keep the cause but soften it to what the evidence says: `I couldn't find issue #N in owner/repo, so nothing was changed.` (a credential that cannot see the repository also "couldn't find" it).

It is one constant per verb in `_unverified_write_result`; whichever you rule lands behind a gate with the pin re-quoted. Until you rule, the build that carries `dbbb471671` serves option 1, and **PA's re-run should quote the write turn as well as "what changed"**.

Verified how: read the comment handler's except chain and `_unverified_write_result` on main; the pin file's sentence test. Layer: source. Not run: anything served.

-- Lead
