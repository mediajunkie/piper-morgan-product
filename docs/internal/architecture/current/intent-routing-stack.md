# The Intent Routing Stack — read this BEFORE touching LLM responses or intent handling

**Why this doc exists**: on 2026-07-08 the #1283 behavioral probe produced 12 apparent
routing failures, of which **7 were the investigator not knowing this stack existed** —
the probe measured one layer and mistook the other layers' work for breakage. The
static audit that preceded it modeled three vocabularies and missed a fourth. This doc
is the map that had to be rediscovered; the consult rule (CLAUDE.md Progressive Loading
table) exists so nobody re-derives it a third time.

**Consult rule**: working on ANY of — intent classification, action handlers, chat
response behavior, the dispatch rail, prompt vocabulary, routing tests — read this doc
first. If your change makes it stale, update it in the same commit (agent-who-notices
rule applies).

## The chain (in execution order)

A user message traverses up to FOUR dispatch surfaces (plus a Stage-0 resolver in
front of them); earlier surfaces win:

| # | Surface | Where | Nature | What it does |
|---|---------|-------|--------|--------------|
| 0 | **B3 referent resolution** (Stage 0) | `services/intent_service/classifier.py` (`_resolve_issue_referent`), consulted at the TOP of **both** `classify_multiple` and `classify` — before `detect_multiple_intents`, before the classification cache, before surface 1 | Deterministic (regex detect + owner-scoped `session_activity` ledger read) | ADR-078 D2/OQ-3 (#1394): "change the title" / "add a label to it" after creating an issue THIS session resolves to the ledgered issue and emits `update_issue` directly. **Needs `session_id` as its own kwarg** (2026-07-20 fix: the chat path passes `session_id=` explicitly; it must NEVER ride in `context` — context injects into the LLM prompt and disables the classifier cache). Sits above the cache because referent messages are session-relative (a cross-session cache hit would bypass resolution); sits above `detect_multiple_intents` because that pre-classifier pattern-matches update-verb messages (e.g. "change the title to X" → `update_document_query`) and would otherwise return before B3 runs — the live Scenario-B turn-3 misroute mechanism. N-guards: no referent / fresh topic / explicit `#N` → falls through untouched; D4 intact (the LLM classifier never sees history). |
| 1 | **Pre-classifier** | `services/intent_service/pre_classifier.py` | Deterministic (regex/pattern) | Intercepts known shapes BEFORE any LLM call — identity ("who am I?" → `get_identity`), insights (`pull_insights`), stakeholder updates (`write_stakeholder_update`), portfolio (`manage_portfolio`), status (`get_project_status`), standup, etc. Cheap, deterministic, and the reason "the LLM classified X wrong" is often unobservable in production: the LLM never saw the phrase. |
| 2 | **LLM classifier** | `services/intent_service/classifier.py` (`IntentClassifier.classify`) + `llm_classifier.py` | LLM | Emits an `Intent` (category + action + confidence). Its ACTION VOCABULARY is prompt-suggested, not enforced — it can and does emit paraphrase variants (probe evidence: `list_stale_prs`, `analyze_productivity`). |
| 3 | **Action rail** | `services/intent_service/workflow_entries.py` (`register_default_workflows`) → `workflow_dispatcher.get_action_workflows()`; consumed in `services/intent/intent_service.py::process_intent` | Deterministic dict lookup | If `intent.action` is a registered key (canonical or alias), dispatch pre-floor to that handler. 102 keys ≈ 30 handlers + aliases (census D count, 2026-07-16; corrected here 2026-08-02 by #1433 — the old "~86" sat stale for weeks, F24). The alias lists are **mode-4 defense** against variant emissions — necessary, provably insufficient alone (4 stale-PR aliases still missed a live 5th variant). |
| 4 | **Category handlers + floor-internal action checks** | category routing in `intent_service.py`; `conversational_floor.py`, `context_assembler.py` | Mixed | Anything not action-railed routes by `intent.category` (TEMPORAL/STATUS/PRIORITY/IDENTITY/…). Several of these check `intent.action` BY NAME internally (e.g. `pull_insights` in `conversational_floor.py`, MEMORY handling in `context_assembler.py`) — this is the **fourth vocabulary**: real dispatch that no rail listing shows. Bottom: the unhandled-LLM floor (improvised response) — the place #1283 exists to keep phrases OUT of. |

## The vocabularies (where action names live)

1. **Prompt vocabulary** — action names the classifier prompt suggests (`services/prompts.py`, ~17).
2. **`ACTION_REGISTRY`** — `services/intent_service/action_registry.py`, the documented
   canonical (category, action) pairs (~43). SSOT-in-waiting (#1283 AC-4, Arch).
3. **Rail keys** — `workflow_entries.py` registrations (102 incl. aliases, 2026-08-02).
4. **Floor/pre-classifier names** — action strings matched inside surface-1 and surface-4
   code. Not statically enumerable; the accounting lives in
   `tests/unit/services/intent_service/test_routing_vocabulary_1283.py::KNOWN_OFF_RAIL`.

**Enforcement**: that same test is the no-LLM ratchet — every registry canonical must be
rail-registered or explicitly ledgered as off-rail-but-surface-handled; the ledger only
shrinks; corpus expectations must name known actions. The LLM half (behavioral corpus,
`tests/fixtures/routing_corpus_1283.yaml` + `scripts/routing_probe_1283.py`) runs
out-of-CI on cost grounds, gated on Arch ratification.

**Product-inward enforcement (#1433, 2026-08-02)**: the registry-outward lint's missing
half is the CHAT_POINTERS reachability ratchet —
`tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet`. It derives
the product-surface set (ui.py page routes + connectable integrations + decline-copy
capabilities) at collection time, requires a ledger row per surface (a POINTER utterance
that resolves DETERMINISTICALLY through this stack's surfaces 1/3/4 with the resolution
path asserted, or a structured-citation CHAT_INVISIBLE under a shrink-only ceiling in
`scripts/ratchet_ceilings.json`), and enforces decline-copy freshness
(`UNWIRED_WRITE_DECLINES` + `_get_contextual_fallback` denials must stay disjoint from
the reachable-action set). It also supersedes `validate_registry_coverage()`'s circular
example-driven check as the census F24 accounting fix.

## Failure modes (the #1283 taxonomy, probe-confirmed)

- **Mode 1** — prompt suggests a name nothing dispatches → floor improvisation.
- **Mode 2** — registry documents a canonical no surface dispatches (`productivity_query`
  was, until 2026-07-08 — its own handler's alias list omitted it).
- **Mode 3** — handler exists but classifier never emits its name (dead registration —
  OR mode-4 defense; check before pruning).
- **Mode 4** — LLM emits a paraphrase variant that misses every alias
  (`list_stale_prs` past 4 aliases, live). Countermeasures: aliases (necessary),
  prompt-vocabulary constraint + near-miss normalization + CI accounting (the AC-4
  SSOT design, with Arch as of 2026-07-08).

## Probe/test seam rules (learned the expensive way)

- A **classifier-only probe undercounts correctness**: surface 1 intercepts before the
  LLM ("give me my standup" routes perfectly; the classifier alone says otherwise).
- A **rail-membership check undercounts handledness**: surface 4 dispatches by name
  outside the rail (`pull_insights` et al.).
- Verdicts about "routing" must model the whole chain or say explicitly which layer
  they measured.

## Pointers

- Probe report + recalibration trace: `dev/2026/07/08/routing-probe-1283-run1.md`
- Dispatch-site ratchet (the no-new-elif rule): `tests/test_architecture_enforcement.py::TestPreFloorDispatchSiteRatchet` + CLAUDE.md §"Intent dispatch"
- Migration roadmap off the legacy chains: `docs/internal/architecture/current/pre-floor-handler-migration-roadmap-1124.md`
