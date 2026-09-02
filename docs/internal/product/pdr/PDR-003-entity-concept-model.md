# PDR-003: Entity Concept Model — Product, Project, Repository

**Status**: DRAFT
**Authors**: PPM, CXO
**Date**: February 26, 2026
**Supersedes**: None
**Related**: ADR-045 (Object Model), PDR-001 (FTUX), PDR-002 (Conversational Glue)

---

## Summary

This PDR defines the concept model for three core entities — **Product**, **Project**, and **Repository** — establishing their meanings, relationships, and UX surfacing strategy. The goal is to align domain model, database schema, and user mental models into a coherent whole.

---

## Problem Statement

### Current State

1. **Repository is not a first-class entity.** It exists only as a config field inside `ProjectIntegration`, requiring a project_id FK. This prevents:
   - Connecting a repo without having a project
   - Sharing a repo across multiple projects
   - Managing repos independently

2. **Product and Project have confused identity.** The codebase has both entities but:
   - `Project` extends `Product` in some places (inheritance)
   - No explicit relationship between them (no FK, no join table)
   - Unclear which concept users interact with

3. **User mental models are simpler than our architecture.** Most users think:
   - "The thing I'm building" (product)
   - "The work I'm doing" (project)
   - "Where the code lives" (repo)

### Impact

- Users can't connect repos to multiple projects (common in monorepo setups)
- No path to portfolio management (multiple products)
- Onboarding asks about "projects" but users think about "products"
- Technical debt accumulates as workarounds proliferate

---

## Concept Definitions

### Product

**Definition**: The thing you're building and shipping. The whole. What users/customers experience.

**User's mental model**:
- "My product is Piper Morgan"
- "My product is the mobile app"
- "My products are the iOS app and the Android app"

**Typical PM questions about a Product**:
- What's the vision?
- Who are the users?
- What's the roadmap?
- How is it doing in the market?

**Domain characteristics**:
- Has vision, strategy, roadmap
- Has stakeholders (users, customers, internal teams)
- May have multiple Projects contributing to it
- Persists across project boundaries

### Project

**Definition**: A bounded effort with intent. A workstream, a release, a feature initiative, an epic.

**User's mental model**:
- "The Q1 release"
- "The authentication overhaul"
- "The mobile redesign project"

**Typical PM questions about a Project**:
- What's the scope?
- What's the timeline?
- Who's working on it?
- What's blocking?

**Domain characteristics**:
- Has scope, timeline, deliverables
- Has team/contributors
- May involve multiple Repositories
- Has a lifecycle (active → complete → archived)

### Repository

**Definition**: Where code lives. A technical artifact that may or may not map 1:1 to products or projects.

**User's mental model**:
- "The frontend repo"
- "The monorepo"
- "The shared components library"

**Typical PM questions about a Repository**:
- What's changed recently?
- Are there open PRs?
- What's the CI status?

**Domain characteristics**:
- Has URL, branch, provider (GitHub, GitLab, etc.)
- May serve multiple Projects
- May be shared across Products
- Independent lifecycle from Projects

---

## Relationship Model

### Product ↔ Project: Many-to-Many

| Scenario | Example |
|----------|---------|
| One product, one project | Solo PM: "Piper Morgan" with "Current Work" |
| One product, many projects | "Piper Morgan" with M0, M1, Website, Content |
| Many products, one project | Platform work serving iOS and Android products |
| Many products, many projects | Enterprise portfolio |

**Implementation**: `product_projects` join table

```
products
  ├── id
  ├── name
  ├── vision
  └── ...

product_projects (join table)
  ├── product_id (FK)
  └── project_id (FK)

projects
  ├── id
  ├── name
  ├── description
  └── ...
```

### Project ↔ Repository: Many-to-Many

| Scenario | Example |
|----------|---------|
| One project, one repo | Website project uses website repo |
| One project, many repos | M0 touches platform and web repos |
| Many projects, one repo | Monorepo serves all projects |
| Many projects, many repos | Microservices architecture |

**Implementation**: `project_repositories` join table

```
projects
  ├── id
  └── ...

project_repositories (join table)
  ├── project_id (FK)
  └── repository_id (FK)

repositories (NEW first-class entity)
  ├── id
  ├── name
  ├── url
  ├── provider (github, gitlab, etc.)
  ├── default_branch
  ├── owner_id (FK to users)
  └── ...
```

### Product ↔ Repository: Derived

Products don't directly own repositories. The relationship is derived through Projects:

```
Product → Projects → Repositories
```

This matches user mental models: "Which repos are part of my product?" = "Which repos do my product's projects use?"

---

## UX Surfacing Strategy

### Principle: Progressive Disclosure

Most users have simple relationships. Don't force complexity upfront.

### Phase 1: MVP (Current + Repository First-Class)

**Changes**:
- Repository becomes first-class entity
- Setup flow: "Connect a repository" (independent of project)
- Project view: "Repos" section showing linked repos
- Settings: Full repo management

**User experience**:
- Connect repos during or after project setup
- Link repos to projects (optional, defaults to current project)
- View all repos in settings

**What's NOT surfaced**: Product concept remains hidden

### Phase 2: Settings-Based Product Management (M1/M2)

**Changes**:
- Settings page for creating/editing Products
- Link Projects to Products in settings
- Product selector in nav (only if user has multiple)

**User experience**:
- Power users can organize projects into products
- Optional — solo PMs never need to touch it
- No onboarding changes

### Phase 3: Conversational Product Emergence (Later)

**Changes**:
- Piper observes patterns and suggests groupings
- "You have 3 projects that seem related — want me to group them as a product?"

**User experience**:
- Products emerge from use, not upfront definition
- Piper as colleague noticing organizational opportunities
- Validates concept through acceptance rate

### Phase 4: Onboarding Integration (If Data Warrants)

**Changes**:
- Onboarding asks "Are you working on one product or several?" (only if data shows it helps)
- Portfolio-first flow for enterprise users

**User experience**:
- Only implemented if Phases 2-3 show strong adoption
- May never happen for consumer/prosumer audience

---

## Domain Model Changes

### New Entity: Repository

```python
@dataclass
class Repository:
    """A code repository — first-class entity"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    url: str = ""
    provider: str = "github"  # github, gitlab, bitbucket
    default_branch: str = "main"
    owner_id: str = ""  # User who connected it
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Derived/cached fields
    last_synced_at: Optional[datetime] = None

    # Relationships
    projects: List["Project"] = field(default_factory=list)
```

### Updated Entity: Project

```python
@dataclass
class Project:
    """A PM project — bounded effort with intent"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    owner_id: str = ""
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    products: List["Product"] = field(default_factory=list)  # NEW
    repositories: List["Repository"] = field(default_factory=list)  # NEW
    integrations: List["ProjectIntegration"] = field(default_factory=list)
```

### Updated Entity: Product

```python
@dataclass
class Product:
    """A product being managed — the thing you ship"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    owner_id: str = ""  # NEW
    is_default: bool = False  # NEW
    is_archived: bool = False  # NEW
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    projects: List["Project"] = field(default_factory=list)  # NEW
    features: List["Feature"] = field(default_factory=list)
    stakeholders: List["Stakeholder"] = field(default_factory=list)
    metrics: List["Metric"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)
```

### Deprecated: Project extends Product

The current inheritance (`class Project(Product)`) should be removed. Project and Product are distinct concepts with a many-to-many relationship, not an inheritance hierarchy.

---

## Migration Strategy

### Phase 1: Repository (Immediate)

1. Create `repositories` table
2. Create `project_repositories` join table
3. Migrate existing `ProjectIntegration` GitHub configs to Repository entities
4. Update setup/settings UI
5. Deprecate repo-related fields in ProjectIntegration

### Phase 2: Product-Project Relationship (Near-term)

1. Create `product_projects` join table
2. Add `owner_id`, `is_default`, `is_archived` to Product
3. Remove `Project extends Product` inheritance
4. No UI changes yet — backend only

### Phase 3: Settings UI (M1/M2)

1. Add Product management to settings
2. Add Product selector to nav (conditional)
3. Update project views to show Product association

---

## Test Case: Piper Morgan

Applying this model to our own usage:

| Entity | Instance |
|--------|----------|
| **Product** | Piper Morgan |
| **Projects** | M0, M1, Website, Content/Newsletter, Alpha Program |
| **Repositories** | piper-morgan-platform, piper-morgan-web, pipermorgan.ai |

**Relationships**:
- Product "Piper Morgan" → all 5 Projects
- Project "M0" → repos: platform, web
- Project "M1" → repos: platform, web
- Project "Website" → repos: web, pipermorgan.ai
- Project "Content" → repos: (none — no code)
- Repo "platform" → projects: M0, M1, Alpha (many-to-many)

This confirms the model handles real-world complexity.

---

## Open Questions

### 1. Product Inheritance

Should Products have parent/child relationships (product hierarchy)?

**Current position**: No. Keep it flat for MVP. Hierarchy adds complexity without clear user demand.

### 2. Repository Ownership vs. Project Ownership

If a repo is shared across projects with different owners, who "owns" the repo?

**Current position**: The user who connected it owns it. Project-level permissions are separate from repo ownership.

### 3. Integration Migration

What happens to existing `ProjectIntegration` records with GitHub configs?

**Current position**: Migrate to Repository entities. Keep ProjectIntegration for non-repo integrations (Slack, Calendar, etc.).

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Repo connection success rate | >90% | Setup completion analytics |
| Multi-project repo usage | >20% of repos | Join table cardinality |
| Product feature adoption | >10% of users (Phase 2+) | Settings page usage |
| Piper product suggestions accepted | >50% (Phase 3+) | Suggestion acceptance rate |

---

## References

- [CXO Memo: Domain Model Response (Feb 26, 2026)](../../../../mailboxes/lead/read/memo-cxo-to-ppm-lead-xian-domain-model-response-2026-02-26.md) *(path corrected 2026-09-02 — filename had drifted; this is the real memo, addressed to PPM/Lead/xian)*
- PPM Memo: Domain Model Synthesis (Feb 26, 2026) *(dead link removed 2026-09-02 — no file at this or any other path; a synthesis memo may never have been written)*
- [Lead Developer Memo: Domain Model Gaps (Feb 26, 2026)](../../../../mailboxes/cxo/read/2026-02-26-domain-model-product-project-repo-relationships.md) *(path corrected 2026-09-02 — file exists in mailboxes/, not alongside this PDR)*
- [ADR-045: Object Model](../../architecture/adrs/adr-045-object-model.md)
- [domain-models.md](../../architecture/current/models/domain-models.md) — requires update per this PDR

---

*PDR-003 v1.0 — February 26, 2026*
