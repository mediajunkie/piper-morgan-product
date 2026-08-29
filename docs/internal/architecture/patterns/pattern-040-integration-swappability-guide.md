# Pattern-040: Integration Swappability Guide

## Status

**Proven** | Emerging | Experimental | Deprecated

## Context

Enterprise customers often have standardized toolchains and don't want to change their issue tracker, chat platform, or other tools just to use a new product. This creates several challenges:

- **Vendor lock-in**: Forcing customers onto specific tools (GitHub, Slack) limits market reach
- **Migration barriers**: "We can't switch from Jira to GitHub" blocks adoption
- **Enterprise requirements**: Large companies standardize on MS-SQL, Teams, JIRA, etc.
- **Risk diversification**: Dependency on single providers (OpenAI) creates business risk
- **Cost optimization**: Ability to switch providers based on pricing/performance

Traditional approaches either:
1. **Hard-code integrations**: Direct API calls scattered throughout codebase (unmaintainable)
2. **Support everything**: Build N×M integrations for every combination (impossible to maintain)

This pattern enables **plug-and-play integration swapping** with manageable complexity.

### Architectural Principle

Ted Nadeau's insight: **"Many-to-One-to-Many Pattern"**

```
Business Logic (many call sites)
       ↓
Integration Router (one abstraction)  ← Swap happens here
       ↓
External API / MCP Adapter (many providers)
```

Change provider by swapping the router implementation, not changing business logic.

## Pattern Description

The **Integration Swappability Pattern** uses a Router layer to abstract external integrations. Business logic depends on the Router interface, not specific provider implementations. This enables swapping providers (GitHub ↔ Jira, Slack ↔ Teams, OpenAI ↔ Gemini) by changing configuration or dependency injection, not code.

### Core Concept

**Router Layer** = Abstract interface + pluggable implementations

```python
# Business logic depends on interface
class IssueRouter(ABC):
    @abstractmethod
    async def create_issue(self, title: str, body: str) -> Issue:
        pass

# Implementations are swappable
class GitHubRouter(IssueRouter):
    async def create_issue(self, title: str, body: str) -> Issue:
        # GitHub-specific implementation
        pass

class JiraRouter(IssueRouter):
    async def create_issue(self, title: str, body: str) -> Issue:
        # Jira-specific implementation
        pass

# Business logic uses router, doesn't care which
router: IssueRouter = get_configured_router()  # GitHub or Jira
issue = await router.create_issue("Bug report", "Details...")
```

### Key Components

1. **Router Interface**: Abstract base class defining operations
2. **Provider Implementations**: Concrete routers for each external service
3. **Configuration**: Which router to use (env var, DB setting)
4. **Dependency Injection**: Business logic receives router via DI
5. **Common Domain Model**: Router returns provider-agnostic models

## Implementation

### Structure

```
services/integrations/
├── base_router.py          # Abstract router interface
├── github/
│   ├── github_router.py    # GitHub implementation
│   └── mcp_adapter.py      # MCP protocol adapter
├── jira/
│   ├── jira_router.py      # Jira implementation
│   └── rest_adapter.py     # REST API adapter
└── factory.py              # Router factory (config-based)
```

### Code Example

```python
# services/integrations/base_router.py
from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class Issue:
    """Provider-agnostic issue model."""
    id: str
    title: str
    body: str
    url: str
    status: str

class IssueTrackerRouter(ABC):
    """Abstract router for issue tracker integrations."""

    @abstractmethod
    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> Issue:
        """Create issue in tracker. Returns provider-agnostic Issue."""
        pass

    @abstractmethod
    async def get_issue(self, issue_id: str) -> Optional[Issue]:
        """Retrieve issue by ID."""
        pass

    @abstractmethod
    async def update_issue(self, issue_id: str, **updates) -> Issue:
        """Update issue with new data."""
        pass

# services/integrations/github/github_router.py
class GitHubIssueRouter(IssueTrackerRouter):
    """GitHub implementation of issue tracker router."""

    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client

    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> Issue:
        # Use MCP protocol to create GitHub issue
        gh_issue = await self.mcp.issues.create(
            title=title,
            body=body,
            labels=labels or []
        )

        # Convert to provider-agnostic model
        return Issue(
            id=gh_issue["node_id"],
            title=gh_issue["title"],
            body=gh_issue["body"],
            url=gh_issue["html_url"],
            status=gh_issue["state"]
        )

# services/integrations/jira/jira_router.py
class JiraIssueRouter(IssueTrackerRouter):
    """Jira implementation of issue tracker router."""

    def __init__(self, jira_client: JiraRESTClient):
        self.jira = jira_client

    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> Issue:
        # Use Jira REST API
        jira_issue = await self.jira.create(
            project="PM",
            issue_type="Task",
            summary=title,
            description=body,
            labels=labels or []
        )

        # Convert to provider-agnostic model
        return Issue(
            id=jira_issue["key"],
            title=jira_issue["fields"]["summary"],
            body=jira_issue["fields"]["description"],
            url=jira_issue["self"],
            status=jira_issue["fields"]["status"]["name"]
        )

# services/integrations/factory.py
def get_issue_tracker_router() -> IssueTrackerRouter:
    """Factory: Returns configured issue tracker router."""
    tracker_type = os.getenv("ISSUE_TRACKER", "github")

    if tracker_type == "github":
        mcp_client = get_mcp_client("github")
        return GitHubIssueRouter(mcp_client)
    elif tracker_type == "jira":
        jira_client = get_jira_client()
        return JiraIssueRouter(jira_client)
    else:
        raise ValueError(f"Unsupported tracker: {tracker_type}")

# Business logic (services/intent_service/handlers.py)
async def handle_create_issue(title: str, body: str):
    """Business logic doesn't know about GitHub or Jira."""
    router = get_issue_tracker_router()  # Gets GitHub or Jira
    issue = await router.create_issue(title, body)
    return {"issue_id": issue.id, "url": issue.url}
```

### Configuration

```yaml
# .env or config file
ISSUE_TRACKER=github  # or jira, linear, gitlab

# GitHub config (if using GitHub)
GITHUB_TOKEN=ghp_...
GITHUB_REPO=owner/repo

# Jira config (if using Jira)
JIRA_URL=https://company.atlassian.net
JIRA_TOKEN=...
JIRA_PROJECT=PM
```

## Usage Guidelines

### When to Use

- **External service integrations**: Any integration with 3rd party APIs
- **Enterprise requirements**: Customers need specific tool support
- **Multi-provider strategy**: Want to support GitHub + Jira + Linear
- **Risk diversification**: Don't want lock-in to single LLM provider
- **Cost optimization**: Swap providers based on pricing
- **Testing**: Swap real APIs for mock routers in tests

### When NOT to Use

- **Internal services**: Don't need router layer between your own services
- **Single provider forever**: If you'll never support alternatives (rare!)
- **Trivial integrations**: If it's one API call in one place, just call it
- **Over-abstraction**: Don't abstract "just in case" - wait for 2nd provider

### Best Practices

1. **Provider-agnostic models**: Return common domain models, not provider-specific
2. **Graceful degradation**: If provider is down, degrade gracefully (Pattern-007)
3. **Feature parity matrix**: Document which features work on which providers
4. **Integration tests**: Test each router implementation thoroughly
5. **Migration guides**: Document switching from Provider A to Provider B
6. **Monitoring**: Track which provider is in use, error rates per provider
7. **Fallback chains**: `primary_router → fallback_router` for resilience

### Common Pitfalls

- **Leaky abstractions**: Provider-specific details leak through router interface
- **Lowest common denominator**: Only supporting features all providers have
- **Performance overhead**: Router adds latency if not careful
- **Complex error handling**: Different providers fail differently
- **Configuration sprawl**: Need configs for all possible providers

## Examples in Codebase

### Primary Usage

**Issue Trackers**:
- `services/integrations/github/github_router.py` - GitHub implementation (currently active)
- Future: `services/integrations/jira/jira_router.py` (when enterprise customers need it)
- Future: `services/integrations/linear/linear_router.py` (when requested)

**Chat Platforms**:
- `services/integrations/slack/slack_router.py` - Slack implementation (currently active)
- Future: `services/integrations/teams/teams_router.py` (for Microsoft shops)
- Future: `services/integrations/discord/discord_router.py` (for developer communities)

**LLM Providers**:
- `services/llm/clients.py` - Abstraction exists
- Supports: Anthropic (primary), OpenAI (fallback)
- Future: Gemini, Cohere, local models

**Calendar**:
- `services/integrations/calendar/` - MCP adapter pattern
- Future: Outlook, iCal support

**Docs/Wiki**:
- `services/integrations/notion/notion_router.py` - Notion implementation
- Future: Confluence, Google Docs

### Swappability Matrix

| Integration | Current | Alternatives Ready | Effort to Add | Enterprise Value |
|-------------|---------|-------------------|---------------|------------------|
| Issue Tracker | GitHub | Jira, Linear, GitLab | Medium | High |
| Chat | Slack | Teams, Discord | Medium | High |
| LLM | Anthropic/OpenAI | Gemini, Cohere, local | Low-Medium | Medium |
| Calendar | Google | Outlook, iCal | Medium | Medium |
| Docs | Notion | Confluence, Google Docs | Medium | Medium |
| Database | PostgreSQL | MS-SQL, MySQL | High | Medium |

### Test Examples

```python
# tests/unit/services/integrations/test_issue_routers.py
class MockIssueRouter(IssueTrackerRouter):
    """Mock router for testing without real API calls."""

    async def create_issue(self, title: str, body: str, labels=None):
        return Issue(
            id="mock-123",
            title=title,
            body=body,
            url="https://mock.example.com/issue/123",
            status="open"
        )

# Test business logic with mock router
@pytest.mark.asyncio
async def test_create_issue_handler_with_mock():
    router = MockIssueRouter()
    issue = await router.create_issue("Test", "Body")
    assert issue.id == "mock-123"
    assert issue.title == "Test"
```

## Related Patterns

### Complements

- **Pattern-013: Router Pattern** - This is the core router pattern
- **Pattern-007: Graceful Degradation** - Router handles provider failures gracefully
- **ADR-038: MCP Integration Pattern** - How routers use MCP protocol

### Alternatives

- **Direct API calls**: Simpler, but creates vendor lock-in
- **Adapter Pattern**: Similar, but adapter wraps existing interface (router defines new one)
- **Strategy Pattern**: Similar, but strategy is algorithm choice (router is provider choice)

### Dependencies

- **MCP Protocol** (for integrations that support it)
- **Dependency Injection** (to inject routers into business logic)

## Migration Notes

### From Direct API Calls

**Before** (tightly coupled):
```python
# Business logic directly calls GitHub API
gh_client = GitHubClient(token)
issue = gh_client.create_issue(title, body)
# Now locked to GitHub!
```

**After** (swappable):
```python
# Business logic uses router
router = get_issue_tracker_router()  # Config determines GitHub/Jira
issue = await router.create_issue(title, body)
# Can swap to Jira by changing config!
```

### From Ted Nadeau Architecture Review (Nov 20, 2025)

Ted's insight:
> "External library calls should go through abstraction layers (many-to-one-to-many pattern)"
> "Example: GitHub API abstraction enables swapping to Jira, monitoring, metering"

This pattern **implements exactly what Ted described**. Our Router pattern is his many-to-one-to-many pattern:
- Many call sites → One router interface → Many provider implementations

**Ted's validation**: "You're describing what we already built!" (Router pattern)

## References

### Documentation

- **ADR-013**: MCP + Spatial Intelligence Integration Pattern
- **ADR-038**: Three Integration Abstraction Patterns
- **Pattern-013**: Router Pattern (core architectural pattern)
- **Research source**: `dev/2025/11/20/ted-nadeau-follow-up-research.md` (Section 3)

### External References

- **Gang of Four**: Adapter Pattern, Strategy Pattern
- **Martin Fowler**: Gateway Pattern, Service Stub
- **Enterprise Integration Patterns**: Content-Based Router

### Usage Analysis

- **Created**: November 20, 2025
- **Current usage**: GitHub, Slack, Notion, Calendar integrations
- **Proven pattern**: In production since early 2025
- **Maintenance**: Active
- **Validation**: External review by Ted Nadeau (experienced architect)

### Feature Parity Matrix

Document which features work on each provider:

| Feature | GitHub | Jira | Linear | Notes |
|---------|--------|------|--------|-------|
| Create issue | ✅ | 🔜 | 🔜 | Core functionality |
| Add comment | ✅ | 🔜 | 🔜 | |
| Update status | ✅ | 🔜 | 🔜 | |
| Assign user | ✅ | 🔜 | 🔜 | User mapping needed |
| Attach files | ✅ | 🔜 | 🔜 | |
| Link issues | ✅ | 🔜 | 🔜 | |
| Custom fields | ❌ | 🔜 | 🔜 | Jira-specific |
| Spatial intelligence | ✅ | ❌ | ❌ | Piper-specific |

Legend: ✅ Implemented | 🔜 Planned | ❌ Not supported

---

**Pattern created**: November 20, 2025
**Author**: Code Agent (Research Session)
**Inspired by**: Ted Nadeau's inter-operability questions
**Status**: Proven (already in production)
**Validated by**: Ted Nadeau (external architecture review)
