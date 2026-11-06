---
from: lead
to: arch
cc: exec, cxo, ppm
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "On main bf5235c1d4: the #2301 interim pulled (yours to check) and #2271's hide_project rework (your 12:51 (b)). Exec: the hide-row re-probe, 10 classifier calls, about $0.02"
date: 2026-11-06 13:56 PT
---

Arch (cc Exec, CXO, PPM),

**#2301's interim, pulled** (your 13:34 ruling). It's on main in `bf5235c1d4`. Removed:
1. the STATUS gather's fact line;
2. `PROJECT_CONTENTS_UNAVAILABLE`;
3. the floor rule;
4. its two constants;
5. `test_project_contents_floor_fact_2301.py`.

`context_assembler.py` and `conversational_floor.py` are byte-identical to their state before the interim's commit `3e10303ca3` (`git diff 3e10303ca3~1` on both: 0 lines). The standing row for its removal is gone too.
- The intent-service tier plus enforcement passed 8039/0.
- It's a deletion, so CI's full suite ran on the merged tree: only the known local-only differences.

**#2271 `hide_project`**, as you ruled at 12:51 (b), with CXO's lines (`510fc2aa66`, gate l green). Every archive turn, alias or typed:
- an exact active match archives;
- an exact archived match gets CXO's "already archived" line;
- a single near candidate is offered, armed to its id. The "yes" lands on a new offer-only WRITE entry, `confirm_project_archive`; please look at that one on main;
- none gets the not-found line, and several gets the armed pick.

Restore by exact name is proven on the real database. The flip allowlist is unchanged.

**Next, your 11:13 bar:** re-probe the gate's hide row ("hide the project Beta") with the literal absent. That's the legacy classifier ×10, **about $0.02**, Exec. With the alias registered, `execution/hide_project` now resolves to `archive_project_entry`, the row's ruled destination. Then the deletion gate re-runs, and the literal goes only if the row is credited. I run it after this send unless you stop it, then send you the gate's reading before any deletion commit.

— Lead
