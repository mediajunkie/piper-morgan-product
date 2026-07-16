# Finish-the-Unfinished Census — Frozen Inventory (2026-07-16)

**Sprint**: epic #1424 · plan `docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md`
**Status**: **ALL FOUR CENSUSES COMPLETE — BACKLOG FROZEN 2026-07-16 ~15:20 PT.** Ceilings frozen + ratchets live on main (`scripts/ratchet_ceilings.json`, `tests/test_completion_ratchets.py`): silent_death_core=254 · unscoped_reads=64 · notimplementederror=9 · todo_markers=78. Proposed mypy per-code ceilings (Census B, pending gate build): call-arg=94 · arg-type=437 · attr-defined=308 · union-attr=221.
**Rule reminder**: this list is the sprint scope, FROZEN. Anything discovered after this doc closes gets filed and tagged for the next census — not chased.

---

## THE FROZEN FIX LIST (ranked, cross-census)

### P0 — trust-boundary / affirmative-false-output (fix first in Phase 2)

| # | Finding | Source | Where | Issue |
|---|---|---|---|---|
| F1 | **Provider-consent filter fails OPEN**: any keychain error reading `authorized_llm_providers` → falls through to ALL configured providers; user messages can route to providers they explicitly de-authorized (#946 control silently disabled). WARN log only. | A | `services/config/llm_config_service.py:189` | fold into #1415 (same subsystem rewrite) |
| F2 | **Affirmative-false-claims family** (5 handlers, one fix pattern — formatter must distinguish "source failed" from "source empty"): priority query claims "No P0/P1 issues found" on GitHub error (DEBUG log!); status report claims 0 open todos on DB error; agenda claims "No pending tasks"; retrospective claims "No completed tasks — keep up the momentum!"; promised reminders never fire (double-swallowed at two layers). | A | `canonical_handlers.py:1606, 2973, 2344, 2641` + `todo_handlers.py:116`/`context_assembler.py:968` | **#1425** |
| F3 | **Personality prefs dead product-wide** (#262 never migrated the column; every user gets hardcoded defaults). | A (cal.) | `personality_profile.py:234` | **#1422** (filed) |

### P1 — false denials + the mocked REST surface (user-facing lies, both directions)

| # | Finding | Source | Where | Issue |
|---|---|---|---|---|
| F4 | **"connect my github/slack" unreachable**: three real capabilities exist (OAuth flow, settings page, a purpose-built chat guidance answer `_format_integration_setup_guidance`) — the natural utterance reaches none; generic "still on the way" decline misdirects to "the relevant tool (e.g. GitHub)". Probe-verified 4-surface drop mechanism documented in Census D §5. | D (cal.) | `pre_classifier.py:893-906` (no connect pattern), `unwired_writes.py:93`, `canonical_handlers.py:1978` (GUIDANCE-only gate) | **#1417** (filed; mechanism now precise) |
| F5 | **File-upload FALSE DENIAL**: bespoke copy "I can't accept file uploads yet…" while `/files` page + `POST /api/v1/files/upload` + preview/download/tags are fully shipped. Worse than the generic decline — a stale hand-written lie. | D | `intent_service.py:6812` vs `web/api/routes/files.py`, `ui.py:428` | **#1426** |
| F6 | **Reminder FALSE DENIAL** on mapper-missed phrasings: "I can't set reminders yet" while `create_reminder` shipped (#903). | D | `intent_service.py:6755` | **#1426** (folded with F5) |
| F7 | **`/api/v1/todos` REST surface is mocked**: GET-by-id always 404 ("Mock response for now"); list CRUD/membership/search return fabricated data with random UUIDs, persisting nothing; hardcoded `user_id="default-user"`. Mounted live at `web/app.py:255`. (Chat todo flow is separate and real.) | C | `services/api/todo_management.py` (37 TODO lines) | **#1427** (finish-or-unmount decision inside) |
| F8 | **"What can you do?" systematically understates**: capabilities list built solely from rail entry descriptions — omits canonical handlers, EXECUTION-elif capabilities, floor capabilities, every web flow; leaks internal markers ("(#1124)") into the floor prompt. | D | `context_assembler.py:370-385` | **#1428** |

### P2 — silent feature-death clusters (Census A's 57 MED, fix-shaped)

| # | Cluster (fix as a unit) | Where |
|---|---|---|
| F9 | Context-assembler core-work sources (9 handlers): floor answers "what should I work on" without real todos/projects/issues — the file's own comment warns zero context makes the LLM "invent data" | `context_assembler.py:326,691,1021,1066,1112,1152,1235,1336,1442` |
| F10 | Answer-section sources (10): changes/attention/productivity queries silently underreport | `intent_service.py:5803-6308` family, `:11310`, `:1095` |
| F11 | Guidance context — silent `pass`, ZERO logging (worst hygiene in census) | `intent_service.py:11908,11916,11928,11945` |
| F12 | Conversational state-machine checks (5): mid-flow "yes"/slot answers re-classified as fresh intents on persistent bug — conversation-breaking | `intent_service.py:1785,1841,1933,2247,2314` |
| F13 | Learning + preference-detection loop (10): Piper permanently stops learning, ERROR logs only | `intent_service.py` + `intent_hooks.py` + `classifier.py` per census |
| F14 | Todo KG side-writes (4; incl. a `print()` instead of logger): KG starves, #1420's family | `todo_knowledge_service.py:89,237,290`, `todo_management_service.py:148` |
| F15 | Onboarding persistence (2): user told setup worked; nothing persisted | `intent_service.py:2463,2466` |
| F16 | Status/priority/calendar metadata (5): #1231 honest-degrade copy silently bypassed when the check throws | `canonical_handlers.py:1504,1541,1610,1344,1410` |
| F17 | Identity capabilities, soft-offer/persona, rail-dispatch fall-through, similarity internals, doc-anchor write (8) | per census A tables |

### P2 — remaining stubs/gaps (Census C/D)

| # | Finding | Where |
|---|---|---|
| F18 | Slack `/standup` renders empty Yesterday/Today always (data sources return `[]`) | `webhook_router.py:1449,1459` |
| F19 | Learning dashboard phantom user (`USER_ID='current_user'` in 8 fetches; routes take raw user_id unauthenticated) | `learning-dashboard.html:610` + `learning.py:571,604,638` |
| F20 | Latent: `list_archived_projects()` mathematically always `[]` (filters an active-only source) — bites the moment anyone wires "show archived projects" | `portfolio_service.py:153,415` |
| F21 | api-keys / lists / work-items chat-unreachable (product objects with zero chat vocabulary; decline misdirects) — DISPOSITION NEEDED: chat-invisible by design (ledger) or wire pointers | D table §2 rows 3–4 |
| F22 | Half-landed #1124 Phase-4 prompt flip: verb prompt + shim shipped, primary chat path never flipped; `llm_classifier_factory.py` imported by no production code | `llm_classifier.py:359-408` vs `classifier.py:1587` / `prompts.py` |
| F23 | `home_state_service._generate_briefing_summary` commented out → Stage-3 home briefing never appears; workflow-offer session cap can never trip (`suggestions_count=0` TODO) | `home_state_service.py:343`; `intent_service.py:299` |
| F24 | Registry-contract accounting holes: 5 pre-classifier actions absent from ACTION_REGISTRY (its "MUST" docstring is false); `validate_registry_coverage()` is circular; routing-stack doc rail-count stale (~86 → 102) | `action_registry.py`, `intent-routing-stack.md` |

**Census B issues (2026-07-16 ~15:30)**: B1→#1434 · B3→#1435 · B-umbrella + mypy gate→#1436 · B6→#1422(comment, 3-services scope) · B1/B16→#1419(comment).

**Issues filed off this table (2026-07-16 ~15:00)**: F1→#1415(comment) · F2→#1425 · F3=#1422 · F4=#1417(comment, mechanism) · F5/F6→#1426 · F7→#1427 · F8→#1428 · F9–F17→#1423(comment, clusters) · F18→#1429 · F19→#1430 · F20→#1431 · F21→disposition pending (PM/Arch, via #1433 ledger) · F22→#1432 · F24→folded into #1433 · extended ratchet→#1433.

### Cleared / by-design (do not touch; seeds allowlists)
Census A: 85 LEGIT + 123 NARROW (clusters in census record). Census C: 7 documented-legit NIE (abstract-method idiom, #1342 resolver guard, #1220 provisioning gate, key-rotation stub — module itself orphaned), honest Coming-Soon pages, fail-safe migration blocker, #692/#932 ratified behaviors; 12 internal-only dead/POC placeholders (notion_queries, recovery_strategies fabrications — dangerous if ever wired, POC MCP server mocks, token_blacklist.revoke_user_tokens no-op — security-relevant if relied on). Census D: #1333 decline set KNOWN-BY-DESIGN; 79 rail alias keys intentional; accurate-decline copy list (Slack post, calendar events, documents, batch-create).

---

## Census A — silent-death handlers (full record: task output 2026-07-16)
274 real handlers classified (275 grep hits − 1 docstring FP): **85 LEGIT · 123 NARROW · 66 UNSWALLOW (9 HIGH + 57 MED) · 0 UNKNOWN**. Calibration #1420 + #1422 both found. Cross-cutting: worst offenders log at DEBUG or not at all; the affirmative-false family (F2) shares one fix pattern; `workflow_dispatcher.py:148` flagged for sprint discussion (deliberate rail fall-through vs. mode-4 masking).

## Census C — stubs/TODOs (full record: task output 2026-07-16)
9 NIE raise sites (0 user-reachable · 2 internal-only · 7 documented-legit); 6 user-reachable placeholder findings (F7, F18, F19, F23, CSV-export-honest, F20 latent); TODO decomposition: 22 false positives (identifiers/format strings — excluded from ratchet semantics), 41 lines/4 findings bucket-(a), 6 bucket-(b), 2 stale. UNKNOWNs listed in record (MCPResourceManager consumption, UniversalList migration state, github_adapter spatial placeholders, `/api/v1/todos` external callers).

## Census D — reachability (full record: task output 2026-07-16)
Matrix: 46 registry pairs · 102 rail keys (~30 handlers) · 31 pre-classifier actions · classifier free-form. registry−(rail∪preclf∪floor)=∅ (#1283 holds; zero mode-2 gaps). Direction-1 gaps = F4, F5-adjacent upload, api-keys, lists/work-items, stakeholder-update fragility, reminder variants. Direction-2: #1333 set confirmed by-design; NEW = F22 half-landed prompt flip, Verb.COMPOSE unruled (cosmetic), F24 accounting holes. Direction-3 copy audit: 2 false denials + 1 misdirect + 1 systematic understatement; 5 decline strings verified accurate. **Extended-ratchet design** (CHAT_POINTERS product-surface ledger + decline-copy freshness ratchet) recorded in census D §6 — Phase 1.5 build, Arch-ratified alongside the lints.

## Census B — signature drift (mypy 2.3.0, one-shot) — COMPLETE

**Run**: scratch venv (shared venv untouched) + typed deps (`sqlalchemy==2.0.23`, `pydantic==2.12.5`, `fastapi==0.115.14`) + plugins (`pydantic.mypy`, `sqlalchemy.ext.mypy.plugin`); `--ignore-missing-imports --check-untyped-defs`, 605 files. **1,862 raw errors → 1,060 in the 4 target codes (call-arg 94 · arg-type 437 · attr-defined 308 · union-attr 221) → 698 deduped → ~30 verified distinct defects/families** after discarding Optional-discipline noise (310), SQLAlchemy/typing artifacts, and runtime-tolerant smells (buckets in task record, condensed here). Both calibration instances flagged (#1420 call-arg ×3; #1422 attr-defined).

**Why mypy was structurally blind until now (the census's meta-finding)**: (1) `session_scope()` at `services/database/session_factory.py:136/182/219` is mis-annotated `-> AsyncContextManager[AsyncSession]` — mypy infers the yield as `Never`, so **every `async with session_scope() as session:` body in the codebase was analyzed as unreachable** (all DB-block errors suppressed); (2) `declarative_base()` without the SQLAlchemy plugin makes every model an `Any` fallback (no attr checking). The authoritative run fixed the 3 annotations in a scratch copy + enabled the plugin. **Prerequisite one-commit fix before the gate lands**: those 3 annotation lines (pure annotation, zero runtime effect).

### Tier 1 — LIVE path, verified by reading each call site (F25–F29 umbrella)

| # | Location | What's wrong | Mask |
|---|---|---|---|
| B1 | `web/api/routes/setup.py:1561` | **Missing `await` on `jwt_service.validate_token()`** — coroutine is truthy, `.sub` raises → auth silently falls back to non-scoped key on every request through this path | `except Exception: pass` |
| B2 | `web/api/dependencies.py:155` | DI yields `KnowledgeGraphService(session)`; `__init__` requires a `KnowledgeGraphRepository` — every KG route call explodes | 500 surface |
| B3 | `services/database/models.py:2164,2759` | `ListDB/TodoDB.from_domain` pass `metadata=`; column is `list_metadata`. SQLAlchemy doesn't raise (`metadata` = class-level MetaData attr) — **list/todo metadata silently never persists** | Silent no-op — worst mask in census |
| B4 | `web/api/routes/learning.py` ×12 | error-helper kwargs (`error_id=`, …) not in signatures — every error branch raises TypeError → 500 instead of clean 422/404 | 500 surface |
| B5 | `web/api/routes/todos.py:316,324,366` | route param `status: str\|None` shadows the `starlette.status` module — every 404/400/500 branch raises AttributeError | 500 surface |
| B6 | `personality_profile.py:229` **+ `user_context_service.py:241,245,247` + `intent_service.py:2453,2456`** | `user.preferences` — #1422 is **3 services wide**, not 1; A's F15 onboarding-persistence swallow likely masks this exact AttributeError | silent defaults |
| B7 | `todo_knowledge_service.py:127`, `llm_classifier.py:240` | #1420 calibration (similarity_search kwargs) | swallowed TypeError |
| B8 | `todo_management_service.py:147` | `create_todo_knowledge_node(saved_todo)` missing required `user_id` → **KG node creation fails on every todo creation** (F14's root) | explicit swallow |
| B9 | `preference_handler.py:427` | `PatternType.PREFERENCE` doesn't exist (enum has `USER_PREFERENCE_PATTERN`) → preference-learning hook dies (F13's root) | `classifier.py:317` swallow |
| B10–B20 | intent paths reading dicts-as-objects (`intent_service.py:11294-11305`) and AuditLog-rows-as-todos (`:5965-6015`); `todo.title` vs `text` (`canonical_handlers.py:2338,2632`); `github_domain_service.py:63,179` positional-shift vs router kwargs; KG routes `owner_id=`+str-vs-enum; `feedback.py:57` missing domain class; **config services missing now-required `user_id`** (`setup.py:1251,1372`, `integrations.py:521`, `production_client.py:110` — #1419-family migration drift); `UploadedFile` model drift in file queries; `AsyncSessionFactory.get_session` (doesn't exist) in conversation context; key-audit + cross-feature enum members missing | various swallows / 500s |

**Tier 2 (flag/config-gated)**: Slack webhook `Intent(raw_input=, classification=)` TypeError (3 sites); structlog-kwargs on stdlib loggers (5 files, 13 sites — `query_router.py:164` is LIVE); Slack spatial adapter call missing required args (`USE_SPATIAL_SLACK` — **spatial is PROTECTED**, prioritize despite the gate); staging-health reads config fields that don't exist (router currently unmounted).
**Tier 3 (COLD but real)**: `PersonalityProfileDB.to_domain()` missing 4 required fields; `notion_spatial.py` calls 12 never-defined methods (75%-complete class); 4 MCP adapters call `initialize()/close()` vs core's `connect()/disconnect()`; trust_integration logger kwargs; key_rotation/publisher/project_context/session_aware_wrappers/file_repository_old/notion_queries/multi_agent drift; graph multi-hop traversal reads attrs off ID-strings; 13 test files calling signatures that no longer exist (cannot pass — presumably never collected).
**Systemic family (1 issue, not 48)**: UUID-vs-str identity drift across user_id/todo_id plumbing (#262 residue) — mostly runtime-tolerated, dict-lookup/equality sites can silently miss.

### CI gate recommendation (B §4)
Viable and worth it: pinned mypy 2.3.0 + the 3 typed deps + both plugins, 4-code filter, **per-code ratchet ceilings 94/437/308/221** (per-code so a fix in one code can't hide regressions in another), few minutes runtime. Prerequisite: the 3-line `session_factory.py` annotation fix — without it the gate is hollow (blind inside every DB block). Minimal no-plugin config (744) rejected: can't see the #1422 class.

---

## Ratchet state (live on main)
- `tests/test_completion_ratchets.py` (smoke-marked, growth fails build, shrinkage forces same-commit ceiling lock-in)
- `scripts/check_silent_death.py` (#1423) · `scripts/check_unscoped_reads.py` (#1419) — warn-mode rich output; counts CI-gated
- Ceilings: silent_death_core **254** · unscoped_reads **64** · notimplementederror **9** · todo_markers **78**
- Pending Arch ratification (memo sent 2026-07-16 ~14:15): lint designs CI-blocking flip; extended reachability ratchet (census D §6); mypy gate (census B rec, when it lands)
