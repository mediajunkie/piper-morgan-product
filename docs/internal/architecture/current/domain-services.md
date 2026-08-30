# Domain Services Documentation

## MarkdownFormatter Domain Service

**File**: `services/utils/markdown_formatter.py`
**Purpose**: Ensure LLM-generated markdown follows CommonMark standards
**Domain**: Document Analysis & Summarization

### Business Rules Enforced

1. **Standard Bullet Syntax**: Converts `• -` to `-` (CommonMark standard)
2. **Header Spacing**: Ensures `##Header` becomes `## Header`
3. **Bold Formatting**: Fixes unclosed `**` tags
4. **Multi-space Cleanup**: Normalizes spacing in headers

### Usage

```python
from services.utils.markdown_formatter import MarkdownFormatter

# Clean and validate LLM output
cleaned_text, issues = MarkdownFormatter.clean_and_validate(llm_output)

# Just clean (no validation)
cleaned_text = MarkdownFormatter.ensure_standard_format(llm_output)

# Just validate (no cleaning)
issues = MarkdownFormatter.validate_markdown_syntax(llm_output)
```

### Integration Points

- ~~**TextAnalyzer**: Applied after LLM summary generation~~ *(disposed 2026-08-30, census disposal Batch 3 — `services/analysis/text_analyzer.py` had zero production callers; DocumentAnalyzer is the live analysis path)*
- **DocumentAnalyzer**: Applied after LLM summary generation
- **Prompt Templates**: Updated with explicit formatting rules

### Monitoring

The service logs validation issues for LLM output quality monitoring:

```
INFO: Markdown formatting issues detected and fixed: ['Non-standard bullet syntax: • - found']
```

### Why This Approach

1. **Domain-Driven**: Business rule (markdown format) belongs in domain layer
2. **Testable**: Domain service can be unit tested independently
3. **Maintainable**: Single source of truth for formatting rules
4. **Scalable**: Works for all future LLM summarization features
5. **Architectural Compliance**: No business logic in presentation layer

### Alternative Rejected

❌ **Frontend Preprocessing**: Would have violated clean architecture by putting business logic in presentation layer

✅ **Domain Service**: Proper separation of concerns, follows project's DDD patterns

## BotMessageRenderer Domain Service (Web UI, 2025)

**File**: `web/bot-message-renderer.js`
**Purpose**: Unify all bot message rendering and response handling in the web UI, following DDD principles
**Domain**: Web UI Response Handling

### Business Rules Enforced

1. All bot messages (success, error, thinking) are rendered with consistent structure and CSS classes
2. Markdown is rendered for success messages using `marked.js`
3. Error and feedback messages are actionable and user-friendly
4. All rendering logic is test-driven (TDD) and fully covered by unit/integration tests

### Usage

```javascript
import {
  renderBotMessage,
  handleDirectResponse,
  handleWorkflowResponse,
  handleErrorResponse,
} from "./bot-message-renderer";

// Render a success message
const html = renderBotMessage("Operation complete!", "success", false);

// Handle a direct API response
handleDirectResponse(result, element);

// Handle a workflow completion
handleWorkflowResponse(data, element);

// Handle an error
handleErrorResponse(error, element);
```

### Integration Points

- Used by all web UI code for bot message rendering
- Shared between UI and test files for consistency

### Why This Approach

1. **Domain-Driven**: All business rules for message rendering live in the domain module, not the presentation layer
2. **Testable**: Fully covered by TDD (unit and integration tests)
3. **Maintainable**: Single source of truth for UI feedback and error handling
4. **Extensible**: Easy to add new message types or business rules
5. **Architectural Compliance**: No business logic in presentation layer; all domain logic is modular and reusable

### Alternative Rejected

❌ **Inline UI Logic**: Would have violated DDD and made testing/maintenance difficult

✅ **Domain Service**: Proper separation of concerns, follows project's DDD patterns

---

## DocumentService Domain Service (Document Memory Integration, 2025)

**File**: `services/knowledge_graph/document_service.py`
**Purpose**: Extended with document memory capabilities for decision search, context retrieval, and document recommendations
**Domain**: Document Management & Memory Integration

### Business Rules Enforced

1. **Document Decision Search**: Find decisions on topics within timeframes using existing ChromaDB infrastructure
2. **Context Retrieval**: Get relevant document context for specified time periods
3. **Document Recommendations**: Suggest documents for review based on focus areas
4. **Infrastructure Reuse**: Use existing PM-011 infrastructure exclusively (no parallel storage systems)

### Extended Methods

#### `find_decisions(topic: str, timeframe: str) -> Dict[str, Any]`

Searches for decisions on specific topics within timeframes using existing ChromaDB collection.

```python
# Find architecture decisions from last week
decisions = await service.find_decisions("architecture", "last_week")

# Returns structured response with decisions, count, and source
{
    "decisions": [{"topic": str, "decision": str, "date": str, "confidence": float}],
    "count": int,
    "source": str
}
```

#### `get_relevant_context(timeframe: str) -> Dict[str, Any]`

Retrieves relevant document context for specified timeframes.

```python
# Get context from last 7 days
context = await service.get_relevant_context("last_7_days")

# Returns structured response with context documents
{
    "context_documents": [{"title": str, "summary": str, "date": str, "relevance": float}],
    "count": int,
    "source": str
}
```

#### `suggest_documents(focus_area: str = "") -> Dict[str, Any]`

Provides document recommendations for review based on focus areas.

```python
# Get general recommendations
suggestions = await service.suggest_documents()

# Get architecture-focused recommendations
suggestions = await service.suggest_documents("architecture")
```

### Integration Points

- **CLI Commands**: All document memory operations via `python main.py documents [command]`
- **Morning Standup**: Document context integration ready via DocumentService extensions
- **ChromaDB**: Uses existing `pm_knowledge` collection (8 documents accessible)
- **PM-011 Infrastructure**: Fully integrated with existing document processing pipeline

### Architecture Compliance

1. **No Parallel Storage**: Uses existing DocumentService singleton and ChromaDB infrastructure
2. **Method Extensions**: Adds new capabilities to existing service without breaking changes
3. **Infrastructure Reuse**: Leverages existing PM-011 document processing workflow
4. **Error Handling**: Graceful degradation with informative user feedback

### Why This Approach

1. **Infrastructure Reuse**: Extends existing DocumentService without creating new storage systems
2. **Architectural Consistency**: Follows established service extension patterns
3. **Performance**: Leverages existing ChromaDB collection and processing pipeline
4. **Maintainability**: Single service handles all document memory operations
5. **Integration Ready**: Enables Morning Standup and other features to access document context

### Alternative Rejected

❌ **New Storage Systems**: Would have violated architectural constraints and created maintenance overhead

✅ **Service Extensions**: Proper extension of existing infrastructure, follows established patterns

---

*Last Updated: August 25, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
- **August 25, 2025**: Added DocumentService extensions for document memory integration (PM-126)
