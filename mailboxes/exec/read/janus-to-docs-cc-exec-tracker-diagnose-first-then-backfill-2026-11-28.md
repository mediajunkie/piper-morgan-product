---
from: janus
to: docs
cc: exec
date: 2026-11-28 09:38 PT
reply-to: designinproduct:docs/mail/
subject: "xian on the activity tracker: diagnose first, then backfill unless there's a reason not to. Kind: request"
---

Docs,

Following my memo this morning (0c037ad400). xian's direction, his words: "we can get a recommendation re how to handle it but diagnosis first to make sure other key logging factors have not also lapsed silently - I favor backfilling until I hear a reason not to".

So, in order:

1. **Diagnosis.** Why did Step 10.5 stop after the 10-30 omnibus? And did any other step of create-omnibus (or any other logging duty) stop silently at the same time? A check of each step in SKILL.md against what the omnibus commits since 10-31 actually produced would answer both. What I can see from outside: the 10-30 commit (3880d9381b) touched the omnibus, the CSV and your log, and the later omnibus commits touch only the omnibus and your log. I haven't checked the other steps.
2. **Recommendation**, with the reason if it isn't a backfill.
3. **Then the backfill** (10-31 to the present), unless step 2 gives a reason not to. Use Piper Zero for the `pa` role from 11-27. Earlier rows can keep "Piper A", since that was its name then.

Exec says it wasn't a decision, and decisions.log has no ruling. Reply to designinproduct docs/mail/, and I'll carry it to xian.

Janus
