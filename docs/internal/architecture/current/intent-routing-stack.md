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
| 0 | **B3 referent resolution** (Stage 0) | `services/intent_service/classifier.py` (`_resolve_issue_referent`), consulted at the TOP of **both** `classify_multiple` and `classify` — before `detect_multiple_intents`, before the classification cache, before surface 1 | Deterministic (regex detect + owner-scoped `session_activity` ledger read) | ADR-078 D2/OQ-3 (#1394): "change the title" / "add a label to it" after creating an issue THIS session resolves to the ledgered issue and emits `update_issue` directly. **Needs `session_id` as its own kwarg** (2026-07-20 fix: the chat path passes `session_id=` explicitly; it must NEVER ride in `context` — context injects into the LLM prompt and disables the classifier cache). Sits above the cache because referent messages are session-relative (a cross-session cache hit would bypass resolution); sits above `detect_multiple_intents` because that pre-classifier pattern-matches update-verb messages (e.g. "change the title to X" → `update_document_query`) and would otherwise return before B3 runs — the live Scenario-B turn-3 misroute mechanism. N-guards: no referent / fresh topic → falls through untouched; D4 intact (the LLM classifier never sees history). **Explicit-`#N` extension (#1411, 2026-08-09)**: an update-verb + issue-field message that NAMES its issue ("change the title of issue #108 to …") also resolves here (`_detect_explicit_issue_update`) — number bound from the message, repository bound opportunistically from the ledger iff THIS session created that same issue (else the handler slot-fills — and since 2026-08-13 the slot-fill consults the user's DEFAULT repo via `resolve_repo` (the first_contact/#1590 rail) before asking; **#1567 (2026-08-16)**: the "which repo?" dead-end is now a BINDABLE question — natural repo phrasing ("in the test-Piper-Morgan repository", quoted names, case-insensitive; bare names resolved against the user's actual repos via the #1327 `search_user_repositories` rail, default-name match first) extracts from the ORIGINAL ask (`repo_clarification.extract_natural_repo_name`; a user-NAMED repo that doesn't resolve ASKS, never falls to the default silently), and when no repo resolves at all the update/close handlers ARM the #1190 action-agnostic carrier (kind `issue_repo_question`, `services/intent_service/repo_clarification.py`) instead of refusing: the next turn's answer — bare `owner/name`, bare name, natural phrasing, or a same-operation restatement (restatement title/body slot-fills win) — binds at the pop seam and re-dispatches the ORIGINAL intent via `run_confirm_pending_action_workflow`; bare "yes" on the open form self-re-asks (the confirm re-dispatch lands back in the handler, which re-arms); a failed name lookup with a default repo set asks the closed "say 'yes' to use your default, owner/name" form; unrelated commands abandon via the pop and route normally (#1631 discrimination inherited at the generic seam). `_handle_close_issue_query` gains session threading (`run_close_issue_workflow`) + explicit-repo honoring (a named repo threads `owner/repo_name` through `get_issue`/`update_issue`; unnamed closes keep the router-internal resolution unchanged). The no-session refusal (teaching the routable `set my default repo to owner/name` phrase) remains the fallback. **#1641 (2026-08-18)**: the same carrier now serves the REMAINING call sites — the reopen + comment handlers get the identical shape (explicit/natural repo honoring, carrier armed on the router's no-repo dead-end, `session_id` threaded via `run_reopen_issue_workflow`; comment scans with the extracted comment TEXT scrubbed out so body prose never reads as routing); the three ANALYSIS 'repository not specified' dead-ends (`_handle_analyze_commits`/`_handle_generate_report`/`_handle_analyze_data`, shared consult in `_resolve_analysis_repository`) go explicit → slot-fill → natural phrasing → the #1411 default-repo consult → the carrier (non-issue-anchored form: `issue_number=None` + an `operation` phrase, e.g. "Which repository should I use to analyze commits?"), with the answer re-dispatching into the SAME analysis handler via the rail (`_ANALYSIS_QUERY_COHORT` entries now `pass_session_id=True`); and the create path resolves the natural "in the X repository" phrasing via the same extraction (owner/name slot-fill unchanged; a user-NAMED repo that doesn't resolve asks via the carrier — never silently falls to the default). Same date, clarify-first (PM ruling, decisions.log ~14:1x): a close-shaped unmapped status value ("status → Done") ASKS "By 'Done' do you mean close issue #N?" via the #1190 `pending_action` carrier (kind `unmapped_field_value_clarification`); "yes" dispatches `close_issue` through the same confirm path — no silent synonym mapping). Before this, the no-`#` form ("issue 108") was claimed by surface 1's document pattern (`change … to`) and the `#` form fell to the LLM (reachability = corpus). Guards: update verb + issue-field word required; any document noun (doc/readme/spec/…) declines; bare explicit `#N` withOUT the update-field shape still falls through untouched. |
| 1 | **Pre-classifier** | `services/intent_service/pre_classifier.py` | Deterministic (regex/pattern) | Intercepts known shapes BEFORE any LLM call — identity ("who am I?" → `get_identity`), insights (`pull_insights`), stakeholder updates (`write_stakeholder_update`), portfolio (`manage_portfolio`), status (`get_project_status`), standup, etc. Cheap, deterministic, and the reason "the LLM classified X wrong" is often unobservable in production: the LLM never saw the phrase. **#1527 delete-claim narrowing (2026-08-29)**: the PORTFOLIO delete-family patterns (delete / remove / get rid of) DECLINE via a negative lookahead (`REMINDER_TODO_NOUN_GUARD`) when the delete-target noun phrase carries reminder/todo vocabulary (reminder(s) / todo(s) / to-do(s) / task(s)) — PM live 2026-08-29: 'delete the reminder to hydrate' and the system-taught 'delete my hydrate reminder' were claimed by the greedy `\bdelete\s+…(.+)` capture into "couldn't find a project called '…'", three misroutes in one exchange, and because this surface runs before the Inversion consult the flip never saw them. Narrowing only — a guarded miss falls through BOTH pattern entry surfaces (`pre_classify` AND `detect_multiple_intents`, which consult the same PORTFOLIO_PATTERNS) to the LLM lane, whose delete_todo emission dispatches the #1666 DESTRUCTIVE rail family; no new pre-classifier claim was added (moratorium-clean: this removes deprecated-layer claims). Companion narrowing, exposed by the fix: REMINDER_QUERY_BLOCKERS gains the phrasal destructive verb "get rid of" so the released 'get rid of my reminders' cannot be claimed by the reminder LIST lane. Legitimate project deletes ('delete the alpha project') still claim; archive/hide/restore untouched. Regression: `tests/unit/services/intent_service/test_reminder_delete_misroute_1527.py` (both surface-1 entry points + e2e that the routed destination is the todo family and the #1666 title-bound confirm still arms). **#1738 portfolio-list subsumption (2026-09-12)**: `detect_multiple_intents` no longer emits a phantom STATUS/`get_project_status` sibling beside PORTFOLIO on list phrasings — "list my archived projects" matched both PORTFOLIO's list pattern (now the named `PORTFOLIO_LIST_PATTERN` constant) and STATUS's broad `\blist.*projects\b`, making every list-projects turn multi-intent; when the STATUS sibling failed, the orchestrator stapled "I wasn't able to check on project status…" onto a SUCCESSFUL listing (PM live 2026-09-09 v70; same rider as the #1431 screenshots). New `_apply_subsumption_filter` rule (the #1084 mechanism — no new claim, moratorium-clean) drops only `get_project_status`, only when the message matches the list claim, so a portfolio WRITE beside a genuine status ask keeps both. Regression: `tests/unit/services/intent_service/test_truncated_render_provenance_1738.py`. **#1884 widening (2026-09-24)**: the list-only condition left the same phantom on every OTHER portfolio verb — a bare 'archive project X in my portfolio' / 'add a new project…' / 'restore project X…' / 'link owner/repo to project X…' came out PORTFOLIO + a phantom STATUS (delete alone was already declined by #1756's DESTRUCTIVE_ASK_BLOCKERS on the STATUS lane), which #1763 found because it made a one-topic write a multi-intent turn. The rule is now: drop the `get_project_status` sibling iff (a) any PORTFOLIO intent survived the turn (any verb, `manage_portfolio` or `manage_repos`) AND (b) every STATUS_PATTERNS entry that actually matched the message is one of the nine project-noun overlaps (`my portfolio`, `my projects`, `current/active projects`, `project overview/landscape`, `show/list.*projects`, `projects.*working on`) rather than genuine status vocabulary (`project status`, `status update`, standup*, progress*). Consequently 'archive X and what's my project status?' keeps both — and so does 'list my archived projects and what's my project status', which the old literal-anywhere list check wrongly subsumed. The overlap set is a local inside `_apply_subsumption_filter`, not a `*PATTERNS` list, so `TestExtractionPatternRatchet` is untouched. Regression: `test_subsumption_portfolio_write_family_1884.py`. **#1755 span-aware TEMPORAL-skip on the multi-intent connect path (2026-09-24)**: `detect_multiple_intents` has an INTEGRATION_CONNECT_PATTERNS group (#1505, 2026-09-12 — the single path's #1417/#1471 connect claim made reachable on the multi path, guarded by the shared `_integration_connect_match` so the #862 repo-lane and #1471 event-write blockers hold here too) checked BEFORE TEMPORAL_PATTERNS; a connect claim used to suppress the WHOLE TEMPORAL group (#1471's original rationale: 'connect my calendar' also matches the temporal `\bmy calendar\b` pattern on the SAME words, and without a skip the user gets a current-time phantom beside the setup guidance). That skip was GROUP-LEVEL, not span-aware, so a genuinely two-part message lost its temporal half too — 'what time is it? also connect my github' resolved to connect-only (found during the #1505 repro probe). The skip is now span-aware: `PreClassifier._temporal_disjoint_from_connect` retains the connect match's `.span()` (`connect_span`, hoisted above the loop) and checks every `TEMPORAL_PATTERNS` match (`re.finditer`, all patterns, all occurrences — not just the first hit per pattern) for one whose span is DISJOINT from `connect_span`; only a temporal match that OVERLAPS (or is contained in) the connect span stays suppressed, and a disjoint one falls through to the normal match-and-append logic. No new extraction pattern — reuses `TEMPORAL_PATTERNS` as-is; the `re.finditer` call passes a bare loop-variable pattern, never an inline literal, so `TestExtractionPatternRatchet`'s counter is unaffected. Append ORDER is priority-list order, not message-word order: `INTEGRATION_CONNECT_PATTERNS` precedes `TEMPORAL_PATTERNS` in `pattern_groups`, so the connect intent is always appended before a surviving temporal intent regardless of which half comes first in the actual text (same convention as the pre-existing greeting-before-connect order in the #1505 pins). The #1471 calendar-collision parity (temporal words CONTAINED WITHIN the connect span, e.g. 'connect my calendar') is unchanged, byte-for-byte. Regression: `tests/unit/services/intent_service/test_multi_intent_temporal_span_1755.py`; parity: `test_multi_intent_connect_1505.py`, `test_integration_connect_preclassifier_1417.py`. **Extraction-pattern ratchet**: argument-extraction-by-regex — this surface's pattern lists AND the handler-side slot-fills (`_slotfill_issue_request`, `todo_handlers`' todo/reminder extraction, `drafted_issue`'s answer patterns) — is interpretation-layer work: gate-side, corpus-deposit by default, enforced by `TestExtractionPatternRatchet` in `tests/test_architecture_enforcement.py` (added 2026-08-29, PM-ratified after the live round). **Pre-claim shadow probe (2026-09-02)**: this surface now carries an OBSERVATION layer — on a sampled claimed turn (`PIPER_PRECLAIM_SHADOW`, default OFF) the constrained inversion router is consulted post-claim and the agree/disagree line carries the claiming `*PATTERNS` list's NAME, the unit the narrowing schedule deletes at; see the pre-claim probe block below the #1677 entry. |
| 2 | **LLM classifier** | `services/intent_service/classifier.py` (`IntentClassifier.classify`) + `llm_classifier.py` | LLM | Emits an `Intent` (category + action + confidence). Its ACTION VOCABULARY is prompt-suggested, not enforced — it can and does emit paraphrase variants (probe evidence: `list_stale_prs`, `analyze_productivity`). |
| 3 | **Action rail** | `services/intent_service/workflow_entries.py` (`register_default_workflows`) → `workflow_dispatcher.get_action_workflows()`; consumed in `services/intent/intent_service.py::process_intent` | Deterministic dict lookup | If `intent.action` is a registered key (canonical or alias), dispatch pre-floor to that handler. 110 keys ≈ 32 handlers + aliases (census D count 2026-07-16; corrected 2026-08-02 by #1433 — the old "~86" sat stale for weeks, F24; +4 keys 2026-08-08, #1521 reminder-list cohort; +4 keys 2026-08-10, #1570 archived-projects list — `list_archived_projects` + 3 aliases, effect=READ, self-contained entry point; +4 keys 2026-08-16, #1624 uploaded-document summarize — `summarize_document` + 3 aliases, effect=READ, outwardness=PRIVATE: the first SYNTHESIS registry canonical, reached LLM-lane via the Phase-4 verb shim's one mapped SUMMARIZE cell (`(SUMMARIZE, "document")`) or classifier.py's bare-`summarize` normalization; the handler calls the SAME `handle_summarize_document` the REST route uses, resolves "the document" via the un-orphaned `FileResolver` (owner-scoped since #1312), answers deterministically-honestly when no upload resolves, and returns None (rail fall-through to the #1187 SYNTHESIS floor path) for issue/commit-shaped requests. Every OTHER summarize source stays floor-by-#1158; the dormant `_handle_summarize` + IntentEnricher + the never-fired summarize template rows were deleted in the same change — forensics: `docs/internal/operations/summarize-intent-forensics-2026-08-15.md`; +3 keys 2026-08-19, #1666 delete_todo family; +3 keys 2026-08-25, #1685 create_todo family — **live count re-measured 2026-08-25: 123 keys / 43 unique entries**, all `action_triggered`, so read the running "+N" notes as provenance, not as an arithmetic you should trust over `len(get_action_workflows())`). The alias lists are **mode-4 defense** against variant emissions — necessary, provably insufficient alone (4 stale-PR aliases still missed a live 5th variant). **#1190 destructive-confirmation gate (2026-08-10, PM ruling)**: inside this surface's dispatch branch, an entry whose declared effect derives `needs_confirm` (== `EffectClass.DESTRUCTIVE`; currently the close/reopen pair, 4 alias keys — the first live DESTRUCTIVE entries — plus the delete_todo family, 3 alias keys (delete_todo/remove_todo/cancel_todo), added 2026-08-19 by #1666: Arch found delete_todo rail-UNREGISTERED, so it never reached this gate and the legacy elif deleted IMMEDIATELY with no confirm; the elif is now REMOVED (rail is the single dispatch surface, `run_delete_todo_workflow` carries its body incl. the #1605 clear-family seam) and the confirm is built by the ASYNC `build_todo_delete_confirmation` — positional "todo N" target means the honest ask needs the owner-scoped list read, so the gate binds the REAL todo text into the question ('Delete todo N: "text"? (yes/no)', never number-only) AND the resolved row into the intent (`delete_todo_resolved` + the confirmed marker → the yes deletes exactly the row named in the ask, never a positional re-resolve against a shifted list); clear-family shapes pass through so reminder_clear keeps first claim; lookup failure returns an honest no-op turn, never an ungated delete. Regression: `test_delete_todo_confirm_1666.py` + `tests/integration/test_todo_delete_chat_path_1666.py`) does NOT execute on the classified turn — the gate stores the deferred action as a pending offer (the #846 session-scoped store, popped before classification, so #1529 offer-binding ordering holds) and asks one yes/no question. "yes" re-dispatches the ORIGINAL intent via the offer-acceptance seam → `run_confirm_pending_action_workflow` (registered `confirm_pending_action`, action_triggered=False — rail-unreachable); "no"/bare-exit cancels honestly; off-intent abandons (the pop already cancelled). **#1650 crisp-accept (2026-08-18)**: every offer dispatching the confirm carrier (`workflow_type == confirm_pending_action` — destructive confirms, consent checks, reminder-clear delete confirms, drafted-issue file confirms, repo-question default binds) consults the STRICT `detect_confirm_response` (soft_invocation.py) at the pop seam instead of the generic `detect_offer_response`: accept ONLY when the whole message is a crisp anchored affirmative (yes / y / yes please / do it / confirm / go ahead / short combinations). The greedy generic rows ("^please\s" etc.) had claimed PM's one-line ~95-char aside as a YES — under the #1631 prose floor, so the shape override never triggered — and fired an armed delete. Non-crisp non-decline turns fall to each kind's documented off-intent rule; declines unchanged; generic (non-confirm) offers keep #1631 behavior byte-for-byte. Kind-specific accept layers hardened the same way: drafted-issue near-accepts RE-ASK + re-arm (never file, never drop composed work), the repo-question closed-default bind requires a crisp yes, and reminder-clear's correction-window claim is anchored + non-prose (`_CORRECTION_CLAIM_RE` — an aside that merely mentions deleting no longer claims the window). Regression: `test_confirm_crisp_accept_1650.py` + pins in the 1605/1571/1567 suites. Generic deferred-action carrier documented in `services/intent_service/destructive_confirm.py`; **#1571 drafted-issue binding (2026-08-15) is now the carrier's second consumer** (`services/intent_service/drafted_issue.py`): the #1510 collaborate turn in `_handle_create_issue` ARMS a pending action (kind `drafted_issue`) binding the rendered draft, so "file it (as is)" — including the original incident phrase "file it in owner/repo", repo override honored — IS the confirmation: handled kind-specifically at the pop seam BEFORE generic accept/decline (the #1605 precedent), acceptance delegates to `run_confirm_pending_action_workflow` (original Intent re-dispatched through the create rail; the `destructive_confirmed` marker now also tells the collaborate gate consent-was-given, so no double-ask), success copy derives from the actual tool result, and any non-created outcome RE-ARMS the draft (retry never loses it). Off-intent abandons per the carrier's rules. **#1627 mid-compose prose hold (2026-08-15, round 2)**: while the drafted_issue offer is armed, a PROSE turn that answers the open body question ("What should the body say…?") binds to the draft at this same pop seam — appended to the draft body and `intent.context["description"]` (so it is what actually files), offer re-armed, draft echoed back — BEFORE any classification surface can see it. The live thief was surface 1's greedy #1527 portfolio pattern (`\bdelete\s+…(.+)`) claiming PM's long body answer ("I couldn't find a project called '(a destructive action)…'"); the #1623 mid-interview hold could not cover it because the draft flow is floor-composed prose, not a registered gathering process. NOT a turn lock: file/accept phrases still file, declines/bare exits still drop the draft honestly, and anchored-imperative asks (the shared collaborate-gate execute check plus a close/read/destructive verb supplement) still route normally, abandoning the draft; long or multi-line turns read as prose regardless of how they open (`is_body_prose_answer` in `drafted_issue.py` — discrimination limits stated in its docstring; regression: `tests/unit/services/intent_service/test_drafted_issue_body_steal_1627.py`). **#1630 subjectless arm (2026-08-15, round 3 — the unarmed face)**: "help me write a ticket" with NO extractable subject used to arm nothing (no subject = no draft), so the answer to "What's it about?" was a bare prose turn for the same greedy chain — the #1627 theft, one turn earlier. The collaborate turn now arms a minimal SUBJECTLESS `drafted_issue` carrier at the ask; the FIRST bound prose names the draft (`derive_subject_from_prose` → draft title, mirrored into `intent.context["title"]` so the create rail files it — the subjectless original message slot-fills nothing) and seeds the body per the same append semantics. Same discriminator, same seam, same exits; the subjectless ask copy still teaches no file phrase until the draft has content (regression: `test_drafted_issue_subjectless_1630.py`). **#1648 (2026-08-18, round 4 — the fabrication face)**: PM's "file as is thanks" missed the file-command regex (object-less "file **as is**"), read as an anchored EXECUTE imperative, fell through the seam as off-intent, and the FLOOR roleplayed the entire filing ("Filed in test-piper-morgan" — zero writes). Three-part fix: (a) `_FILE_COMMAND_RE` broadened — object optional when an "as is" tail carries the reference, trailing pleasantries/affirmative lead-ins absorbed, still anchored full-message; (b) an honest NEAR-MISS fallback at the seam — a file/submit-headed turn without its own subject that matches neither file-command, prose, accept/decline, nor exit RE-ASKS and RE-ARMS (`is_file_near_miss` + `_reask_near_miss`), never a silent mid-compose abandon into the chain; disjoint from and composed with #1650's near-accept re-ask (that branch needs a loose ACCEPT read, this one needs NO offer-response read); genuinely-new file asks ("file a bug about X") and other command families still abandon and route; (c) the floor prompt's action-claims contract (surface 4). The same silent-abandon audit found and fixed the identical gap in the #1605 clear-verb question (`reminder_clear._reask_verb_question_if_unrecognized`). **Companion carrier, same issue**: `handle_create_reminder`'s honest time-clarify ask ("When should I remind you?") used to arm NOTHING, so the answer turn ("at 3pm") orphaned into the chain and the floor roleplayed "Reminder set" (no row, no 📅). The ask now arms a `reminder_time_question` pending offer (`todo_handlers.build_reminder_time_offer`); the answer binds at the pop seam (`handle_reminder_time_turn`) and performs the REAL save with the real 📅 confirmation; unbindable/absent times re-ask + re-arm; full reminder restatements and unrelated commands abandon via the pop and route normally; `clarify_reminder_time` is the offer-only generic-accept landing (`action_triggered=False`). Regression: `test_action_fabrication_1648.py`. **#1654 (2026-08-22) — the same treatment one question earlier**: `handle_create_reminder`'s OTHER honest ask, the no-task clarify ("I didn't catch what you'd like to be reminded about" — PM hit it twice on 08-18 via the colon-form parse misses, which themselves stay #1606/corpus), also armed nothing. It now arms a `reminder_task_question` pending offer (`todo_handlers.build_reminder_task_offer`, payload carries the ORIGINAL message — strings only) and the answer binds as the TASK at the pop seam (`handle_reminder_task_turn`): the time is then either already known from the original message (rare — e.g. "set a reminder: at 3pm", re-parsed at answer time, only when an explicit `_has_time_signal` — never the parser's tomorrow-morning default, #1490) and the REAL save runs with the shared 📅 copy, or the flow CHAINS into the existing `reminder_time_question` carrier (the full two-question recovery: task answer → time ask → time answer → real save). An answer carrying its own trailing time saves in one turn (time expression shed from the saved text via the shared strip); a pure-time answer re-asks for the task. ⚠️ Off-intent discrimination deviates from the shared `is_command_shaped` DELIBERATELY: the task-answer space is arbitrary imperative phrases and the shape-read's verb heads (check/get/set/…) claim legitimate task answers ("check in with the team" is the ask's own example copy) — the discriminator is the pre-classifier's DETERMINISTIC claim instead (probed 2026-08-22: claims every product command tried, no bare task phrase); declines/bare exits drop via `decline_message`, restatements + claimed commands release-and-route, everything else binds (visible, declinable) rather than orphaning to the LLM lane. `clarify_reminder_task` is the offer-only generic-accept landing (`action_triggered=False`); `reminder_task_question_pending` joins the `_apply_soft_offer` no-clobber flags; the kind is pinned OUTSIDE the #1664 confirm set. Regression: `test_task_clarify_1654.py`. **#1654 consume-half adoption (#1739 epic 3, 2026-09-12)**: BOTH reminder question turn handlers (`handle_reminder_task_turn` / `handle_reminder_time_turn`) now consult `acceptance.evaluate_acceptance` at their registry-declared axes (`clarify_reminder_task` / `clarify_reminder_time`: READ×PRIVATE → LOW_CEREMONY) with the arm-site's stored ask threaded (#1665), replacing the legacy `detect_offer_response` (the todo_handlers ratchet row shrank out). Contract axis (a) is the load-bearing gain, reproduced red-first: a question no deterministic surface claimed BOUND AS THE TASK ("what do you mean?" → "Got it — **what do you mean**"), and a time-bearing state question at the time seam SAVED a reminder ("did I say 3pm?" parsed and wrote a row). A STATE_QUESTION verdict now falls through to the generic seam's adopted READ branch — silent §5a re-arm, normal processing answers, the arm survives (nothing can fire from it; the REAL save runs only off a fresh answer turn). ACCEPT still only re-asks (the crisp CONFIRM superset it adds used to bind as the task text, so the wider accept surface is a strict improvement); DECLINE still falls to the honest decline; question-suffixed time answers ("tomorrow at 9?") now cost a turn, not an action (§5b, pinned deliberately). Regression: `test_reminder_question_acceptance_1654.py`. Instruction-shaped draft refinement ("make the title snappier") remains deliberately not built (an anchored-imperative refinement turn abandons the binding; carrying an evolving floor-composed draft under interpreted edits needs a durable store — Inversion Phase 2 is the durable fix). Companion renderer guard: `strip_placeholder_slots` (conversational_floor.py) makes the `#[issue number]` template-slot class structurally unrenderable (replaced with deterministic no-tool-result honesty) — the literal PM saw live exists nowhere in prompts/copy; the model improvised it, so the kill is renderer-side like `strip_scaffolding_artifacts`. Orthogonal to the #1510 collaborate-gate (execute-mode users still confirm destructive actions). +3 offer-only registry keys (`confirm_pending_action` #1190; `verify_inference` #1510 read-back acceptance; `standup_interview` #1591 invitation acceptance) → NOT in the 110 action-rail count; all `action_triggered=False`, reachable ONLY via the offer-acceptance seam. **#1591 standup preference capture (2026-08-13)** is surface-internal to the standup handler, NOT a routing change: an explicit report token (`\breport\b|\bquick\b`) mirrors the #1511 interview token inside the already-claiming handler; a stored verified `standup_mode` (the #1510 rail's store) redirects the generic ask without re-inference; the post-report invitation / low-confidence read-back binds via the same #846 pending-offer store (popped before classification, so the #1529 ordering holds). **Declaration path added later the same day (PM live PARTIAL verdict)**: a standup-token DECLARATION turn ("use the standup interview format by default from now on", `standup_preferences.detect_standup_mode_declaration` — durativity composed from `collaboration_gate.has_durative_marker` + a `back to` switch-back marker) is checked FIRST inside the handler and stores the mode directly (`source=user_declared`, confidence 1.0 — store + confirmation copy, never a read-back); the taught switch-back phrase `back to my standup report` rides the `_is_standup_query` "my standup" cue so it routes AND re-declares deterministically. ⚠️ Reachability of the bare-'standup' declaration form is still LLM-lane (no deterministic surface claims bare "standup" — #1595 corpus material), and the tokenless "use the interview from now on" is a corpus row, deliberately unclaimed. **#1651 standup offer-referent binding (2026-08-18)**: the standup's closing copy stopped offering actions it couldn't consume — PM live: the report closed with "mark that overdue todo done?", the verbatim acceptance fell to `complete_todo`'s title matching ("I couldn't find a todo matching 'overdue'"). When the user has an OVERDUE todo, the non-empty report's trailing line now offers to complete the single strongest (most overdue) one WITH the todo's id bound into the #846 carrier at offer time (`services/intent_service/standup_todo_offer.py`, kind `standup_todo_offer` — the reminder-clear/drafted-issue idiom); acceptance (crisp "yes" or the verbatim phrase) dispatches the offer-only `standup_complete_todo` entry (WRITE, `action_triggered=False` — the count of offer-only keys grows by one), which completes the BOUND id via `TodoManagementService` — never a re-parse of the user's phrasing; decline drops honestly; off-intent abandons via the pop with #1631 prose discrimination inherited at the generic seam. One-slot discipline: when the bound offer arms, the #1591 mode asks stay quiet that turn; the empty-report branch is untouched (PPM's empty rule — invitation leads, no referent offer). **#1652 (2026-09-12) closed the partial-coverage residue #1651 left**: the two OLDER #1591 arms (the interview invitation — BOTH its after-report and empty-lead sites — and the low-confidence mode read-back) armed the same one-slot #846 store on the rail-dispatched `get_standup` path with NO `*_pending` intent_data flag, so `_apply_soft_offer` could clobber them with a soft workflow offer (#1651's flag covered only its new bound todo offer). Arm half: the three sites now stamp `standup_interview_invitation_pending` / `verify_inference_read_back_pending`, both listed in `_apply_soft_offer`'s no-clobber `_pending_flags`. Consume half (#1739 adoption, epic 3): the `verify_inference` and `standup_interview` kinds consult `acceptance.evaluate_acceptance` at their registry-declared axes (WRITE×PRIVATE → LOW_CEREMONY) with the arm-site's stored ask threaded (#1665); a STATE_QUESTION verdict re-arms SILENTLY (contract §5a LOW-tier survival — normal processing answers) instead of the legacy detector's None → off-intent pop silently costing the user the pending ask. Regression: `tests/unit/services/intent_service/test_standup_offer_flag_1652.py`. |
| 4 | **Category handlers + floor-internal action checks** | category routing in `intent_service.py`; `conversational_floor.py`, `context_assembler.py` | Mixed | Anything not action-railed routes by `intent.category` (TEMPORAL/STATUS/PRIORITY/IDENTITY/…). Several of these check `intent.action` BY NAME internally (e.g. `pull_insights` in `conversational_floor.py`, MEMORY handling in `context_assembler.py`) — this is the **fourth vocabulary**: real dispatch that no rail listing shows. Bottom: the unhandled-LLM floor (improvised response) — the place #1283 exists to keep phrases OUT of. **Since #1570 (2026-08-10) BOTH floor doors gather domain context**: `_handle_floor_with_context` always did; `_handle_unknown_intent` (the generic-QUERY / offer-fallback / ANALYSIS-etc fall-through door) previously floored with `domain_context=None` — a data query landing there ("what todos are pending?" as an unrailed QUERY emission) saw zero user data while the store had rows. It now runs `ContextAssembler.gather_context` (caller-curated context, e.g. #1187 summarize, is preserved and skips the gather). **#1544 (2026-08-16) closed the residual empty-case misframe on this path**: zero pending todos is now a VERIFIED-EMPTY fact, not an absence — `_compute_pending_todos` returns `{"pending_todos": [], "pending_todo_count": 0}` (never `None`) when the owner-scoped read succeeds with zero rows, and `_format_domain_context` renders a distinct `PENDING TODOS: none — checked this turn` line, so the floor can say "your todo list has no pending items" as an account-level fact. The floor prompt's never-fabricate section was the OTHER half of PM's 2026-08-09 transcript ("I don't see any todos in your list right now — nothing's showing up on my end for this conversation"): its empty-data guidance *itself* supplied both example strings ("I don't see any todos in your list right now", "… in this conversation"); the guidance is rewritten — data absence is a visibility claim about THIS TURN, never a conversation-scoped fact, and the empty-list claim is licensed only by the verified-empty context line. The todo data path is owner-scoped end-to-end (`TodoManagementService.list_todos(user_id=…)` → `get_todos_by_owner`); no conversation-scoped todo read exists anywhere — the scoping was prompt-seeded copy. Pins: `test_todo_scope_framing_1544.py` (prompt + renderer), `tests/integration/test_pending_todos_query_1544.py` (real-Postgres gather, both cases). **#1639 (2026-08-18) applied the same verified-empty treatment to the sibling gathers**: `_compute_projects` and `_compute_completed_todos` now return `{"projects": [], "project_count": 0}` / `{"completed_todos": [], "completed_todo_count": 0}` instead of `None` when the owner-scoped read succeeds with zero rows (an errored read still returns `None` — never verified-empty), and `_format_domain_context` renders distinct `PROJECTS: none — checked this turn` / `COMPLETED TODOS: none — checked this turn` lines, so per lane populated / verified-empty / never-gathered are three distinguishable states at the renderer; the never-fabricate guidance's context-line examples name all three lanes (context lines only — no example reply strings, #1544's root cause). Pins: `test_sibling_verified_empty_1639.py`. **#1648 (2026-08-18) — the floor ACTION-CLAIMS CONTRACT**: the never-fabricate guidance constrained DATA claims; nothing constrained the floor from claiming ACTIONS, and in one PM session it roleplayed a full issue-filing ("Filed in test-piper-morgan", no issue existed) and a reminder save ("Reminder set for 3pm today", no row). The #1331 section is rewritten as an explicit contract: the floor composes replies ONLY — actions run solely via dispatched rails whose handlers compose their own confirmations from tool results; no success confirmations, progress narration, action role-play, or offers to "confirm"/"go ahead" with an undispatchable action; implied-but-unperformable actions get an honest can't-do-this-turn plus a pointer at the one-line ask that routes. Per the #1544 root cause, the rewrite REMOVED the section's example reply strings (the old prompt's own "On it — creating that now…" example is the near-verbatim shape of the live "On it — setting a reminder for 3pm today" fabrication) — the guidance states rules, never sample sentences (pins: `test_floor_action_claims_1648.py`). Floor output is also scrubbed renderer-side: `strip_scaffolding_artifacts` (conversational_floor.py) makes the prompt's own bracketed scaffolding headers (`[Available context…]`, `[Context: …]`, `[Reference binding: …]`, `[Redirect context: …]`) structurally unrenderable in user copy — #1393's prompt-side prohibition alone did not hold (PM live 2026-08-10). A new scaffolding block added to the prompt builders must join `_SCAFFOLDING_BLOCK_RE` in the same commit. **#1536 FTUX-COLDSTART (2026-08-10)**: on the FIRST exchange of a conversation (no completed turn yet — per-conversation, judged from the #1122 in-flight-turn semantics) with a configured connector (#1547 `IntegrationStatusService`, binding-first), `gather_context` additionally runs the first-contact rail (`services/intent_service/first_contact.py`, rides outside the category dispatch like the #1566 reminder rail): a small recency-ranked slice of the user's real GitHub data (repo via the #1042/#1327 default-repo rail; no resolvable repo → NO demo and NO "which repo?" question) lands as `first_contact_demo` / `first_contact_source_failed`, which the floor renders as an open-with-their-data demonstration directive (entities confined to the gathered payload). The canonical CONVERSATION pure-greeting path (which never touches the assembler) appends the same payload via the DETERMINISTIC `render_first_contact_block` in `ConversationHandler._respond_to_greeting`. **#1596 (2026-09-12) — post-guided-flow-escape floor amnesia, closed at the two layers still open** (the history half was already fixed by #1394 on 2026-08-08 — verified e2e through a real escape and pinned, not re-fixed): (1) *the floor's read* — the assembler's CONVERSATION special-case (`pass`, "deliberately-minimal context for greetings") is REMOVED; CONVERSATION falls into the #960 else-branch baseline. The rationale was keyed to a caller that no longer exists — pure pleasantries take the canned canonical greeting and never reach the assembler, while the turns that DO arrive as CONVERSATION are the classifier's vague/low-confidence rewrite (`clarification_needed`, classifier.py's `_seems_vague`/`confidence<0.3` seam — exactly where post-escape fragments like PM's verbatim 'none' land), compound greetings (#1416), and chitchat/farewell floor turns; those floored with domain_context ≈ `{current_time}` while the structurally identical UNKNOWN fall-through got the baseline. (2) *the escape's state handoff* — the #899/#1529 fall-through prefix is glued onto the reply AFTER floor composition and the in-flight turn is excluded from history, so the escape-turn floor composed with the flow's open question visible and nothing saying the flow closed (it could re-open the interview the user just escaped). `_check_active_guided_process` now returns the escaped `ProcessType` beside the prefix (3-tuple); the classification seam stamps `intent.context["guided_flow_escape"]` (strings only, per-turn — never sticky); the three floor doors merge it into domain_context; `_format_domain_context` renders a rule-stating GUIDED-FLOW-ENDED directive (#1655-clean). Arms/acceptance untouched — no detector added, `evaluate_acceptance` not involved, §5a/§5b interplay unchanged. Regression: `tests/unit/services/intent_service/test_floor_escape_amnesia_1596.py` (10 red pre-fix / 7 green control pins). **#1772 residual — post-compose SCOPE GUARD (2026-09-26)**: the #1717 source-failed directive (see `SOURCE_FAILED_FLAGS` in `conversational_floor.py`) is a PROMPT instruction — a request the model can decline — and three measurement rounds (`dev/2026/09/15/1772-scope-leak-measurement.md`, `dev/2026/09/24/1772-candidate-measurement-2026-09-24.md`, `dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md`) showed anthropic's floor composing a second sentence naming UNARMED sources as failed/unavailable at 50% → 20% → 10% across three copy revisions of the same single-armed-flag prompt (the dominant template: *"For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn"* — "calendar" is not even a registered `SOURCE_FAILED_FLAGS` check, so the model was inventing the category, not just over-scoping to adjacent real checks). CXO ruled BUILD, not accept the residual (a measured rate is a promise about phrasing, not a mechanism property); Arch ruled the mechanism sound, with a binding adversarial-pass condition. `services/intent_service/scope_guard.py`'s `apply_scope_guard` runs at the SAME output seam as `strip_scaffolding_artifacts`/`strip_placeholder_slots`/`enforce_armed_offers` (`ConversationalFloor.respond()`, right after the placeholder-slot strip): it drops any sentence that CLAIMS an unarmed source failed/was unchecked this turn (never rewrites), computing the armed set from the identical `SOURCE_FAILED_FLAGS` registry the prompt used, plus a small explicit synonym table (`SOURCE_FAMILIES` — todos/reminders/calendar/projects/github, calendar deliberately unarmable since it has no registered flag). A sentence naming BOTH an armed and an unarmed source under a failure claim is KEPT (the true claim about the armed source would otherwise be lost to filter the false half). If dropping empties the reply or leaves a fragment, a fallback honest sentence is composed from the armed check_names (`build_fallback_sentence`, copy owed to CXO). Zero cost when nothing is armed — a turn with no source-failed flag never scans. `FloorResponse.scope_guard_dropped` carries the per-turn drop count for measurement without re-reading reply prose; `floor_scope_guard_dropped` logs the count and the unarmed source names, never the reply text. This is deterministic POST-COMPOSE OUTPUT FILTERING, not argument extraction — it is NOT scanned by `TestExtractionPatternRatchet` (which only scans named symbols in `pre_classifier.py`/`todo_handlers.py`/`drafted_issue.py`/`intent_service.py`'s slot-fill helper). Regression: `tests/unit/services/intent_service/test_scope_guard_1772.py` (12+ hand-written legitimate-mention over-trigger corpus, all 8 distinct leaking replies from the three measurement docs as the under-trigger corpus, fallback, no-armed-flag no-scan, the armed+unarmed-in-one-sentence keep decision). The unit layer proves the filter is deterministic and narrow; the live leak rate WITH the guard active is a separate measurement the Lead is scheduling, not something this entry or its tests claim. |

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
⚠️ Known boundary: legacy `_handle_execution_intent` chain actions have no declared
effect and are OUTSIDE this gate — their consent rides their rail migration.
**delete_todo migrated 2026-08-19 (#1666)**: DESTRUCTIVE rail entry, elif removed,
#1190-gated (see surface 3). **create_todo migrated 2026-08-25 (#1685)**: WRITE rail
entry (PRIVATE, `action_triggered`), elif removed, `run_create_todo_workflow` carries
its body — Arch found #1666's exact gap on the create side while checking a claim
rather than trusting it. The distinction #1685 turns on: create_todo was not "a WRITE
the matrix waves through", it was UNREGISTERED, so `effect_for_action` returned None
and nothing evaluated it. ⚠️ The registration adds EVALUATION, not ceremony: PRIVATE ×
WRITE × execute framing is PROCEED, and every natural create phrasing is verb-initial
imperative, so a create turn still writes the row in one step (A/B-verified against the
pre-#1685 tree: the no-ceremony assertions pass on BOTH sides, the consent-consulted
assertions pass only after — the m-44 indistinguishability this closes). An
AMBIGUOUS-framed create emission is now held for a consent check exactly as its
already-registered sibling create_reminder is; that is the ratified #1509/#1510
matrix, not a create-todo gate. Alias family enumerated from `ActionMapper`
(create_todo / add_todo / new_todo — it does NOT mirror delete's
delete/remove/cancel). Regression: `test_create_todo_rail_1685.py`.
Still on the chain and outside the gate: complete_todo / list_todos / next_todo (and
create_reminder's backstop elif — its rail entry is the consented surface);
`capability_legibility.catalog_coverage()` states the denominator.

**#1605 reminder-clear verb disambiguation (2026-08-14, CXO/PPM jointly-signed-off
design)** — surface-internal to the EXECUTION lane, NOT a routing change (routing
moratorium honored; no pre-classifier or prompt-pattern additions).
`services/intent_service/reminder_clear.py`: a clear-family verb (clear / handle /
take care of / reset) over the reminder/todo domain, with NO explicit
complete/delete verb, is detected from the ORIGINAL MESSAGE inside the three
already-claiming EXECUTION surfaces — the legacy `complete_todo` elif branch, the
delete_todo dispatch surface (the elif when #1605 shipped; since #1666 the seam
lives unchanged in the rail entry point `run_delete_todo_workflow`, still FIRST —
the #1190 delete-confirm gate passes clear-family shapes through untouched) (the classifier's guess for the ambiguous utterance; candidate effect
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
now refuses to clobber a just-armed pending action (the one-slot #846 store is
shared with soft offers) — guarded TWO ways since #1753 (2026-09-12): the
`*_pending` intent_data flags cover ARM turns (the arming handler composes the
result and stamps its flag), and a read-only STORE PEEK (#1595) covers
STATE_QUESTION survival turns (#1739 §5a), whose result is composed by normal
processing with no flag — any entry present at apply time was armed or
survival-re-armed THIS turn (the store is popped before classification, #1529),
so the soft offer is skipped honestly instead of replacing the arm. Since #1770
(same day) the peek covers BOTH one-slot arm rails: the #846 store and the
#852/#1529 one-turn `last_offer` rail (where the #1769 resume survival
re-arms) — same soundness argument (`last_offer` is always-cleared at turn
start, before every apply-seam call site), one skip log naming the store
(`armed_store`); the canonical `offer_hint` write is first-arm-wins on the same
argument (a live rail entry was armed THIS turn — the hint skip is logged, the
#852 tracking unchanged on free turns). Regression:
`test_soft_offer_survival_clobber_1753.py` (store half),
`test_soft_offer_last_offer_clobber_1770.py` (rail half + no-over-block). **#1569 render half** (same commit): the floor's
`_format_domain_context` renders the two context families as visually distinct
sections with per-origin vocabulary instructions — `due_reminders` (from
`context:reminders:{user_id}`) says "reminder", `pending_todos` (from
`context:pending_todos:{user_id}`) gets a `PENDING TODOS (N)` section header and
says "todo"; mixed-origin turns instruct todo-list-first + a separate
"Also due:" reminder block, an item in both origins appearing in the reminder
block only. No new store, no schema change, no per-item data field.
**#1653 verb-answer anchoring + contract adoption (2026-09-12)**: the verb-question
answer turn shared the unanchored `\bdelete\b` claim #1650 fixed for the correction
window — with the verb question armed, a prose aside mentioning "delete" (PM's live
one-liner, under the #1631 floor) stored a wrong STICKY verb default and armed the
V3 confirm. The reminder_clear kind-specific turns now adopt the #1739 acceptance
contract: the seam consults `acceptance.evaluate_acceptance` at its declared axes
(`clarify_reminder_clear_verb` READ×PRIVATE → LOW_CEREMONY; arm-site's stored ask
threaded per #1665); a STATE_QUESTION verdict ("delete them?") falls through to the
generic seam's adopted READ branch — silent §5a re-arm, normal processing answers —
instead of being claimed as a verb answer. The verb CLAIMS are judged at their
TARGET action's axes: delete → `clear_reminders_delete` (DESTRUCTIVE×PRIVATE →
NAMED_OBJECT) takes the anchored `_CORRECTION_CLAIM_RE` crisp bar (same pattern
reused — no new extraction regex) + prose floor; complete → `complete_todo`
(WRITE×PRIVATE → LOW_CEREMONY) keeps word-level detection behind the prose floor.
The correction window gets the same axis-(a) gate. Echo-answers at the armed delete
confirm ("yes, delete them") remain deliberately non-firing (not crisp full-message
vocabulary; the pop stands — issue #1653 note 2, evidence-gated to change).
Regression: `test_reminder_clear_verb_anchor_1653.py`.
**#1696 explicit bulk delete (2026-09-12)**: the seam's `_EXPLICIT_VERB_RE`
decline (correct — an explicit verb isn't ambiguous) left 'delete my
reminders' with LESS capability than the ambiguous 'clear my reminders': it
dispatched the delete_todo rail, named no single target (every word is
command vocabulary — `_named_delete_target` → ""), and fell to
`handle_delete_todo`'s single-item which-todo ask. A SECOND seam in
`run_delete_todo_workflow`, AFTER the clear-family seam declines
(`reminder_clear.maybe_handle_explicit_bulk_delete`), claims the bulk shape —
plural domain noun (reminders / todos / to-dos / tasks), no todo number, no
named target, no exception clause (#1563's lane) — and arms the clear-family
flow's already-#1190-gated delete leg: targets resolved at OFFER time (the
noun scopes the set, #1569 — 'reminders' = reminder-dated rows, 'todos' = all
active), ids+texts bound, plain confirm copy ("Delete these N reminders?
(yes/no)" — no stored-preference framing; the user SAID delete, and the #1510
verb store is neither read nor written), "yes" dispatches
`clear_reminders_delete`. No verb vocabulary added: the delete_todo emission
is the verb evidence, so remove/erase/'get rid of' phrasings ride the same
seam. Companion: `_DELETE_COMMAND_NOISE` gains the bare quantifier "all"
('delete all my reminders' used to resolve 'all' as a NAMED target and
answer with the matching-"all" miss). Boundaries pinned both ways: #1605
keeps first claim on ambiguous shapes; singular unnamed 'delete my reminder'
keeps the which-todo ask; the #1527 named-target and #1666 numbered legs
unchanged. Regression: `test_bulk_delete_reminders_1696.py` + the updated
bulk pin in `test_reminder_delete_misroute_1527.py`.
**#1906 pick-target carrier (2026-09-30) — the ONE unarmed branch in
`reminder_clear.py` now arms.** PM live, test card session: a named-target ask
that matches zero or several candidates (`named_target_unmatched` — "clear the
overdue reminder" against candidates none of whom literally say "overdue")
rendered "tell me which one you mean" WITHOUT `set_pending_offer` — every OTHER
branch in the module arms. PM's pick ("Clear the first one.") had nothing to
bind to, re-classified as a fresh turn, and on alpha fell to the floor, which
improvised an unarmed yes/no ask outside the #1855 opener family; "Yes" found
nothing to execute. The branch now arms a FOURTH offer-only registry key,
`reminder_clear_pick_target` (kind `CLEAR_PICK_TARGET_KIND`, READ×PRIVATE →
LOW_CEREMONY, `action_triggered=False` — the surface-3 rail-scope denominator
stays unchanged), carrying the rendered candidate list (ids + texts, in
render order) plus each candidate's relevant due-ish timestamp (ISO, bound at
OFFER time — no fresh DB read on the answer turn). The answer binds
deterministically to exactly one candidate: an ordinal/positional reference
("the first one", "second", "#2", "1", "last"), a name/substring match against
the rendered texts, or an unambiguous status word ("the overdue one" — resolved
off the bound timestamps; skipped honestly, never guessed, when none or several
qualify). A bound answer re-enters `_act_on_resolved_targets` — extracted
verbatim from `maybe_handle_clear_family`'s post-resolution tail so there is
ONE source of truth for the three-variant decision tree, not a parallel copy —
with the single bound id/text, exactly the flow a matched name would have
reached (variant 1's either/or, variant 2's auto-apply, or variant 3's REAL
#1190 confirm). A bare "yes" (names nothing) falls through to the generic
seam's ACCEPT path, which dispatches the registered
`run_reminder_clear_pick_target_workflow` re-ask + re-arm (the
`clarify_reminder_clear_verb` idiom — never a blind bind); a decline falls
through to the honest `decline_message`; an unrelated command releases via the
SAME #1899 reads-only discriminator the reminder-task carrier uses
(`PreClassifier.pre_classify` surface 1 first, then `read_op_claims_turn`); a
SECOND consecutive unresolved/ambiguous answer re-asks once then releases
rather than looping. Regression: `test_reminder_clear_pick_target_1906.py`.
**#1769 resume-offer seam adoption (2026-09-12, #1739 epic 3)**: the #889
pre-classification resume check (`_check_pending_resume_offer`, the seam the
#1595 flip-1 note calls "resume check") decided accept/decline with FOUR
bespoke inline word-sets — a private acceptance vocabulary invisible to both
#1739 ratchet scans (no legacy detector call, no shared vocabulary name;
found by the #1766 census build). It now consults
`acceptance.evaluate_acceptance` at registry-declared axes
(`standup_interview` WRITE×PRIVATE → LOW_CEREMONY — accepting re-enters the
same flow that entry declares) with the arm-site's rendered ask threaded
(#1665: `LastOffer.offer_text` rides the pipeline into the seam as
`resume_offer_question`). The #1529 explicit-anytime commands became TAUGHT
vocabulary (`_RESUME_TAUGHT_*`, module constants) threaded into the
predicate — `taught_declines` added to `evaluate_acceptance` (full-message,
LOW tier only, symmetric with `taught_accepts`); with no offer pending the
seam consults the predicate DIFFERENTIALLY (taught-vs-bare verdicts) so only
flow-naming commands act unarmed — no local matcher survives, and the
standup-hijack pin holds. Contract axis (a): "yes?" / "resume?" never fire;
the armed STATE_QUESTION survives in the SILENT §5a form by re-arming the
one-turn `last_offer` rail (clobber residue filed on #1769 as #1770 and
discharged same day: the apply-seam guard now peeks this rail too, and the
canonical `offer_hint` write is first-arm-wins). Flow-exit ("end
standup") stays first and deterministic. NOT zero-widening (stated): the
legacy sets were exact-match, so the LOW-tier vocabulary (greedy residue
included) widens both surfaces while armed — pinned deliberately
(recoverable re-entry; inherits the CXO-owned tightening); "n"/"yea"
narrowed out. ARM half (#1766): the reentry offer already armed with its
rendered ask; the other two ask sites (`_start_standup_conversation`
session-exists ask, `_resume_suspended_standup` legacy either/or ask) now
arm via `_arm_resume_offer(question=…)` — both census rows shrank out.
Regression: `test_resume_offer_acceptance_1769.py`.

**#1762 capped-list remainder seam (2026-09-13, epic 6 first build) — a NEW
pre-classification deterministic seam, and the chain's first PERSISTING arm.**
Sits immediately after the #889 resume check and before classification, guarded
by `not contextual_offer_bound` (`_check_pending_list_remainder` in
`services/intent/intent_service.py`). It exists because the six GitHub listing
handlers (`_handle_list_{issues,prs,milestones,releases,labels,branches}_query`)
rendered `"...and N more"` — an honest SOURCE count they could not CASH, which
is GatherOutcome contract §5b's violation profile and, per the #1738 joint
invariant, real information loss inside the turn (whatever the render drops is,
from the model's own position next turn, information it never had).

RENDER half: all six now build the whole HELD set into lines and hand them to
one shared renderer, `services/intent_service/list_remainder.compose_capped_list`
— the renderer CONSUMES the gathered outcome and never rewrites it. Copy is
CXO's §5b-i: *"That's 5 of 340 — say the word and I'll pull the rest."* (what
you're holding, not what's missing); PPM's threshold skips the offer entirely
when the hidden tail is ≤3 and renders them all; a PAGED source (issues:
`total_count` 179 vs. a 50-item page) offers only what it can actually cash
rather than promising "the rest"; a source that caps its own count supplies
`source_total_display` so `1000+` prints as `1000+` and never as a fabricated
exact number.

ARM half: `_arm_list_remainder` stores the unrendered tail on
`ConversationContext.pending_list_remainder` — DELIBERATELY its own store, not
the #852/#1529 one-turn `last_offer` rail, because that rail's always-cleared-
at-turn-start invariant is exactly what makes the #1753/#1770 no-clobber peeks
sound. `session_id` reaches the six via `pass_session_id=True` on their
`_READ_QUERY_COHORT` entries (`_READ_QUERY_SESSION_THREADED` in
workflow_entries.py). The arm turn stamps `list_remainder_offer_pending`, which
joins `_apply_soft_offer`'s `_pending_flags` so no second offer competes on the
same turn; the STORE is deliberately NOT added to that method's store peek —
it lives up to 30 minutes and peeking it would suppress soft offers for the
whole window.

CONSUME half (#1739 adoption): the seam consults `evaluate_acceptance` at the
arming actions' registry-declared axes (all six declare `EffectClass.READ`,
PRIVATE → LOW_CEREMONY) with the stored offer threaded as the armed ask
(#1665). The offer's own copy TEACHES "the rest" via `taught_accepts`, additive
over the shared vocabulary so a bare "yes" still cashes — §5b-i decision 2:
offer the affordance, never the syntax. ⭐ **Arm survival is the NON-default
PERSISTING form, stated**: STATE_QUESTION *and* PASS both leave the remainder
standing, across arbitrary intervening turns, because a capped-list offer is
precisely the kind users answer LATE (CXO) — an acceptance test of
"immediate next turn asks" passes without exercising the property that fails.
CXO's per-tier ruling licenses it (READ arms may survive; only CONFIRM must
not) and nothing can FIRE from it: cashing prints lines already gathered.
Bounded by cashed / declined / replaced by a newer capped list / stale past
`REMAINDER_MAX_AGE_MINUTES` (30, borrowed from `ConversationContext.max_age_
minutes`). A gone-or-stale remainder returns the honest `list_remainder_moved`
turn — *the list has moved on, ask me again and I'll pull a fresh one* — and
NEVER a silent re-fetch, which would be a fabrication of continuity (the user
believes they hold items 6–340 of the list they saw). No GitHub surface is
touched anywhere on the consume path; that is structural, pinned by explosive
adapter/router stubs on both the cash and stale paths. Honest boundary pinned
rather than papered over: contract axis (a) makes an interrogative REQUEST
("can I see the rest?") a STATE_QUESTION, not an accept — the arm survives and
normal processing answers, but the CONTRACT is where that would change.
Regression: `test_cashable_list_remainder_1762.py`.

**#1855 ask-only-when-armed, enforced at the FLOOR'S OUTPUT SEAM (2026-09-23,
Lead design / Arch ruling; layer 1 of 2)** — surface 4's reply text now passes a
contract check before it becomes user copy. CXO's sentence: *the floor may
SUGGEST an action in the imperative, but may only ASK "want me to X?" when X is
armed this turn.* PM live 2026-09-23, twice: the floor composed *"Want me to add
'One Job' with the Design-in-Product/one-job repo to your projects now?"*, PM
answered *"Yes, please."*, and nothing was armed — the floor's LLM prose is the
one producer of offers that touches NEITHER arming rail (the #846 one-slot store
and the #852/#1529 `last_offer` rail), so the acceptance predicate correctly
refused to bind (#1694 (b)) and the honest no-result fallback fired. The
predicate's exactly-armed rule is the right half; the OFFER was the lie, and the
fix is producer-side. This also closes at RUNTIME the gap
`TestUnarmedAskSiteRatchet` (#1766) names as its own boundary — *"above all LLM
FREE TEXT — the conversational floor can generate a question in prose at runtime;
no static census can see it… Present, not Enforced."*
`ConversationalFloor.respond()` is the SINGLE seam (all four floor doors —
ethics-denial, `_handle_floor_with_context`, guidance, `_handle_unknown_intent` —
return through it); the check runs LAST, after `strip_scaffolding_artifacts` /
`strip_placeholder_slots` / `_maybe_append_push`, so it covers the whole reply
rather than the LLM's half. DETECT (`services/intent_service/unarmed_offer.py`):
the narrow anchored family `Want me to …?` / `Would you like me to …?` /
`Should I …?` / `Shall I …?`, opener sentence-initial + sentence-final `?`, the
ratchet's literal-scanning discipline — imperatives and non-offer questions
("What's the repo?") don't match, and neighbours like "Do you want me to …?" are
deliberately uncovered (widening is a reviewed decision, not a patch). ARMED is
read by `IntentService._armed_offer_signal` and threaded as
`FloorContext.armed_offer`: the #846 store via `peek_pending_offer` and the
`last_offer` rail via `_peek_last_offer` — both sound for the same
popped/cleared-before-classification reason `_apply_soft_offer`'s no-clobber
guard is (#1753/#1770). ⚠️ The third signal, `interview_offer_accepted` (#1837),
is NOT readable here and structurally need not be: it lives in
`StandupConversation.context` and an active standup is claimed by the process
registry above classification, so those turns never reach the floor; what is live
while a floor turn can still run is the standup *invitation*, which arms through
the #846 store. `armed_offer=None` is the FAIL-SAFE default — a door that proves
no arm degrades a question into a suggestion; the opposite default would
reinstate the defect. REWRITE, three tiers, never a bare deletion: a catalogued
action whose slots bind AND round-trip through #1856's real
`extract_add_project_slots` → *"To do that, say: add project One Job with repo
Design-in-Product/one-job."*; family recognised but slots unbound → the bracket
template the app already teaches (`add project [name] with repo [owner/repo]`,
kept byte-identical to `CanonicalHandlers._ADD_PROJECT_IMPERATIVE`, drift pinned
by test); uncatalogued → *"If you'd like me to <action>, just tell me
directly."* — names the action, suggests no command string we have not verified
parses (#1108). The round-trip gate is what keeps tier 1 from recommending a
known-failing action. Every rewrite logs `floor_unarmed_offer_rewritten` with the
ORIGINAL sentence into #1595's corpus sink, so the rewrite cannot silently absorb
the evidence of how often the floor does this. Same change: the never-built
reserved `LastOffer.offer_type` value was DELETED rather than built (Arch:
never instantiated, never set, never checked — building the adapter would create
a SECOND independently-truthful answer to "is anything armed this turn"; one
authority, not two).
Regression: `tests/unit/services/intent_service/test_floor_unarmed_offer_seam_1855.py`.

**#1855 LAYER 2 — the floor ARMS what it offers (2026-09-24, Lead design / Arch
ruling on both mechanism questions)** — the other half of CXO's sentence: the
floor may ASK when X *is* armed this turn. `enforce_armed_offers` gains a THIRD
outcome beside pass/rewrite — **arm** — taken only when (i) tier 1 BINDS a
command (catalogued family + slots from the floor's OWN sentence + round-trip
through the real `extract_add_project_slots`), (ii) nothing is armed this turn,
(iii) exactly one offer-question is present (the #846 store is one slot; a
two-question reply makes "which one did yes bind to?" ambiguous, so it is
rewritten rather than half-armed), and (iv) the caller passed an **arming
callback**. `IntentService._floor_arming_callback(session_id, user_id)` builds
it and all FOUR floor doors thread it as `FloorContext.arm_offer`; it returns
None when the #846 store is unreadable, and **a door that passes no callback is
layer 1 byte-for-byte — that is the rollback switch.** Every failure mode falls
back to the rewrite (no bind, callback refuses, callback raises): an offer that
could not be armed must never stand as a question. The record is the #1190
carrier's own shape — `workflow_type=confirm_pending_action`, `question` = the
rendered ask verbatim (#1665 — the key the accept seam threads into
`evaluate_acceptance`; `offer_message`/`ask_rendered` mirror it), and
`pending_action = {kind: "floor_bound_offer", command: "add project One Job with
repo Design-in-Product/one-job", action: "add_project", summary}`. **The BINDING
is the command STRING, not a parsed guess**: on a crisp accept
`run_confirm_pending_action_workflow` re-runs that text through the ordinary
rail, so the action executes by exactly the path the user would have taken by
typing it — no second implementation of add-project anywhere. It calls
`_process_intent_internal`, **not** `process_intent`, deliberately: the public
wrapper records the message it is given as a USER TURN (#563/#1122), so
re-running the command through it would write a sentence the user never typed
into the durable transcript and save the reply twice. ⚠️ Consequence, and it
constrains the catalogue: the `destructive_confirmed` marker cannot ride a text
re-run (there is no Intent to stamp before classification), so **only families
whose handler executes from an explicit imperative may be armed this way** —
EXECUTE framing is PROCEED at the #1509 consent gate, which is why add-project
completes in one turn. Acceptance is at the carrier's REGISTRY-DECLARED axes
(`confirm_pending_action`: DESTRUCTIVE×PRIVATE → NAMED_OBJECT, crisp
full-message affirmatives only) — deliberately NOT per-pending-action axes:
threading add-project's own WRITE×PRIVATE would drop this arm to LOW_CEREMONY,
whose vocabulary still carries the #1631 greedy rows, so the floor-bound offer
takes the STRICTER bar exactly as every other kind on this carrier does.
`floor_bound_offer` joins `_CONFIRM_KINDS` (#1664) — the question is literally a
yes/no and a crisp accept fires the bound command — and the offer seam names its
abandonment `floor_bound_offer_abandoned`; decline/off-intent are the existing
#1529 semantics, nothing new. Question COPY is a one-line switch pending CXO:
`unarmed_offer.ARMED_QUESTION_FORM` is `None` (the model's own question stands)
or a `{command}` format string the seam substitutes before arming — either way
the STORED ask is what the user actually read. `revise_draft()` gets the
DETECTOR ONLY, log-only (`floor_offer_in_revise_draft`): its output is a draft
artifact, not chat copy, and rewriting it would edit the user's document.
Regression: `tests/unit/services/intent_service/test_floor_armed_offer_layer2_1855.py`
— including the two-turn PM fixture through the real rail (explosive classifier
LLM; the add-project handler patched only at its DB seam) and a catalogue
denominator pin asserting the catalogue is exactly the round-trip-tested set.

**#1763 the multi-intent branch orchestrates only an ALL-CANONICAL plan
(2026-09-24, Lead design) — a gate on surface 3's sibling of the chain, not a
new surface.** `process_intent`'s #764 multi-substantive branch dispatched every
≥2-substantive plan into `IntentOrchestrator`, which executes each sibling
through `CanonicalHandlers` alone. But `can_handle` accepts only TEMPORAL /
GUIDANCE / PORTFOLIO / CONVERSATION / PROVENANCE (canonical_handlers.py:141-157;
STATUS and PRIORITY left that set when #925 Phase 3 floor-routed them, and #1877
corrected the registry to say so), so **every floor-routed sibling —
STATUS, PRIORITY, IDENTITY, DISCOVERY, TRUST, MEMORY, QUERY, ANALYSIS — came
back `success=False, error="No handler for category: …"` DETERMINISTICALLY**: no
exception, no handler invocation, no data touched, nothing tried. The failure is
then rendered by `_aggregate_messages` as *"I wasn't able to check on project
status right now — ask me again and I'll retry"* — the false-retry-promise shape
#1198 forbids, since retrying reproduces it byte-for-byte — or, when EVERY
sibling is floor-routed, as the blanket *"I'm having trouble processing that
right now."* #1738's subsumption removed the phantom STATUS sibling that made
this fire on archived-list turns, so the *occasion* PM hit is gone; the
*mechanism* was live for any genuine two-topic ask naming a floor-routed topic.
THE GATE: the branch partitions the substantive siblings up front with
`IntentService._is_orchestratable_sibling`, which is **the single-intent path's
own predicate pair in the same order** — `not _should_route_to_floor(i) and
canonical_handlers.can_handle(i)` (intent_service.py ~2542/2567) — so the two
paths can never disagree about where a given intent belongs. ⚠️
`_requires_canonical_handler` alone is NOT that predicate: it returns False for
PROVENANCE, which the single path still routes canonically because PROVENANCE is
absent from `_FLOOR_ROUTED_CATEGORIES`; a "simplification" to the single gate
would silently strand a canonical category on the floor (pinned by test). A
predicate that raises returns False — the floor is the safe default. Orchestration
runs only when the floor-routed partition is EMPTY and there are still ≥2
substantive siblings. OTHERWISE the branch **skips orchestration entirely** and
falls into the ordinary single-intent path with the FIRST floor-routed sibling as
`intent`: surface 4 is a whole-message surface, so it receives the user's entire
message plus its category's domain context and answers both topics from the layer
that actually holds the data. The rider becomes **structurally unreachable** — no
failed `IntentExecutionResult` is ever produced — rather than merely unlikely.
The orchestrator's own code path is untouched for the all-canonical case, and
deliberately gains NO floor leg: the floor is a whole-message surface and a
per-sibling floor call inside a plan would compose N partial answers to one
message. Because the floor reads `FloorContext.user_message` from
`intent.original_message or intent.context["original_message"]`, the skip
backfills the whole message onto the chosen sibling when a classification surface
bound neither (fill-only; a surface's own binding always wins) — without it the
floor would compose against an EMPTY message, trading one silent loss for
another. The decision logs `multi_intent_orchestration_skipped` with `reason`
(`floor_routed_sibling` / `no_canonical_sibling`), the substantive /
floor-routed / orchestratable category lists, and the chosen intent, so a live
transcript is readable against it. No new `elif intent.action` site (the #1124
ratchet is untouched; this branches on categories, not actions). Regression:
`tests/unit/services/intent_service/test_multi_intent_floor_sibling_1763.py`.
⚠️ Same commit, and the reason this survived a green suite for months: the #764
suite's orchestrated cases used STATUS/PRIORITY siblings with `can_handle`
mocked True — a configuration that cannot occur in production, so the tests
measured the branch's plumbing and never the registry it dispatches against
(m-43). Those cases now use categories canonical on BOTH sides (TEMPORAL,
PORTFOLIO), and the new suite reads the REAL `CanonicalHandlers`.

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
⚠️ **Since #1668 (2026-08-21) this observer has TWO modes** — the description
above is the LEGACY-ROUTED one, unchanged. On a turn the live inversion routed,
it runs the legacy counterfactual instead; see the #1668 block below.
Corpus-side instrument: `scripts/inversion_phase1_shadow_score.py` scores the
router against `tests/fixtures/inversion_corpus_phase0.yaml` per category vs
the Phase-0 full-chain baseline (first run:
`inversion-phase1-shadow-score-2026-08-14.md`). The Phase-2 flip (per-category,
queries first) is the reviewed commit that relaxes the boundary test — until
then this observer changes NO routing behavior.

**#1595 Phase 2.0 SessionSnapshot (2026-08-19) — the conversational state the
router has never seen, shadow-fed first.** Two sibling modules:
`services/intent_service/session_snapshot.py` (the Lead-authored CONTRACT —
frozen dataclass, `serialize_for_prompt` with a golden-pinned deterministic
rendering, ≤1800-char cap; five contract items in its docstring: read-only,
<10ms, fail-open per field, bounded serialization, no user prose beyond
labeled slots) and `services/intent_service/snapshot_assembly.py`
(`assemble_session_snapshot(session_id, user_id, intent_service)` — populates
every field from the REAL stores, never raises, never writes). The reads:
`WorkflowOfferService.peek_pending_offer` (the #846 one-slot store, observer
peek — the production pop seam is untouched), `ProcessRegistry.first_active_type`
(`any_active`'s loop returning WHICH type; the lazy-timeout housekeeping in
the adapters is an accepted convergent side effect, documented on the method),
the #1394 ledger head via `services/intent_service/session_activity_read.py`
(the query extracted to ONE shared home — `classifier._resolve_issue_referent`
now calls the same `list_session_activities`/`issue_head` instead of its two
inline copies), `collaboration_gate.read_declared_working_mode` (the DECLARED
#1510 mode or None — deliberately NOT `get_working_mode`, whose collaborate
default would fabricate a declaration), and the #1605 per-verb default via
`get_verified_inference(user_id, inference_key("clear"))`. The four awaited
reads run gathered (measured 2.4ms median / 2.7ms p90 on real Postgres).
Wiring is SHADOW-ONLY: `process_intent`'s existing post-turn call site
assembles the snapshot iff `shadow_enabled()` and passes it to
`maybe_schedule_shadow_check(snapshot=...)`; the shadow task serializes it
via `serialize_for_prompt` into the routing prompt's `Session state:` block
(the router-side `SessionSnapshot.state_block` field). Live routing is
byte-identical with the flag on/off (pinned in
`tests/unit/services/intent_service/test_snapshot_assembly_1595.py`, which
also pins idempotence — assemble twice, the offer still pops — fail-open
field naming, and the golden serialization string). Phase 2.2 (threading the
snapshot into the LIVE constrained routing call, pre-classification state) is
a separate reviewed flip; the floor and handlers must never read routing
context from the snapshot (one-direction dependency, per the contract).
**#1595 Phase 2.2 flip-1 (2026-08-19) — the LIVE inversion consult, per-category
and DEFAULT-EMPTY.** A new consult seam in `_process_intent_internal` sits AFTER
every deterministic pre-classification surface (the #846 pop seam, contextual
offer binding, the guided-process claim, resume check, /standup + standup-query
deterministic routes, ethics) and IMMEDIATELY BEFORE the `classify_multiple`
block. When `PIPER_INVERSION_LIVE_CATEGORIES` is set (comma-separated
ACTION_REGISTRY category names; **unset/empty = the consult returns None with
zero work — routing byte-identical to the pre-flip chain; revert = unset**),
an UNARMED turn runs ONE constrained routing call
(`services/intent_service/inversion_live.py::consult_inversion_live`, the sole
sanctioned live consumer of the router — named-allowlist amendment in
`TestInversionShadowNoExecutionBoundary`). The consult returns a fully-formed
`Intent` ONLY when ALL of: decision outcome is `operation`; the operation's
registry category (alias-resolved via the registry-derived grammar) ∈ the live
set; confidence ≥ `PIPER_INVERSION_LIVE_MIN_CONFIDENCE` (default 0.8); AND the
operation is a rail key whose declared effect is `EffectClass.READ` (load-bearing,
not belt: ACTION_REGISTRY files `create_issue` WRITE and `close_issue`
DESTRUCTIVE under QUERY — a write can never flip via this seam regardless of
config; **amended 2026-08-28 by #1677 — read the named-WRITE allowlist entry
below before relying on that last clause: an UNALLOWLISTED write can never
flip, and the allowlist holds exactly one individually verified operation**).
That Intent then flows into the SAME surface-3 rail dispatch a
classified intent uses — the router chooses the key; the rail, consent gates,
and handlers are untouched (no new dispatch site; the #1124 ratchet is
unchanged at 0). EVERY other outcome — armed turn (offer popped this turn,
bound contextual offer, or snapshot-armed: pending offer / active process /
draft-in-compose — flip-1 scope is ZERO-armed-state per the #1663 addendum;
the seam-consumption amendment builds with the first armed-capable flip),
REFUSED, transport error, NONE/CLARIFY, sub-threshold, off-set category,
non-rail or non-READ operation — falls through to the legacy chain below
UNCHANGED, each with its own reason on the ONE structured
`inversion_live_decision` telemetry line (route, operation, category,
confidence, threshold, snapshot presence + field errors, utterance sha).
⚠️ **The seam is WHOLE-MESSAGE, and that had a live defect — #1896, fixed
2026-09-25, then narrowed by unit 4 (see the unit-4 block below).** A live
route REPLACES the entire `classify_multiple` block, so on a turn surface 1
would SPLIT ("what are my todos and what time is it") the router's ONE
operation answered one half and the other half was silently DROPPED. Latent
while every wave was dark; armed the moment `read_status` went live. The
consult now runs the SAME deterministic splitter first (no LLM, no new
pattern) and stands down on `_n > 1` with reason
`multi_intent_split_stand_down`. **Since #1595 unit 4 (2026-09-26) that
stand-down is the ENTRY POINT to the sibling path rather than the end of the
turn** — it publishes its provenance (`routed_live=False`, the same #1668
observer branch as no record at all), and the dispatch layer reads that
reason to decide whether to split and route the halves. When the sibling path
declines, the stand-down is exactly what it was.
Flip-1's disagreement telemetry compares against the DETERMINISTIC legacy
counterfactual only — `PreClassifier.pre_classify` (surface 1), no second LLM
call; a phrase surface 1 wouldn't claim compares as incomparable (None) and
the standing post-turn shadow observer remains the deep comparison. The
router call carries the PRE-classification Phase-2.0 SessionSnapshot
(assembled at the consult, serialized via the golden-pinned renderer) — the
threading Phase 2.0's shadow wiring deferred. An inversion failure of any
shape never breaks the turn: `route()` returns honest REFUSED/error decisions,
and the call site belt-catches with a loud `inversion_live_consult_failed`
error log before running the legacy chain. Pins:
`tests/unit/services/intent_service/test_inversion_live_1595.py`
(default-empty zero-work + e2e, same-handler-result e2e with the classifier
consult explosive, armed guards incl. armed+in-set-category e2e, all
fallthrough reasons incl. the WRITE-in-QUERY pin, error-path e2e,
divergence telemetry). Coverage note (flip-1 as shipped; **superseded by
#1667 below** — kept for the fall-through structure it records; the not-live
bucket names were renamed by #1670, mapping note in
`inversion-phase2-gate-2026-08-19.md`): rail READ ops with no ACTION_REGISTRY
category (`show_standup`, `list_projects`, the analysis family) were outside
the category flag's addressable space and fall through with reason
`not_live_uncategorized` (carried a different name pre-#1670); registry-only
canonicals (`get_identity`, `get_project_status`) fall through
`not_rail_dispatchable`.

**#1667 flip UNIT on the rail entry (2026-08-20) — the flag widens, the four
dispatch conditions do not.** Flip-1's flag keyed on ACTION_REGISTRY
categories, and the measurement that forced this change is that the category
addressed **33 of 93** rail READ keys — 60 had no registry category at all, so
most of wave 1 was not expressible in the flag meant to express it. (The #1667
issue and the kickoff decision cite **23 of 93**; that is the same fact counted
against ACTION_REGISTRY's *direct* action names, while `inversion_live.
_category_by_operation` also back-maps through `grammar.alias_to_canonical`.
Both numbers are printed side by side in `--audit` so nobody has to reconcile
them from memory. The conclusion is identical either way.) The rejected fix was
bulk-registering 70 ops into ACTION_REGISTRY — that registry holds canonical
action vocabulary, not routing policy. **The flip unit is now declared on the
rail entry**: `WorkflowEntry.flip_group: Optional[str]`, beside `effect` and
`outwardness` (the #1509 precedent — declare on the entry, derive everything
else), each assignment carrying its reasoning in the comment above it.
Wave-1 groups: **`read_status`** (status/listing/identity — zero armed state,
no referent, no time expression), **`read_referent`** (issue/PR detail + the
analysis family — the #1641 repo ask makes the referent real), **`read_synthesis`**
(the summarize family only; PA's issue/commit shapes join it when built).
**Wave 2 (#1595 epic-0 scope doc, 2026-09-25): `read_temporal`** — reads whose
answer is a time window the user expressed or implied (what changed since X,
my week, meeting load, recurring meetings); the changes_query alias family (4
rail keys) + the calendar cohort (9 rail keys, `_CALENDAR_QUERY_FLIP_GROUPS` in
`workflow_entries.py`, mirroring `_READ_QUERY_FLIP_GROUPS`'s own-map shape).
Held out of wave 1 because time faces were unowned (kickoff §2.2 puts temporal
last among queries); #1887 (2026-09-24) gave the product one timezone
resolver, which is what changed. Grouping only in this unit — the flag itself
stays unset pending a per-category shadow-score budget (PM-gated, epic-0 scope
doc).

**Wave 3 (#1595 epic-0 scope doc, 2026-09-25): `read_strategic`** — the last 8
ungrouped READ rail keys (strategic_planning/create_plan, learn_pattern/
detect_pattern, prioritize/set_priorities, generate_content/create_content):
reads that produce a plan, a priority ordering, a pattern, or generated
content over the user's own material, with nothing written anywhere.
Deliberately not folded into wave 1's three classes when #1667 built them —
grouping them then would have redefined those names (each entry's own
comment says so at the time). They get their own group now so the ungrouped
READ list reaches zero (`scripts/inversion_phase2_gate.py --audit`: 93/93
grouped) — the honest "reads done" line for epic 0. Grouping only, same as
wave 2 — the flag stays unset for this group pending its own shadow-score
budget.

`PIPER_INVERSION_LIVE_CATEGORIES` **keeps its name** and now accepts **a group
name, an individual operation name, or a registry category** — a wave flips by
naming its group, a surgical experiment by naming one op, and every flip-1
deploy string keeps its exact meaning. Default-empty still means fully dark
(zero work, no log line). The four dispatch conditions are UNCHANGED — this
widened *what can be named*, never what happens once named: the armed-turn
guard, the confidence threshold, and the declared-READ rail-entry guard all
hold as before. **A non-READ entry carrying a `flip_group` is now
unconstructible** (`WorkflowEntry.__post_init__` raises, as it does for an
unknown group name), so the group surface cannot introduce a write even in
principle (amended 2026-08-28 by #1677: unless it declares an allowlisted
`flip_write_allowlist_key` — see that entry; no allowlisted op carries a
group today, so no wave sweeps a write in); the runtime effect check remains the belt and the only guard for the
category and operation-name surfaces. Two honesty properties worth knowing
before flipping: the decision line logs **`live_match`** (`operation`/`group`/
`category`/`None`) and `flip_group`, so a live route traces back to the flag
token that caused it, plus `unrecognized_flag_tokens` so a typo'd wave name is
loud rather than a silent no-op; and **"ungrouped" does not mean "unreachable"**
— an ungrouped op that carries a registry category is still swept in when that
category is named (`week_calendar` under QUERY, pinned). Ops with no group are
unaddressable by any WAVE, by design, until someone assigns one; the deliberate
wave-1 holds are the temporal class (`changes_query` + the calendar cohort —
kickoff §2.2 puts temporal last), and `strategic_planning` / `learn_pattern` /
`prioritize` / `generate_content` (not one of wave 1's three classes; grouping
them would redefine the group names). `scripts/inversion_phase2_gate.py --audit`
(no LLM, a registry read) prints the coverage table with denominators, lists
every unassigned op BY NAME split into "reachable only by naming the op" vs
"still swept by its category", and re-measures the READ-only invariant rather
than asserting it. Pins: `tests/unit/services/intent_service/
test_inversion_flip_groups_1667.py` (unconstructible non-READ group, closed
group vocabulary, each of the three naming surfaces live e2e, ungrouped-op
never dispatches while its group-mates are live, single-op flip does not sweep
its group, default-empty dark, audit lists the unassigned).

**#1668 the shadow observer's SECOND mode — the legacy counterfactual
(2026-08-21).** With both flags on, a turn routed LIVE by the inversion that
was also sampled by the shadow used to have its utterance re-routed through the
SAME constrained router: a redundant Haiku-class call whose only finding was
self-agreement. That call is repurposed, not deleted. **Branch:**
`inversion_shadow.maybe_schedule_shadow_check` now takes `live_route`, this
turn's routing provenance, and picks the mode from it — `routed_live` True →
`_legacy_counterfactual_check`; anything else (no provenance, `routed_live`
False) → `_shadow_check`, **byte-identical to before** (the existing shadow
pins pass unchanged). The provenance is **published by the consult itself**
(`inversion_live.LiveRouteProvenance` in a per-turn `ContextVar`, taken via
`consume_live_route_provenance()` inside `process_intent`'s existing
`shadow_enabled()` gate and passed to the observer as a kwarg) — nothing
re-derives how a turn was routed, and the record is one-shot plus cleared at
every consult entry, so it cannot leak into a later turn sharing the Task.
**What the counterfactual measures, and what it does not (m-43).** It runs the
legacy chain's legs in the legacy chain's order, short-circuiting the way that
chain short-circuits: `multi_intent_rules`
(`PreClassifier.detect_multiple_intents`) → `pre_classifier`
(`PreClassifier.pre_classify`) → `llm_classifier`
(`IntentClassifier.classify`, reached ONLY when both deterministic legs
decline). The LLM leg is called **unscoped** (no `user_id` / `session_id` /
`context`) and **uncached** (`use_cache=False`), so a post-turn observer
performs no owner-scoped ledger read and can never write the production
classifier cache. The legs that therefore do NOT run are named on every line in
`legacy_legs_not_run` — B3 referent resolution, the classifier cache,
the ADR-075 D4 identity-scoped system prompt, #278 graph context, #248
preference hooks — beside `legacy_legs_run` (what actually executed) and the
`layer_note`: *this line reports the unscoped, uncached, single-intent legacy
route, not the full production `classify_multiple` call.* **Cost never grows**:
the counterfactual REPLACES the re-route rather than joining it, and spends
**0** LLM calls when a deterministic leg claims, **1** when both decline —
never more than the single router call it replaced, and strictly fewer on
deterministically-claimed turns. **Telemetry** is a distinct event family so a
counterfactual row can never be mistaken for a router-shadow row:
`shadow_legacy_counterfactual_agreement` / `_disagreement` / `_incomparable`,
carrying `mode`, the live route + `live_match` + `live_confidence`, the legacy
label + which leg decided it, per-leg errors, `legacy_llm_calls`, snapshot
presence + field errors, and alias-resolved `agreement`. Absence of a legacy
answer scores **incomparable, never disagreement** (m-44). Every leg is
individually error-caught: a broken leg degrades the line and is recorded in
`legacy_leg_errors`, never failing the (already-completed) turn. Default-OFF is
untouched — shadow flag off ⇒ no task, no provenance read, nothing. Pins:
`tests/unit/services/intent_service/test_inversion_counterfactual_1668.py`
(mode branching with the router explosive on the counterfactual path, leg
honesty, the ≤1-call cost ceiling, agree/disagree/incomparable, exploding legs,
provenance one-shot + stale-clear + publish-on-dispatch-and-fall-through).

**#1677 the first NAMED WRITE may flip — via an allowlist, not a relaxed
effect check (2026-08-28, PM chose this over three classifier/pre-classifier
options; mechanism ruled by Arch 2026-08-25).** The defect: "add todo …" has
no deterministic pre-classifier claim, so every todo-create turn rides the LLM
classifier, whose prompt teaches `create_ticket` by example and has no
`create_todo` example — `add todo buy oat milk` drew `create_ticket` 2/3 and
`Add a todo: P1GT-life-<hex>` 1/3 (measured 2026-08-22, cache off). The fix
routes the shape through the successor system instead of patching surface 2.
**The guard did NOT become `READ or WRITE`.** That check is what caught
`create_issue` filed under `QUERY` in ACTION_REGISTRY, and relaxing the class
would drop that protection for every future write at once. Instead both
enforcement points now accept `EffectClass.READ` **or** an entry that declares
a `flip_write_allowlist_key` present in `workflow_dispatcher.FLIP_WRITE_ALLOWLIST`
(today: exactly `{"create_todo"}`) — the shared predicate is
`workflow_dispatcher.flip_write_allowed`, consulted by *both*
`WorkflowEntry.__post_init__` (structural) and `inversion_live.
_effect_guard_passes` (runtime); they were changed in one commit because
relaxing one and not the other leaves a gap between what is checked and what
is enforced. The runtime half additionally requires the **routed operation
name** to BE the declared key (or canonicalize to it): one entry object serves
the whole `create_todo`/`add_todo`/`new_todo` alias family, so the declaration
says "this entry was reviewed", not "this name was". **Every allowlist entry
owes three verifications, re-run and not cited** (Arch): registered on the rail
(`action_triggered`), declared `EffectClass` confirmed by *reading the
handler's behavior* — `handle_create_todo` persists one row via
`todo_service.create_todo` and deletes nothing ⇒ WRITE, never DESTRUCTIVE —
and confirmed to reach `consent_gate.evaluate_consent` on the shared rail
(`needs_consent` derives True; PRIVATE × WRITE × execute framing = PROCEED, so
evaluation without ceremony). The conditions are written beside the constant,
and a test asserts the comment still carries them. Two consequences worth
knowing **before** the flag goes on: (1) `create_todo` carries **no
`flip_group`** — no wave sweeps a write in — but it *does* carry registry
category `EXECUTION`, so **flipping the `EXECUTION` category token flips this
write too**; the allowlist bounds *which writes*, never *which surface*
(pinned, and now printed by `--audit`, whose READ-only-invariant section would
otherwise read as "no write can flip"). (2) An allowlisted write with **no**
registry category takes legacy under a new `allowlisted_write_uncategorized`
reason rather than the `IntentCategory.QUERY` fall-through, which would be a
lie about a write in the Intent itself (no op is in that state today). Pins:
`tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py`
(allowlist constant + its comment, unallowlisted WRITE/DESTRUCTIVE still
unconstructible with a group and still refused at dispatch when named
directly, allowlisted-but-unnamed stays legacy, category surface reaches it,
sub-threshold still blocks, default-empty still byte-identically dark, the
flipped turn reaches the same rail handler and writes the row with the consent
gate spied, and the #1677 defect phrasings route to `create_todo`).
⚠️ Layer honesty (m-43): those routing pins use a deterministic router fake, so
they prove the *path*, not the *draw distribution* — the one non-faked
structural fact is that `create_ticket` is not in the router's grammar at all
(it canonicalizes to `create_issue`), so the classifier's specific failure
output is unavailable to the constrained router. Real improvement is
observable only live, in `inversion_live_decision` telemetry.

`create_reminder` allowlisted 2026-09-25 (#1595 unit 3, for #1559) — the
second named write on the same mechanism, not a relaxed check; three
conditions re-run against the handler as it exists today (not cited from
#1560/#1685), no `flip_group`, flag unset. Pins:
`tests/unit/services/intent_service/test_inversion_write_allowlist_create_reminder_1559.py`.

`delete_todo` allowlisted 2026-09-25 (#1595 unit 3b, for #1606) — the FIRST
DESTRUCTIVE entry on the allowlist, per Arch's floor ruling the same day:
"#1677's 'WRITE' was never a categorical ceiling — extend the allowlist to
a DESTRUCTIVE op, individually verified, same as create_todo/create_reminder
were." `delete_todo` is the operation the live constrained router actually
draws for #1606's corpus phrasing (2026-09-25 shadow score: "please clear
the reminders except for 'Review the PR'" → `delete_todo` @0.9; "delete my
hydrate reminder" → `delete_todo` @0.9). Arch's three conditions re-run
against the handler as it exists today (not cited from #1666's ruling), no
`flip_group`, flag unset. Arch's one ADDITIONAL build-time condition for a
DESTRUCTIVE flip — the rendered confirm prompt must pull its identifying
detail from the SAME slot-extraction path the legacy dispatch uses, never a
differently-shaped inversion-specific confirm — is proven, not assumed: the
#1190 gate (`intent_service.py`'s consent block →
`build_todo_delete_confirmation`) is the SAME entry-agnostic code regardless
of which router produced the Intent (`consult_inversion_live` REPLACES the
classifier draw for the turn; one `intent` variable flows into the rail),
and `build_todo_delete_confirmation` resolves its title from
`intent.original_message`/`intent.context["original_message"]`, which both
routers set to the identical raw user text. Two tests build the SAME
message through each provenance and compare the rendered confirm strings
for equality (both render `'Delete todo: "hydrate"? (yes/no)'`). Pins:
`tests/unit/services/intent_service/test_inversion_write_allowlist_delete_todo_1606.py`
(`TestConfirmProvenanceParity` for the provenance proof).

`set_default_repo` allowlisted 2026-09-27 (#1595 unit 3c, for #1606's
set-default-repo half — the OTHER half of #1606's corpus row, closed
separately from `delete_todo` above). The fourth named write on the
allowlist, via the same #1677 mechanism, not a relaxed check; three
conditions re-run against the handler as it exists today (not cited from
#1327's original ruling): (1) registered — `get_action_workflows()
["set_default_repo"]` exists, `action_triggered=True`, no alias family (the
pre-classifier's `SET_DEFAULT_REPO_PATTERNS` emits the literal action string
directly, and it's the same name `derive_routing_grammar()` and
ACTION_REGISTRY both use — `("QUERY", "set_default_repo")`,
action_registry.py:150); (2) effect correct by behavior —
`_handle_set_default_repo` calls `ConnectorConfigService.set_default_repo`,
which upserts one key into the owner's github config blob, preserving other
keys, deleting nothing → WRITE, never DESTRUCTIVE (overwritable, same as
`set_timezone`'s precedent); (3) reaches consent — the same entry-agnostic
rail block the other three named writes use evaluates it. No `flip_group`,
flag unset. ⚠️ **UNLIKE its three EXECUTION-category siblings,
`set_default_repo`'s ACTION_REGISTRY category is `QUERY`** — flip-1's own
original, and by far the broadest, category on the rail — so naming the raw
category token `QUERY` (not a `read_*` wave; no wave sweeps a write in)
sweeps this write in too, exactly as naming `EXECUTION` does for
create_todo/create_reminder/delete_todo. `--audit`'s NAMED-WRITE ALLOWLIST
line now prints all four keys. ⚠️ **Discovered work, filed not fixed here
(#1898)**: `_handle_set_default_repo` reads its repo argument from
`intent.context.get("original_message", "")` only — it does not fall back
to `Intent.original_message` the way `handle_create_reminder`/
`handle_delete_todo` do. `consult_inversion_live` sets `original_message` on
the Intent's TOP-LEVEL field only (context carries just
`inversion_live`/`inversion_args`), so a flipped turn reaches the handler
and the consent gate fires correctly (proven live, independent of #1898),
but the handler itself cannot see the repo the user named and answers the
graceful bad-shape nudge instead of writing the row — verified behaviorally
by direct call, not assumed. The allowlist entry is still structurally
correct (registration/effect/consent-reachability are properties of the
entry and the rail, not of this one handler's internal extraction), but
#1898 must land before flipping this token actually closes #1606's corpus
row live. Pins:
`tests/unit/services/intent_service/test_inversion_write_allowlist_set_default_repo_1606.py`.

**#1595 unit 4 — a SPLIT turn routes sibling-by-sibling through the ONE rail
(2026-09-26; Arch ruled shape (ii) on 2026-09-25, sequencing rules approved
2026-09-26).** Not a new surface: the siblings run through the SAME surface-3
rail block the single-intent path runs, N times.

*Why not the orchestrator (the measured refutation of option (a))*: the
multi-intent branch dispatches by CATEGORY through `CanonicalHandlers` and
**never consults the action rail** — `_execute_single` gates on `can_handle`,
which accepts only {TEMPORAL, GUIDANCE, PORTFOLIO, CONVERSATION, PROVENANCE},
while the consult emits QUERY for 123 of 127 rail keys (EXECUTION 3,
SYNTHESIS 1). **0 of 127 rail keys clear that gate**; the consult's output set
and the orchestrator's input set are disjoint, so a rail leg inside
`_execute_single` (shape (i)) would have been a SECOND "is this action
rail-dispatchable?" site — the exact proliferation #1124 exists to close.
Arch's ruling: build (ii).

*Mechanism.* Surface 1 now RETAINS each claim's match span
(`MultiIntentResult.spans`, realigned post-subsumption by the same
object-identity trick `pattern_lists` uses; `_matches_patterns` is a
byte-identical delegator over a new `_first_pattern_match` — same single
`re.search` pass, no new pattern literal, `TestExtractionPatternRatchet`
untouched at 567). `inversion_live.sibling_segments` turns those anchors into
one text SEGMENT per sibling (anchor *i* to anchor *i+1*, segment 0 extended
back to index 0, greeting anchors participate so a greeting's words don't ride
into the first substantive half; declines honestly on a missing span, a
length-changing case-fold, or a blank segment). Each sibling then consults
`consult_inversion_live` on its OWN segment with `multi_intent_sibling=(i, n)`
— which skips the #1896 split guard and stamps `sibling_index`/`sibling_count`
on every decision line that consult emits. **All four dispatch conditions hold
per sibling**; `None` leaves the sibling on its surface-1 Intent.

*Dispatch and sequencing (Arch's three rules).* The resulting siblings run
SEQUENTIALLY through `IntentService._dispatch_action_rail` — the rail block
extracted verbatim from `_process_intent_internal` so it has two callers and
one body. (1) **Order**: every sibling whose rail entry declares READ first, in
message order, then the FIRST sibling declaring WRITE/DESTRUCTIVE — reads
cannot pause, so the user always gets every read answer. (2) **Pause = stop**:
the first sibling that arms a pending action ends the turn; siblings after it
are NOT run and are NAMED in the reply (`_compose_deferred_sibling_line`,
quoting the deferred sibling's own words — *CXO copy pass owed*), never queued
for auto-run, because the user's "yes" binds to the item they were SHOWN. An
arm is detected two ways: the #1190/#1509 gate returns (`_RailOutcome.armed`)
and a #846 store peek across the dispatch, which catches a handler that armed
its own carrier — continuing past either would CLOBBER the one-slot store.
(3) **No cross-sibling state**: no sibling's result feeds another's arguments.
Reply parts are joined by the orchestrator's OWN `_aggregate_messages` (the
joiner, reused without the `can_handle` gate).

*Refusal conditions — the path declines and the legacy chain does the whole
turn unless ALL hold*: the stand-down fired for the split reason, ≥2
substantive siblings with derivable segments, **at least one sibling actually
consult-routed**, and **EVERY sibling's final action is a rail key**. That last
one is load-bearing: a sibling the rail can't serve (`get_current_time` is not
a rail key) would be the #1896 dropped half in a new coat. Declines are logged
`inversion_multi_intent_declined` with a reason; a handled turn logs
`inversion_multi_intent_dispatched`. No new dispatch site — `MAX_DISPATCH_SITES`
stays 0, and `dispatch_workflow`'s call-site count in `intent_service.py` is
unchanged at 3 (classified-turn rail, #846 offer-acceptance seam, #300
autonomous handler).

⚠️ **Denominator, measured 2026-09-26**: **surface 1's splitter cannot emit a
WRITE or DESTRUCTIVE sibling at all** — every action in its `pattern_groups`
is a read lane and the #1527/#1756/#1794/#1881 guards make those lanes decline
a destructive ask outright. So "what are my todos and delete my hydrate
reminder" splits into ONE intent and "delete my hydrate reminder and what are
my todos" into ZERO. A destructive sibling exists only when a CONSULT produces
one. **Residual, filed not hidden**: because those two phrasings don't split,
they never reach the #1896 guard either, so the whole-message consult can
still answer the delete half and drop the read half — closing that needs the
router to return an ordered PLAN (option (b)). **#1606 is NOT closed by this
unit**: its corpus row doesn't split at surface 1, and its repo half is
`set_default_repo`, a WRITE that nobody has run Arch's three allowlist
conditions against (a separate unit-3-style entry). Regression:
`tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py`
(24 tests; real `detect_multiple_intents` throughout, deterministic router
stub keyed by segment).

**#1595 unit 4b (#1897/#1606) — the ADDITIVE `plan` outcome, for the turns
unit 4's own splitter can never reach (2026-09-27; grammar shape ruled by
Arch, `mailboxes/lead/read/rule-arch-to-lead-cc-ppm-1595-unit4b-…-2026-09-26.md`;
consumption wiring is Lead's, not Arch's — Arch's ruling explicitly deferred
it).** The residual named directly above (surface 1 never splits
"what are my todos and delete my hydrate reminder" at all, so unit 4's
sibling path never engages and the whole-message consult can answer one
half and drop the other) is exactly option (b): the router itself may
answer a genuinely multi-operation message as an ORDERED PLAN instead of
one operation.

*Shape (`inversion_router.py`), additive at every layer — the single-op
contract is byte-identical, never touched.* `RoutingDecision` gains
`outcome="plan"` and a new field `operations: List[Dict[str, Any]]`
(default empty; populated ONLY on a plan decision, never alongside
`operation`/`args`). `route_label` renders a plan as
`PLAN[op1→op2→...]`. The system prompt's single-op instruction becomes the
DEFAULT clause with the plan as the stated EXCEPTION — verbatim before/after
text and the exact wording rationale are in the dispatch session log
(`dev/2026/09/28/2026-09-28-0815-prog-code-log-1595-unit4b-plan-outcome.md`).
`_parse_and_validate` accepts a plan object
(`{"outcome":"plan","operations":[...]}`) and validates EVERY element
against the identical grammar a single object gets (vocabulary, no invented
names, confidence numeric/clamped) — ALL-OR-NOTHING: <2 elements, any
invalid element, a NONE/CLARIFY sentinel as an element, or <2 DISTINCT
operation names all produce the SAME parse failure a bad single object
gets (the repair path), never partial acceptance. The one-level-of-nesting
`_JSON_OBJECT_RE` regex could not represent a plan's own nesting (plan →
operations[i] → args — three brace levels) and is replaced by
`_extract_json_object`, a string-aware balanced-brace scanner — byte-identical
on every reply the old regex already matched. The repair-retry prompt (Arch
flagged this exact gap as unsolved in the grammar ruling) is now SHAPE-AWARE:
attempt 2 restates both the single-op and the plan JSON forms, so a
malformed plan on attempt 1 can still be repaired AS a plan on attempt 2
(and a malformed single object is unaffected). Regression:
`tests/unit/services/intent_service/test_inversion_router_1595.py` (10 new
tests: valid plan, nested-args parsing, <2 elements, invented op, malformed
element, duplicate-collapse, NONE/CLARIFY-as-element, both repair-retry
shapes, prompt-wording order pin).

*Consumption (`inversion_live.py` + the unit-4 rail loop in
`services/intent/intent_service.py`) — the smallest wiring that reuses unit
4's own hand-off mechanism, not a second one.* A whole-message consult
(`multi_intent_sibling is None`) that decodes a `"plan"` decision validates
EVERY element against the SAME four dispatch conditions a single operation
is checked against (live match, confidence threshold, rail-dispatchable,
the #1677 effect guard) via `_resolve_plan_for_dispatch` —
ALL-OR-NOTHING at this layer too: one ineligible element declines the WHOLE
plan (a plan element has no surface-1 Intent of its own to fall back to,
unlike a real sibling, so this is NOT the same as unit 4's "sibling the rail
can't serve declines the whole turn" — it is a *different, stricter*
necessity: nothing survives to fall back to). A fully-validated plan is
handed off exactly the way the #1896 split stand-down is: the consult still
returns `None` (no single `Intent` can represent 2+ operations) and
publishes `reason=PLAN_STAND_DOWN` plus a new
`LiveRouteProvenance.plan_operations` field for the rail loop to peek. A
sibling consult (real split path) that itself gets a plan back declines
(`plan_in_sibling_unsupported`) — no segment-within-a-segment mechanism was
built. `IntentService._maybe_dispatch_multi_intent_inversion` now accepts
EITHER hand-off reason (`MULTI_INTENT_SPLIT_STAND_DOWN` or
`PLAN_STAND_DOWN`); for a plan, `finals`/`routed_count` are built directly
from `stand_down.plan_operations` (no per-element consult loop — everything
was already validated at the whole-message consult) and then run through
the IDENTICAL shared code the split path already proved: rail-dispatchability
check, reads-first/first-write sequencing, the sequential
`_dispatch_action_rail` loop, pause-defers-the-rest, reply composition, and
provenance republish. **Known, documented gap**: a plan element carries no
independent text SEGMENT of the user's own words the way a real sibling's
claim span does. The router's own per-element `rationale` (falling back to
the bare operation name) stands in as BOTH the deferred-sibling label AND
the element's `Intent.original_message` — the latter matters beyond
cosmetics, since handler-side slot-fills that key off the message (e.g.
`destructive_confirm._named_delete_target`) need text about ONE operation;
feeding the whole multi-clause message in produced a materially worse
target-word match in manual testing during this build (`"what are my todos
and delete my hydrate reminder"` → `_named_delete_target` → `"what are
hydrate"`, a fragile 1/3-word match that happened to still clear the fuzzy
threshold, vs `"delete hydrate reminder"` → `"hydrate"`, an exact match) — a
rationale is a short paraphrase, not the user's own words, so anything that
echoes it back verbatim echoes the router's phrasing, not the user's.
Regression: `tests/unit/services/intent_service/test_inversion_live_1595.py`
(`TestPlanOutcome`, 5 tests: full hand-off + provenance shape, one ineligible
element declines the whole plan, sub-threshold declines the whole plan,
nested-plan-in-a-sibling declines, default-empty costs zero work) and
`tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py`
(`TestPlanOutcome` + `TestPlanMessageShape`, 6 tests: the #1897 message
verified NOT to split at surface 1, read-then-write dispatch, the confirmed
yes deletes the named row, two writes — first arms/second is named and never
queued, the non-plan-stand-down-reason guard across three decline reasons,
no-second-dispatch-site).

**Two amendments, 2026-10-02 (#1606 closed; Arch's ruling of 2026-10-01).** They
supersede two sentences above, left in place for the record:

1. **All-or-nothing has ONE exception, ruled by KIND not position.** A plan
   element that is a FLOOR-disposition **read** — registry disposition FLOOR
   *and* a read verb, both looked up mechanically through `get_disposition` /
   `get_verb` (`_is_floor_read_element`), unknown pairs get no credit — no
   longer declines the plan: it is the one element that always has a fallback,
   because the floor can always engage. It resolves with `floor: True`, no rail
   entry, no confidence threshold, and the rail loop runs it **in the reads
   phase like any read sibling** through `_handle_floor_with_context`, scoped
   to its own ask plus "the other part is being handled separately" (never the
   whole message, which would let the floor claim or contradict the rail's
   outcome). Reply composition is execution order, the rail's text verbatim.
   Two guards: a plan made ONLY of floor elements declines (`plan_all_floor`)
   so the ordinary single floor turn serves it — otherwise this is a floor
   multiplier — and every other non-live element still declines with today's
   reasons. `plan_floor_elements=N` on both the decision and dispatch lines.
   PM's #1606 sentence (`clear the reminders except for "Review the PR" — also,
   are you able to set my default repo for me conversationally?`) now routes
   `PLAN[delete_todo → get_capabilities]`: capability answer first, then the
   delete half's own #1605 carrier, nothing deleted — proven through the real
   app by `tests/e2e/test_1606_two_part_turn_floor_element_live.py` (llm-marked).
   The first live run declined `plan_not_live` because Haiku named the
   capability half `get_contextual_guidance` (CANONICAL — correctly excluded);
   the lever was `get_capabilities`' registry description, which now names
   "can you / are you able to X?".
2. **The "known, documented gap" above bit for real and is closed.** The live
   probe's delete half ran `reminder_clear`'s except-clause extraction on the
   router's rationale ("User asks clear except one destructive operation
   exclusion") and found nothing. Each plan element now carries `text` — a
   verbatim, contiguous quote of the user's words for that part (prompt rule +
   `_validate_operation_element`); the rail loop uses it as the element's
   `original_message` only when it really is a case-insensitive substring of
   the message (`inversion_plan_text_verbatim` on the Intent context), and
   falls back to the rationale otherwise — never to the whole message. The
   floor element's message is its quote plus the handled-separately note.

⚠️ **What is NOT measured here (m-43)**: every test above uses a stubbed
`inversion_router.route` — they prove the parse contract, the dispatch-time
validation, and the hand-off/rail-loop mechanism, never that the LIVE
constrained router reliably reaches for a plan on a genuinely multi-op
message, or that the new prompt clause doesn't regress single-op routing
accuracy on the ~95%+ common case (Arch's own explicit ask: "measuring
single-op routing accuracy before/after the prompt change, same discipline
as #1772"). That before/after measurement is the Lead's, run separately,
and is **pending** as of this entry — no live-corpus number is claimed by
this unit. `PIPER_INVERSION_LIVE_CATEGORIES` gates the DISPATCH-time flip as
before; nothing about the plan shape itself is behind a flag — the grammar
and parser changes are live in the router's prompt/schema as soon as this
lands, only the flip's four dispatch conditions gate whether a validated
plan actually reaches the rail loop.

**Pre-claim shadow probe (2026-09-02) — the #1668 MIRROR: surface 1's claims
made falsifiable per-pattern-list.** The narrowing schedule (PM-ratified
2026-08-29, decisions.log same date: a pre-classifier claim must meet ~100%
precision measured by shadow divergence; below-bar patterns get deleted ON
EVIDENCE) needs a measurement no existing surface produced: #1668's
counterfactual runs on INVERSION-routed turns, and the #1595 router shadow on
legacy turns compares against the turn's production LABEL without saying which
`*PATTERNS` list claimed it. `services/intent_service/preclaim_shadow.py`
closes that: on a turn surface 1 CLAIMS — at BOTH entry surfaces, wired at the
two claim sites in `classifier.py` (`classify`'s `pre_classify` branch and
`classify_multiple`'s `detect_multiple_intents` branch; a cached repeat
returns without re-claiming and is deliberately not re-sampled) — under
sampling (`PIPER_PRECLAIM_SHADOW` "1"/"true" enables, default OFF = pinned
byte-identical; `PIPER_PRECLAIM_SHADOW_SAMPLE` rate, default 1.0; the shared
`PIPER_INVERSION_LOG_UTTERANCE` privacy knob), a fire-and-forget task runs ONE
constrained-router call and logs `preclaim_shadow_agreement` /
`_disagreement` / `_incomparable` carrying **the claiming pattern-list name**
(threaded via `PreClassifier.pre_classify_with_pattern_list` — `pre_classify`
is now a byte-identical delegator over it — and
`MultiIntentResult.pattern_lists`, aligned post-subsumption; the two claim
sites without a class-level list report `MILESTONE_STATUS_INLINE_PATTERNS` and
the helper-guarded lanes their underlying lists), the pre-claimed
category/action, the router's operation/outcome/confidence, and alias-resolved
agreement. Layer statement on every line (m-43): the router is consulted
STATELESS (no session snapshot) — the same zero-state layer at which the
patterns themselves claim. Incomparability is its own bucket, never folded
into either side (m-44): `router_refused`/`router_error`, and
`claimed_action_outside_grammar` for a claim the grammar cannot express
(agreement impossible by construction). Observer only: the module joins
`TestInversionShadowNoExecutionBoundary`'s allowlist as the third named file;
nothing dispatches; measurement changes NO claims — narrowing happens later,
in reviewed commits, each citing its probe rows (the 08-09 condition). Cost:
one Haiku-class call per sampled claimed turn, bounded by the sample rate;
zero latency (never awaited). The readout the schedule reads:
`scripts/preclaim_shadow_report.py` (no LLM — parses the telemetry lines;
per-pattern-list claim counts, agreement rates, precision =
agree/(agree+disagree) with incomparables shown beside the denominator, and
the precision-vs-bar verdict per list, bar default 1.0). Pins:
`tests/unit/services/intent_service/test_preclaim_shadow.py` (default-off
byte-identical with explosive router, exactly-one-consult +
transcript-identical, fail-open, identity threading across ≥3 lists on both
entry surfaces, comparison semantics, report shape).

**Phase 2.2 prerequisites landed 2026-08-19 (issues 1665 + 1664, gate-doc
caveats)**: (a) every #846 arm site now stores its ALREADY-RENDERED ask on
the offer record (`offer["question"]` — the exact copy the user saw that
turn; re-arm seams update it as the open question changes state), so the
live snapshot's `pending_offer_question` matches the Phase-2.1 fixtures'
strength instead of serializing "(question text unavailable)"; and (b)
`pending_offer_is_confirm` derives from the offer KIND via
`destructive_confirm.offer_is_confirm` — the #1650 confirm-kind table in ONE
place (destructive confirms now kind-stamped `destructive_action_confirmation`,
reminder-clear delete confirms, consent checks, the unmapped-status close
confirm, the drafted-issue ready-to-file state, the closed-default repo
bind) — never from the carrier `workflow_type`, which the OPEN repo question
also rides (the 1664 defect: a which-repo ask rendered "(yes/no confirm)").
The verb question and open repo question are pinned NOT-confirm. Regression:
`tests/unit/services/intent_service/test_rendered_ask_1665.py` (per-arm-site
stored-copy-equals-said pins + the kind-table pins).

### The floor's LLM-ERROR path — a fifth, orthogonal classification, not a
### routing surface (#1872, 2026-09-24)

Distinct from the four dispatch surfaces above: this is what happens when
surface 4's OWN LLM call (`llm.complete(...)` inside
`ConversationalFloor.respond()`) itself raises, not how a turn gets routed.
Included here because it decides the floor's user-facing COPY on an outage —
squarely "LLM responses" per this doc's own consult rule — and because #1872
found the same two-classifier-drift shape the rest of this doc tracks for
routing.

**The producer** (`services/llm/clients.py::LLMClient._complete_raw`): when
every attempted provider (primary + consent-filtered fallbacks) fails, it
used to raise a bare `RuntimeError("All configured LLM providers failed.
Details: <provider>: <reason>; ...")`. That ONE string wraps three different
truths — zero providers actually attempted, a configured provider's
credential rejected, a transient connection failure — and the floor's own
classifier didn't recognize its own trigger (`no_provider` keyed on "not
configured"/"no llm provider", neither substring present), so every terminal
LLM failure fell to `transient` ("try again in a moment") regardless of
cause. #1872 fixes this AT THE PRODUCER, not with a smarter string pattern
(a one-line pattern can't honestly cover three causes behind one string):
`_complete_raw` now raises a typed `AllProvidersFailed(RuntimeError)`
carrying `attempts: list[tuple[provider, reason]]`, `.no_providers` (an
honest fact read off `attempts`, never inferred from text), and
`.primary_reason` (the first/primary provider's own failure text).
`str(exc)` stays BYTE-IDENTICAL to the pre-#1872 message, so every existing
string-matching consumer (the web route's `_extract_degradation_message` in
`web/api/routes/intent.py`, the translator's own pattern table, every
pre-#1872 test) keeps working unchanged.

**Two classifiers exist for this family and can drift** — the same failure
class this doc's "vocabularies" section tracks for routing action names,
here for error copy:
  - `services/intent_service/conversational_floor.py::_classify_llm_error` —
    picks a `FLOOR_FALLBACK_*` chat message (8 buckets: `consent_unreadable`,
    `quota_exhausted`, `no_provider`, `not_configured`,
    `insufficient_permission`, `rejected_credential`, `config_endpoint`,
    `transient`).
  - `services/ui_messages/user_friendly_errors.py::make_error_user_friendly`
    — picks a translator `category` (`llm_key`/`llm`/generic HTTP buckets),
    reused at key-validation time (`humanize_validation_result`) and by the
    web route's degradation extractor.

#1872 unifies the TEXT half: `_classify_llm_error` now classifies from the
exception's TYPE first (the two checks that can only ever live in the floor
— `isinstance(error, ConsentUnreadableError)`, `isinstance(error,
AllProvidersFailed)` → `no_provider` if `.no_providers` else classify
`.primary_reason`) and delegates everything else to a NEW shared function,
`classify_llm_error_text(text) -> bucket`, exported from
`user_friendly_errors.py` — branch order preserved verbatim from the old
floor code. The translator's OWN pattern-table decision (`category`) is
UNCHANGED and not merged into this function; the two vocabularies stay
related, not identical. Same commit adds Gemini's real invalid-key wording
(`API_KEY_INVALID` / "API key not valid", HTTP 400) to a shared
`INVALID_KEY_PATTERN` (built from `GEMINI_INVALID_KEY_PATTERN`) consulted by
BOTH classifiers — a gap neither recognized before.

**Where the two DISAGREE, #1872 does not pick a winner** (explicit issue
instruction): the pinned mismatch table in
`tests/unit/services/intent_service/test_llm_error_classifier_agreement_1870.py`
only shrinks where the TYPED exception (or the new shared Gemini pattern)
makes the resolution unambiguous — the floor's own real production trigger
(finding (a): zero-providers / rejected-credential / transient now
correctly separated for the TYPED path) and the shared Gemini gap (finding
(d)). Two disagreements stay deliberately unresolved and are CXO/PM copy
calls, not defects: (b) bare status-word text ("Unauthorized" alone) — the
floor's broader substring net correctly catches it, the translator's
narrower LLM-key patterns don't and fall to a non-LLM-aware generic "auth"
category; (c) config-endpoint (stale model ID / 404) text — the floor has a
dedicated honest bucket, the translator falls to a generic "unknown"/"api"
bucket. A resolved mismatch that regresses fails the pinned test file
loudly, by design.

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

## Phase 3 — deletion gate (#1595 epic-0 unit 5, instrument built 2026-09-27)

The epic's own condition on the endpoint (issue #1595 body, "Conditions on the endpoint
(Phase 3)"): **"Deletion ratchet asserts corpus non-regression ALONGSIDE shrink"** and
**"pattern→corpus-case conversion is a STEP IN the deletion procedure, not an
intention."** `scripts/inversion_phase3_deletion_gate.py` is the INSTRUMENT that
enforces both — it deletes nothing itself; it is the gate a future deletion commit
must pass, run BEFORE that commit and cited in it.

**What it asserts, per `*_PATTERNS` list**: for every corpus row (`tests/fixtures/
inversion_corpus_phase0.yaml`, 116 rows) surface 1 claims — via
`PreClassifier.pre_classify_with_pattern_list` / `MultiIntentResult.pattern_lists`, the
SAME claiming-list identity the pre-claim shadow probe already threads (never a second
regex pass) — a list is **deletable** iff every row it claims is one of:
  (a) **MATCH** against the corpus-expected action, read from the 2026-09-25 Phase-1
      shadow-score report's own tables (no LLM call in this script — the router's
      verdict is READ, never re-scored);
  (b) **REVIEW** where the router's own route equals THAT ROW'S surface-1-claimed
      action (the inversion agrees with surface 1 on this specific case); or
  (c) the row's corpus-expected action is already a member of the LIVE flag's routable
      set (`--live` override, else `PIPER_INVERSION_LIVE_CATEGORIES`, read via the
      SAME `resolve_live_match` the live consult itself uses) — the pattern's fate no
      longer matters for a row whose destination the Phase-2 per-category gate already
      covers.
Any row failing all three (MISMATCH, UNSCORED, or a REVIEW disagreement to a non-live
destination) fails the WHOLE list, named with its reason.

**Precedence, documented not implicit**: for TEMPORAL-category rows, the same-day
TEMPORAL RE-SCORE report (`inversion-phase1-shadow-score-2026-09-25-temporal-rescore.md`)
OVERRIDES the full run — it exists because the full run's TEMPORAL numbers predate a
registry-description sharpening (the full run's `what's on my calendar today?` MISMATCH
became the re-score's MATCH). Every other category reads the full run only.

**The pattern→corpus conversion step**: for a DELETABLE list, the gate also reports
which of its regex literals matched NO corpus row (`PreClassifier._first_pattern_match`
called on the SAME claiming list, read-only — reusing the production matcher on an
already-known list is not a new claim surface) — printed as "needs a corpus row before
deletion", never invented. A deletion commit must deposit those rows first; the gate
does not do this for you.

**Non-regression ledger**: `scripts/inversion_phase3_deleted_patterns.json`'s
`DELETED_PATTERN_LISTS` array — EMPTY as of 2026-09-27 (no list has been deleted; this
unit built the gate, not a deletion). Each future entry records the deleted list, its
literal count, and the corpus rows it claimed at deletion time;
`gate.check_deleted_entry_non_regression` re-verifies on every run that none of those
rows is claimed again by a surviving list and each still scores MATCH/agreeing-REVIEW —
pinned by `tests/unit/test_inversion_phase3_deletion_1595.py`.

**Measured 2026-09-27** (`--all`, no `--live`): 84/116 corpus rows claimed by some
surface-1 list, 32 unclaimed. `TEMPORAL_PATTERNS` (56 literals) claims only 2 of the 10
TEMPORAL corpus rows directly (`what time is it?`, `when is my next meeting?` — both
MATCH) — the reminder/calendar-shaped TEMPORAL rows claim via `REMINDER_PATTERNS` /
`CALENDAR_QUERY_PATTERNS` instead, a genuine finding of the census, not a bug. GO/NO-GO
is data that moves with the reports; this doc states the mechanism, not a frozen
verdict — run the script for the current read. ⚠️ This specific measurement predates the
first deletion below — `REMINDER_PATTERNS` no longer claims anything as of the same day.

### Any change to the router's prompt or catalog is scored on BOTH tables, with a control (rule, 2026-09-29)

Learned on 4b (2026-09-28, `inversion-4b-single-op-before-after-2026-09-28.md`) and stated here so
it outlives that doc. The router's prompt text and its catalog (which is derived from
`action_registry.py` descriptions) reach **every** live router call, so a change to either — a
new outcome clause, a description edit, an example — is a routing change for the whole corpus,
not for the rows it was aimed at. The procedure:

1. **Full corpus, one run, on the exact text that ships** — not a subset, not the draft before
   the last wording tweak. 151 rows ≈ 151 calls to the dev key's model; cents.
2. **Compare per row against each row's frozen verdict**, never pooled totals. Read **both
   tables**: the asserted rows (MATCH/MISMATCH) *and* the REVIEW rows (route only). 4b read
   0-regressed on the asserted table while the REVIEW table carried a deterministic live
   regression (`delete my reminders` → a listing, "needs to list them first").
3. **Any changed row gets sampled n≥6 against a same-session control on the old text** before it
   is called noise. The pre-change source is loaded from git (`git show <sha>~1:…`) and run in the
   same process, same model, same minute — not "I remember it used to say X."
4. **Attribute, then fix at the cause.** On 4b the cause was one word in the opening sentence
   ("which operation(s)"), not the clause everyone would have edited. On GUIDANCE it was the
   registry description, not the pattern.
5. Deploy only after the run on the shipping text reads 0 regressed on the asserted table and
   every REVIEW change is either the intended effect or attributed by step 3.

Scoring reports land in `docs/internal/architecture/current/` and, when they carry Phase 3 rows,
go at the FRONT of `PHASE3_REPORTS` in `scripts/inversion_phase3_deletion_gate.py` (newest
first; a re-score overrides). `scripts/inversion_phase1_shadow_score.py` has `--phrase` for a
one-row re-score and `--source-prefix` for a deposit batch.

### First deletion (2026-09-27): `REMINDER_PATTERNS` + `REMINDER_QUERY_PATTERNS`

The gate's `--list REMINDER_PATTERNS` / `--list REMINDER_QUERY_PATTERNS` calls (run
BEFORE deletion, per the deletion procedure) both read **GO, 0 "needs a corpus row"**:
`REMINDER_PATTERNS` (5 literals) claimed 5/5 corpus rows (4 MATCH from the same-day
Phase-3 conversion deposits scoring, `inversion-phase3-deposits-score-2026-09-27.md`,
+ 1 pre-existing REVIEW-agrees row, `inversion-phase1-shadow-score-2026-09-25.md`);
`REMINDER_QUERY_PATTERNS` (4 literals) claimed 4/4 (3 MATCH from the deposits scoring +
1 pre-existing REVIEW-agrees row — Arch's demanded "what reminders do I have?" pin).
Both lists' literals were then emptied to `[]` in `pre_classifier.py` (kept as
tombstones — the class attributes and their consumer code paths, incl.
`REMINDER_QUERY_BLOCKERS` which is now inert, survive; only the literals are gone), and
both entries were appended to `scripts/inversion_phase3_deleted_patterns.json`'s
`DELETED_PATTERN_LISTS`, each carrying its `rows_claimed_at_deletion` and
`expected_ops`. Re-measured post-deletion: corpus claimed dropped 99 → 90 (exactly the 9
ledgered rows), and **no sibling `*_PATTERNS` list reabsorbed any of the 9 phrases** —
they are now genuinely unclaimed at surface 1, covered instead by the ledger's
non-regression evidence (`test_inversion_phase3_deletion_1595.py`,
`TestDeletedPatternListsLedger`, re-checked every run).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]`
567 → 558 (567 − 5 − 4 = 558; `pattern_literal_counts.total_literal_count()` confirms
558 post-deletion).

**Gate-wiring fix landed in the same commit**: the deletion gate previously read only
the 2026-09-25 full report + temporal-rescore, so the same-day Phase-3 conversion
deposits (scored in a separate report) came back UNSCORED and both lists read NO-GO.
`RouterReports` now also consults `DEPOSITS_REPORT`
(`inversion-phase3-deposits-score-2026-09-27.md`, asserted-rows only — its REVIEW table
is empty boilerplate), checked first, all categories; no overlap with the other two
reports' phrases so this is additive, not a precedence change.

**Reachability-ratchet fix, also same commit**: `TestChatPointersReachabilityRatchet`'s
`pin:reminder-query` row ("what reminders do I have?") broke — `_static_resolve` only
ever consulted `pre_classify`, which now returns `None` for this phrase. Added a new
deterministic resolver, `phase3-deletion-ledger`: when pre-classify is `None`,
`_static_resolve` checks whether the utterance is one of a `DELETED_PATTERN_LISTS`
entry's verified `rows_claimed_at_deletion`, re-derives the destination from that
entry's `expected_ops` via `ACTION_REGISTRY`, and only claims resolution if
`check_deleted_entry_non_regression` passes THIS run (real corpus row, real
router-report verdict — no LLM call, ever). This is the general shape every future
Phase-3 deletion whose corpus rows include a POINTER/pin will need.

**Live-flag dependency, stated plainly**: this deletion is safe only because
`list_reminders_query` and `create_reminder` are corpus-verified AND (for the
non-REVIEW rows) MATCH under the constrained router — but the router itself is
*consulted live* only when the corresponding category/operation is in
`PIPER_INVERSION_LIVE_CATEGORIES`. **If a deployment ever runs with `create_reminder`
or `read_status` (which carries `list_reminders_query`) OUT of the live flag, these
phrasings fall through the now-empty pattern lists straight to the general LLM
classifier — the pre-#1559/#1521 state, unroutable-by-pattern and unrouted-by-inversion
at once.** As of this unit the live flag on alpha does carry both (dispatch-verified);
this is a standing operational dependency, not a one-time fact — check the live flag
before trusting these phrases route correctly on any given deployment.

**A fifth consumer of surface 1 the procedure did not model — #1899 (found by this deletion,
Lead 2026-09-27; CLOSED same day, reads-only release shipped)**: two armed-offer carriers decide
"unrelated command, or the answer to my question?" by calling `PreClassifier.pre_classify(text)`
**directly, FIRST** — `handle_reminder_task_turn` (`todo_handlers.py`, #1654) and the FTUX interview
turn (`first_contact.py`, #1688). The Inversion's own live consult cannot backfill them: it stands
down on any turn that popped a pending offer (`turn_had_pending_offer`, #1190) — exactly the
condition every carrier turn meets. So each Phase 3 deletion narrowed what those discriminators
could release on surface 1 alone — concretely, once `REMINDER_QUERY_PATTERNS` was deleted,
answering "list my reminders" to "what should I remind you about?" would have **bound as the task
text** instead of releasing to the listing.

**The fix (CXO ruling + Arch concur, 2026-09-27)**: both carriers now consult a SECOND, narrower
oracle when surface 1 declines — `inversion_live.read_op_claims_turn`. It calls the Inversion
router **directly** (never through `consult_inversion_live`, whose `turn_had_pending_offer`
stand-down is exactly what this helper routes around) and releases the turn **only** when ALL of:
outcome is a concrete operation; confidence clears `live_min_confidence()`; the operation's rail
entry declares READ effect (checked the same way `_effect_guard_passes` reads it — `entry.effect
== EffectClass.READ`, deliberately NOT the whole gate function, which also passes an allowlisted
WRITE — CXO ruled READ-verdict-only, no exception); and the operation is inversion-routable under
the CURRENT live flag (`resolve_live_match` non-`None`) — so an unflipped deployment, or an
unflipped operation, behaves exactly as before: bind. A READ verdict can never sensibly complete
"remind me to ___" or stand in for an FTUX answer (structural, not a heuristic), so gating on it
alone is safe in a way gating on any non-trivial router confidence would not be; write/none/clarify
still bind as before ("buy milk" never releases on a `create_todo` hunch). Cost: one router call
only on an armed-answer turn where surface 1 already declined (rare). Tests:
`tests/unit/services/intent_service/test_inversion_read_release_1899.py` (the helper's four gates,
including the router-exception and threshold-boundary cases) plus wiring pins in
`test_task_clarify_1654.py::TestTaskTurnHandlerSeam` and
`test_ftux_interview_1688.py::TestHandleFtuxInterviewTurn`.

**Consequence for future Phase 3 deletions**: the two REAL discriminator sites no longer erode on a
READ destination — a deleted pattern whose corpus row named a READ operation is recoverable via the
reads-only release (once that operation/group/category is live-flagged). A deleted pattern whose
corpus row named a WRITE destination is **still a live erosion risk** for these two carriers — the
reads-only release structurally cannot and must not cover it (see CXO's ruling above); that
consideration remains open for future deletions. **Before every further deletion, run**
`git grep -n "PreClassifier\.pre_classify(" -- services` and check whether the list being deleted is
load-bearing for a direct consumer (today: `action_registry` — registry check; `first_contact` +
`todo_handlers` — carrier discriminators, now covered for READ destinations by #1899's second oracle;
`inversion_live` — telemetry compare; `inversion_shadow` — shadow).

### Second deletion (2026-09-28): `TODO_QUERY_PATTERNS`

The gate's `--list TODO_QUERY_PATTERNS` call (run BEFORE deletion) read **GO, 10/10 literals
exercised, 11/11 claimed rows, 0 "needs a corpus row"**: 3 pre-existing REVIEW-agrees rows
("show me my todos" / "show all my todos" / "what's my next todo?", each `router=list_todos_query@1.0`
against their surface-1 claim, full report) + 7 deposited rows scoring MATCH in the 2026-09-27
deposits report (`expected: action:list_todos_query`) + 1 deposited row ("what should I do next")
whose ORIGINAL deposit expectation (`list_todos_query`) was a genuine MISMATCH against the router's
`get_top_priority` answer — resolved not by forcing the wrong destination but by RE-EXPECTING the row:
CXO/PPM ruled `get_top_priority` the correct destination (the row's own semantics — "what should I do
next" is a priority ask, not a listing ask), re-scored 1/1 MATCH in a dedicated report
(`inversion-phase3-todo-query-rescore-2026-09-27.md`, commit `657b4fc0c0`), and the gate script gained
an ordered, newest-first `PHASE3_REPORTS` list so a later re-score overrides an earlier verdict for the
same phrase without needing a second precedence rule. `TODO_QUERY_PATTERNS`'s 10 literals were then
emptied to `[]` in `pre_classifier.py` (same tombstone form as the first deletion — the class attribute
and its consumer code path, `_todo_query_match`, survive; only the literals are gone).
`RESTORATIVE_ASK_BLOCKERS` — whose ONLY consumer is `_todo_query_match` — is now INERT for the same
reason `REMINDER_QUERY_BLOCKERS` went inert in the first deletion (an empty pattern list can't be
blocked into claiming anything); `DESTRUCTIVE_ASK_BLOCKERS` stays live (shared by the STATUS/TEMPORAL/
MEMORY/CALENDAR_QUERY lanes too).

**Ledger entry** carries all 11 `rows_claimed_at_deletion` phrases, `expected_ops:
["list_todos_query", "get_top_priority"]` (TODO_QUERY_PATTERNS is the first entry whose deletion
routed to TWO distinct destinations), and a new `expected_op_by_phrase` map naming which of the two
ops each row specifically verified against. This closes a real precision gap the two-op shape exposed:
`check_deleted_entry_non_regression`'s un-asserted-REVIEW fallback previously accepted a route iff it
matched **any** of an entry's `expected_ops` — sound for every single-op entry (nothing to disambiguate
against), but for a heterogeneous entry that "any" check could in principle accept a REVIEW row that
drifted to the OTHER destination it was never actually scored against. `scripts/
inversion_phase3_deletion_gate.py::expected_op_for_phrase` now resolves each phrase's own target op
with explicit precedence — (1) the corpus row's own asserted `action:` expectation, (2) the entry's
`expected_op_by_phrase` map, (3) `expected_ops` only when it has exactly one member — and both the
non-regression checker and the reachability ratchet's `phase3-deletion-ledger` resolver
(`tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet._phase3_ledger_resolve`)
consult it instead of the old "any of expected_ops" / "bail if `len(expected_ops) != 1`" logic — the
latter would have silently refused to resolve EVERY row in this entry (including the 10 unambiguous
`list_todos_query` ones) the moment a second op appeared, which is exactly the failure the `page:/todos`
POINTER (`chat_pointers.py`, "show me my todos") would have hit on the reachability ratchet had this
not been fixed in the same commit.

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 558 → 548
(558 − 10 = 548; `pattern_literal_counts.total_literal_count()` confirms 548 post-deletion).

**Sibling-takeover finding, named not hidden**: post-deletion census measured corpus claimed dropping
**110 → 100** — nine less than the "exactly 11" a clean deletion would produce. One of the 11 ledgered
phrases, **"what should I do next"**, is now claimed DIRECTLY by `PRIORITY_PATTERNS` at surface 1
(`pre_classify` returns non-`None`, action `get_top_priority`) rather than falling through unclaimed.
This is not a new pattern or a silent drift: `git blame` shows `PRIORITY_PATTERNS` has carried an
IDENTICAL literal (`r"\bwhat should i do next\b"`) since commit `33f3a43ad42` (2026-03-22) — it was
DEAD CODE for this exact phrase the whole time, shadowed by `TODO_QUERY_PATTERNS`'s earlier position
in `pre_classify`'s if-chain (first-claim-wins). Once `TODO_QUERY_PATTERNS` emptied, the shadow lifted
and `PRIORITY_PATTERNS` claims it — landing on the SAME destination (`get_top_priority`) the rescore
ruling already established, so this is a benign, verified-agreeing reabsorption rather than a routing
regression. The ledger entry documents it explicitly under a new `known_reabsorptions` field (phrase →
reclaiming list + rationale), and `check_deleted_entry_non_regression` treats a reclaim as OK **only**
when it is (a) named in `known_reabsorptions` for that exact phrase, (b) reclaimed by the SAME list
named there, and (c) the reclaiming list's current action still agrees with the phrase's own target op
— any OTHER reclaim (a different list, an undocumented phrase, or a documented one whose answer has
since drifted) still fails the check loud, exactly as before. No sibling list reabsorbed any of the
other 10 phrases. Regression: `tests/unit/test_inversion_phase3_deletion_1595.py::
TestDeletedPatternListsLedger` (all three ledger entries, including this one's exception, re-verified
every run).

**Carrier discriminators (#1899)**: `handle_reminder_task_turn` and the FTUX interview turn's tests
that used a todo-listing phrase as their "surface 1 still claims this, release without a router call"
example (`test_task_clarify_1654.py::TestTaskTurnHandlerSeam::test_preclassifier_claim_releases_without_calling_router`;
`test_ftux_interview_1688.py::TestHandleFtuxInterviewTurn::test_preclassifier_claimed_command_releases_unbound`
and `::test_preclassifier_claim_releases_without_calling_router`) moved to "give me my standup"
(`STATUS_PATTERNS`, unaffected by either deletion) — same idiom as the first deletion's own conversions.
The todo-listing phrasings themselves are covered for these two carriers by #1899's reads-only release
(`inversion_live.read_op_claims_turn`), exercised directly via
`test_reminder_query_preclassifier_1521.py::test_todo_listing_unchanged` and
`test_todo_query_handlers.py::TestPreClassifierRoutingIntegration` (converted to the two-part
decline+inversion-routes idiom); no new #1899 gap was found by this deletion (unlike the first
deletion, which discovered #1899 itself).

### `get_current_time` becomes a rail key (2026-10-01, Arch's ruling)

Arch's 2026-10-01 ruling (`mailboxes/lead/read/rule-arch-to-lead-cc-ppm-cxo-temporal-give-get-current-
time-a-rail-entry-and-the-gate-has-a-false-live-path-2026-10-01.md`) found the deletion gate's `--live`
mechanism had a false-live path: `expected_action_is_live` matched a row's `expected` field against
op/canonical/group/category names WITHOUT requiring a `WorkflowEntry` to exist for it, so `--live
get_current_time` would read GO for `TEMPORAL_PATTERNS` even though `get_current_time` had no rail
entry and `consult_inversion_live` (condition 4: dispatches only operations in
`get_action_workflows()`) could never actually serve it. The gate was fixed the same day
(`expected_action_is_live` now requires `entry is not None` AND the real effect guard,
`tests/unit/test_inversion_phase3_deletion_1595.py::TestLiveMeansDispatchable`).

Before that fix could apply to TEMPORAL honestly, the 48 `TEMPORAL_PATTERNS` deposit rows (2026-09-30
session) needed a per-row sort: the pre-classifier's code comment at `intent_service.py` ~15380 says
plainly that surface 1 "assigns `get_current_time` to ALL temporal queries" including conversational
ones, which the TEMPORAL floor/keyword split (`_requires_canonical_handler`) then separates by MESSAGE
CONTENT, not by corpus row. The deposit rows had inherited that over-claim as their `expected` value.
Sorted 2026-10-01 against the live router's own answers (evidence, not authority — several rows
override the router where the reasoning is documented in-row): 15 pure time/date asks stay
`action:get_current_time`; 11 single-day calendar/meeting asks (today, tomorrow, a named day, "my next
meeting") become `action:meeting_time`; 13 multi-day/"upcoming"/"all X"/"walk me through my X" asks
become `action:week_calendar`; 8 rows where no TEMPORAL-family operation serves the ask (no team-
calendar feature, pure retrospective/duration, or a compound PRIORITY-shaped PLAN this corpus's
single-`expected:action:X` format can't represent) become `floor`; 3 rows name a genuinely different,
already-real operation the live router identified (`action:session_activity_query`,
`action:check_completion_status`, `action:changes_query`) rather than collapsing to the generic floor
catch-all. Full per-row table and reasoning: the sorting prog session's log,
`dev/2026/10/01/2026-10-01-0830-prog-code-log-1595-temporal-sort-and-rail.md`.

**The rail entry** (`get_current_time_entry`, `services/intent_service/workflow_entries.py`): READ
effect, `flip_group="read_temporal"` (joining `changes_query` and the calendar cohort —
`_READ_TEMPORAL_KEYS` is now 14 keys, not 13), `action_triggered=True`. Its entry point
(`run_get_current_time_workflow`) wraps the EXISTING canonical handler
(`CanonicalHandlers._handle_temporal_query`, `canonical_handlers.py`) — the same function
`_requires_canonical_handler`'s keyword split already reaches for a pure date/time ask — converting its
dict return into `IntentProcessingResult` (the one conversion this entry needs that the other
IntentService-method-backed entries don't, since `_handle_temporal_query` lives on `CanonicalHandlers`
and returns a dict the main canonical-dispatch call site converts inline).

**`ACTION_REGISTRY` disposition stays `CANONICAL`, deliberately not flipped to `WORKFLOW`.**
`CanonicalHandlers.can_handle()` claims the WHOLE TEMPORAL category unconditionally, so in the real
`_process_intent_internal` order (`_should_route_to_floor` → `canonical_handlers.can_handle` →
`_dispatch_action_rail`), the canonical branch returns before the action rail is ever reached for any
TEMPORAL intent — this rail entry is structurally unreachable from that path, same as every other
canonical-category action (GUIDANCE/PORTFOLIO/CONVERSATION/PROVENANCE — none has a rail entry either,
verified empirically 2026-10-01). Flipping the registry to `WORKFLOW` would make
`test_registry_disposition_matches_live_runtime` (`test_action_registry.py`) fail, because the modeled
live runtime still resolves `CANONICAL` via that short-circuit regardless of the rail entry's
existence. **What the rail entry actually changes**: it is consulted by `consult_inversion_live` (which
REPLACES `intent.action`/category before the normal dispatch order resumes — a different surface from
`_dispatch_action_rail` on the unreplaced path) and by the Phase 3 deletion gate's live-match
mechanism. Concretely: "what time is it" is now routed by the Inversion when the live flag carries
`read_temporal`; the pre-classifier/floor split (surface 1) remains the fallback when it doesn't.

Two existing tests asserted "`get_current_time` has no rail entry" as their example of an unrailed
destination; both were swapped to `explain_suggestion` (`PROVENANCE`, `CANONICAL`, still genuinely
rail-free as of this change) rather than deleted, per each test's own stated intent to pin the
property, not the example:
`tests/unit/test_inversion_phase3_deletion_1595.py::TestLiveMeansDispatchable::test_floor_routed_canonical_is_not_live_even_when_named_in_the_flag`
and
`tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py::TestConsultDeclinedSibling::test_a_sibling_the_rail_cannot_serve_declines_the_whole_turn`.

### Third deletion (2026-10-01): `CALENDAR_QUERY_PATTERNS` — the first live list

The gate's `--list CALENDAR_QUERY_PATTERNS --live read_status,read_referent,read_synthesis,
create_todo,create_reminder,read_strategic,read_temporal` call (run BEFORE deletion) read **GO,
52 literals, 49/49 claimed rows, 0 "needs a corpus row"** (3 literals remain structurally
shadowed by earlier siblings in the same list — `\bon my agenda\b`, `\bwhat'?s on my calendar.
*tomorrow\b`, `\bmy calendar tomorrow\b` — unexercisable, documented in the ledger's
`shadowed_literals`, not a blocker, same property the 09-30 deposits lane found). This is the
FIRST deletion whose rows' destinations (`meeting_time`/`week_calendar`/`recurring_meetings`)
are themselves live-dispatchable rail keys (flip_group `read_temporal`, all three registered the
same way `get_current_time` was the same day — see the subsection above) rather than purely
pattern-vs-pattern evidence: several of the 49 rows pass via condition (c) — a MISMATCH whose
ROUTER's own route is itself a live op (e.g. "what is on my calendar" expects `meeting_time` but
the router answers `week_calendar`@0.85, which is live, so the consult owns the phrase either
way). Verdict of record: the served-model (Haiku) baseline
(`inversion-phase1-shadow-score-2026-10-01-haiku-baseline.md`) plus the CALENDAR-specific
rescores (`inversion-phase3-calendar-score-2026-09-30.md`,
`inversion-phase3-calendar-rescore-2026-09-30.md`,
`inversion-phase3-calendar-query-rescore-2026-10-01.md`) plus CXO's 10-01 ruling that 5
no-feature capability-gap asks (calendar-conflict checks, find-time, booking) honestly floor
rather than claim a week dump as an answer. `CALENDAR_QUERY_PATTERNS`'s 52 literals were then
emptied to `[]` (same tombstone form) — the class attribute, `pre_classify`'s inline
meeting_time/recurring_meetings/week_calendar sub-lists, `_get_calendar_action` (the
`detect_multiple_intents` equivalent), and `CALENDAR_QUERY_PATTERNS`'s membership in
`_READ_LANE_GROUPS` all survive as documented, structurally-inert dead code (an empty pattern
list can never claim, so none of these can run).

**Sibling-takeover finding, an order of magnitude past the second deletion's one row**:
post-deletion census shows `TEMPORAL_PATTERNS` reabsorbing **19 of the 49** claimed phrases —
every one DISAGREEING (claimed as `get_current_time`, never the ruled meeting_time/week_calendar/
recurring_meetings/floor destination). This is the "4 of its literals shadowed by CALENDAR's"
property the TEMPORAL deposits lane found (2026-09-30 progress log entry) playing out at scale
once the shadowing list is actually deleted — `TEMPORAL_PATTERNS`' calendar/meeting/schedule
vocabulary overlaps `CALENDAR_QUERY_PATTERNS`' far more broadly than the 4 originally-measured
literals suggested, because that measurement only covered TEMPORAL's OWN unexercised literals,
not every corpus phrase CALENDAR used to shadow. Per the CXO/Arch instruction behind this
deletion — report every reabsorption, and ONLY fold it into the non-regression-passing mechanism
when the reclaiming action AGREES with the ruled destination — none of the 19 qualify for the
agreeing shape the second deletion's `known_reabsorptions` precedent used. They are documented
instead with an explicit `"agrees": false` per entry (reclaimed list, claimed action, and a note),
never silenced.

**Mechanism gap found and fixed, same commit**: `check_deleted_entry_non_regression` never had a
live-flag-aware (condition-c) escape for either (a) an unclaimed phrase whose router verdict is
MISMATCH-but-live-route, or (b) a documented reclaim that DISAGREES — it only ever checked
MATCH/agreeing-REVIEW, because no earlier ledger entry needed more (REMINDER_PATTERNS/
REMINDER_QUERY_PATTERNS/TODO_QUERY_PATTERNS' rows were all MATCH or agreeing-REVIEW). CALENDAR's
entry exposed both gaps in the same run (3 rows failed: 1 unclaimed-but-MISMATCH-live, 2
reclaimed-but-disagreeing). Fixed by unifying both code paths onto a single re-derivation of
`row_disposition` — the SAME MATCH/agreeing-REVIEW/live-MISMATCH proof `build_census` used at
gate time — fed a synthetic `ClaimResult` carrying the phrase's resolved target op
(`expected_op_for_phrase`) rather than the surviving pattern's own (possibly wrong) claim. A new
`cats: Optional[frozenset]` parameter threads the live-flag routable set through
`check_deleted_entry_non_regression` (omitted/`None` reproduces every earlier entry's behavior
byte-for-byte — none of them ever needed a live condition, so this is purely additive).
`known_reabsorptions` gained an `"agrees"` field (omitted/`true` = the original second-deletion
shape, unchanged): a documented DISAGREEING reclaim (`"agrees": false`) can still pass
non-regression when the phrase's own frozen router evidence independently re-proves it safe
regardless of what the reclaiming pattern claims — sound because `consult_inversion_live` runs
BEFORE this surface-1 fallback and already proves the row safe when the live flag carries
`read_temporal`; the fallback reclaim only matters when the live consult stands down (unflipped
deployment, armed turn, sub-threshold confidence, REFUSED, transport error), a pre-existing,
orthogonal fallback-quality question this deletion did not introduce. An UNDOCUMENTED reclaim
still fails loud unconditionally — the SURPRISE itself, not just eventual safety, is what the
check exists to catch. Pinned with 7 new synthetic tests (floor-row handling both unclaimed and
reclaimed, documented-agreeing, documented-disagreeing-but-independently-safe,
undocumented-reclaim-still-fails-even-if-safe, cats-required-for-a-MISMATCH-live-row) plus 2
ledger-specific tests (`test_calendar_entry_fails_non_regression_without_the_live_flag`,
`test_calendar_entry_known_reabsorptions_are_all_documented_disagreements`) in
`tests/unit/test_inversion_phase3_deletion_1595.py`.

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 548 → 496
(548 − 52 = 496; `pattern_literal_counts.total_literal_count()` confirms 496 post-deletion).

**Every broken surface-1 pin converted, never deleted**, across 7 test files — two of which
(`test_action_registry.py`, `test_keyword_disambiguation_901.py`) pinned the ORIGINAL #901/#919
disambiguation fixes that `CALENDAR_QUERY_PATTERNS` existed to provide (routing calendar-shaped
asks to QUERY instead of TEMPORAL, and suppressing the TEMPORAL phantom beside a QUERY claim) —
those fixes are intentionally SUPERSEDED by this deletion plus the CXO floor ruling, not broken,
so the tests were rewritten to pin the new intended reality rather than converted to the generic
decline+inversion-routes idiom:
- `test_calendar_query_handlers.py::TestPreClassifierRoutingIntegration` — converted to the
  decline+inversion-routes idiom (`_inversion_pin_helper.assert_inversion_routes`,
  `live_categories="read_temporal"`); a new `test_meeting_time_variants_reabsorbed_by_temporal`
  pins 2 test-local phrases ("how much time in meetings today", "meeting time today") that are
  TEMPORAL-reabsorption casualties outside the 49 corpus rows (found empirically, not predicted).
- `test_action_registry.py::TestRegistryCoverage::test_example_messages_classify_correctly` —
  gained a documented skip-list (`_KNOWN_TEMPORAL_REABSORPTION_EXAMPLES`) for the one
  `ACTION_EXAMPLES` documentation string ("How much time do I spend in meetings today?") that is
  itself now a TEMPORAL-reabsorption casualty.
  `TestMultiIntentSubsumption::test_calendar_check_does_not_produce_temporal` rewritten: asserts
  no QUERY claim survives (CALENDAR_QUERY_PATTERNS deleted) and pins the current TEMPORAL
  reabsorption explicitly rather than asserting its absence.
- `test_keyword_disambiguation_901.py::TestKeywordDisambiguationQ33`/`Q62` — 7 tests rewritten:
  the capability-gap phrases (find-time/schedule/book, calendar-overlap-check) now assert decline
  (`None`); the two phrases that are TEMPORAL-reabsorption casualties ("Check my calendar for
  conflicts", "What's on my calendar today?") assert the documented reabsorption explicitly.
- `test_greeting_pleasantry_only_1416.py::test_agenda_phrasing_still_reaches_agenda_not_greeting`
  — converted to a STRONGER form of its own contract: the compound greeting+agenda message now
  declines entirely at `pre_classify` (TEMPORAL_PATTERNS has no "agenda" vocabulary, confirmed
  empirically) rather than merely avoiding the "greeting" mislabel.
- `test_preclaim_shadow.py::TestSampledOn::test_multi_intent_surface_schedules_with_all_lists` and
  `TestPatternIdentityThreading::test_multi_surface_pattern_lists_align_with_intents` — both swapped
  from the "hi piper! what's on my agenda?" (greeting + calendar) pairing to "hi piper! what's
  blocking the milestone?" (greeting + ANALYSIS_PATTERNS), same idiom as the first two deletions'
  "give me my standup" swaps (the greeting+agenda pairing collapses to greeting-only post-deletion
  — TEMPORAL_PATTERNS doesn't claim "agenda").

**Reachability ratchet**: no `chat_pointers.py` POINTER row uses a CALENDAR-shaped canonical
phrase (verified by grep for `meeting_time`/`week_calendar`/`recurring_meetings` and for
calendar/meeting/schedule/agenda vocabulary) — `TestChatPointersReachabilityRatchet`'s
`phase3-deletion-ledger` resolver is therefore never exercised for this entry; it stays
mechanically correct (confirmed via the two prior deletions' POINTER rows, unaffected) without
needing a new case.

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/intent/` all green after
conversion (18 pins converted/rewritten, 0 net regressions); `tests/test_architecture_
enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` ceiling exact at 496.
`ruff format`/`ruff check --fix` clean. No LLM calls anywhere in this unit — every router verdict
consulted is a frozen, already-scored report, or a monkeypatched stub in tests.

### Fourth deletion (2026-10-01): `TEMPORAL_PATTERNS`

The gate's `--list TEMPORAL_PATTERNS --live read_status,read_referent,read_synthesis,
create_todo,create_reminder,read_strategic,read_temporal` call (run BEFORE deletion) read **GO,
56 literals, 69/69 claimed rows, 4 "needs a corpus row"** (2 shadowed by an earlier sibling
literal in the same list — `\bwhat'?s on my calendar\b` shadowed by `\bmy calendar\b`,
`\bhow long.*been working\b` shadowed by `\bhow long.*working\b` — and 2 genuinely never
corpus-exercised vocabulary — `\bwhat'?s on my schedule\b`, `\bwhat'?s.{0,10}tomorrow\b` —
documented in the ledger's `shadowed_literals`, not a blocker). This deletion was gated on two
prerequisites landing first, same day: the per-row sort of the 48 TEMPORAL deposit rows away
from the pattern's own ALL-temporal over-claim, and the `get_current_time_entry` READ rail entry
(flip_group `read_temporal`) so the live Inversion consult can actually dispatch
`get_current_time` — both per Arch's ruling (see "`get_current_time` becomes a rail key" above).
Verdict of record: the served-model (Haiku) baseline
(`inversion-phase1-shadow-score-2026-10-01-haiku-baseline.md`) plus the 10-01 TEMPORAL re-score
run after the per-row sort (`inversion-phase3-temporal-rescore-2026-10-01.md`).
`TEMPORAL_PATTERNS`'s 56 literals were then emptied to `[]` (same tombstone form) — the class
attribute, `pre_classify`'s inline TEMPORAL branch, the `detect_multiple_intents` pattern-groups
entry, `_READ_LANE_GROUPS`'s membership of this list, and `_temporal_disjoint_from_connect`
(which iterates this now-empty list and so always returns `False`) all survive as documented,
structurally-inert dead code. `services/intent/intent_service.py`'s TEMPORAL floor/keyword split
(`_requires_canonical_handler`, ~line 15380) and `canonical_handlers.py`'s `can_handle()` TEMPORAL
claim are UNCHANGED code (both read-only this unit) — gained a comment noting surface 1 no longer
produces a TEMPORAL claim at all, so this split is now reached only via the LLM classifier
(surface 2), never via surface-1 pre-classify.

**69 claimed rows, three distinct licensing shapes**: 50 are `TEMPORAL_PATTERNS`'s own corpus
rows (2 pre-existing + 48 sorted deposits); 19 are `CALENDAR_QUERY_PATTERNS`'s ledgered rows that
`TEMPORAL_PATTERNS` had reabsorbed after that list's own third-deletion (all disagreeing — claimed
`get_current_time`, never the ruled destination); and of the 50 own rows, **5 pass via a NEW gate
rule found this session — `row_disposition`'s "mis-serves this row" branch**: the router declined
(CLARIFY) AND `TEMPORAL_PATTERNS`'s own claim disagreed with the ruled destination (`pull up my
calendar`, `schedule check for today`, `show all events`, `when's my next free slot`, `what's my
available time` — all claimed `get_current_time`, ruled `week_calendar`/`meeting_time`), so the
pattern was deterministically WRONG for these rows and deleting it can only improve the fallback,
never worsen it — documented per-phrase in the ledger's new `misserved_at_deletion` field.

**The 19 ex-CALENDAR reabsorptions are now resolved**: `CALENDAR_QUERY_PATTERNS`' ledger entry's
`known_reabsorptions` gained a `"resolved_by": "TEMPORAL_PATTERNS deletion 2026-10-01"` tag on
each of the 19 (history kept, not deleted); empirically confirmed (direct `claim_for_phrase`
probe against the live, now-tombstoned `PreClassifier`) that all 69 claimed phrases — the 50 own
rows AND the 19 ex-CALENDAR ones — are genuinely UNCLAIMED by any surviving surface-1 list, zero
new reabsorptions.

**Mechanism additions, both needed by this entry specifically**:
1. **`misserved_at_deletion`** (`check_deleted_entry_non_regression`, `scripts/
   inversion_phase3_deletion_gate.py`): the "mis-serves this row" proof is a one-time fact about
   the DELETED pattern's own (wrong) claim, and can never be re-derived by the non-regression
   checker's synthetic-claim re-proof (which deliberately carries the CORRECT target op, not the
   deleted pattern's wrong one — so the mis-serve condition structurally can't fire on it). The
   re-verified invariant instead: the phrase must stay UNCLAIMED (strictly as safe or safer than
   being wrongly claimed) — a reclaim by any OTHER pattern still falls through to the existing
   reclaim-and-`known_reabsorptions` branch, so this escape never bypasses documentation.
2. **`gate.CURRENT_LIVE_CATEGORIES`**: a shared constant for the `--live` set every Phase-3
   deletion run has used throughout this epic, promoted when `TestChatPointersReachabilityRatchet`
   `._phase3_ledger_resolve` (`tests/test_architecture_enforcement.py`) needed it — the
   `page:/settings/preferences` POINTER resolves through `TEMPORAL_PATTERNS`'s ledger entry, which
   now carries a MISMATCH-but-live-route row (`what is on my calendar`, reabsorbed from
   `CALENDAR_QUERY_PATTERNS`); `_phase3_ledger_resolve`'s old `cats=None` call failed non-regression
   for the WHOLE entry over that one unrelated row, blocking every other phrase (including the
   POINTER's own) from resolving. Fixed by passing `gate.CURRENT_LIVE_CATEGORIES` — matching
   production's actual live flag, which is what this ratchet exists to confirm against.
   `TestDeletedPatternListsLedger._LIVE_CATS` (`tests/unit/test_inversion_phase3_deletion_1595.py`)
   now references the same constant instead of a second hand-copied literal.

**A POINTER swap, not a new corpus deposit**: `page:/settings/preferences`'s canonical utterance
was `"what time is it for me?"` — never itself a corpus row (TEMPORAL_PATTERNS claimed it only via
substring match). Depositing it fresh would add an UNSCORED corpus row (no frozen router report has
ever seen that exact phrase, and scoring one costs a live LLM call this unit's dispatch forbids),
which would fail `check_deleted_entry_non_regression` for the entire `TEMPORAL_PATTERNS` entry, not
just this phrase. Swapped to `"what time is it?"` instead — already one of the ledger's 69 verified
`rows_claimed_at_deletion` (pre-existing, MATCH@0.99) — same destination, zero new corpus/scoring
needed; the "for me" framing was flavor text for this one example utterance, not load-bearing for
the page or the default-zone-copy behavior it demonstrates.

**Every broken surface-1 pin converted, never deleted**, across 12 test files (the largest
conversion count of the four deletions — TEMPORAL_PATTERNS' vocabulary was the broadest and the
most heavily depended-on by OTHER tests' fixture phrases, not just its own regression suite):
- `test_action_registry.py` — 3 `TestMultiIntentSubsumption` tests rewritten to pin the new reality
  (no TEMPORAL claim survives at all, for "check my calendar for conflicts", "what time is it?",
  "hello! what time is it?"); the `_KNOWN_TEMPORAL_REABSORPTION_EXAMPLES` skip-list from the third
  deletion removed (the one documentation example it exempted now declines cleanly, confirmed
  directly — no special-casing needed any more).
- `test_calendar_query_handlers.py` — the third deletion's own
  `test_meeting_time_variants_reabsorbed_by_temporal` (2 phrases pinning the TEMPORAL reabsorption)
  renamed to `..._resolved_after_temporal_deletion` and converted to the decline+inversion-routes
  idiom — the reabsorption it pinned is itself resolved by this deletion.
- `test_integration_connect_preclassifier_1417.py`, `test_keyword_disambiguation_901.py`,
  `test_reminder_query_preclassifier_1521.py` — `test_temporal_queries_unchanged*` groups (7 phrases
  total) converted to the decline+inversion-routes idiom (`_inversion_pin_helper
  .assert_inversion_routes`, `live_categories="read_temporal"`).
- `test_inversion_split_stand_down_1896.py` — `SPLIT_TURN` swapped a SECOND time (first swap was
  the second deletion's TODO_QUERY_PATTERNS removal): `"give me my standup and what time is it"` no
  longer genuinely splits into 2 intents (TEMPORAL half degrades to no claim) — swapped to `"give me
  my standup and what should i do next"` (STATUS_PATTERNS + PRIORITY_PATTERNS, unaffected by any of
  the five deletions to date).
- `test_multi_intent_connect_1505.py`, `test_multi_intent_temporal_span_1755.py` — the entire
  #1755 span-aware-suppression test file (6 tests) rewritten to pin the new reality: TEMPORAL never
  claims regardless of span, so every "disjoint span survives" assertion becomes "only the
  connect/GUIDANCE half survives, correctly single-intent now, since TEMPORAL has nothing left to
  be disjoint FROM"; `_temporal_disjoint_from_connect` itself is now permanently, structurally
  inert (documented in its own docstring and in `pre_classifier.py`'s tombstone comments).
- `test_original_message_1460.py` — `MULTI_INTENT_MESSAGE` ("What's my schedule today and show my
  todos") now claims ZERO intents (both halves' patterns deleted across the second and fourth
  deletions) — kept unchanged for its OWN still-valid reader-side keyword-detection use, but a new
  `STILL_CLAIMED_MULTI_INTENT_MESSAGE` ("give me my standup and what should i do next") replaces it
  in the one parametrize case that needs a genuinely multi-claiming message.
- `test_read_lane_destructive_greed_1756.py` — the largest single conversion: `TEMPORAL_READS` (14
  phrases) and `CALENDAR_READS` (3 phrases) moved OUT of `KEEP_CLAIMING` (there is no claim left to
  keep) into a new `TestTemporalReadsNowDeclineAtSurfaceOne` class pinning the decline directly,
  plus one Inversion-routing plumbing test for "what time is it"; 2 of
  `READS_MENTIONING_DESTRUCTIVE_VERBS`' phrases (which matched TEMPORAL's generic `\bdid.*
  yesterday\b`/`\bwhat.*yesterday\b`) swapped for STATUS-lane equivalents exercising the same
  mention-not-ask property.
- `test_spend_free_canonical_ratchet_1818.py` — `("TEMPORAL", "get_current_time")` REMOVED from
  both `PAIR_MESSAGES` and `SPEND_FREE` (not swapped — no replacement message exists, since
  TEMPORAL_PATTERNS claims nothing at surface 1 any more). **Discovered work, not resolved here**:
  a direct keyless probe (`real_intent_service.process_intent(message="what time is it?", ...)`,
  this session) confirms the turn now reaches `intent_classifier.classify()` (the full LLM
  classifier) — it no longer has a zero-LLM-touch path. But the failure that produces is
  `ContainerNotInitializedError` (wrapped `IntentProcessingError`), NOT `UnboundLLMKeyError` —
  `classifier.py`'s `self.llm` property resolves via `ServiceContainer.get_service("llm")` BEFORE
  any code path reaches this file's `request_spend_key` chokepoint. So: (a) this pair almost
  certainly now SPENDS in a fully-initialized deployment, but (b) the #1818 ratchet's
  instrumentation cannot currently measure that — a gap in chokepoint coverage for turns falling
  through to the full LLM classifier via the container-based `classify()` path, distinct from the
  `LLMClient`/`clients.py` paths the other `SPENDS` pairs cross. Flagged in the test file's own
  NOTE comment for Lead/Arch/CXO (the #1818 gate's owners) — not guessed at or silently patched.

**Reachability ratchet**: the `page:/settings/preferences` POINTER (the only time-shaped POINTER
row) swapped utterance as described above; confirmed resolving via `phase3-deletion-ledger` after
the `gate.CURRENT_LIVE_CATEGORIES` fix. No other POINTER/`pin:` row is time-shaped (grep-confirmed
for `get_current_time`/temporal vocabulary across `chat_pointers.py`).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 496 → 440
(496 − 56 = 440; `pattern_literal_counts.total_literal_count()` confirms 440 post-deletion).

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/intent/` — **5020/5020**
passed (no subset); `tests/test_architecture_enforcement.py` + `tests/unit/
test_inversion_phase3_deletion_1595.py` — **98 passed, 1 xfailed**, ceiling exact at 440;
`scripts/run-sweep.sh ratchets` — **73 passed, 1 xfailed**, mypy gate unchanged (24 ratcheted
codes at ceiling, total=1121). `ruff format`/`ruff check --fix` clean (1 file reformatted,
whitespace only). No LLM calls anywhere in this unit — every router verdict consulted is a frozen,
already-scored report, or a monkeypatched stub in tests; the one live-process probe used to
characterize the #1818 discovered-work finding ran keyless and ended in a refusal before any
provider call, confirmed by direct inspection of the traceback, not inferred.

### Fifth deletion (2026-10-02): `GITHUB_QUERY_PATTERNS`

The gate's `--list GITHUB_QUERY_PATTERNS --live read_status,read_referent,read_synthesis,
create_todo,create_reminder,read_strategic,read_temporal,delete_todo` call (run BEFORE deletion)
read **GO, 64 literals, 66/66 claimed rows, 0 "needs a corpus row"** — every one of the 64
literals is exercised by at least one claimed row (the gate's own pattern→corpus conversion
check), unlike CALENDAR/TEMPORAL this list carries no `shadowed_literals`. Verdict of record: the
served-model (Haiku) baseline (`inversion-phase1-shadow-score-2026-10-01-haiku-baseline.md`) plus
the GitHub-specific rescore (`inversion-phase3-github-rescore-02-2026-10-01.md`, 53 rows after
CXO/PPM rulings + review_issue/list_issues description sharpening), five individually-ruled rows
(CXO/PPM day-bundle rulings, `inversion-phase3-ruled-rows-rescore-2026-10-01-{19,20,43,44,52}.md`),
and the original full-corpus review table (`inversion-phase1-shadow-score-2026-09-25.md`, 7
REVIEW-agrees rows). All 66 claimed rows are this list's OWN corpus rows — unlike CALENDAR's 19
ex-TEMPORAL and TEMPORAL's 19 ex-CALENDAR, no sibling-list reabsorption existed to resolve at
deletion time; 1 row ("prs needing review") passes via `row_disposition`'s "MISMATCH but the
router's own route live via group" branch (the router independently routes `list_prs@0.95` while
the corpus rules this a floor ask — the live consult owns the phrase regardless).
`GITHUB_QUERY_PATTERNS`'s 64 literals were then emptied to `[]` (same tombstone form) — the class
attribute, the claim branch (`pre_classify`'s GITHUB_QUERY_PATTERNS if-block with its action
sub-cases and the `_github_read_claim_blocked` destructive-ask guard), the mirrored branch in
`detect_multiple_intents` (`_get_github_action`, `_GITHUB_GATED_RAIL_ACTIONS`),
`detect_multiple_intents`'s pattern-groups table entry, and the GITHUB-subsumes-STATUS
subsumption filter (`_apply_subsumption_filter`'s `github_specific_query_actions` branch, ~line
2481 — its action names are produced ONLY by this list's own now-dead claim paths) all survive as
documented, structurally-inert dead code.

**One post-deletion reabsorption, agreeing — not nineteen, this time**: the empirical
`claim_for_phrase` probe (against the live, now-tombstoned `PreClassifier`) found exactly ONE
reabsorption across all 66 phrases: "any update on the next milestone" is now reclaimed by
`STATUS_PATTERNS`'s own pre-existing `\bnext milestone\b` literal — a BYTE-IDENTICAL duplicate
that predates this deletion by months (git blame: commits `33f3a43ad4`/`dc467511eb`, #898/#1039
era), previously shadowed because `GITHUB_QUERY_PATTERNS`'s earlier if-chain position (and its own
broader `\bwhen.*milestone\b` literal) matched first. STATUS_PATTERNS's claim
(`get_project_status`) is byte-identical to this row's ruled destination (router=
`get_project_status@0.85`, MATCH) — AGREEING, the same shape TODO_QUERY_PATTERNS' PRIORITY_PATTERNS
case (first ledger entry) established, not a new mechanism. `check_deleted_entry_non_regression`
needed NO modification for this deletion — the pre-existing agreeing-reclaim branch already covers
it. The other 65 phrases are genuinely unclaimed by any surviving surface-1 list (confirmed
empirically). Post-deletion gate census: `corpus denominator: 382 rows total = 167 claimed + 215
unclaimed` (was 232 claimed + 150 unclaimed; 232 − 167 = 65 = 66 minus the 1 reabsorbed — STATUS_
PATTERNS's own claimed-row count rose 51 → 52 in the same `--all` run). `gate --all` confirms
`GITHUB_QUERY_PATTERNS 0 0 NO ROWS`.

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 440 → 376
(440 − 64 = 376; `pattern_literal_counts.total_literal_count()` confirms 376 post-deletion).

**Every broken surface-1 pin converted, never deleted**, across 19 test files — GITHUB_QUERY_
PATTERNS' vocabulary (issues/PRs/milestones/releases/labels/branches/shipped/stale, plus the
close/reopen/comment destructive-rail actions) was the most heavily depended-on of the five
deletions by OTHER tests' fixture phrases and end-to-end arm steps, not just its own regression
suite:
- `test_pre_classifier_milestones_releases_1039.py`, `test_pre_classifier_labels_branches_1040.py`
  — both tested `PreClassifier._matches_patterns`/`_get_github_action` directly against the (now
  empty) list; every `test_positive_match`/`test_existing_patterns_unchanged` converted from
  "matches + correct action" to "does not match"; a new `TestInversionRoutesSurvive` class in each
  pins 2 representative live-routes proofs (stubbed router, no LLM) for
  `list_milestones_query`/`list_releases_query`/`list_labels_query`/`list_branches_query` (all
  flip_group `read_status`, confirmed via direct probe of `get_action_workflows()`).
- `test_github_query_handlers.py` — `TestPreClassifierRoutingIntegration` and
  `TestListPRsPreClassifierRouting` converted to assert `pre_classify(...) is None`; a new
  `TestGithubInversionRoutesSurvive` pins 4 live-routes proofs (shipped_query, stale_prs_query,
  review_issue_query [flip_group `read_referent`], list_prs_query [`read_status`]).
  close_issue_query/comment_issue_query are DELIBERATELY excluded from the live-routes pin —
  **discovered work, not resolved here**: a direct probe of `get_action_workflows()` confirms BOTH
  have `flip_group=None`, i.e. no registered live-rail key at all, so unlike `get_current_time`
  (which the fourth deletion gave a rail entry before deleting its pattern) there is NO zero-LLM
  path left for `close issue #N` / `comment on issue #N` — the same shape as the fourth deletion's
  "what time is it" gap, flagged to Arch/CXO, not resolved in this unit either.
- `test_read_lane_destructive_greed_1756.py` — `TestGithubLaneDestructiveGreed1794`'s per-claim
  discrimination tests (`test_gated_rail_claims_keep_their_lane`, `test_plain_reads_unchanged`)
  converted to assert decline on both surfaces (the discrimination logic they tested is now dead
  code — nothing left to discriminate); a new `TestGithubPatternsNowDeclineAtSurfaceOne` pins 2
  live-routes proofs for the plain-read actions.
- **The close/reopen/comment arm-step casualty, six files**: `close_issue_query` and
  `reopen_issue_query`/`comment_issue_query` have no flip_group, so every END-TO-END test that
  armed a `#1190`/`#1650`/`#1509`/`#1641`/`#1648`/`#1571`/`#1627`/`#1630` confirm gate via a bare
  `process_intent(message="close issue #108", ...)` against an EXPLOSIVE-LLM `live_service` fixture
  broke — that bare call previously resolved deterministically for free via this list, and now has
  no zero-LLM path at all. Converted (never weakened): each file gained an inline or shared
  `classify()` monkeypatch that returns the canned `close_issue_query`/`reopen_issue_query`/
  `comment_issue_query` Intent for the EXACT arm message(s) the test sends, and re-raises the SAME
  "LLM boundary touched" signal for any other message — so every later assertion in each test
  (yes/no/cancel/off-intent/#1631-prose/#1650-crisp-accept/#1567-repo-clarification mechanics)
  is proved exactly as before. Touched: `test_acceptance_contract_1739.py` (`_arm_close_confirm`),
  `test_destructive_confirm_1190.py` (`_stub_close_reopen_classify`, 7 call sites),
  `test_confirm_crisp_accept_1650.py` (`_stub_close_classify`, 4 call sites),
  `test_consent_gate_1509.py`, `test_repo_wiring_1641.py` (`_stub_github_arm_classify`, shared
  across reopen + comment), `test_action_fabrication_1648.py`, `test_drafted_issue_1571.py`,
  `test_drafted_issue_body_steal_1627.py`, `test_drafted_issue_subjectless_1630.py` (one inline
  stub each — the SAME off-intent shape: "close issue #108" abandons an armed draft and arms its
  own #1190 confirm).
- `test_action_registry.py::test_single_intent_not_affected` — swapped "Close issue #42" for "What
  branch are we on" (`LOCAL_GIT_STATUS_PATTERNS`, same QUERY category, unaffected by any of the
  five deletions).
- `test_subsumption_1084.py` — the WHOLE file's premise (#1084's GITHUB-subsumes-STATUS collapse)
  is now vacuous: "What's the next milestone?" only ever matched `STATUS_PATTERNS` now (GITHUB
  can't contribute a competing QUERY claim any more), so there is nothing left to subsume.
  Converted every test to pin the new reality (single-intent, STATUS/get_project_status, not
  QUERY/list_milestones_query) rather than assert a now-impossible collapse; the pure-QUERY control
  case ("list milestones") swapped to "what branch are we on" (its own GITHUB-based control phrase
  no longer claims at all either).
- `test_inversion_multi_intent_unit4_1595.py` — **the hardest conversion of the five deletions**:
  the file's three core split turns paired "what are my open issues" (GITHUB, list_issues_query)
  with "what did we create this session" (SESSION_ACTIVITY_QUERY_PATTERNS); with GITHUB gone the
  paired turn stopped splitting into two siblings at all (collapsed 2 intents → 1, confirmed
  empirically). Swapped the first segment to "what branch are we on"
  (`local_git_status_query`, confirmed still splitting, QUERY category, registered READ rail key)
  — updated the `TURN_*`/`SEG_ISSUES_AND` constants, every `list_issues_query` expected-action
  assertion, the greeting-prefix segment-boundary assertion (the new literal requires the FULL
  phrase, so unlike GITHUB's partial-match shadowing the greeting no longer shifts where the
  segment starts), `_named_delete_target`'s expected output ("what are open issues" → "what branch
  are", verified via direct call), and the `todo_boundary` fixture's first row (`_todo("open
  issues")` → `_todo("branch check")`, verified via `fuzzy_todo_match_score` = 0.33 against the
  0.3 threshold, uniquely) plus its 6 downstream literal-text assertions. **One test needed a
  DIFFERENT swap, not the reused one**: `test_the_destructive_phrasings_the_dispatch_named_do_not_
  split` relies on the `#1794`-family destructive-ask guard suppressing a READ claim when the
  destructive ask comes FIRST — `LOCAL_GIT_STATUS_PATTERNS` is NOT a member of `_READ_LANE_GROUPS`
  (confirmed by inspection), so it does not get suppressed (measured: still 1 intent, not 0, in the
  write-first ordering); used "give me my standup" (`STATUS_PATTERNS`, which IS a `_READ_LANE_
  GROUPS` member) for that one test instead, reproducing the exact suppression property —
  `get_project_status` has no WorkflowEntry (floor-routed, #925) so this phrase is deliberately NOT
  reused for the rail-dispatchability tests elsewhere in the file.
- `test_inversion_counterfactual_1668.py` — two tests needed "show my issues"/`list_issues`
  swapped to "what branch are we on"/`local_git_status` (an alias of the same rail entry_point,
  same canonical shape) to keep the "deterministic surface claims it, zero LLM calls" property the
  legacy-counterfactual shadow check pins.

**Two findings surfaced, neither caused by this deletion, both left for the Lead/Arch rather than
silently absorbed**:
1. `tests/unit/services/test_pre_classifier.py::test_current_time_still_routes_to_temporal` — root
   cause is the FOURTH deletion (`TEMPORAL_PATTERNS`, commit `dfec3e908d`, 2026-10-01); confirmed
   via `git show HEAD:services/intent_service/pre_classifier.py` that `TEMPORAL_PATTERNS` was
   already `[]` before this unit touched anything. This file sits outside the directory scope that
   commit's own "full suite" verification covered (`tests/unit/services/intent_service/` +
   `tests/unit/services/intent/`, not the sibling `tests/unit/services/` root) — surfaced only
   because this unit's required test scope happens to include it. Converted anyway (decline + a
   new live-routes pin), same idiom as the fourth deletion's own TEMPORAL conversions.
2. `test_reminder_clear_pick_target_1906.py::TestOffIntentReleases::test_unrelated_command_
   releases` — `_handle_pick_target_turn`'s #1899 "unrelated command releases the pick"
   discriminator (`services/intent_service/reminder_clear.py` ~1481) checks `PreClassifier.
   pre_classify(text) is not None` first, falling back to `read_op_claims_turn` (READ-only)
   second. With `GITHUB_QUERY_PATTERNS` gone, "close issue #108" passes NEITHER check any more
   (pre_classify declines; `close_issue_query` is destructive, not a READ op) — confirmed
   empirically: the discriminator now returns a "Still not sure which one" RE-ASK instead of
   releasing. This is live PRODUCT behavior, not a test-fixture artifact — converted the TEST
   (swapped the example to "give me my standup", which still releases correctly) WITHOUT touching
   product code, but the underlying gap (no destructive/non-READ surviving pattern can trigger
   this release path any more) is real and unresolved.

Also found, OUT OF SCOPE for this unit and unrelated to it: `tests/e2e/test_1897_two_part_turn_
live.py::test_shape_is_the_1897_shape_before_spending` is ALSO currently broken by the fourth
deletion (asserts `pre_classify(...).action == "get_current_time"`, which no phrase can ever
produce again now that `TEMPORAL_PATTERNS` is `[]` — confirmed present and already broken at
`HEAD`, before this session). Unlike the `test_pre_classifier.py` case above, this one could NOT
be fixed by a simple phrase swap to a different action — `get_current_time` is the ONLY action the
#1897 shape's design names, and no substitute preserves what the test is actually proving (the
specific temporal+github "both live READs" pairing). Left unconverted and reported, not guessed
at — a genuine test-design question for the Lead/Arch, not a mechanical pin update.

Full suite: `tests/unit/services/intent_service/` + `tests/unit/test_inversion_phase3_deletion_
1595.py` + `tests/test_architecture_enforcement.py` + `tests/unit/services/test_pre_classifier.py`
— **5127 passed, 1 xfailed, 0 failed** (full run, not a subset; ceiling exact at 376).
`scripts/run-sweep.sh ratchets` — 1 PRE-EXISTING unrelated failure found
(`test_todo_marker_ratchet`, count 36 vs frozen ceiling 35) — confirmed via independent
re-computation of the exact same scan (`services/` + `web/` `.py` files only, excluding archive/
`__pycache__`) that ZERO of the 36 hits are in any file this unit touched, and that the scan never
even looks at `tests/` (where every change in this unit lives) — a discovered, unrelated debt
ceiling breach, not caused here. `ruff format`/`ruff check --fix` clean (5 files reformatted,
whitespace-only; 0 lint errors). No LLM calls anywhere in this unit — every router verdict
consulted is a frozen, already-scored report, or a monkeypatched stub in tests.

### Sixth deletion (2026-10-02): `PRIORITY_PATTERNS`

The gate's `--list PRIORITY_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,
create_reminder,read_strategic,read_temporal,delete_todo` call (run BEFORE deletion) read **GO, 47
literals, 42/42 claimed rows, 0 [FAIL]** — 5 of the 47 literals were flagged "needs a corpus row
before deletion" (unexercised): 2 shadowed by an earlier, broader sibling literal in this same list
(`\bwhat are my priorities\b` shadowed by `\bmy priorities\b`; `\bwhat'?s most important\b` shadowed
by `\bmost important\b`), 3 genuinely never exercised by any corpus row in any category
(`\bmost important task\b`, `\bmost important work\b`, `\bwhat.*work on next\b`) — see the ledger's
`shadowed_literals` for the full per-literal account. Destination: `get_top_priority`, a
FLOOR-disposition action (no WorkflowEntry; confirmed via `get_action_workflows()` — same shape as
`get_project_status`/`get_current_time` before their own rail entries, where applicable). All 42
claimed rows are this list's OWN corpus rows — no sibling-list reabsorption existed at deletion
time, unlike CALENDAR's/TEMPORAL's.

**A new condition, (d), licensed 2 rows that neither MATCH, agreeing-REVIEW, nor live-MISMATCH would
cover** — Arch's 2026-10-02 ruling, closing the morning's gate-defect review: a FLOOR-destination row
whose pattern claim agrees with the ruling, but whose router MISMATCHES to a non-live op, is
ordinarily NOT OK to delete (the pattern is the live path and serves the row right). Condition (d)
licenses it anyway when a frozen surface-2 probe (the LLM classifier, i.e. what the phrase reaches
once surface 1 is gone) shows the SAME destination category on EVERY sample — the user reaches the
same floor either way, so the pattern was never load-bearing. Two rows qualify: "what are my focus
areas this sprint" (router MISMATCH → `get_contextual_guidance@0.72`) and "what's my focus this
week" (router MISMATCH → `week_calendar@0.72`) — both below the live dispatch threshold regardless.
A frozen N=5 probe (`inversion-phase3-surface2-floor-probe-2026-10-02-n5-anthropic.md`, served
`anthropic:claude-sonnet-4-6`, checked first per `SURFACE2_FLOOR_PROBES`' order; the sibling gpt-4o
report carries the same two phrases, also 5/5) shows the LLM classifier landing BOTH phrases in the
PRIORITY category on all 5 samples each — `get_top_priority` is reached by category once surface 1
declines, same as it was reached by pattern before. 2 further rows pass via the pre-existing
`misserved_at_deletion` shape (fourth deletion's shape, TEMPORAL_PATTERNS): "show priorities for
this sprint" and "not sure what to do about this" both had a claim that DISAGREED with the ruled
destination (floor / `get_contextual_guidance` respectively) AND the router independently declined —
deleting a deterministically-wrong fallback cannot regress a row that was already unserved
correctly.

`PRIORITY_PATTERNS`'s 47 literals were then emptied to `[]` (same tombstone form) — the class
attribute, the claim branch (`pre_classify`'s PRIORITY_PATTERNS if-block), and
`detect_multiple_intents`'s pattern-groups table entry all survive as documented, structurally-inert
dead code.

**Zero post-deletion reabsorptions** — the empirical `claim_for_phrase` probe (against the live,
now-tombstoned `PreClassifier`) found NO reabsorption across all 42 phrases. STATUS_PATTERNS,
GUIDANCE_PATTERNS, TODO_COMPLETE_PATTERNS, and ANALYSIS_PATTERNS were specifically checked (per the
dispatch's watch-list, those being the lists most likely to carry a shadowed duplicate literal, the
same shape GITHUB's "next milestone" and TODO_QUERY's "what should I do next" both found) — none
reclaim any of the 42 phrases. Post-deletion gate census: `corpus denominator: 382 rows total = 125
claimed + 257 unclaimed` (was 167 claimed + 215 unclaimed; 167 − 125 = 42, exactly the full claimed
count — no partial reabsorption to net out, unlike GITHUB's −65/−66). `gate --all` confirms
`PRIORITY_PATTERNS 0 0 NO ROWS`.

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 376 → 329
(376 − 47 = 329; `pattern_literal_counts.total_literal_count()` confirms 329 post-deletion).

**`check_deleted_entry_non_regression` gained ONE new sibling branch** for condition (d)'s shape,
keyed by a new ledger field `surface2_verified_at_deletion`: a documented phrase is OK iff it is
still UNCLAIMED by surface 1 post-deletion — the SAME narrower, cheaper re-verified invariant
`misserved_at_deletion` already uses (the original N=5 probe proof is a one-time fact recorded at
GO time and is never re-derived on each future test run, since this function does not thread
`phrase` into its own `row_disposition` re-proof call). Pinned with two new synthetic tests in
`tests/unit/test_inversion_phase3_deletion_1595.py`
(`test_passes_for_a_surface2_verified_phrase_still_unclaimed` /
`test_fails_for_the_same_phrase_without_the_surface2_documentation`), using the real "what are my
focus areas this sprint" row.

**Every broken surface-1 pin converted, never deleted**, across 6 test files. Two fixture classes of
breakage recurred from earlier deletions in this epic — a soon-to-be-deleted-list avoidance rule and
the usual "the swapped-to phrase/list itself got deleted next" cascade:
- `test_contextual_query_handlers.py::test_priority_patterns_still_work` — directly tested
  `PreClassifier.pre_classify` against 5 PRIORITY phrases, all mapping to `get_top_priority`.
  Converted "matches + correct action" to "does not match" (decline) for all 5; no
  `TestInversionRoutesSurvive`-style pin added, since `get_top_priority` has NO WorkflowEntry (the
  Inversion never dispatches it by name — once surface 1 declines, the phrase reaches the floor by
  CATEGORY through the LLM classifier, nothing a stubbed-router pin can prove).
- `test_todo_query_handlers.py::test_next_todo_query_variants` — this test's OWN prior docstring
  documented a sibling-reabsorption finding from the SECOND deletion (TODO_QUERY_PATTERNS): "what
  should I do next" was claimed by PRIORITY_PATTERNS' own pre-existing identical literal, agreeing
  with the ruling. With PRIORITY_PATTERNS itself now gone, that sibling is gone too — the phrase is
  genuinely unclaimed at surface 1 for the first time. Converted to pin the decline (same
  no-WorkflowEntry rationale as above — no routes-survive pin possible for `get_top_priority`); the
  file's other `list_todos_query` assertions (rail-live, `read_status`/`read_strategic`) are
  unaffected and untouched.
- `test_spend_free_canonical_ratchet_1818.py` — `("PRIORITY", "get_top_priority")` removed from
  `PAIR_MESSAGES` (same idiom as the fourth deletion's `("TEMPORAL", "get_current_time")` removal):
  step 1 of this ratchet needs `pre_classify` to directly produce the pair, which it no longer can.
  Simpler case than TEMPORAL's, though — `get_top_priority` was already a measured-`SPENDS` pair
  (never `SPEND_FREE`), so removing it changes nothing the #1818 gate actually protects; a NOTE
  explains the distinction and flags (not resolves) whether the action is reachable at all via the
  LLM classifier's own re-categorization, which is outside this ratchet's step-1 contract.
- `test_inversion_split_stand_down_1896.py` — the THIRD swap of this file's `SPLIT_TURN` fixture in
  this epic (TODO_QUERY_PATTERNS → `second deletion`; TEMPORAL_PATTERNS → `fourth deletion`; now
  PRIORITY_PATTERNS → `sixth deletion`). "give me my standup and what should i do next"
  (STATUS_PATTERNS + PRIORITY_PATTERNS) degraded to a single STATUS claim once PRIORITY_PATTERNS
  emptied. Swapped to "give me my standup and what branch are we on" (STATUS_PATTERNS +
  LOCAL_GIT_STATUS_PATTERNS, confirmed still splitting into exactly 2 intents) —
  STATUS_PATTERNS/GUIDANCE_PATTERNS deliberately avoided for the SECOND half specifically, both
  being the next two lists scheduled for deletion in this epic.
- `test_pre_classifier.py::test_priority_next_patterns_not_greedy` — the first two of three
  assertions ("What's next?", "What should I work on next?") expected PRIORITY; both now decline.
  The third ("What's the next milestone?" → STATUS, unaffected by PRIORITY's own deletion) is
  unchanged — the "not greedy against milestone" property it demonstrates no longer needs PRIORITY
  to be a live competitor to prove STATUS wins.
- `test_inversion_phase3_deletion_1595.py` (this unit's own gate-mechanics pins) — THREE synthetic
  non-regression fixtures were built on real corpus rows PRIORITY_PATTERNS itself used to claim
  (`test_fails_when_phrase_is_claimed_by_a_surviving_list`'s "surviving list" WAS PRIORITY_PATTERNS;
  the floor-reclaimed-but-documented-disagreeing pair's "list priorities for the team" was claimed by
  PRIORITY_PATTERNS) — the same fixture-breakage shape TEMPORAL's own deletion caused here before it.
  Checked empirically (2026-10-02): no surviving list besides STATUS_PATTERNS claims ANY
  floor-expected corpus row today — but STATUS_PATTERNS/GUIDANCE_PATTERNS were deliberately avoided
  per the dispatch's own swap-avoidance rule (both are the next two lists scheduled for deletion).
  Found an alternative shape instead: a real `expected: "plan"` corpus row (the #1606 two-op plan
  row) that SET_DEFAULT_REPO_PATTERNS claims as `set_default_repo` — `row_disposition` treats
  `"plan"` identically to `"floor"` in every branch this shape exercises, so it is a structurally
  equivalent, non-STATUS/GUIDANCE replacement for all three fixtures. `TestPriorityPatternsVerdictIsReported`
  (the class exercising the verdict-reporting mechanism itself, previously swapped to PRIORITY_
  PATTERNS after TEMPORAL's own fourth-deletion breakage) swapped again, to `REPO_MANAGEMENT_
  PATTERNS` (2 claimed rows, GO) — plus a new `test_priority_patterns_now_claims_zero_rows` pin,
  mirroring `test_temporal_patterns_now_claims_zero_rows`.

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/test_architecture_enforcement.py` + the #1897 spend-free shape pin —
**5136 passed, 1 xfailed, 0 failed** (full run, not a subset; ceiling exact at 329). `scripts/run-sweep.sh
ratchets` — 1 PRE-EXISTING unrelated failure (`test_todo_marker_ratchet`, count 36 vs frozen ceiling
35), same as the fifth deletion found and left — confirmed unrelated again (no file this unit touched
is in its scan scope). `ruff format`/`ruff check --fix` clean. No LLM calls anywhere in this unit —
every router verdict consulted is a frozen, already-scored report (including the two N=5 surface-2
probe reports), or a monkeypatched stub in tests.

### STATUS_PATTERNS deposits + two instrument rules (2026-10-01, scored, NOT deleted)

56 literals, 51 claimed rows after a 46-row deposit lane (5 literals proven unreachable: 4 are
byte-identical duplicates of `GITHUB_QUERY_PATTERNS` / `MILESTONE_STATUS_INLINE_PATTERNS` literals
checked earlier in the if-chain, 1 is shadowed by its own shorter sibling). The claim branch has no
per-literal branching — every literal returns `get_project_status`, which `action_registry.py`
marks **FLOOR** (no WorkflowEntry; #925). The score exposed two places the instruments disagreed
with production, both fixed and pinned the same day:

1. **Scorer — a FLOOR-disposition `action:` expectation is a floor expectation**
   (`_expected_action_is_floor_disposition`, `scripts/inversion_phase1_shadow_score.py`).
   Production serves `get_project_status` from the floor whether the router names it, declines
   (NONE) or asks (CLARIFY) — all three land the user in the same place, so all three MATCH. The
   first score read 15/46 because NONE/CLARIFY were counted against rows the router could not
   have improved; the re-score reads 29/46 with only genuine disagreements left (router prefers
   `list_todos_query` for "my tasks" ×7, `attention_query` for "my assignments"/"what I'm working
   on" ×5, `generate_report` for "status/progress report" ×2 — rulings owed, PPM/CXO). The lookup
   goes through `get_disposition` on an action the registry actually knows; the registry's own
   FLOOR default for unknown pairs is NOT credited.
2. **Gate — a router op below the dispatch threshold is a stand-down, not "the consult owns this
   phrase"** (`row_disposition`, `scripts/inversion_phase3_deletion_gate.py`). `consult_inversion_live`
   dispatches only at confidence ≥ `live_min_confidence()` (0.8); the MISMATCH-but-router-live rule
   now requires the same, read from the same function. Found on "show today's assignments" →
   `meeting_time` @0.6, which the old rule would have marked OK.

Corpus corrections (anchored, not guessed): `upcoming milestones` → `list_milestones` (the 10-01
GITHUB milestone ruling), three "current/active projects" phrasings → `manage_portfolio` (the lane's
own `what are my projects?` anchor), and three "archived projects" phrasings → the dedicated
`list_archived_projects` entry via `RULED_EXPECTATIONS` (the corpus-1283 `REVIEW` and the
`manage_portfolio` expectations both predated that entry; Haiku names it @0.99 on all three,
re-scored 3/3). Gate read with the 8-token live flag: **47 OK / 4 FAIL — NO-GO**. The four: "what am I
working on?" (router `get_top_priority` vs `category:STATUS`, both floor families — a ruling), and
three sub-threshold rows (`session_activity_query` @0.72/@0.7, `meeting_time` @0.6) where the
consult stands down and the deleted pattern would hand the phrase to the LLM classifier, which the
gate cannot measure. Corpus 336 → 382; ceiling unchanged at 440. Reports:
`inversion-phase3-status-score-2026-10-01.md` (15/46, pre-rule) and
`inversion-phase3-status-rescore-2026-10-01.md` (29/46), both in `PHASE3_REPORTS`.

### Seventh deletion (2026-10-02): `STATUS_PATTERNS` (partial — 52 of 56)

The first **PARTIAL** deletion in this epic. BEFORE gate
(`--list STATUS_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,
create_reminder,read_strategic,read_temporal,delete_todo`): **GO (partial) — 4 load-bearing
literal(s) SURVIVE, deleting the other 52: ceiling 329 → 277**. 56 literals, 52 corpus rows claimed
(48 `[OK]`, 4 `[FAIL]`). The 4 `[FAIL]` rows are exactly the 4 survivors: each is a MATCH on a
NON-LIVE op (`get_project_status` has no WorkflowEntry — #925 FLOOR) where the consult stands down
and a frozen N=5 surface-2 probe does NOT show the LLM classifier landing in STATUS on every
sample:

| survives | corpus row | surface-2 (10 samples) |
|---|---|---|
| `\bnext milestone\b` | "any update on the next milestone" | 9/10 |
| `\bcurrent work\b` | "can you summarize my current work" | 5/10 |
| `\bproject overview\b` | "give me a project overview" | 4/10 |
| `\bproject landscape\b` | "what's the project landscape" | 0/10 |

**The partial rule**: a list whose FAILING rows are not uniformly covered by surface 2 does not go
NO-GO as a whole — the literals those specific rows depend on stay (load-bearing), and every other
literal in the list is deleted. `scripts/inversion_phase3_deletion_gate.py`'s `load_bearing_literals`
(added the same day the GUIDANCE/STATUS lane first hit this shape) resolves the survivor set via the
production matcher (`PreClassifier._first_pattern_match`), exactly as `unexercised_literals` does —
never a second regex pass. `STATUS_PATTERNS` is NOT emptied to `[]`: it becomes exactly the 4
survivor literals, each with a one-line comment naming the corpus row it carries. The claim branch
(`pre_classify`'s STATUS_PATTERNS if-block, ~line 1741) stays LIVE — unlike every prior (full)
deletion in this epic, there is no dead-code tombstone comment on the branch, because the list still
has 4 real, reachable literals.

Of the 48 `[OK]` rows: 18 pass via "expected action live via group" (`show_standup` /
`list_archived_projects` / `list_milestones` / `list_todos_query` / `generate_report` all have
registered flip_groups), 4 pass via "MATCH (ruled floor)" (the router declining IS the destination —
`\bwhat'?s assigned\b`'s floor-expected rows), 9 pass via the mis-serve escape (STATUS_PATTERNS'
single hardcoded claim `get_project_status` disagrees with the ruled destination — 6 PORTFOLIO-
collision rows the `my projects`/`my portfolio`/`active projects`/`current projects` family mis-
serves, plus 2 `floor`-ruled rows the pattern also mis-serves, plus "give me a project status
report" vs. `generate_report`), and 17 pass via the surface-2-floor shape this epic's sixth
deletion introduced: a frozen N=5 probe (both provider legs, 10/10 combined) shows the LLM
classifier landing the phrase in the STATUS category on every sample once surface 1 is gone.

**The literal→corpus-row audit the gate only prints on a full GO** (computed by hand for the
partial case, same method as `unexercised_literals`): 4 of the 56 literals were unexercised by any
STATUS-claimed row, all 4 inside the 52-to-delete set.

- `\bmy current work\b` — **shadowed WITHIN the list** by its own earlier, shorter sibling
  `\bcurrent work\b` (a SURVIVOR, checked first in list order — "current work" is a guaranteed
  substring of "my current work" preceded by a space, so the shorter pattern always claims first).
  Confirmed via `PreClassifier._first_pattern_match("my current work", STATUS_PATTERNS)` →
  `\bcurrent work\b`. Permanently unreachable, pre- and post-deletion.
- `\bwhat'?s the (?:next|upcoming) milestone\b`, `\bmilestone status\b`, `\bmilestone progress\b` —
  **CROSS-LIST shadowed**: byte-identical to literals inside the inline (non-class-attribute)
  `MILESTONE_STATUS_INLINE_PATTERNS` check (this file, Issue #1068), checked BEFORE
  `STATUS_PATTERNS` in `pre_classify`'s if-chain. This is the discovered-work incident of this unit
  (see below) — a first audit using `_first_pattern_match` against `STATUS_PATTERNS` ALONE (the
  wrong instrument: it proves reachability only WITHIN one list) found these 3 "reachable but
  unexercised" and triggered a STOP; `PreClassifier.pre_classify_with_pattern_list` (the real
  production if-chain) shows all three claimed by `MILESTONE_STATUS_INLINE_PATTERNS` first — no
  corpus deposits were needed. `\bnext milestone\b` is NOT in this shadowed set: it is reachable
  (e.g. "any update on the next milestone", which doesn't match the inline check's "what's the
  next/upcoming milestone" shape) and is one of the 4 survivors above — a PRE-EXISTING note in
  `scripts/build_inversion_corpus_phase0.py`'s STATUS deposit block comment had called it
  "structurally unreachable" too (true only before the fifth deletion emptied GITHUB_QUERY_PATTERNS'
  own shadowing copy of this literal); corrected in this unit's commit (block comment + the "any
  upcoming milestones for this project" row's own `notes` field, regenerated via
  `python scripts/build_inversion_corpus_phase0.py` — 385 rows unchanged, only `notes` text
  differs).

**Discovered-work incident, mid-dispatch**: the Coding Agent's first-pass audit used
`PreClassifier._first_pattern_match` against `STATUS_PATTERNS` alone to check literal reachability
— correct for the IN-LIST shadow (`\bmy current work\b`) but the WRONG instrument for a CROSS-LIST
shadow, since it never consults any other list or the real if-chain ordering. That audit flagged 3
literals as "genuinely unexercised and reachable" and STOPPED per the dispatch's explicit condition.
The Lead re-ran `PreClassifier.pre_classify_with_pattern_list` (the actual production entry point)
against the same 3 phrases and found all three claimed by `MILESTONE_STATUS_INLINE_PATTERNS` — a
fact the STATUS deposit lane had ALREADY discovered and documented the day before (`### STATUS_
PATTERNS deposits...` subsection above: "5 literals proven unreachable: 4 are byte-identical
duplicates of GITHUB_QUERY_PATTERNS / MILESTONE_STATUS_INLINE_PATTERNS literals... 1 is shadowed by
its own shorter sibling" — exactly these 4 plus `\bmy current work\b`, confirming the lane's
original finding independently). Lesson for future deletions in this epic: **`_first_pattern_match`
against a single list is the wrong reachability instrument whenever an EARLIER-CHECKED list or
inline check might also claim the phrase — `pre_classify_with_pattern_list` (or `claim_for_phrase`)
is the only instrument that reflects the real if-chain.**

**AFTER**: for each of the 48 deleted-literal rows, `claim_for_phrase` (both entry surfaces —
`pre_classify_with_pattern_list` AND `detect_multiple_intents`) was re-run against the live,
post-deletion `PreClassifier` — **ZERO reabsorptions**. All 4 survivor rows remain claimed by
`STATUS_PATTERNS` itself. `gate --all`: `STATUS_PATTERNS 4 4 NO-GO` (4 literals, 4 rows, all
`[FAIL]` — expected: a partial list's remaining literals ARE its own failing rows by construction).
Corpus denominator unchanged at 385 (77 claimed + 308 unclaimed, down from 125 claimed before this
deletion — 125 − 77 = 48, the full deleted-row count, no partial reabsorption to net out).
`gate --list GUIDANCE_PATTERNS` re-checked post-deletion: still **GO (partial)**, 3 survivors
(`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`) — unaffected by this
deletion (GUIDANCE is checked before STATUS in the if-chain, so its 3 FAIL rows were never
reclaimable by STATUS_PATTERNS' now-deleted `\bmy projects\b`/`\bmy portfolio\b` literals; this is a
structural re-confirmation, not a change this deletion caused).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 329 → 277
(329 − 52 = 277; `pattern_literal_counts.total_literal_count()` confirms 277 post-deletion). The
ledger-count pin (`test_real_ledger_has_the_first_eight_deletions`, renamed from "...seven...")
gains STATUS_PATTERNS as the 8th entry, with new assertions on `entry["partial"]` (`True`) and
`entry["surviving_literals"]` (the 4-literal set). The "a deleted list claims zero rows" pin family
(`test_temporal_patterns_now_claims_zero_rows` / `test_priority_patterns_now_claims_zero_rows`)
gained a sibling for the partial case, `test_status_patterns_now_claims_four_rows`: asserts exactly
4 rows (the 4 survivor phrases), all `[FAIL]`, `lv.deletable is False`.

**Every broken surface-1 pin converted, never deleted**, across 16 test files — by far the largest
conversion wave in this epic, because STATUS_PATTERNS' deleted vocabulary (tasks/status/progress/
standup/assignments/portfolio-noun phrasing) was the most heavily reused fixture vocabulary in the
whole intent-service test suite:

- `test_read_lane_destructive_greed_1756.py` — `STATUS_READS` (13 phrases) and 3 of
  `READS_MENTIONING_DESTRUCTIVE_VERBS`' 5 phrases ALL matched now-deleted literals. Swapped for 13 +
  3 phrases confirmed claiming deterministically at confidence 1.0 this session, drawn from
  STATUS_PATTERNS' 4 survivors, `COMPLETION_HISTORY_PATTERNS` (STATUS category), and
  `LOCAL_GIT_STATUS_PATTERNS` (#1044, QUERY category, untouched by any Phase 3 deletion) — same
  property (legitimate reads keep their claim; a destructive verb mentioned mid-sentence, not
  heading the ask, is a read about deletion, not a deletion).
- `test_subsumption_portfolio_write_family_1884.py` — the PORTFOLIO-subsumes-STATUS filter's
  `status_project_noun_overlap` set (`pre_classifier.py`, `_apply_subsumption_filter`) is a VALUE
  COPY of 9 STATUS_PATTERNS literals; 7 of the 9 are now deleted. Pruned the production set to its
  2 surviving members (`\bproject overview\b`, `\bproject landscape\b`) — not a new deletion
  decision, since `matched_status_patterns` is built by filtering `STATUS_PATTERNS` itself, so a
  member absent there could never match anyway. `TestOverlapSetIsValueCopyNotNewVocabulary`'s two
  guard-rail tests updated to the new 2-member set; `TestGenuineTwoTopicControlUnchanged`'s 3 tests
  and `TestUnaffectedControls::test_pure_status_ask_no_portfolio_claim_keeps_status` swapped their
  probe phrases from deleted literals (`status update`, `project status`, `what.*working on`) to
  the surviving `\bcurrent work\b`.
- `test_truncated_render_provenance_1738.py`, `test_subsumption_1084.py`,
  `test_keyword_disambiguation_901.py` — each had one STATUS-only control phrase using a deleted
  literal (`what.*working on` / `project status`); swapped to `\bcurrent work\b`'s "can you
  summarize my current work".
- `test_task_clarify_1654.py`, `test_ftux_interview_1688.py` (2 call sites),
  `test_reminder_clear_pick_target_1906.py` — the epic's recurring "a deterministically-claimed
  command releases without spending a router call / abandons a pick" discriminator fixture had
  already cycled through TODO_QUERY_PATTERNS → STATUS_PATTERNS' "give me my standup" across the
  second and fifth deletions; that literal (`\bmy standup\b`) is now gone too. Swapped to "what
  branch are we on?" (`LOCAL_GIT_STATUS_PATTERNS`, untouched by any Phase 3 deletion, confirmed
  claiming at confidence 1.0).
- `test_inversion_multi_intent_unit4_1595.py`, `test_inversion_split_stand_down_1896.py`,
  `test_original_message_1460.py` — all three needed a GENUINE two-claim split (one STATUS half +
  one other-lane half) to prove their respective properties (no destructive sibling ever emitted /
  the consult stands down on a real split / both surfaces populated on EACH intent); their STATUS
  half was "give me my standup" (now dead). Swapped to "can you summarize my current work" paired
  with "what branch are we on" / "delete my hydrate reminder" / "what should i do next" as
  appropriate per file — each reconfirmed splitting into exactly the expected intent count.
- `test_spend_free_canonical_ratchet_1818.py` — `("STATUS", "get_project_status")`'s probe message
  "project status" (deleted literal) swapped to "can you summarize my current work"; the pair
  itself is unaffected (STATUS_PATTERNS is partially emptied, not tombstoned).
- `services/intent_service/chat_pointers.py` (PRODUCT code, not a test) — the `page:/standup`
  CHAT_POINTERS entry's VERIFIED, user-facing utterance "give me my standup" no longer resolves
  deterministically. Swapped to "can you summarize my current work" (same destination, confirmed
  this session) to keep the `TestChatPointersReachabilityRatchet` ratchet's "LLM-free, verified"
  contract. **Known gap, flagged not fixed**: the replacement utterance no longer reads as an
  obvious path to the standup page specifically — no surviving STATUS_PATTERNS literal is
  standup-themed. `get_project_status` was always the generic STATUS destination this page resolved
  through (not a dedicated standup action), so the underlying mapping is unchanged; only the
  example phrase's user-facing legibility degraded.

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/unit/test_inversion_phase1_shadow_score_1595.py` +
`tests/test_architecture_enforcement.py` + the #1897 spend-free shape pin — **5166 passed, 1
xfailed, 0 failed** (full run, not a subset; ceiling exact at 277; re-run twice, identical both
times — once before and once after a JSON-ledger mishap, see below). `scripts/run-sweep.sh
ratchets` — 1 PRE-EXISTING unrelated failure (`test_todo_marker_ratchet`, count 36 vs frozen
ceiling 35), same as the fifth and sixth deletions found and left — confirmed unrelated again (no
file this unit touched is in its scan scope). `ruff format`/`ruff check --fix` clean on every
touched `.py` file. No LLM calls anywhere in this unit — every router verdict consulted is a
frozen, already-scored report (including all surface-2 probe reports), or a monkeypatched stub in
tests.

**Tooling incident, discovered and self-corrected mid-unit**: `ruff format`/`ruff check --fix` were
run with `scripts/inversion_phase3_deleted_patterns.json` in the file list (ruff is a Python
tool; it has no business touching `.json`). It silently rewrote the file introducing TRAILING
COMMAS after every array/object's last element — valid in nothing ruff actually targets, invalid
in JSON (`json.load` failed immediately: `Expecting value`). Caught by loading the file
immediately after the ruff run (never assume a formatter no-ops on a file type it wasn't asked to
touch); fixed by `git checkout HEAD -- scripts/inversion_phase3_deleted_patterns.json` (safe here —
own worktree, no committed work at risk, confirmed via `git diff HEAD` before discarding) followed
by a clean re-append via `json.dump`, never hand-edited. **Lesson for future deletions in this
epic: never pass `.json` paths to `ruff format`/`ruff check` — list only `.py` files.**

### Eighth deletion (2026-10-02): `GUIDANCE_PATTERNS` (partial — 18 of 21)

The second **PARTIAL** deletion in this epic. BEFORE gate
(`--list GUIDANCE_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,
create_reminder,read_strategic,read_temporal,delete_todo`): **GO (partial) — 3 load-bearing
literal(s) SURVIVE, deleting the other 18: ceiling 277 → 259**. 21 literals, 21 corpus rows claimed
(18 `[OK]`, 3 `[FAIL]`). The 3 `[FAIL]` rows are exactly the 3 survivors: each is a MATCH on a
NON-LIVE op (`get_contextual_guidance` has no WorkflowEntry) where the consult stands down and a
frozen N=5 surface-2 probe shows the LLM classifier landing EXECUTION 10/10 — never GUIDANCE on any
sample:

| survives | corpus row | surface-2 (10 samples, both legs) |
|---|---|---|
| `\bsetup.*projects?\b` | "I need to setup my projects" | 0/10 GUIDANCE (10/10 EXECUTION) |
| `\bset up.*projects?\b` | "I want to set up my projects" | 0/10 GUIDANCE (10/10 EXECUTION) |
| `\bset up.*portfolio\b` | "I'd like to set up my portfolio" | 0/10 GUIDANCE (10/10 EXECUTION) |

`GUIDANCE_PATTERNS` is NOT emptied to `[]`: it becomes exactly the 3 survivor literals, each with a
one-line comment naming the corpus row it carries and the probe that proves it EXECUTION, not
GUIDANCE. The claim branch (`pre_classify`'s GUIDANCE_PATTERNS if-block) and the
`INTEGRATION_CONNECT_PATTERNS` skip-guard (`patterns is PreClassifier.GUIDANCE_PATTERNS and
connect_claimed`) stay LIVE — same partial-list idiom as STATUS_PATTERNS' seventh deletion.

**Reachability audit**: all 21 literals were exercised 1:1 by exactly one claimed corpus row each
(confirmed via `PreClassifier._first_pattern_match` against each claimed phrase — no literal
unexercised, no corpus deposit needed). `claim_for_phrase`'s real if-chain (the gate's own by-list
grouping, which calls `pre_classify_with_pattern_list` then `detect_multiple_intents` — never a
within-list-only check) attributed all 21 claimed rows to `GUIDANCE_PATTERNS` itself; none of the 18
to-be-deleted literals was cross-list shadowed. Of the 18 `[OK]` rows: 17 pass via the surface-2-floor
shape (a frozen N=5 probe, both provider legs, 10/10 combined per phrase, landing the phrase in the
GUIDANCE category once surface 1 is gone), and 1 (`\bgetting started\b`, "just getting started here")
passes via the mis-serve escape — the literal claims `get_contextual_guidance` but the ruled
destination is `action:greeting`; the router independently declined, so deleting a
deterministically-wrong fallback cannot regress the row.

**A prior same-day attempt at this deletion STOPPED, and this lane resolves why it's now safe.**
Earlier on 2026-10-02 (`dev/2026/10/02/2026-10-02-1030-prog-code-log-1595-phase3-deletion-
guidance.md`) a Coding Agent tried a FULL tombstone of `GUIDANCE_PATTERNS` (all 21 literals, matching
the then-fully-GO gate verdict) and found 4 of its claimed phrases reabsorbed by `STATUS_PATTERNS`'
then-live `\bmy projects\b`/`\bmy portfolio\b` literals (checked AFTER GUIDANCE in the if-chain) into
a **disagreeing** deterministic wrong answer (`get_project_status` instead of
`get_contextual_guidance`) — a genuine regression, correctly caught and STOPPED per the dispatch's
"a reabsorption DISAGREES" condition. Two things changed since: (1) `STATUS_PATTERNS`' own seventh
deletion (same day, earlier) removed both `\bmy projects\b` and `\bmy portfolio\b` from
`STATUS_PATTERNS` entirely; (2) this lane's PARTIAL verdict (not a full tombstone) keeps GUIDANCE's
own `\bsetup.*projects?\b`/`\bset up.*projects?\b`/`\bset up.*portfolio\b` literals alive regardless
of STATUS_PATTERNS' state — so the collision cannot recur for 3 of the 4 originally-reabsorbed
phrases even if STATUS_PATTERNS' literals ever returned. The 4th phrase, "how do I configure my
projects" (literal `\bconfigure.*projects?\b`), **is** one of the 18 deleted here — confirmed
post-deletion via `claim_for_phrase`: **UNCLAIMED** (`pattern_list=None`). `STATUS_PATTERNS`'
`\bmy projects\b` is gone since the seventh deletion, so nothing reabsorbs it; it now falls through
to the LLM classifier, which the frozen probe shows lands it in GUIDANCE 10/10 anyway.

**"Set up / configure / connect integrations" phrasings**: 6 of the 18 deleted literals
(`\bhelp.*setup\b`, `\bhelp.*configure\b`, `\bhelp.*set up\b`, `\bhow do i.*setup\b`,
`\bhow do i.*configure\b`, `\bhow do i.*set up\b`) claimed CONNECTOR-flavored rows ("help me
setup/configure the integration/connector", "how do I setup/configure/set up the connector").
Post-deletion these are surface-2-verified into GUIDANCE by category (10/10 probe samples each).
`INTEGRATION_CONNECT_PATTERNS` (#1417: connect/link/hook-up/integrate/add/enable ×
github/slack/notion/calendar) is a narrower, noun-gated pattern and does not claim any of these
"help"/"how do I" phrasings (confirmed: none of the 6 phrases match its regex) — so nothing besides
surface 2 was reabsorbing them before this deletion either; no reassignment needed.

**AFTER**: for each of the 18 deleted-literal rows, `claim_for_phrase` (both entry surfaces) was
re-run against the live, post-deletion `PreClassifier` — **ZERO reabsorptions**. All 3 survivor rows
remain claimed by `GUIDANCE_PATTERNS` itself. `gate --all`: `GUIDANCE_PATTERNS 3 3 NO-GO` (3
literals, 3 rows, all `[FAIL]` — expected for a partial list's remainder). Corpus denominator
unchanged at 385 (59 claimed + 326 unclaimed, down from 77 claimed before this deletion —
77 − 59 = 18, the full deleted-row count, no partial reabsorption to net out).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 277 → 259
(277 − 18 = 259; `pattern_literal_counts.total_literal_count()` confirms 259 post-deletion). The
ledger-count pin (`test_real_ledger_has_the_first_eight_deletions`, renamed to "...nine...") gains
`GUIDANCE_PATTERNS` as the 9th entry, with new assertions on `entry["partial"]` (`True`) and
`entry["surviving_literals"]` (the 3-literal set). The "a list claims N rows post-partial-deletion"
pin family gained `test_guidance_patterns_now_claims_three_rows` (mirrors
`test_status_patterns_now_claims_four_rows`): asserts exactly 3 rows (the 3 survivor phrases), all
`[FAIL]`, `lv.deletable is False`.

**Broken pins converted, never deleted**:

- `tests/unit/services/intent_service/test_setup_routing_814.py` —
  `test_help_me_get_started_matches_guidance_patterns` asserted `"help me get started"` (matching the
  now-deleted `\bget started\b`) still matches `GUIDANCE_PATTERNS`. Renamed to
  `test_help_me_set_up_my_portfolio_matches_guidance_patterns`, fixture swapped to "help me set up my
  portfolio" (matches the surviving `\bset up.*portfolio\b` literal, confirmed this session) — the
  test's actual job (GUIDANCE_PATTERNS still fires on an onboarding-setup phrasing) is unchanged.
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` —
  `("GUIDANCE", "get_contextual_guidance")`'s probe message "any guidance?" (matched the deleted
  `\bguidance\b`) could not simply be swapped: ALL 3 surviving literals require a setup verb +
  project/portfolio noun, which is EXACTLY the shape `CanonicalHandlers._detect_setup_request`'s
  "projects" topic checks for — so every message step 1 can still pose for this pair now
  STRUCTURALLY routes to the non-spending onboarding branch (`_handle_project_setup_request`),
  never the generic/spending guidance branch the pair was measured against. Confirmed empirically:
  driving "help me set up my projects" through this test's real step 2 crossed the spend chokepoint
  0x (was >0 for "any guidance?"). Removed the pair from `PAIR_MESSAGES` with a NOTE block (same
  idiom as the TEMPORAL_PATTERNS/PRIORITY_PATTERNS removals above) flagging this as discovered work
  for Lead/Arch/CXO: the generic/spending guidance branch is NOT categorically gone (it still spends
  for messages reaching it via the LLM classifier without a setup phrase), only unreachable via this
  harness's step-1 pre_classify drive — a message-shape-keyed SPEND_FREE carve-out is a design
  question, not resolved by this deletion unit.
- `services/intent_service/chat_pointers.py` — checked, NOT touched: all of its GUIDANCE-category
  `CHAT_POINTERS` entries use "connect my X" phrasings, which resolve via
  `INTEGRATION_CONNECT_PATTERNS` (confirmed: `pre_classify_with_pattern_list("connect my github")` →
  `(GUIDANCE, get_contextual_guidance, 'INTEGRATION_CONNECT_PATTERNS')`), never `GUIDANCE_PATTERNS`
  directly — none of this deletion's 18 literals back any pointer's verified utterance.

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/unit/test_inversion_phase1_shadow_score_1595.py` +
`tests/test_architecture_enforcement.py` + the #1897 spend-free shape pin — **5175 passed, 1
xfailed, 0 failed** (full run, not a subset; ceiling exact at 259; re-run twice — once before and
once after `ruff format`/`ruff check --fix`, identical both times). `scripts/run-sweep.sh ratchets`
— 1 PRE-EXISTING unrelated failure (`test_todo_marker_ratchet`, count 36 vs frozen ceiling 35), same
as the fifth/sixth/seventh deletions found and left — confirmed unrelated again (no file this unit
touched is in its scan scope). `ruff format`/`ruff check --fix` run on `.py` files only (never the
ledger JSON — confirmed via `git status --porcelain` before invoking ruff); clean on every touched
file. No LLM calls anywhere in this unit — every surface-2 probe consulted is a frozen,
already-scored report file read as data.

### `read_floor` — FLOOR ops reachable by the rail (2026-10-02, Arch's ruling; NOT flipped)

The four small lists deposited and probed on 2026-10-02 (DISCOVERY 20, TRUST 16, MEMORY 15, ANALYSIS
16) came out almost entirely **load-bearing** under condition (d): the LLM classifier never emits
DISCOVERY, TRUST or MEMORY (0 of 620 samples on both provider legs — "what are your capabilities?" →
IDENTITY 10/10, "do you trust me…" → CONVERSATION 10/10), so those regexes were the only path into
their floor categories, while the Inversion router names the right FLOOR op (DISCOVERY 18/19 on
Haiku). Arch's ruling: the router is the better owner — **build rail ENTRIES, not a consult branch**.

- `workflow_entries.py`: `_READ_FLOOR_MEMBERS` (explicit: `get_capabilities`, `explain_trust`,
  `get_memory`, `pull_insights`, `analyze_blockers` — never "every FLOOR op") →
  `_make_read_floor_entry_point(op, category)` → a READ `WorkflowEntry` with
  `flip_group="read_floor"` whose entry point re-keys the rail's Intent to the op's own registry
  category and calls the EXISTING `IntentService._handle_floor_with_context`, resolving the user's
  formality baseline and trust stage through the two helpers factored out of
  `_process_intent_internal` for exactly this. ACTION_REGISTRY disposition stays FLOOR (a routing
  adapter, the `get_current_time` note); `_read_floor_entries()` cross-checks every member against
  the registry at registration and raises on a non-floor member. `MAX_DISPATCH_SITES` unchanged.
- `workflow_dispatcher.py`: `FLIP_GROUPS` gains `read_floor` (closed-set pin grown to 6).
- Scorer: the lenient FLOOR rule (NONE/CLARIFY = MATCH) now applies only to a floor op WITHOUT a
  rail entry — once an op can be reached by name, a router decline hands the turn to the classifier
  (a different floor framing) and is no longer "the same destination".
- The drift test (`test_action_registry.py`) traces a `read_floor` adapter to FLOOR (its terminal
  path), not WORKFLOW.
- **The router reads a rail entry's description in preference to `ACTION_DESCRIPTIONS` once an
  op has an entry** (`derive_routing_grammar`). Found the hard way the same evening: the first
  adapters carried a "via the read_floor rail adapter" label, which the noise stripper reduced to
  the bare op name, and the served router declined every TRUST row (0/10) — the sharpened registry
  text never reached it. The adapters now carry the registry's own description (pinned:
  `test_entries_carry_the_registry_description_for_the_router`). **Rule for any future adapter
  around a registry op: the entry's description IS the router's description — copy the registry
  text, never a label.** With that, and four sharpened descriptions (explain_trust names the
  relationship / limits / accountability questions and explicitly cedes a prior suggestion's
  hedging to `explain_suggestion` and what-have-you-learned to `pull_insights`; get_memory names
  history / recall phrasings; analyze_blockers names risks and threats; get_capabilities names
  'help' / features / menu), the served router's own coverage went TRUST 0 → 15/15, DISCOVERY
  16 → 22/24, ANALYSIS 7 → 10/14, MEMORY 5 → 9/15 on the full Phase-2 gate
  (`inversion-phase2-gate-2026-10-02-read-floor-haiku{,-02}.md`), no category regressing.
- **Not flipped.** Arch's condition 3: the Phase-2 per-category gate runs on `read_floor` like any
  wave, with TRUST's remaining misses read row by row (PPM's rule), before the token goes in the
  flag (PM's hand). Only after it is live and clean do the four lists go, on condition (a) evidence.
  PPM's 7 concurrences (10-02) already moved the rows the router had right: the three "what are your
  limits" rows → `get_capabilities`, etc.

### Ninth deletion (2026-10-03): `DISCOVERY_PATTERNS` (partial — 19 of 20)

The third **PARTIAL** deletion in this epic. BEFORE gate
(`--list DISCOVERY_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
read_referent,read_status,read_strategic,read_synthesis,read_temporal`): **GO (partial) — 1
load-bearing literal SURVIVES, deleting the other 19: ceiling 259 → 240**. 20 literals, 20 corpus
rows claimed (19 `[OK]`, 1 `[FAIL]`). The 1 `[FAIL]` row is the survivor: a MISMATCH where the router
declines with `CLARIFY@0.6` and a frozen N=10 surface-2 probe shows the LLM classifier landing
`get_capabilities` 0/10 samples:

| survives | corpus row | router | surface-2 (10 samples) |
|---|---|---|---|
| `\bneed\s*help\b` | "I need help understanding something" | `CLARIFY@0.6` (MISMATCH) | 0/10 `get_capabilities` |

`DISCOVERY_PATTERNS` is NOT emptied to `[]`: it becomes exactly the 1 survivor literal, with a
one-line comment naming the corpus row it carries and the probe that proves it the only live path.
The claim branch (`pre_classify`'s DISCOVERY_PATTERNS if-block, ~line 1210, checked before IDENTITY)
stays LIVE — same partial-list idiom as STATUS_PATTERNS' seventh and GUIDANCE_PATTERNS' eighth
deletions.

**Unexercised-literal audit — the clean case**: all 20 literals (19 deleted + the 1 survivor) were
exercised 1:1 by exactly one claimed corpus row each (confirmed via the gate's own
`unexercised_literals("DISCOVERY_PATTERNS", lv.rows)`, which returned zero). `claim_for_phrase`'s
real if-chain attributed all 20 claimed rows to `DISCOVERY_PATTERNS` itself — no cross-list
shadowing, no `shadowed_literals` entries, no corpus deposit needed. Unlike STATUS/GUIDANCE, this
list had no unexercised or cross-list-shadowed literals to resolve.

**Why no `surface2_verified_at_deletion` or `misserved_at_deletion` entries this time**: all 19
`[OK]` deleted-literal rows pass via a plain live MATCH/REVIEW-agrees (18 MATCH + 1 REVIEW-agrees:
"what can you do?" is a pre-existing REVIEW row from the 09-25 full report, the other 18 are
2026-10-02 DISCOVERY-deposit MATCH rows) — `get_capabilities` is itself a LIVE op
(`_READ_FLOOR_MEMBERS` gives it a `read_floor` rail entry, per the section above) and the router
actually serves it live with high confidence (0.95–1.0) on every one of these rows. None of them
needed a surface-2 floor probe or a mis-serve licence — the consult already owns the phrase before
deletion, so surface 1 was never load-bearing for any of the 19.

**AFTER**: for each of the 19 deleted-literal rows, `claim_for_phrase` (both entry surfaces) was
re-run against the live, post-deletion `PreClassifier` — **ZERO reabsorptions**. The survivor row
remains claimed by `DISCOVERY_PATTERNS` itself. `gate --all`: `DISCOVERY_PATTERNS 1 1 NO-GO` (1
literal, 1 row, `[FAIL]` — expected for a partial list's remainder). Corpus denominator: 447 = 102
claimed + 345 unclaimed (down from 121 claimed before this deletion — 121 − 102 = 19, the full
deleted-row count, no partial reabsorption to net out).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 259 → 240
(259 − 19 = 240; `pattern_literal_counts.total_literal_count()` confirms 240 post-deletion). The
ledger-count pin (`test_real_ledger_has_the_first_nine_deletions`, renamed to "...ten...") gains
`DISCOVERY_PATTERNS` as the 10th entry, with new assertions on `entry["partial"]` (`True`) and
`entry["surviving_literals"]` (the 1-literal set). The "a list claims N rows post-partial-deletion"
pin family gained `test_discovery_patterns_now_claims_one_row` (mirrors
`test_guidance_patterns_now_claims_three_rows`): asserts exactly 1 row (the survivor phrase),
`[FAIL]`, `lv.deletable is False`.

**Broken pins converted, never deleted**:

- `tests/unit/services/intent_service/test_discovery_intent.py` — `test_discovery_patterns_match`
  parametrized 16 phrasings that all matched now-deleted literals; renamed to
  `test_discovery_patterns_now_unclaimed_by_surface_1` and flipped to assert `PreClassifier.
  pre_classify(message) is None` (unclaimed, not misrouted — surface 1 no longer serves these; a
  live-LLM claim about surface 2 is out of scope for this suite). Added
  `test_discovery_survivor_literal_still_matches` to keep the "DISCOVERY still claims
  get_capabilities" coverage this file's job requires. `test_discovery_before_identity_precedence`'s
  fixture ("what can you do for me", matched the same deleted literal) swapped to the survivor
  phrase — still proves DISCOVERY is checked before IDENTITY.
- `tests/unit/services/intent_service/test_setup_routing_814.py` —
  `test_what_can_you_do_still_routes_to_discovery` asserted `"what can you do"` (matching the deleted
  `\bwhat can you do\b`) still matches `DISCOVERY_PATTERNS`. Fixture swapped to "I need help
  understanding something" (matches the surviving `\bneed\s*help\b` literal, confirmed this
  session) — the test's actual job (DISCOVERY_PATTERNS still fires on a capability/help phrasing) is
  unchanged.
- `tests/unit/services/intent_service/test_preclaim_shadow.py` — the file's canonical
  DISCOVERY-claimed fixture, "what can you do?" (12 occurrences across all 5 pins), matched the
  deleted `\bwhat can you do\b` literal; every occurrence swapped to "I need help understanding
  something" (matches the survivor, confirmed mapping to the same `DISCOVERY_PATTERNS`/
  `get_capabilities` claim this session) — every pin's actual point (explosive-router default-off,
  sampled-on single-consult, fail-open, pattern-list identity threading) is unchanged; only the
  literal exercised moved to the one that survived.
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` —
  `("DISCOVERY", "get_capabilities")`'s probe message "what can you do?" (matched the deleted
  literal) swapped to "I need help understanding something" (matches the survivor). Unlike the
  GUIDANCE eighth deletion's pair, this swap needed no removal: the handler flow for
  `get_capabilities` does not depend on which literal matched it, so the pair still crosses the
  spend chokepoint exactly as before (confirmed empirically: `crossings > 0`, same as the original
  fixture) — `DISCOVERY`/`get_capabilities` stays in `SPENDS`, unaffected.
- `services/intent_service/chat_pointers.py` — checked, NOT touched: no `CHAT_POINTERS` entry
  resolves through `DISCOVERY_PATTERNS` (grepped for `get_capabilities`/`DISCOVERY`; none found).

Full suite: `tests/unit/services/intent_service/` + `tests/test_architecture_enforcement.py` —
**5072 passed, 1 xfailed, 0 failed** (full run). Plus
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/unit/test_inversion_phase1_shadow_score_1595.py` — **77 passed** (the #1897
spend-free shape pin is covered inside the `tests/unit/services/intent_service/` run above, not run
separately — `test_1897_two_part_turn_live.py` under `tests/e2e/` is `pytest.mark.llm`-gated and
genuinely spends; out of scope for a no-LLM-calls unit). `ruff format`/`ruff check` run on every
touched `.py` file only (never the ledger JSON — confirmed via `git status --short` before invoking
ruff); clean on every file (one file needed `ruff format`, re-verified clean after). No LLM calls
anywhere in this unit — every surface-2 probe consulted is a frozen, already-scored report file read
as data; the `--live` gate runs and `claim_for_phrase`/`pre_classify` checks are deterministic.

### Tenth deletion (2026-10-03): `TRUST_PATTERNS` (partial — 15 of 16)

The fourth **PARTIAL** deletion in this epic. BEFORE gate
(`--list TRUST_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
read_referent,read_status,read_strategic,read_synthesis,read_temporal`): **GO (partial) — 1
load-bearing literal SURVIVES, deleting the other 15: ceiling 240 → 225**. 16 literals, 16 corpus
rows claimed (15 `[OK]`, 1 `[FAIL]`). The 1 `[FAIL]` row is the survivor: a REVIEW-disagrees row
where the router names `get_capabilities@0.9` (a live op) but the expected destination is
REVIEW/not-action-shaped, so the pattern is the only live path for this phrase:

| survives | corpus row | router | expected |
|---|---|---|---|
| `\bwhy can'?t you\b` | "why can't you create issues?" | `get_capabilities@0.9` (REVIEW-disagrees) | REVIEW / not-action-shaped |

`TRUST_PATTERNS` is NOT emptied to `[]`: it becomes exactly the 1 survivor literal, with a
one-line comment naming the corpus row it carries. The claim branch (`pre_classify`'s
TRUST_PATTERNS if-block, checked before INSIGHT_PULL_PATTERNS/MEMORY_PATTERNS and after
PROVENANCE_PATTERNS) stays LIVE — same partial-list idiom as STATUS_PATTERNS' seventh,
GUIDANCE_PATTERNS' eighth, and DISCOVERY_PATTERNS' ninth deletions.

**Unexercised-literal audit — the clean case**: all 16 literals (15 deleted + the 1 survivor) were
exercised 1:1 by exactly one claimed corpus row each (confirmed via the gate's own
`unexercised_literals("TRUST_PATTERNS", lv.rows)`, which returned zero). `claim_for_phrase`'s real
if-chain attributed all 16 claimed rows to `TRUST_PATTERNS` itself — no cross-list shadowing, no
`shadowed_literals` entries, no corpus deposit needed.

**The one `misserved_at_deletion` row**: "why are you always cautious about this suggestion"
matched the now-deleted `\bwhy (are|do) you (so|being so|always) (cautious|careful|conservative)\b`
literal, which claimed `explain_trust` — disagreeing with the ruled destination
(`action:explain_suggestion`). The router independently reaches `explain_suggestion@0.95` live (a
MATCH on a non-live op under TRUST_PATTERNS' own claim), and a frozen N=10 surface-2 probe does
**not** show the LLM classifier landing in PROVENANCE on every sample (0/10 — the
surface2-reaches-floor escape does not apply here). But the pattern's claim is deterministically
WRONG regardless of the probe result (`claim=explain_trust != ruled action:explain_suggestion`), so
deleting it cannot make the surviving fallback worse than a deterministic wrong answer —
`row_disposition`'s "mis-serves this row" branch. `surface2_verified_at_deletion` is empty for this
entry: the one row that attempted that escape failed its probe and passed via the mis-serve rule
instead. The other 14 deleted rows pass via a plain live MATCH ("expected action live via group" —
`explain_trust`/`get_capabilities`/`pull_insights` are all live under this flag).

**AFTER**: for each of the 15 deleted-literal rows, `claim_for_phrase` (both entry surfaces) was
re-run against the live, post-deletion `PreClassifier` — **ZERO reabsorptions**. The survivor row
remains claimed by `TRUST_PATTERNS` itself. `gate --all`: `TRUST_PATTERNS 1 1 NO-GO` (1 literal, 1
row, `[FAIL]` — expected for a partial list's remainder). Corpus denominator: 447 = 87 claimed + 360
unclaimed (down from 102 claimed before this deletion — 102 − 87 = 15, the full deleted-row count,
no partial reabsorption to net out).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 240 → 225
(240 − 15 = 225; `pattern_literal_counts.total_literal_count()` confirms 225 post-deletion). The
ledger-count pin (`test_real_ledger_has_the_first_ten_deletions`, renamed to "...eleven...") gains
`TRUST_PATTERNS` as the 11th entry, with new assertions on `entry["partial"]` (`True`) and
`entry["surviving_literals"]` (the 1-literal set). The "a list claims N rows post-partial-deletion"
pin family gained `test_trust_patterns_now_claims_one_row` (mirrors
`test_discovery_patterns_now_claims_one_row`): asserts exactly 1 row (the survivor phrase),
`[FAIL]`, `lv.deletable is False`.

**Broken pins converted, never deleted**:

- `tests/unit/services/test_pre_classifier.py::test_trust_patterns` — asserted 14 phrasings all
  matched a `TRUST_PATTERNS` literal and routed to TRUST/`explain_trust`; 13 of the 14 matched
  now-deleted literals (the 14th, "why can't you do that", matches the survivor). Renamed to
  `test_trust_patterns_now_unclaimed_by_surface_1` and flipped to assert
  `PreClassifier.pre_classify(message) is None` for the 13 now-unclaimed phrasings. Added
  `test_trust_survivor_literal_still_matches` to keep the "TRUST still claims explain_trust"
  coverage this file's job requires. `test_memory_not_trust`'s second fixture ("how well do you
  know me", matched a deleted literal) swapped to the survivor phrase — still proves a
  TRUST-claimed phrase doesn't collide with MEMORY_PATTERNS.
  `test_trust_still_routes_after_provenance` asserted 7 phrasings all routed to TRUST as a
  PROVENANCE-collision regression guard; 6 of the 7 matched now-deleted literals. Split into a
  `now_unclaimed` list (asserting `None`, confirming PROVENANCE's own verb list — mention/bring
  up/suggest/recommend/surface/raise/flag — does not steal these "do"/"just"/"go ahead"/"how
  well"/"what are your limits"/"always ask" phrasings) plus the 1 survivor query ("Why can't you
  help me?"), still asserted TRUST/`explain_trust`. `test_trust_not_identity` was unaffected (its
  fixture, "why can't you delete my project", matches the survivor).
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` — unaffected:
  `("TRUST", "explain_trust")`'s probe message "why can't you do that?" matches the surviving
  `\bwhy can'?t you\b` literal, confirmed unchanged by a direct run.
- `tests/e2e/test_read_floor_live.py` — checked, NOT touched: `pytest.mark.llm`-gated (skipped
  without a live header key), tests end-to-end dispatch (router/floor), not which literal matched —
  out of scope for a no-LLM-calls unit regardless.
- `services/intent_service/chat_pointers.py` — checked, NOT touched: no `CHAT_POINTERS` entry
  resolves through `TRUST_PATTERNS` (grepped for `explain_trust`/`TRUST`; none found).

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
`tests/unit/test_inversion_phase1_shadow_score_1595.py` (one combined invocation, run in background
due to runtime) — **5184 passed, 1 xfailed, 0 failed**. `tests/unit/services/test_multi_intent.py`
(pre-existing, out of scope, run separately with `-o addopts="--import-mode=importlib --tb=line"`):
**16 failed, 11 passed** — same count as the baseline this lane was told to expect, confirming no
new failures. `ruff format`/`ruff check` run on every touched `.py` file only (never the ledger
JSON — confirmed via `git status --short` before invoking ruff); clean on every file (no formatting
needed this time). No LLM calls anywhere in this unit — every surface-2 probe consulted is a
frozen, already-scored report file read as data; the `--live` gate runs and
`claim_for_phrase`/`pre_classify` checks are deterministic.

### Eleventh deletion (2026-10-03): `MEMORY_PATTERNS` (partial — 12 of 15)

The fifth **PARTIAL** deletion in this epic. BEFORE gate
(`--list MEMORY_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
read_referent,read_status,read_strategic,read_synthesis,read_temporal`): **GO (partial) — 3
load-bearing literals SURVIVE, deleting the other 12: ceiling 225 → 213**. 15 literals, 14 corpus
rows claimed (11 `[OK]`, 3 `[FAIL]`). The 3 `[FAIL]` rows are the survivors — each has no live
fallback naming the same op, so the pattern is the only live path for its phrase:

| survives | corpus row | router | expected |
|---|---|---|---|
| `\b(my|our) (conversation )?history\b` | "our history together has been good" | `NONE@0.95` | `action:get_memory` |
| `\bsearch (my |our )?(conversation )?history\b` | "search history for that conversation topic" | `CLARIFY@0.4` | `action:get_memory` |
| `\bwhat (i|we) (said|talked|discussed)\b` | "what we discussed yesterday was helpful" | `NONE@0.95` | `action:get_memory` |

`MEMORY_PATTERNS` is NOT emptied to `[]`: it becomes exactly the 3 survivor literals, each with a
one-line comment naming the corpus row it carries, in their original relative order. The claim
branch (`pre_classify`'s MEMORY_PATTERNS if-block, checked after INSIGHT_PULL_PATTERNS and guarded
by `_is_destructive_ask`) stays LIVE — same partial-list idiom as STATUS_PATTERNS' seventh,
GUIDANCE_PATTERNS' eighth, DISCOVERY_PATTERNS' ninth, and TRUST_PATTERNS' tenth deletions.

**Unexercised-literal audit — NOT the clean case this time**: 14 of the 15 literals were exercised
1:1 by a claimed corpus row, but 1 (`\bhow (much|far back) do you remember\b`) was NOT — confirmed
via the gate's own `unexercised_literals("MEMORY_PATTERNS", lv.rows)`, which returned exactly this
one literal (MEMORY claims 14 rows for 15 literals, the discrepancy the dispatch prompt flagged in
advance). The audit this procedure exists for: constructing the most natural phrasings that would
hit it ("how much do you remember", "how much do you remember about me", "how far back do you
remember", "how far back do you remember our conversations") and running them through the REAL
if-chain, `PreClassifier.pre_classify_with_pattern_list` — never `_first_pattern_match` alone. Every
one of those phrasings is claimed by `\bdo you remember\b` (list index 2, checked BEFORE this
literal's former index 13) — "do you remember" is a guaranteed substring of every phrase the
unexercised literal would ever match, preceded by a word boundary, so the earlier sibling provably
claims first regardless of corpus coverage. **PROVABLY SHADOWED within the same list**, not
cross-list — `\bdo you remember\b` is itself one of the 12 literals this same commit deletes (not a
survivor), so the shadowing changes nothing about the deletion's safety: neither literal ever
independently determined a row's claim once the other fires first. No corpus deposit was needed; no
STOP.

**The one `misserved_at_deletion` row**: "remember when we shipped the last release?" matched the
now-deleted `\bremember (when|that|our|my)\b` literal, which claimed `get_memory` — disagreeing with
the ruled destination (`action:check_completion_status`). The router independently MATCHes
`check_completion_status@0.85` on a non-live op (the live consult stands down), and a frozen N=10
surface-2 probe does **not** show the LLM classifier landing in STATUS on every sample (0/10 — the
surface2-reaches-floor escape does not apply here). But the pattern's claim is deterministically
WRONG regardless of the probe result (`claim=get_memory != ruled action:check_completion_status`),
so deleting it cannot make the surviving fallback worse than a deterministic wrong answer —
`row_disposition`'s "mis-serves this row" branch. `surface2_verified_at_deletion` is empty for this
entry. The other 10 deleted rows pass via a plain live MATCH ("expected action live via group" —
`get_memory` is live under this flag).

**AFTER**: for each of the 11 deleted-literal rows plus the shadowed literal's 2 candidate
phrasings, `claim_for_phrase` (both entry surfaces) was re-run against the live, post-deletion
`PreClassifier`. **1 AGREEING reabsorption**: "can you show my conversation history" (formerly
claimed by the deleted `\b(show|view|see) (my |our )?(conversation )?history\b` literal) is now
reclaimed by the surviving `\b(my|our) (conversation )?history\b` literal — "my conversation
history" is a substring of the phrase, same action (`get_memory`), same list, same category. The
other 10 deleted-row phrases plus both unexercised-literal candidates are genuinely UNCLAIMED.
`gate --all`: `MEMORY_PATTERNS 3 4 NO-GO` (3 literals, 4 rows — the 3 survivors plus the 1
reabsorbed row — `[FAIL]` on the 3 survivors, `[OK]` on the reabsorbed one, expected for a partial
list's remainder). Corpus denominator: 447 = 77 claimed + 370 unclaimed (down from 87 claimed before
this deletion — 87 − 77 = 10, net of the 11 deleted-row claims losing the 1 reabsorbed row).

**Ceiling arithmetic**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 225 → 213
(225 − 12 = 213; `pattern_literal_counts.total_literal_count()` confirms 213 post-deletion). The
ledger-count pin (`test_real_ledger_has_the_first_eleven_deletions`, renamed to "...twelve...")
gains `MEMORY_PATTERNS` as the 12th entry, with new assertions on `entry["partial"]` (`True`) and
`entry["surviving_literals"]` (the 3-literal set). The "a list claims N rows post-partial-deletion"
pin family gained `test_memory_patterns_now_claims_four_rows` (mirrors
`test_trust_patterns_now_claims_one_row`, extended for the 1 reabsorbed row): asserts exactly 4
rows (the 3 survivor phrases `[FAIL]` plus the 1 reabsorbed phrase `[OK]`), `lv.deletable is False`.

**Broken pins converted, never deleted**:

- `tests/unit/services/test_pre_classifier.py::test_memory_patterns` — asserted 12 phrasings all
  matched a `MEMORY_PATTERNS` literal and routed to MEMORY/`get_memory`; 9 of the 12 matched
  now-deleted literals with no surviving literal covering them. Renamed to
  `test_memory_patterns_now_unclaimed_by_surface_1` and flipped to assert
  `PreClassifier.pre_classify(message) is None` for the 9 now-unclaimed phrasings. Added
  `test_memory_survivor_literals_still_match` for the 3 remaining ("show my history" and "view my
  conversation history" — reabsorbed by the surviving `\b(my|our) (conversation )?history\b`
  literal — plus "search my history for budget", unaffected, already claimed by the surviving
  `\bsearch (my |our )?(conversation )?history\b` literal). `test_memory_not_trust`'s first fixture
  ("what do you remember about our project", matched a deleted literal) swapped to the survivor
  phrase "our history together has been good" — still proves a MEMORY-claimed phrase doesn't
  collide with TRUST. `test_portfolio_not_memory`'s second fixture ("what do you remember about
  me", matched a deleted literal) swapped the same way — still proves MEMORY doesn't collide with
  PORTFOLIO. `test_memory_get_memory_still_works_after_pull_insights` asserted 4 phrasings all
  routed to MEMORY/`get_memory` as an INSIGHT_PULL-ordering regression guard; 3 of the 4 matched
  now-deleted literals. Split into a `now_unclaimed` list (asserting `None`) plus the 1 survivor
  query ("Show my conversation history"), still asserted MEMORY/`get_memory`.
- `tests/unit/services/intent_service/test_read_lane_destructive_greed_1756.py` —
  `MEMORY_LANE_DESTRUCTIVE` (15 phrases) unaffected: the `_is_destructive_ask` guard declines these
  before any MEMORY_PATTERNS literal is even consulted, confirmed unchanged by a direct run.
  `MEMORY_READS` (11 phrases, in `KEEP_CLAIMING`): 8 of the 11 matched now-deleted literals with no
  surviving literal covering them. Moved those 8 to a new `MEMORY_READS_NOW_UNCLAIMED` set and added
  `TestMemoryReadsNowDeclineAtSurfaceOne` (mirrors `TestTemporalReadsNowDeclineAtSurfaceOne`,
  adjusted: MEMORY_PATTERNS is partial, not tombstoned, but none of these 8 phrases is covered by a
  surviving literal); `MEMORY_READS` keeps the 3 still-claimed phrases ("show my history", "my
  conversation history", "search my history"). `READS_MENTIONING_DESTRUCTIVE_VERBS`: 2 of its 5
  phrases ("do you remember what i deleted", "what did we discuss about deleting projects") matched
  now-deleted literals; swapped for 2 phrases confirmed claiming at confidence 1.0 AND confirmed NOT
  an ask position, via MEMORY_PATTERNS' surviving history literals ("can you show my history before
  i delete these old notes", "search my history before i cancel this project").
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` —
  `("MEMORY", "get_memory")`'s probe message "what do you remember?" matched the now-deleted
  `\bwhat do you remember\b` literal. Swapped to "our history together has been good" (matches the
  surviving `\b(my|our) (conversation )?history\b` literal, confirmed mapping to the same pair this
  session) — the pair itself is unaffected.
- `tests/e2e/test_read_floor_live.py` — checked, NOT touched: `pytest.mark.llm`-gated (skipped
  without a live header key), tests end-to-end dispatch (router/floor) when `read_floor` is live,
  not which literal matched — out of scope for a no-LLM-calls unit regardless.
- `services/intent_service/chat_pointers.py` — checked, NOT touched: no `CHAT_POINTERS` entry
  resolves through `MEMORY_PATTERNS` (grepped for `get_memory`/`MEMORY`; none found).

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
`tests/unit/test_inversion_phase1_shadow_score_1595.py` (one combined invocation, run in background
due to runtime) — **5186 passed, 1 xfailed, 0 failed**. `tests/unit/services/test_multi_intent.py`
(pre-existing, out of scope, run separately with `-o addopts="--import-mode=importlib --tb=line"`):
**16 failed, 11 passed** — same count as the baseline this lane was told to expect, confirming no
new failures. `ruff format`/`ruff check` run on every touched `.py` file only (never the ledger
JSON — confirmed via `git status --short` before invoking ruff); clean on every file (no formatting
needed this time). No LLM calls anywhere in this unit — every surface-2 probe consulted is a
frozen, already-scored report file read as data; the `--live` gate runs and
`claim_for_phrase`/`pre_classify` checks are deterministic.

## Pointers

- Probe report + recalibration trace: `dev/2026/07/08/routing-probe-1283-run1.md`
- Dispatch-site ratchet (the no-new-elif rule): `tests/test_architecture_enforcement.py::TestPreFloorDispatchSiteRatchet` + CLAUDE.md §"Intent dispatch"
- Migration roadmap off the legacy chains: `docs/internal/architecture/current/pre-floor-handler-migration-roadmap-1124.md`
