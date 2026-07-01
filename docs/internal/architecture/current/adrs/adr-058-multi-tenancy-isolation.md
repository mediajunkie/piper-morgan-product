# ADR-058: Multi-Tenancy Isolation Architecture

**Status**: APPROVED
**Date**: 2026-01-30
**Authors**: Lead Developer (Claude Code)
**Approved By**: Chief Architect (2026-01-30)
**Issue**: #734
**Deciders**: Chief Architect, PM

## Context

### Problem Statement

Investigation of alpha testing bug #734 revealed that **multi-tenancy isolation was never fully implemented**. User A's data leaks to User B because:

1. **OAuth tokens stored globally** - All users share same calendar/Slack/GitHub tokens
2. **OAuth state lacks user identity** - Callbacks can't identify initiating user
3. **RequestContext migration incomplete** - `user_id` often optional, not enforced
4. **Repository filtering optional** - `owner_id` parameter defaults to None (no filtering)
5. **Singleton managers use wrong key** - Keyed by `session_id` (ephemeral) not `user_id` (persistent)
6. **Config services are user-agnostic** - Return global credentials for all users

**Evidence**: Full audit in `dev/2026/01/30/734-multi-tenancy-audit-report.md`

### Strategic Context

This is not a bug fix but a **foundational architectural refactor** that:
- Blocks multi-user alpha testing (users see each other's data)
- Enables proper multi-tenant operation
- Prepares architecture for future workspace/team features

### Relationship to ADR-051

ADR-051 (RequestContext Pattern) established the identity model. This ADR extends it to cover:
- How that identity flows through all layers
- How credentials are isolated by user
- How data access is scoped by user

## Decision

### Core Principle

**"Break loudly now" over gradual migration**. In alpha, it's better to fail fast than leak data silently.

### 1. Credential Separation (Bounded Contexts)

**App credentials** and **user tokens** are different bounded contexts:

| Type | Examples | Storage | Service |
|------|----------|---------|---------|
| App credentials | client_id, client_secret | System config | `IntegrationConfigService` |
| User tokens | access_token, refresh_token | User-scoped | `UserAPIKeyService` |

**Implementation**:
- `IntegrationConfigService` - Read-only access to app credentials (no user scoping)
- `UserAPIKeyService` - User-scoped token storage with mandatory `user_id`

### 2. RequestContext Enforcement

**Boundary enforcement**: Routes are the trust boundary where user identity is established.

**Pattern**:
- Middleware/dependency ensures RequestContext exists for all authenticated routes
- Services receive RequestContext as **required** parameter
- Services that are user-agnostic don't need it
- Background tasks use `JobContext` pattern

**Anti-pattern avoided**: "None-checking everywhere"

### 3. OAuth State Design

**Embed user_id in OAuth state** so callbacks can identify the initiating user:

```python
# On OAuth initiation (route must be authenticated)
state = {
    "user_id": current_user.id,
    "return_url": "/settings/integrations",
    "nonce": generate_secure_nonce()
}
encoded_state = base64url_encode(json.dumps(state))

# On callback
decoded_state = json.loads(base64url_decode(state_param))
user_id = decoded_state["user_id"]
# Verify nonce, then store token for user_id
```

### 4. Repository Isolation

**Make `owner_id` required** - This is a "forcing function" that reveals all hidden gaps:

```python
# Before (broken)
async def get_all(self, owner_id: Optional[str] = None):
    if owner_id:
        query = query.filter(owner_id=owner_id)
    # If None, returns ALL data across ALL users

# After (correct)
async def get_all(self, owner_id: str):
    if not owner_id:
        raise ValueError("owner_id is required")
    query = query.filter(owner_id=owner_id)
```

**Second dimension**: Add `workspace_id` for future multi-tenant (users within workspaces):

```python
@dataclass
class TenantContext:
    owner_id: str
    workspace_id: str = "default"
```

### 5. Singleton Manager Keying

**Key by `user_id`** (not `session_id`):

| Concept | Granularity | Use As Key? |
|---------|-------------|-------------|
| `session_id` | Browser tab (ephemeral) | NO |
| `user_id` | User account (persistent) | YES |

```python
# Before (broken)
self._sessions: Dict[str, OnboardingSession] = {}  # keyed by session_id

# After (correct)
self._sessions: Dict[str, OnboardingSession] = {}  # keyed by user_id
```

### 6. Config Service Signatures

**Pass user context to methods** (keep singletons):

```python
# Before (broken)
config_service.get_calendar_token()  # Returns global token

# After (correct)
config_service.get_user_calendar_token(user_id: str)  # Returns user's token
```

### 7. Background Task Context

Different webhook types need different approaches:

| Webhook Type | User Identification |
|--------------|---------------------|
| User-initiated (Slack message) | Extract from webhook payload, lookup internal user |
| System (GitHub push) | Use "connector user" stored at integration setup |

**JobContext pattern** for background tasks:
```python
@dataclass
class JobContext:
    user_id: str
    workspace_id: str
    created_at: datetime
    # Captured at job creation, restored at execution
```

### 8. Error Handling

**Don't reveal resource existence** to unauthorized users:
- "Not found" for: resource doesn't exist
- "Not found" for: resource exists but belongs to another user
- Never "not authorized" which confirms existence

## Implementation Sequence

| Phase | Work | Rationale |
|-------|------|-----------|
| 1 | ADR-058 creation | Document decisions first |
| 2 | OAuth state investigation | Audit existing before designing |
| 3 | RequestContext enforcement | Foundation for all other work |
| 4 | Repository isolation (owner_id required) | "Forcing function" reveals all gaps |
| 5 | OAuth state redesign | Repos now fail without owner_id |
| 6 | Credential storage separation | App vs user services |
| 7 | Config service signatures | Pass user context to methods |
| 8 | Singleton manager refactor | Key by user_id |
| 9 | workspace_id activation | Last - needs all above |

**Parallelization**: Phases 4+5 can run in parallel. Phases 6+7 can run in parallel.

## Implementation Status

- **Identity unification (#1233 / RECONNECT-WS9, closed 2026-06):** the single-identity model — one human principal owning many connector identities (GitHub / Slack / Calendar / Notion) — is unified and in place. A user's connector credentials key to their single principal `user_id`: the `owner_id` on repositories (§4 Repository Isolation) and the `{user_id}_{provider}_api_key` username scoping on user-scoped keychain entries (§1 Credential Separation). This realizes the "one human, many connector identities" boundary this ADR calls for, and closed the identity half of the RECONNECT connector refactor. (Recorded per #1316.)

## Alternatives Considered

### Alternative A: Incremental Fix

Fix only the specific bug (#734 calendar tokens) without broader refactor.

**Pros**: Quick, minimal scope
**Cons**: Doesn't fix root cause, other integrations still leak

**Decision**: Rejected - PM approved "do it right, timeline not a constraint"

### Alternative B: Global Token Mode

Keep global tokens, add flag for "single-tenant mode" vs "multi-tenant mode".

**Pros**: No migration, simple
**Cons**: Tech debt, won't scale, alpha users already multi-tenant

**Decision**: Rejected - alpha is multi-tenant by necessity

### Alternative C: Workspace-First Isolation

Start with workspace isolation, derive user isolation from that.

**Pros**: Future-proof
**Cons**: More complex, workspaces not in current roadmap

**Decision**: Rejected - user isolation first, workspace later

## Consequences

### Positive

- User A's data never visible to User B
- Clear separation of app vs user credentials
- Foundation for workspace/team features
- Fail-fast behavior catches bugs early
- Cleaner domain model with explicit boundaries

### Negative

- Significant refactoring effort (mitigated by alpha phase)
- All routes/services need context updates
- Existing global tokens become inaccessible (users re-authenticate)
- Tests need updates

### Risks

- Incomplete migration leaves dual patterns (mitigated by compressed timeline)
- OAuth flow breaks during transition (mitigated by TDD approach)

## Testing Strategy

### Cross-User Isolation Tests

```python
async def test_user_a_data_not_visible_to_user_b():
    # User A creates data
    list_a = await repo.create(owner_id="user_a", name="A's List")

    # User B queries
    lists_b = await repo.get_all(owner_id="user_b")

    # User A's data NOT in User B's results
    assert list_a.id not in [l.id for l in lists_b]
```

### Token Isolation Tests

```python
async def test_user_a_token_not_accessible_to_user_b():
    # Store token for User A
    await user_api_key_service.store_user_key(
        user_id="user_a", provider="google_calendar", key="token_a"
    )

    # User B retrieves
    token = await user_api_key_service.get_user_key(
        user_id="user_b", provider="google_calendar"
    )

    # Should be None, not User A's token
    assert token is None
```

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| No direct keychain in routes | `grep -r "keychain" web/api/routes/` returns empty |
| Repositories require owner_id | `grep -r "owner_id: Optional" services/repositories/` returns empty |
| OAuth state has user_id | Tests + manual OAuth flow verification |
| Config services accept user_id | All methods have user_id parameter |
| Cross-user isolation | All isolation tests pass |

## Workspace ID Implementation

### Default Workspace

For single-tenant deployments, a `DEFAULT_WORKSPACE_ID` constant is defined:

```python
# services/domain/models.py
DEFAULT_WORKSPACE_ID = UUID("00000000-0000-0000-0000-000000000000")
```

This ensures:
1. `RequestContext.workspace_id` is **never None** after construction
2. Single-tenant deployments work without explicit workspace configuration
3. Future multi-tenant deployments can override with real workspace UUIDs

### RequestContext Factory

The `from_jwt_and_request` factory method now uses the default:

```python
workspace = (
    UUID(claims.workspace_id)
    if claims.workspace_id
    else DEFAULT_WORKSPACE_ID
)
```

### Future Work

When workspace/team features are implemented:
1. Add `workspace_id` column to database tables
2. Update repository queries to filter by `workspace_id`
3. Add workspace management UI
4. Update JWT token generation to include workspace_id for multi-tenant users

## References

- Issue #734 - Multi-Tenancy Isolation bug
- Issue #724 - LLM keys (same root cause, duplicate)
- ADR-051 - RequestContext Pattern (foundation)
- Chief Architect Memo - `mailboxes/lead/read/memo-arch-to-lead-multitenancy-guidance-2026-01-30.md`
- Audit Report - `dev/2026/01/30/734-multi-tenancy-audit-report.md`

---

_ADR created: 2026-01-30_
_Status: APPROVED by Chief Architect (2026-01-30)_
_Implementation: Issue #734 gameplan v2_
_Phase 9 (workspace_id): Completed 2026-01-30_
