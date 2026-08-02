> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# Entity Relationship Diagram

**Last Updated**: January 22, 2026
**Status**: Current
**Source Files**: `services/domain/models.py`, `services/domain/primitives.py`, `services/database/models.py`

## Overview

This document provides visual representations of Piper Morgan's domain entity relationships. It serves as a reference for understanding how core entities relate to each other.

---

## Core Domain Entities

### High-Level Entity Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER DOMAIN                                     │
│                                                                             │
│    ┌──────────┐                                                             │
│    │   User   │──────────────────────────────────────────┐                  │
│    └────┬─────┘                                          │                  │
│         │ owns                                           │ owns             │
│         ▼                                                ▼                  │
│    ┌──────────┐      associated       ┌──────────┐  ┌──────────┐           │
│    │ Project  │◄─────────────────────►│   List   │  │   Todo   │           │
│    └────┬─────┘      (many:many)      └────┬─────┘  └────┬─────┘           │
│         │                                  │              │                 │
│         │ contains                         │ contains     │ member of       │
│         ▼                                  ▼              │                 │
│    ┌──────────────┐                   ┌──────────┐       │                 │
│    │ Integration  │                   │   Item   │◄──────┘                 │
│    └──────────────┘                   └──────────┘                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Relationships

### User Ownership

```
User
 │
 ├──owns──► Project (one-to-many)
 │           └── ProjectIntegration (one-to-many)
 │
 ├──owns──► List (one-to-many)
 │           └── Item/Todo (one-to-many via list_id)
 │
 ├──owns──► Todo (one-to-many, direct ownership)
 │
 ├──owns──► UploadedFile (one-to-many)
 │
 └──has──► Session (one-to-many)
```

### List/Item Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    LIST/ITEM TYPE HIERARCHY                      │
│                                                                  │
│    ┌──────────────────────────────────────────────────────────┐ │
│    │                        Item                               │ │
│    │  (services/domain/primitives.py)                         │ │
│    │                                                          │ │
│    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│    │  │     id      │  │    text     │  │  position   │      │ │
│    │  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│    │  ┌─────────────┐                                        │ │
│    │  │   list_id   │ ─────────────────────────────────┐     │ │
│    │  └─────────────┘                                  │     │ │
│    └───────────────────────────┬──────────────────────┼─────┘ │
│                                │ extends              │       │
│                                ▼                      │       │
│    ┌──────────────────────────────────────────────┐  │       │
│    │                     Todo                      │  │       │
│    │  (services/domain/models.py)                 │  │       │
│    │                                              │  │       │
│    │  + description    + status      + priority   │  │       │
│    │  + completed      + due_date    + project_id │  │       │
│    │  + external_refs  (boundary object pattern)  │  │       │
│    └──────────────────────────────────────────────┘  │       │
│                                                      │       │
│    ┌──────────────────────────────────────────────┐  │       │
│    │                     List                      │◄─┘       │
│    │  (services/domain/models.py)                 │          │
│    │                                              │          │
│    │  + name           + item_type   + list_type  │          │
│    │  + is_default     + project_ids (many:many)  │          │
│    │  + owner_id       + shared_with              │          │
│    └──────────────────────────────────────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Project Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT RELATIONSHIPS                         │
│                                                                  │
│    ┌──────────────┐                                             │
│    │   Project    │                                             │
│    │              │                                             │
│    │  + id        │                                             │
│    │  + owner_id  │──────────────────────────► User             │
│    │  + name      │                                             │
│    │              │                                             │
│    └──────┬───────┘                                             │
│           │                                                     │
│           │ contains                    associated (many:many)  │
│           ▼                                   │                 │
│    ┌──────────────────┐              ┌───────┴───────┐         │
│    │ ProjectIntegration│              │     List      │         │
│    │                  │              │               │         │
│    │  + type (GitHub, │              │ project_ids[] │─────────┤
│    │    Slack, etc.)  │              │               │         │
│    │  + config        │              └───────────────┘         │
│    │  + is_active     │                                        │
│    └──────────────────┘                                        │
│                                                                │
│    Association via List.project_ids (JSONB array)             │
│    - List can belong to 0, 1, or many Projects                │
│    - Project can have 0, 1, or many Lists                     │
│    - Lists can exist independently (personal lists)           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## MUX Ownership Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUX OWNERSHIP MODEL                           │
│                                                                  │
│    OwnershipCategory (Enum)                                     │
│    ┌────────────┬────────────┬────────────┐                    │
│    │   NATIVE   │ FEDERATED  │ SYNTHETIC  │                    │
│    │            │            │            │                    │
│    │  "Mind"    │  "Senses"  │"Understanding"                  │
│    │            │            │            │                    │
│    │ Created by │ Observed   │ Inferred   │                    │
│    │   Piper    │ externally │ by Piper   │                    │
│    └────────────┴────────────┴────────────┘                    │
│                                                                  │
│    OwnershipMetadata (Embeddable)                               │
│    ┌──────────────────────────────────────────────────────────┐│
│    │  category: OwnershipCategory                              ││
│    │  source: str                                              ││
│    │  confidence: float (1.0 native, 0.9 federated, 0.7 synth) ││
│    │  can_modify: bool                                         ││
│    │  derived_from: List[str]                                  ││
│    │  transformation_chain: List[str]                          ││
│    └──────────────────────────────────────────────────────────┘│
│                                                                  │
│    Entities with OwnershipMetadata:                             │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│    │  Project │ │   Todo   │ │  Session │ │ WorkItem │        │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Schema Summary

### Core Tables

| Table | Primary Key | Foreign Keys | Indexes |
|-------|-------------|--------------|---------|
| `users` | `id` (UUID) | - | email, username |
| `projects` | `id` (String) | `owner_id` → users | owner_id |
| `lists` | `id` (String) | `owner_id` → users | owner_type, owner_archived, shared (GIN), tags (GIN), **projects (GIN)** |
| `items` | `id` (String) | `list_id` → lists | list_id, position |
| `todos` | `id` (String) | `list_id` → lists, `owner_id` → users | owner_status, list_id, due_date |
| `list_items` | `id` (String) | `list_id` → lists | list_id, item_id, position |

### Key Relationship Patterns

1. **Ownership**: Most entities have `owner_id` → users FK
2. **Sharing**: `shared_with` JSONB array for role-based access
3. **Many-to-Many**: Implemented via JSONB arrays with GIN indexes
   - `List.project_ids` (List ↔ Project)
   - `List.shared_with` (List ↔ User sharing)
4. **Polymorphism**: `item_type` discriminator on List and ListItem

---

## Integration Points

### External System Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEDERATION PATTERN                            │
│                                                                  │
│    External System              Piper Domain                    │
│    ───────────────              ────────────                    │
│                                                                  │
│    ┌─────────────┐              ┌─────────────────────────────┐│
│    │   GitHub    │              │           Todo              ││
│    │   Issue     │─────────────►│  external_refs: {           ││
│    └─────────────┘              │    "source": "github",      ││
│                                 │    "external_id": "123",    ││
│    ┌─────────────┐              │    "repo": "owner/repo",    ││
│    │   Asana     │─────────────►│    "sync_status": "synced"  ││
│    │   Task      │              │  }                          ││
│    └─────────────┘              └─────────────────────────────┘│
│                                                                  │
│    ┌─────────────┐              ┌─────────────────────────────┐│
│    │   Trello    │              │           List              ││
│    │   Board     │─────────────►│  (federated list sync)      ││
│    └─────────────┘              └─────────────────────────────┘│
│                                                                  │
│    Boundary Object Pattern:                                     │
│    - Same domain model for native and federated                │
│    - external_refs tracks provenance                           │
│    - Enables uniform queries across sources                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

### Cardinality Summary

| Relationship | Cardinality | Implementation |
|--------------|-------------|----------------|
| User → Project | 1:N | FK: projects.owner_id |
| User → List | 1:N | FK: lists.owner_id |
| User → Todo | 1:N | FK: todos.owner_id |
| Project ↔ List | M:N | JSONB: lists.project_ids |
| List → Item | 1:N | FK: items.list_id |
| List → Todo | 1:N | FK: todos.list_id |
| Project → Integration | 1:N | FK: integrations.project_id |

### Model Location Reference

| Model | File | Line |
|-------|------|------|
| Item | `services/domain/primitives.py` | 21 |
| List | `services/domain/models.py` | ~1015 |
| Todo | `services/domain/models.py` | ~1135 |
| Project | `services/domain/models.py` | ~303 |
| OwnershipMetadata | `services/mux/ownership.py` | - |

---

*This document replaces the archived `dependency-diagrams.md` and reflects the current (January 2026) architecture.*
