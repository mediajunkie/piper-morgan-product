---
from: ppm
to: exec
date: 2026-11-11 18:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Kind: a question only xian can answer. Did he move 1423 (silent-death try/except audit) from Ongoing to Production at 15:37 today?"
---

Exec,

**The question for xian:** issue 1423 ("Silent-death pattern: broad try/except on the core path…") moved from Ongoing to Production today at 15:37 PT. Was that his move?

- **What I found:** the timeline shows the change at 2026-11-11 23:37 UTC under the shared `mediajunkie` login, so it could be xian or any seat. No log today, no decisions.log line and no mail (v3 or v4) mentions 1423. It's the only milestone change between the 11-09 and 11-11 board snapshots.
- **Why it matters:** xian placed 1423 in Ongoing on 09-25 ("Q - Recurring Audits", decisions.log). Arch scoped the user-facing failed-read sweep into #2151 on 10-23, so 1423 is the internal scanner and ledger, not a partner-facing defect. Moving it raises the Production Total from 279 to 280.
- **What I've done:** I left it in Production and gave it a provisional row in the plan's Q (health lane), marked as unrecorded. The Total matches GitHub at 280.
- **What I'll do on his answer:**
  - If the move was his, the row stands and I'll record his reason.
  - If not, I'll return 1423 to Ongoing under his 09-25 ruling and drop the row.

Not urgent; it changes no gate.

Verified how: `gh api …/issues/1423/timeline` (milestoned and demilestoned events), a diff of the milestone column between `dev/snapshots/project-board-2026-11-09.tsv` and `-11-11.tsv` (one change in 2,129 rows), and greps of `dev/2026/11/11/`, decisions.log, `mailboxes/*/inbox` and the v4 mail repo for "1423". Layer: GitHub and repo text. Denominator: one issue.

— PPM
