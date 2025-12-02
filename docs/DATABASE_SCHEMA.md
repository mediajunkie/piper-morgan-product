# Piper Morgan - Backend Database Schema (SQL DDL)

## Overview
This document contains the SQL DDL for the Piper Morgan backend database schema.
Database: PostgreSQL 15+
Port: 5433 (non-standard to avoid conflicts)

---

## Core Tables

### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(500),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    is_alpha BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
```

### user_api_keys
```sql
CREATE TABLE user_api_keys (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    key_reference VARCHAR(500) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_validated BOOLEAN DEFAULT FALSE,
    last_validated_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(255),
    previous_key_reference VARCHAR(500),
    rotated_at TIMESTAMP,
    UNIQUE(user_id, provider)
);

CREATE INDEX idx_user_api_keys_user_id ON user_api_keys(user_id);
CREATE INDEX idx_user_api_keys_provider ON user_api_keys(provider);
CREATE INDEX idx_user_api_keys_active ON user_api_keys(is_active);
```

### audit_logs
```sql
CREATE TABLE audit_logs (
    id VARCHAR(255) PRIMARY KEY,
    user_id UUID,  -- No FK constraint (intentional for data retention)
    session_id VARCHAR(255),
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    status VARCHAR(20) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    request_id VARCHAR(255),
    request_path VARCHAR(500),
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_user_date ON audit_logs(user_id, created_at);
CREATE INDEX idx_audit_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_severity ON audit_logs(severity);
CREATE INDEX idx_audit_status ON audit_logs(status);
CREATE INDEX idx_audit_ip ON audit_logs(ip_address);
CREATE INDEX idx_audit_session ON audit_logs(session_id);
CREATE INDEX idx_audit_request ON audit_logs(request_id);
```

### token_blacklist
```sql
CREATE TABLE token_blacklist (
    id SERIAL PRIMARY KEY,
    token_id VARCHAR(255) NOT NULL UNIQUE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    reason VARCHAR(50) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_token_blacklist_token_id ON token_blacklist(token_id);
CREATE INDEX idx_token_blacklist_expires ON token_blacklist(expires_at);
CREATE INDEX idx_token_blacklist_user_id ON token_blacklist(user_id);
CREATE INDEX idx_token_blacklist_user_expires ON token_blacklist(user_id, expires_at);
```

---

## Product Management Tables

### products
```sql
CREATE TABLE products (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    vision TEXT,
    strategy TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### features
```sql
CREATE TABLE features (
    id VARCHAR PRIMARY KEY,
    product_id VARCHAR REFERENCES products(id),
    name VARCHAR NOT NULL,
    description TEXT,
    hypothesis TEXT,
    acceptance_criteria JSONB,
    status VARCHAR DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### work_items
```sql
CREATE TABLE work_items (
    id VARCHAR PRIMARY KEY,
    product_id VARCHAR REFERENCES products(id),
    feature_id VARCHAR REFERENCES features(id),
    title VARCHAR NOT NULL,
    description TEXT,
    type VARCHAR,
    status VARCHAR DEFAULT 'open',
    priority VARCHAR DEFAULT 'medium',
    labels JSONB,
    assignee VARCHAR,
    project_id VARCHAR,
    source_system VARCHAR,
    external_id VARCHAR,
    external_url VARCHAR,
    item_metadata JSONB,
    external_refs JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### stakeholders
```sql
CREATE TABLE stakeholders (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    role VARCHAR,
    interests JSONB,
    influence_level INTEGER DEFAULT 1,
    satisfaction FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Workflow & Intent Tables

### intents
```sql
CREATE TABLE intents (
    id VARCHAR PRIMARY KEY,
    category VARCHAR,  -- IntentCategory enum
    action VARCHAR,
    confidence FLOAT,
    context JSONB,
    original_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    workflow_id VARCHAR REFERENCES workflows(id)
);
```

### workflows
```sql
CREATE TABLE workflows (
    id VARCHAR PRIMARY KEY,
    type VARCHAR,  -- WorkflowType enum
    status VARCHAR,  -- WorkflowStatus enum
    input_data JSONB,
    output_data JSONB,
    context JSONB,
    result JSONB,
    error TEXT,
    intent_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### tasks
```sql
CREATE TABLE tasks (
    id VARCHAR PRIMARY KEY,
    workflow_id VARCHAR REFERENCES workflows(id),
    name VARCHAR NOT NULL,
    type VARCHAR,  -- TaskType enum
    status VARCHAR,  -- TaskStatus enum
    input_data JSONB,
    output_data JSONB,
    result JSONB,
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Project Tables

### projects
```sql
CREATE TABLE projects (
    id VARCHAR PRIMARY KEY,
    owner_id VARCHAR,
    name VARCHAR NOT NULL UNIQUE,
    description TEXT,
    shared_with JSONB DEFAULT '[]',
    is_default BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### project_integrations
```sql
CREATE TABLE project_integrations (
    id VARCHAR PRIMARY KEY,
    project_id VARCHAR NOT NULL REFERENCES projects(id),
    type VARCHAR NOT NULL,  -- IntegrationType enum
    name VARCHAR NOT NULL,
    config JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## File Management

### uploaded_files
```sql
CREATE TABLE uploaded_files (
    id VARCHAR PRIMARY KEY,
    owner_id UUID NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(255),
    file_size INTEGER,
    storage_path VARCHAR(1000),
    upload_time TIMESTAMP DEFAULT NOW(),
    last_referenced TIMESTAMP,
    reference_count INTEGER DEFAULT 0,
    file_metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_files_owner ON uploaded_files(owner_id, upload_time);
CREATE INDEX idx_files_filename ON uploaded_files(filename);
```

---

## Conversation Tables

### conversations
```sql
CREATE TABLE conversations (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    session_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL DEFAULT '',
    context JSONB NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_activity_at TIMESTAMP
);

CREATE INDEX idx_conversations_user_session ON conversations(user_id, session_id);
CREATE INDEX idx_conversations_last_activity ON conversations(last_activity_at);
```

### conversation_turns
```sql
CREATE TABLE conversation_turns (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL DEFAULT 0,
    user_message TEXT NOT NULL DEFAULT '',
    assistant_response TEXT NOT NULL DEFAULT '',
    intent VARCHAR,
    entities JSONB NOT NULL DEFAULT '[]',
    references JSONB NOT NULL DEFAULT '{}',
    context_used JSONB NOT NULL DEFAULT '{}',
    metadata JSONB NOT NULL DEFAULT '{}',
    processing_time FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX idx_conversation_turns_conversation ON conversation_turns(conversation_id, turn_number);
CREATE INDEX idx_conversation_turns_created ON conversation_turns(created_at);
```

---

## Knowledge Graph Tables

### knowledge_nodes
```sql
CREATE TABLE knowledge_nodes (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    node_type VARCHAR NOT NULL,  -- NodeType enum
    description TEXT,
    node_metadata JSONB DEFAULT '{}',
    properties JSONB DEFAULT '{}',
    session_id VARCHAR,
    owner_id VARCHAR REFERENCES users(id),
    embedding_vector JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_nodes_session ON knowledge_nodes(session_id);
CREATE INDEX idx_nodes_type ON knowledge_nodes(node_type);
CREATE INDEX idx_nodes_name ON knowledge_nodes(name);
```

### knowledge_edges
```sql
CREATE TABLE knowledge_edges (
    id VARCHAR PRIMARY KEY,
    source_node_id VARCHAR NOT NULL REFERENCES knowledge_nodes(id),
    target_node_id VARCHAR NOT NULL REFERENCES knowledge_nodes(id),
    edge_type VARCHAR NOT NULL,  -- EdgeType enum
    weight FLOAT DEFAULT 1.0,
    node_metadata JSONB DEFAULT '{}',
    properties JSONB DEFAULT '{}',
    session_id VARCHAR,
    owner_id VARCHAR REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_edges_source ON knowledge_edges(source_node_id);
CREATE INDEX idx_edges_target ON knowledge_edges(target_node_id);
CREATE INDEX idx_edges_type ON knowledge_edges(edge_type);
CREATE INDEX idx_edges_session ON knowledge_edges(session_id);
CREATE INDEX idx_edges_source_target ON knowledge_edges(source_node_id, target_node_id);
```

---

## Todo & List Management (PM-081 Universal List Architecture)

### items (Base Primitive)
```sql
CREATE TABLE items (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    list_id VARCHAR,
    item_type VARCHAR(50) NOT NULL DEFAULT 'item',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_items_list_id ON items(list_id);
CREATE INDEX idx_items_item_type ON items(item_type);
CREATE INDEX idx_items_list_position ON items(list_id, position);
CREATE INDEX idx_items_created ON items(created_at);
```

### todo_items (Extends items via polymorphic inheritance)
```sql
CREATE TABLE todo_items (
    id VARCHAR PRIMARY KEY REFERENCES items(id),
    description TEXT DEFAULT '',
    status VARCHAR(11) NOT NULL DEFAULT 'pending',
    priority VARCHAR(6) NOT NULL DEFAULT 'medium',
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    parent_id VARCHAR REFERENCES todo_items(id),
    due_date TIMESTAMP,
    reminder_date TIMESTAMP,
    scheduled_date TIMESTAMP,
    tags JSONB DEFAULT '[]',
    project_id VARCHAR REFERENCES projects(id),
    context VARCHAR,
    estimated_minutes INTEGER,
    actual_minutes INTEGER,
    completion_notes TEXT DEFAULT '',
    list_metadata JSONB DEFAULT '{}',
    knowledge_node_id VARCHAR,
    related_todos JSONB DEFAULT '[]',
    creation_intent VARCHAR,
    intent_confidence FLOAT,
    external_refs JSONB DEFAULT '{}',
    completed_at TIMESTAMP,
    owner_id VARCHAR NOT NULL,
    assigned_to VARCHAR
);

CREATE INDEX idx_todos_owner_status ON todo_items(owner_id, status);
CREATE INDEX idx_todos_owner_priority ON todo_items(owner_id, priority);
CREATE INDEX idx_todos_assigned_status ON todo_items(assigned_to, status);
CREATE INDEX idx_todos_due_date ON todo_items(due_date);
CREATE INDEX idx_todos_owner_due ON todo_items(owner_id, due_date);
CREATE INDEX idx_todos_scheduled ON todo_items(scheduled_date);
CREATE INDEX idx_todos_reminder ON todo_items(reminder_date);
CREATE INDEX idx_todos_parent ON todo_items(parent_id);
CREATE INDEX idx_todos_context ON todo_items(context);
CREATE INDEX idx_todos_project ON todo_items(project_id);
CREATE INDEX idx_todos_tags ON todo_items USING gin(tags);
CREATE INDEX idx_todos_knowledge_node ON todo_items(knowledge_node_id);
CREATE INDEX idx_todos_creation_intent ON todo_items(creation_intent);
CREATE INDEX idx_todos_external_refs ON todo_items USING gin(external_refs);
```

### todo_lists (Legacy, being migrated to universal lists)
```sql
CREATE TABLE todo_lists (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT DEFAULT '',
    list_type VARCHAR NOT NULL DEFAULT 'personal',
    ordering_strategy VARCHAR NOT NULL DEFAULT 'manual',
    color VARCHAR(7),
    emoji VARCHAR(4),
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    owner_id VARCHAR NOT NULL,
    shared_with JSONB DEFAULT '[]',
    todo_count INTEGER NOT NULL DEFAULT 0,
    completed_count INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_todo_lists_owner_type ON todo_lists(owner_id, list_type);
CREATE INDEX idx_todo_lists_owner_archived ON todo_lists(owner_id, is_archived);
CREATE INDEX idx_todo_lists_shared ON todo_lists USING gin(shared_with);
CREATE INDEX idx_todo_lists_default ON todo_lists(owner_id, is_default);
CREATE INDEX idx_todo_lists_tags ON todo_lists USING gin(tags);
```

### lists (Universal List Architecture)
```sql
CREATE TABLE lists (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT DEFAULT '',
    item_type VARCHAR NOT NULL DEFAULT 'todo',
    list_type VARCHAR NOT NULL DEFAULT 'personal',
    ordering_strategy VARCHAR NOT NULL DEFAULT 'manual',
    color VARCHAR(7),
    emoji VARCHAR(4),
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    owner_id VARCHAR NOT NULL,
    shared_with JSONB DEFAULT '[]',
    item_count INTEGER NOT NULL DEFAULT 0,
    completed_count INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_lists_owner_type ON lists(owner_id, item_type);
CREATE INDEX idx_lists_owner_list_type ON lists(owner_id, list_type);
CREATE INDEX idx_lists_owner_archived ON lists(owner_id, is_archived);
CREATE INDEX idx_lists_shared ON lists USING gin(shared_with);
CREATE INDEX idx_lists_default ON lists(owner_id, item_type, is_default);
CREATE INDEX idx_lists_tags ON lists USING gin(tags);
```

### list_items (Universal list membership)
```sql
CREATE TABLE list_items (
    id VARCHAR PRIMARY KEY,
    list_id VARCHAR NOT NULL REFERENCES lists(id),
    item_id VARCHAR NOT NULL,
    item_type VARCHAR NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    added_at TIMESTAMP NOT NULL DEFAULT NOW(),
    added_by VARCHAR NOT NULL,
    list_priority VARCHAR,
    list_due_date TIMESTAMP,
    list_notes TEXT DEFAULT ''
);

CREATE INDEX idx_list_items_list_id ON list_items(list_id);
CREATE INDEX idx_list_items_item_id_type ON list_items(item_id, item_type);
CREATE INDEX idx_list_items_position ON list_items(list_id, position);
CREATE INDEX idx_list_items_added_by ON list_items(added_by);
```

### list_memberships (Legacy todo-list bridge)
```sql
CREATE TABLE list_memberships (
    id VARCHAR PRIMARY KEY,
    list_id VARCHAR NOT NULL REFERENCES todo_lists(id),
    todo_id VARCHAR NOT NULL REFERENCES todo_items(id),
    position INTEGER NOT NULL DEFAULT 0,
    added_at TIMESTAMP NOT NULL DEFAULT NOW(),
    added_by VARCHAR NOT NULL,
    list_priority VARCHAR,
    list_due_date TIMESTAMP,
    list_notes TEXT DEFAULT ''
);

CREATE UNIQUE INDEX idx_unique_list_todo ON list_memberships(list_id, todo_id);
CREATE INDEX idx_membership_list_position ON list_memberships(list_id, position);
CREATE INDEX idx_membership_todo ON list_memberships(todo_id);
CREATE INDEX idx_membership_list ON list_memberships(list_id);
CREATE INDEX idx_membership_added_by ON list_memberships(added_by);
CREATE INDEX idx_membership_added_at ON list_memberships(added_at);
CREATE INDEX idx_membership_list_priority ON list_memberships(list_id, list_priority);
CREATE INDEX idx_membership_list_due ON list_memberships(list_id, list_due_date);
```

---

## Feedback & Learning Tables

### feedback
```sql
CREATE TABLE feedback (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    feedback_type VARCHAR NOT NULL,
    rating INTEGER,
    comment TEXT NOT NULL,
    context JSONB DEFAULT '{}',
    user_id UUID REFERENCES users(id),
    conversation_context JSONB DEFAULT '{}',
    source VARCHAR DEFAULT 'api',
    status VARCHAR DEFAULT 'new',
    priority VARCHAR DEFAULT 'medium',
    sentiment_score FLOAT,
    categories JSONB DEFAULT '[]',
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feedback_session_id ON feedback(session_id);
CREATE INDEX idx_feedback_type ON feedback(feedback_type);
CREATE INDEX idx_feedback_rating ON feedback(rating);
CREATE INDEX idx_feedback_status ON feedback(status);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);
CREATE INDEX idx_feedback_user_id ON feedback(user_id);
CREATE INDEX idx_feedback_source ON feedback(source);
```

### learned_patterns (Issue #300 - Auto-Learning System)
```sql
CREATE TABLE learned_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pattern_type VARCHAR NOT NULL,  -- PatternType enum
    pattern_data JSONB NOT NULL,
    confidence FLOAT NOT NULL DEFAULT 0.5,
    usage_count INTEGER NOT NULL DEFAULT 0,
    success_count INTEGER NOT NULL DEFAULT 0,
    failure_count INTEGER NOT NULL DEFAULT 0,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ix_learned_patterns_user_confidence ON learned_patterns(user_id, confidence);
CREATE INDEX ix_learned_patterns_user_enabled ON learned_patterns(user_id, enabled);
```

### learning_settings (Issue #300 - Learning Configuration)
```sql
CREATE TABLE learning_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    learning_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    suggestion_threshold FLOAT NOT NULL DEFAULT 0.7,
    automation_threshold FLOAT NOT NULL DEFAULT 0.9,
    auto_apply_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    notification_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Personality Profiles

### personality_profiles
```sql
CREATE TABLE personality_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES users(id),
    warmth_level FLOAT NOT NULL DEFAULT 0.6,
    confidence_style VARCHAR(50) NOT NULL DEFAULT 'contextual',
    action_orientation VARCHAR(50) NOT NULL DEFAULT 'medium',
    technical_depth VARCHAR(50) NOT NULL DEFAULT 'balanced',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_personality_profiles_user_id ON personality_profiles(user_id);
CREATE INDEX idx_personality_profiles_active ON personality_profiles(is_active);
CREATE INDEX idx_personality_profiles_user_active ON personality_profiles(user_id, is_active);
CREATE INDEX idx_personality_profiles_warmth ON personality_profiles(warmth_level);
CREATE INDEX idx_personality_profiles_confidence ON personality_profiles(confidence_style);
CREATE INDEX idx_personality_profiles_action ON personality_profiles(action_orientation);
CREATE INDEX idx_personality_profiles_technical ON personality_profiles(technical_depth);
```

---

## Enum Types

### IntentCategory
- EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING, QUERY
- CONVERSATION, IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE, UNKNOWN

### WorkflowType
- CREATE_FEATURE, ANALYZE_METRICS, CREATE_TICKET, CREATE_TASK, REVIEW_ITEM
- GENERATE_REPORT, PLAN_STRATEGY, LEARN_PATTERN, ANALYZE_FEEDBACK
- CONFIRM_PROJECT, SELECT_PROJECT, ANALYZE_FILE, LIST_PROJECTS, MULTI_AGENT

### TaskType
- ANALYZE_REQUEST, EXTRACT_REQUIREMENTS, IDENTIFY_DEPENDENCIES
- CREATE_WORK_ITEM, UPDATE_WORK_ITEM, NOTIFY_STAKEHOLDERS
- GENERATE_DOCUMENT, CREATE_SUMMARY
- GITHUB_CREATE_ISSUE, GENERATE_GITHUB_ISSUE_CONTENT, ANALYZE_GITHUB_ISSUE
- ANALYZE_FILE, SUMMARIZE, LIST_PROJECTS, EXTRACT_WORK_ITEM
- JIRA_CREATE_TICKET, SLACK_SEND_MESSAGE
- PROCESS_USER_FEEDBACK, ANALYZE_DOCUMENT, QUESTION_ANSWER_DOCUMENT
- COMPARE_DOCUMENTS, SUMMARIZE_DOCUMENT, SEARCH_DOCUMENTS

### TodoStatus
- pending, in_progress, completed, cancelled, blocked

### TodoPriority
- low, medium, high, urgent

### ListType
- personal, project, team, template, archive

### OrderingStrategy
- manual, priority, due_date, created_date, alphabetical, status

### NodeType (Knowledge Graph)
- concept, document, person, organization, technology, process

### EdgeType (Knowledge Graph)
- relates_to, depends_on, part_of, similar_to, derived_from

### IntegrationType
- github, jira, linear, slack

---

## Notes

1. **PostgreSQL Port**: Database runs on port **5433** (not default 5432)
2. **UUID Type**: Uses PostgreSQL native UUID type with `uuid_generate_v4()`
3. **JSONB**: Extensive use of JSONB for flexible data storage
4. **GIN Indexes**: Used for JSONB columns to enable efficient JSON queries
5. **Polymorphic Inheritance**: `todo_items` extends `items` via joined table inheritance
6. **Audit Logs**: Intentionally no FK constraint on `user_id` for data retention
7. **Enum Migration**: Several enums migrated from Enum type to VARCHAR for flexibility
8. **Universal Lists**: PM-081 architecture supports any item type in lists

## Database Migrations

Managed via Alembic:
```bash
alembic upgrade head              # Apply all migrations
alembic revision --autogenerate -m "description"  # Generate new migration
```

Migration files located in: `alembic/versions/`

---

Generated from: `services/database/models.py` (1822 lines)
Last updated: November 24, 2025
