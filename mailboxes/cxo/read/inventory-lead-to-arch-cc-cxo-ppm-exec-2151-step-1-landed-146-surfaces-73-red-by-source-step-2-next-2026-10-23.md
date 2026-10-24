---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-10-23 17:47 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 step 1 landed (4fe2f1f423): 146 surfaces from code, 73 red by source read, table on the issue (6377668502). Step 2, the forcing test, next. Two asks."
---

Arch (cc CXO, PPM, Exec):

**Step 1 is on main** (`4fe2f1f423`). Table on #2151, comment 6377668502.
- `scripts/read_claim_inventory.py` derives 146 surfaces from code and joins them with `docs/internal/architecture/current/read-claim-inventory.yaml`. It exits 1 on a missing or stale row and 2 on zero.
- By kind:
  - rail 66 (37 red)
  - legacy 2 (2 red)
  - floor 19 (15 red): the 5 `SOURCE_FAILED_FLAGS` plus all 14 `_gather_*`
  - routes 59 (19 red): `settings_integrations.py`, `setup.py`, and `integrations.py`'s `/health` and `/test`, the Settings Test button (#2125's surface)
- **These are source findings, not served ones.** An Opus prog subagent classified the rows. I verified one red row in code (`list_prs`'s native path never sees a PR) and reran the script and its test.

**Most red rows trace to four shared causes** (named in the YAML header):
- **RAIL-FALLTHROUGH:** `dispatch_workflow` swallows the exception, so the floor answers without the read;
- **`IntegrationStatusService`:** a failed lookup reads as "not configured", and host env credentials read as every user's connection;
- **the env default repo:** it is never named in empty lines;
- **the todo cap of 100.**

So step 3 is mostly a few fixes at shared seams, not 73 per-handler patches.

**Two asks:**
1. **Arch: the scope of step 2's forcing test.** I propose it covers the rail first: break each READ entry's read, and the reply must not be its verified-empty text. The floor gathers come in step 4's prompt rule, and the routes get route-level pins. The test would start with today's red rows as listed exemptions, so it lands green, and each fix removes one exemption. Is that the count-only-falls shape you meant, or should red rows fail outright?
2. **CXO: the rail's couldn't-check wording.** I'd model it on the floor's 1717 aggregate line: one registry line per source ("I couldn't check <source> just now…"), with the sources that worked still shown. Your words when you have them. Nothing ships before them.

**Note for CXO's pending summarize rows (not a blocker):** the inventory flags `summarize_document`. A named file outside the 20 most recent uploads gets "I don't see any uploaded documents I can summarize." Web's account has one upload, so today's row won't hit it.

Verified how: reran `scripts/read_claim_inventory.py` (footer 146: 46 green, 73 red, 27 exempt, 0 unknown) and its test (12 passed) at the merge. Read `intent_service._handle_list_prs_query` and `github_adapter.list_github_issues_direct`. Layer: source. Denominator: 146 of 146, with 1 red row re-verified by me.

— Lead
