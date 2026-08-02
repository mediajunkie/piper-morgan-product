> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# GitHub Issue Creation: Sequence Diagram
**Purpose**: Document what SHOULD happen vs what ACTUALLY happens
**Date**: September 19, 2025

---

## Ideal Flow (What Should Happen)

```mermaid
sequenceDiagram
    participant User
    participant Chat as Web Chat
    participant Intent as IntentClassifier
    participant Router as QueryRouter
    participant Engine as OrchestrationEngine
    participant WF as GitHubWorkflow
    participant GH as GitHubService
    participant API as GitHub API

    User->>Chat: "Create issue about login bug"
    Chat->>Intent: classify(message)
    Intent-->>Chat: Intent(EXECUTION, CREATE_ISSUE)
    Chat->>Router: route(intent)
    Router-->>Chat: GitHubWorkflow
    Chat->>Engine: create_workflow(intent, context)
    Engine-->>Chat: Workflow(id, tasks)
    Engine->>WF: execute_workflow()
    WF->>GH: create_issue(title, body)
    GH->>API: POST /repos/.../issues
    API-->>GH: Issue(id, url)
    GH-->>WF: Success(issue)
    WF-->>Engine: WorkflowResult
    Engine-->>Chat: Result
    Chat-->>User: "Created issue #123: [link]"
```

---

## Current Reality (What Actually Happens - BROKEN)

```mermaid
sequenceDiagram
    participant User
    participant Chat as Web Chat
    participant Intent as IntentClassifier
    participant Router as QueryRouter ❌
    participant Engine as OrchestrationEngine ❌

    User->>Chat: "Create issue about login bug"
    Chat->>Intent: classify(message)
    Intent-->>Chat: Intent(EXECUTION, CREATE_ISSUE)
    Chat->>Router: route(intent)
    Note over Router: QueryRouter disabled!<br/>Returns None
    Router-->>Chat: None ❌
    Chat->>Engine: create_workflow(None, context)
    Note over Engine: Engine is None!<br/>AttributeError
    Engine-->>Chat: ERROR ❌
    Chat-->>User: "Error: workflow_id undefined"
```

---

## After REFACTOR-1 (Target State)

The goal is to restore the ideal flow with these specific fixes:

1. **Enable QueryRouter** (uncomment line 79 in engine.py)
2. **Initialize OrchestrationEngine** (in web/app.py startup)
3. **Wire LLM dependencies** (ensure llm_client available)
4. **Complete PM-034 integration** (A/B testing at 100%)

---

## Key Validation Points

When testing if the flow works:

1. ✅ Intent classification returns EXECUTION/CREATE_ISSUE
2. ✅ QueryRouter returns GitHubWorkflow (not None)
3. ✅ Engine creates workflow with ID and tasks
4. ✅ GitHub API call succeeds with 201 Created
5. ✅ User sees "Created issue #X" with clickable link

If ANY of these fail, the flow is broken.

---

## Performance Targets

From PM-034 specifications:
- Intent Classification: <200ms
- Query Routing: <50ms
- Workflow Creation: <100ms
- GitHub API: <1000ms
- **Total End-to-End: <1500ms**

Current Reality: ❌ Infinite (never completes)
After Refactor: ✅ <1500ms target
