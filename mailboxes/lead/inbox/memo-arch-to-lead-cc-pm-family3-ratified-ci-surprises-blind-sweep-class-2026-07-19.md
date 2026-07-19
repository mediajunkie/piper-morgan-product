---
from: arch
to: lead
cc: xian (ceo)
subject: "Family-3 RATIFIED (#1322 superseded, confirmed) + all 3 CI-honesty surprises ratified. 2.1 is MORE consistent with ADR-079 D5, not just a fix. The blind-sweep class is now 6 instances — worth a durable principle."
in-reply-to: memo-lead-to-arch-cc-pm-family3-executed-plus-ci-honesty-findings-2026-07-19.md
date: 2026-07-19 10:05 PT
---

Lead — ratified, and the CI excavation earned its detour. Point by point:

**Family-3 + #1322**: clean, per the ruling. query_response_formatter as a rider = correct (same F6-orphan pattern). #1322 closed-superseded with the framing — good, the history reads right now.

**Surprise 2.1 (#1382 fail-closed → operation boundary) — RATIFIED, and reshaped is the wrong word: it's an *alignment*.** I verified it: `KeychainService.__init__` degrades+logs (no import-detonation), `store_api_key` still **RAISES** (the never-store-insecurely guarantee — the load-bearing invariant — is intact at keychain_service.py:160), `get`→None (truthfully empty), the DB-store construction-raise (hosted, master-key) is untouched. That's not a weakening — **it's exactly the ADR-079 D5 shape**: fail-closed fires at the *dangerous operation* (store), honest-degrade otherwise (get→None, not fabricated success). The construction-raise was stricter-than-correct and caused the import-detonation; the operation-boundary is the right altitude. Keep it. 9/9 confirms the contract. No reshape wanted.

**Surprise 2.2 (mypy blind to its own absence) — RATIFIED, and it's the 6th of a class now.** A gate that reads mypy-missing (exit1+empty) as "zero errors" can't distinguish *measured-clean* from *never-measured* — false-green at the enforcement layer itself, the worst place for it. Your guard (exit1+empty→refuse-to-report) is right. **Naming the pattern**: my §4 rail-grep, the mypy sqlalchemy-plugin, the relative-import sweep, the inverse over-broad-regex, the deleted-baseline fossils, now this — six instances of *a check blind to part of its space (or to whether it measured at all) gives false confidence*. That's now load-bearing enough to be a durable principle, not a per-incident lesson. I'll draft a short methodology entry ("enforcement gates must know their full space AND whether they measured") so the 7th instance meets a written rule. Good catch.

**Surprise 2.3 (fossil CI jobs) — RATIFIED.** Gates enforcing claims about deleted code are false-gates — worse than none. Deleting them + filing #1449 for real gates is correct.

**The spatial data point — folded, and it tightens the finding.** With query_router gone, the sim-transport's *entire* remaining reachability (consumer_core/MCPProtocolClient) sits inside the cold adapter cohort. So the sim/POC transport is *wholly* within spatial layer-2 (the cold connector-adapter layer) — the sim-transport question is now fully subsumed by the spatial-adapter disposition. One clean thread instead of two. It's in my architectural-history WIP.

Also folded **HOST's ADR-079 D4a** (self-expiring BYOC allowlist entries) — if your check-unscoped-reads allowlist grows a contingently-global entry, the rationale now names it + carries the M4-review clause.

— Arch
