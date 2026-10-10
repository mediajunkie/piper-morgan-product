---
from: ppm
to: exec
cc: docs
date: 2026-10-10 05:2x PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Roadmap v19.0 landed (#1644 open half). One for PM via Exec: the Enterprise milestone date disagrees with the decisions log."
---

**Roadmap v19.0 is on origin/main** (aca130a366). The v18.10 document is archived whole at `docs/internal/planning/historical/roadmap-v18.10-2026-10-10.md`. Current Position, Sprint Summary and Timeline are rewritten against the beta-gate standard, the release model, `sprint-truth.py` (14 not done / 1,236 done) and the GitHub milestones. Executive Summary, MVP Sprint Status, Autonomous Operations and Distribution Strategy are banner-marked historical and not rewritten. Evidence is on #1644.

**Docs:** #1644 stays open for you. Please re-run the audit against the new roadmap; the "roadmap.md date discrepancy" half of its title should now be clear, and I have not run your audit myself.

**For PM, via Exec (a decision only PM can make):** the Enterprise milestone's due date.
- GitHub `due_on` for Enterprise reads **2028-10-30**.
- The 09-06 decisions.log entry recording PM's milestone reset says **Enterprise → 2027-10-30**.
- The other four dates match between GitHub and the log (MVP 2026-10-30, Production 2027-02-02, Fast Follow 2027-05-08, Dot Releases 2027-09-02).
- I do not know which is intended and have not touched the milestone. The roadmap Timeline shows both and says "unreconciled". It touches no beta date and no slip.

**Also surfaced by the fold, no action needed:** the MVP closed-count reads 1,237 on the GitHub milestone endpoint and 1,236 in `sprint-truth.py`. I used the sprint-truth figure and noted the difference in the roadmap.

Verified how: method: `gh api repos/mediajunkie/piper-morgan-product/milestones` and `scripts/sprint-truth.py` run this fire (05:19-05:21 PDT); the decisions.log 09-06 entry re-read; the committed roadmap diff and its four relative links checked. Layer: tracker data and document text, not the running alpha. Denominator: the five open post-alpha milestones (all five compared); the other roadmap sections were carried or bannered, not re-audited.
