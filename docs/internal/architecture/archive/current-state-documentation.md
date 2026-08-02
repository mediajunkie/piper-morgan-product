> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# Piper Morgan Current State Documentation

**Date**: September 19, 2025
**Purpose**: Truth about what exists, what works, what doesn't

---

## 🟢 What Actually Works

### Core Functions

1. **Basic Chat**

   - "Hello" → Response ✅
   - "Help" → Menu display ✅
   - Simple conversation ✅

2. **Intent Classification**

   - Rule-based patterns work ✅
   - LLM fallback exists ✅
   - Categories: CONVERSATION, EXECUTION, QUERY ✅

3. **Database Layer**

   - PostgreSQL connection ✅
   - Repository patterns ✅
   - Model persistence ✅

4. **Individual Services**
   - GitHubService can create issues (directly) ✅
   - SlackService can send messages ✅
   - Knowledge base can store/retrieve ✅

### Development Infrastructure

- Session logging system ✅
- Multi-agent coordination methodology ✅
- Excellence Flywheel documented ✅
- Git/GitHub workflow ✅

---

## 🔴 What's Broken

### Critical Breaks

1. **QueryRouter**

   - Status: Commented out in engine.py line 79
   - Impact: Can't route queries to handlers
   - Workaround: Unknown (probably direct calls)

2. **~~OrchestrationEngine~~** ✅ FIXED (Late Sept 2025)

   - ~~Status: Declared as Optional but never initialized~~
   - **Current Status**: Fully wired up, 50+ references across codebase
   - Used in: web/app.py, IntentService, SlackResponseHandler, etc.

3. **~~Complex Workflows~~** ⚠️ PARTIALLY FIXED
   - "Show standup" → ✅ Works (MorningStandupWorkflow using direct async)
   - Multi-step flows → ⚠️ Works via OrchestrationEngine (Python async, not Temporal)
   - Workflow creation → ✅ WorkflowFactory operational

---

## 🟡 What's Partially Working

### Incomplete Systems

1. **Plugin Architecture** (15% complete)

   - Design exists but not implemented
   - All integrations still monolithic
   - MCP readiness not achieved

2. **Conversational Interface** (5% complete)

   - Command processing only
   - No state management
   - No multi-turn conversation

3. **A/B Testing Framework** (75% complete)

   - PM-034 shows sophisticated design
   - Code exists but not wired
   - Rollout mechanism incomplete

4. **Knowledge Graph Integration** (Unknown%)
   - Knowledge base works
   - Graph relationships unclear
   - PM-040 status uncertain

---

## 📁 File Structure Reality

### Web Layer

```
web/
├── app.py          # Main FastAPI app (NOT main.py!)
├── templates/      # May or may not exist
└── static/         # May or may not exist
```

### Services

```
services/
├── orchestration/
│   ├── engine.py   # OrchestrationEngine (broken)
│   └── workflows/  # Various workflow implementations
├── intent_service/
│   ├── classifier.py  # Works
│   └── service.py     # Works
├── queries/
│   └── query_router.py  # Disabled
└── integrations/
    ├── github/      # Works directly
    ├── slack/       # Works directly
    └── notion/      # Status unknown
```

---

## 📊 MVP Feature Reality Check

| Feature          | Expected | Reality                |
| ---------------- | -------- | ---------------------- |
| **Chitchat**     | ✅       | ✅ Works               |
| Greeting         | ✅       | ✅ Works               |
| Help/Menu        | ✅       | ✅ Works               |
| **GitHub**       | ✅       | ❌ Broken              |
| Create Issue     | ✅       | ❌ Broken through chat |
| Edit Issue       | ✅       | ❌ Broken              |
| Review Issue     | ✅       | ❌ Broken              |
| Get Recent       | ✅       | ❌ Broken              |
| **Knowledge**    | ✅       | 🟡 Partial             |
| Upload File      | ✅       | ✅ Works               |
| Summarize        | ✅       | ❌ Broken              |
| Analyze          | ✅       | ❌ Broken              |
| **Integrations** | ✅       | ❌ Broken              |
| Slack            | ✅       | ❌ Not through chat    |
| Notion           | ✅       | ❌ Unknown             |
| Calendar         | ✅       | ❌ Unknown             |
| **Standup**      | ✅       | ❌ Completely broken   |

**Reality: ~20% of MVP working, not 80%**

---

## 🏗️ Dependency Chain

```
QueryRouter (broken)
    ↓ blocks
OrchestrationEngine
    ↓ blocks
Complex Workflows
    ↓ blocks
- GitHub operations
- Standup
- Multi-step operations
- Query operations
    ↓ blocks
80% of MVP Features
```

**Fix QueryRouter = Unblock Everything**

---

## 🎯 The Truth

**We have a sophisticated architecture that's 75% built but with critical connection points disabled or never initialized.**

The good news:

- The code exists
- The design is sound
- Just needs connection
- Should work once connected

---

## 🔍 How to Verify Current State

```bash
# Check if orchestration is initialized
grep -n "OrchestrationEngine" web/app.py

# Find QueryRouter disabling
grep -n "TODO.*QueryRouter" services/orchestration/engine.py

# Look for workarounds
grep -r "workaround\|TODO\|FIXME" services/

# Test GitHub issue creation
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "create GitHub issue about login bug"}'
```

---

_This document represents ground truth as of September 19, 2025._
_Update after each REFACTOR epic completes._
