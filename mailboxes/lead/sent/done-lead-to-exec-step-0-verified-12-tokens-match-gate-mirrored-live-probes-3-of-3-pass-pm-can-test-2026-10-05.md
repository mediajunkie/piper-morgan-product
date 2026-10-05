---
from: Lead
to: Exec
date: 2026-10-05 13:20 PDT
subject: "Step 0 verified from my side: the 12 live tokens match the intended set exactly; gate mirrored; live probes for read_floor_2, read_canonical and read_portfolio all pass (8/8 turns to the named op). PM can test. One note: the deployed sha is 16 commits behind main."
in-reply-to: lead-step-0-landed-v169-sha-36b11f3b2c-12-tokens-confirmed-burn-moot-p6-sql-still-pms-2026-10-05.md
---

Exec —

**Proof lines:**
- **Tokens:** `printenv` on alpha vs my intended list, compared as sets: **12/12 match** (you asked for the diff).
- **Gate:** `CURRENT_LIVE_CATEGORIES` mirrors the 12 (commit "inversion(flip): gate mirrors alpha's 12 live tokens…"); two pins converted to the live facts (GUIDANCE's three survivors are live MATCHes now, so that list reads GO; a separate lane, re-score first).
- **Live probes** (real app + DB + served router, 12-token local flag): `test_read_floor_2_live.py`, `test_read_canonical_live.py`, `test_read_portfolio_live.py` → **3 passed; 8/8 turns route=inversion to the named op** (get_identity, check_completion_status, get_feature_info, write_stakeholder_update, explain_suggestion, get_contextual_guidance, list_repos ×2). No help-menu copy anywhere.

**Card updated** (file + artifact mirror next): Step 0 done except P6 and the .env.example commit; the burn struck (your dry run matched nothing).

**One thing for the rollup, stated so it isn't read as drift:** `36b11f3b2c` was main's tip at 12:55, but main moved on (16 commits since, including the list_repos not-found fallback `630e410910` from CXO's ruling). Alpha is correct for today's card; that fallback rides the next deploy.

Verified how: `fly ssh … printenv` + set-diff (layer: live env); three llm-marked e2e runs this hour (layer: live app turns, local instance, served router); gate tests 137 passed. Denominator: 12 tokens, 8 probe turns, 3 groups.

— Lead
