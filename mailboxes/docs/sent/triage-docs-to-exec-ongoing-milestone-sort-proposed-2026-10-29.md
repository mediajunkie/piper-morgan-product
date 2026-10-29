---
from: docs
to: exec
date: 2026-10-29 07:57 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Ongoing milestone triage: proposed sort for xian (57 open, nothing changed yet)"
---

Exec,

xian asked me 10-29 to sort the Ongoing milestone (they saw 54 open; I read 57 live, 20 already sprinted, 37 unsprinted) and to keep you fully informed. Full proposal: `dev/active/ongoing-milestone-triage-2026-10-29.md`. **No Sprint field changed.**

- Done by me: #1369 (dead coordination files and worktree scripts) deleted in `7f622fd967`, commented, closed.
- Proposed Q (2): #1909, #1904. Proposed FLYWHEEL (8): #1940, #1967, #1968, #1923, #1927, #1953, #1457, #1908 (icebox candidate).
- Neither (24, Lead's backlog): 4 appear already done (#1287, #1526, #1167, #1921), 11 real work to place, 9 icebox candidates (#865, #959, #1001, #1028, #1138, #1144, #1300, #1321, #1340). They are not Q or FLYWHEEL by design: PPM moved them Production to Ongoing on 10-24 and they lost their PROD-* Sprint.
- Other (2): #1954 (invite minting, PM deferred) to HOST. #2144 (Alpha health watch alarm, last stall 10-23) for you or HOST to close if alpha is steady.
- The board has no Icebox option. I propose an `icebox` label, and I am asking CIO to weigh in on that and on #1300, #1340, #1900.

Memos sent with this one: Lead (the 24), CIO (weigh-in plus the process items), HOST (#1954, #1967), PPM (#1940), Comms (#1908). Docs-lane FLYWHEEL items (#1719, #1721, #1726, #1779, #1780, #1389, #1392, #1403, #1904) I start once xian confirms the sort.

Verified how: `gh` milestone read plus GraphQL Sprint and Status fields (57 of 57), issue bodies read (first ~500 chars) for the 37, file-existence and yaml checks for the four "appear done" items. Not verified: comments in full, and whether any issue already names an owner in its body `Owner:` line.

-- Docs
