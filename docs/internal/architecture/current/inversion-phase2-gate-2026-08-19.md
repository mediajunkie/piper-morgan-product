# Inversion Phase-2.1 gate — SNAPSHOT-AWARE router vs context-free, per category
Run: 2026-08-19 16:51Z · corpora: inversion_corpus_phase0.yaml (93 rows, untouched) + inversion_corpus_phase2_armed.yaml (14 rows: 7 armed + 7 control twins) · scripts/inversion_phase2_gate.py

LAYER (m-43): **router only, against corpus fixtures** — one constrained Haiku-class call per (row, condition) (115 LLM calls incl. repair retries across 114 routed (row, condition) pairs; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (63 canonical operations, 76 input-side aliases collapsed, + NONE/CLARIFY). NOT live traffic, NOT the production chain, NOT handler behavior: a MATCH here means the router would have picked the right destination, not that the destination's handler succeeds (the #1651 extraction failure lived one layer below routing). Armed-state session context is FIXTURE-built via the real `SessionSnapshot` dataclass and `serialize_for_prompt` — the exact shadow-path serialization, but the field VALUES are corpus assertions, not live store reads.

## Part 1 — phase0 corpus rerun, context-free (denominators stated — m-44)

Method identical to Phase 1b (inversion-phase1-shadow-score-2026-08-14b.md: 33/39). Baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md: 36/39).

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 30 | 12 | 11 | 12/12 | -1 | 18 | **REGRESSION** |
| EXECUTION | 15 | 6 | 5 | 5/6 | +0 | 9 | no regression |
| PORTFOLIO | 9 | 7 | 6 | 6/7 | +0 | 2 | no regression |
| TEMPORAL | 7 | 4 | 3 | 4/4 | -1 | 3 | **REGRESSION** |
| GUIDANCE | 6 | 1 | 1 | 1/1 | +0 | 5 | no regression |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| STATUS | 4 | 2 | 1 | 1/2 | +0 | 2 | no regression |
| PRIORITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| SYNTHESIS | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| MEMORY | 3 | 1 | 1 | 1/1 | +0 | 2 | no regression |
| DISCOVERY | 2 | 0 | 0 | 0/0 | — | 2 | **UNGATEABLE** (REVIEW-only denominator) |
| PROVENANCE | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| TRUST | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| ANALYSIS | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| **TOTAL** | 93 | 39 | 34 | 36/39 | -2 | 54 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate**. REVIEW-only-denominator categories remain ungateable, same as Phase 0/1 stated.

🔴 **Per-category regressions vs baseline** (recorded as data — this run does not tune-until-green): QUERY: 12→11; TEMPORAL: 4→3

## Part 2 — ARMED-STATE rows: with-snapshot vs without (the gate question)

**Armed-state delta: 1/7 with-snapshot vs 3/7 without-snapshot** (asserted armed rows; the same expectation scored under both conditions). Does context flip the loss class: **NO** — the snapshot did not improve the armed rows. This is the reported result; nothing was tuned to move it.

Each armed row: fixture → real `SessionSnapshot` → `serialize_for_prompt` → `RouterSnapshot(state_block=…)`. Control twins (same text, no fixture) run once: an empty snapshot's with/without prompts are byte-identical by construction, so a second call would measure only stochasticity.

| pair | phrase | armed expected | WITH snapshot | WITHOUT snapshot | control (stateless) |
|---|---|---|---|---|---|
| verb-question | delete | route:NONE | `delete_todo` @0.85 → MISS(delete_todo) | `CLARIFY` @0.3 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.3 → REVIEW |
| confirm-aside | please note that I'll need to figure out lat | route:NONE | `NONE` @0.95 → MATCH | `NONE` @0.95 → MATCH | route:NONE: `NONE` @0.95 → MATCH |
| draft-file-command | file as is thanks | route:NONE | `create_issue` @0.95 → MISS(create_issue) | `NONE` @0.95 → MATCH | REVIEW: `NONE` @0.95 → REVIEW |
| draft-body-prose | The problem: deleting a project (a destructi | route:NONE | `update_document` @0.95 → MISS(update_document) | `NONE` @0.95 → MATCH | REVIEW: `NONE` @0.95 → REVIEW |
| reminder-time-answer | at 3pm | route:NONE | `create_reminder` @0.95 → MISS(create_reminder) | `CLARIFY` @0.95 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.15 → REVIEW |
| standup-todo-offer | Yes mark the overdue todo done. | route:NONE | `complete_todo` @0.95 → MISS(complete_todo) | `complete_todo` @0.85 → MISS(complete_todo) | action:complete_todo: `complete_todo` @0.85 → MATCH |
| repo-question-answer | in the test-Piper-Morgan repository | route:NONE | `create_issue` @0.95 → MISS(create_issue) | `CLARIFY` @0.3 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.3 → REVIEW |

### Armed-family raw router output (verbatim rationales)

| pair | condition | route @conf | rationale | error |
|---|---|---|---|---|
| verb-question | with-snapshot | `delete_todo` @0.85 | User answers open question: 'delete' clarifies they want reminders removed, not marked done. |  |
| verb-question | without-snapshot | `CLARIFY` @0.3 | Delete what? Todo, issue, reminder, document, project, or repo? |  |
| verb-question | control | `CLARIFY` @0.3 | Delete what? Todo, issue, reminder, document, or project? |  |
| confirm-aside | with-snapshot | `NONE` @0.95 | User is expressing frustration/clarification about a prior misunderstanding, not answering the open reminder-deletion confirmation. This is conversational pushback, not a yes/no answer. |  |
| confirm-aside | without-snapshot | `NONE` @0.95 | User is expressing concern about a prior suggestion/action, requesting explanation of assistant's reasoning. |  |
| confirm-aside | control | `NONE` @0.95 | User is providing feedback/context about a prior interaction, not requesting an operation. |  |
| draft-file-command | with-snapshot | `create_issue` @0.95 | User answers open question to file drafted issue without body changes. |  |
| draft-file-command | without-snapshot | `NONE` @0.95 | Conversational acknowledgment; no operation applies. |  |
| draft-file-command | control | `NONE` @0.95 | Conversational acknowledgment; no operation applies. |  |
| draft-body-prose | with-snapshot | `update_document` @0.95 | User is answering the open DRAFTED_ISSUE question with issue body content. |  |
| draft-body-prose | without-snapshot | `NONE` @0.95 | User describes a product issue/feature request, not requesting an operation. |  |
| draft-body-prose | control | `NONE` @0.95 | User describes a product issue/feature request, not requesting an operation. |  |
| reminder-time-answer | with-snapshot | `create_reminder` @0.95 | User answers open reminder-time question with specific time. |  |
| reminder-time-answer | without-snapshot | `CLARIFY` @0.95 | Fragment lacks context—could be meeting time, reminder, or scheduling intent. |  |
| reminder-time-answer | control | `CLARIFY` @0.15 | Incomplete context: set reminder, meeting check, or calendar query? |  |
| standup-todo-offer | with-snapshot | `complete_todo` @0.95 | User explicitly confirms marking the overdue todo as done. |  |
| standup-todo-offer | without-snapshot | `complete_todo` @0.85 | User confirms marking a todo as done; likely refers to previously discussed overdue item. |  |
| standup-todo-offer | control | `complete_todo` @0.85 | User confirms marking a todo as done; likely refers to previously discussed overdue item. |  |
| repo-question-answer | with-snapshot | `create_issue` @0.95 | User answers open repo question; routes to pending create_issue flow. |  |
| repo-question-answer | without-snapshot | `CLARIFY` @0.3 | Fragment lacks verb/intent; unclear if querying repo status, listing issues, or setting default repo |  |
| repo-question-answer | control | `CLARIFY` @0.3 | Fragment lacks verb/intent. Set default repo, list issues, or query status? |  |

## Part 3 — phase0 REVIEW rows (informational, unscored)

| phrase | category | router route @conf | rationale |
|---|---|---|---|
| can you clarify what you meant? | QUERY | `NONE` @0.95 | User asks for clarification of prior context, but no prior a |
| show me my archived projects | QUERY | `list_archived_projects` @0.99 | User explicitly requests archived projects list. |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.99 | Direct what-have-you-learned question about work style patte |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.95 | User requests GitHub integration setup; contextual guidance  |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.95 | User requests Notion integration setup; contextual guidance  |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.95 | Integration setup request; contextual guidance handles conne |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.95 | User wants to link a GitHub repository to their project port |
| show me my todos | QUERY | `list_todos_query` @0.99 | Direct request to display user's todo list |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests calendar integration setup; contextual guidanc |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | User directly asks for their reminders list. |
| hello | CONVERSATION | `greeting` @0.99 | Simple greeting pleasantry. |
| goodbye | CONVERSATION | `farewell` @0.99 | User said goodbye; matches farewell pleasantry pattern |
| thank you! | CONVERSATION | `thanks` @0.99 | Simple expression of gratitude; pleasantry-only message. |
| what can you do? | DISCOVERY | `get_capabilities` @0.99 | Direct what-can-you-do question about assistant capabilities |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asking for provenance of a prior recommendation. |
| why can't you create issues? | TRUST | `NONE` @0.95 | User asking why assistant lacks capability; conversational/m |
| what do you remember about me? | MEMORY | `get_memory` @0.99 | Direct what-do-you-remember question about stored user conte |
| what's my default repo? | QUERY | `get_default_repo` @0.99 | Direct question about default repository setting |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | User explicitly requests setting default repo with owner/rep |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.95 | User requests a stakeholder update for a named audience (CEO |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User requests document update with new dates via slot-fillin |
| tell me more about the github integration | QUERY | `get_feature_info` @0.99 | User explicitly requests details about a specific Piper feat |
| who are you? | IDENTITY | `get_identity` @0.99 | Direct who-are-you question about the assistant's identity a |
| show my recurring meetings | QUERY | `recurring_meetings` @0.99 | Direct request to list recurring meetings |
| what's my week look like? | QUERY | `week_calendar` @0.95 | Direct calendar overview query for the week ahead. |
| what's the next milestone? | STATUS | `list_milestones` @0.85 | User asks for next milestone; list_milestones retrieves mile |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | Direct question about current Git branch status. |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped items this week |
| show stale prs | QUERY | `stale_prs` @0.95 | User explicitly requests stale PRs list |
| close issue #123 | EXECUTION | `close_issue` @0.95 | User explicitly requests closing issue #123. |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.95 | Clear request to reopen a specific issue by number. |
| comment on issue #123 | EXECUTION | `comment_issue` @0.95 | User requests commenting on a specific issue number. |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asking for count of open issues; list_issues handles is |
| show my prs | QUERY | `list_prs` @0.95 | User requests to see their pull requests |
| show issue #123 | QUERY | `review_issue` @0.95 | User requests to view/show a specific issue by number. |
| show milestones | QUERY | `list_milestones` @0.95 | User requests milestone list; list_milestones operation dire |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | Direct match to session-activity recall pattern |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query matching catalog operation. |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | User requests a reminder for a specific task at a future tim |
| complete todo 3 | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking todo 3 as done. |
| show all my todos | QUERY | `list_todos_query` @0.99 | Direct request to display user's todo list |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for next todo item from their list |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.95 | User asks when past work (onboarding project) was completed. |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.85 | Getting-started question; user seeks guidance on how to begi |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | Direct match to blocker-analysis operation description. |
| what are my priorities? | PRIORITY | `get_top_priority` @0.95 | User asking for prioritization guidance; top-priority query |
| Yes please | CONVERSATION | `CLARIFY` @0.1 | Affirmative response without prior context; unclear what use |
| end standup | CONVERSATION | `NONE` @0.85 | User ending standup is a session control action, not a query |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `manage_portfolio` @0.92 | User declines standup, requests project restore by name. |
| delete my reminders | TEMPORAL | `CLARIFY` @0.45 | Ambiguous: delete all reminders vs. list reminders to select |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.95 | User requests GitHub integration setup; contextual guidance  |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `CLARIFY` @0.65 | Two distinct operations requested: manage reminders (unclear |
| are you able to set my default repo for me conversation | DISCOVERY | `get_contextual_guidance` @0.85 | User asking how to set default repo; guidance on setup/confi |
| please mark 1, 2, 4, and 5 done | EXECUTION | `CLARIFY` @0.4 | Ambiguous: could mark todos 1,2,4,5 done OR issues/PRs. Need |

## Row detail — phase0 asserted rows

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `week_calendar` @0.85 | MISMATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what am I working on? | STATUS | category:STATUS | `get_top_priority` @0.85 | MISMATCH |  |
| what should I focus on today? | PRIORITY | category:PRIORITY | `get_top_priority` @0.92 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.3 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.95 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_contextual_guidance` @0.92 | MATCH |  |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.92 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `analyze_document` @0.95 | MISMATCH |  |
| summarize the document | SYNTHESIS | action:summarize_document | `summarize_document` @0.95 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @0.99 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.99 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.92 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| give me a project status report | EXECUTION | action:update_issue | `get_project_status` @0.95 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `manage_repos` @0.95 | MATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.95 | MATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.98 | MATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |

## Honest caveats — what this measures and does not (m-43 / m-44)

- **Routing layer only, corpus fixtures only.** Not live traffic, not handlers, not the floor. A route:NONE MATCH says the router declined to steal an answer-turn; whether the offer seam then consumes it (and whether the floor stays honest if it doesn't — #1648's fabrication class) are separate lanes this run cannot see.
- **Fixture `pending_offer_question` values exceed today's live assembly.** Arm sites currently store `summary`, not their rendered ask, so live snapshots carry question=None for most kinds (snapshot_assembly.py module docstring). The fixtures carry the ask copy the user actually saw (quoted from each arm site's own question-copy functions) — measuring the contract as designed for Phase 2.2 threading. A live shadow rerun BEFORE arm sites carry their asks would see weaker context than this run did.
- **route:NONE conflates two readings on one pair.** For the confirm-aside pair, NONE is correct both as 'aside, not an answer' and as 'answer belongs to the flow' — the rationale column, not the verdict, shows which reading the router took.
- **Armed expectations are Lead-contract-derived, not PM-ratified.** The route:NONE assertions follow the serialized RULE in session_snapshot.py; if Phase 2.2 decides answer-turns should emit a different sentinel, these rows re-score, not the runner.
- **Single run per condition.** No repetition; margin rows can flip run-to-run (the Phase-1b calendar-flip precedent). Deltas of ±1 on any category are within observed stochasticity.
- **is_confirm=true on the repo-question fixture is faithful to live assembly** (the repo question rides CONFIRM_PENDING_ACTION_WORKFLOW), but renders '(yes/no confirm)' on a which-repo question — a rendering wrinkle for Phase 2.2 to consider (flagged as discovered work).

Cost/duration: 115 LLM calls incl. repair retries across 114 routed (row, condition) pairs; 0 ERROR, 0 REFUSED; wall time 345s.

---

## Run provenance + analysis (hand-authored; everything above this rule is generator output)

### Model identity (m-43 — which instrument ran, and is it the live one?)

**Every scored call in this run was served by Anthropic `claude-haiku-4-5`.** The resolution
chain, quoted from code:

1. The runner calls `route()` → `LLMClient.complete(task_type="inversion_routing")` with no
   `user_id` (`scripts/inversion_phase2_gate.py`).
2. `services/llm/config.py:129` maps `inversion_routing` → `model_tier: "light"`.
3. `_complete_raw` resolved primary provider = **openai** (server selection default; the light
   tier there is `gpt-4o-mini`, config.py:28/65). **All 115 calls hit HTTP 429
   `credit_balance_exhausted`** — the run log carries exactly 115
   `llm_primary_failed provider=openai` lines against 115 LLM calls, 1:1. This is the same
   account state Phase 1b recorded and #1620 tracks.
4. The fallback order (`services/llm/clients.py:44` — Anthropic, Gemini, OpenAI) tries
   Anthropic next: `resolve_model(ANTHROPIC, "inversion_routing")` = light tier =
   **`claude-haiku-4-5`** (config.py:24/60). Gemini is unconfigured on this seat
   ("No GEMINI_API_KEY configured" at startup), so no third model is reachable. 0 ERROR
   outcomes → every decision that scored came from an Anthropic-served completion.

**Does the LIVE shadow run on the same instrument? Yes, under the current account state —
same chain, one difference stated.** `inversion_shadow._shadow_check` calls the same
`route()` with `llm_service = intent_classifier._llm` — the container's `LLMClient`
(`services/intent/intent_service.py:787`, `classifier.py:232`), or a fresh `LLMClient` when
that is None (`inversion_router.route`) — same class, same `task_type`, same tier tables.
The one difference: the live path passes `user_id`, so #1415 per-principal provider selection
and the consent-gated fallback apply. On this seat that resolves primary = openai against the
same exhausted account (recorded for the live path in Phase 1b's environment note) → the same
Anthropic Haiku fallback. A principal whose consent list excluded Anthropic would produce a
recorded ERROR, never a silently different model — for `inversion_routing`,
`claude-haiku-4-5` is the only non-openai model configured. **The gate and the live shadow
are the same instrument.** This section also discharges #1620's "record resolved
provider+model in the results doc" for this run.

### Coverage (m-44 — the denominator of the run itself)

All planned (row, condition) pairs completed; none skipped for time or latency:
93/93 phase0 context-free + 7/7 armed WITH-snapshot + 7/7 armed WITHOUT + 7/7 controls =
**114/114 routed**, 115 LLM calls (one repair retry somewhere in the batch), 0 ERROR,
0 REFUSED, 345s wall (~3.0s/call, dominated by the per-call 429-then-fallback hop).
Corpus arithmetic: 93 existing rows untouched + 14 new (7 armed + 7 control twins) = 107 rows.

### The armed-state result, decomposed (reported, not tuned)

**Scored as written, the gate question answers NO: 1/7 with-snapshot vs 3/7 without.** The
corpus asserts `route:NONE` for armed answer-turns — this run's encoding of the contract RULE
("a turn that plausibly ANSWERS the open question routes to that flow's handler, not to a
fresh operation"), on the reading that the flow's handler is the offer seam, which is not a
catalog entry, so the router should stand down with NONE.

**The router took the other reading. With the snapshot it correctly identified the
answer-binding in 6 of 7 rows — and then emitted the armed flow's own COMPLETING operation
instead of NONE.** Verbatim:

- "delete" → `delete_todo` @0.85 — *"User answers open question: 'delete' clarifies they want reminders removed, not marked done."*
- "file as is thanks" → `create_issue` @0.95 — *"User answers open question to file drafted issue without body changes."*
- "at 3pm" → `create_reminder` @0.95 — *"User answers open reminder-time question with specific time."*
- "in the test-Piper-Morgan repository" → `create_issue` @0.95 — *"User answers open repo question; routes to pending create_issue flow."*
- PM's body prose → `update_document` @0.95 — *"User is answering the open DRAFTED_ISSUE question with issue body content"* (binding read correctly; the operation choice is the one arguable pick — a drafted issue is not a document).
- "Yes mark the overdue todo done." → `complete_todo` @0.95 — the armed flow's own action, confidence up from the stateless 0.85.
- The #1650 aside → `NONE` @0.95 — *"conversational pushback, not a yes/no answer"* — exactly right, including NOT treating it as an accept while a delete confirm was armed.

Two honest readings of the same rows:

- **Strict-sentinel (the corpus as written): 1/7.** This number stands as the scored result;
  re-scoring it post-hoc would be tuning the gate to its outcome.
- **Flow-matching seam reading: 6 of the 7 selections equal the armed flow's own pending
  action** (delete_todo≈the armed delete, create_issue=the draft's filing, create_reminder=the
  time question's pending create, complete_todo=the offered completion, create_issue=the repo
  question's pending action; update_document is the one non-matching pick). If Phase 2.2's
  dispatch treated "router-selected operation == the armed flow's action" as binding to the
  flow, this run reads as 6/7-to-7/7 correct understanding-layer behavior — with args in hand.

And a caveat against this run's own metric (m-43): the WITHOUT column's three "MATCHes" are
**hollow NONEs** — stateless NONE means "no idea, falls to the floor," which in production is
precisely where #1648 fabricated. The armed-column's `create_reminder` and the bare-column's
`NONE` carry the same verdict-table polarity as MISS/MATCH while being opposite in user
consequence. The 1/7-vs-3/7 delta is therefore a statement about the emission convention at
least as much as about router competence.

**What the snapshot demonstrably did**: on all four fragment rows ("delete", "at 3pm",
"in the test-Piper-Morgan repository", and the confidence on the standup accept) the context
flipped the router from CLARIFY/low-confidence to a confident, correctly-bound resolution.
The snapshot changes routing behavior decisively and in the intended direction of
understanding; **what is unsettled is the emission convention for answer-turns** — RULE says
"the flow's handler," the grammar offers no such entry, and the model resolves to the flow's
operation. That contract decision (re-word the RULE to demand NONE, or make the seam consume
flow-matching selections) belongs to the Lead/Arch, not to this gate — filed as issue 1663.
Until re-ruled, **the armed-state gate is NOT passed as scored.**

### Phase0 movement vs Phase 1b (33/39 → 34/39), decomposed

- **+1**: "summarize the document" → `summarize_document` @0.95 MATCH — the #1624 grammar
  entry (document-summarize entered the registry; the derived grammar is 63 ops vs 1b's 62).
  Exactly the mechanism 1b's caveat predicted: the row was unpassable while the grammar had
  no summarize operation; the registry change cleared SYNTHESIS's regression.
- **Changed miss, same row**: "analyze the file I uploaded" — 1b `CLARIFY` @0.4 → now
  `analyze_document` @0.95 vs expected `action:analyze_data`. The new adjacent grammar entry
  captured it; still the sole QUERY miss.
- **Unchanged misses**: "what's on my calendar today?" (`week_calendar` @0.85 — the 1b
  stochastic calendar flip persists; sole TEMPORAL −1) · "what am I working on?" (now
  `get_top_priority` @0.85; the full-chain baseline also missed this row → STATUS +0) ·
  "give me a project status report" (Family-3 vocabulary artifact, unchanged) · "list my
  archived projects" (`list_archived_projects` — strictly more specific than the expected
  `manage_portfolio`, Family 3, unchanged).
- **Per-category gate**: the same two regressions as 1b (QUERY 11 vs 12, TEMPORAL 3 vs 4),
  both single-row, both previously attributed (Family-4 context-free abstention now turned
  adjacent-op pick; stochastic calendar flip). SYNTHESIS's 1b regression is CLEARED. No new
  regressions appeared.

### Discovered work filed from this run

- **issue 1663** — the armed answer-turn emission convention (RULE vs sentinel vs the
  router's flow-completing reading); the Phase 2.2 contract decision this gate surfaced.
- **issue 1664** — `is_confirm` renders "(yes/no confirm)" on the which-repo question
  (repo clarification rides the confirm carrier's workflow_type).
- **issue 1665** — arm sites don't store their rendered ask; live snapshots carry
  question=None, strictly weaker than this run's gated condition (Phase 2.2 prerequisite).

---

## Addendum — not-live telemetry bucket rename (#1670, 2026-08-21)

**This is the single mapping note for the corpus migration.** After the #1667
widening, the not-live check consults every naming surface — operation name,
canonical alias, `flip_group`, registry category — but the flip-1 bucket names
still described only the category surface. #1667 retained them deliberately
(flip-1's pins are byte-for-byte; existing corpus/telemetry rows carry the old
names); #1670 is the sanctioned rename. Historical runs and dated session logs
keep the old strings; interpret them via this table.

| old (flip-1, pre-2026-08-21) | new (#1670) | the fact both assert | the fact that differs |
|---|---|---|---|
| `category_not_live` | `not_live_categorized` | no naming surface put the op in the live set (`live_match=None`) | an ACTION_REGISTRY category existed |
| `no_registry_category` | `not_live_uncategorized` | no naming surface put the op in the live set (`live_match=None`) | no ACTION_REGISTRY category existed at all |

Naming rationale: the shared `not_live_` prefix names the check's actual
outcome without enumerating surfaces, so a fourth naming surface leaves both
names true, and a prefix query aggregates the family; the suffix carries the
one fact on which the buckets differ. (`no_flip_surface`-style names were
rejected as false — every op always has at least the op-name surface.) The
precise per-turn account remains on the log line itself: `live_match=None`
plus `flip_group`, `category`, and `live_categories`.

Emission site: `services/intent_service/inversion_live.py` (single site).
Pins updated same-commit: `test_inversion_live_1595.py`,
`test_inversion_flip_groups_1667.py`. No corpus fixture, gate script, or
other repo surface carried the old strings (repo-wide grep, 2026-08-21).
