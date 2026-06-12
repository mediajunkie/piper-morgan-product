# Orchestration System Setup Guide

## Quick Start

### Basic Setup
```python
from services.orchestration.engine import OrchestrationEngine

# Standard initialization pattern - no session required
engine = OrchestrationEngine()

# Optional: Provide custom LLM client
from services.llm.clients import LLMClient
custom_llm = LLMClient()
engine = OrchestrationEngine(llm_client=custom_llm)
```

### Processing Requests
```python
# Process user requests through orchestration
async def process_user_request(user_input: str):
    engine = OrchestrationEngine()

    # Create intent from user input
    from services.domain.models import Intent, IntentCategory
    intent = Intent(
        category=IntentCategory.QUERY,
        action=user_input,
        confidence=0.9,
        context={}
    )

    # Process through orchestration
    result = await engine.handle_query_intent(intent)
    return result
```

## Initialization Components

### Core Components Initialized
Based on code analysis, OrchestrationEngine initializes these components:

1. **llm_client**: LLM service integration (global or provided)
2. **factory**: WorkflowFactory for workflow creation
3. **workflows**: Dictionary to track active workflows
4. **query_router**: QueryRouter (lazy initialization)
5. **intent_enricher**: Intent processing and enrichment
6. **logger**: Structured logging
7. **workflow_integration**: Multi-agent workflow coordination
8. **session_integration**: Session management integration
9. **performance_monitor**: Performance tracking

### Lazy-Loaded Components
```python
# QueryRouter is initialized on first access
engine = OrchestrationEngine()
print(engine.query_router)  # None - not yet initialized

# First access triggers initialization
query_router = await engine.get_query_router()
print(engine.query_router)  # Now initialized and cached
```

## Common Setup Patterns

### Web Application Integration
```python
# FastAPI integration example
from fastapi import FastAPI
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

app = FastAPI()

# Global engine instance (recommended pattern)
orchestration_engine = OrchestrationEngine()

@app.post("/process")
async def process_request(user_input: str):
    intent = Intent(
        category=IntentCategory.QUERY,
        action=user_input,
        confidence=0.9,
        context={}
    )

    result = await orchestration_engine.handle_query_intent(intent)
    return {"result": result}
```

### Testing Setup
```python
# Test setup with proper initialization verification
import pytest
from services.orchestration.engine import OrchestrationEngine

@pytest.fixture
def orchestration_engine():
    return OrchestrationEngine()

def test_orchestration_initialization(orchestration_engine):
    # Verify core components
    assert orchestration_engine.llm_client is not None
    assert orchestration_engine.factory is not None
    assert orchestration_engine.intent_enricher is not None
    assert orchestration_engine.logger is not None

    # Verify lazy-loaded components
    assert orchestration_engine.query_router is None  # Not yet loaded

@pytest.mark.asyncio
async def test_query_router_initialization(orchestration_engine):
    # Trigger QueryRouter initialization
    query_router = await orchestration_engine.get_query_router()

    # Verify initialization
    assert query_router is not None
    assert orchestration_engine.query_router is not None  # Now cached
```

## Configuration Options

### Environment Variables
```bash
# LLM service configuration
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.service.com

# Database configuration (for QueryRouter session-aware services)
DATABASE_URL=postgresql://localhost/piper
POSTGRES_DB=piper
POSTGRES_USER=piper
POSTGRES_PASSWORD=your-password
```

### Custom LLM Client
```python
# Provide custom LLM configuration
from services.llm.clients import LLMClient

# Custom LLM client with specific configuration
custom_llm = LLMClient(
    api_key="your-key",
    base_url="https://custom-llm-service.com",
    timeout=60
)

engine = OrchestrationEngine(llm_client=custom_llm)
```

## QueryRouter Integration

### Session-Aware Services Pattern
The QueryRouter uses session-aware wrapper services that handle database connections automatically:

```python
# QueryRouter initialization (happens automatically)
from services.queries.session_aware_wrappers import (
    SessionAwareProjectQueryService,
    SessionAwareFileQueryService
)
from services.queries.conversation_queries import ConversationQueryService

query_router = QueryRouter(
    project_query_service=SessionAwareProjectQueryService(),
    conversation_query_service=ConversationQueryService(),
    file_query_service=SessionAwareFileQueryService()
)
```

### Benefits of Session-Aware Pattern
- **Automatic session management**: No need to pass database sessions
- **Clean separation**: Each service handles its own database needs
- **Proper cleanup**: Sessions automatically closed after operations
- **Error handling**: Database errors contained within service scope

## Troubleshooting

### "No module named 'services'" Error
```python
# Add project root to Python path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Then import orchestration components
from services.orchestration.engine import OrchestrationEngine
```

### LLM Client Initialization Issues
```python
# Verify global LLM client is available
try:
    from services.llm.clients import llm_client
    print("✅ Global LLM client available")
except ImportError as e:
    print(f"❌ LLM client import failed: {e}")
    # Provide explicit LLM client
    engine = OrchestrationEngine(llm_client=custom_llm_client)
```

### QueryRouter Initialization Failures
```python
# Test QueryRouter initialization separately
async def test_query_router():
    try:
        engine = OrchestrationEngine()
        query_router = await engine.get_query_router()
        print("✅ QueryRouter initialized successfully")
        return query_router
    except Exception as e:
        print(f"❌ QueryRouter initialization failed: {e}")
        # Check database connectivity
        from services.database.session_factory import AsyncSessionFactory
        try:
            async with AsyncSessionFactory.session_scope() as session:
                print("✅ Database connection working")
        except Exception as db_error:
            print(f"❌ Database connection failed: {db_error}")
```

### Component Not Available
```python
# Check component initialization status
engine = OrchestrationEngine()

# Verify all components
components = [
    'llm_client', 'factory', 'workflows', 'intent_enricher',
    'logger', 'workflow_integration', 'session_integration',
    'performance_monitor'
]

for component in components:
    if hasattr(engine, component) and getattr(engine, component) is not None:
        print(f"✅ {component} initialized")
    else:
        print(f"❌ {component} not initialized")

# Check lazy-loaded components
print(f"QueryRouter (lazy): {'✅ Available' if engine.query_router else '⏳ Not yet loaded'}")
```

## Best Practices

### Component Reuse
```python
# Reuse engine instance within application scope
class OrchestrationService:
    def __init__(self):
        self.engine = OrchestrationEngine()

    async def process_query(self, query: str):
        # Reuse the same engine instance
        return await self.engine.handle_query_intent(...)
```

### Error Handling
```python
async def robust_orchestration(user_input):
    try:
        engine = OrchestrationEngine()

        # Create intent
        intent = Intent(
            category=IntentCategory.QUERY,
            action=user_input,
            confidence=0.9,
            context={}
        )

        return await engine.handle_query_intent(intent)

    except ImportError as e:
        # Handle missing dependencies
        logger.error(f"Dependency error: {e}")
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Orchestration error: {e}")
        raise
```

### Performance Optimization
- **Singleton pattern**: Reuse OrchestrationEngine instances
- **Lazy loading**: QueryRouter only initialized when needed
- **Component caching**: Initialized components are cached
- **Session management**: Automatic cleanup prevents connection leaks

## Integration Examples

### Command Line Tool
```python
#!/usr/bin/env python3
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def main():
    engine = OrchestrationEngine()

    while True:
        user_input = input("Enter query (or 'quit'): ")
        if user_input.lower() == 'quit':
            break

        intent = Intent(
            category=IntentCategory.QUERY,
            action=user_input,
            confidence=0.9,
            context={}
        )

        try:
            result = await engine.handle_query_intent(intent)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Jupyter Notebook Integration
```python
# Cell 1: Setup
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

# Initialize engine
engine = OrchestrationEngine()

# Cell 2: Test Query
async def test_query(query_text):
    intent = Intent(
        category=IntentCategory.QUERY,
        action=query_text,
        confidence=0.9,
        context={}
    )
    return await engine.handle_query_intent(intent)

# Cell 3: Execute
result = await test_query("List recent files")
print(result)
```

## SSL Certificate Requirements

For fresh environments, ensure SSL certificates are properly configured:

```bash
# Install/upgrade certificate bundle (fixes missing cacert.pem)
pip install --upgrade --force-reinstall certifi

# Verify SSL functionality
python3 -c "import certifi, requests; print('SSL ready:', requests.get('https://httpbin.org/get').status_code == 200)"
```

### Common SSL Issues

**Problem**: `FileNotFoundError: cacert.pem`
**Solution**: Reinstall certifi package with `pip install --upgrade --force-reinstall certifi`

**Problem**: `NotOpenSSLWarning` about LibreSSL vs OpenSSL
**Solution**: This is a warning only and does not affect functionality

If SSL errors persist:
- Ubuntu/Debian: `sudo apt-get install ca-certificates`
- macOS: `brew install ca-certificates`
- Verify: `python3 -c "import certifi; print(certifi.where())"`

---

*For detailed initialization sequence, see [initialization-sequence.md](../internal/architecture/current/initialization-sequence.md)*
