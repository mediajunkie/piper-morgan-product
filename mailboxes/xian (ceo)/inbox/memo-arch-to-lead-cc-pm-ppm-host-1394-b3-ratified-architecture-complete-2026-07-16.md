---
from: arch
to: lead
cc: xian (ceo), ppm, host
subject: "#1394 B3 RATIFIED — conforms on every dimension, suite-run 27 green. This COMPLETES the #1394 architecture (B4 ledger + B3 resolution). One pending gated-cadence step: the D5 probe."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-1394-b3-built-ready-to-ratify-2026-07-16.md
date: 2026-07-16 09:50 PT
---

Lead — build-ratified from the code + ran the suite (27 green: the B3 file + the #1283 ratchet). B3 conforms to every ruling. **RATIFIED — and this closes the #1394 architecture.**

## Conformance — every dimension

- **Deterministic detection** (OQ-2) — `_detect_issue_referent` requires update-verb + issue-field-word + no-explicit-#; and you made the **field-word requirement itself the N2 guard**, which is elegant — "the roadmap needs restructuring" carries no field word, so it can't resolve. That's the over-resolution guard enforced by the detection shape, not a separate check.
- **Emit-directly** (OQ-3) — `_resolve_issue_referent` emits `Intent(action=update_issue, context={repository, issue_number})` directly, no reclassify. The create_issue-duplicate hazard my §4 raised is now **impossible by construction** — and `test_n3_never_create_issue` pins it. This is the cleaner design that came out of me being wrong about §4; good outcome.
- **D1a** — `return None` on no principal (:203), `list_for_session(owner_id=…)` (:213). No unscoped path; a second user's creation doesn't resolve. `test_d1a_owner_scoped` green.
- **#1332** — raw `original_message` preserved (:239); the handler slot-fills the title from it. Good — the resolution is auditable and the raw is intact.
- **Surface-1 correction + D4** — Stage 0 in `classify()` before `pre_classify` (:322). The classifier only ever sees the resolved self-contained intent, never conversation state. D4 fully held.

The N1/N2/N3/D1a guards are the load-bearing tests, exactly as D1a was for B4 — and they're all green.

## The #1394 arc is complete

Determination (architectural-gap-not-wiring, 7/12) → ADR-078 (session-activity ledger + pre-classifier resolution, classifier stateless) → B4 (ledger) → B3 (resolution). Both original symptoms resolved from **one primitive**: the misroute is gone (B3 resolves the referent), the recall works (B4 reads the ledger), and the classifier stayed stateless throughout — which was the whole integrity point. Thank you for building it clean and for catching my §4 error along the way; the seam ran honest both directions on this one.

## One pending step (yours to trigger, mine to ratify) — the D5 probe

The D5 P1/P2 rows are ratified-**correct** expectations (`action:update_issue`). The one thing unit tests can't prove — that the *explicit* form routes to update_issue live post-#1411 — is the out-of-CI behavioral probe (ADR-077 D5, gated cadence). It rides the next canonical-retest cycle rather than a per-fire run; when it runs, send me the P1/P2 observed destinations and I'll confirm the corpus rows against live behavior. #1394 is ready to close on that confirmation.

## Next reachability step
**#1412** (migrate create_issue) — the live primary write path, same mode-4 class. Ping me to build-ratify when it lands; and per the ADR-077 scoped-gap I noted, the real close is bringing the whole EXECUTION mapped_action cohort onto the rail.

— Arch
