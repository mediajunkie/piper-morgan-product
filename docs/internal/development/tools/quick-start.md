# Piper Morgan 1.0 - Quick Start Guide

_Quick start guide for new developers_

For comprehensive development standards and patterns, see [Development Guidelines](./dev-guidelines.md).

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- VS Code (recommended)

### Local Setup

```bash
# Clone repository
git clone <repository-url>
cd piper-morgan-platform

# Start infrastructure services
docker-compose up -d

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Development Workflow

1. Create feature branch from main
2. Implement changes following architecture patterns
3. Test locally with Docker Compose
4. Update documentation as needed
5. Submit pull request

### Code Structure

```
services/
├── analysis/           # Content analysis and sampling
├── api/               # Web API endpoints
├── conversation/      # Conversation management
├── database/          # Database connection and models
├── domain/            # Core business logic and models
├── feedback/          # User feedback capture
├── file_context/      # File resolution and context
├── infrastructure/    # Configuration and monitoring
├── integrations/      # External system integrations
│   ├── github/        # GitHub integration
│   └── slack/         # Slack spatial intelligence system
├── intelligence/      # AI intelligence services
├── intent_service/    # Natural language processing
├── knowledge/         # Knowledge base management
├── knowledge_graph/   # Document ingestion and graph
├── llm/               # LLM client management
├── mcp/               # Model Context Protocol
├── orchestration/     # Workflow management
├── persistence/       # Data persistence layer
├── project_context/   # Project context management
├── prompts/           # Prompt management
├── queries/           # Query processing
├── repositories/      # Data access layer
├── session/           # Session management
├── ui_messages/       # UI message templates
└── utils/             # Utility functions
```

### Excellence Flywheel Development Workflow

**MANDATORY**: Follow the Excellence Flywheel methodology for all development work:

1. **Systematic Verification First** - Verify requirements and existing state before implementation
2. **TDD Requirements** - Write tests FIRST, then implementation
3. **Agent Coordination** - Coordinate parallel work systematically
4. **Quality Vigilance** - Maintain high standards throughout

**Key Principles**:

- Quality creates velocity creates quality
- Systematic approaches create self-reinforcing productivity cycles
- Foundation-first approach enables impossible speed with perfect quality

For detailed methodology, see [Excellence Flywheel Documentation](../methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md).

### Testing

```bash
# Run all tests
pytest

# Run specific service tests
pytest services/intent_service/tests/

# Run Slack spatial intelligence tests
PYTHONPATH=. pytest services/integrations/slack/tests/ -v

# Run specific spatial integration tests
PYTHONPATH=. pytest services/integrations/slack/tests/test_spatial_system_integration.py -v

# Run with coverage
pytest --cov=services
```

### Common Tasks

- **Add new workflow**: Implement in `services/orchestration/workflows/`
- **Add external integration**: Create plugin in `services/integrations/`
- **Update domain model**: Modify `services/domain/models.py`
- **Add API endpoint**: Update `services/api/routes/`
- **Add spatial intelligence**: Extend `services/integrations/slack/` spatial components

For detailed technical information, see [Technical Specification](../../architecture/current/technical-spec.md).

## Environment Variables Checklist

When creating new services that need API keys or config:

✅ **Always add `load_dotenv()` at the top of modules that use `os.getenv()`**
✅ **Import pattern**: `from dotenv import load_dotenv; load_dotenv()`
✅ **Place before any `os.getenv()` calls**
✅ **Test with fresh terminal/environment to catch missing env loading**

### Common Modules That Need This:

- LLM clients (Claude, OpenAI)
- Database connections
- External API integrations
- Knowledge/embedding services

### Slack Integration Environment Variables

For Slack spatial intelligence system:

```bash
# Slack App Configuration
SLACK_CLIENT_ID=your_slack_app_client_id
SLACK_CLIENT_SECRET=your_slack_app_client_secret
SLACK_SIGNING_SECRET=your_slack_app_signing_secret

# Spatial Intelligence Configuration
SPATIAL_MEMORY_ENABLED=true
SPATIAL_ATTENTION_MODEL_ENABLED=true
SPATIAL_WORKSPACE_NAVIGATION_ENABLED=true

# Ngrok for webhook testing (development)
NGROK_AUTH_TOKEN=your_ngrok_auth_token
```

### Spatial Metaphor Environment Variables

For spatial intelligence system configuration:

```bash
# Spatial Intelligence Settings
SPATIAL_TERRITORY_ENABLED=true
SPATIAL_ATTENTION_ATTRACTORS_ENABLED=true
SPATIAL_EMOTIONAL_MARKERS_ENABLED=true
SPATIAL_CONVERSATIONAL_PATHS_ENABLED=true

# Spatial Memory Configuration
SPATIAL_MEMORY_PERSISTENCE_ENABLED=true
SPATIAL_MEMORY_TTL_HOURS=24
```

---

_Last Updated: July 28, 2025_

## Revision Log

- **July 28, 2025**: Updated with Slack spatial intelligence system, Excellence Flywheel methodology, and current architecture
- **June 21, 2025**: Added systematic documentation dating and revision tracking
