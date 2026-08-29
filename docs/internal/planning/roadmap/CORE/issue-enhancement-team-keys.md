# CORE-KEYS-TEAM-SHARING: Team API Key Sharing (Enterprise)

## Context

Enterprise teams need to share API keys across team members while maintaining security, access control, and audit trails. Currently, each user must provide their own keys, creating management overhead and potential security issues.

**Parent Issue**: #228 (API Key Management)
**Target**: Enterprise customers (post-Alpha/Beta)

---

## Problem Statement

**Current State**:
- Each user stores their own individual keys
- No key sharing mechanism
- Teams duplicate API costs (each member has their own OpenAI key)
- No centralized key management
- No role-based access control

**Enterprise Pain Points**:
- **Cost**: Each team member pays for their own OpenAI/Anthropic access
- **Management**: IT must provision keys for each user individually
- **Security**: No way to revoke access for departed team members
- **Compliance**: No audit trail for key usage
- **Control**: No way to limit which services team members can access

---

## Proposed Solution

### 1. Team/Organization Model
```python
class Organization(Base):
    """Enterprise organization"""
    __tablename__ = "organizations"

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)
    plan = Column(String(50))  # free, team, enterprise
    created_at = Column(DateTime)

    # Relationships
    teams = relationship("Team", back_populates="organization")
    members = relationship("OrganizationMember", back_populates="organization")
    shared_keys = relationship("SharedAPIKey", back_populates="organization")

class Team(Base):
    """Team within organization"""
    __tablename__ = "teams"

    id = Column(UUID, primary_key=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Relationships
    members = relationship("TeamMember", back_populates="team")
    shared_keys = relationship("TeamAPIKey", back_populates="team")

class SharedAPIKey(Base):
    """Shared API key at organization level"""
    __tablename__ = "shared_api_keys"

    id = Column(UUID, primary_key=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    provider = Column(String(50), nullable=False)
    encrypted_key_ref = Column(String(255), nullable=False)

    # Access control
    access_level = Column(String(50))  # organization, team, user
    allowed_teams = Column(ARRAY(UUID))  # If team-level access
    allowed_users = Column(ARRAY(UUID))  # If user-level access

    # Metadata
    created_by = Column(UUID, ForeignKey("users.id"))
    created_at = Column(DateTime)
    rotated_at = Column(DateTime)

    # Usage limits
    monthly_limit = Column(Integer)  # Optional cost cap
    daily_limit = Column(Integer)

    UNIQUE(organization_id, provider)
```

### 2. Access Control
```python
class KeyAccessPolicy:
    """Control who can access shared keys"""

    async def can_user_access_key(
        self,
        user_id: str,
        shared_key: SharedAPIKey
    ) -> bool:
        """Check if user can access shared key"""

        # Check organization membership
        if not await self._is_org_member(user_id, shared_key.organization_id):
            return False

        # Organization-wide key
        if shared_key.access_level == "organization":
            return True

        # Team-specific key
        if shared_key.access_level == "team":
            user_teams = await self._get_user_teams(user_id)
            return any(team.id in shared_key.allowed_teams for team in user_teams)

        # User-specific key
        if shared_key.access_level == "user":
            return user_id in shared_key.allowed_users

        return False

class KeyPermissions:
    """Define what users can do with shared keys"""

    READ = "read"        # Use key for API calls
    ROTATE = "rotate"    # Rotate the key
    MANAGE = "manage"    # Edit access policies
    REVOKE = "revoke"    # Remove key

    async def get_user_permissions(
        self,
        user_id: str,
        shared_key: SharedAPIKey
    ) -> Set[str]:
        """Get user's permissions for key"""

        role = await self._get_user_role(user_id, shared_key.organization_id)

        if role == "owner":
            return {self.READ, self.ROTATE, self.MANAGE, self.REVOKE}
        elif role == "admin":
            return {self.READ, self.ROTATE, self.MANAGE}
        elif role == "member":
            return {self.READ}
        else:
            return set()
```

### 3. Key Resolution Strategy
```python
class KeyResolver:
    """Determine which key to use for a request"""

    async def resolve_key(
        self,
        user_id: str,
        provider: str
    ) -> str:
        """Get API key for user (personal or shared)"""

        # 1. Check for user's personal key (highest priority)
        personal_key = await user_api_key_service.retrieve_user_key(
            user_id, provider
        )
        if personal_key:
            return personal_key

        # 2. Check for team shared key
        user_teams = await self._get_user_teams(user_id)
        for team in user_teams:
            team_key = await self._get_team_key(team.id, provider)
            if team_key and await self._can_access(user_id, team_key):
                return team_key.decrypt()

        # 3. Check for organization shared key
        user_org = await self._get_user_organization(user_id)
        if user_org:
            org_key = await self._get_org_key(user_org.id, provider)
            if org_key and await self._can_access(user_id, org_key):
                return org_key.decrypt()

        # 4. No key available
        raise NoAPIKeyError(
            f"No {provider} API key available. "
            f"Add a personal key or ask your organization admin."
        )
```

### 4. Usage Tracking & Limits
```python
class SharedKeyUsageTracker:
    """Track usage of shared keys"""

    async def record_usage(
        self,
        shared_key_id: UUID,
        user_id: str,
        provider: str,
        cost: float,
        tokens_used: int
    ):
        """Record key usage"""
        # For audit trail and cost allocation

    async def check_limits(
        self,
        shared_key_id: UUID
    ) -> LimitStatus:
        """Check if usage limits exceeded"""
        usage = await self._get_monthly_usage(shared_key_id)
        key = await self._get_key(shared_key_id)

        if key.monthly_limit and usage.cost >= key.monthly_limit:
            return LimitStatus(
                exceeded=True,
                message=f"Monthly limit of ${key.monthly_limit} exceeded"
            )

        return LimitStatus(exceeded=False)
```

---

## Implementation Phases

### Phase 1: Organization Model (6 hours)
- Create organization/team tables
- Add organization membership
- Add role-based access control
- Migration for existing single-user data

### Phase 2: Shared Key Storage (4 hours)
- SharedAPIKey model
- Keychain storage for shared keys
- Access control enforcement
- Key resolution strategy

### Phase 3: Usage Tracking (4 hours)
- Usage logging (per user, per key)
- Cost allocation
- Limit enforcement
- Usage dashboards

### Phase 4: Management UI (6 hours)
- Organization management
- Team management
- Key sharing UI
- Access control UI
- Usage reports

### Phase 5: Audit & Compliance (4 hours)
- Audit trail for all key access
- Compliance reports
- Access reviews
- Security alerts

---

## Acceptance Criteria

### Core Functionality
- [ ] Organizations can create shared API keys
- [ ] Teams can access organization/team keys
- [ ] Users inherit key access from team membership
- [ ] Personal keys take priority over shared keys
- [ ] Access control enforced at all levels

### Access Control
- [ ] Role-based permissions (owner, admin, member)
- [ ] Team-based access restrictions
- [ ] User-specific access grants
- [ ] Key rotation by authorized users only
- [ ] Audit trail for all access

### Usage Management
- [ ] Track usage per user per key
- [ ] Cost allocation per user/team
- [ ] Monthly/daily usage limits
- [ ] Alerts when limits approached
- [ ] Usage dashboards

### User Experience
- [ ] Clear indication of key source (personal vs shared)
- [ ] Easy key sharing workflow
- [ ] Intuitive access control UI
- [ ] Helpful error messages
- [ ] Usage visibility for users

---

## Technical Design

### Key Resolution Flow
```
User makes request requiring API key
           ↓
1. Check personal key
   └─ If found → Use it (highest priority)
           ↓
2. Check team keys
   ├─ Get user's teams
   ├─ For each team, check for provider key
   ├─ Check user has access to team key
   └─ If found → Use first matching key
           ↓
3. Check organization key
   ├─ Get user's organization
   ├─ Check for organization key for provider
   ├─ Check user has access to org key
   └─ If found → Use it
           ↓
4. No key found
   └─ Raise NoAPIKeyError with helpful message
```

### Access Control Matrix
```
Role      | Read | Rotate | Manage | Revoke
----------|------|--------|--------|--------
Owner     |  ✓   |   ✓    |   ✓    |   ✓
Admin     |  ✓   |   ✓    |   ✓    |   ✗
Member    |  ✓   |   ✗    |   ✗    |   ✗
Guest     |  ✗   |   ✗    |   ✗    |   ✗
```

### Database Schema
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE teams (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE organization_members (
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    role VARCHAR(50) NOT NULL,  -- owner, admin, member
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, organization_id)
);

CREATE TABLE shared_api_keys (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    provider VARCHAR(50) NOT NULL,
    encrypted_key_ref VARCHAR(255) NOT NULL,
    access_level VARCHAR(50) NOT NULL,
    allowed_teams UUID[],
    allowed_users UUID[],
    created_by UUID REFERENCES users(id),
    monthly_limit INTEGER,
    created_at TIMESTAMP NOT NULL,
    rotated_at TIMESTAMP,
    UNIQUE (organization_id, provider)
);

CREATE TABLE key_usage_logs (
    id UUID PRIMARY KEY,
    shared_key_id UUID REFERENCES shared_api_keys(id),
    user_id UUID REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    cost DECIMAL(10, 4),
    tokens_used INTEGER,
    created_at TIMESTAMP NOT NULL
);
```

---

## Example User Flows

### Flow 1: Organization Admin Adds Shared Key
```bash
$ piper org keys add openai --org acme-corp

Enter OpenAI API key: sk-proj-...
Validating key... ✓

Key sharing options:
1. Organization-wide (all members)
2. Specific teams
3. Specific users

Choice: 1

Monthly spending limit (optional): $500
Daily limit (optional): $50

Success! OpenAI key added for Acme Corp
- Access: All organization members
- Monthly limit: $500
- Daily limit: $50

123 members now have access to this key.
```

### Flow 2: User Uses Shared Key
```bash
$ piper chat "Explain quantum computing"

Using API key:
- Provider: OpenAI (gpt-4)
- Source: Acme Corp shared key
- Your usage today: $2.34 / $50 daily limit
- Org usage this month: $234.56 / $500 monthly limit

[Response from GPT-4...]
```

### Flow 3: Usage Dashboard
```bash
$ piper org usage --month current

Acme Corp - API Usage (October 2025)

OpenAI (gpt-4):
- Total cost: $342.15 / $500 limit
- Total requests: 1,234
- Active users: 23 / 123 members

Top users:
1. alice@acme.com: $45.23 (13%)
2. bob@acme.com: $38.91 (11%)
3. charlie@acme.com: $29.44 (9%)

Anthropic (claude-3-opus):
- Total cost: $128.33 / $300 limit
- Total requests: 456
- Active users: 12 / 123 members

Recommendations:
→ Consider increasing OpenAI monthly limit
→ 100 members haven't used API keys this month
```

---

## Success Metrics

### Cost Efficiency
- **Target**: 50% reduction in per-user API costs
- **Measure**: Average cost per user before/after
- **Success**: Teams report significant savings

### Management Overhead
- **Target**: 80% reduction in key management time
- **Measure**: Time spent provisioning/revoking keys
- **Success**: IT teams report time savings

### Security
- **Target**: 100% audit trail coverage
- **Measure**: All key access logged
- **Success**: No access without audit record

### Adoption
- **Target**: 75% of enterprise teams use shared keys
- **Measure**: Teams with at least one shared key
- **Success**: >75% adoption within 90 days

---

## Pricing Implications

### Current Model (Personal Keys)
```
Cost per User: $20-50/month (they pay directly)
Piper Revenue: $0 from API costs
```

### Proposed Model (Shared Keys)
```
Option 1: Cost Pass-Through
- Organization pays API costs
- Piper Revenue: $0 from API costs
- Value: Management & visibility

Option 2: Managed Service
- Piper pays API costs
- Charge organization: API cost + 20% margin
- Piper Revenue: 20% of API spend
- Value: Consolidated billing

Option 3: Hybrid
- Organization provides keys (free)
- OR Piper provides keys (cost + margin)
- Piper Revenue: Optional managed service
```

---

## Dependencies

**Required**:
- ✅ #228: API Key Management (personal keys infrastructure)
- ❌ Organization/team models (new)
- ❌ Role-based access control (new)
- ❌ Usage tracking infrastructure (new)

**Optional**:
- #249: Audit logging (key access tracking)
- Billing system (for managed service model)
- SSO integration (enterprise auth)

---

## Time Estimate

**Total**: 24 hours (~3 days)

**Breakdown**:
- Organization model: 6 hours
- Shared key storage: 4 hours
- Usage tracking: 4 hours
- Management UI: 6 hours
- Audit & compliance: 4 hours

---

## Priority

**Priority**: Low (enterprise feature, post-Beta)
**Milestone**: Production (1.0)
**Sprint**: TBD (after Alpha and Beta)

**Rationale**: Enterprise feature needed for production but not for Alpha/Beta. Individual users can use personal keys. Add after core product validated.

---

## Related Issues

- #228: API Key Management (parent - provides foundation)
- #249: Audit Logging (key usage tracking)
- Future: SSO integration (enterprise auth)
- Future: Billing system (managed keys revenue)

**Epic**: CORE-USERS (Multi-user & Security)
**Labels**: enhancement, enterprise, component: security, priority: low, milestone: 1.0
