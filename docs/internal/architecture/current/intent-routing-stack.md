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
| 0 | **B3 referent resolution** (Stage 0) | `services/intent_service/classifier.py` (`_resolve_issue_referent`), consulted at the TOP of **both** `classify_multiple` and `classify` — before `detect_multiple_intents`, before the classification cache, before surface 1 | Deterministic (regex detect + owner-scoped `session_activity` ledger read) | ADR-078 D2/OQ-3 (#1394): "change the title" / "add a label to it" after creating an issue THIS session resolves to the ledgered issue and emits `update_issue` directly. **Needs `session_id` as its own kwarg** (2026-07-20 fix: the chat path passes `session_id=` explicitly; it must NEVER ride in `context` — context injects into the LLM prompt and disables the classifier cache). Sits above the cache because referent messages are session-relative (a cross-session cache hit would bypass resolution); sits above `detect_multiple_intents` because that pre-classifier pattern-matches update-verb messages (e.g. "change the title to X" → `update_document_query`) and would otherwise return before B3 runs — the live Scenario-B turn-3 misroute mechanism. N-guards: no referent / fresh topic → falls through untouched; D4 intact (the LLM classifier never sees history). **Explicit-`#N` extension (#1411, 2026-08-09)**: an update-verb + issue-field message that NAMES its issue ("change the title of issue #108 to …") also resolves here (`_detect_explicit_issue_update`) — number bound from the message, repository bound opportunistically from the ledger iff THIS session created that same issue (else the handler slot-fills — and since 2026-08-13 the slot-fill consults the user's DEFAULT repo via `resolve_repo` (the first_contact/#1590 rail) before asking; the "which repo?" refusal fires only when resolution also fails and teaches the routable `set my default repo to owner/name` phrase. Same date, clarify-first (PM ruling, decisions.log ~14:1x): a close-shaped unmapped status value ("status → Done") ASKS "By 'Done' do you mean close issue #N?" via the #1190 `pending_action` carrier (kind `unmapped_field_value_clarification`); "yes" dispatches `close_issue` through the same confirm path — no silent synonym mapping). Before this, the no-`#` form ("issue 108") was claimed by surface 1's document pattern (`change … to`) and the `#` form fell to the LLM (reachability = corpus). Guards: update verb + issue-field word required; any document noun (doc/readme/spec/…) declines; bare explicit `#N` withOUT the update-field shape still falls through untouched. |
| 1 | **Pre-classifier** | `services/intent_service/pre_classifier.py` | Deterministic (regex/pattern) | Intercepts known shapes BEFORE any LLM call — identity ("who am I?" → `get_identity`), insights (`pull_insights`), stakeholder updates (`write_stakeholder_update`), portfolio (`manage_portfolio`), status (`get_project_status`), standup, etc. Cheap, deterministic, and the reason "the LLM classified X wrong" is often unobservable in production: the LLM never saw the phrase. |
| 2 | **LLM classifier** | `services/intent_service/classifier.py` (`IntentClassifier.classify`) + `llm_classifier.py` | LLM | Emits an `Intent` (category + action + confidence). Its ACTION VOCABULARY is prompt-suggested, not enforced — it can and does emit paraphrase variants (probe evidence: `list_stale_prs`, `analyze_productivity`). |
| 3 | **Action rail** | `services/intent_service/workflow_entries.py` (`register_default_workflows`) → `workflow_dispatcher.get_action_workflows()`; consumed in `services/intent/intent_service.py::process_intent` | Deterministic dict lookup | If `intent.action` is a registered key (canonical or alias), dispatch pre-floor to that handler. 110 keys ≈ 32 handlers + aliases (census D count 2026-07-16; corrected 2026-08-02 by #1433 — the old "~86" sat stale for weeks, F24; +4 keys 2026-08-08, #1521 reminder-list cohort; +4 keys 2026-08-10, #1570 archived-projects list — `list_archived_projects` + 3 aliases, effect=READ, self-contained entry point; +4 keys 2026-08-16, #1624 uploaded-document summarize — `summarize_document` + 3 aliases, effect=READ, outwardness=PRIVATE: the first SYNTHESIS registry canonical, reached LLM-lane via the Phase-4 verb shim's one mapped SUMMARIZE cell (`(SUMMARIZE, "document")`) or classifier.py's bare-`summarize` normalization; the handler calls the SAME `handle_summarize_document` the REST route uses, resolves "the document" via the un-orphaned `FileResolver` (owner-scoped since #1312), answers deterministically-honestly when no upload resolves, and returns None (rail fall-through to the #1187 SYNTHESIS floor path) for issue/commit-shaped requests. Every OTHER summarize source stays floor-by-#1158; the dormant `_handle_summarize` + IntentEnricher + the never-fired summarize template rows were deleted in the same change — forensics: `docs/internal/operations/summarize-intent-forensics-2026-08-15.md`). The alias lists are **mode-4 defense** against variant emissions — necessary, provably insufficient alone (4 stale-PR aliases still missed a live 5th variant). **#1190 destructive-confirmation gate (2026-08-10, PM ruling)**: inside this surface's dispatch branch, an entry whose declared effect derives `needs_confirm` (== `EffectClass.DESTRUCTIVE`; currently the close/reopen pair, 4 alias keys — the first live DESTRUCTIVE entries) does NOT execute on the classified turn — the gate stores the deferred action as a pending offer (the #846 session-scoped store, popped before classification, so #1529 offer-binding ordering holds) and asks one yes/no question. "yes" re-dispatches the ORIGINAL intent via the offer-acceptance seam → `run_confirm_pending_action_workflow` (registered `confirm_pending_action`, action_triggered=False — rail-unreachable); "no"/bare-exit cancels honestly; off-intent abandons (the pop already cancelled). Generic deferred-action carrier documented in `services/intent_service/destructive_confirm.py`; **#1571 drafted-issue binding (2026-08-15) is now the carrier's second consumer** (`services/intent_service/drafted_issue.py`): the #1510 collaborate turn in `_handle_create_issue` ARMS a pending action (kind `drafted_issue`) binding the rendered draft, so "file it (as is)" — including the original incident phrase "file it in owner/repo", repo override honored — IS the confirmation: handled kind-specifically at the pop seam BEFORE generic accept/decline (the #1605 precedent), acceptance delegates to `run_confirm_pending_action_workflow` (original Intent re-dispatched through the create rail; the `destructive_confirmed` marker now also tells the collaborate gate consent-was-given, so no double-ask), success copy derives from the actual tool result, and any non-created outcome RE-ARMS the draft (retry never loses it). Off-intent abandons per the carrier's rules. **#1627 mid-compose prose hold (2026-08-15, round 2)**: while the drafted_issue offer is armed, a PROSE turn that answers the open body question ("What should the body say…?") binds to the draft at this same pop seam — appended to the draft body and `intent.context["description"]` (so it is what actually files), offer re-armed, draft echoed back — BEFORE any classification surface can see it. The live thief was surface 1's greedy #1527 portfolio pattern (`\bdelete\s+…(.+)`) claiming PM's long body answer ("I couldn't find a project called '(a destructive action)…'"); the #1623 mid-interview hold could not cover it because the draft flow is floor-composed prose, not a registered gathering process. NOT a turn lock: file/accept phrases still file, declines/bare exits still drop the draft honestly, and anchored-imperative asks (the shared collaborate-gate execute check plus a close/read/destructive verb supplement) still route normally, abandoning the draft; long or multi-line turns read as prose regardless of how they open (`is_body_prose_answer` in `drafted_issue.py` — discrimination limits stated in its docstring; regression: `tests/unit/services/intent_service/test_drafted_issue_body_steal_1627.py`). **#1630 subjectless arm (2026-08-15, round 3 — the unarmed face)**: "help me write a ticket" with NO extractable subject used to arm nothing (no subject = no draft), so the answer to "What's it about?" was a bare prose turn for the same greedy chain — the #1627 theft, one turn earlier. The collaborate turn now arms a minimal SUBJECTLESS `drafted_issue` carrier at the ask; the FIRST bound prose names the draft (`derive_subject_from_prose` → draft title, mirrored into `intent.context["title"]` so the create rail files it — the subjectless original message slot-fills nothing) and seeds the body per the same append semantics. Same discriminator, same seam, same exits; the subjectless ask copy still teaches no file phrase until the draft has content (regression: `test_drafted_issue_subjectless_1630.py`). Instruction-shaped draft refinement ("make the title snappier") remains deliberately not built (an anchored-imperative refinement turn abandons the binding; carrying an evolving floor-composed draft under interpreted edits needs a durable store — Inversion Phase 2 is the durable fix). Companion renderer guard: `strip_placeholder_slots` (conversational_floor.py) makes the `#[issue number]` template-slot class structurally unrenderable (replaced with deterministic no-tool-result honesty) — the literal PM saw live exists nowhere in prompts/copy; the model improvised it, so the kill is renderer-side like `strip_scaffolding_artifacts`. Orthogonal to the #1510 collaborate-gate (execute-mode users still confirm destructive actions). +3 offer-only registry keys (`confirm_pending_action` #1190; `verify_inference` #1510 read-back acceptance; `standup_interview` #1591 invitation acceptance) → NOT in the 110 action-rail count; all `action_triggered=False`, reachable ONLY via the offer-acceptance seam. **#1591 standup preference capture (2026-08-13)** is surface-internal to the standup handler, NOT a routing change: an explicit report token (`\breport\b|\bquick\b`) mirrors the #1511 interview token inside the already-claiming handler; a stored verified `standup_mode` (the #1510 rail's store) redirects the generic ask without re-inference; the post-report invitation / low-confidence read-back binds via the same #846 pending-offer store (popped before classification, so the #1529 ordering holds). **Declaration path added later the same day (PM live PARTIAL verdict)**: a standup-token DECLARATION turn ("use the standup interview format by default from now on", `standup_preferences.detect_standup_mode_declaration` — durativity composed from `collaboration_gate.has_durative_marker` + a `back to` switch-back marker) is checked FIRST inside the handler and stores the mode directly (`source=user_declared`, confidence 1.0 — store + confirmation copy, never a read-back); the taught switch-back phrase `back to my standup report` rides the `_is_standup_query` "my standup" cue so it routes AND re-declares deterministically. ⚠️ Reachability of the bare-'standup' declaration form is still LLM-lane (no deterministic surface claims bare "standup" — #1595 corpus material), and the tokenless "use the interview from now on" is a corpus row, deliberately unclaimed. |
| 4 | **Category handlers + floor-internal action checks** | category routing in `intent_service.py`; `conversational_floor.py`, `context_assembler.py` | Mixed | Anything not action-railed routes by `intent.category` (TEMPORAL/STATUS/PRIORITY/IDENTITY/…). Several of these check `intent.action` BY NAME internally (e.g. `pull_insights` in `conversational_floor.py`, MEMORY handling in `context_assembler.py`) — this is the **fourth vocabulary**: real dispatch that no rail listing shows. Bottom: the unhandled-LLM floor (improvised response) — the place #1283 exists to keep phrases OUT of. **Since #1570 (2026-08-10) BOTH floor doors gather domain context**: `_handle_floor_with_context` always did; `_handle_unknown_intent` (the generic-QUERY / offer-fallback / ANALYSIS-etc fall-through door) previously floored with `domain_context=None` — a data query landing there ("what todos are pending?" as an unrailed QUERY emission) saw zero user data while the store had rows. It now runs `ContextAssembler.gather_context` (caller-curated context, e.g. #1187 summarize, is preserved and skips the gather). Floor output is also scrubbed renderer-side: `strip_scaffolding_artifacts` (conversational_floor.py) makes the prompt's own bracketed scaffolding headers (`[Available context…]`, `[Context: …]`, `[Reference binding: …]`, `[Redirect context: …]`) structurally unrenderable in user copy — #1393's prompt-side prohibition alone did not hold (PM live 2026-08-10). A new scaffolding block added to the prompt builders must join `_SCAFFOLDING_BLOCK_RE` in the same commit. **#1536 FTUX-COLDSTART (2026-08-10)**: on the FIRST exchange of a conversation (no completed turn yet — per-conversation, judged from the #1122 in-flight-turn semantics) with a configured connector (#1547 `IntegrationStatusService`, binding-first), `gather_context` additionally runs the first-contact rail (`services/intent_service/first_contact.py`, rides outside the category dispatch like the #1566 reminder rail): a small recency-ranked slice of the user's real GitHub data (repo via the #1042/#1327 default-repo rail; no resolvable repo → NO demo and NO "which repo?" question) lands as `first_contact_demo` / `first_contact_source_failed`, which the floor renders as an open-with-their-data demonstration directive (entities confined to the gathered payload). The canonical CONVERSATION pure-greeting path (which never touches the assembler) appends the same payload via the DETERMINISTIC `render_first_contact_block` in `ConversationHandler._respond_to_greeting`. |

**#1510 collaborate-first additions (2026-08-09), two deterministic checks that sit
around the chain rather than in it** (`services/intent_service/collaboration_gate.py`):
(a) a **working-mode declaration surface** at the very top of
`_process_intent_internal` — an explicit standing declaration ("just do things
directly from now on" / "ask me first from now on", durative marker required) is a
meta-instruction, caught before any surface and persisted per-user to the
`users.preferences` JSONB (`working_mode`: collaborate default / execute); and (b) a
**collaborate-first gate at the top of `_handle_create_issue`** — compose-phrased
requests ("help me write a ticket about X", the Jake shape) always draft-and-ask,
explicit imperatives always execute, and AMBIGUOUS framing is decided by the declared
mode (collaborate unless the user established execute). Background: the classifier
prompt has NO compose-side action name for issue writes, so compose and execute
phrasings collapse into `create_ticket`/`create_issue` at surface 2 — the classifier
half is corpus material (routing moratorium); the gate is the action-layer half.

**#1617 completion-tail release (2026-08-13), at the guided-process seam that
sits ABOVE this whole chain** (`ProcessRegistry.check_active_processes`, run
before classification): a guided flow in a post-delivery tail state
(standup REFINING/FINALIZING) no longer claims off-tail turns. The final
confirmation now COMPLETES the flow directly (no FINALIZING tail turn), and
the #1529 escape module's off_intent tier — tail-only — DELEGATES to the
Stage-0 `_detect_explicit_issue_update` detector, releasing the flow
(terminal COMPLETE, duck-typed `release()` on the adapter) so the turn falls
through to this chain with an honest release prefix. This generalizes the
property that let PM's mode-flip declaration escape the same tail live: the
working-mode declaration surface (below) runs above the process claim.
Related fix, same commit: the #899 off-topic/release prefix used to be
silently dropped by every early handler return — it now rides
`_apply_soft_offer` (the 12-site funnel).

**#1623 mid-gathering hold (2026-08-15), the same seam's inverse guarantee**:
an ACTIVE gathering flow HOLDS its turns. The thief was never a surface in
this chain — measured, every content-dependent surface at/above the process
claim passes PM's stolen answers — it was `StandupProcessAdapter.check_active`'s
LAZY #888 15-minute timeout: with no background reaper it fires inside the
NEXT turn's processing, which mid-gathering is by construction the answer to
the open question, so >15 min of think-time silently auto-suspended the flow
and dropped the answer to the LLM classifier (files-family denial ate PM's
plans answer; the temporal surface ate the blocker answer). The timeout
auto-suspend is now gated to the completion tail (REFINING/FINALIZING);
mid-gathering the flow holds regardless of think-time, and the deliberate
exits remain the #888/#1529 escape tiers, #899 off-topic, and the #1510
mode-declaration surface (which escapes the turn without touching the flow).
Regression: `tests/unit/services/process/test_midgather_hold_1623.py` (PM's
two verbatim turns e2e, stale-clock, explosive LLM).

**#1509 unified consent gate (2026-08-13)** — `services/intent_service/consent_gate.py`
generalizes #1190 + #1510 into ONE decision (`decide_consent(effect, framing, mode)`;
the named boundary condition lives in that module's docstring, per #1509 AC-1). At the
surface-3 dispatch branch, every `needs_consent` entry (declared `effect >= WRITE`,
the Arch derivation) is evaluated BEFORE dispatch: **DESTRUCTIVE → CONFIRM** in every
cell (the #1190 yes/no gate, behavior unchanged — the verdict just has one home);
**WRITE + compose framing → COLLABORATE**; **WRITE + explicit imperative → PROCEED**
(the imperative IS the consent); **WRITE + ambiguous → the declared working mode
decides**; **READ → PROCEED always**. A held WRITE turn renders one of two copy
surfaces (copy selection, not a second gate): the create family falls through to
`_handle_create_issue`'s #1510 draft-collaboration copy (its `gate_holds` now
DELEGATES to the same `decide_consent`, with effect looked up from the registry — the
swap the old `GATED_WRITE_ACTIONS` comment tracked; the set survives as
`DRAFT_COLLABORATION_ACTIONS`, copy-surface selection only); every other held WRITE
action gets the generic consent check — a #1190-carrier pending offer
(`confirm_pending_action`, "kind": "consent_check") whose "yes" re-dispatches the
ORIGINAL intent, "no"/bare-exit cancels honestly, off-intent abandons via the pop.
The check copy states the action + its declared effect tier
(`capability_legibility.describe_effect`, registry-derived) — the gate's own prompt is
a capability-legibility surface (`capability_legibility.py` holds the full derivation
chain: registry effect → `decide_consent` → behavior lines; `chat_pointers` POINTER
rows → example asks; `capability_catalog()` is the #1462 tool-description seam).
Framing generalized in the same commit: the anchored execute-imperative check runs
FIRST and carries the update/comment/reminder/preference verb families, so every
deterministic-surface phrasing (#1411/B3/#1560/#1327) stays an un-checked imperative.
⚠️ Known boundary: legacy `_handle_execution_intent` chain actions (todo family) have
no declared effect and are OUTSIDE this gate — their consent rides their rail
migration (still pending; #1605 shipped handler-internal, below, without moving the
todo family onto the rail); `capability_legibility.catalog_coverage()` states the
denominator.

**#1605 reminder-clear verb disambiguation (2026-08-14, CXO/PPM jointly-signed-off
design)** — surface-internal to the EXECUTION lane, NOT a routing change (routing
moratorium honored; no pre-classifier or prompt-pattern additions).
`services/intent_service/reminder_clear.py`: a clear-family verb (clear / handle /
take care of / reset) over the reminder/todo domain, with NO explicit
complete/delete verb, is detected from the ORIGINAL MESSAGE inside the three
already-claiming EXECUTION surfaces — the legacy `complete_todo` and `delete_todo`
elif branches (the classifier's guess for the ambiguous utterance; candidate effect
WRITE / DESTRUCTIVE respectively) and the #1333 unmapped else-branch (unmapped
sibling emissions like `clear_reminders`, candidate effect DESTRUCTIVE — previously
a FALSE capability denial, the #1605 transcript bug). The mechanism consumed is
`consent_gate.decide_verb_interpretation` (effect-weighted #1510 read-back) + the
#1510 verified-inference store (per-verb keys `reminder_clear_verb:{verb}`) + the
#1190 `pending_action` carrier. Three ratified copy variants (pinned verbatim in
`test_reminder_clear_verb_1605.py`): first-encounter ask (answer binds at the
offer seam — kind `reminder_clear_verb_question`, handled kind-specifically BEFORE
generic accept/decline, the verify_inference precedent); stored complete →
auto-apply + disclosure-after with a ONE-TURN correction window (kind
`reminder_clear_correction`, "I meant delete" → #1190-gated delete of the
just-completed batch, stored default unchanged); stored delete → the REAL #1190
confirm (`confirm_pending_action` → `clear_reminders_delete`) — a stored verb
preference changes the MAPPING, never the consent tier, and a DESTRUCTIVE
candidate reads back even under `trust_inferences` (pinned cell). An exception
clause ("except …") is #1563's set-complement lane: variant-1-style clarification
of the whole ask, nothing bound, nothing touched. Three new offer-only registry
keys (`clarify_reminder_clear_verb` READ, `reminder_clear_correction` READ,
`clear_reminders_delete` DESTRUCTIVE — all `action_triggered=False`, so the
surface-3 destructive rail-scope denominator is unchanged). `_apply_soft_offer`
now refuses to clobber a just-armed pending action (guarded on the
`*_pending` intent_data flags — the one-slot #846 store is shared with soft
offers). **#1569 render half** (same commit): the floor's
`_format_domain_context` renders the two context families as visually distinct
sections with per-origin vocabulary instructions — `due_reminders` (from
`context:reminders:{user_id}`) says "reminder", `pending_todos` (from
`context:pending_todos:{user_id}`) gets a `PENDING TODOS (N)` section header and
says "todo"; mixed-origin turns instruct todo-list-first + a separate
"Also due:" reminder block, an item in both origins appearing in the reminder
block only. No new store, no schema change, no per-item data field.

**#1595 Phase 1 inversion shadow observer (2026-08-14) — an explicitly
NON-dispatching fifth party that watches the chain, never joins it.** When
`PIPER_INVERSION_SHADOW` is on (default OFF), `process_intent` fires-and-forgets
one async task AFTER the turn completes
(`services/intent_service/inversion_shadow.maybe_schedule_shadow_check`): the
same utterance goes through the CONSTRAINED inversion routing call
(`services/intent_service/inversion_router.route` — one Haiku-class LLM call,
task type `inversion_routing`, output validated against a grammar of canonical
operations DERIVED FROM THE REGISTRY AT CALL TIME: rail entries collapsed by
shared-entry alias identity + `ACTION_REGISTRY`-only canonicals + NONE/CLARIFY,
with catalog descriptions from registry metadata — rail `entry.description`
for rail operations, `ACTION_DESCRIPTIONS` in `action_registry.py` for
registry-only canonicals (Phase 1b Family-1 enrichment, metadata-only: nothing
dispatches on it), honest disposition fallback when an entry has none;
strict JSON + one repair retry + honest REFUSED, never a guessed route), and a
structured line (`shadow_route_agreement` / `shadow_route_disagreement`,
registry-alias-aware comparison against the #1518 production label) becomes
corpus telemetry. **Nothing dispatches from it**: the decision type is
un-importable from dispatch code by construction —
`tests/test_architecture_enforcement.py::TestInversionShadowNoExecutionBoundary`
enforces that only `inversion_shadow.py` may reference the router, and that
`intent_service.py` sees only the fire-and-forget scheduler. This is Arch's
"falsifiable CONTINUOUSLY" property (decisions.log 2026-08-09 09:0x): surfaces
0–4 above answer the user; the shadow line records what the constrained LLM
router WOULD have done. Zero latency cost (post-turn task), sampled
(`PIPER_INVERSION_SHADOW_SAMPLE`), shadow failure logged and swallowed.
Corpus-side instrument: `scripts/inversion_phase1_shadow_score.py` scores the
router against `tests/fixtures/inversion_corpus_phase0.yaml` per category vs
the Phase-0 full-chain baseline (first run:
`inversion-phase1-shadow-score-2026-08-14.md`). The Phase-2 flip (per-category,
queries first) is the reviewed commit that relaxes the boundary test — until
then this observer changes NO routing behavior.

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
`tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet`. The ledger
itself lives in `services/intent_service/chat_pointers.py` (moved 2026-08-03, #1428) —
a single source imported by BOTH the ratchet and the product's "what can you do?" answer
path (`context_assembler._gather_identity_context` derives the DISCOVERY/IDENTITY
capability list from the ledger's POINTER rows via `capability_answer_lines()`, replacing
the rail-descriptions-only build that understated capabilities and leaked internal
markers like "(#1124)" — census F8). The ratchet derives
the product-surface set (ui.py page routes + connectable integrations + decline-copy
capabilities) at collection time, requires a ledger row per surface (a POINTER utterance
that resolves DETERMINISTICALLY through this stack's surfaces 1/3/4 with the resolution
path asserted, or a structured-citation CHAT_INVISIBLE under a shrink-only ceiling in
`scripts/ratchet_ceilings.json`), and enforces decline-copy freshness
(`UNWIRED_WRITE_DECLINES` + `_get_contextual_fallback` denials must stay disjoint from
the reachable-action set). It also supersedes `validate_registry_coverage()`'s circular
example-driven check as the census F24 accounting fix. The ledger additionally carries
**`pin:` rows** (#1521, 2026-08-08): regression pins for once-misrouted natural phrasings
whose capability has no page/integration surface to ride (#1471's calendar fix could reuse
existing surface rows; "what reminders do I have?" — misrouted to the temporal lane by the
LLM classifier until the pre-classifier claimed it — could not). A `pin:` row is exempt
from surface derivation ONLY; it must be a POINTER and is resolution-tested forever like
any surface row (first instance: `pin:reminder-query` → QUERY/`list_reminders_query`).

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
