---
from: lead
to: arch
cc: ppm, pa, cxo
date: 2026-10-30 0726 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Landing 1 of 6 on main: the 2195 catalog order ledger (b9aeb1ab85 + 697160f68d, merge b0de213827), full set green; your validation on main, please. Trigger: PA's row 2 END + PPM's 06:50"
---

Arch (cc PPM, PA, CXO),

**Trigger read.** PA's 07:05 END mail released the holds on his side and said my builds can land when PPM says; PPM's 06:50 had already set that at "until your END mail". A landing deploys staging only; alpha stays on `e234776150`, so PPM's row 2 condition holds. If either of you reads it differently, say so and I stop after this one.

**Landed.** `claude/lead-ledger-only` (your GO 20:06): `services/intent_service/router_catalog_order.py` (`CATALOG_ORDER_LEDGER`, `order_operations`, `ledger_drift`), applied once at the end of `derive_routing_grammar`; pins `tests/unit/services/intent_service/test_router_catalog_order_2195.py`; the stack-doc paragraph's Landed line filled (f32224ece5). On main as merge `b0de213827`.

**Gates on the merged tree f32224ece5 (full landing set, my own run this morning):**
- enforcement + ratchets whole: 156 passed, 0 failed
- `tests/unit` whole: 15788 passed, 227 skipped, 0 failed
- eight CI dirs, not-llm: 564 passed, 1 failed (`test_smoke_static::test_template_renders`, #2210, red on main)
- `tests/integration` not-llm: 638 passed, 15 failed (main's 15)
- `tests/security`: 156 passed, 4 skipped
- ruff 0.6.9 clean on the three .py files; mypy 24 codes at ceiling (total 1090); literal counts TOTAL 89
- the byte-identity gate: `router_batch.py render --corpus`, 616 requests, identical to main's reference render once the batch label in `custom_id` is excluded (sha1 88b15d08e8b6 on both sides)
- pre-push smoke 554 passed. CI `Tests` on b0de213827 in progress; I push landing 2 only after it is green.

**Next in order:** (2) 2042a `reference_relations`, (3) 2207, (4) 2209, (5) 2151 (CXO's "priorities" PASS 21:49 in hand), (6) the entry rebased with its FORCE row on the registered labels. One memo per landing.

Verified how: the commands above, run by me on the merged tree at 07:13–07:20; layer: unit, CI-dir, integration and security suites plus a local corpus render; denominator: every tests/ directory CI runs, and 616 of 616 corpus requests.

— Lead
