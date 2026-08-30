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
| 1 | **Pre-classifier** | `services/intent_service/pre_classifier.py` | Deterministic (regex/pattern) | Intercepts known shapes BEFORE any LLM call — identity ("who am I?" → `get_identity`), insights (`pull_insights`), stakeholder updates (`write_stakeholder_update`), portfolio (`manage_portfolio`), status (`get_project_status`), standup, etc. Cheap, deterministic, and the reason "the LLM classified X wrong" is often unobservable in production: the LLM never saw the phrase. **#1527 delete-claim narrowing (2026-08-29)**: the PORTFOLIO delete-family patterns (delete / remove / get rid of) DECLINE via a negative lookahead (`REMINDER_TODO_NOUN_GUARD`) when the delete-target noun phrase carries reminder/todo vocabulary (reminder(s) / todo(s) / to-do(s) / task(s)) — PM live 2026-08-29: 'delete the reminder to hydrate' and the system-taught 'delete my hydrate reminder' were claimed by the greedy `\bdelete\s+…(.+)` capture into "couldn't find a project called '…'", three misroutes in one exchange, and because this surface runs before the Inversion consult the flip never saw them. Narrowing only — a guarded miss falls through BOTH pattern entry surfaces (`pre_classify` AND `detect_multiple_intents`, which consult the same PORTFOLIO_PATTERNS) to the LLM lane, whose delete_todo emission dispatches the #1666 DESTRUCTIVE rail family; no new pre-classifier claim was added (moratorium-clean: this removes deprecated-layer claims). Companion narrowing, exposed by the fix: REMINDER_QUERY_BLOCKERS gains the phrasal destructive verb "get rid of" so the released 'get rid of my reminders' cannot be claimed by the reminder LIST lane. Legitimate project deletes ('delete the alpha project') still claim; archive/hide/restore untouched. Regression: `tests/unit/services/intent_service/test_reminder_delete_misroute_1527.py` (both surface-1 entry points + e2e that the routed destination is the todo family and the #1666 title-bound confirm still arms). **Extraction-pattern ratchet**: argument-extraction-by-regex — this surface's pattern lists AND the handler-side slot-fills (`_slotfill_issue_request`, `todo_handlers`' todo/reminder extraction, `drafted_issue`'s answer patterns) — is interpretation-layer work: gate-side, corpus-deposit by default, enforced by `TestExtractionPatternRatchet` in `tests/test_architecture_enforcement.py` (added 2026-08-29, PM-ratified after the live round). |
| 2 | **LLM classifier** | `services/intent_service/classifier.py` (`IntentClassifier.classify`) + `llm_classifier.py` | LLM | Emits an `Intent` (category + action + confidence). Its ACTION VOCABULARY is prompt-suggested, not enforced — it can and does emit paraphrase variants (probe evidence: `list_stale_prs`, `analyze_productivity`). |
| 3 | **Action rail** | `services/intent_service/workflow_entries.py` (`register_default_workflows`) → `workflow_dispatcher.get_action_workflows()`; consumed in `services/intent/intent_service.py::process_intent` | Deterministic dict lookup | If `intent.action` is a registered key (canonical or alias), dispatch pre-floor to that handler. 110 keys ≈ 32 handlers + aliases (census D count 2026-07-16; corrected 2026-08-02 by #1433 — the old "~86" sat stale for weeks, F24; +4 keys 2026-08-08, #1521 reminder-list cohort; +4 keys 2026-08-10, #1570 archived-projects list — `list_archived_projects` + 3 aliases, effect=READ, self-contained entry point; +4 keys 2026-08-16, #1624 uploaded-document summarize — `summarize_document` + 3 aliases, effect=READ, outwardness=PRIVATE: the first SYNTHESIS registry canonical, reached LLM-lane via the Phase-4 verb shim's one mapped SUMMARIZE cell (`(SUMMARIZE, "document")`) or classifier.py's bare-`summarize` normalization; the handler calls the SAME `handle_summarize_document` the REST route uses, resolves "the document" via the un-orphaned `FileResolver` (owner-scoped since #1312), answers deterministically-honestly when no upload resolves, and returns None (rail fall-through to the #1187 SYNTHESIS floor path) for issue/commit-shaped requests. Every OTHER summarize source stays floor-by-#1158; the dormant `_handle_summarize` + IntentEnricher + the never-fired summarize template rows were deleted in the same change — forensics: `docs/internal/operations/summarize-intent-forensics-2026-08-15.md`; +3 keys 2026-08-19, #1666 delete_todo family; +3 keys 2026-08-25, #1685 create_todo family — **live count re-measured 2026-08-25: 123 keys / 43 unique entries**, all `action_triggered`, so read the running "+N" notes as provenance, not as an arithmetic you should trust over `len(get_action_workflows())`). The alias lists are **mode-4 defense** against variant emissions — necessary, provably insufficient alone (4 stale-PR aliases still missed a live 5th variant). **#1190 destructive-confirmation gate (2026-08-10, PM ruling)**: inside this surface's dispatch branch, an entry whose declared effect derives `needs_confirm` (== `EffectClass.DESTRUCTIVE`; currently the close/reopen pair, 4 alias keys — the first live DESTRUCTIVE entries — plus the delete_todo family, 3 alias keys (delete_todo/remove_todo/cancel_todo), added 2026-08-19 by #1666: Arch found delete_todo rail-UNREGISTERED, so it never reached this gate and the legacy elif deleted IMMEDIATELY with no confirm; the elif is now REMOVED (rail is the single dispatch surface, `run_delete_todo_workflow` carries its body incl. the #1605 clear-family seam) and the confirm is built by the ASYNC `build_todo_delete_confirmation` — positional "todo N" target means the honest ask needs the owner-scoped list read, so the gate binds the REAL todo text into the question ('Delete todo N: "text"? (yes/no)', never number-only) AND the resolved row into the intent (`delete_todo_resolved` + the confirmed marker → the yes deletes exactly the row named in the ask, never a positional re-resolve against a shifted list); clear-family shapes pass through so reminder_clear keeps first claim; lookup failure returns an honest no-op turn, never an ungated delete. Regression: `test_delete_todo_confirm_1666.py` + `tests/integration/test_todo_delete_chat_path_1666.py`) does NOT execute on the classified turn — the gate stores the deferred action as a pending offer (the #846 session-scoped store, popped before classification, so #1529 offer-binding ordering holds) and asks one yes/no question. "yes" re-dispatches the ORIGINAL intent via the offer-acceptance seam → `run_confirm_pending_action_workflow` (registered `confirm_pending_action`, action_triggered=False — rail-unreachable); "no"/bare-exit cancels honestly; off-intent abandons (the pop already cancelled). **#1650 crisp-accept (2026-08-18)**: every offer dispatching the confirm carrier (`workflow_type == confirm_pending_action` — destructive confirms, consent checks, reminder-clear delete confirms, drafted-issue file confirms, repo-question default binds) consults the STRICT `detect_confirm_response` (soft_invocation.py) at the pop seam instead of the generic `detect_offer_response`: accept ONLY when the whole message is a crisp anchored affirmative (yes / y / yes please / do it / confirm / go ahead / short combinations). The greedy generic rows ("^please\s" etc.) had claimed PM's one-line ~95-char aside as a YES — under the #1631 prose floor, so the shape override never triggered — and fired an armed delete. Non-crisp non-decline turns fall to each kind's documented off-intent rule; declines unchanged; generic (non-confirm) offers keep #1631 behavior byte-for-byte. Kind-specific accept layers hardened the same way: drafted-issue near-accepts RE-ASK + re-arm (never file, never drop composed work), the repo-question closed-default bind requires a crisp yes, and reminder-clear's correction-window claim is anchored + non-prose (`_CORRECTION_CLAIM_RE` — an aside that merely mentions deleting no longer claims the window). Regression: `test_confirm_crisp_accept_1650.py` + pins in the 1605/1571/1567 suites. Generic deferred-action carrier documented in `services/intent_service/destructive_confirm.py`; **#1571 drafted-issue binding (2026-08-15) is now the carrier's second consumer** (`services/intent_service/drafted_issue.py`): the #1510 collaborate turn in `_handle_create_issue` ARMS a pending action (kind `drafted_issue`) binding the rendered draft, so "file it (as is)" — including the original incident phrase "file it in owner/repo", repo override honored — IS the confirmation: handled kind-specifically at the pop seam BEFORE generic accept/decline (the #1605 precedent), acceptance delegates to `run_confirm_pending_action_workflow` (original Intent re-dispatched through the create rail; the `destructive_confirmed` marker now also tells the collaborate gate consent-was-given, so no double-ask), success copy derives from the actual tool result, and any non-created outcome RE-ARMS the draft (retry never loses it). Off-intent abandons per the carrier's rules. **#1627 mid-compose prose hold (2026-08-15, round 2)**: while the drafted_issue offer is armed, a PROSE turn that answers the open body question ("What should the body say…?") binds to the draft at this same pop seam — appended to the draft body and `intent.context["description"]` (so it is what actually files), offer re-armed, draft echoed back — BEFORE any classification surface can see it. The live thief was surface 1's greedy #1527 portfolio pattern (`\bdelete\s+…(.+)`) claiming PM's long body answer ("I couldn't find a project called '(a destructive action)…'"); the #1623 mid-interview hold could not cover it because the draft flow is floor-composed prose, not a registered gathering process. NOT a turn lock: file/accept phrases still file, declines/bare exits still drop the draft honestly, and anchored-imperative asks (the shared collaborate-gate execute check plus a close/read/destructive verb supplement) still route normally, abandoning the draft; long or multi-line turns read as prose regardless of how they open (`is_body_prose_answer` in `drafted_issue.py` — discrimination limits stated in its docstring; regression: `tests/unit/services/intent_service/test_drafted_issue_body_steal_1627.py`). **#1630 subjectless arm (2026-08-15, round 3 — the unarmed face)**: "help me write a ticket" with NO extractable subject used to arm nothing (no subject = no draft), so the answer to "What's it about?" was a bare prose turn for the same greedy chain — the #1627 theft, one turn earlier. The collaborate turn now arms a minimal SUBJECTLESS `drafted_issue` carrier at the ask; the FIRST bound prose names the draft (`derive_subject_from_prose` → draft title, mirrored into `intent.context["title"]` so the create rail files it — the subjectless original message slot-fills nothing) and seeds the body per the same append semantics. Same discriminator, same seam, same exits; the subjectless ask copy still teaches no file phrase until the draft has content (regression: `test_drafted_issue_subjectless_1630.py`). **#1648 (2026-08-18, round 4 — the fabrication face)**: PM's "file as is thanks" missed the file-command regex (object-less "file **as is**"), read as an anchored EXECUTE imperative, fell through the seam as off-intent, and the FLOOR roleplayed the entire filing ("Filed in test-piper-morgan" — zero writes). Three-part fix: (a) `_FILE_COMMAND_RE` broadened — object optional when an "as is" tail carries the reference, trailing pleasantries/affirmative lead-ins absorbed, still anchored full-message; (b) an honest NEAR-MISS fallback at the seam — a file/submit-headed turn without its own subject that matches neither file-command, prose, accept/decline, nor exit RE-ASKS and RE-ARMS (`is_file_near_miss` + `_reask_near_miss`), never a silent mid-compose abandon into the chain; disjoint from and composed with #1650's near-accept re-ask (that branch needs a loose ACCEPT read, this one needs NO offer-response read); genuinely-new file asks ("file a bug about X") and other command families still abandon and route; (c) the floor prompt's action-claims contract (surface 4). The same silent-abandon audit found and fixed the identical gap in the #1605 clear-verb question (`reminder_clear._reask_verb_question_if_unrecognized`). **Companion carrier, same issue**: `handle_create_reminder`'s honest time-clarify ask ("When should I remind you?") used to arm NOTHING, so the answer turn ("at 3pm") orphaned into the chain and the floor roleplayed "Reminder set" (no row, no 📅). The ask now arms a `reminder_time_question` pending offer (`todo_handlers.build_reminder_time_offer`); the answer binds at the pop seam (`handle_reminder_time_turn`) and performs the REAL save with the real 📅 confirmation; unbindable/absent times re-ask + re-arm; full reminder restatements and unrelated commands abandon via the pop and route normally; `clarify_reminder_time` is the offer-only generic-accept landing (`action_triggered=False`). Regression: `test_action_fabrication_1648.py`. **#1654 (2026-08-22) — the same treatment one question earlier**: `handle_create_reminder`'s OTHER honest ask, the no-task clarify ("I didn't catch what you'd like to be reminded about" — PM hit it twice on 08-18 via the colon-form parse misses, which themselves stay #1606/corpus), also armed nothing. It now arms a `reminder_task_question` pending offer (`todo_handlers.build_reminder_task_offer`, payload carries the ORIGINAL message — strings only) and the answer binds as the TASK at the pop seam (`handle_reminder_task_turn`): the time is then either already known from the original message (rare — e.g. "set a reminder: at 3pm", re-parsed at answer time, only when an explicit `_has_time_signal` — never the parser's tomorrow-morning default, #1490) and the REAL save runs with the shared 📅 copy, or the flow CHAINS into the existing `reminder_time_question` carrier (the full two-question recovery: task answer → time ask → time answer → real save). An answer carrying its own trailing time saves in one turn (time expression shed from the saved text via the shared strip); a pure-time answer re-asks for the task. ⚠️ Off-intent discrimination deviates from the shared `is_command_shaped` DELIBERATELY: the task-answer space is arbitrary imperative phrases and the shape-read's verb heads (check/get/set/…) claim legitimate task answers ("check in with the team" is the ask's own example copy) — the discriminator is the pre-classifier's DETERMINISTIC claim instead (probed 2026-08-22: claims every product command tried, no bare task phrase); declines/bare exits drop via `decline_message`, restatements + claimed commands release-and-route, everything else binds (visible, declinable) rather than orphaning to the LLM lane. `clarify_reminder_task` is the offer-only generic-accept landing (`action_triggered=False`); `reminder_task_question_pending` joins the `_apply_soft_offer` no-clobber flags; the kind is pinned OUTSIDE the #1664 confirm set. Regression: `test_task_clarify_1654.py`. Instruction-shaped draft refinement ("make the title snappier") remains deliberately not built (an anchored-imperative refinement turn abandons the binding; carrying an evolving floor-composed draft under interpreted edits needs a durable store — Inversion Phase 2 is the durable fix). Companion renderer guard: `strip_placeholder_slots` (conversational_floor.py) makes the `#[issue number]` template-slot class structurally unrenderable (replaced with deterministic no-tool-result honesty) — the literal PM saw live exists nowhere in prompts/copy; the model improvised it, so the kill is renderer-side like `strip_scaffolding_artifacts`. Orthogonal to the #1510 collaborate-gate (execute-mode users still confirm destructive actions). +3 offer-only registry keys (`confirm_pending_action` #1190; `verify_inference` #1510 read-back acceptance; `standup_interview` #1591 invitation acceptance) → NOT in the 110 action-rail count; all `action_triggered=False`, reachable ONLY via the offer-acceptance seam. **#1591 standup preference capture (2026-08-13)** is surface-internal to the standup handler, NOT a routing change: an explicit report token (`\breport\b|\bquick\b`) mirrors the #1511 interview token inside the already-claiming handler; a stored verified `standup_mode` (the #1510 rail's store) redirects the generic ask without re-inference; the post-report invitation / low-confidence read-back binds via the same #846 pending-offer store (popped before classification, so the #1529 ordering holds). **Declaration path added later the same day (PM live PARTIAL verdict)**: a standup-token DECLARATION turn ("use the standup interview format by default from now on", `standup_preferences.detect_standup_mode_declaration` — durativity composed from `collaboration_gate.has_durative_marker` + a `back to` switch-back marker) is checked FIRST inside the handler and stores the mode directly (`source=user_declared`, confidence 1.0 — store + confirmation copy, never a read-back); the taught switch-back phrase `back to my standup report` rides the `_is_standup_query` "my standup" cue so it routes AND re-declares deterministically. ⚠️ Reachability of the bare-'standup' declaration form is still LLM-lane (no deterministic surface claims bare "standup" — #1595 corpus material), and the tokenless "use the interview from now on" is a corpus row, deliberately unclaimed. **#1651 standup offer-referent binding (2026-08-18)**: the standup's closing copy stopped offering actions it couldn't consume — PM live: the report closed with "mark that overdue todo done?", the verbatim acceptance fell to `complete_todo`'s title matching ("I couldn't find a todo matching 'overdue'"). When the user has an OVERDUE todo, the non-empty report's trailing line now offers to complete the single strongest (most overdue) one WITH the todo's id bound into the #846 carrier at offer time (`services/intent_service/standup_todo_offer.py`, kind `standup_todo_offer` — the reminder-clear/drafted-issue idiom); acceptance (crisp "yes" or the verbatim phrase) dispatches the offer-only `standup_complete_todo` entry (WRITE, `action_triggered=False` — the count of offer-only keys grows by one), which completes the BOUND id via `TodoManagementService` — never a re-parse of the user's phrasing; decline drops honestly; off-intent abandons via the pop with #1631 prose discrimination inherited at the generic seam. One-slot discipline: when the bound offer arms, the #1591 mode asks stay quiet that turn; the empty-report branch is untouched (PPM's empty rule — invitation leads, no referent offer). |
| 4 | **Category handlers + floor-internal action checks** | category routing in `intent_service.py`; `conversational_floor.py`, `context_assembler.py` | Mixed | Anything not action-railed routes by `intent.category` (TEMPORAL/STATUS/PRIORITY/IDENTITY/…). Several of these check `intent.action` BY NAME internally (e.g. `pull_insights` in `conversational_floor.py`, MEMORY handling in `context_assembler.py`) — this is the **fourth vocabulary**: real dispatch that no rail listing shows. Bottom: the unhandled-LLM floor (improvised response) — the place #1283 exists to keep phrases OUT of. **Since #1570 (2026-08-10) BOTH floor doors gather domain context**: `_handle_floor_with_context` always did; `_handle_unknown_intent` (the generic-QUERY / offer-fallback / ANALYSIS-etc fall-through door) previously floored with `domain_context=None` — a data query landing there ("what todos are pending?" as an unrailed QUERY emission) saw zero user data while the store had rows. It now runs `ContextAssembler.gather_context` (caller-curated context, e.g. #1187 summarize, is preserved and skips the gather). **#1544 (2026-08-16) closed the residual empty-case misframe on this path**: zero pending todos is now a VERIFIED-EMPTY fact, not an absence — `_compute_pending_todos` returns `{"pending_todos": [], "pending_todo_count": 0}` (never `None`) when the owner-scoped read succeeds with zero rows, and `_format_domain_context` renders a distinct `PENDING TODOS: none — checked this turn` line, so the floor can say "your todo list has no pending items" as an account-level fact. The floor prompt's never-fabricate section was the OTHER half of PM's 2026-08-09 transcript ("I don't see any todos in your list right now — nothing's showing up on my end for this conversation"): its empty-data guidance *itself* supplied both example strings ("I don't see any todos in your list right now", "… in this conversation"); the guidance is rewritten — data absence is a visibility claim about THIS TURN, never a conversation-scoped fact, and the empty-list claim is licensed only by the verified-empty context line. The todo data path is owner-scoped end-to-end (`TodoManagementService.list_todos(user_id=…)` → `get_todos_by_owner`); no conversation-scoped todo read exists anywhere — the scoping was prompt-seeded copy. Pins: `test_todo_scope_framing_1544.py` (prompt + renderer), `tests/integration/test_pending_todos_query_1544.py` (real-Postgres gather, both cases). **#1639 (2026-08-18) applied the same verified-empty treatment to the sibling gathers**: `_compute_projects` and `_compute_completed_todos` now return `{"projects": [], "project_count": 0}` / `{"completed_todos": [], "completed_todo_count": 0}` instead of `None` when the owner-scoped read succeeds with zero rows (an errored read still returns `None` — never verified-empty), and `_format_domain_context` renders distinct `PROJECTS: none — checked this turn` / `COMPLETED TODOS: none — checked this turn` lines, so per lane populated / verified-empty / never-gathered are three distinguishable states at the renderer; the never-fabricate guidance's context-line examples name all three lanes (context lines only — no example reply strings, #1544's root cause). Pins: `test_sibling_verified_empty_1639.py`. **#1648 (2026-08-18) — the floor ACTION-CLAIMS CONTRACT**: the never-fabricate guidance constrained DATA claims; nothing constrained the floor from claiming ACTIONS, and in one PM session it roleplayed a full issue-filing ("Filed in test-piper-morgan", no issue existed) and a reminder save ("Reminder set for 3pm today", no row). The #1331 section is rewritten as an explicit contract: the floor composes replies ONLY — actions run solely via dispatched rails whose handlers compose their own confirmations from tool results; no success confirmations, progress narration, action role-play, or offers to "confirm"/"go ahead" with an undispatchable action; implied-but-unperformable actions get an honest can't-do-this-turn plus a pointer at the one-line ask that routes. Per the #1544 root cause, the rewrite REMOVED the section's example reply strings (the old prompt's own "On it — creating that now…" example is the near-verbatim shape of the live "On it — setting a reminder for 3pm today" fabrication) — the guidance states rules, never sample sentences (pins: `test_floor_action_claims_1648.py`). Floor output is also scrubbed renderer-side: `strip_scaffolding_artifacts` (conversational_floor.py) makes the prompt's own bracketed scaffolding headers (`[Available context…]`, `[Context: …]`, `[Reference binding: …]`, `[Redirect context: …]`) structurally unrenderable in user copy — #1393's prompt-side prohibition alone did not hold (PM live 2026-08-10). A new scaffolding block added to the prompt builders must join `_SCAFFOLDING_BLOCK_RE` in the same commit. **#1536 FTUX-COLDSTART (2026-08-10)**: on the FIRST exchange of a conversation (no completed turn yet — per-conversation, judged from the #1122 in-flight-turn semantics) with a configured connector (#1547 `IntegrationStatusService`, binding-first), `gather_context` additionally runs the first-contact rail (`services/intent_service/first_contact.py`, rides outside the category dispatch like the #1566 reminder rail): a small recency-ranked slice of the user's real GitHub data (repo via the #1042/#1327 default-repo rail; no resolvable repo → NO demo and NO "which repo?" question) lands as `first_contact_demo` / `first_contact_source_failed`, which the floor renders as an open-with-their-data demonstration directive (entities confined to the gathered payload). The canonical CONVERSATION pure-greeting path (which never touches the assembler) appends the same payload via the DETERMINISTIC `render_first_contact_block` in `ConversationHandler._respond_to_greeting`. |

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
