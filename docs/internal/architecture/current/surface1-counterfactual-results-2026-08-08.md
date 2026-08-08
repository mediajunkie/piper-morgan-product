# Surface-1 counterfactual — what the LLM classifier would have done with surface 1's claims

Run: 2026-08-08 15:59 PT · `scripts/surface1_counterfactual_probe_1283.py` · Arch ruling 2026-08-08 (make surface 1's claims observable before narrowing).

## Method

- **Claim**: `PreClassifier.pre_classify(utterance)` (surface 1's single-intent entry); the multi-intent entry (`detect_multiple_intents` primary) is recorded in its own column where it diverges.
- **Counterfactual**: `IntentClassifier.classify(utterance, use_cache=False)` with `PreClassifier.pre_classify` monkeypatched to return `None` — the full production Stage-2 LLM path runs (normalization map, #1124 verb shim, low-confidence clarification). B3/Stage-0 self-bypasses (no user/session → D1a early return); cache off. Bypass verified per call (patched surface 1 consulted, declined).
- **m-43 layer note**: the LLM ran with EMPTY conversation context. That is D4's production shape — the classifier never sees history — so this is the classifier's real input shape, not a lab impoverishment.
- **Verdicts**: AGREE = same action (category drift annotated). VARIANT = same semantic target under a paraphrase-drift name (mode-4): same rail handler via alias equivalence, or same category + content-stem match. DISAGREE = different destination. ERROR = the call failed (never a faked verdict).

## Denominator

- **52 unique utterances probed**: 11 from `chat_pointers.py` POINTER rows surface 1 claims (incl. `pin:` rows; duplicates deduped, ledger keys listed per row), plus 41 hand-written group representatives asserted at build time to be claimed with the expected (category, action).
- **0 POINTER rows excluded** (utterance resolves via surfaces 3/4, not surface 1).
- **Scope caveat**: ONE representative per pre-classifier pattern group/sub-action — not the infinite pattern space. A group's verdict generalizes only as far as its representative does.

## Result: **14 AGREE / 36 DISAGREE / 2 VARIANT / 0 ERROR** of 52

Cost: 52 LLM classification calls (one per utterance, no retries).

| # | utterance | surface-1 claim | multi-path claim | LLM verdict (cat/action @conf) | verdict |
|---|---|---|---|---|---|
| 1 | give me my standup | `status/get_project_status` | same | `status/show_standup` @0.9 | DISAGREE |
| 2 | what have you learned about my work style? | `memory/pull_insights` | same | `identity/work_style_insight` @0.85 | DISAGREE |
| 3 | connect my github | `guidance/get_contextual_guidance` | — | `execution/connect_github` @0.9 | DISAGREE |
| 4 | connect my notion | `guidance/get_contextual_guidance` | — | `execution/connect_service` @0.85 | DISAGREE |
| 5 | connect my slack | `guidance/get_contextual_guidance` | — | `execution/connect_slack` @0.85 | DISAGREE |
| 6 | link my google calendar | `guidance/get_contextual_guidance` | — | `execution/link_calendar` @0.85 | DISAGREE |
| 7 | add a repo to my portfolio | `portfolio/manage_repos` | same | `execution/add_repo_to_portfolio` @0.9 | DISAGREE |
| 8 | show me my todos | `query/list_todos_query` | same | `status/list_todos` @0.9 | DISAGREE |
| 9 | list my projects | `portfolio/manage_portfolio` | same | `identity/manage_portfolio` @0.9 | AGREE(action; category identity) |
| 10 | connect my calendar | `guidance/get_contextual_guidance` | same | `execution/connect_calendar` @0.9 | DISAGREE |
| 11 | what reminders do I have? | `query/list_reminders_query` | same | `temporal/list_reminders` @0.9 | VARIANT(rail-alias: same handler) |
| 12 | hello | `conversation/greeting` | same | `conversation/greeting` @0.9 | AGREE |
| 13 | goodbye | `conversation/farewell` | same | `conversation/farewell` @0.9 | AGREE |
| 14 | thank you! | `conversation/thanks` | same | `conversation/acknowledgment` @0.9 | DISAGREE |
| 15 | what can you do? | `discovery/get_capabilities` | same | `identity/describe_capabilities` @0.95 | DISAGREE |
| 16 | why did you suggest that? | `provenance/explain_suggestion` | same | `conversation/clarification_needed` @0.6 | DISAGREE |
| 17 | why can't you create issues? | `trust/explain_trust` | same | `identity/explain_capabilities` @0.85 | DISAGREE |
| 18 | what do you remember about me? | `memory/get_memory` | same | `identity/get_identity` @0.9 | DISAGREE |
| 19 | what's my default repo? | `query/get_default_repo` | — | `identity/get_default_repo` @0.9 | AGREE(action; category identity) |
| 20 | set my default repo to mediajunkie/piper-morgan-product | `query/set_default_repo` | — | `execution/set_default_repo` @0.9 | AGREE(action; category execution) |
| 21 | write a short update for the CEO on the beta | `query/write_stakeholder_update` | same | `synthesis/compose_update` @0.85 | DISAGREE |
| 22 | update the roadmap doc with the new dates | `query/update_document_query` | same | `execution/update_document_query` @0.9 | AGREE(action; category execution) |
| 23 | tell me more about the github integration | `query/get_feature_info` | same | `query/get_integration_info` @0.85 | DISAGREE |
| 24 | who are you? | `identity/get_identity` | same | `identity/get_identity` @0.97 | AGREE |
| 25 | what changed since yesterday? | `query/changes_query` | same | `status/get_project_status` @0.82 | DISAGREE |
| 26 | what needs my attention? | `query/attention_query` | same | `priority/prioritize` @0.88 | DISAGREE |
| 27 | what's on my calendar today? | `query/meeting_time` | same | `temporal/meeting_time` @0.95 | AGREE(action; category temporal) |
| 28 | show my recurring meetings | `query/recurring_meetings` | same | `temporal/meeting_time` @0.92 | DISAGREE |
| 29 | what's my week look like? | `query/week_calendar` | same | `temporal/weekly_schedule` @0.95 | DISAGREE |
| 30 | what's the next milestone? | `status/get_project_status` | query/list_milestones_query | `query/get_milestone_info` @0.8 | DISAGREE |
| 31 | what branch are we on? | `query/local_git_status_query` | same | `query/get_branch_info` @0.85 | DISAGREE |
| 32 | what did we ship this week? | `query/shipped_query` | same | `status/get_shipment_status` @0.85 | DISAGREE |
| 33 | show stale prs | `query/stale_prs_query` | same | `query/stale_prs_query` @0.9 | AGREE |
| 34 | close issue #123 | `query/close_issue_query` | same | `execution/close_issue_query` @0.95 | AGREE(action; category execution) |
| 35 | reopen issue #123 | `query/reopen_issue_query` | same | `execution/reopen_issue_query` @0.95 | AGREE(action; category execution) |
| 36 | comment on issue #123 | `query/comment_issue_query` | same | `execution/comment_issue_query` @0.9 | AGREE(action; category execution) |
| 37 | how many open issues do we have? | `query/list_issues_query` | same | `query/list_open_issues` @0.9 | VARIANT(stem-match) |
| 38 | show my prs | `query/list_prs_query` | same | `status/show_pull_requests` @0.9 | DISAGREE |
| 39 | show issue #123 | `query/review_issue_query` | same | `query/get_issue_details` @0.9 | DISAGREE |
| 40 | show milestones | `query/review_issue_query` | query/list_milestones_query | `query/list_milestones` @0.85 | DISAGREE |
| 41 | what did we create this session? | `query/session_activity_query` | same | `synthesis/summarize_session_output` @0.85 | DISAGREE |
| 42 | what's my productivity? | `query/productivity_query` | same | `status/get_productivity_status` @0.9 | DISAGREE |
| 43 | remind me to review the roadmap tomorrow | `execution/create_reminder` | — | `temporal/set_reminder` @0.9 | DISAGREE |
| 44 | complete todo 3 | `execution/complete_todo` | — | `execution/complete_todo` @0.9 | AGREE |
| 45 | show all my todos | `query/list_completed_todos` | query/list_todos_query | `status/list_todos` @0.9 | DISAGREE |
| 46 | what's my next todo? | `query/next_todo_query` | same | `priority/prioritize` @0.95 | DISAGREE |
| 47 | when did I complete the onboarding project? | `status/check_completion_status` | same | `status/complete_todo` @0.9 | DISAGREE |
| 48 | what time is it? | `temporal/get_current_time` | same | `query/get_time_info` @0.9 | DISAGREE |
| 49 | how do I get started? | `guidance/get_contextual_guidance` | same | `guidance/provide_guidance` @0.9 | DISAGREE |
| 50 | what's blocking the milestone? | `analysis/analyze_blockers` | same | `status/identify_blockers` @0.9 | DISAGREE |
| 51 | what am I working on? | `status/get_project_status` | same | `status/get_project_status` @0.95 | AGREE |
| 52 | what are my priorities? | `priority/get_top_priority` | same | `priority/prioritize` @0.9 | DISAGREE |

## Mode-4 variant list (paraphrase-drift emissions)

- 'what reminders do I have?': claim `list_reminders_query` vs LLM `list_reminders` (VARIANT(rail-alias: same handler))
- 'how many open issues do we have?': claim `list_issues_query` vs LLM `list_open_issues` (VARIANT(stem-match))

## Row sources

- 'give me my standup' — (a) page:/standup
- 'what have you learned about my work style?' — (a) page:/insights
- 'connect my github' — (a) page:/settings/integrations, page:/settings/integrations/github, integration:github
- 'connect my notion' — (a) page:/settings/integrations/notion, integration:notion
- 'connect my slack' — (a) page:/settings/integrations/slack, integration:slack
- 'link my google calendar' — (a) page:/settings/integrations/calendar
- 'add a repo to my portfolio' — (a) page:/settings/projects
- 'show me my todos' — (a) page:/todos
- 'list my projects' — (a) page:/projects
- 'connect my calendar' — (a) integration:calendar
- 'what reminders do I have?' — (a) pin:reminder-query
- 'hello' — (b) greeting
- 'goodbye' — (b) farewell
- 'thank you!' — (b) thanks
- 'what can you do?' — (b) discovery
- 'why did you suggest that?' — (b) provenance
- "why can't you create issues?" — (b) trust
- 'what do you remember about me?' — (b) memory
- "what's my default repo?" — (b) get-default-repo
- 'set my default repo to mediajunkie/piper-morgan-product' — (b) set-default-repo
- 'write a short update for the CEO on the beta' — (b) stakeholder-update
- 'update the roadmap doc with the new dates' — (b) document-query
- 'tell me more about the github integration' — (b) feature-info
- 'who are you?' — (b) identity
- 'what changed since yesterday?' — (b) contextual/changes
- 'what needs my attention?' — (b) contextual/attention
- "what's on my calendar today?" — (b) calendar/meeting_time
- 'show my recurring meetings' — (b) calendar/recurring
- "what's my week look like?" — (b) calendar/week
- "what's the next milestone?" — (b) milestone-status (#1068)
- 'what branch are we on?' — (b) local-git (#1044)
- 'what did we ship this week?' — (b) github/shipped
- 'show stale prs' — (b) github/stale-prs
- 'close issue #123' — (b) github/close-issue
- 'reopen issue #123' — (b) github/reopen-issue
- 'comment on issue #123' — (b) github/comment-issue
- 'how many open issues do we have?' — (b) github/list-issues
- 'show my prs' — (b) github/list-prs
- 'show issue #123' — (b) github/review-issue
- 'show milestones' — (b) github/milestones
- 'what did we create this session?' — (b) session-activity (#1394)
- "what's my productivity?" — (b) productivity
- 'remind me to review the roadmap tomorrow' — (b) reminder-create (#903)
- 'complete todo 3' — (b) todo-complete (#904)
- 'show all my todos' — (b) todo-query/completed
- "what's my next todo?" — (b) todo-query/next
- 'when did I complete the onboarding project?' — (b) completion-history (#1117)
- 'what time is it?' — (b) temporal
- 'how do I get started?' — (b) guidance
- "what's blocking the milestone?" — (b) analysis
- 'what am I working on?' — (b) status
- 'what are my priorities?' — (b) priority

## Analysis (computed from the rows above — no additional LLM calls)

### The headline number needs its layers named (m-43)

**14 AGREE / 36 DISAGREE / 2 VARIANT** compares *emitted labels*. But routing dispatches
through the 4-surface chain, where a rail-registered ACTION wins before category — so the
label comparison overstates functional disagreement. Splitting each bucket by what would
actually happen:

**AGREE (14)** = 6 exact + 8 action-match-with-category-drift (rows 9, 19, 20, 22, 27, 34,
35, 36). For a rail-registered action, category drift is routing-irrelevant (surface 3
dispatches on action before category handling) — e.g. `execution/close_issue_query` and
`query/close_issue_query` dispatch identically. The 8 drift rows are functionally full agreement
wherever the action is on the rail.

**DISAGREE (36)** splits into:
- **9 category-agree DISAGREEs** (rows 1, 14, 23, 31, 39, 40, 47, 49, 52): the LLM lands the
  same category with a free-form action name. Where the action is off-rail, category routing
  decides — several of these would land the same category handler and produce similar floor
  behavior (e.g. `guidance/provide_guidance` vs `guidance/get_contextual_guidance`), but the
  deterministic sub-action is lost (e.g. `show milestones` → the LLM's `list_milestones` is
  closer to the user's ask than surface 1's own `review_issue_query` claim — see below).
- **27 category-DISAGREEs**: genuinely different destination. This is the load-bearing set.

### Decision-relevant reading (the ruling's three buckets)

1. **Surface 1 is load-bearing for most of what it claims.** 27/52 (52%) would change
   category if handed to the LLM, including the exact misroute classes surface 1 was built
   against: `remind me to…` → `temporal/set_reminder` (the #903 lane re-broken — a WRITE ask
   answered by the temporal lane), `when did I complete…` → `status/complete_todo` (a
   history READ that the LLM labels with a WRITE-shaped action, #1117's class), all four
   `connect my <integration>` → `execution/connect_*` (the pre-#1417 mode-4 category-luck
   → unwired-write decline), `what time is it?` → `query/get_time_info` (the temporal lane's
   own canonical utterance lost). **The Arch counterexample generalizes.**
2. **The narrow-with-evidence set is small.** Only the 6 exact AGREEs + 8 rail-registered
   action-matches (≈27%) are candidates where surface 1 is arguably gratuitous — and even
   there, one probe utterance per group is not phrasing-space coverage.
3. **Mode-4 pressure confirmed at high rate.** Beyond the 2 mechanical VARIANTs, nearly every
   DISAGREE action name is a paraphrase off every alias list (`show_standup`,
   `get_issue_details`, `list_milestones`, `get_branch_info`, `provide_guidance`,
   `identify_blockers`, `prioritize`×3…). More LLM traffic = more of these hitting a defense
   already known to leak (stack doc: aliases "necessary, provably insufficient").
4. **The #1521 pin verifies as load-bearing with a twist** (row 11): the LLM classed
   `what reminders do I have?` as `temporal/list_reminders` — the temporal-lane misroute PM
   hit live — **but** `list_reminders` is now a rail alias on the same handler (#1521's own
   cohort), so today the action rail would rescue it before category routing. The pin +
   alias pair, not either alone, is what makes that utterance safe.

### Seam caveats

- **Provider mix**: the probe used the production `LLMClient` task routing (primary resolved
  to OpenAI `gpt-4o` for `intent_classification`). At least 5 calls hit gpt-4o TPM 429s
  mid-run and fell back down the configured provider order — the identical fallback
  production takes under load, so the counterfactual is production-faithful, but per-row
  model identity was not captured; the run is a mixed-model sample, as production is.
- **Monkeypatch scope**: only `PreClassifier.pre_classify` was patched (to `None`);
  `detect_file_reference` and everything else in Stage 2 ran real. B3 self-bypassed
  (no user/session), cache off. The patched surface was verified consulted on all 52 calls.
- **One utterance per group**: a DISAGREE on a representative says the LLM mislabels *that
  phrasing*; siblings in the same pattern group may fare differently. The (a) rows are
  exact production utterances (ledger POINTERs); the (b) rows are canonical but hand-picked.
- **Empty conversation context is production shape** (D4), not a limitation — but the
  per-principal personalization prompt resolved for `user_id=None` (unscoped default),
  which slightly differs from a signed-in user's scoped prompt.
