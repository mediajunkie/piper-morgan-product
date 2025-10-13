# Prompt for Code Agent: GREAT-4C Phase 1 - Spatial Intelligence Integration

## Context

Phase 0 complete: Hardcoded user context removed, multi-user support operational.

**Next priority**: Integrate spatial intelligence patterns into the 5 canonical handlers per ADR requirements.

## Session Log

Continue: `dev/2025/10/05/2025-10-05-2020-prog-code-log.md` (or create new for Oct 6)

## Mission

Apply spatial intelligence patterns from ADRs to canonical handlers, ensuring architectural compliance and appropriate response granularity.

---

## Phase 1: Spatial Intelligence Integration

### Step 1: Review Spatial Intelligence ADRs

Search for spatial intelligence documentation:

```bash
# Find spatial intelligence ADRs
find docs -name "*spatial*" -type f

# Search for spatial patterns in ADRs
grep -r "spatial" docs/internal/architecture --include="*.md" | head -20

# Check if spatial context already exists in Intent
grep -r "spatial_context" services/intent_service/ --include="*.py"
```

**Expected to find**: Spatial patterns like GRANULAR, EMBEDDED, CONSOLIDATED, etc.

### Step 2: Understand Current Spatial Support

The classifier already accepts `spatial_context`:

```python
# In classifier.py (already exists)
async def classify(
    self,
    text: str,
    context: Optional[Dict] = None,
    session: Optional[Any] = None,
    spatial_context: Optional[Dict] = None,  # Already supported!
):
```

**Your task**: Make handlers USE this spatial context to adjust response detail.

### Step 3: Add Spatial Pattern Handling to Handlers

Edit: `services/intent_service/canonical_handlers.py`

Add spatial awareness to each handler:

```python
async def _handle_status_query(self, intent: Intent, session_id: str) -> Dict:
    """Handle 'What am I working on?' with spatial awareness."""

    # Get user context
    user_context = await user_context_service.get_user_context(session_id)

    # Get spatial context from intent
    spatial_pattern = None
    if hasattr(intent, 'spatial_context') and intent.spatial_context:
        spatial_pattern = intent.spatial_context.get('pattern')

    # Load projects from PIPER.md
    projects = user_context.projects

    # Adjust response detail based on spatial pattern
    if spatial_pattern == "GRANULAR":
        # Detailed status with all projects
        response = self._format_detailed_status(projects)
    elif spatial_pattern == "EMBEDDED":
        # Consolidated status, key highlights only
        response = self._format_consolidated_status(projects)
    else:
        # Default: moderate detail
        response = self._format_standard_status(projects)

    return {
        "message": response,
        "spatial_pattern": spatial_pattern,
        "intent": {
            "category": IntentCategoryEnum.STATUS.value,
            "action": "provide_status",
            "confidence": 1.0
        }
    }

def _format_detailed_status(self, projects: list) -> str:
    """GRANULAR: Full project details."""
    if not projects:
        return "No active projects configured."

    details = ["Here's your detailed project status:\n"]
    for project in projects:
        details.append(f"\n**{project}**:")
        details.append("  - Status: [from PIPER.md]")
        details.append("  - Next steps: [from PIPER.md]")
        details.append("  - Blockers: [from PIPER.md]")

    return "\n".join(details)

def _format_consolidated_status(self, projects: list) -> str:
    """EMBEDDED: Brief overview."""
    if not projects:
        return "No active projects."

    return f"Working on {len(projects)} projects: {', '.join(projects[:3])}"

def _format_standard_status(self, projects: list) -> str:
    """DEFAULT: Moderate detail."""
    if not projects:
        return "No active projects configured in your PIPER.md."

    summary = [f"You're working on {len(projects)} active projects:\n"]
    for project in projects[:5]:  # Top 5
        summary.append(f"- {project}")

    if len(projects) > 5:
        summary.append(f"... and {len(projects) - 5} more")

    return "\n".join(summary)
```

### Step 4: Apply to All 5 Handlers

Apply spatial pattern to:

1. **_handle_status_query** ✅ (example above)
2. **_handle_priority_query** - Adjust priority detail level
3. **_handle_temporal_query** - Adjust calendar detail level
4. **_handle_guidance_query** - Adjust guidance specificity
5. **_handle_identity_query** - Minimal adjustment (identity is fixed)

**Pattern for each**:
```python
# 1. Extract spatial pattern
spatial_pattern = intent.spatial_context.get('pattern') if intent.spatial_context else None

# 2. Branch on pattern
if spatial_pattern == "GRANULAR":
    return detailed_response
elif spatial_pattern == "EMBEDDED":
    return brief_response
else:
    return standard_response
```

### Step 5: Test Spatial Intelligence

Create: `dev/2025/10/06/test_spatial_intelligence.py`

```python
"""Test spatial intelligence in handlers."""
import asyncio
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.classifier import Intent

async def test_spatial_patterns():
    """Test different spatial patterns produce different detail levels."""

    handlers = CanonicalHandlers()

    # Test STATUS query with different patterns
    base_intent = Intent(
        text="What am I working on?",
        category="STATUS",
        action="provide_status",
        confidence=1.0
    )

    print("=== Testing Spatial Intelligence ===\n")

    # Test GRANULAR (detailed)
    granular_intent = Intent(
        text=base_intent.text,
        category=base_intent.category,
        action=base_intent.action,
        confidence=base_intent.confidence,
        spatial_context={"pattern": "GRANULAR"}
    )
    granular_response = await handlers._handle_status_query(granular_intent, "test_session")
    print("GRANULAR Pattern (detailed):")
    print(granular_response["message"])
    print(f"\nLength: {len(granular_response['message'])} chars\n")

    # Test EMBEDDED (brief)
    embedded_intent = Intent(
        text=base_intent.text,
        category=base_intent.category,
        action=base_intent.action,
        confidence=base_intent.confidence,
        spatial_context={"pattern": "EMBEDDED"}
    )
    embedded_response = await handlers._handle_status_query(embedded_intent, "test_session")
    print("EMBEDDED Pattern (brief):")
    print(embedded_response["message"])
    print(f"\nLength: {len(embedded_response['message'])} chars\n")

    # Test DEFAULT (standard)
    default_intent = Intent(
        text=base_intent.text,
        category=base_intent.category,
        action=base_intent.action,
        confidence=base_intent.confidence,
        spatial_context=None  # No spatial context
    )
    default_response = await handlers._handle_status_query(default_intent, "test_session")
    print("DEFAULT Pattern (standard):")
    print(default_response["message"])
    print(f"\nLength: {len(default_response['message'])} chars\n")

    # Validate different detail levels
    granular_len = len(granular_response["message"])
    embedded_len = len(embedded_response["message"])
    default_len = len(default_response["message"])

    assert granular_len > default_len, "GRANULAR should be more detailed than DEFAULT"
    assert embedded_len < default_len, "EMBEDDED should be briefer than DEFAULT"

    print("✅ Spatial intelligence working - detail levels adjust appropriately")

if __name__ == "__main__":
    asyncio.run(test_spatial_patterns())
```

Run test:
```bash
python3 dev/2025/10/06/test_spatial_intelligence.py
```

### Step 6: Document Spatial Patterns

Create: `dev/2025/10/06/spatial-intelligence-implementation.md`

```markdown
# Spatial Intelligence Implementation

## Overview
Canonical handlers now support spatial intelligence patterns to adjust response detail based on context.

## Supported Patterns

### GRANULAR
**Use case**: User wants comprehensive details
**Response**: Full information with all available data
**Example**: Complete project status with blockers, next steps, timeline

### EMBEDDED
**Use case**: User wants brief overview (embedded in other content)
**Response**: Minimal information, key facts only
**Example**: "Working on 3 projects: ProjectA, ProjectB, ProjectC"

### DEFAULT (no pattern)
**Use case**: Standard query without spatial context
**Response**: Moderate detail level
**Example**: List of projects with basic status

## Handler Implementation

Each handler checks for spatial context:
```python
spatial_pattern = intent.spatial_context.get('pattern') if intent.spatial_context else None

if spatial_pattern == "GRANULAR":
    return detailed_response
elif spatial_pattern == "EMBEDDED":
    return brief_response
else:
    return standard_response
```

## Handlers with Spatial Support
- ✅ _handle_status_query
- ✅ _handle_priority_query
- ✅ _handle_temporal_query
- ✅ _handle_guidance_query
- ⚠️ _handle_identity_query (minimal - identity is fixed)

## Testing
See `dev/2025/10/06/test_spatial_intelligence.py` for validation tests.
```

---

## Success Criteria

- [ ] Spatial intelligence ADRs reviewed
- [ ] All 5 handlers check for spatial_context
- [ ] GRANULAR pattern provides detailed responses
- [ ] EMBEDDED pattern provides brief responses
- [ ] DEFAULT (no pattern) provides standard responses
- [ ] Test script validates different detail levels
- [ ] Documentation complete
- [ ] Session log updated

---

## Evidence Format

```bash
$ python3 dev/2025/10/06/test_spatial_intelligence.py
=== Testing Spatial Intelligence ===

GRANULAR Pattern (detailed):
Here's your detailed project status:

**Project Alpha**:
  - Status: In progress
  - Next steps: Complete API integration
  - Blockers: None

**Project Beta**:
  - Status: Planning phase
  ...

Length: 450 chars

EMBEDDED Pattern (brief):
Working on 3 projects: Alpha, Beta, Gamma

Length: 45 chars

DEFAULT Pattern (standard):
You're working on 3 active projects:
- Project Alpha
- Project Beta
- Project Gamma

Length: 120 chars

✅ Spatial intelligence working - detail levels adjust appropriately
```

---

**Effort**: Medium (~30-45 minutes)
**Priority**: HIGH (architectural compliance)
**Complexity**: Moderate (pattern matching + response formatting)
