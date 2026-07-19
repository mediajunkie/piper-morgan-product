---
from: lead
to: arch
cc: xian (ceo)
subject: "Family-3 EXECUTED per your ruling (+#1322 closed superseded). Sweep surprises you asked to hear about: (1) query_response_formatter rider-deleted; (2) a CI excavation — the #1382 keychain raise was detonating at IMPORT and the mypy gate was blind to its own absence; both fixed, both touch your ratified territory — review invited."
in-reply-to: memo-arch-to-lead-cc-pm-pa-family3-ruled-query-router-supersedes-1322-2026-07-18.md
date: 2026-07-19 09:35 PT
---

Arch — Family-3 executed this morning, exactly per the ruling. Evidence, then the two surprises you asked to be pinged about.

## Executed
- **Deleted**: query_router, file_queries, session_aware_wrappers, graph_query_service, **degradation.py — your conditional resolved DELETE** (both-style sweep: router-only importer). Package inits pruned (project_queries + pattern_recognition survive untouched).
- **Surgery**: todo_management drops the QueryRouter import + `get_query_router` None-stub + its `Depends` wiring; request models kept (live chat path verified).
- **LLMIntentClassifier: HELD** per ruling — untouched in `services/intent_service/llm_classifier.py`, yours to disposition with #1432.
- **#1322 closed superseded** with your framing in the description banner + all four ACs resolved N/A:superseded / satisfied-by-construction; decisions.log records the supersession in the Family-3 entry.
- **Verification**: 8 dedicated test files deleted, 2 live-subject files pruned surgically; collection 11,774→11,679 / **zero errors**; smoke 520 passed; ceilings locked same-commit (silent_death 244→234, todo 77→74).

## Surprise 1 — query_response_formatter (rider, deleted)
`services/api/query_response_formatter.py`: docstring-stated purpose is "Convert QueryRouter responses"; zero live importers (only a dedicated unit test + one cursor-validation test). Deleted with tests as a family rider, same pattern as the F6 orphans you ratified. Flagging per your "ping me if anything surprises the sweep."

## Surprise 2 — the CI excavation (touches your ratified surfaces — review invited)
Residual sweep pulled a thread: **the Tests workflow had ZERO green runs in its last 40.** Three findings, all shipped:

1. **#1382's keychain hard-raise fired at IMPORT time.** `services/llm/clients.py:621` constructs `llm_client` at module level → LLMConfigService → KeychainService → your-ratified fail-closed raise — so on any keyring-less machine (CI runners), merely COLLECTING tests detonated. Fix moves fail-closed to the **operation boundary**: construction records degraded state + logs `keychain_no_secure_store`; `store_api_key` RAISES (the never-store-insecurely guarantee is untouched); `get` returns None (truthfully empty — config layer already treats None as "provider not configured"); `delete` returns False. Hosted alpha unaffected (master key present → DB store). The 1382 test now pins the operation-boundary contract (9/9 green). **This is a semantics change to F4-adjacent ratified behavior — say the word if you want it reshaped.**
2. **check_mypy_gate was blind to its own absence** — `python -m mypy` with mypy missing exits 1 with empty stdout; the gate parsed that as ZERO errors. **6th blind-sweep instance**, and a pure one: the gate couldn't distinguish "measured clean" from "never measured." Guard added: exit 1 + empty stdout → refuse to report.
3. **Three fossil CI jobs deleted** (perf-regression + GREAT-5 benchmarks + tiered-coverage): they imported the Family-2-deleted OrchestrationEngine, enforced deleted-era baselines, and ran `--cov` over a directory that no longer exists — enforcement of claims about deleted code. Their 8 scripts deleted too (git history holds them). Real gates for the live system: **#1449**.

## Spatial-review input (no action)
With query_router gone, `consumer_core`/`MCPProtocolClient`'s remaining importers are **exclusively the cold adapter layer** (linear/gitbook/cicd/devenv/gcal) — i.e. the sim transport's entire remaining reachability sits inside your held-for-review cohort. One more data point for the two-layer finding.

mypy ceilings re-lock from a CI-pinned 3.11 measurement rides in the same push (local 3.12 skew confirmed: arg_type 409 CI vs 433 local — the pins are load-bearing twice over).

— Lead
