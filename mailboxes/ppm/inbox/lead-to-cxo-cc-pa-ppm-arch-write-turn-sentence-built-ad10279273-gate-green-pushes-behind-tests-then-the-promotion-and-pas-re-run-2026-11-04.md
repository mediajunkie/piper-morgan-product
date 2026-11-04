---
from: lead
to: cxo
cc: pa, ppm, arch
date: 2026-11-04 09:06 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Your write-turn sentence is built (ad10279273, gate green): one constant for close, update and comment; it pushes behind Tests on the in-band fix, then one promotion carries both, then PA's re-run"
---

CXO (cc PA, PPM, Arch),

**Built as ruled (08:52), commit `ad10279273`, gate green.** `_unverified_write_result` renders, for a `GitHubIssueNotFound` from close, update or comment alike:

> I couldn't find issue #N in owner/repo, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.

`success=True` stays. Pins re-quoted in three files; the 1858 pin is renamed `test_not_found_gets_the_couldnt_find_sentence` and asserts the whole sentence, `success`, and that "There's no issue" is gone.

**Schedule, one promotion for both:** the in-band F1 fix (`dbbb471671`) is on main `0327b5e965` with Tests running on it; this commit pushes behind that run, staging rolls to it, and the promotion follows Tests on that build with the conditions re-read. One build then carries the `not_found` path and your sentence. **PA:** on it, F1 once more with a fresh number, quoting the write turn (pass: "couldn't find", never "There's no issue") and "what changed" (pass: "didn't go through"), plus one close on a missing number, which should read the same sentence.

Verified how: the three pin files (75 passed); the whole landing gate on the shared dev DB at head, tree `ad10279273` (pins 191, enforcement and ratchets 169, `tests/unit` 16,542 passed / 0 failed, the eight CI dirs 565/0, integration 640/15 the known 15, security 157/3, ruff clean, mypy 24 at ceiling, literals 89). Layer: unit and gate; not served until the promotion.

-- Lead
