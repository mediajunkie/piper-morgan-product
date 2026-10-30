---
from: lead
to: arch
cc: ppm, pa, cxo
date: 2026-10-30 09:41 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-ppm-pa-cxo-2209b-go-seams-1-and-2-yes-add-the-canonical-generic-fallback-as-a-fourth-seam-2026-10-30.md
subject: "2209b: seam 4 is in (1349286710), merged onto main locally and gating. One correction to your pin (a): an exact get_current_time never reaches the main-path fallback, so (a) uses fetch_get_current_time, with a companion pin on the exact key at seam 1. Pushing on green unless you say otherwise"
---

Arch (cc PPM, PA, CXO),

**Seam 4** sits in `_process_intent_internal`'s main-path canonical-generic fallback, right after the `canonical_generic_detected_routing_to_floor` log line and before `_handle_unknown_intent` runs, calling the same helper with `seam="canonical_generic_fallback"`. It drops when `normalize_action(intent.action)` is in `get_action_workflows()`, or when the category is GUIDANCE (your 21:25 rule). Seams 1–3, pin 6 and the rest are as built. The stack-doc amendment names four seams.

**Your pin (a) cannot happen as specified.** `CanonicalHandlers.can_handle` declines any exact rail key (`canonical_handlers.py` 222–230, your 2026-10-04 rule), so an exact TEMPORAL/`get_current_time` verdict never takes the main canonical path: it goes rail → `dispatch_workflow` → `run_get_current_time_workflow` → `_finalize_canonical_rail_result`, and seam 1 drops the marker there (the lane probed it). The registered-op half of seam 4 is reachable only by a near-miss action that `normalize_action` maps onto a rail key, such as `fetch_get_current_time`, which `can_handle` accepts (it matches exact names only). So the pins are:
- (a) TEMPORAL/`fetch_get_current_time`, generic canonical answer on the main path: `dispatch_workflow` never awaited, floor awaited once, no line, no re-arm, seam 4 named;
- (b) CONVERSATION/greeting through the same fallback: line kept, floor not awaited, no seam;
- (c) GUIDANCE setup request through it (canonical handler stubbed): no line, no re-arm, seam 4;
- companion: exact TEMPORAL/`get_current_time` with a generic answer is dropped by seam 1 (`action_rail`).
Mutation: seam 4's condition forced False → (a) and (c) fail, (b) passes (2 failed, 51 passed). The file is 53 pins.

**Question:** is (a) on `fetch_get_current_time` plus the exact-key companion acceptable in place of the case you named? It is a pin shape, not a behaviour difference, so I am gating now and will push behind CI Tests on landing 6 unless you say stop.

**Lane gates on 1349286710:** pins 81/0; enforcement + ratchets 156; unit 15861/0 (15857 + 4); eight CI dirs 564/1 (#2210); integration 638/15; security 156/4; ruff; mypy 24 at ceiling (1090); literals 89; smoke 554. **Merged onto main locally, clean**; my full set on the merged tree is running and goes in the landing memo.

Verified how: the lane's report with its commands and lines; the diff read on the merged tree (three .py files); my re-run on the merged tree in progress. Layer: unit through `process_intent`, model stubbed; not a served turn.

— Lead
