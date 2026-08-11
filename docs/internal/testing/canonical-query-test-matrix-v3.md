# Canonical Query Test Matrix v3 — Post-M1

**Version**: 3.0
**Date**: 2026-04-11
**Author**: Lead Developer
**Status**: Active — supersedes v1 and v2

> **v1 and v2 archived**: `docs/internal/testing/historical/canonical-query-test-matrix.md` (Dec 2025) and `canonical-query-test-matrix-v2.md` (Jan 2026, moved to `historical/` 2026-08-11) describe a pre-M1 architecture in which canonical handlers were the primary routing destination. After the M1 floor inversion (#911) and the Apr 8 IDENTITY full migration (commit 33e6758a), most read-only categories route to the conversational floor. v1 and v2 remain in-repo for historical reference but should not be used as current truth.

---

## What This Document Is

A test methodology and reference matrix for evaluating Piper Morgan against the v2 canonical query corpus (61 queries across 14 categories). v3 differs from v2 in three critical ways:

1. **Dual scoring**: Routing PASS/FAIL **and** quality (Colleague Test rubric, 0-9). v2 only checked routing.
2. **Floor-aware**: Recognizes that most queries now route to the conversational floor instead of canonical handlers. "Routing PASS" for floor-routed queries means "reached the floor with non-empty domain context."
3. **Honest failure tagging**: Known issues are tagged with their tracking issue but still run. Per PM guidance: "Things that we know are going to fail still need to be run."

---

## Methodology

### Routing Verdict

Each query has an **expected routing destination** based on M1 reality (not v2's pre-M1 expectations):

- **Floor**: Routes through `_handle_floor_with_context()` to `ConversationalFloor.respond()`
- **Canonical**: Routes through `canonical_handlers.handle()` to a domain-specific handler
- **Workflow**: Routes through `workflow_dispatcher` to a workflow process
- **Action**: Routes through `_handle_execution_intent()` to a mutation handler (todos, GitHub, etc.)
- **Pre-classified**: Resolved by pre-classifier (no LLM call needed for classification)

A query gets **routing PASS** if it reaches its expected destination. The destination is determined by reading current `_should_route_to_floor()` and `_requires_canonical_handler()` logic in `services/intent/intent_service.py` plus `canonical_handlers.can_handle()`.

### Quality Verdict

Each query also gets a **Colleague Test score** (R/C/T 0-3, total 0-9):

- **Relevance**: Does the response engage with what the user actually asked?
- **Context**: Does the response reference real system state, prior conversation, or appropriate knowledge?
- **Tone**: Does the response sound like a colleague, not a chatbot or template?

**Pass threshold**: 7 or higher.
**Auto-fail**: Any single dimension scoring 0 fails the query regardless of total.

### Dual Scoring Pipeline

1. **Tier A (preliminary)**: Heuristic check — non-empty, non-error response, no template fingerprint. Used for first-pass screening.
2. **Tier B (rigorous, primary)**: LLM-as-judge using the Colleague Test rubric. Returns score + confidence.
3. **Tier C (escalation)**: Human review for queries where:
   - LLM judge confidence < 0.7
   - Auto-fail (any dimension == 0)
   - Regression from M0 baseline (PASS → FAIL)

### Honest Failure Reporting

Per PM guidance, all queries are run regardless of known limitations. Each result row includes:
- `routing_verdict` (PASS / FAIL / N/A)
- `quality_verdict` (PASS / FAIL / MARGINAL)
- `quality_score` (0-9)
- `judge_confidence` (0.0-1.0)
- `escalated_to_human` (boolean)
- `known_issue` (issue number if applicable)
- `notes` (free text)

### Multi-turn fixtures (#1070, Run 8+)

A query in the corpus may optionally carry a sixth element `follow_ups: list[str]` that turns it into a multi-turn fixture. When present, the harness:

1. Sends the initial query (turn 1).
2. For each follow-up in order, sends it as a subsequent POST reusing the same `session_id` — the server preserves conversation state across turns.
3. Accumulates a structured transcript with `[Turn N] User: ... / [Turn N] Assistant: ...` lines.
4. Passes the FULL transcript to the judge, which uses a multi-turn rubric (`JUDGE_SYSTEM_PROMPT_MULTITURN` in `canonical-retest-run8.py`) that evaluates the conversation as a whole.

**Fixture format**:
```python
# Single-turn (existing, 5-tuple — unchanged):
(query_num, query_text, category, expected_routing, known_issue)

# Multi-turn (6-tuple — Run 8+):
(query_num, query_text, category, expected_routing, known_issue, follow_ups)
```

**Calibration note**: the multi-turn rubric explicitly accounts for legitimate openers that ask a clarifying question (e.g. `/standup` → "Quick or detailed?"). These score as good context-gathering when the LATER turns deliver substantive content. A single-turn judge would mark the bare opener as `R=1 C=0 T=1 = FAIL`; the multi-turn rubric is the methodologically correct evaluation surface for these flows.

**Current multi-turn coverage** (Run 8):
- Q49 `/standup` → `["quick"]` — happy-path branch (AC headline metric)
- Q149 `/standup` → `["detailed"]` — longer-output branch
- Q150 `/standup` → `["no"]` — cancel branch

Future flows likely to need multi-turn fixtures: action-confirm sequences (`close issue #123` → `"yes, close #123"`), conversation-continuity queries, voice-flow handoffs.

---

## Routing Reference (Post-M1)

### Categories that route to FLOOR (default)

Per `_FLOOR_ROUTED_CATEGORIES` in `_should_route_to_floor()` (intent_service.py:9907-9916):

- **GUIDANCE** (except setup requests, which are canonical)
- **IDENTITY** (all queries — Apr 8 migration)
- **DISCOVERY**
- **TRUST**
- **MEMORY**
- **CONVERSATION** (except greetings, which are canonical for calendar side effects)
- **UNKNOWN**

### Categories that require CANONICAL handler

Per `_requires_canonical_handler()` (intent_service.py:9829):

- **PORTFOLIO** (all — mutations)
- **EXECUTION** (all — mutations)
- **CONVERSATION/greeting** (calendar side effects)
- **TEMPORAL** (deterministic fast-path)
- **STATUS** (not yet migrated to floor — #925 Phase 3)
- **PRIORITY** (not yet migrated to floor — #925 Phase 3)
- **GUIDANCE/setup** (triggers setup workflow)

---

## Test Matrix

The matrix below maps each of the 61 canonical queries to its expected M1 routing and quality criteria.

**Format**: `Q# | Query | Category | Expected Routing | Quality Bar | Known Issue`

### Identity (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 1 | What's your name and role? | Floor | 7+, no template tone | — |
| 2 | What can you help me with? | Floor (DISCOVERY) | 7+, must list real capabilities | — |
| 3 | Are you working properly? | Floor (IDENTITY-adjacent) | 7+, honest health check | — |
| 4 | How do I get help? | Floor (IDENTITY-adjacent) | 7+, actionable guidance | — |
| 5 | What makes you different? | Floor (IDENTITY-adjacent) | 7+, substantive answer | — |

### Temporal (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 6 | What day is it? | Canonical (deterministic) | Correct date, friendly tone | — |
| 7 | What did we accomplish yesterday? | Canonical | Real activity or honest empty | — |
| 8 | What's on the agenda for today? | Canonical | Calendar + todos integrated | — |
| 9 | When was the last time we worked on this? | Canonical | Activity tracking | — |
| 10 | How long have we been working on this? | Canonical | Duration calculation | — |

### Spatial / Status (4)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 11 | What projects are we working on? | Canonical (STATUS) | Real project list | — |
| 12 | Show me the project landscape | Canonical (STATUS) | Landscape view | — |
| 13 | Which project should I focus on? | Canonical (PRIORITY) | Reasoned recommendation | — |
| 14 | What's the status of project X? | Canonical (STATUS) | Project-specific data | — |

### Capability (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 16 | Create a GitHub issue about testing | Action (EXECUTION) | If GitHub not configured: friendly pre-flight message (#943 fix) | — |
| 17 | Analyze this document | Action (EXECUTION) | Analysis or honest "no document provided" | — |
| 18 | List all my projects | Canonical (PORTFOLIO query) | Real list | — |
| 19 | Generate a status report | Canonical (STATUS) | Real data | — |
| 20 | Search for X in documents | Action (EXECUTION) | Search results or honest empty | — |

### Predictive (5) — partially implemented

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 21 | What should I focus on today? | Canonical (PRIORITY) | Time-based + project-aware | — |
| 22 | What patterns do you see? | Floor or learning handler | Honest about pattern reporting state | M2 Beta target |
| 23 | What risks should I be aware of? | Floor | Substantive risk analysis | M2 Beta target |
| 24 | What opportunities should I pursue? | Floor | Substantive suggestions | M2 Beta target |
| 25 | What's the next milestone? | Floor | Honest if no milestone data | M2 Beta target |

### Conversational (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 26 | What else can you help with? | Floor | Contextual discovery | — |
| 27 | Tell me more about the GitHub integration | Floor | Substantive feature deep-dive | — |
| 28 | How do I use the calendar feature? | Floor | Actionable guidance | — |
| 29 | What changed since yesterday? | Floor | Honest about change tracking | — |
| 30 | What needs my attention? | Canonical (PRIORITY) or Floor | Notification aggregation or honest empty | — |

### Scheduling (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 31 | Schedule a meeting about the roadmap | Action (EXECUTION) | Calendar creation or graceful "not yet supported" | M2 |
| 32 | Remind me to review PRs tomorrow | Action (EXECUTION) | Reminder created | M2 |
| 33 | Find time for a 1:1 with the team lead | Floor | Honest about scheduling not yet implemented | M2 |
| 34 | How much time am I spending in meetings? | Canonical (TEMPORAL) | Time audit | — |
| 35 | Review my recurring meetings | Canonical (TEMPORAL) | Meeting audit | — |

### Documents (4, #39 removed)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 36 | Create a doc from this conversation | Action (EXECUTION) | Conversation→Doc or graceful | M2 |
| 37 | Compare these documents | Action (EXECUTION) | Document diff or graceful | M2 |
| 38 | Synthesize these sources | Action (EXECUTION) | Multi-doc synthesis or graceful | M2 |
| 40 | Update the project roadmap document | Action (EXECUTION) | Document update or graceful | M2 |

### GitHub Operations (8)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 41 | What did we ship this week? | Floor or canonical | Real release data or honest | — |
| 42 | Show me stale PRs | Action (EXECUTION) | PR hygiene or pre-flight friendly | — |
| 43 | What's blocking the milestone? | Floor | Substantive blocker analysis | — |
| 44 | Create issues from this meeting | Action (EXECUTION) | Pre-flight friendly if not configured | — |
| 45 | Close completed issues | Action (EXECUTION) | Pre-flight friendly if not configured | — |
| 58 | Update issue #X | Action (EXECUTION) | Pre-flight friendly | — |
| 59 | Comment on issue #X | Action (EXECUTION) | Pre-flight friendly | — |
| 60 | Review issue #X | Floor or canonical | Issue summary | — |

### Slack (5)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 46 | Any mentions I missed? | Action (EXECUTION) | Mention tracking or graceful | M2 |
| 47 | Summarize #channel | Action (EXECUTION) | Summary or graceful | M2 |
| 48 | Post update to team | Action (EXECUTION) | Broadcast or graceful | M2 |
| 49 | /standup | Slash command | Generates standup | — |
| 50 | /piper help | Slash command | Capabilities list | — |

### Productivity (3)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 51 | What's my productivity? | Floor or canonical | Substantive metrics or honest | — |
| 52 | Are we on track? | Floor or canonical (STATUS) | Goal tracking | — |
| 53 | What did the team accomplish? | Floor | Team metrics or honest | — |

### Todo Management (4)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 54 | Add a todo: review the deployment plan | Action (EXECUTION) | Todo persists in DB | — |
| 55 | Complete the PR review todo | Action (EXECUTION) | Completion persists in DB | — |
| 56 | Show my todos | Canonical (QUERY) | Real list, no fabrication (#960) | — |
| 57 | What's my next todo? | Canonical (PRIORITY) | Real next or honest empty | — |

### Calendar Extended (2)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 61 | What's my week look like? | Canonical (TEMPORAL) | Real calendar or honest | — |
| 62 | Check calendar conflicts | Canonical (TEMPORAL) | Conflict detection or honest | — |

### Knowledge (1)

| # | Query | Routing | Quality Bar | Known Issue |
|---|-------|---------|-------------|-------------|
| 63 | Upload a file to the knowledge base | Action (EXECUTION) | File upload or graceful | M2 |

---

## Comparison to M0 Baseline (#884)

The M0 retest (Mar 12, 2026) used pure routing matching. v3 results will be comparable on the routing dimension only. Quality dimension is new and has no M0 baseline.

| Metric | M0 (Mar 12) | M1 Target |
|--------|-------------|-----------|
| Routing pass (implemented) | 81.1% (43/53) | ≥85% (#926 gate criterion) |
| Quality pass (Colleague 7+) | N/A (no quality test) | ≥80% on floor-routed queries |
| Auto-fails (any dim = 0) | N/A | 0 expected; 1-2 acceptable |
| Regressions (M0→M1) | N/A | 0 expected |

---

## Out of Scope for v3

These were considered but deferred:

1. **Adding new queries** — v2 corpus is the test set. Recommendations for query corpus changes go in the report, not the test.
2. **Adding non-canonical queries from M1 UAT** — The 9 CXO queries are tracked in the Gate #926 evidence; merging them is a v4 / future decision.
3. **Multi-turn / conversational continuity tests** — Single-shot only for v3. Multi-turn (#922) is M2 work.
4. **Performance / latency tests** — Functional only.

---

## Companion Documents

- `docs/internal/testing/colleague-test-rubric.md` — Detailed scoring guide for the Colleague Test (0-3 per dimension)
- `dev/2026/04/11/canonical-retest-m1-plan.md` — Execution plan for the first v3 run
- `dev/2026/04/11/canonical-retest-m1.py` — Runner script (TBD as of this writing)

---

*Test methodology: dual-scoring (routing + quality), LLM-as-judge primary with human escalation, honest failure reporting.*
