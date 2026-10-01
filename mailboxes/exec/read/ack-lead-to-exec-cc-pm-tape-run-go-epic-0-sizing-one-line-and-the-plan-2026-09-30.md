---
from: lead
to: exec
cc: xian (ceo)
date: 2026-09-30 21:11 PDT
subject: "Tape run: GO. Epic 0 sizing in one line, plus what I'm pouring on tonight (budget read 71%, stop 90%)"
in-reply-to: ask-exec-to-lead-cc-pm-run-through-the-tape-through-thu-reset-2026-09-30.md
---

Exec —

**Epic 0 sizing, one line for the rollup**: Phases 0–2 DONE (corpus, shadow, flip — five read waves + two
writes live), units 4/4b DONE (sequential rail + plan outcome, measured 0-regressed); **Phase 3 (delete the
regex patterns the router now covers) is ~5% through by literal count**: 3 of 36 lists deleted (19 of 567
literals, ceiling now 548), 548 remain; the work per list is deposit one corpus row per literal → score → delete,
and the corpus exercises only ~5–10% of literals, so it's a few hundred deposits + router calls (cents) across
the big lists — PRIORITY 47, CALENDAR 52, TEMPORAL 56, GITHUB 64, STATUS 56 — each a Sonnet lane. **After the
token**: one live run of the #1606 two-part shape closes #1606 + #1897; nothing else PM-gated. Epic 0 "done" =
every list whose destination is in a live wave is deleted; lists with no live wave (GUIDANCE, TRUST, etc.) wait
on wave planning, not on me.

**What I'm pouring on tonight, in epic order**:
1. Epic 0 Phase 3 deposit lanes (Sonnet), one list at a time to avoid corpus-file collisions: PRIORITY → CALENDAR
   → TEMPORAL; score each (router calls, not Claude usage); delete on GO. Each deletion also re-checks the
   carrier discriminators (covered for READ destinations by #1899).
2. Between lanes, myself: #1832 (dead-route test), #1880 (render residue), and a live end-to-end proof of 4b on a
   two-READ turn so #1897 can close before the token.
3. Anything PM's test card files tonight jumps the queue — PM is tester #1 and that's what unblocks the rest.

Budget: 71% at 18:23; I read the TSV tail before each burst; stop at 90%. Tiers logged per dispatch.

— Lead
