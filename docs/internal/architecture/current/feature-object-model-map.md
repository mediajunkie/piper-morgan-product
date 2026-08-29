# Feature Object Model Map

**Issue**: #406 MUX-VISION-FEATURE-MAP
**Phase**: 1-2 Complete (All Feature Mappings Populated)
**Date Created**: 2026-01-20
**Last Updated**: 2026-01-20 20:30 PST
**Agent**: Claude Code (Programmer)

---

## Purpose

This document maps Piper Morgan's 16 major features to the Object Model (Entity/Moment/Place/Lenses/Situation) defined in ADR-055 and formalized in MUX infrastructure.

The map serves three functions:

1. **Reference Architecture**: Shows how each feature currently implements (or should implement) grammar elements
2. **Transformation Guide**: Identifies gaps and provides concrete patterns for uplift
3. **Implementation Checklist**: Developers use this to apply grammar patterns consistently across features

---

## How to Use This Document

### For Auditing Features
1. Find your feature in the Feature Summary table (section 2)
2. Review its current compliance level and priority
3. Jump to the feature's detailed section to see object model mapping

### For Implementing Grammar Transformation
1. Identify your feature's target compliance level (usually "Conscious" ✅)
2. Review the "Object Model Mapping" table
3. Use the "Canonical Queries" table to understand Place/Lenses interaction
4. Follow the template pattern to implement Context/Result pairs
5. Check "Transformation Notes" for integration-specific patterns

### For Pattern Discovery
1. Find a **Conscious** feature (Morning Standup recommended)
2. Extract patterns from Reference Implementation column
3. Apply reusable patterns to your feature

---

## Feature Summary Table

| # | Feature | Compliance | Priority | File | Effort | User Impact |
|---|---------|-----------|----------|------|--------|-------------|
| 1 | Morning Standup | ✅ Conscious | Reference | `services/features/morning_standup.py` | - | Very High |
| 2 | Intent Classification | ⚠️ Partial | High | `services/intent_service/classifier.py` | Medium | Very High |
| 3 | Todo Management | ❌ Flattened | High | `services/todo/todo_service.py` | High | Very High |
| 4 | Feedback System | ⚠️ Partial | Medium | `services/feedback/feedback_service.py` | Medium | High |
| 5 | Slack Integration | ⚠️ Partial | High | `services/integrations/slack/slack_plugin.py` | Medium | Very High |
| 6 | GitHub Integration | ⚠️ Partial | High | `services/integrations/github/github_plugin.py` | Medium | Very High |
| 7 | Notion Integration | ❌ Flattened | Medium | `services/integrations/notion/notion_plugin.py` | Medium | Medium |
| 8 | Calendar Integration | ⚠️ Partial | Medium | `services/integrations/calendar/calendar_integration.py` | Medium | High |
| 9 | Auth/Session Management | ❌ Flattened | Low | `services/auth/auth_service.py` | Low | Low |
| 10 | Conversation Handler | ⚠️ Partial | Medium | `services/conversation/conversation_handler.py` | Medium | High |
| 11 | Onboarding System | ⚠️ Partial | Medium | `services/onboarding/portfolio_onboarding_handler.py` | Medium | High |
| 12 | List Management | ❌ Flattened | Low | `services/repositories/list_repository.py` | Low | Low |
| 13 | Project Management | ❌ Flattened | Low | `services/repositories/project_repository.py` | Low | Low |
| 14 | File Management | ❌ Flattened | Low | `services/repositories/file_repository.py` | Low | Low |
| 15 | Personality System | ⚠️ Partial | Medium | `services/personality/standup_bridge.py` | Medium | High |
| 16 | MCP Integration | ❌ Flattened | Low | `services/integrations/mcp/mcp_plugin.py` | Low | Low |

**Legend**:
- ✅ **Conscious**: All 5 elements present; grammar flows naturally
- ⚠️ **Partial**: 3-4 elements present; some flattening exists
- ❌ **Flattened**: 0-2 elements; mechanical/database language dominant

---

## Lifecycle Model Wiring Status

**Updated**: 2026-01-26 (Post #685 MUX-LIFECYCLE-OBJECTS)

This section tracks which domain models have lifecycle infrastructure wired in.

### Domain Models with Lifecycle

| Model | Has `lifecycle_state`? | `to_dict()` wiring? | Location | Notes |
|-------|----------------------|---------------------|----------|-------|
| **WorkItem** | ✅ Yes | ✅ Yes (#685) | `services/domain/models.py:251` | Full lifecycle support |
| **Feature** | ✅ Yes | ✅ Yes (#705) | `services/domain/models.py:209` | Full lifecycle support |
| **Insight** | ❌ No | N/A | `services/mux/composting_models.py` | Has `confidence` but no lifecycle |
| **SurfaceableInsight** | ❌ No | Has `to_dict()` | `services/mux/composting_pipeline.py` | Trust-gating, no lifecycle |

### UI Integration Status

| View/Template | Displays Model | Model Ready? | UI Ready? | Issue |
|--------------|----------------|--------------|-----------|-------|
| Morning Standup | WorkItem | ✅ Yes | ❌ No | #703 Phase 1 |
| Insights Page | SurfaceableInsight | ❌ No | ❌ No | Needs model work first |
| Todos Page | (needs investigation) | ? | ❌ No | TBD |

### Lifecycle UI Components (from #423)

All components exist in `templates/components/`:
- `lifecycle_indicator.html` - Visual indicator with experience phrases
- `lifecycle_detail.html` - Detailed lifecycle view
- `lifecycle_notification.html` - Trust-gated notification component

JavaScript API: `LifecycleIndicator.create(stage, compact)` returns DOM element.

### Integration Roadmap

See #703 and child issues for the phased integration plan.

---

## Reference Implementation (Morning Standup)

**See**: `dev/2026/01/19/p0-morning-standup-analysis.md` for complete analysis

**Key Patterns to Extract**:
1. **Context/Result Dataclass Pair** - Separates input gathering from output synthesis
2. **Parallel Place Gathering** - Fetches from Slack, GitHub, Calendar concurrently
3. **Personality Bridge** - Transforms raw data to conversational narrative
4. **Warmth Calibration** - Adapts tone based on accomplishment level
5. **Honest Failure with Suggestion** - Graceful error handling with actionable guidance

---

## Per-Feature Object Model Mappings

---

### 1. Morning Standup ✅ CONSCIOUS (Reference)

**File**: `services/features/morning_standup.py`
**Compliance**: Conscious (All 5 elements)
**Priority**: Reference Implementation

#### Object Model Mapping

| Element | Current State | Implementation |
|---------|---------------|-----------------|
| **Entity** | ✅ `StandupContext.user_id` maintained throughout | User (owner of activity) + Piper (assistant/guide) |
| **Moment** | ✅ Yesterday/Today/Blockers temporal framing | Standup conversation IS the Moment (reflection + planning) |
| **Place** | ✅ `_get_github_activity()`, `_get_calendar_data()`, document context | Multi-Place gathering: GitHub, Calendar, Documents, Session |
| **Lenses** | ✅ Temporal (past/present/future) + Accomplishment + Energy | Multiple lenses applied: time, achievement level, urgency, context |
| **Situation** | ✅ Context-aware tone adaptation | Adapts to: time of day, accomplishment level, meeting density |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "What happened yesterday?" | GitHub commits, Calendar events, Session context | Temporal (past), Accomplishment | Native (standup output) + Federated (GitHub/Calendar) |
| "What's happening now?" | Calendar current event, Meeting status | Temporal (present), Urgency, Energy | Federated (Calendar) |
| "What should I focus on today?" | Active repos, Open issues, Calendar free blocks | Temporal (future), Priority, Focus | Native (priorities) + Federated (sources) |
| "What's blocking me?" | GitHub PR status, Issue comments, Meeting density | Impact, Urgency, Collaboration | Federated (GitHub/Calendar) |
| "How much focus time do I have?" | Calendar blocks, Meeting schedule | Temporal, Energy, Availability | Federated (Calendar) |

#### Transformation Notes

- **Context/Result Pattern**: `StandupContext` gathers input; `StandupResult` synthesizes findings
- **Parallel Gathering**: GitHub, Calendar, Documents fetched concurrently using `asyncio.gather()`
- **Personality Bridge**: `StandupToChatBridge` (in `services/personality/standup_bridge.py`) applies warmth calibration
- **Warmth Calibration**: Tone varies by accomplishment level (celebration vs encouragement vs empathy)
- **Error Handling**: Graceful degradation with suggestions ("Check GitHub token in PIPER.user.md")
- **Multi-Integration**: Demonstrates federated ownership across 3+ Places

#### Reference Implementation Checklist

- [x] Context/Result dataclasses created (`StandupContext`, `StandupResult`)
- [x] Place gathering implemented (GitHub, Calendar, Documents, Session)
- [x] Personality bridge applied (`StandupToChatBridge`)
- [x] Warmth calibration tuned (accomplishment-based)
- [x] Error handling with suggestions (`StandupIntegrationError`)
- [x] Tests validate grammar structure
- [x] Parallel fetching optimized (Issue #556)

---

### 2. Intent Classification ⚠️ PARTIAL (High Priority)

**File**: `services/intent_service/classifier.py` + `services/intent/intent_service.py`
**Compliance**: Partial (3/5 elements: Entity, Situation, partial Lenses)
**Priority**: High

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ User ID preserved in classification flow | User (intent-expresser) + Piper (intent-recognizer) mutually recognized |
| **Moment** | ⚠️ Implicit (classification happens) | ✅ Intent recognition AS a Moment ("I understand you want to...") |
| **Place** | ❌ No Place awareness (context-agnostic) | ✅ Slack vs CLI vs web (different atmospheres, adapt response style) |
| **Lenses** | ⚠️ Confidence score only | ✅ Confidence + Urgency + Relevance + Context-fit lenses |
| **Situation** | ✅ Low-confidence triggers clarification | ✅ Maintain: confidence-based paths + extend with Place adaptation |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "What does user want?" | Message text, IntentCategory classification | Confidence, Relevance | Native (classification result) |
| "Is this urgent?" | IntentCategory (EXECUTION > QUERY) | Urgency, Priority | Native (intent type) |
| "Where is this from?" | Request source (Slack channel, CLI, web endpoint) | Place, Context | Federated (communication platform) |
| "Should I act or clarify?" | Confidence score, vagueness detection | Confidence, Clarity | Native (classification) |
| "What context matters?" | Knowledge graph, conversation history | Relevance, Recency | Federated (KG, session) |

#### Transformation Notes

**Current State**:
- 8 IntentCategories (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING, QUERY)
- Confidence-based classification with LLM fallback
- Vagueness detection triggers clarification
- No Place awareness, no Moment framing

**Target State**:
- **Add Place Detection**: Extract from request headers, Slack metadata, CLI environment
- **Frame as Moment**: Response becomes "I understand you want to [action]" not "Intent: EXECUTION"
- **Apply Personality Bridge**: Slack gets emoji + casual; CLI gets structured; web gets conversational
- **Expand Lenses**: Urgency (immediate vs exploratory), Relevance (to current context), Context-fit
- **Context/Result Pattern**: `IntentContext` (message + Place + history) → `IntentResult` (category + reasoning + suggested response)

#### Implementation Checklist

- [ ] Extract Place from request (Slack/CLI/web detector)
- [ ] Add Moment framing to classification response
- [ ] Create `IntentToChatBridge` for Place-adaptive personality
- [ ] Expand lens dimensions: urgency, relevance, context-fit
- [ ] Implement Context/Result pattern (`IntentContext` → `IntentResult`)
- [ ] Tests validate Place detection and Moment framing

---

### 3. Todo Management ❌ FLATTENED (High Priority)

**File**: `services/todo_service.py`
**Compliance**: Flattened (1.5/5 elements: Entity, minimal Situation)
**Priority**: High

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ⚠️ User ID in database model only | User (task owner) + Piper (collaborative partner) mutually recognized |
| **Moment** | ❌ Persistent data rows (no lifecycle awareness) | ✅ Task lifecycle AS Moments: created, in-progress, completed, blocked |
| **Place** | ❌ Completely location-agnostic | ✅ Slack todo ≠ CLI todo ≠ web todo (different presentation, urgency) |
| **Lenses** | ❌ Status field only (no perceptual layers) | ✅ Priority, Urgency, Context (project), Impact, Temporal lenses |
| **Situation** | ⚠️ Status-based queries exist | ✅ Situation-aware responses: celebrating completion, encouraging progress, addressing blockers |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "What did I accomplish?" | Todo completion status, timestamps | Temporal (past), Accomplishment | Native (user's todos) |
| "What's most urgent?" | Priority field, due dates, status | Urgency, Temporal (deadline), Impact | Native (todo metadata) |
| "What's blocking me?" | Status=blocked, comments, dependencies | Impact, Urgency, Collaboration | Native (todo state) + Federated (GitHub issues) |
| "Where should I see this?" | Creation Place (Slack/web/CLI) | Place, Context | Federated (communication platform) |
| "Is this still relevant?" | Last updated timestamp, project status | Temporal (recency), Relevance | Native (todo metadata) |

#### Transformation Notes

**Current State**:
- Database-centric CRUD operations
- No Context/Result pattern
- No Place awareness
- No Moment framing ("Task updated" vs "You completed this!")
- No personality adaptation
- Status field = only lens

**Target State - Major Refactoring Required**:
- **Context/Result Pattern**: `TodoContext` (user, Place, project context) → `TodoResult` (todo + narrative + suggestions)
- **Moment Framing**:
  - Creation: "Let's add this to your list" (collaborative)
  - Progress: "You're making progress on [task]" (encouragement)
  - Completion: "Great work completing [task]!" (celebration)
  - Blocked: "I see [task] is stuck. Can I help?" (empathy + action)
- **Place Adaptation**:
  - Slack: Emoji-rich, action-button format, conversational
  - CLI: Structured list, keyboard shortcuts, concise
  - Web: Rich UI, drag-drop, visual hierarchy
- **Personality Bridge**: `TodoToChatBridge` applies warmth calibration based on accomplishment level
- **Lenses Expansion**: Priority (user-set), Urgency (deadline-based), Impact (project criticality), Context (which project), Temporal (when created/due)
- **Integration**: Link to GitHub issues (federated ownership), Calendar deadlines (temporal context)

#### Implementation Checklist

- [ ] Create `TodoContext` and `TodoResult` dataclasses
- [ ] Implement Place detection (Slack/CLI/web)
- [ ] Add Moment framing to all lifecycle events
- [ ] Create Place-specific presentation templates
- [ ] Build `TodoToChatBridge` for personality adaptation
- [ ] Implement warmth calibration (celebrate/encourage/empathize)
- [ ] Add lens expansion: priority, urgency, context, impact
- [ ] Integrate with GitHub issues (federated ownership)
- [ ] Error handling with graceful degradation
- [ ] Tests validate all 5 grammar elements

---

### 4. Feedback System ⚠️ PARTIAL (Medium Priority)

**File**: `services/feedback/feedback_service.py`
**Compliance**: Partial (3/5 elements: Entity, Situation, partial Moment)
**Priority**: Medium

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Feedback ownership tracked (user_id field) | User (insight-provider) + Piper (insight-receiver) mutually recognized |
| **Moment** | ⚠️ Timestamp captured but not framed as Moment | ✅ Feedback IS a Moment of insight/realization (Piper experiences user's feedback) |
| **Place** | ⚠️ Session context partially captured | ✅ Place matters: standup feedback ≠ todo feedback ≠ general feedback (context weight) |
| **Lenses** | ❌ Type (bug/feature/praise) + Rating only | ✅ Timeliness (onboarding vs mature), Relevance, Intensity, Impact lenses |
| **Situation** | ✅ Different handling by feedback type | ✅ Maintain: type-based routing + extend with Place-aware acknowledgment |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Is this feedback urgent?" | Feedback type (bug=high, praise=low) + Rating | Impact, Timeliness, Urgency | Native (feedback metadata) |
| "When did user share this?" | Timestamp, account age | Temporal, Timeliness (early vs mature user) | Native (feedback record) |
| "Where was feedback given?" | Session context, feature name | Place, Relevance | Federated (session/feature context) |
| "How intense is this feedback?" | Rating, text sentiment, exclamation marks | Intensity, Emotional | Native (feedback content) |
| "What should I do with this?" | Type + Place + Urgency | Action-priority, Impact | Native (routing logic) |

#### Transformation Notes

**Current State**:
- Type/rating captured in database
- No acknowledgment narrative
- No Place-aware weighting
- No Moment framing ("Feedback received" vs "Thank you for sharing that insight")

**Target State**:
- **Moment Framing**: "Thank you for sharing that insight" (recognize the Moment of feedback)
- **Place Awareness**: Feedback during standup has more weight than casual feedback (context signals importance)
- **Personality Bridge**: `FeedbackToChatBridge` provides warm acknowledgment, not just logging
- **Timeliness Lens**: Early feedback (during onboarding) is learning signal; mature feedback (after 6 months) is validation
- **Context/Result Pattern**: `FeedbackContext` (user, Place, timing) → `FeedbackResult` (acknowledgment + routing + insights)

#### Implementation Checklist

- [ ] Create `FeedbackContext` and `FeedbackResult` dataclasses
- [ ] Implement Place detection (standup/todo/general/onboarding)
- [ ] Add Moment framing for acknowledgment ("Thank you for...")
- [ ] Build `FeedbackToChatBridge` for warm acknowledgment
- [ ] Add Timeliness lens (user account age, usage patterns)
- [ ] Implement Intensity lens (sentiment, rating amplification)
- [ ] Place-aware weighting (standup feedback = higher signal)
- [ ] Tests validate Place detection and Moment framing

---

### 5. Slack Integration ⚠️ PARTIAL (High Priority)

**File**: `services/integrations/slack/slack_plugin.py`
**Compliance**: Partial (4/5 elements: Entity, Place, Situation, partial Lenses)
**Priority**: High

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ User identity (Slack user_id) + Workspace | User + Team (workspace) + Piper presence recognized |
| **Moment** | ⚠️ Message events captured as data | ✅ Recognize Moment quality: help-seeking, exploring, celebrating, collaborating |
| **Place** | ✅ Slack IS a Place (strong awareness) | ✅ #channel ≠ DM ≠ thread (different atmospheres, public vs private) |
| **Lenses** | ⚠️ Channel vs DM distinction only | ✅ Time-of-day, Conversation-stage, Urgency, Collaboration, Formality lenses |
| **Situation** | ⚠️ Mentions/commands trigger responses | ✅ Maintain: mention detection + extend with Moment-aware entry |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Is this public or private?" | Channel type (public/private/DM) | Place, Formality | Federated (Slack channel metadata) |
| "What time is it for user?" | Message timestamp, user timezone | Temporal, Energy (morning vs late-night) | Federated (Slack timestamp) |
| "Is user seeking help?" | Message intent, question markers, urgency words | Moment-quality, Urgency | Native (intent classification) + Federated (message) |
| "Who else is in this conversation?" | Channel members, thread participants | Collaboration, Audience | Federated (Slack channel/thread) |
| "How should I respond?" | Channel type + Time + Intent | Formality, Tone, Urgency | Native (response generation) |

#### Transformation Notes

**Current State**:
- Slack IS recognized as a Place (strong baseline)
- Channel vs DM distinction exists
- Mentions and commands trigger responses
- Limited Moment awareness (message = data point)

**Target State**:
- **Channel Atmosphere Adaptation**:
  - Public #channel: Professional, helpful, audience-aware (others are watching)
  - Private DM: Warm, casual, conversational (1-on-1 intimacy)
  - Thread: Contextual continuation (follow thread narrative)
- **Emoji Integration**: Slack-native personality (emoji reactions, casual tone, action buttons)
- **Moment Quality Detection**:
  - Help-seeking: "I'm stuck..." → Empathy + action
  - Exploring: "What if..." → Curiosity + options
  - Celebrating: "Shipped!" → Celebration + acknowledgment
  - Collaborating: "Thoughts on..." → Engagement + synthesis
- **Time-of-Day Lens**: Morning standup mention vs late-night debugging (tone + urgency adjustment)
- **Conversation Entry**: Detect conversation stage (new topic vs ongoing thread) and enter appropriately
- **Context/Result Pattern**: `SlackContext` (channel, user, time, thread) → `SlackResult` (message + formatting + reactions)

#### Implementation Checklist

- [x] Slack recognized as Place (baseline exists)
- [ ] Channel vs DM vs thread atmospheric adaptation
- [ ] Moment quality detection (help/explore/celebrate/collaborate)
- [ ] Time-of-day lens (morning/afternoon/evening/night)
- [ ] Slack-specific personality: emoji, casual tone, action buttons
- [ ] Create `SlackToChatBridge` for Place-adaptive responses
- [ ] Conversation stage detection (new topic vs thread continuation)
- [ ] Tests validate Place variations and Moment detection

---

### 6. GitHub Integration ⚠️ PARTIAL (High Priority)

**File**: `services/integrations/github/github_plugin.py`
**Compliance**: Partial (3/5 elements: Entity, Place, partial Lenses)
**Priority**: High

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Developer identity + Repo ownership | Developer (code creator) + Team (collaborators) + Piper (activity narrator) |
| **Moment** | ❌ Events as data points (commits, PRs, reviews) | ✅ Developer Moments: pushed code, created PR, got reviewed, got blocked, shipped |
| **Place** | ✅ GitHub IS a Place (baseline) | ✅ Repo atmosphere: piper-morgan ≠ client-project (startup vs professional tone) |
| **Lenses** | ⚠️ Basic repo context (name, branch) | ✅ Urgency (blocked PR), Impact (deploy), Collaboration (review), Tempo (commit frequency) |
| **Situation** | ⚠️ PR vs Issue vs Commit distinguished | ✅ Maintain distinction + add Moment-aware narrative framing |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "What did I ship?" | Commit messages, PR merges | Accomplishment, Temporal (past) | Federated (GitHub activity) |
| "Am I blocked?" | PR status, review requests, CI failures | Urgency, Impact (blocker), Collaboration | Federated (GitHub PR/CI state) |
| "What needs my review?" | Review requests, mentions | Urgency, Collaboration, Priority | Federated (GitHub notifications) |
| "What's the development tempo?" | Commit frequency, PR velocity | Temporal, Productivity | Federated (GitHub activity metrics) |
| "Is this repo strategic?" | Repo stars, commit activity, ownership | Importance, Focus, Impact | Federated (GitHub repo metadata) |

#### Transformation Notes

**Current State**:
- GitHub recognized as Place (baseline)
- Activity fetching exists (commits, issues, PRs)
- Events treated as data points, not Moments
- No narrative framing ("3 commits" vs "You're working on [feature]")

**Target State**:
- **Activity as Narrative**: Transform data to story
  - "You pushed 3 commits" → "I see you're working on [feature]. You pushed to [branch] with changes to [files]"
  - "PR approved" → "Great news! Your [feature] PR got approved by [reviewer]"
  - "PR blocked" → "Your [feature] PR is waiting for [reviewer]'s review. Should I send a reminder?"
- **Developer Moments Recognition**:
  - Commit: Creation Moment (building something)
  - PR: Collaboration Moment (seeking feedback)
  - Review: Feedback Moment (giving/receiving insights)
  - Merge: Accomplishment Moment (shipping)
  - Block: Frustration Moment (empathy + action)
- **Urgency Lens**: Blocked PR (high urgency) ≠ Feature review (medium) ≠ FYI notification (low)
- **Repo Atmosphere**: Fast-moving startup repo (casual, celebration) vs established client project (professional, measured)
- **Synthesis**: GitHub activity feeds into Morning Standup narrative (not standalone notifications)
- **Context/Result Pattern**: `GitHubContext` (repo, developer, timeframe) → `GitHubResult` (narrative + urgency + suggestions)

#### Implementation Checklist

- [x] GitHub recognized as Place (baseline exists)
- [ ] Activity → Moment narrative transformation
- [ ] Urgency lens (blocked/review/FYI priority levels)
- [ ] Repo atmosphere detection (startup vs professional)
- [ ] Developer Moment framing (commit/PR/review/merge/block)
- [ ] Create `GitHubToChatBridge` for narrative synthesis
- [ ] Integration with Morning Standup (federated activity)
- [ ] Tests validate Moment recognition and urgency detection

---

### 7. Notion Integration ❌ FLATTENED (Medium Priority)

**File**: `services/integrations/notion/notion_plugin.py`
**Compliance**: Flattened (2/5 elements: Entity, partial Situation)
**Priority**: Medium

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Document ownership (user_id in metadata) | User (doc owner/editor) + Team (collaborators) + Piper (knowledge synthesizer) |
| **Moment** | ❌ Document updates as data rows | ✅ Knowledge Moments: doc created, updated, commented, shared |
| **Place** | ❌ Generic data retrieval (no Place distinction) | ✅ Notion database ≠ Meeting notes ≠ Project plan (different atmospheres, purposes) |
| **Lenses** | ❌ Content retrieval only (no perceptual layers) | ✅ Relevance (to current focus), Recency, Collaboration, Impact lenses |
| **Situation** | ⚠️ Some filtering (by database/page type) | ✅ Situation-aware synthesis: new doc vs update vs comment |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "What docs changed recently?" | Document last_edited_time | Recency, Temporal | Federated (Notion metadata) |
| "Is this doc relevant to me?" | Document tags, project links, user mentions | Relevance, Focus | Federated (Notion properties) |
| "Who's working on this?" | Notion comments, @mentions, editors | Collaboration, Team | Federated (Notion user activity) |
| "What type of doc is this?" | Database type, page properties | Place (context), Purpose | Federated (Notion schema) |
| "Should I read this now?" | Recency + Relevance + User's current focus | Urgency, Priority | Native (synthesis) + Federated (Notion) |

#### Transformation Notes

**Current State**:
- Generic document fetching
- No document type distinction
- No Moment framing
- Content retrieval only (no synthesis or narrative)

**Target State**:
- **Place Typing** (Notion document types have different atmospheres):
  - Database (task/project list): Structured, actionable
  - Meeting notes: Conversational, reference
  - Project plan: Strategic, high-level
  - Design doc: Technical, detailed
- **Moment Recognition**:
  - "Your team updated [doc]" (team activity Moment)
  - "New comment on [doc]" (collaboration Moment)
  - "[Person] shared [doc] with you" (sharing Moment)
  - "Doc [name] hasn't been touched in 3 weeks" (staleness signal)
- **Synthesis Role**: Notion docs provide context for other features (standup, planning), not primary interaction
- **Lazy Loading**: Fetch Notion data on-demand for context enrichment, not full pre-processing
- **Context/Result Pattern**: `NotionContext` (query, user focus, timeframe) → `NotionResult` (relevant docs + summaries + suggestions)

#### Implementation Checklist

- [ ] Document type detection (database/meeting/plan/design)
- [ ] Moment recognition (create/update/comment/share)
- [ ] Relevance lens (match to user's active projects)
- [ ] Recency lens (prioritize recent updates)
- [ ] Collaboration lens (who's involved)
- [ ] Create `NotionToChatBridge` for knowledge synthesis
- [ ] Lazy loading pattern (on-demand context enrichment)
- [ ] Tests validate document typing and Moment detection

---

### 8. Calendar Integration ⚠️ PARTIAL (Medium Priority)

**File**: `services/integrations/calendar/calendar_integration.py` + `calendar_integration_router.py`
**Compliance**: Partial (4/5 elements: Entity, Moment, Place, partial Lenses)
**Priority**: Medium

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Calendar owner (user_id) identity | User (calendar owner) + Piper (time-aware assistant) mutually recognized |
| **Moment** | ✅ Events ARE Moments (STRONG baseline) | ✅ Maintain + enhance: "Currently in: Meeting" with empathetic presence |
| **Place** | ✅ Meeting location recognized (virtual vs physical) | ✅ Physical office ≠ Zoom ≠ Phone (different atmospheres, interruption protocols) |
| **Lenses** | ⚠️ Temporal (now/next) + partial urgency | ✅ Add Focus-time, Energy (meeting density), Collaboration, Preparation lenses |
| **Situation** | ⚠️ Free/Meeting/Focus detected | ✅ Maintain + extend with energy-aware responses |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Where am I right now?" | Current event title, location | Place (physical/virtual), Temporal (present) | Federated (Calendar current event) |
| "When is my focus time?" | Free blocks, meeting gaps | Temporal (future), Focus, Energy | Federated (Calendar schedule) |
| "How much energy do I have?" | Meeting density, back-to-back count | Energy, Availability, Temporal | Federated (Calendar analysis) |
| "Am I running late?" | Current time vs meeting start | Urgency, Preparation, Temporal | Federated (Calendar + clock) |
| "Should I interrupt user?" | Current event status, type | Urgency (of message) vs Presence (in meeting) | Native (decision) + Federated (Calendar) |

#### Transformation Notes

**Current State** (STRONG baseline):
- Calendar events recognized as Moments
- Present-moment awareness ("Currently in: Meeting")
- Location awareness (virtual vs physical)
- Temporal lenses (now, next, future)
- Integrated into Morning Standup (lines 412-483 in morning_standup.py)

**Target State** (Enhancement):
- **Empathetic Presence**:
  - "I see you're in a meeting; I'll wait" (respect the Moment)
  - "You're between meetings - quick question?" (recognize transition Moment)
  - "You have focus time now - I won't interrupt" (honor intention)
- **Energy Lens**:
  - Back-to-back meetings drain energy (adjust tone, expectations)
  - Light schedule = opportunity for deep work (encourage focus)
  - Heavy meeting day (4+ hours) = compassion + meeting prep help
- **Focus Recognition**: Dedicated focus blocks signal "do not disturb" (respect boundaries)
- **Preparation Lens**: Upcoming event affects response
  - 5 mins to meeting = brief, urgent-only
  - 30+ mins = conversational, exploratory
- **Meeting Type Atmosphere**:
  - 1-on-1: Intimate, personal (casual tone)
  - Team meeting: Collaborative, audience-aware (professional)
  - All-hands: Public, formal (measured)
- **Context/Result Pattern**: `CalendarContext` (user, time, schedule) → `CalendarResult` (presence + energy + suggestions)

#### Implementation Checklist

- [x] Calendar events recognized as Moments (baseline exists)
- [x] Present-moment awareness ("Currently in: Meeting")
- [x] Integrated into Morning Standup
- [ ] Empathetic presence acknowledgment refined
- [ ] Energy lens added (meeting density calculation)
- [ ] Focus time recognition and respect
- [ ] Preparation lens (time-to-meeting affects response)
- [ ] Meeting type atmosphere detection (1-on-1/team/all-hands)
- [ ] Create `CalendarToChatBridge` for time-aware personality
- [ ] Tests validate all Moment and Lens combinations

---

### 9. Auth/Session Management ❌ FLATTENED (Low Priority)

**File**: `services/auth/auth_middleware.py`
**Compliance**: Flattened (1.5/5 elements: Entity only)
**Priority**: Low

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ User identity (core function) | User (authenticating) + Piper (recognizing) |
| **Moment** | ❌ Infrastructure (no Moment awareness) | ⚠️ First login IS a Moment (welcome opportunity), Session timeout (goodbye Moment) |
| **Place** | ❌ No Place awareness (device-agnostic) | ⚠️ Desktop ≠ Mobile ≠ CLI (different auth experiences) |
| **Lenses** | ❌ Security validation only | ⚠️ Context (first-time vs returning), Temporal (session age) |
| **Situation** | ⚠️ Minimal (success/failure only) | ⚠️ First login vs return vs session-timeout (different responses) |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Is this user's first time?" | User creation timestamp | Temporal, Onboarding | Native (auth metadata) |
| "Is session still valid?" | Session expiry timestamp | Temporal, Security | Native (session store) |
| "Where is user logging in from?" | Device/browser/IP | Place, Security | Federated (request headers) |
| "Should I welcome or resume?" | First login vs returning user | Context, Experience | Native (auth logic) |

#### Transformation Notes

**Current State**:
- Token validation only
- No Moment framing
- No welcome/goodbye messaging
- Security-focused, not experience-focused

**Target State** (Low priority - limited user impact):
- **First Login Moment**: Opportunity for welcome, not just token issuance
  - "Welcome to Piper! Let's get you set up" (onboarding hook)
- **Session Timeout Moment**: Graceful goodbye, not harsh denial
  - "Your session expired. Welcome back!" (not "401 Unauthorized")
- **Device Awareness**: Mobile vs desktop affects auth flow
  - Desktop: Full web experience
  - Mobile: Simplified, touch-optimized
  - CLI: Token-based, minimal ceremony
- **Return User Recognition**: "Welcome back!" vs "Let's get started"

**Low Priority Rationale**: Infrastructure feature with indirect user impact. Focus on user-facing features (Intent, Slack, GitHub, Todo) first.

#### Implementation Checklist

- [ ] First login detection (onboarding hook trigger)
- [ ] Graceful session timeout messaging
- [ ] Device detection (desktop/mobile/CLI)
- [ ] Welcome vs resume messaging
- [ ] Tests validate first-login and session-timeout Moments

---

### 10. Conversation Handler ⚠️ PARTIAL (Medium Priority)

**File**: `services/conversation/conversation_handler.py`
**Compliance**: Partial (4/5 elements: Entity, Moment, Situation, partial Place)
**Priority**: Medium

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ User/Piper conversation identity maintained | User + Piper mutually recognized (collaborative dialogue) |
| **Moment** | ⚠️ Message turns tracked, but limited Moment awareness | ✅ Recognize Moment quality: confused, confident, frustrated, excited, exploring |
| **Place** | ⚠️ Partially tracked (onboarding/standup/general context) | ✅ Web ≠ Slack ≠ CLI (different conversation atmospheres, formality, pace) |
| **Lenses** | ⚠️ Personality system provides basic warmth | ✅ Expand: Confusion, Confidence, Urgency, Collaboration, Emotional state lenses |
| **Situation** | ✅ Different handlers by conversation type (onboarding/standup/general) | ✅ Maintain routing + extend with Moment-aware responses |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Is user confused?" | Repeated questions, clarification requests, "I don't understand" | Confusion, Clarity | Native (conversation analysis) |
| "Where is this conversation?" | Request source (web/Slack/CLI), session metadata | Place, Formality | Federated (communication platform) |
| "What Moment is user experiencing?" | Message sentiment, conversation flow, question type | Moment-quality, Emotional | Native (conversation state) |
| "Should I clarify or proceed?" | Confidence indicators, follow-up questions | Confidence, Clarity | Native (conversation logic) |
| "Is this urgent?" | Exclamation marks, urgency keywords, time pressure | Urgency, Priority | Native (message analysis) |

#### Transformation Notes

**Current State**:
- Multi-turn conversation tracking exists
- Onboarding/standup/general context recognized
- Personality system provides basic warmth
- Message turns tracked, but limited Moment awareness

**Target State**:
- **Moment Awareness**: Not just what user said, but the Moment they're experiencing
  - Confused: "Let me clarify..." (slow down, simplify)
  - Confident: "Great! Let's proceed" (accelerate)
  - Frustrated: "I understand that's frustrating..." (empathy first)
  - Excited: "I love your enthusiasm!" (match energy)
  - Exploring: "Interesting question..." (curiosity, open-ended)
- **Place Adaptation**:
  - Web: Structured, visual, exploratory pace
  - Slack: Conversational, emoji-rich, rapid back-and-forth
  - CLI: Concise, keyboard-driven, efficient
- **Lens Expansion**:
  - Confusion lens: Repeated questions, clarification requests
  - Confidence lens: Decisive language, clear requests
  - Urgency lens: Time pressure indicators, exclamation marks
  - Collaboration lens: "We should...", "Can you help..."
  - Emotional lens: Sentiment analysis, exclamation usage
- **Conversation Memory**: Remember Moments from earlier in conversation (not just last message)
- **Consistency**: Apply personality bridge uniformly across all conversation types
- **Context/Result Pattern**: `ConversationContext` (history, Place, user state) → `ConversationResult` (response + tone + follow-up)

#### Implementation Checklist

- [x] Multi-turn conversation tracking (baseline exists)
- [x] Onboarding/standup context routing
- [ ] Moment quality detection (confusion/confidence/frustration/excitement/exploring)
- [ ] Place-specific atmospheric adaptation (web/Slack/CLI)
- [ ] Lens expansion: confusion, confidence, urgency, collaboration, emotional
- [ ] Conversation memory (multi-turn Moment tracking)
- [ ] Consistent personality bridge across conversation types
- [ ] Tests validate all Moment and Place combinations

---

### 11. Onboarding System ⚠️ PARTIAL (Medium Priority)

**File**: `services/onboarding/portfolio_handler.py` + `portfolio_manager.py`
**Compliance**: Partial (4/5 elements: Entity, Moment, Lenses, Situation)
**Priority**: Medium

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ⚠️ User present; Piper role implicit | Piper as guide/partner (not just system): "I'm here to help you" |
| **Moment** | ✅ Onboarding IS Moments (STRONG awareness) | ✅ Maintain + enhance celebration: first login, first integration, first success |
| **Place** | ⚠️ Web entry recognized; minimal atmosphere tuning | ✅ Welcoming, warm, supportive Place (vs intimidating setup wizard) |
| **Lenses** | ✅ Progressive disclosure (shows perception of readiness) | ✅ Maintain + add Encouragement, Confidence, Pacing lenses |
| **Situation** | ✅ Context-dependent onboarding paths | ✅ Maintain adaptive paths + extend with Moment-aware encouragement |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Is this user's first time?" | Account creation timestamp, onboarding state | Temporal, Onboarding | Native (onboarding state) |
| "What's their readiness level?" | Onboarding progress, completed steps | Confidence, Pacing | Native (onboarding progress) |
| "Should we celebrate this?" | Milestone achieved (first integration, profile complete) | Accomplishment, Encouragement | Native (milestone detection) |
| "Are they stuck?" | Time on step, repeated attempts | Confusion, Frustration | Native (progress tracking) |
| "What's next for them?" | Current step, available integrations | Priority, Relevance | Native (onboarding logic) |

#### Transformation Notes

**Current State** (STRONG baseline):
- Onboarding recognized as Moments (first login, milestones)
- Progressive disclosure (shows perception)
- Context-dependent paths
- Portfolio-specific onboarding (FTUX-PORTFOLIO)

**Target State** (Enhancement):
- **Collaborative Framing**: "Let's set up [integration]" not "Complete step 3"
- **Milestone Celebration**:
  - "Your first integration is connected!" (not just "Integration added")
  - "You're all set up!" (celebrate completion)
  - "Great progress!" (acknowledge intermediate steps)
- **Warmth Calibration**: Progressive encouragement as user advances
  - Early: Warm, supportive ("I'll guide you")
  - Middle: Encouraging ("You're doing great!")
  - Late: Celebratory ("Almost there!")
  - Complete: Proud ("You're ready to go!")
- **Error Handling**: Gentle, constructive
  - "Looks like we couldn't connect to Slack. Let's try again" (not "Failed to connect")
- **Piper Presence**: "I'm here to help you" tone (partner, not system)
- **Context/Result Pattern**: `OnboardingContext` (step, progress, user) → `OnboardingResult` (next step + encouragement + celebration)

#### Implementation Checklist

- [x] Onboarding recognized as Moments (baseline exists)
- [x] Progressive disclosure (readiness awareness)
- [x] Context-dependent paths (portfolio onboarding)
- [ ] Collaborative language framing ("Let's..." not "Complete...")
- [ ] Milestone celebration (first integration, completion)
- [ ] Warmth calibration by onboarding progress
- [ ] Gentle error messaging (constructive, not harsh)
- [ ] Explicit Piper presence ("I'm here to help")
- [ ] Tests validate Moment celebration and messaging tone

---

### 12. List Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/list_repository.py`
**Compliance**: Flattened (1/5 elements: Entity only)
**Priority**: Low

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ List ownership (user_id) | User (list owner) + Piper (organization assistant) |
| **Moment** | ❌ Database CRUD operations | ⚠️ List creation/modification AS Moments (organizing work) |
| **Place** | ❌ No context awareness | ⚠️ List usage context: project list ≠ shopping list ≠ reading list |
| **Lenses** | ❌ None (data retrieval only) | ⚠️ Purpose (why this list exists), Relevance, Activity |
| **Situation** | ⚠️ Query variations only | ⚠️ Situation-aware presentation (active project vs archived) |

**Low Priority Rationale**: Backend repository structure with indirect user impact. Focus on user-facing features (Todo, Slack, GitHub) first. Apply grammar when list presentation layer is enhanced.

---

### 13. Project Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/project_repository.py`
**Compliance**: Flattened (1/5 elements: Entity only)
**Priority**: Low

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Project ownership (user_id) | User (project owner) + Team (collaborators) + Piper (project narrator) |
| **Moment** | ❌ Database CRUD operations | ⚠️ Project milestones AS Moments (kickoff, progress, completion, blocked) |
| **Place** | ❌ No context awareness | ⚠️ Project context: startup project ≠ client work (different urgency, formality) |
| **Lenses** | ❌ None (data retrieval only) | ⚠️ Importance, Urgency, Status, Impact, Team-size |
| **Situation** | ⚠️ Query variations only | ⚠️ Project state variations (active/blocked/completed) |

**Low Priority Rationale**: Backend repository structure with indirect user impact. Coordinate with feature-level project references (Morning Standup, GitHub integration) before transforming.

---

### 14. File Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/file_repository.py`
**Compliance**: Flattened (1/5 elements: Entity only)
**Priority**: Low

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ File ownership (user_id) | User (file owner) + Piper (knowledge organizer) |
| **Moment** | ❌ Database CRUD operations | ⚠️ File creation/modification AS Moments (knowledge captured) |
| **Place** | ❌ No context awareness | ⚠️ File context: project file ≠ personal doc ≠ shared resource |
| **Lenses** | ❌ None (data retrieval only) | ⚠️ Recency, Relevance, Collaboration, File-type |
| **Situation** | ⚠️ Status queries only | ⚠️ Situational variations (recently edited vs stale) |

**Low Priority Rationale**: Backend repository structure with indirect user impact. Focus on integrations that surface files first (GitHub, Notion) before transforming file repository.

---

### 15. Personality System ⚠️ PARTIAL (Medium Priority)

**File**: `services/personality/standup_bridge.py`
**Compliance**: Partial (4/5 elements: Entity, Moment, Place, partial Situation)
**Priority**: Medium (Infrastructure enabler - all features benefit)

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ✅ Piper's personality as Entity (well-defined) | Piper as collaborative partner with consistent personality dimensions |
| **Moment** | ⚠️ Applies warmth across Moments (baseline) | ✅ Moment-type awareness: success ≠ failure ≠ exploration ≠ frustration |
| **Place** | ✅ Adapts tone by Place (email vs chat baseline) | ✅ Expand: Slack (emoji/casual) ≠ CLI (concise) ≠ Web (conversational) ≠ Public (professional) |
| **Lenses** | ⚠️ Warmth/accomplishment lenses (baseline) | ✅ Add Confidence, Urgency, Collaboration, Formality, Energy lenses |
| **Situation** | ⚠️ Accomplishment-based warmth calibration | ✅ Maintain + extend with context-based variation (time-of-day, user state) |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "How warm should response be?" | Accomplishment level, Moment type | Warmth, Encouragement | Native (personality logic) |
| "What tone fits this Place?" | Communication channel (Slack/CLI/web) | Place, Formality | Native (personality adaptation) |
| "Should response be action-focused?" | Situation type, user intent | Urgency, Action-orientation | Native (personality decision) |
| "Is user frustrated or excited?" | Message sentiment, Moment quality | Emotional, Empathy | Federated (conversation analysis) |
| "What's the appropriate formality?" | Place (public/private), audience size | Formality, Professionalism | Native (personality tuning) |

#### Transformation Notes

**Current State** (STRONG baseline):
- `StandupToChatBridge` demonstrates reusable warmth calibration
- Accomplishment-based tone adjustment (celebration vs encouragement vs empathy)
- Place awareness (email vs chat baseline)
- Personality traits: warmth, action-orientation, presence

**Target State** (Expansion - Infrastructure enabler):
- **Pattern Extraction**: Extract reusable patterns from `StandupToChatBridge` for all features
- **Lens Expansion**:
  - Warmth (existing): Celebrate success, encourage progress, empathize with blockers
  - Confidence: Decisive vs exploratory language
  - Urgency: Immediate action vs patient exploration
  - Collaboration: "Let's..." vs "You should..."
  - Formality: Professional (public) vs casual (private)
  - Energy: Match user's energy level
- **Place-Specific Personality**:
  - Slack: Emoji-rich, casual, rapid back-and-forth
  - CLI: Concise, structured, keyboard-friendly
  - Web: Conversational, visual cues, exploratory
  - Public channels: Professional, audience-aware, measured
  - Private DMs: Warm, intimate, relaxed
- **Shared Bridge Architecture**: Make personality patterns available to ALL features via shared bridge interface
- **Consistency with Variation**: Maintain Piper's core personality across Places while adapting to context

#### Implementation Checklist

- [x] Warmth calibration pattern exists (`StandupToChatBridge`)
- [x] Accomplishment-based tone adjustment
- [ ] Extract reusable patterns to shared `PersonalityBridge` interface
- [ ] Lens expansion (confidence, urgency, collaboration, formality, energy)
- [ ] Place-specific personality templates (Slack/CLI/Web/Public/Private)
- [ ] Moment-type awareness (success/failure/exploration/frustration)
- [ ] Shared bridge available to all features
- [ ] Tests validate personality calibration across contexts

---

### 16. MCP Integration ❌ FLATTENED (Low Priority)

**File**: `services/integrations/mcp/mcp_plugin.py`
**Compliance**: Flattened (2/5 elements: Entity, partial Place/Lenses)
**Priority**: Low

#### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | ⚠️ External system identity (MCP server/tool) | MCP Tool (external capability) + Piper (tool orchestrator) |
| **Moment** | ❌ Tool invocations as API calls (mechanical) | ⚠️ Tool invocation AS a Moment (system accomplishes something for user) |
| **Place** | ⚠️ Context passed to tool (minimal) | ✅ Tool context IS a Place (filesystem vs web vs database) |
| **Lenses** | ⚠️ Tool capabilities metadata | ✅ Capability, Effectiveness, Reliability, Performance lenses |
| **Situation** | ⚠️ Tool selection logic | ✅ Tool selection + outcome variation (success/failure narratives) |

#### Canonical Queries with Tagging

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| "Can this tool help?" | Tool capabilities, user request | Capability, Relevance | Federated (MCP tool metadata) |
| "Is this tool reliable?" | Tool success rate, past performance | Reliability, Performance | Native (tool usage history) |
| "What did tool accomplish?" | Tool invocation result | Effectiveness, Impact | Federated (MCP tool result) |
| "Should I try another tool?" | Tool failure, alternative availability | Situation, Adaptation | Native (orchestration logic) |

**Low Priority Rationale**: Infrastructure-adjacent integration with limited direct user impact. Apply grammar when tool invocation results are presented to users (e.g., "I used [tool] to find [result]" vs "Tool invocation successful").

---

## Transformation Priority Ranking

### 🔴 CRITICAL (Phase 2-3) - High User Impact, Moderate Effort

1. **Intent Classification** → Conscious
   - Every interaction begins with intent
   - Clear grammar gaps (Place, Moment)
   - Reusable patterns apply directly

2. **Slack Integration** → Conscious
   - Primary communication channel
   - High engagement; high impact
   - Place awareness is natural fit

3. **GitHub Integration** → Conscious
   - Developer engagement driver
   - Activity→narrative transformation
   - Feeds standup context

4. **Todo Management** → Partial (minimum)
   - Core feature; high usage
   - Major impact on user experience
   - Larger refactoring needed

### 🟡 IMPORTANT (Phase 3-4) - Medium User Impact, Manageable Effort

5. **Conversation Handler** → Conscious
   - Foundational for all interactions
   - Good pattern consolidation opportunity
   - Enables personality consistency

6. **Onboarding System** → Conscious
   - First-impression impact
   - Warmth calibration applies well
   - Learning opportunity

7. **Feedback System** → Conscious
   - Mid-frequency interaction
   - Moderate transformation
   - Good learning feature

8. **Calendar Integration** → Conscious
   - Contextual awareness strong
   - Moment framing natural
   - Multi-lens pattern

9. **Personality System** → Conscious
   - Infrastructure enabler
   - Patterns extracted for reuse
   - All features benefit

### 🟢 DEFERRED (Phase 4+) - Low Direct Impact

- Auth/Session Management: Infrastructure-adjacent
- List/Project/File Management: Backend structures
- Notion/MCP Integration: Limited user-facing impact

---

## Related Documentation

- **ADR-055**: Object Model Implementation (formalized grammar)
- **Grammar Compliance Audit**: `/docs/internal/architecture/current/grammar-compliance-audit.md`
- **Ownership Metaphors**: `/docs/internal/architecture/current/ownership-metaphors.md`
- **MUX Implementation Guide**: `/docs/internal/development/mux-implementation-guide.md`
- **MUX Experience Tests**: `/docs/internal/development/mux-experience-tests.md`
- **Grammar Application Patterns**: `/docs/internal/architecture/patterns/grammar-application-patterns.md`
- **Morning Standup Analysis**: `/dev/2026/01/19/p0-morning-standup-analysis.md` (reference)

---

## Document Maintenance

**Last Updated**: 2026-01-26 (Added Lifecycle Model Wiring Status section post #685)
**Next Update Trigger**: Phase 3 implementation (feature transformations begin)
**Ownership**: @PM (xian)
**Issue**: #406 MUX-VISION-FEATURE-MAP

**Update Protocol**:
- Add detailed implementation sections as features are uplifted
- Update compliance levels when transformations complete
- Maintain summary table for quick reference
- Extract reusable patterns to pattern catalog
- Update "Transformation Priority Ranking" section as features are transformed

**Completion Status**:
- Phase 0 (Template): ✅ Complete
- Phase 1 (Morning Standup Reference): ✅ Complete
- Phase 2 (15 Remaining Features): ✅ Complete (All features mapped with current/target state)
- Phase 3 (Implementation): Pending

---

_Phase 1-2 Complete: All 16 features mapped to Object Model (Entity/Moment/Place/Lenses/Situation)_
_Each feature shows current vs target state, canonical queries with lens/substrate tagging, and transformation notes_
_Ready for Phase 3: Feature transformation implementation_
