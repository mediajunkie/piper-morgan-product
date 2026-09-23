---
to: xian (ceo)
cc: exec, lead
from: arch
date: 2026-09-23
subject: "CORRECTION — I told you #1744 was done. It wasn't. Reopened, and said why plainly on the issue."
in-reply-to: closed-arch-to-pm-cc-exec-lead-1744-behaviorally-confirmed-classic-gone-mainold-untouched-2026-09-23.md
---

**My last memo was wrong.** I closed #1744 based on the issue body's checklist showing
`[x] delivery path observed end-to-end` — I read the checkbox and not the issue's own 09-10 comment,
which says explicitly: *"Checkbox stands as written — the delivery path has still not been observed
working."* The issue is a synthetic test fixture; that checkbox being checked is the fixture's
**target condition for testing whether a scanner catches it**, not a real attestation. I mistook the
bait for the answer.

**Reopened it, full correction posted on the issue itself.**

**What's actually true, and it's real progress, just not closure**: everything I verified this
afternoon and this fire (ruleset live, Admin bypass confirmed behaviorally via my own push, classic
gone, `main-old` untouched) is correct and unaffected by this error. What's still unverified is the
one thing the issue was always actually testing: **whether the scope-guard Action's own
`GITHUB_TOKEN` push — not my admin push — now lands a memo at PPM's inbox end-to-end.** That needs an
actual re-run of the synthetic test, same as the 09-11 re-test after the PR rule was removed. Nobody
has done that since today's fix landed.

**Not asking anyone to do that re-test right now** — naming what's left, not creating urgency. I
caught this myself, before anyone else had to, by going back to the issue's own history instead of
trusting a closed-issue notification to mean what it said.

— Arch, 2026-09-23
