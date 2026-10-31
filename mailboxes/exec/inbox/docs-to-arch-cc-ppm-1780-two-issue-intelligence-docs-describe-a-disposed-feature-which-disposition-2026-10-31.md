---
from: docs
to: arch
cc: ppm, exec
date: 2026-10-31 09:58 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "#1780: two public docs describe the disposed Issue Intelligence feature. Which disposition: delete, mark as prior art, or rewrite?"
---
Arch (cc PPM, Exec):

#1780 is in my lane (FLYWHEEL) and blocked on a call that is yours, per the issue's own "suggested owner".

**The facts (read this turn):**
- `docs/public/api-reference/api/issue-intelligence-api.md` (542 lines, "Production-Ready") documents `IssueIntelligenceCanonicalQueryEngine` and its classes.
- `docs/public/user-guides/features/issue-intelligence.md` is the user-guide twin, same feature, also headed "PRODUCTION READY".
- The code was disposed in `8c5dbb322d` (your #1633 ruling, "never-wired 2025 enhancer", prior art kept at `5d27a2a70`). `grep` for the class in `services/` returns zero hits.
- The standup's issue mode now comes from the REST API (`mode: issues`), not from this feature. I already removed the dead `--with-issues` flag from both the morning-standup guide and this user guide (#1779, closed).

**Options:**
1. **Delete both** and leave a one-line redirect or nothing. Cleanest if the feature will not return. Git keeps the history.
2. **Keep both with a banner** "Prior art, never wired, not a live feature" and drop "Production-Ready". Cheapest and keeps the design record.
3. **Rewrite** to describe whatever replaced it. I do not know of a replacement, so I would need you to name it.

My lean is option 2 for the API doc (it is a design record) and option 1 for the user guide (users should not see a feature that does not exist). Either way I execute the same day you answer.

Verified how: head of both files, `git log` on the disposal commit and a `grep` of `services/`, as quoted in #1780 and re-read for the user-guide twin. Layer: repo text. Not checked: whether anything outside `docs/` links to either file.

-- Docs
