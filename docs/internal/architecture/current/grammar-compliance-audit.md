# Grammar Compliance Audit

**Date**: 2026-01-20
**Auditor**: Claude Code (Haiku)
**Issue**: #404 MUX-VISION-GRAMMAR-CORE
**Phase**: 1 (Feature Grammar Audit)

---

## Executive Summary

This audit surveys 16 major Piper Morgan features and systems to assess their compliance with the Entity/Moment/Place/Lenses/Situation grammar model (formalized in ADR-055 and MUX infrastructure).

**Key Finding**: Grammar compliance varies widely across the system. Morning Standup demonstrates full consciousness, while most features exhibit flattened or partial compliance. This creates an opportunity to systematically uplift features through a prioritized transformation roadmap.

**Compliance Distribution**:
- **Conscious** (fully compliant): 1 feature
- **Partial** (some elements present): 6 features
- **Flattened** (mechanical/database language): 9 features

---

## Audit Methodology

For each feature, we evaluate five grammar elements:

| Element | Definition | Pass Criteria |
|---------|-----------|---------------|
| **Entity** | Actors (user, Piper, integrations) tracked with identity persistence | User/Piper identity preserved throughout flow; self-reference preserved |
| **Moment** | Discrete occurrences framed as scenes, not timestamps | More than temporal markers; narrative/experiential language present |
| **Place** | Context and atmosphere acknowledged; not just config strings | Integration/location-specific behavior; "where" affects "how" |
| **Lenses** | Perceptual dimensions applied (8D spatial, temporal, relational) | At least one lens applicable; multiple lenses preferred |
| **Situation** | Dramatic tension or context beyond raw data | Conditional behavior based on state; appropriate responses to circumstances |

**Compliance Levels**:
- **Conscious** ✅: All 5 elements present; grammar flows naturally
- **Partial** ⚠️: 3-4 elements present; some flattening present
- **Flattened** ❌: 0-2 elements; mechanical/database language dominant

---

## Feature Compliance Matrix

| Feature | Entity | Moment | Place | Lenses | Situation | Overall | Priority |
|---------|--------|--------|-------|--------|-----------|---------|----------|
| **Morning Standup** | ✅ | ✅ | ✅ | ✅ | ✅ | **Conscious** | Reference |
| **Intent Classification** | ✅ | ⚠️ | ❌ | ⚠️ | ✅ | **Partial** | High |
| **Todo Management** | ⚠️ | ❌ | ❌ | ❌ | ✅ | **Flattened** | High |
| **Feedback System** | ✅ | ⚠️ | ⚠️ | ❌ | ✅ | **Partial** | Medium |
| **Slack Integration** | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | **Partial** | High |
| **GitHub Integration** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | **Partial** | High |
| **Notion Integration** | ✅ | ❌ | ❌ | ❌ | ⚠️ | **Flattened** | Medium |
| **Calendar Integration** | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | **Partial** | Medium |
| **Auth/Session Management** | ✅ | ❌ | ❌ | ❌ | ⚠️ | **Flattened** | Low |
| **Conversation Handler** | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ | **Partial** | Medium |
| **Onboarding System** | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | **Partial** | Medium |
| **List Management** | ⚠️ | ❌ | ❌ | ❌ | ✅ | **Flattened** | Low |
| **Project Management** | ⚠️ | ❌ | ❌ | ❌ | ✅ | **Flattened** | Low |
| **File Management** | ⚠️ | ❌ | ❌ | ❌ | ✅ | **Flattened** | Low |
| **Personality System** | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | **Partial** | Medium |
| **MCP Integration** | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | **Flattened** | Low |

---

## Detailed Feature Analysis

### 1. Morning Standup ✅ CONSCIOUS (Reference Implementation)

**File**: `services/features/morning_standup.py`

**Grammar Assessment**:
- ✅ **Entity**: `StandupContext.user_id` and workflow identity maintained throughout
- ✅ **Moment**: Yesterday/Today/Blockers categorization; present moment awareness ("Currently in: Meeting")
- ✅ **Place**: `_get_github_activity()`, `generate_with_calendar()`, `generate_with_documents()` show Place-aware gathering
- ✅ **Lenses**: Temporal perception (past/present/future); emotional intelligence (accomplishment levels)
- ✅ **Situation**: Contextual encouragement; morning vs evening tone adaptation; intelligent failure handling

**Evidence**: See `dev/2026/01/19/p0-morning-standup-analysis.md` for detailed analysis.

**Key Patterns to Extract**:
1. Context/Result dataclass pair
2. Parallel place gathering with synthesis
3. Personality bridge for data transformation
4. Warmth calibration
5. Honest failure with suggestions

**Recommendation**: This is the reference architecture. Use as template for other features.

---

### 2. Intent Classification ⚠️ PARTIAL (High Priority)

**File**: `services/intent_service/classifier.py`

**Grammar Assessment**:
- ✅ **Entity**: User ID preserved; category/action mapped to user's context
- ⚠️ **Moment**: Intent recognized, but treated as data classification not experiential recognition
- ❌ **Place**: No Place awareness; intent classification is context-agnostic
- ⚠️ **Lenses**: Classification confidence provides perception, but limited dimensionality
- ✅ **Situation**: Different responses for low-confidence vs high-confidence intents

**Current Language**: Mechanical/database-like
```python
intent = Intent(
    category=IntentCategory.EXECUTION,
    action="complete_todo",
    confidence=0.95
)
```

**Grammar Deficits**:
- No Place attribute (where is this intent being expressed?)
- No Moment framing (what temporal context triggers this?)
- Response is data, not experience

**Transformation Potential**: HIGH
- Could add Place awareness (Slack vs CLI vs web detection)
- Could frame intent as Moment of understanding (user's intent is a moment Piper experiences)
- Response bridge could add warmth/encouragement

---

### 3. Todo Management ❌ FLATTENED (High Priority)

**File**: `services/todo/todo_service.py`

**Grammar Assessment**:
- ⚠️ **Entity**: User ID present but minimal self-reference
- ❌ **Moment**: Treated as persistent data, not scenes/occurrences
- ❌ **Place**: No Place awareness; todos are location-agnostic
- ❌ **Lenses**: Basic status tracking only; no perceptual dimensions
- ✅ **Situation**: Status-based behavior (open vs completed vs archived)

**Current Language**: Pure database
```python
async def create_todo(
    self,
    title: str,
    user_id: str,
    status: TodoStatus = TodoStatus.OPEN,
    priority: TodoPriority = TodoPriority.MEDIUM
) -> Todo:
```

**Grammar Deficits**:
- No connection to Experience or Moment
- No Place-specific behavior (Slack todo vs web todo feels same)
- No Piper personality or encouragement

**Transformation Potential**: HIGH
- Add Moment framing to todo lifecycle (creation moment, completion moment, blocker moment)
- Add Place-aware presentation (Slack format vs email vs web)
- Bridge for personality (celebrate completion; encourage on blocker)
- Context dataclass pair pattern applicable

---

### 4. Feedback System ⚠️ PARTIAL (Medium Priority)

**File**: `services/feedback/feedback_service.py`

**Grammar Assessment**:
- ✅ **Entity**: Feedback ownership tracked with session/user ID
- ⚠️ **Moment**: Capture timestamp, but not framed as significant moment
- ⚠️ **Place**: Session context captured, but not elevation to atmospheric Place
- ❌ **Lenses**: Minimal; just type/rating dimensions
- ✅ **Situation**: Different handling for bug vs feature vs UX feedback

**Current Language**: Mostly mechanical with some awareness
```python
async def capture_feedback(
    self,
    session_id: str,
    feedback_type: str,  # "bug", "feature", "ux"
    comment: str,
    rating: Optional[int] = None
) -> str:
```

**Grammar Deficits**:
- Feedback is treated as data capture, not as a Moment of insight
- No Place atmosphere (where feedback was given affects meaning)
- Response doesn't acknowledge the moment (no gratitude, no understanding)

**Transformation Potential**: MEDIUM
- Frame feedback capture as Moment Piper experiences user's insight
- Add Place awareness (feedback in standup = different from feedback in todo)
- Add personality to acknowledgment
- Temporal lens (is this early feedback or after long use?)

---

### 5. Slack Integration ⚠️ PARTIAL (High Priority)

**File**: `services/integrations/slack/slack_plugin.py`

**Grammar Assessment**:
- ✅ **Entity**: Slack user/workspace identity maintained
- ⚠️ **Moment**: Message events captured, but as data not Experience
- ✅ **Place**: Slack IS a Place; channel-specific behavior present
- ⚠️ **Lenses**: Some spatial awareness; #channel vs DM context
- ⚠️ **Situation**: Different behavior for mentions vs commands vs background

**Current Language**: Plugin structure with limited personality
```python
class SlackPlugin(PiperPlugin):
    def __init__(self):
        self.config_service = SlackConfigService()
        self.integration_router = SlackIntegrationRouter(self.config_service)
```

**Grammar Deficits**:
- Responses feel templated, not personality-infused
- Channel atmosphere not really appreciated (public #channel response same tone as DM)
- No Moment framing (user is in middle of conversation; how should Piper enter?)

**Transformation Potential**: HIGH
- Add Slack-specific personality (casual, emoji-friendly, channel-aware)
- Moment bridge: Detect when user is seeking help vs exploring vs collaborating
- Place atmosphere: DM feels intimate; #channel feels professional
- Temporal lens: Time of day affects tone (morning standup mention vs late night)

---

### 6. GitHub Integration ⚠️ PARTIAL (High Priority)

**File**: `services/integrations/github/github_plugin.py`

**Grammar Assessment**:
- ✅ **Entity**: Repository/org identity; user as contributor maintained
- ⚠️ **Moment**: Events (push, PR, issue) captured as data, not Moments
- ⚠️ **Place**: GitHub IS a Place; but response is generic
- ⚠️ **Lenses**: Repository context provides some lens
- ⚠️ **Situation**: PR vs issue vs commit - different handling, but subtle

**Current Language**: Templated/mechanical
```python
class GitHubPlugin(PiperPlugin):
    def get_router(self) -> Optional[APIRouter]:
        """Return FastAPI router with GitHub routes."""
```

**Grammar Deficits**:
- GitHub activity is summarized as data, not as Moments the developer experienced
- No Moment narrative (what happened and why it matters to developer)
- Repository identity is Place, but atmosphere not adapted
- Urgency lens missing (is this a blocker? A nice-to-have review?)

**Transformation Potential**: HIGH
- Frame activity as developer's Moments (you pushed code, created PR, got review)
- Add urgency/impact lens (blocked PR affects tempo differently than review comment)
- Adapt tone to repo culture (fast-moving startup vs established project)
- Synthesize into standup narrative

---

### 7. Notion Integration ❌ FLATTENED (Medium Priority)

**File**: `services/integrations/notion/notion_plugin.py`

**Grammar Assessment**:
- ✅ **Entity**: Document ownership preserved
- ❌ **Moment**: Document updates treated as data, not meaningful occurrences
- ❌ **Place**: Notion workspace is Place, but no atmosphere adaptation
- ❌ **Lenses**: Just content retrieval; no perceptual adaptation
- ⚠️ **Situation**: Some filtering by document type, but minimal

**Current Language**: Data retrieval
```python
async def get_documents(self, workspace_id: str) -> List[Document]:
    """Fetch documents from Notion workspace."""
```

**Grammar Deficits**:
- Notion docs are treated as data sources, not Places or Moments
- No narrative about what changed or why it matters
- Response format is query result, not experience

**Transformation Potential**: MEDIUM
- Frame docs as Places (database = place to work; meeting notes = Place to remember)
- Change-tracking as Moments (you updated this doc)
- Add context about relevance (this doc mentions your current project)
- Synthesize into broader context awareness

---

### 8. Calendar Integration ⚠️ PARTIAL (Medium Priority)

**File**: `services/integrations/calendar/calendar_integration.py`

**Grammar Assessment**:
- ✅ **Entity**: Calendar owner identity maintained
- ✅ **Moment**: Events ARE Moments; temporal framing present (current meeting, upcoming events)
- ⚠️ **Place**: Calendar events have location, but not atmospherically adapted
- ⚠️ **Lenses**: Temporal lens strong; urgency/focus lenses partial
- ⚠️ **Situation**: Free time vs meeting time vs focus time - some situational awareness

**Current Language**: Temporal but mechanical
```python
temporal_summary = {
    "current_meeting": current_meeting,
    "free_blocks": free_blocks,
    "focus_time": focus_time
}
```

**Grammar Deficits**:
- Moment is recognized (current meeting) but presentation could be warmer
- Place (meeting location) recognized but atmosphere not adapted
- No Piper presence in the narrative (just facts)

**Transformation Potential**: MEDIUM
- Add empathy to current meeting awareness ("I see you're in a meeting; I'll wait")
- Adapt response based on next event (running late? prepare for standup?)
- Multiple lenses: focus time affects response differently than free time

---

### 9. Auth/Session Management ❌ FLATTENED (Low Priority)

**File**: `services/auth/auth_service.py`

**Grammar Assessment**:
- ✅ **Entity**: User identity is core function
- ❌ **Moment**: Authentication is treated as security check, not Moment
- ❌ **Place**: No Place awareness in auth flow
- ❌ **Lenses**: Security-only dimension; no other perceptual lenses
- ⚠️ **Situation**: Different auth flows exist, but minimal situational variation

**Current Language**: Security/technical
```python
async def authenticate_user(
    self,
    username: str,
    password: str
) -> AuthToken:
    """Authenticate user and return token."""
```

**Grammar Deficits**:
- Auth is necessary but low-grammar component
- First login IS a Moment (onboarding opportunity), but not treated as such
- Session timeout could be graceful (acknowledged) vs harsh (denied)

**Transformation Potential**: LOW
- Reason: Auth is infrastructure-adjacent; grammar application limited
- Possible: Frame first login as Moment; acknowledge session end gracefully
- Not a priority for Phase 2 (focus on high-impact features first)

---

### 10. Conversation Handler ⚠️ PARTIAL (Medium Priority)

**File**: `services/conversation/conversation_handler.py`

**Grammar Assessment**:
- ✅ **Entity**: User/Piper conversation identity maintained
- ⚠️ **Moment**: Message turns treated as exchanges, some sequence awareness
- ⚠️ **Place**: Conversation context (onboarding vs standup vs general) partially tracked
- ⚠️ **Lenses**: Personality system provides some lenses; limited perceptual adaptation
- ✅ **Situation**: Different handlers for different conversation types (standup vs onboarding vs portfolio)

**Current Language**: Conversation-aware but mechanical
```python
async def handle_message(
    self,
    conversation_id: str,
    user_id: str,
    message: str
) -> str:
```

**Grammar Deficits**:
- Conversation is fundamentally about Moments, but frames them mechanically
- No Place atmosphere adjustment (web vs Slack conversation different?)
- Response bridge not consistently applied

**Transformation Potential**: MEDIUM
- Frame each message as Moment of understanding/expression
- Add Place awareness (where is conversation happening?)
- Consistent personality bridge application
- Memory of conversation Moments (not just last message)

---

### 11. Onboarding System ⚠️ PARTIAL (Medium Priority)

**File**: `services/onboarding/portfolio_onboarding_handler.py`

**Grammar Assessment**:
- ⚠️ **Entity**: User identity present but Piper's role unclear
- ✅ **Moment**: Onboarding IS Moments (first login, first integration, first success)
- ⚠️ **Place**: Recognizes web as entry Place but minimal atmosphere
- ✅ **Lenses**: Progressive disclosure uses perception (user's readiness level)
- ✅ **Situation**: Context-dependent prompts; different paths for different states

**Current Language**: Structured but somewhat mechanical
```python
async def process_portfolio_step(
    self,
    user_id: str,
    step: str,
    data: Dict[str, Any]
) -> PortfolioStep:
```

**Grammar Deficits**:
- Onboarding framing is prescriptive not collaborative
- Place (web onboarding) could feel warmer
- Piper's encouragement not consistent

**Transformation Potential**: MEDIUM
- Frame onboarding as journey Piper guides user through (collaborative)
- Add warmth/encouragement at key Moments (first integration successful!)
- Place-specific messaging (welcoming tone for web)
- Celebrate progress points

---

### 12. List Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/list_repository.py`

**Grammar Assessment**:
- ⚠️ **Entity**: List ownership preserved
- ❌ **Moment**: Lists treated as persistent data structure
- ❌ **Place**: No Place awareness
- ❌ **Lenses**: No perceptual adaptation
- ✅ **Situation**: Minimal - different queries, same response format

**Transformation Potential**: LOW
- Reason: Lists are foundational data structures; low user-facing impact
- Possible: Treat list creation as Moment; adapt based on usage pattern
- Better focus: Uplift features that present to users first

---

### 13. Project Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/project_repository.py`

**Grammar Assessment**:
- ⚠️ **Entity**: Project ownership preserved
- ❌ **Moment**: Projects are data, not Experiences
- ❌ **Place**: No atmosphere adaptation
- ❌ **Lenses**: Basic filtering only
- ✅ **Situation**: Different queries exist but no situational response variation

**Transformation Potential**: LOW
- Reason: Behind other features; indirect user impact
- Better focus: Uplift features that present to users first

---

### 14. File Management ❌ FLATTENED (Low Priority)

**File**: `services/repositories/file_repository.py`

**Grammar Assessment**:
- ⚠️ **Entity**: File ownership preserved
- ❌ **Moment**: Files treated as data objects
- ❌ **Place**: No context/atmosphere
- ❌ **Lenses**: No perceptual dimensions
- ✅ **Situation**: Status-based queries only

**Transformation Potential**: LOW
- Reason: Low-level infrastructure; uplift user-facing features first

---

### 15. Personality System ⚠️ PARTIAL (Medium Priority)

**Correction (2026-09-24, #1775/#1883)**: `standup_bridge.py` was deleted 2026-09-24 as
unreachable dead code (#1775) — never instantiated or called in production. Everything below
describes the design, not a running assessment; read the present-tense claims accordingly.

**File**: `services/personality/standup_bridge.py` (deleted 2026-09-24, #1775)

**Grammar Assessment** (as designed, never verified running):
- ✅ **Entity**: Piper's personality as Entity
- ⚠️ **Moment**: Applies warmth calibration across Moments
- ✅ **Place**: Adapts tone based on Place (email vs chat)
- ⚠️ **Lenses**: Warmth/encouragement lenses; limited other dimensions
- ⚠️ **Situation**: Adjusts based on accomplishment level, but limited situational variation

**Current Language**: Personality-aware but targeted
```python
accomplishment_prefixes = {
    0.8: ["Outstanding work!", "Incredible progress!"],
    0.6: ["Great job!", "Nice work!"],
    0.4: ["Good progress!", "Moving forward!"],
}
```

**Grammar Deficits**:
- Excellent example of warmth calibration
- Could apply more broadly beyond standup

**Transformation Potential**: MEDIUM
- Extract personality patterns for reuse across all features
- Expand lenses beyond warmth (confidence, urgency, collaboration)
- Consistent application across all Piper responses

---

### 16. MCP Integration ❌ FLATTENED (Low Priority)

**File**: `services/mcp/mcp_plugin.py`

**Grammar Assessment**:
- ⚠️ **Entity**: External system identity preserved
- ❌ **Moment**: Tool invocations treated as API calls
- ⚠️ **Place**: Context passed but not atmospherically adapted
- ⚠️ **Lenses**: Tool capabilities create lens, but limited
- ⚠️ **Situation**: Tool selection based on context, but minimal variation

**Transformation Potential**: LOW
- Reason: Infrastructure-adjacent; limited user-facing impact
- Focus: Higher-priority features first

---

## Transformation Priority Ranking

### 🔴 CRITICAL (High Priority) - Implement in Phase 2-3

**Impact**: High user-facing impact; moderate transformation complexity

1. **Intent Classification** (⚠️ Partial → ✅ Conscious)
   - User touches every interaction
   - Clear grammar gaps: missing Place, Moment framing
   - Reusable patterns: Context/Result pair, Moment bridge

2. **Slack Integration** (⚠️ Partial → ✅ Conscious)
   - Core communication channel; high usage
   - Clear Place (Slack channel); needs Moment framing + Personality bridge
   - High impact on user experience

3. **GitHub Integration** (⚠️ Partial → ✅ Conscious)
   - High-engagement developers
   - Activity data ready to transform into Moment narrative
   - Reusable: Activity→Moment framing

4. **Todo Management** (❌ Flattened → ⚠️ Partial)
   - Core feature; high usage
   - Major transformation needed
   - Pattern: Context/Result + Personality bridge

### 🟡 IMPORTANT (Medium Priority) - Implement in Phase 3-4

5. **Feedback System** (⚠️ Partial → ✅ Conscious)
   - Mid-frequency user interaction
   - Moderate transformation (mostly personality + Moment framing)
   - Good learning opportunity

6. **Conversation Handler** (⚠️ Partial → ✅ Conscious)
   - Foundational; affects all interactions
   - Moderate complexity; good for pattern consolidation
   - Enables better personality consistency

7. **Onboarding System** (⚠️ Partial → ✅ Conscious)
   - First-impression impact
   - Transformation: collaborative framing + warmth calibration
   - Learning opportunity: progressive disclosure + Situation awareness

8. **Calendar Integration** (⚠️ Partial → ✅ Conscious)
   - Contextual awareness is strong; Moment framing needed
   - Good for multi-lens pattern (temporal + spatial + urgency)

9. **Personality System** (⚠️ Partial → ✅ Conscious)
   - Infrastructure; but enables above features
   - Extract reusable patterns; expand lens dimensions
   - Creates bridge for all features to use consistently

### 🟢 DEFERRED (Low Priority) - Implement in Phase 4+

- **Auth/Session Management**: Infrastructure-adjacent; limited grammar impact
- **List/Project/File Management**: Backend features; low direct user impact
- **MCP Integration**: Infrastructure-adjacent; limited user-facing impact

---

## Key Patterns for Reuse

Based on audit and P0 analysis, these patterns are consistently needed:

### Pattern: Context/Result Dataclass Pair
**Applicable To**: Intent, Todo, Feedback, Conversation, Onboarding, GitHub, Slack

```python
@dataclass
class [Feature]Context:
    """Input context before processing"""
    user_id: str                    # Entity
    timestamp: datetime             # Moment
    source_places: Dict[str, Any]   # Places

@dataclass
class [Feature]Result:
    """Output result after processing"""
    user_id: str                    # Entity preserved
    generated_at: datetime          # Moment of result
    findings: List[str]             # What was learned
    source_places: Dict[str, str]   # Where data came from
```

### Pattern: Place Gathering (Parallel)
**Applicable To**: Intent, Todo, Feedback, GitHub, Slack, Conversation

```python
async def gather_context(self) -> Dict[str, Any]:
    # Parallel fetch from Places
    results = await asyncio.gather(
        self._get_place_1_context(),
        self._get_place_2_context(),
        self._get_place_3_context(),
    )
    return self._synthesize(results)
```

### Pattern: Personality Bridge
**Applicable To**: ALL features that present data to users

```python
class [Feature]ToChatBridge:
    def adapt_for_chat(self, raw_data: Dict) -> str:
        """Transform raw data to conversational format"""

    def apply_personality(self, content: str, context: Dict) -> str:
        """Apply warmth, action orientation, presence"""
```

### Pattern: Warmth Calibration
**Applicable To**: Todo, Feedback, Intent responses, Onboarding feedback

```python
warmth_levels = {
    0.8: ["Outstanding!", "Fantastic!", "Incredible!"],   # High
    0.6: ["Great!", "Nice work!", "Well done!"],          # Medium
    0.4: ["Good progress", "Moving forward"],             # Neutral
    0.2: ["Progress made", "Continuing on"],              # Low
}
```

### Pattern: Honest Failure with Suggestion
**Applicable To**: All integration features

```python
except IntegrationError as e:
    error_msg = f"[Feature] encountered: {str(e)}"
    suggestion = self._diagnose_failure(e)
    raise [Feature]Error(
        f"{error_msg}\nSuggestion: {suggestion}",
        suggestion=suggestion
    )
```

### Pattern: Moment Framing
**Applicable To**: All features

```python
# Instead of:
"Query returned 5 items"

# Use:
"I noticed 5 items since your last review"
# or
"I found 5 items that might interest you"
# or
"5 important items need attention"
```

---

## Recommendations by Feature

### Intent Classification

**Current**: Mechanical classification
**Goal**: Conscious intent recognition

**Approach**:
1. Add Place detection (Slack vs CLI vs web)
2. Frame intent as Moment Piper experiences
3. Apply Personality bridge to response
4. Use warmth calibration for confidence-based responses

**Estimated Effort**: Medium (5-7 patterns to apply)
**User Impact**: High (all interactions begin with intent)

### Slack Integration

**Current**: Templated responses
**Goal**: Channel-aware, personality-infused

**Approach**:
1. Detect Channel atmosphere (public vs DM vs bot-mention)
2. Frame messages as Moments user is experiencing
3. Adapt personality to Slack culture (emoji, casual tone)
4. Time-aware responses (morning standup mention vs random evening)

**Estimated Effort**: Medium (4-5 patterns)
**User Impact**: High (primary communication channel)

### GitHub Integration

**Current**: Data summaries
**Goal**: Activity narrative

**Approach**:
1. Frame commits/PRs/issues as developer Moments
2. Add urgency lens (blocked vs review vs FYI)
3. Adapt tone to repo culture
4. Synthesize into standup context

**Estimated Effort**: Medium (5-6 patterns)
**User Impact**: High (developer engagement)

### Todo Management

**Current**: Database operations
**Goal**: Conscious task management

**Approach**:
1. Add Place awareness (Slack vs email vs web todo)
2. Frame task lifecycle as Moments (creation, completion, blocking)
3. Apply personality bridge with warmth calibration
4. Context/Result pair for structured feedback

**Estimated Effort**: High (6-7 patterns, larger refactoring)
**User Impact**: Very High (core feature)

---

## Related Documentation

- **Feature-Object Model Map**: `docs/internal/architecture/current/feature-object-model-map.md` - Per-feature mapping of Entities/Moments/Places with canonical queries
- **ADR-055**: Object Model Implementation (formalized grammar)
- **MUX Implementation Guide**: `docs/internal/development/mux-implementation-guide.md`
- **MUX Experience Tests**: `docs/internal/development/mux-experience-tests.md`
- **Morning Standup Analysis**: `dev/2026/01/19/p0-morning-standup-analysis.md`
- **B1 FTUX Grammar Mapping**: `dev/2026/01/19/p0-b1-ftux-grammar-mapping.md`

---

## Next Steps

**Phase 2 (Planned)**: Extract and formalize 5+ reusable patterns from Morning Standup into pattern catalog

**Phase 3 (Planned)**: Create transformation guide with worked examples (Intent Classification recommended)

**Phase Z (Planned)**: Update ADRs, create developer onboarding checklist, enable independent application

---

## Appendix: Audit Evidence

### Files Reviewed

**Core Features**:
- `services/features/morning_standup.py` (reference)
- `services/intent_service/classifier.py` (intent)
- `services/todo/todo_service.py` (todo)
- `services/feedback/feedback_service.py` (feedback)

**Integrations**:
- `services/integrations/slack/slack_plugin.py`
- `services/integrations/github/github_plugin.py`
- `services/integrations/notion/notion_plugin.py`
- `services/integrations/calendar/calendar_integration.py`
- `services/integrations/mcp/mcp_plugin.py`

**Infrastructure**:
- `services/conversation/conversation_handler.py`
- `services/onboarding/portfolio_onboarding_handler.py`
- `services/auth/auth_service.py`
- `services/personality/standup_bridge.py` (deleted 2026-09-24, #1775 — never wired to production)
- `services/repositories/list_repository.py`
- `services/repositories/project_repository.py`
- `services/repositories/file_repository.py`

### Analysis References

- P0 Morning Standup Analysis: 6 consciousness patterns identified
- P0 B1 FTUX Grammar Mapping: Grammar vocabulary present in existing specs
- MUX Infrastructure: 302 tests validating grammar compliance framework

---

*Audit completed: 2026-01-20*
*Next review: Post-Phase 2 pattern extraction*
