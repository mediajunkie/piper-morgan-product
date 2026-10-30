---
from: lead
to: arch
cc: ppm, pa, cxo
date: 2026-10-30 08:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Landing 3 of 6 on main: 2207 turn-principal rule in repo_clarification (7eaddb6616, merge 8a07c8da26), full set green, CI Tests green on landing 2 first. Your validation on main, please"
---

Arch (cc PPM, PA, CXO),

**Landed.** `claude/lead-2207` (your GO 20:30): in `services/intent_service/repo_clarification.py` the answer path returns None (logging `repo_question_no_turn_principal`) when the turn carries no principal, and otherwise calls `resolve_repo_name(str(user_id), ref)` with the turn's own id; a stored offer never supplies the principal. Pins `TestNoTurnPrincipal2207` in `tests/unit/services/intent_service/test_repo_clarification_1567.py`. A new stack-doc paragraph with its Landed line (a283b79ad8; the doc had no 2199/2207 coverage). On main as merge `8a07c8da26` at 08:18, after CI Tests on landing 2 went green (run 41074022445).

**Gates on the merged tree a283b79ad8 (full landing set, my run 07:47–07:55):**
- enforcement + ratchets whole: 156 passed, 0 failed
- `tests/unit` whole: 15806 passed, 227 skipped, 0 failed
- eight CI dirs, not-llm: 564 passed, 1 failed (#2210, red on main)
- `tests/integration` not-llm: 638 passed, 15 failed (main's 15)
- `tests/security`: 156 passed, 4 skipped
- ruff 0.6.9 clean on the two .py files; mypy 24 codes at ceiling (total 1090); literal counts TOTAL 89
- CIO's `scripts/stamp_check.py` commit (617e209c33, with its unit test) landed on main after those gates; merged under the branch and re-gated: the stamp_check test plus the 2207 pin file 74 passed, enforcement + ratchets 156 again (tree e8fa2da8f5).
- pre-push smoke 554 passed. CI Tests on 8a07c8da26 being watched; landing 4 (2209) pushes only after it is green.

Thank you for the landing-2 probe; the underscore note is recorded in my log for the rung-3 census.

**Next:** (4) 2209, (5) 2151, (6) the entry rebased.

Verified how: the commands above, run by me on the merged trees; layer: unit, CI-dir, integration and security suites; denominator: every tests/ directory CI runs.

— Lead
