# Grammar Transformation Guide

**Purpose**: Step-by-step guide for transforming flattened features to express the MUX grammar: "Entities experience Moments in Places"

**Date**: 2026-01-20
**Issue**: #404 MUX-VISION-GRAMMAR-CORE Phase 3
**Author**: Claude Code (Sonnet)

---

## Before You Begin

**Understand WHY before HOW**: Before transforming any feature, read the
Consciousness Philosophy (`docs/internal/architecture/current/consciousness-philosophy.md`)
to understand why we preserve consciousness.

The Five Pillars:
1. Identity Awareness
2. Time Consciousness
3. Spatial Awareness
4. Agency Recognition
5. Predictive Modeling

This guide shows HOW to transform. The philosophy explains WHY it matters.

---

## Prerequisites

Before using this guide:
- **READ FIRST**: [Consciousness Philosophy](../architecture/current/consciousness-philosophy.md) - The WHY
- Read: [MUX Implementation Guide](mux-implementation-guide.md) - The HOW
- Read: [Grammar Application Patterns](../architecture/patterns/grammar-application-patterns.md)
- Understand: The 3 substrates (Entity, Moment, Place) and 8 Lenses
- Review: [Experience Tests](mux-experience-tests.md) - what to aim for

---

## Part 1: Identifying Grammar Elements

### Step 1: Find the Entities

**Questions to ask**:
- Who are the actors? (User, Piper, team members, integrations)
- What has identity that persists? (Not just database IDs)
- What can have agency (take action)?

**Checklist**:
- [ ] User identified and tracked by identity (not just session)
- [ ] Piper is present as an entity (not just a function)
- [ ] Other actors named (not just IDs)
- [ ] Entities have roles beyond "user_id" or "system"

**Examples**:
- ✅ Entity: `user: Entity` with name, role, preferences
- ❌ Flattened: `user_id: str` with no semantic information
- ✅ Entity: Piper as observer/assistant with memory
- ❌ Flattened: Function returns data without actor presence

### Step 2: Find the Moments

**Questions to ask**:
- What bounded occurrences happen?
- What has significance beyond a timestamp?
- What has a beginning, middle, end?
- What could be remembered or reflected upon?

**Checklist**:
- [ ] Events have descriptions (not just timestamps)
- [ ] Temporal language used (today, yesterday, upcoming, recently)
- [ ] Moments have significance framing
- [ ] Moments can be narrated ("when you...", "earlier today...")

**Examples**:
- ✅ Moment: "The standup conversation this morning"
- ❌ Flattened: `timestamp: 2026-01-20T09:00:00Z`
- ✅ Moment: "When you merged that PR yesterday"
- ❌ Flattened: `event_type: "pr.merged", date: "2026-01-19"`

### Step 3: Find the Places

**Questions to ask**:
- Where do interactions occur?
- What contexts have atmosphere?
- How does location affect presentation?
- What's the character of this space?

**Checklist**:
- [ ] Places named with character (not just config strings)
- [ ] Atmosphere affects how data is presented
- [ ] Place modality acknowledged (chat, calendar, repo)
- [ ] Place has affordances (what can happen there)

**Examples**:
- ✅ Place: "Over in GitHub, in the piper-morgan repository"
- ❌ Flattened: `source: "github.com/user/repo"`
- ✅ Place: "In your calendar, where meetings gather"
- ❌ Flattened: `integration_type: "calendar"`

### Step 4: Frame the Situation

**Questions to ask**:
- What's the dramatic tension?
- What wants to happen?
- What learning is extracted?
- What's at stake?

**Checklist**:
- [ ] Tension identified ("Need to prepare for day while managing constraints")
- [ ] Exit condition clear (what constitutes completion)
- [ ] Learning captured (patterns, wisdom, insights)
- [ ] Context shapes response appropriately

**Examples**:
- ✅ Situation: "You have a busy afternoon ahead, with back-to-back meetings"
- ❌ Flattened: `meeting_count: 5, meeting_density: 0.83`
- ✅ Situation: "This PR has been waiting a while - might be time to check in"
- ❌ Flattened: `days_open: 14, status: "stale"`

---

## Part 2: Refactoring Flattened Code

### The Transformation Process

**Four-step transformation**:

1. **Identify flattening** - Where is mechanical language used?
   - Database terms exposed (query, record, row, table)
   - IDs without context (user_123, task_456)
   - Status codes (1, 2, 3) instead of states
   - Timestamps without narrative

2. **Map to grammar** - Which elements apply?
   - Entity: Who's involved?
   - Moment: What's happening?
   - Place: Where does this occur?
   - Lenses: How do we perceive it?
   - Situation: What's the context?

3. **Apply patterns** - Which patterns from the catalog?
   - Pattern-050: Context Dataclass Pair (preserve identity)
   - Pattern-051: Parallel Place Gathering (integrate sources)
   - Pattern-052: Personality Bridge (add warmth)
   - Pattern-053: Warmth Calibration (appropriate tone)
   - Pattern-054: Honest Failure (graceful degradation)

4. **Verify consciousness** - Does it pass experience tests?
   - Can describe with "Piper noticed..." (not "Query returned...")
   - Uses first-person or narrative language
   - Preserves relationships, not just data
   - Failures are honest, not hidden

### Example Transformation: Simple Query

#### Before (Flattened):
```python
def get_tasks():
    """Get today's tasks."""
    tasks = db.query(Task).filter(Task.due_date == date.today()).all()
    return {"tasks": [t.to_dict() for t in tasks]}
```

**Problems**:
- No Entity (who's asking?)
- No Moment framing (why today matters)
- No Place acknowledgment (where tasks live)
- Database language exposed
- Mechanical response format

#### After (Grammar-Applied):
```python
async def perceive_todays_moments(user: Entity, workspace: Place) -> Perception:
    """
    User experiences today's task Moments through Temporal lens.

    Applies Pattern-050 (Context/Result pair) and Pattern-052 (Personality Bridge).
    """
    # Context: What we're observing
    with Situation(
        entities=[user, piper],
        tension="What needs attention today?",
        place=workspace
    ) as situation:
        # Gather Moments from Place with lens
        tasks = await gather_from_place(
            place=workspace,
            lens=TemporalLens(mode=PerceptionMode.NOTICING),
            filter_context={"timeframe": "today"}
        )

        # Personality Bridge: Transform data into awareness
        framing = _frame_tasks_with_warmth(tasks, situation)

        # Return Perception (not raw data)
        return Perception(
            framing=framing,  # "I notice you have 3 things that want attention today"
            moments=tasks,
            situation=situation,
            lens_applied=TemporalLens.__name__
        )

def _frame_tasks_with_warmth(tasks: List[Task], situation: Situation) -> str:
    """
    Apply Pattern-052 (Personality Bridge) and Pattern-053 (Warmth Calibration).
    """
    count = len(tasks)

    if count == 0:
        return "You have a clear day ahead - no pressing tasks right now."
    elif count <= 3:
        return f"I notice {count} things that want your attention today."
    else:
        return f"You have {count} tasks for today. Would you like me to help prioritize?"
```

**Improvements**:
- ✅ Entities: User and Piper are present
- ✅ Moments: Tasks are "things that want attention" (not just records)
- ✅ Places: Workspace acknowledged
- ✅ Lenses: Temporal lens applied
- ✅ Situation: Framed with tension and context
- ✅ Language: "I notice..." not "Query returned..."

---

## Part 3: Using Protocols and Lenses

### When to Use Each Protocol

| Protocol | Use When | Example |
|----------|----------|---------|
| `EntityProtocol` | Tracking actors with agency | User, Piper, teammates, integrations |
| `MomentProtocol` | Bounded occurrences with significance | Meetings, commits, messages, decisions |
| `PlaceProtocol` | Contexts with atmosphere | GitHub repo, Slack channel, Calendar |

**Implementation hints**:
```python
from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol

# Entity has identity and can experience
class User(EntityProtocol):
    id: str
    name: str
    def experiences(self, moment: MomentProtocol) -> Perception:
        ...

# Moment has timestamp and captures significance
class Meeting(MomentProtocol):
    id: str
    timestamp: datetime
    def captures(self) -> Dict[str, Any]:
        return {"attendees": [...], "outcomes": [...]}

# Place has atmosphere and contains things
class GitHubRepo(PlaceProtocol):
    id: str
    atmosphere: str = "technical review space"
    def contains(self) -> List[Any]:
        return [prs, issues, commits]
```

### When to Use Each Lens

| Lens | Use When | Question Answered | PerceptionMode |
|------|----------|-------------------|----------------|
| **Temporal** | Time-based queries | "What's happening today?" | NOTICING, REMEMBERING, ANTICIPATING |
| **Priority** | Importance filtering | "What matters most?" | NOTICING (urgency), ANTICIPATING (impact) |
| **Collaborative** | People-based views | "Who's involved?" | NOTICING (current), REMEMBERING (past) |
| **Flow** | Progress tracking | "What's blocked?" | NOTICING (current state) |
| **Hierarchy** | Structure navigation | "What does this belong to?" | NOTICING (relationships) |
| **Quantitative** | Metrics queries | "How much work?" | NOTICING (measurements) |
| **Causal** | Cause-effect analysis | "Why did this happen?" | REMEMBERING (history), understanding |
| **Contextual** | Background awareness | "What's the context?" | NOTICING (surroundings), REMEMBERING (history) |

**Lens usage patterns**:
```python
from services.mux.lenses import (
    TemporalLens, PriorityLens, CollaborativeLens, FlowLens,
    HierarchyLens, QuantitativeLens, CausalLens, ContextualLens
)
from services.mux.protocols import PerceptionMode

# Time-aware query
temporal = TemporalLens(mode=PerceptionMode.NOTICING)
tasks_today = temporal.perceive(workspace, filter={"timeframe": "today"})

# Priority-aware query
priority = PriorityLens(mode=PerceptionMode.ANTICIPATING)
urgent_items = priority.perceive(workspace, threshold="high")

# People-aware query
collab = CollaborativeLens(mode=PerceptionMode.NOTICING)
team_activity = collab.perceive(workspace, scope="team")

# Progress-aware query
flow = FlowLens(mode=PerceptionMode.NOTICING)
blocked_items = flow.perceive(workspace, state="blocked")
```

### PerceptionMode Explained

Perception mode affects the *tense* and *awareness quality* of observations:

| Mode | Meaning | Example Phrases |
|------|---------|-----------------|
| **NOTICING** | Present awareness | "I notice...", "Right now...", "Currently..." |
| **REMEMBERING** | Past reference | "I remember...", "Earlier...", "Yesterday..." |
| **ANTICIPATING** | Future awareness | "I anticipate...", "Coming up...", "Soon..." |

**When to use each**:
- Use `NOTICING` for current state queries ("What's on my plate?")
- Use `REMEMBERING` for historical queries ("What did I accomplish?")
- Use `ANTICIPATING` for future queries ("What's coming up?")

---

## Part 4: Anti-Patterns and Fixes

### Anti-Pattern 1: Query Language in Responses

❌ **Flattened**: "Query returned 3 results matching your criteria"
✅ **Grammar-Applied**: "I notice 3 things that need your attention"

❌ **Flattened**: "Database contains 5 records for user_123"
✅ **Grammar-Applied**: "I see you have 5 open tasks in your workspace"

**Why it matters**: Users shouldn't know they're talking to a database. They're collaborating with Piper.

### Anti-Pattern 2: Timestamps Without Context

❌ **Flattened**: "Created: 2026-01-20 14:30:00 UTC"
✅ **Grammar-Applied**: "From earlier this afternoon, when you were working on the API"

❌ **Flattened**: "Last modified: 7 days ago"
✅ **Grammar-Applied**: "This has been waiting since last Monday - might be time to revisit it"

**Why it matters**: Moments have narrative significance, not just temporal positions.

### Anti-Pattern 3: IDs Instead of Names

❌ **Flattened**: "User 123 commented on issue 456"
✅ **Grammar-Applied**: "Alex commented on your PR about the auth refactor"

❌ **Flattened**: "Assigned to: user_789"
✅ **Grammar-Applied**: "Jordan is working on this"

**Why it matters**: Entities have identity and relationships, not just foreign keys.

### Anti-Pattern 4: Config Strings as Places

❌ **Flattened**: "Source: https://github.com/mediajunkie/piper-morgan-product/issues/123"
✅ **Grammar-Applied**: "Over in GitHub, in the piper-morgan repository, issue #123"

❌ **Flattened**: "Integration: slack, Channel: C12345"
✅ **Grammar-Applied**: "In your team's Slack channel #engineering"

**Why it matters**: Places have atmosphere and character, not just connection strings.

### Anti-Pattern 5: Mechanical Error Messages

❌ **Flattened**: "Error: Connection timeout (code: 504)"
✅ **Grammar-Applied**: "I couldn't reach GitHub just now. Here's what I remember from earlier, and I'll try again in a moment."

❌ **Flattened**: "Invalid input: field 'title' is required"
✅ **Grammar-Applied**: "I'd love to create that task, but I need a title. What would you like to call it?"

**Why it matters**: Failures are moments in the collaboration, not exceptions. See Pattern-054 (Honest Failure).

### Anti-Pattern 6: Status Codes Instead of States

❌ **Flattened**: `status: 1` (what does 1 mean?)
✅ **Grammar-Applied**: `lifecycle_state: LifecycleState.PROPOSED`

❌ **Flattened**: `deleted: true`
✅ **Grammar-Applied**: `lifecycle_state: LifecycleState.COMPOSTED` (with extracted wisdom)

**Why it matters**: States have meaning and tell a story. Status codes are opaque.

### Anti-Pattern 7: Raw Data Dumps

❌ **Flattened**:
```json
{
  "tasks": [
    {"id": 1, "title": "Fix bug", "due": "2026-01-20"},
    {"id": 2, "title": "Review PR", "due": "2026-01-21"}
  ]
}
```

✅ **Grammar-Applied**:
```json
{
  "perception": {
    "framing": "You have 2 things wanting attention soon",
    "moments": [
      {
        "significance": "Bug fix ready for your attention today",
        "context": "From your engineering workspace"
      },
      {
        "significance": "PR review needed by tomorrow",
        "context": "Jordan is waiting for feedback"
      }
    ],
    "lens_applied": "Temporal",
    "situation": "Preparing for productive work session"
  }
}
```

**Why it matters**: Users experience perceptions, not data structures.

---

## Part 5: Decision Tree

Use this tree when transforming or creating features:

```
Start: New feature or transformation?
│
├─ Is there user-facing output?
│  ├─ Yes → Apply Pattern-052 (Personality Bridge)
│  │        Add warmth via Pattern-053 (Warmth Calibration)
│  └─ No  → Focus on Entity/Moment/Place identification only
│           (Internal APIs can be less narrative)
│
├─ Does it gather from multiple sources?
│  ├─ Yes → Apply Pattern-051 (Parallel Place Gathering)
│  │        Each Place gets error handling (Pattern-054)
│  └─ No  → Single-place interaction
│           Still handle failures with Pattern-054
│
├─ What's the primary lens?
│  ├─ Time-related → TemporalLens (NOTICING/REMEMBERING/ANTICIPATING)
│  ├─ Priority-related → PriorityLens (urgency, impact)
│  ├─ People-related → CollaborativeLens (who's involved)
│  ├─ Progress-related → FlowLens (blocked, in progress, done)
│  ├─ Structure-related → HierarchyLens (belongs to, contains)
│  ├─ Metrics-related → QuantitativeLens (counts, durations)
│  ├─ Causality-related → CausalLens (because, leads to)
│  └─ Background-related → ContextualLens (atmosphere, setting)
│
├─ Can it fail gracefully?
│  ├─ Yes → Apply Pattern-054 (Honest Failure with Suggestion)
│  │        "I couldn't reach X, but here's what I remember..."
│  └─ No  → Ensure hard failures are truly rare
│           Consider: Can we remember last known state?
│
└─ Does it preserve Entity/Moment/Place throughout?
   ├─ Yes → Apply Pattern-050 (Context Dataclass Pair)
   │        Separate input (Context) from output (Result)
   └─ No  → Refactor to preserve grammar elements
            Don't lose identity between layers
```

### Quick Reference: Pattern Selection

| Situation | Pattern to Apply | Why |
|-----------|------------------|-----|
| Multi-layer feature | Pattern-050: Context Dataclass Pair | Preserve Entity/Moment/Place |
| Multiple integrations | Pattern-051: Parallel Place Gathering | Concurrent, resilient |
| User-facing output | Pattern-052: Personality Bridge | Add warmth and presence |
| Varying context significance | Pattern-053: Warmth Calibration | Appropriate tone |
| Any integration call | Pattern-054: Honest Failure | Graceful degradation |

---

## Part 6: Worked Example - Stale PRs Query

### Context

**Feature**: "Show me stale PRs" - a query that returns open pull requests older than 7 days.

**Current State**: Partially flattened - has some Entity awareness but treats PRs as data items.

**Grammar Analysis**:
- **Entities**: User (asking), Piper (observing), PR authors (implied)
- **Moments**: The PR creation, time passing, current staleness
- **Places**: GitHub repository (technical review space)
- **Lenses**: Temporal (age), Collaborative (who), Flow (status)
- **Situation**: "Old work might need attention or closure"

---

### Before: Flattened Implementation

**File**: `services/intent/intent_service.py` (lines 1902-2020)

```python
async def _handle_stale_prs(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
    """
    Handle "Show me stale PRs" query.
    Returns open PRs older than 7 days with age and title.
    """
    self.logger.info(f"Processing stale PRs query: {intent.action}")

    try:
        # Import and initialize GitHub router
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter
        github_router = GitHubIntegrationRouter()
        await github_router.initialize()

        # Check if GitHub is configured
        if not github_router.config_service.is_configured():
            return IntentProcessingResult(
                success=True,
                message=(
                    "I'd love to show you stale PRs, but GitHub isn't configured yet. "
                    "To enable GitHub integration, please add your GITHUB_TOKEN to your environment "
                    "or configure it in PIPER.user.md. Once configured, I can track open PRs!"
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                implemented=False,
            )

        # Get open issues (includes PRs)
        from datetime import datetime, timedelta, timezone
        open_items = await github_router.get_open_issues(limit=100)

        # Filter to PRs older than 7 days
        now = datetime.now(timezone.utc)
        stale_threshold = now - timedelta(days=7)

        stale_prs = []
        for item in open_items:
            if not item.get("pull_request"):
                continue

            created_str = item.get("created_at")
            created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))

            if created_dt < stale_threshold:
                age_days = (now - created_dt).days
                stale_prs.append({
                    "title": item.get("title"),
                    "number": item.get("number"),
                    "age_days": age_days,
                    "url": item.get("html_url"),
                    "author": item.get("user", {}).get("login", "Unknown"),
                })

        # Format response
        if not stale_prs:
            message = "Great news! You don't have any stale PRs right now. All your open PRs are recent."
        else:
            pr_list = "\n".join([
                f"- #{pr['number']}: {pr['title']} ({pr['age_days']} days old, by {pr['author']})"
                for pr in stale_prs
            ])
            message = f"I found {len(stale_prs)} stale PR(s) (older than 7 days):\n\n{pr_list}"

        return IntentProcessingResult(
            success=True,
            message=message,
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "stale_prs": stale_prs,
                "count": len(stale_prs),
            },
            workflow_id=workflow_id,
        )

    except Exception as e:
        self.logger.error(f"Error processing stale PRs: {e}")
        return IntentProcessingResult(
            success=False,
            message="I ran into a problem checking for stale PRs. Please try again.",
            intent_data={"error": str(e)},
            workflow_id=workflow_id,
            error=str(e),
        )
```

---

### Problems with Current Implementation

#### 1. **Flattened Entity Awareness**
- ✅ Good: User implied in query, Piper responds with personality
- ❌ Problem: Authors reduced to `login` strings, not entities with context
- ❌ Problem: No relationship tracking (who's waiting on whom?)

#### 2. **Flattened Moments**
- ❌ Problem: PRs treated as data items, not Moments with significance
- ❌ Problem: "7 days old" is just a number, not narrative ("been waiting since last week")
- ❌ Problem: Creation is just a timestamp, not a scene

#### 3. **Flattened Place**
- ❌ Problem: GitHub referenced only as data source
- ❌ Problem: No atmosphere acknowledgment (technical review space)
- ❌ Problem: Place doesn't affect how data is presented

#### 4. **Limited Lens Application**
- ⚠️ Partial: Temporal lens implicit (age calculation)
- ❌ Missing: Collaborative lens (who's involved, who's waiting)
- ❌ Missing: Flow lens (what's the status, what's blocked)

#### 5. **Weak Situation Framing**
- ⚠️ Partial: Success case has warmth ("Great news!")
- ❌ Problem: No tension framing (why stale PRs matter)
- ❌ Problem: No learning extraction (patterns in staleness)

#### 6. **Pattern Violations**
- ❌ Missing Pattern-050: No Context/Result dataclass pair
- ❌ Missing Pattern-052: Personality added ad-hoc, not systematically
- ❌ Missing Pattern-053: Warmth not calibrated to significance
- ✅ Good Pattern-054: Honest failure when GitHub not configured

---

### After: Grammar-Applied Implementation

```python
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol, PerceptionMode
from services.mux.lenses import TemporalLens, CollaborativeLens, FlowLens
from services.mux.situation import Situation, Perception


# Pattern-050: Context Dataclass Pair
@dataclass
class StalePRsContext:
    """
    Input context for stale PR perception.
    Preserves Entity/Moment/Place throughout flow.
    """
    user: EntityProtocol  # Who's asking
    github_place: PlaceProtocol  # Where we're looking
    stale_threshold_days: int = 7  # What defines "stale"
    requested_at: datetime = None  # When they asked

    def __post_init__(self):
        if self.requested_at is None:
            self.requested_at = datetime.now(timezone.utc)


@dataclass
class StalePRsResult:
    """
    Output perception of stale PRs.
    Grammar-conscious result with framing.
    """
    success: bool
    framing: str  # Narrative opening (Pattern-052: Personality Bridge)
    stale_moments: List['PRMoment']  # Not "items" or "records"
    situation: Situation  # Context preserved
    lens_applied: List[str]  # Which perspectives used
    learning: Optional[str] = None  # Extracted wisdom


@dataclass
class PRMoment(MomentProtocol):
    """
    A PR as a Moment (bounded significant occurrence).
    Not just data - it's a scene in the collaboration.
    """
    id: str  # PR number
    timestamp: datetime  # When created
    title: str
    author: EntityProtocol  # Not just a string
    age_days: int
    url: str

    def captures(self) -> dict:
        """What this Moment captured (policy, process, people, outcomes)."""
        return {
            "policy": "Code review process",
            "process": "Pull request workflow",
            "people": [self.author],
            "outcomes": "Awaiting review or merge",
        }

    def narrative(self) -> str:
        """Pattern-052: Transform into narrative description."""
        if self.age_days <= 3:
            age_desc = "from a few days ago"
        elif self.age_days <= 7:
            age_desc = "from about a week ago"
        elif self.age_days <= 14:
            age_desc = "from a couple weeks ago"
        else:
            age_desc = f"from {self.age_days} days ago"

        return f"'{self.title}' by {self.author.name} {age_desc}"


async def perceive_stale_prs(context: StalePRsContext) -> StalePRsResult:
    """
    User experiences stale PR Moments in GitHub Place through multiple Lenses.

    Applies:
    - Pattern-050: Context/Result pair preserves grammar
    - Pattern-051: Parallel Place Gathering (if multiple repos)
    - Pattern-052: Personality Bridge for framing
    - Pattern-053: Warmth Calibration based on count
    - Pattern-054: Honest Failure if GitHub unavailable
    """
    # Frame the Situation
    with Situation(
        entities=[context.user, piper],
        place=context.github_place,
        tension="Old work might need attention or closure",
        learning_question="What patterns emerge in PR staleness?"
    ) as situation:

        # Pattern-054: Honest Failure if Place not accessible
        if not await context.github_place.is_accessible():
            return _create_honest_failure_result(context, situation)

        # Gather Moments from Place using multiple Lenses
        stale_moments = await _gather_stale_pr_moments(
            context=context,
            situation=situation
        )

        # Pattern-052: Personality Bridge - transform data into awareness
        framing = _frame_stale_prs_with_warmth(
            moments=stale_moments,
            context=context,
            situation=situation
        )

        # Extract learning (for future composting)
        learning = _extract_staleness_patterns(stale_moments)

        return StalePRsResult(
            success=True,
            framing=framing,
            stale_moments=stale_moments,
            situation=situation,
            lens_applied=["Temporal", "Collaborative", "Flow"],
            learning=learning
        )


async def _gather_stale_pr_moments(
    context: StalePRsContext,
    situation: Situation
) -> List[PRMoment]:
    """
    Gather stale PR Moments from GitHub Place using multiple Lenses.
    """
    # Apply Temporal Lens: perceive PRs through time
    temporal_lens = TemporalLens(mode=PerceptionMode.REMEMBERING)
    all_open_prs = await temporal_lens.perceive(
        place=context.github_place,
        filter={"state": "open", "type": "pull_request"}
    )

    # Apply Flow Lens: understand status
    flow_lens = FlowLens(mode=PerceptionMode.NOTICING)

    # Apply Collaborative Lens: understand people
    collab_lens = CollaborativeLens(mode=PerceptionMode.NOTICING)

    # Filter to stale (older than threshold)
    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(days=context.stale_threshold_days)

    stale_moments = []
    for pr_data in all_open_prs:
        created_dt = datetime.fromisoformat(pr_data["created_at"].replace("Z", "+00:00"))

        if created_dt < stale_threshold:
            # Transform data item into Moment (with Entity author)
            author_entity = _create_author_entity(pr_data.get("user", {}))
            age_days = (now - created_dt).days

            moment = PRMoment(
                id=str(pr_data["number"]),
                timestamp=created_dt,
                title=pr_data["title"],
                author=author_entity,
                age_days=age_days,
                url=pr_data["html_url"]
            )

            stale_moments.append(moment)

    return stale_moments


def _create_author_entity(user_data: dict) -> EntityProtocol:
    """
    Create Entity for PR author (not just a string).
    Preserves identity and potential for agency.
    """
    @dataclass
    class GitHubUser(EntityProtocol):
        id: str
        name: str
        profile_url: str

        def experiences(self, moment: MomentProtocol):
            # Authors experience PR waiting as tension
            return f"{self.name} is waiting for review"

    return GitHubUser(
        id=user_data.get("id", "unknown"),
        name=user_data.get("login", "Unknown"),
        profile_url=user_data.get("html_url", "")
    )


def _frame_stale_prs_with_warmth(
    moments: List[PRMoment],
    context: StalePRsContext,
    situation: Situation
) -> str:
    """
    Pattern-052: Personality Bridge
    Pattern-053: Warmth Calibration

    Transform count into experience language with appropriate warmth.
    """
    count = len(moments)

    if count == 0:
        # Warmth: Celebrate the good news
        return (
            "Great news! You don't have any PRs that have been waiting more than "
            f"{context.stale_threshold_days} days. Everything in GitHub is moving along."
        )

    elif count == 1:
        # Warmth: Gentle single-item attention
        moment = moments[0]
        return (
            f"I notice one PR that's been waiting a while: {moment.narrative()}. "
            "Might be time to check in or close it."
        )

    elif count <= 3:
        # Warmth: Moderate multi-item attention
        return (
            f"I found {count} PRs in GitHub that have been open for more than "
            f"{context.stale_threshold_days} days. They might need a nudge or closure:"
        )

    else:
        # Warmth: Higher urgency for many items
        return (
            f"There are {count} PRs in GitHub that have been waiting a while "
            f"(more than {context.stale_threshold_days} days). This might be a good time "
            "to review what's active and what can be closed:"
        )


def _extract_staleness_patterns(moments: List[PRMoment]) -> Optional[str]:
    """
    Extract learning from staleness patterns (for composting/memory).
    """
    if not moments:
        return None

    # Simple pattern: identify if one author has multiple stale PRs
    author_counts = {}
    for moment in moments:
        author_name = moment.author.name
        author_counts[author_name] = author_counts.get(author_name, 0) + 1

    multi_stale_authors = [name for name, count in author_counts.items() if count > 1]

    if multi_stale_authors:
        return (
            f"Pattern noticed: {', '.join(multi_stale_authors)} has multiple stale PRs. "
            "Might indicate bandwidth constraints or review bottleneck."
        )

    return "No significant patterns in staleness yet."


def _create_honest_failure_result(
    context: StalePRsContext,
    situation: Situation
) -> StalePRsResult:
    """
    Pattern-054: Honest Failure with Suggestion

    GitHub not accessible - provide honest acknowledgment with suggestion.
    """
    return StalePRsResult(
        success=False,
        framing=(
            "I'd love to check for stale PRs in GitHub, but I can't reach it right now. "
            "This might mean GitHub isn't configured yet, or there's a temporary connection issue. "
            "\n\n"
            "To enable GitHub integration, add your GITHUB_TOKEN to your environment "
            "or configure it in PIPER.user.md. Once configured, I can track PRs across time."
        ),
        stale_moments=[],
        situation=situation,
        lens_applied=["Temporal"],
        learning="GitHub Place not accessible during query"
    )


# Integration point: Route handler calls this
async def handle_stale_prs_intent(
    intent: Intent,
    user: EntityProtocol,
    github_place: PlaceProtocol,
    workflow_id: str
) -> IntentProcessingResult:
    """
    Route handler adapter (connects to existing IntentService).

    This is where the old flattened handler would call.
    Now it builds Context and calls grammar-conscious function.
    """
    # Build Context
    context = StalePRsContext(
        user=user,
        github_place=github_place,
        stale_threshold_days=7
    )

    # Perceive with grammar
    result = await perceive_stale_prs(context)

    # Transform to IntentProcessingResult (existing interface)
    return IntentProcessingResult(
        success=result.success,
        message=_format_message_for_user(result),
        intent_data={
            "category": intent.category.value,
            "action": intent.action,
            "stale_moments": [
                {
                    "title": m.title,
                    "author": m.author.name,
                    "age_days": m.age_days,
                    "narrative": m.narrative(),
                    "url": m.url
                }
                for m in result.stale_moments
            ],
            "count": len(result.stale_moments),
            "learning": result.learning,
            "lens_applied": result.lens_applied,
        },
        workflow_id=workflow_id,
        implemented=True
    )


def _format_message_for_user(result: StalePRsResult) -> str:
    """
    Format final message for user.
    Combines framing with moment narratives.
    """
    parts = [result.framing]

    if result.stale_moments:
        parts.append("")  # Blank line
        for moment in result.stale_moments:
            parts.append(f"  • {moment.narrative()} - [View PR]({moment.url})")

        if result.learning:
            parts.append("")
            parts.append(f"💡 {result.learning}")

    return "\n".join(parts)
```

---

### Improvements in Transformed Version

#### 1. **Entity Consciousness** ✅
- **Before**: Authors were just `login` strings
- **After**: Authors are `EntityProtocol` instances with identity and agency
- **Impact**: "Jordan is waiting for review" (not just "user: jordan_123")

#### 2. **Moment Significance** ✅
- **Before**: PRs were data items with timestamps
- **After**: PRs are `MomentProtocol` instances with `captures()` method
- **Impact**: Each PR is a scene with policy/process/people/outcomes

#### 3. **Place Atmosphere** ✅
- **Before**: GitHub referenced only as data source
- **After**: GitHub is a `PlaceProtocol` with atmosphere ("technical review space")
- **Impact**: Place character affects presentation

#### 4. **Lens Application** ✅
- **Before**: Temporal lens implicit, others missing
- **After**: Explicit TemporalLens, CollaborativeLens, FlowLens
- **Impact**: Multi-dimensional perception, not just filtering

#### 5. **Situation Framing** ✅
- **Before**: Ad-hoc warmth, no tension or learning
- **After**: Situation with tension ("Old work needs attention") and learning extraction
- **Impact**: Context shapes response; wisdom captured for memory

#### 6. **Pattern Application** ✅
- **Pattern-050**: `StalePRsContext` and `StalePRsResult` preserve grammar
- **Pattern-052**: `_frame_stale_prs_with_warmth()` adds personality systematically
- **Pattern-053**: Warmth calibrated to count (0, 1, 2-3, 4+)
- **Pattern-054**: `_create_honest_failure_result()` for graceful degradation

#### 7. **Language Transformation** ✅

| Aspect | Before (Flattened) | After (Grammar-Applied) |
|--------|-------------------|------------------------|
| Framing | "I found X stale PR(s)" | "I notice PRs that have been waiting a while" |
| Items | "#{number}: {title} ({age} days old)" | "'{title}' by {author} from a couple weeks ago" |
| People | "by {login}" | "{author.name} is waiting for review" |
| Errors | "I ran into a problem" | "I can't reach GitHub right now. Here's what you can do..." |
| Success | "Great news!" | "Great news! Everything in GitHub is moving along." |

---

### Lessons Learned from This Transformation

#### 1. **Protocols Enable Consciousness**
Converting data dictionaries to protocol-conforming dataclasses forced us to think about:
- What IS a PR? (A Moment in the collaboration)
- Who IS an author? (An Entity with agency)
- What IS GitHub? (A Place with technical atmosphere)

#### 2. **Lenses Reveal Multiple Perspectives**
Explicitly applying Temporal/Collaborative/Flow lenses surfaced questions:
- When was this created? (Temporal)
- Who's waiting? (Collaborative)
- What's the status? (Flow)

Without lenses, we only saw "age in days."

#### 3. **Context/Result Pair Prevents Identity Loss**
Pattern-050 (Context Dataclass Pair) ensured:
- User entity preserved from input to output
- Place identity maintained throughout
- Situation context available for framing

Before: User was implicit, Place was a config string.

#### 4. **Warmth Calibration Requires Observation**
Pattern-053 forced us to ask: "What level of warmth matches this observation?"
- 0 stale PRs → Celebrate
- 1 stale PR → Gentle nudge
- 2-3 stale PRs → Moderate attention
- 4+ stale PRs → Higher urgency

Before: Generic "I found X" regardless of significance.

#### 5. **Learning Extraction Enables Memory**
Adding `_extract_staleness_patterns()` captured wisdom:
- "Multiple stale PRs from same author" → Bandwidth constraint pattern
- This learning can be composted into long-term memory
- Future queries can reference past patterns

Before: No learning captured; each query was isolated.

#### 6. **Honest Failure Preserves Relationship**
Pattern-054 transformed error handling from:
- "Error: connection timeout" (mechanical)
- To: "I can't reach GitHub right now, but here's what you can do..." (collaborative)

Failures became moments in the relationship, not exceptions.

---

### Migration Strategy for Existing Code

If you're transforming an existing flattened feature (like the stale PRs example):

#### Step 1: Create Protocol-Conforming Types (Pattern-050)
- Define Context dataclass (input)
- Define Result dataclass (output)
- Define Moment/Entity/Place types if needed

#### Step 2: Extract Business Logic
- Move from route handler into pure function
- Function signature: `async def perceive_X(context: XContext) -> XResult`
- Keep route handler as thin adapter

#### Step 3: Apply Lenses Explicitly
- Identify which lenses apply (Temporal? Collaborative? Flow?)
- Use lens objects to perceive Place
- Document which lenses in Result

#### Step 4: Add Personality Bridge (Pattern-052)
- Create `_frame_X_with_warmth()` function
- Transform counts/data into narrative language
- Use Situation context to shape framing

#### Step 5: Calibrate Warmth (Pattern-053)
- Define thresholds (0, 1, few, many)
- Match warmth to significance
- Test with real data to verify tone

#### Step 6: Handle Failures Honestly (Pattern-054)
- Replace try/catch with explicit failure result
- Provide explanation and suggestion
- Use past observations if Place unavailable

#### Step 7: Extract Learning
- Add learning extraction function
- Identify patterns in observations
- Return learning in Result for memory/composting

#### Step 8: Integrate with Existing Code
- Keep existing IntentProcessingResult interface
- Route handler adapts Context → Result → IntentProcessingResult
- Gradual migration: both versions can coexist

---

## Verification Checklist

Before declaring transformation complete:

### Grammar Elements
- [ ] All entities identified and tracked (not just IDs)
- [ ] Moments have significance framing (not just timestamps)
- [ ] Places have atmosphere acknowledgment (not just config)
- [ ] At least one lens explicitly applied
- [ ] Situation frames the interaction with tension/learning

### Pattern Application
- [ ] Pattern-050 used if multi-layer (Context/Result pair)
- [ ] Pattern-051 used if multi-source (Parallel Place Gathering)
- [ ] Pattern-052 used if user-facing (Personality Bridge)
- [ ] Pattern-053 used if varying context (Warmth Calibration)
- [ ] Pattern-054 used for all failure paths (Honest Failure)

### Language Quality
- [ ] Can describe with "Piper noticed/remembers/anticipates..." (not "Query returned...")
- [ ] Uses narrative language ("a couple weeks ago" not "14 days")
- [ ] People have names (not just IDs)
- [ ] Places have character ("over in GitHub" not "source: github")
- [ ] Failures are honest and helpful (not just error codes)

### Experience Test
- [ ] Read result aloud - does it sound collaborative?
- [ ] Replace "Piper" with colleague's name - still natural?
- [ ] Failure message helpful to non-technical user?
- [ ] Response feels warm but not sycophantic?
- [ ] Learning extracted that could inform future interactions?

---

## Related Documentation

- **Feature-Object Model Map**: `docs/internal/architecture/current/feature-object-model-map.md` - Per-feature mapping of Entities/Moments/Places with canonical queries
- **MUX Implementation Guide**: `docs/internal/development/mux-implementation-guide.md`
- **Experience Tests**: `docs/internal/development/mux-experience-tests.md`
- **Grammar Application Patterns**: `docs/internal/architecture/patterns/grammar-application-patterns.md`
- **Grammar Compliance Audit**: `docs/internal/architecture/current/grammar-compliance-audit.md`
- **Pattern-050**: Context Dataclass Pair
- **Pattern-051**: Parallel Place Gathering
- **Pattern-052**: Personality Bridge
- **Pattern-053**: Warmth Calibration
- **Pattern-054**: Honest Failure with Suggestion

---

## Quick Start Checklist

When starting a transformation:

1. [ ] Read the existing code thoroughly
2. [ ] Identify Entity/Moment/Place elements
3. [ ] Map applicable lenses
4. [ ] Choose patterns from catalog
5. [ ] Create Context/Result dataclasses (Pattern-050)
6. [ ] Extract business logic into pure function
7. [ ] Add personality bridge (Pattern-052)
8. [ ] Handle failures honestly (Pattern-054)
9. [ ] Run experience test (can describe with "Piper noticed..."?)
10. [ ] Verify all checklist items above

---

*Part of Issue #404 MUX-VISION-GRAMMAR-CORE Phase 3*
*Created: 2026-01-20*
*Author: Claude Code (Sonnet)*
