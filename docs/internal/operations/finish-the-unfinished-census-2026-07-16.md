# Finish-the-Unfinished Census — Frozen Inventory (2026-07-16)

**Sprint**: epic #1424 · plan `docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md`
**Status**: Censuses A (silent-death), C (stubs/TODO), D (reachability) COMPLETE; B (signature drift / mypy) landing — appended on completion. Ceilings frozen + ratchets live on main (`scripts/ratchet_ceilings.json`, `tests/test_completion_ratchets.py`): silent_death_core=254 · unscoped_reads=64 · notimplementederror=9 · todo_markers=78.
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

## Census B — signature drift (mypy) — PENDING, appended on completion

---

## Ratchet state (live on main)
- `tests/test_completion_ratchets.py` (smoke-marked, growth fails build, shrinkage forces same-commit ceiling lock-in)
- `scripts/check_silent_death.py` (#1423) · `scripts/check_unscoped_reads.py` (#1419) — warn-mode rich output; counts CI-gated
- Ceilings: silent_death_core **254** · unscoped_reads **64** · notimplementederror **9** · todo_markers **78**
- Pending Arch ratification (memo sent 2026-07-16 ~14:15): lint designs CI-blocking flip; extended reachability ratchet (census D §6); mypy gate (census B rec, when it lands)
