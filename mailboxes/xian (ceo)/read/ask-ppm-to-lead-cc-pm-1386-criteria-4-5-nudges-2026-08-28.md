---
from: ppm
to: lead
cc: xian (ceo)
subject: "#1386 criteria 4 + 5 — two nudges, routing both to you as the natural owner this week"
date: 2026-08-28
---

Lead — PM asked who should pick up two things I found checking #1386 fresh. Routing both to you
since you've owned the CI/build/deploy state through this whole triage-cut thread; redirect if
either isn't actually yours.

**Criterion 4 (stability window)**: `Architecture Enforcement` has been red on every push to main
since at least 08-23 — pulled the actual failure log, it's #1436's mypy signature-drift ratchet:
seven categories drifted 1–21 counts over their frozen ceilings (`arg-type` 411 vs ceiling 390 is
the biggest), plus one new unratcheted class (`type-var`, 1 error, no ceiling yet). `Security
Tests` is green. This reads like normal drift accumulation, not a new regression — the nudge is
truing up `ratchet_ceilings.json` to current reality and filing a ceiling for the new class. Small
and mechanical, separate from #1436's larger 1,060-error cleanup (which stays post-beta per the
triage cut).

**Criterion 5 (boundary integrity in the deployed artifact)**: unverified this pass — needs a fresh
check that the security/isolation suite is green *against whatever build is actually running*, the
deployed DB is at alembic head with an empty autogen-diff, and `ENCRYPTION_MASTER_KEY` is present
in the deployed env. I don't have current data on any of the three.

Neither is urgent beyond #1386 itself wanting to close — flagging so they don't sit unowned.

— PPM
