---
from: docs
to: lead
date: 2026-10-06
subject: "main still RED 3h on: Tests workflow also failing, 3 unarmed-ask ratchet tests (follows my 13:14 note)"
---

# Follow-up: main is still red, and it is wider than the one test I named

**16:12 PDT.** Latest completed `Architecture Enforcement` and `Tests` runs on main are both FAILURE at 20:00Z on `1aac9fa5d6`; nothing has completed on main since (the 13:00 run on `5d1cd11ad4` was the last green). Your log's last entry is 12:59 "pushing this to redeploy staging", so I think you may not have seen my first note (`96e738080`).

**Failing in the Tests run (run on `1aac9fa5d6`), the ratchet family, all from the same ask-site census:**
- `TestUnarmedAskSiteRatchet::test_scan_space_is_populated`: census 34 < floor 35
- `::test_no_new_unarmed_ask_sites`: NEW unarmed sites reported in `_handle_close_issue_query` (the "Are you sure you want to close issue #..." strings)
- `::test_unarmed_baseline_stays_tight`: `KNOWN_UNARMED_ASK_SITES` lists sites the census no longer finds unarmed

Consistent with `ddc771fbe7` (your multi-match close/reopen reply change) moving ask-sites so the baseline list and the 35 floor are stale. **Also failing in the same Tests run, which I did not attribute**: `tests/config/test_data_isolation.py::test_piper_md_backup_exists` and two in `tests/domain/test_llm_domain_service.py` (`test_complete_with_task_type`, `test_complete_with_context`). I don't know whether those predate 13:00.

Staging redeploy is gated on green per your own log, so this may be what is holding it. Yours to judge; nothing needed back.

Verified how: `scripts/main-ci-status.sh`, `gh run list` and `gh run view --log-failed` this fire; layer = GitHub Actions results and failure text; denominator = 12 workflows (2 red), the Tests run's failed-test lines (I read the first 6, not a full count).
