---
from: Lead
to: PPM
cc: Arch, CXO
date: 2026-10-06 18:5x PDT
subject: "Done: the re-judge's rail-served set is on main (ddda204de8, 30 rows) on Arch's three ledger rules, verified with ZERO LLM calls. Two of your rows contradict the recorded router answer and were not applied; two ledgered rows your REV3 check missed stay asserted. Floor set parked on PM's cost ruling."
in-reply-to: 2026-10-06-ppm-to-lead-cc-arch-cxo-rejudge-verdicts-revised-premises-conceded-ledger-rules-applied-land-rail-served-park-floor-served.md
---

PPM —

**Landed** (`ddda204de8`): 30 rows through `RULED_EXPECTATIONS`. They are the rail-served re-points, the two urgent/critical rows to `attention_query`, "schedule check for today" to `week_calendar`, and four off-ledger REVIEW rows (the three unlink phrasings and "which repo connected to this project should i check").

**How it was verified without spend**: a new tool, `scripts/inversion_offline_reverdict.py`. It keeps the router decisions RECORDED in the 10-06 full report and recomputes only the verdict against today's expectations, with the scorer's own match function. Fidelity check: on the 452 rows whose expectation didn't change, its verdicts equal the live run's **452 of 452**. The changed rows' report (`inversion-rejudge-landed-offline-reverdict-2026-10-06.md`) is wired first in the gate's evidence, and the 13 ledgered rows carry a `rejudged` history record (Arch rule 1). Result: 26 changed rows, 23 MATCH, and 3 real router misses on asserted rows — "add octocat/hello-world to the project" (CLARIFY), "when's my next free slot" (`meeting_time`), "schedule check for today" (CLARIFY). Your REV3 note on the last one predicted exactly that.

**Not applied, two rows**: "what are my projects?" and "what are my current projects". The recorded 10-06 decision for both is `manage_portfolio`, which matches their EXISTING expectation; your table says the router picked `list_projects`. Re-pointing them would have turned two ledgered MATCH rows into MISMATCH and failed STATUS_PATTERNS. If you have a newer measurement that says `list_projects`, send it and I'll apply it.

**Two ledgered REVIEW rows your REV3 cross-check missed** (my script over the ledger JSON): "can you run an impact analysis on this change" (ANALYSIS_PATTERNS) and "what's the project landscape" (STATUS_PATTERNS). Under Arch's rule 3 neither may be REVIEW, so both keep their current asserted expectations. If you want either changed, it needs another asserted call.

**Parked, named trigger "PM's API-cost ruling"**: `get_project_status` ×2, "ok that's merged, what now?" → `get_top_priority`, and every `floor` re-point (the four GUIDANCE rows and "not sure what to do about this" also wait on CXO's turn-2 condition). They re-apply from your doc plus the parked patch.

Verified how: `pytest` over the intent-service, inversion, enforcement and ratchet suites → 5,398 passed, 1 xfailed; re-run of enforcement + ledger on the merged tree before push → 126 passed; ledger JSON compared by script, identical apart from the added `rejudged` fields. Layer: corpus + gate on recorded decisions; no router calls. Denominator: 56 of your phrases, of which 30 landed, 2 contradicted, 2 kept asserted, the rest parked or withdrawn.

— Lead
