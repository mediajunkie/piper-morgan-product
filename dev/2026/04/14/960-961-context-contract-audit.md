# Floor Context Contract Audit — #960 + #961

**Date**: 2026-04-14
**Author**: Lead Developer

## 1. Route Map: Every Floor-Routed Category → Context Assembly

| Category | ContextAssembler branch | Context fields provided | Fabrication risk |
|----------|------------------------|------------------------|------------------|
| **IDENTITY** | `_gather_identity_context` | capabilities (from dispatcher registry), integrations (from plugin registry) | LOW — Piper's own capabilities, not user data |
| **DISCOVERY** | `_gather_identity_context` (same) | capabilities, integrations | LOW — same as IDENTITY |
| **TRUST** | `_gather_trust_context` | trust_profile (stage, interaction_count) | LOW — single-value lookup, honest "unknown" on failure |
| **MEMORY** | `_gather_memory_context` | conversation_history_summary (turn_count, recent_topics), persistent_memory | **MEDIUM** — user asks "what did we discuss?" and context may be empty on fresh session |
| **CONVERSATION** | `_gather_reminder_context` | due_reminders (if any) | LOW — non-greeting CONVERSATION is chitchat/thanks, LLM doesn't need user data |
| **TEMPORAL** | `_gather_temporal_context` | current_date, pending_todos, completed_todos, projects (name/created/updated), conversation_history | **MEDIUM** — user asks about "yesterday's work" and no data exists |
| **STATUS** | `_gather_status_priority_context` | projects (from user_context), priorities, organization, pending_todos, github_connected | **MEDIUM** — user asks "what am I working on?" with no projects configured |
| **PRIORITY** | `_gather_status_priority_context` (same) | projects, priorities, organization, pending_todos, github_connected | **MEDIUM** — user asks "what's urgent?" with no priorities configured |
| **GUIDANCE** | `_assemble_guidance_context` (in intent_service.py, not ContextAssembler) | current_time, calendar, projects, priorities | LOW — guidance is about advice, not user data lookup |
| **UNKNOWN** | `else: pass` (empty!) | current_time only | **HIGH** — any unclassified query gets NO context. If it's a data query that was misclassified, fabrication is likely. |

## 2. Gap Analysis: Fabrication Risk Assessment

### HIGH RISK: UNKNOWN category (no context)

The `else: pass` branch in ContextAssembler means UNKNOWN queries get only `current_time`. Any data query that falls through classification (LLM classifier fails, pre-classifier misses, ambiguous intent) gets zero context. The floor system prompt guardrail (#960 fix, commit 4789de64) is the ONLY defense.

**Known instance**: "list todos" before the pre-classifier pattern fix — fell through to UNKNOWN, floor fabricated 9 fake todos.

**Mitigation**: The guardrail is in place. But UNKNOWN should get basic user context (projects, todos, integrations) so the floor can at least reference real entities. Adding this would reduce fabrication risk without over-loading the prompt.

### MEDIUM RISK: Empty-data scenarios

For TEMPORAL, STATUS, PRIORITY, MEMORY — the context assembly works correctly when data exists, but on a **fresh account** (Pattern-045 testing scenario):
- No todos → `pending_todos` key absent from context
- No projects → `projects` key absent
- No conversation history → `conversation_history_summary` absent
- No trust profile → trust_profile shows "new" (honest)

The floor sees an empty `[Available context]` block and must compose without data. The system prompt guardrail (#960) tells it to be honest about gaps. This works — the canonical retest shows honest responses like "I don't have access to your project history."

**Remaining risk**: If the LLM ignores the guardrail (low probability but non-zero), it fabricates. Defense in depth would add a **code-level check** — if the context dict has no data-bearing keys for a data-query category, log a warning.

### LOW RISK: Identity/Discovery/Trust/Conversation

These categories either:
- Query Piper's own capabilities (not user data)
- Have honest fallbacks built into the context assembly ("stage: unknown")
- Don't involve user-specific data lookup (chitchat, thanks)

## 3. Context Contract

For each floor-routed category, the minimum required context fields:

| Category | Required fields | On absence: LLM behavior | On absence: code action |
|----------|----------------|--------------------------|------------------------|
| IDENTITY | capabilities | Describe general PM capabilities | None needed |
| DISCOVERY | capabilities, integrations | List general capabilities + "check Settings for integrations" | None needed |
| TRUST | trust_profile | "We're just getting started" | None needed |
| MEMORY | conversation_history_summary | "We haven't had many conversations yet" | None needed |
| CONVERSATION | (none required) | Natural chitchat | None needed |
| TEMPORAL | current_date | Answer with date only, honest about missing history | Log warning if user asks about activity/agenda with no data |
| STATUS | projects OR pending_todos | "I don't see any projects configured yet" | Log warning if both empty |
| PRIORITY | priorities OR pending_todos | "I don't see any priorities set up" | Log warning if both empty |
| GUIDANCE | (context is nice-to-have) | General PM advice | None needed |
| UNKNOWN | (none guaranteed) | **Must not fabricate.** Rely on system prompt guardrail. | **Log violation**: category=UNKNOWN + data-query keywords in message |

## 4. Recommended Code Changes

### 4a. Add basic context for UNKNOWN category

```python
# In ContextAssembler.gather_context(), replace:
else:
    pass

# With:
else:
    # #960: UNKNOWN queries get basic user context to reduce fabrication risk.
    # This doesn't guarantee the right data for the query, but gives the
    # floor real entities to reference instead of inventing them.
    if user_id:
        ctx = await self._gather_status_priority_context(user_id)
        context.update(ctx)
```

### 4b. Add violation logging for data-query-with-empty-context

```python
# After context assembly, before returning:
data_categories = {"TEMPORAL", "STATUS", "PRIORITY"}
data_keys = {"pending_todos", "completed_todos", "projects", "priorities"}
if category in data_categories:
    has_data = any(k in context for k in data_keys)
    if not has_data:
        logger.warning(
            "context_contract_empty_data",
            category=category,
            user_id=user_id,
            note="Floor received a data-query category with no user data in context"
        )
```

### 4c. Add known_pathological label to canonical retest

Per PA cross-pollination suggestion (OpenLaws eval harness):
- Add a `pathological_category` field to CANONICAL_QUERIES
- Label queries where fabrication is the known failure mode:
  - Any TODO/project/calendar query that could fall through pre-classifier
  - Any UNKNOWN-routed query
  - Any fresh-account scenario where context is empty

## 5. What's Already Done

- ✅ System prompt guardrail (commit 4789de64) — "NEVER fabricate user data"
- ✅ Pre-classifier pattern fix (commit 063edf52) — "list todos" without "my"
- ✅ Context assembly for all major categories (IDENTITY through STATUS/PRIORITY)
- ✅ Honest empty-data responses verified in canonical retest (Run 3)

## 6. What This Audit Recommends

1. **UNKNOWN context enrichment** (4a) — small code change, reduces fabrication risk
2. **Violation logging** (4b) — observability for empty-context scenarios
3. **known_pathological test category** (4c) — methodology improvement
4. **No new guardrails needed** — the system prompt guardrail + context assembly is working
