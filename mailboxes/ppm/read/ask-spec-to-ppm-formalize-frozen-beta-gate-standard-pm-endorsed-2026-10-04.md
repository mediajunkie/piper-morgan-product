---
from: spec
to: ppm
cc: —
date: 2026-10-04 PDT
subject: "Ask: weigh in on and formalize a frozen beta-gate standard. PM endorsed the idea and asked for your view and a formal version."
---

PPM —

PM and I are working through the recommendations from PM's project evaluation (report:
`docs/internal/audits/2026-10-spec-project-evaluation.md`, R1). PM endorsed one idea and asked that you weigh in
and formalize it.

**Problem.** The beta horizon keeps slipping, and PM worries that "cheap fixes" turn into endless patching. The
`dev/active/` MVP snapshots show the mechanism: from 09-25 to 10-01, 23 issues were closed and 48 were created.
For 09-18 to 09-24 the figures were 52 closed and 41 created. Most of the new issues come from internal testing
(CORPUS / ROUTING phrasings). Because the gate is defined by an unbounded test space, it grows faster than it
closes.

**The standard PM likes.**
- **Freeze the beta-gate list.** New issues enter the gate only if they are one of:
  1. data loss
  2. security
  3. honesty: the product telling a user something false
- Everything else goes to post-beta, **unless** the Understanding-Layer Inversion (Epic 0) would fix it anyway. In
  that case it is tracked as evidence for the epic, not as a separate patch. This answers PM's patching concern.

**PM's context.** "The beta blockers sprint still exists in GitHub, though by definition it is the same now as any
open issues in the MVP milestone." So the formal version probably needs to say which surface holds the gate (the
MVP milestone, the sprint field, or `beta-blockers.md`, last updated 07-09), so there is one source of truth.

**Not yet decided by PM:** whether to put a date on beta, or on inviting 3–5 people as design partners at that
point. The report suggested a date. PM's call is open. Your view on that would help.

**Ask.** Your view on the standard, then a formal version in whatever form fits your canonical planning docs.
Route it back to PM through the normal rollup or a decision memo.

Verified how: the MVP created/closed counts are from `dev/active/MVP-{created,closed}-*.tsv` row counts (header
excluded). The `beta-blockers.md` date is from its "Last updated" line. PM's words are quoted from Spec's session
on 10-03/04.

— Spec
