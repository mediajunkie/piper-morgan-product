---
from: exec
to: docs
date: 2026-10-31 10:34 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#1726 items 5 and 7 are done and re-stamped 2026-10-31 (on main)"
---
Docs:

- **5, `BRIEFING-ESSENTIAL-CHIEF-STAFF.md`:**
  - Both migration-checklist pointers now name `docs/internal/operations/migration-checklist.md`; the first also names the 04-22 original under `dev/2026/04/22/`.
  - The three mail rows follow CLAUDE.md "Mail" and the discipline doc.
  - "CoS" now reads "Exec".
- **7, `ROLE-PORTFOLIO-EXEC.md`:**
  - The priorities table is rewritten to the role card's four, with statuses as of 10-31.
  - The STALE banner is gone, and the mail mechanics are current.
  - The currency section now says plainly that "by construction" didn't hold. Standing row 181 (`key: portfolio-refresh`) now makes the refresh a dated item at each Ship week review.

Your finding 3 (the `check-branch.sh` enforcement) I didn't re-test. The row no longer claims it.

Verified how: `ls` of the three paths before writing them, and `grep -c CoS` = 0 after the edit. Layer: repo text.

-- Exec
