# Technical Spec (as of June 20)

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                           │
│  FastAPI Web Server → Chat Interface → Admin Dashboard         │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                           │
│  Intent Classifier → Workflow Factory → Orchestration Engine   │
│  Knowledge Manager → Learning Engine → Response Generator      │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                             │
│  Domain Services → GitHub Agent → Document Processor           │
│  Event Bus → Workflow Engine → Analytics Service               │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                               │
│  PostgreSQL → ChromaDB → Redis → File System                  │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                           │
│  Claude API → OpenAI API → GitHub API → Temporal              │
└─────────────────────────────────────────────────────────────────┘

```

### 1.2 Component Dependencies

- **Python 3.11+**: Runtime environment
- **FastAPI**: Web framework and API server
- **SQLAlchemy 2.0**: Database ORM with async support
- **ChromaDB**: Vector database for embeddings
- **Redis**: Event queue and caching
- **Temporal**: Workflow orchestration
- **Traefik**: API gateway and load balancing

### 1.2 User Interface: DDD-Compliant Web UI (2025)

The web UI is now implemented as a DDD-compliant, test-driven interface. Key aspects:

- All bot message rendering and response handling is unified in a shared domain module (`bot-message-renderer.js`)
- UI logic is modular, reusable, and fully testable
- TDD process: renderer logic is covered by the frontend unit tests under `tests/frontend/unit/` (the original web-root scratch harnesses `test-message-renderer.js` / `test-response-integration.js` were disposed 2026-08-30; retrievable by commit-hash in the disposal record)
- Markdown rendering uses the `marked.js` library for reliability

**Benefits:**

- Consistent user experience
- Separation of concerns (domain logic vs. presentation)
- Easy extensibility for new message types and workflows
- Real-time feedback and error handling

**Architecture Note:**
The UI layer now fully reflects DDD principles, with all message formatting and business rules in the domain module, not the presentation layer.

## 2. Core Components

### 2.1 Intent Classifier (`services/intent_service/classifier.py`)

**Purpose**: Natural language understanding with organizational context

```python
class IntentClassifier:
    def __init__(self, llm_client: LLMClient, knowledge_base: KnowledgeBase):
        self.llm_client = llm_client
        self.knowledge_base = knowledge_base

    async def classify(self, message: str) -> Intent:
        # Search knowledge base for context
        context = await self.knowledge_base.search(message, k=3)

        # Generate classification prompt with context
        prompt = self._build_classification_prompt(message, context)

        # Get LLM response
        response = await self.llm_client.complete(prompt)

        # Parse structured response
        return self._parse_intent(response)

```

**Key Features**:

- Context-aware classification using knowledge search
- Support for QUERY category for read-only operations
- Structured prompt templates for consistent results
- Confidence scoring and uncertainty handling

**Planned Enhancement: Context-Aware Classification**

The current regex-based approach will be enhanced with LLM-powered classification to support:

- **Conversational Memory**: Track recent interactions and entity references
- **Anaphoric Resolution**: Understand "that", "it", "the previous" references
- **Natural Variations**: Multiple ways to express the same intent
- **Dynamic Actions**: Adapt to available capabilities (especially with MCP)

Example evolution:

```python
# Current: Rigid regex
if re.match(r"show_summary project_id:(\w+)", message):
    # Extract project_id

# Future: Natural understanding
# "show me that summary again"
# "can you display the mobile app summary?"
# "summarize the project we just discussed"
```

This enhancement discovered during Claude Code integration (July 2025) when natural conversational patterns emerged during development.

**Intent Routing**:

```python
# In main API handler
if intent.category == IntentCategory.QUERY:
    # Route to Query Service
    result = await query_router.route_query(intent)
else:
    # Route to Workflow Factory
    workflow = await workflow_factory.create_from_intent(
        intent,
        session_id=session_id,
        project_context=project_context
    )

```

### 2.2 Workflow Factory (`services/orchestration/workflow_factory.py`)

**Purpose**: Create workflows from classified intents using stateless pattern

```python
class WorkflowFactory:
    def __init__(self):
        self.workflow_registry = {}
        self._register_default_workflows()

    async def create_from_intent(
        self,
        intent: Intent,
        session_id: str,
        project_context: Optional[ProjectContext] = None
    ) -> Optional[Workflow]:
        """Create workflow instance from intent with per-call context"""
        # Resolve project if context provided
        if project_context:
            project, needs_confirm = await project_context.resolve_project(
                intent, session_id
            )
            # Merge project info into intent context
            intent.context.update({
                "project_id": project.id,
                "project_name": project.name,
                "needs_confirmation": needs_confirm
            })

        # Match workflow type
        workflow_class = self._match_workflow(intent)
        if not workflow_class:
            return None

        # Create workflow with merged context
        workflow = workflow_class(
            id=str(uuid4()),
            intent_id=intent.id,
            context=intent.context,
            created_at=datetime.now()
        )

        return workflow

```

**Stateless Design**:

- No instance variables for context
- All context passed per-call
- Supports concurrent requests safely
- Explicit dependencies

### 2.3 Knowledge Base (`services/knowledge/knowledge_base.py`)

**Purpose**: Document storage and semantic search

```python
class KnowledgeBase:
    def __init__(self, chroma_client: chromadb.Client, embeddings: OpenAIEmbeddings):
        self.client = chroma_client
        self.embeddings = embeddings
        self.collection = self._get_or_create_collection()

    async def search(self, query: str, k: int = 3) -> List[Document]:
        """Semantic search with relevance scoring"""
        query_embedding = await self.embeddings.aembed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=['documents', 'metadatas', 'distances']
        )

        return self._format_search_results(results)

```

**Document Processing Pipeline**:

1. **Content Extraction**: Format-specific parsers (PDF, DOCX, etc.)
2. **Chunking**: Semantic-aware text splitting with overlap
3. **Embedding**: OpenAI text-embedding-ada-002
4. **Storage**: ChromaDB with metadata and hierarchy

### 2.4 GitHub Agent (`services/integrations/github/github_agent.py`)

**Purpose**: GitHub API operations and issue management

```python
class GitHubAgent:
    def __init__(self, token: str, llm_client: LLMClient):
        self.github = Github(token)
        self.llm_client = llm_client

    async def create_issue(self, repo_name: str, description: str, context: Dict) -> GitHubIssue:
        """Create professionally formatted GitHub issue"""
        # Extract project-specific configuration
        project_config = context.get('project_integrations', {}).get('github', {})
        default_labels = project_config.get('default_labels', [])

        # Generate structured issue content
        issue_content = await self._generate_issue_content(description, context)

        # Merge labels
        issue_content.labels.extend(default_labels)

        # Get repository
        repo = self.github.get_repo(repo_name)

        # Create issue
        issue = repo.create_issue(
            title=issue_content.title,
            body=issue_content.body,
            labels=issue_content.labels,
            assignees=issue_content.assignees
        )

        return GitHubIssue(
            id=issue.id,
            number=issue.number,
            title=issue.title,
            url=issue.html_url,
            created_at=issue.created_at
        )

```

### 2.5 Slack Spatial Intelligence System (`services/integrations/slack/`)

**Purpose**: Process Slack events as spatial changes to Piper's environment using spatial metaphors

#### 2.5.1 Spatial Metaphor Architecture

```python
# Core spatial types
class SpatialTerritory:
    """Slack workspace as physical territory"""
    id: str  # workspace_id
    name: str
    inhabitants: List[SpatialInhabitant]
    rooms: List[SpatialRoom]

class SpatialRoom:
    """Slack channel as room with purpose"""
    id: str  # channel_id
    name: str
    purpose: str
    territory_id: str
    inhabitants: List[SpatialInhabitant]

class SpatialObject:
    """Message as spatial object"""
    id: str  # message_ts
    content: str
    room_id: str
    creator_id: str
    coordinates: SpatialCoordinates

class SpatialInhabitant:
    """User as inhabitant moving between rooms"""
    id: str  # user_id
    name: str
    current_room_id: Optional[str]
    attention_focus: Optional[str]
```

#### 2.5.2 Spatial Event Processing

```python
class SlackSpatialAgent:
    def __init__(self, spatial_memory: SpatialMemory, attention_model: AttentionModel):
        self.spatial_memory = spatial_memory
        self.attention_model = attention_model

    async def process_spatial_event(self, slack_event: Dict[str, Any]) -> SpatialEvent:
        """Convert Slack event to spatial metaphor"""
        spatial_event = await self.spatial_mapper.map_message_to_spatial_event(slack_event)

        # Update spatial memory
        await self.spatial_memory.update_from_event(spatial_event)

        # Process attention attractors (@mentions)
        if spatial_event.has_attention_attractor:
            await self.attention_model.process_attention_attractor(spatial_event)

        # Process emotional markers (reactions)
        if spatial_event.has_emotional_markers:
            await self.process_emotional_markers(spatial_event)

        return spatial_event

    async def make_navigation_decision(self, spatial_event: SpatialEvent) -> NavigationDecision:
        """Determine if Piper should navigate to this spatial location"""
        return await self.workspace_navigator.evaluate_navigation(spatial_event)
```

#### 2.5.3 Spatial Intent Classification

```python
class SpatialIntentClassifier:
    def __init__(self, pattern_matcher: PatternMatcher, llm_client: LLMClient):
        self.pattern_matcher = pattern_matcher
        self.llm_client = llm_client

    async def classify_spatial_event(self, spatial_event: SpatialEvent) -> SpatialIntent:
        """Classify spatial event with confidence scoring"""
        # Pattern matching for common spatial intents
        pattern_result = await self.pattern_matcher.match_patterns(spatial_event)

        if pattern_result.confidence > 0.8:
            return pattern_result

        # LLM-based classification for complex spatial events
        llm_result = await self._llm_classify_spatial_event(spatial_event)

        return llm_result
```

#### 2.5.4 Spatial Memory and Attention

```python
class SpatialMemory:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.ttl_hours = 24

    async def update_from_event(self, spatial_event: SpatialEvent):
        """Update spatial memory with new event"""
        # Store spatial object
        await self.redis.setex(
            f"spatial:object:{spatial_event.object_id}",
            self.ttl_hours * 3600,
            spatial_event.to_json()
        )

        # Update inhabitant location
        await self.redis.setex(
            f"spatial:inhabitant:{spatial_event.creator_id}:location",
            self.ttl_hours * 3600,
            spatial_event.room_id
        )

class AttentionModel:
    def __init__(self, proximity_calculator: ProximityCalculator):
        self.proximity_calculator = proximity_calculator

    async def process_attention_attractor(self, spatial_event: SpatialEvent):
        """Process @mentions as high-priority attention attractors"""
        if spatial_event.has_mention:
            # High priority - immediate navigation
            return NavigationDecision(
                should_navigate=True,
                priority=AttentionPriority.HIGH,
                reason="Direct mention detected"
            )
```

#### 2.5.5 Spatial to Workflow Integration

```python
class SlackWorkflowFactory:
    def __init__(self, spatial_intent_classifier: SpatialIntentClassifier):
        self.spatial_intent_classifier = spatial_intent_classifier

    async def create_workflow_from_spatial_event(self, spatial_event: SpatialEvent) -> Workflow:
        """Convert spatial event to Piper workflow"""
        # Classify spatial intent
        spatial_intent = await self.spatial_intent_classifier.classify_spatial_event(spatial_event)

        # Create workflow with spatial context
        workflow = Workflow(
            id=str(uuid.uuid4()),
            type=spatial_intent.workflow_type,
            context={
                "spatial_event": spatial_event.to_dict(),
                "spatial_intent": spatial_intent.to_dict(),
                "emotional_markers": spatial_event.emotional_markers,
                "attention_priority": spatial_event.attention_priority
            }
        )

        return workflow
```

**Key Features**:

- **8 Spatial Components**: Complete spatial intelligence system
- **52 TDD Integration Tests**: Comprehensive test coverage
- **Production-Ready Configuration**: ADR-010 compliant config service
- **Real-time Event Processing**: Webhook routing with ngrok integration
- **Spatial Memory Persistence**: Redis-based spatial awareness
- **Attention Modeling**: @mention processing and priority scoring

### 2.6 Orchestration Engine (`services/orchestration/engine.py`)

**Purpose**: Workflow execution and coordination using internal method handlers for all task types.

```python
class OrchestrationEngine:
    def __init__(self, github_agent: GitHubAgent, ...):
        self.github_agent = github_agent
        self.task_handlers = {
            TaskType.FILE_ANALYSIS: self._analyze_file,
            TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue,
            # ... other handlers ...
        }
        self.workflows = {}  # In-memory workflow tracking

    async def execute_workflow(self, workflow_id: str) -> WorkflowResult:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise WorkflowNotFoundError(workflow_id)
        for task in workflow.tasks:
            if task.status != TaskStatus.PENDING:
                continue
            try:
                task.status = TaskStatus.RUNNING
                handler = self.task_handlers.get(task.type)
                if not handler:
                    raise NotImplementedError(f"No handler for {task.type}")
                result = await handler(task, workflow.context)
                task.status = TaskStatus.COMPLETED
                task.result = result
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                workflow.status = WorkflowStatus.FAILED
                workflow.error = f"Task {task.id} failed: {e}"
                break
        if all(t.status == TaskStatus.COMPLETED for t in workflow.tasks):
            workflow.status = WorkflowStatus.COMPLETED
        return WorkflowResult(
            success=workflow.status == WorkflowStatus.COMPLETED,
            data={"tasks": [t.to_dict() for t in workflow.tasks]},
            error=workflow.error
        )
```

#### Internal Handler Pattern

- All task handlers are methods on the engine instance.
- `self.task_handlers` maps TaskType to handler methods.
- No external handler classes or modules.
- Handlers have direct access to engine state and dependencies.

### 2.5.1 Workflow Execution Return Structure

The `execute_workflow` method returns a dictionary (not WorkflowResult object):

```python
{
    "id": "workflow-uuid",
    "type": "CREATE_TICKET",
    "status": "completed",  # or "failed", "pending"
    "tasks": [
        {
            "id": "task-uuid",
            "type": "GITHUB_CREATE_ISSUE",
            "status": "completed",
            "result": {
                "output_data": {
                    "issue_number": 7,
                    "issue_url": "https://github.com/owner/repo/issues/7",
                    "issue_data": {...}
                }
            }
        }
    ],
    "context": {},
    "error": null,
    "created_at": "2025-06-29T...",
    "updated_at": "2025-06-29T..."
}
```

**Success Check**: Use `result["status"] == "completed"` (no `success` field)

**Task Results**: Access via `result["tasks"][0]["result"]["output_data"]`

### 2.5.2 GitHub Task Handlers

**Example: GitHub Issue Creation Handler**

```python
async def _create_github_issue(self, task: Task, context: dict):
    """
    Handler for GITHUB_CREATE_ISSUE tasks. Uses GitHubAgent to create an issue.
    Expects context to include 'repository', 'title', and 'body'.
    """
    repo = context.get("repository")
    title = context.get("title")
    body = context.get("body")
    if not repo or not title or not body:
        return {"error": "Missing required context for GitHub issue creation"}
    result = await self.github_agent.create_issue(
        repository=repo,
        title=title,
        body=body,
        labels=context.get("labels", [])
    )
    return {"github_issue": result}
```

### 2.6 Query Service (`services/queries/query_service.py`)

> ⚠️ **Dated note (2026-08-30)**: HISTORICAL. `services/queries/` was disposed in the Batch-2
> census-dead-family disposal — the CQRS-lite query layer was never wired to any entrypoint
> (its QueryRouter predeceased it; the 2026-08-29 leg-B census + fresh delete-time sweep found
> zero production callers). Live query traffic rides the intent-service canonical handlers.
> Retrievable by commit hash via the 2026-08-30 disposal record in decisions.log.

**Purpose**: Handle read-only data operations without workflow overhead

```python
class QueryRouter:
    """Routes QUERY intents to appropriate query services"""

    def __init__(self, project_repository: ProjectRepository):
        self.project_queries = ProjectQueryService(project_repository)
        # Add other query services as needed

    async def route_query(self, intent: Intent) -> QueryResult:
        """Route based on intent action"""
        if intent.action == "list_projects":
            projects = await self.project_queries.list_active_projects()
            return QueryResult(
                success=True,
                data={"projects": [p.to_dict() for p in projects]},
                query_type="list"
            )
        elif intent.action == "get_project":
            project_id = intent.context.get("project_id")
            project = await self.project_queries.get_project_by_id(project_id)
            return QueryResult(
                success=True,
                data={"project": project.to_dict() if project else None},
                query_type="get"
            )
        elif intent.action == "find_project":
            name = intent.context.get("project_name")
            projects = await self.project_queries.find_by_name(name)
            return QueryResult(
                success=True,
                data={"projects": [p.to_dict() for p in projects]},
                query_type="find"
            )
        else:
            return QueryResult(
                success=False,
                error=f"Unknown query action: {intent.action}",
                query_type="unknown"
            )

class ProjectQueryService:
    """Query service for project-related data retrieval"""

    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    async def list_active_projects(self) -> List[Project]:
        """Get all active projects"""
        return await self.repo.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get specific project"""
        return await self.repo.get_by_id(project_id)

    async def find_by_name(self, name: str) -> List[Project]:
        """Find projects by name pattern"""
        return await self.repo.find_by_name(name)

    async def get_default_project(self) -> Optional[Project]:
        """Get the default project if one exists"""
        return await self.repo.get_default_project()

```

**Query vs Command Decision Matrix**:

| Operation       | Type    | Handler      | Example                 |
| --------------- | ------- | ------------ | ----------------------- |
| List entities   | Query   | QueryService | "Show all projects"     |
| Get by ID       | Query   | QueryService | "Get project details"   |
| Search/Find     | Query   | QueryService | "Find mobile project"   |
| Create          | Command | Workflow     | "Create new issue"      |
| Update          | Command | Workflow     | "Update project status" |
| Complex process | Command | Workflow     | "Analyze repository"    |

### 2.7 Project Context (`services/project_context/project_context.py`)

> ⚠️ **Dated note (2026-08-30)**: HISTORICAL. `services/project_context/` was disposed in the
> Batch-2 census-dead-family disposal (never loaded from any entrypoint; zero production
> callers at delete time). The live `ProjectContext` dataclass in `services/domain/models.py`
> is a DIFFERENT, unrelated class — same name, name-collision trap. Retrievable by commit hash
> via the 2026-08-30 disposal record in decisions.log.

**Purpose**: Sophisticated project resolution for multi-project support

```python
class ProjectContext:
    """Resolves project context from various sources"""

    def __init__(self, project_repository: ProjectRepository, llm_client: LLMClient):
        self.repo = project_repository
        self.llm = llm_client
        self._session_last_used: Dict[str, str] = {}  # session_id -> project_id

    async def resolve_project(
        self,
        intent: Intent,
        session_id: str,
        confirmed_this_session: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolve project with hierarchy:
        1. Explicit project_id in intent
        2. Last used in session (if confirmed)
        3. Inferred from message context
        4. Default project fallback

        Returns: (project, needs_confirmation)
        """
        # 1. Explicit project_id always wins
        if project_id := intent.context.get("project_id"):
            project = await self.repo.get_by_id(project_id)
            if not project:
                raise ProjectNotFoundError(f"Project {project_id} not found")
            return project, False

        # 2. Check session history
        last_project_id = self._session_last_used.get(session_id)

        # 3. Try to infer from message
        inferred_project = await self._infer_from_context(intent)

        # 4. Decision logic
        if last_project_id and confirmed_this_session:
            # Use last project without confirmation
            project = await self.repo.get_by_id(last_project_id)
            return project, False
        elif inferred_project:
            # Store for future use
            self._session_last_used[session_id] = inferred_project.id
            # Need confirmation if different from last used
            needs_confirm = last_project_id and last_project_id != inferred_project.id
            return inferred_project, needs_confirm
        elif last_project_id:
            # Fall back to last used but need confirmation
            project = await self.repo.get_by_id(last_project_id)
            return project, True
        else:
            # Final fallback - default project
            return await self._get_or_raise_default()

```

## 3. Data Flow Patterns

### 3.1 Command Flow (State Changes)

```
1. User Input: "Create a bug ticket for mobile login"
2. Intent Classification: {category: EXECUTION, action: "create_ticket"}
3. Project Resolution: Infer "mobile-app" project from context
4. Workflow Creation: CreateTicketWorkflow with project context
   - Repository context is automatically enriched (if available)
5. Task Execution:
   - Analyze request
   - Generate issue content
   - Create GitHub issue (uses enriched repository context)
6. Response: "Created issue #123 in mobile-app repository"

```

### 3.2 Query Flow (Data Retrieval)

> ⚠️ **Dated note (2026-08-30)**: the QueryRouter/ProjectQueryService rail below never shipped
> (disposed with `services/queries/`, see §2.6 note). Live query flow routes through the
> intent-service category handlers.

```
1. User Input: "What projects are available?"
2. Intent Classification: {category: QUERY, action: "list_projects"}
3. Query Router: Route to ProjectQueryService
4. Direct Repository Access: Fetch active projects
5. Response: List of projects with details

```

### 3.3 Workflow Context Structure

**Example: GitHub Issue Creation Workflow Context**

```json
{
  "project_id": "proj-123",
  "project_name": "Mobile App",
  "repository": "acme/mobile-app",
  "title": "Login fails on iOS",
  "body": "Steps to reproduce...",
  "labels": ["bug", "ios"]
}
```

- The `repository` field is automatically injected during workflow creation if available from project context.
- Downstream handlers (e.g., GitHub issue creation) consume this context.

## 4. API Design

### 4.1 REST Endpoints

```python
# Main intent processing endpoint
POST /api/v1/intent
{
    "message": "Create a ticket for the login bug affecting mobile users"
}

# Response for commands
{
    "intent": {
        "category": "execution",
        "action": "create_github_issue",
        "confidence": 0.95,
        "context": {...}
    },
    "response": "I'll create a GitHub issue for the mobile login bug...",
    "workflow_id": "uuid-here"
}

# Response for queries
{
    "intent": {
        "category": "query",
        "action": "list_projects",
        "confidence": 0.98
    },
    "response": "Here are your active projects:",
    "data": {
        "projects": [
            {
                "id": "proj-123",
                "name": "Mobile App",
                "description": "iOS and Android applications",
                "integrations": ["github", "jira"]
            }
        ]
    }
}

```

### 4.2 WebSocket Events

```python
# Real-time workflow updates
ws://localhost:8001/ws/workflows/{workflow_id}

# Events
{
    "type": "workflow.task_started",
    "workflow_id": "uuid",
    "task_id": "task-123",
    "task_type": "analyze_request"
}

{
    "type": "workflow.completed",
    "workflow_id": "uuid",
    "result": {...}
}

```

## 5. Error Handling Strategy

### 5.1 Error Categories

```python
class ErrorCategory(Enum):
    USER_INPUT = "user_input"      # Invalid or ambiguous input
    INTEGRATION = "integration"     # External service failures
    PROCESSING = "processing"       # Internal processing errors
    AUTHORIZATION = "authorization" # Permission issues

```

### 5.2 User-Friendly Error Responses

```python
ERROR_MESSAGES = {
    ProjectNotFoundError: "I couldn't find that project. Try 'list projects' to see available options.",
    AmbiguousProjectError: "Multiple projects match your request. Please be more specific.",
    GitHubAPIError: "GitHub is temporarily unavailable. Please try again in a few moments.",
    InsufficientContextError: "I need more information to complete this task. {details}"
}

```

## 6. Security Considerations

### 6.1 API Key Management

- Store all API keys in environment variables
- Rotate keys regularly
- Use separate keys for development/production
- Never log API keys

### 6.2 Data Access Controls

- Repository pattern enforces access boundaries
- User-specific project access
- Audit logging for all state changes
- Read-only query services cannot modify data

## 7. Performance Optimizations

### 7.1 Caching Strategy

- Redis caching for frequent queries
- In-memory caching for session data
- Vector search result caching
- LLM response caching for identical requests

### 7.2 Async Processing

- All I/O operations use async/await
- Background task processing for workflows
- Non-blocking API responses
- Concurrent task execution where possible

## 8. Testing Patterns

### 8.1 Unit Testing

```python
# Test domain logic
async def test_project_resolution_explicit_id():
    # Mock repository
    mock_repo = Mock(spec=ProjectRepository)
    mock_repo.get_by_id.return_value = Project(id="123", name="Test")

    # Test explicit ID resolution
    context = ProjectContext(mock_repo, mock_llm)
    project, needs_confirm = await context.resolve_project(
        Intent(context={"project_id": "123"}),
        session_id="test"
    )

    assert project.id == "123"
    assert needs_confirm is False

```

### 8.2 Integration Testing

```python
# Test full flow
async def test_create_issue_workflow():
    # Real services, test database
    result = await api_client.post("/api/v1/intent", json={
        "message": "Create bug ticket for login issue"
    })

    assert result["workflow_id"] is not None
    # Verify issue created in GitHub

```

---

_Last Updated: July 28, 2025_

## Revision Log

- **July 28, 2025**: Added Slack Spatial Intelligence System specifications (Section 2.5) with spatial metaphor architecture, event processing, intent classification, memory/attention, and workflow integration
- **June 28, 2025**: Updated Orchestration Engine section for internal handler pattern, added GitHub handler example, updated command flow for repository enrichment, added workflow context structure for GitHub integration
- **June 21, 2025**: Added systematic documentation dating and revision tracking
