# Piper Morgan 1.0 - User Guide

> ⚠️ **STALE — describes a target state, not the current product** (banner added 2026-08-12, Docs).
> This guide was written for an aspirational "1.0 / production-ready" Piper Morgan. The current
> release is **v0.8.11.0, invite-only alpha** — several capabilities below are partial, changed,
> or not yet wired. For what actually works today, use the **[Alpha Feature
> Guide](ALPHA_FEATURE_GUIDE.md)** and **[Alpha Quick Start](ALPHA_QUICKSTART.md)**. This doc is
> queued for rewrite or retirement in the 2026-08 docs-site scrub.

**Current Status**: Production-ready AI-powered PM assistant with advanced spatial intelligence

## Production Capabilities Overview

✅ **GitHub Integration**: Full issue creation, analysis, and project management
✅ **Slack Spatial Intelligence**: Revolutionary spatial metaphor system with attention algorithms
✅ **Web Chat Interface**: Real-time conversational UI with workflow status tracking
✅ **Knowledge Management**: Multi-format document processing and semantic search
✅ **Workflow Orchestration**: Multi-step PM workflows with intelligent routing

## Getting Started

### System Requirements

- Web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for AI services
- GitHub account for issue creation

## Personality Customization

### Overview
Piper now offers personality customization to make interactions feel more natural and helpful. You can adjust Piper's communication style while maintaining professional accuracy and reliability.

### Web Interface Configuration
**URL**: `http://localhost:8081/personality-preferences`

#### Available Settings

**Warmth Level** (0.0 - 1.0):
- **0.0**: Professional and formal - direct, business-focused responses
- **0.5**: Balanced tone - friendly but professional
- **0.7**: Default - warm but professional (recommended for most users)
- **1.0**: Friendly and encouraging - enthusiastic and supportive

**Confidence Display Style**:
- **Numeric**: Shows percentages like "87% confident" or "moderate confidence (65%)"
- **Descriptive**: Uses words like "high confidence", "uncertain", or "preliminary analysis"
- **Contextual**: Phrases like "based on recent patterns" or "with current information"
- **Hidden**: No confidence indicators shown - clean, streamlined responses

**Action Orientation**:
- **High**: Every response includes explicit next steps and actionable recommendations
- **Medium**: Actionable guidance when relevant and helpful
- **Low**: Minimal action suggestions - focuses on information delivery

**Technical Depth**:
- **Detailed**: Full technical explanations with implementation details
- **Balanced**: Right level of detail for most users - technical but accessible
- **Simplified**: High-level summaries focused on outcomes and decisions

### File Configuration (Advanced Users)
**File**: `../config/PIPER.user.md`

```yaml
personality:
  profile:
    warmth_level: 0.7
    confidence_style: "contextual"
    action_orientation: "medium"
    technical_depth: "balanced"
```

### Personality Enhancement Examples

**Before Enhancement**:
- "3 meetings scheduled. Sprint planning at 15:00."
- "Analysis complete. Found 5 issues."

**After Enhancement (Default Settings)**:
- "You've got 3 meetings today (based on recent patterns)—Sprint planning kicks off at 3 PM. That gives you 90 minutes of focus time right now!"
- "Perfect! Analysis complete (high confidence) and I found 5 issues that need attention. Here's what I recommend tackling first:"

**Professional Mode (warmth: 0.0, confidence: numeric)**:
- "3 meetings scheduled (95% confident). Sprint planning at 15:00."
- "Analysis complete (87% confident). Found 5 issues requiring resolution."

**Friendly Mode (warmth: 1.0, confidence: hidden)**:
- "Excellent! You've got 3 meetings today—Sprint planning at 3 PM is going to be great!"
- "Fantastic! Analysis is all done and I found 5 opportunities for improvement!"

### API Access
Personality settings can also be accessed programmatically:
- **Profile Endpoint**: `http://localhost:8001/api/personality/profile/default`
- **Enhanced Standup**: `http://localhost:8001/api/standup?personality=true`

### Performance
Personality enhancement adds less than 1ms to response times while significantly improving user engagement and actionability.

### Current Limitations

⚠️ **Important**: Piper Morgan is currently in active development with some limitations:

- Single-user system only (multi-user support planned)
- Some advanced workflow persistence optimizations in progress

#### Web Interface (Current)

**New Feature:** The chat window is now vertically resizable. You can drag the bottom edge of the chat window to adjust its height, with a minimum and maximum limit. If the content exceeds the visible area, a scrollbar will appear automatically.

Piper Morgan now includes a DDD-compliant, test-driven web chat interface:

- Chat-based conversational UI for natural language requests
- Real-time workflow status and progress updates
- File upload for knowledge base documents
- Unified feedback and actionable error messages

To use the web interface:

1. Open your browser and navigate to the Piper Morgan web UI (URL provided by your deployment).
2. Enter your request in the chat box (e.g., "Create a ticket for the login bug affecting mobile users").
3. View real-time responses, workflow progress, and results directly in the chat window.
4. Upload documents to the knowledge base using the upload section.

**Technical Note:**
All bot message rendering and response handling is unified in a shared domain module (`bot-message-renderer.js`), ensuring a consistent user experience and robust error handling. The UI is fully covered by automated tests (TDD).

## Core Capabilities

### 1. Natural Language Intent Understanding

Piper Morgan can interpret PM requests like:

- "Create a ticket for the login bug affecting mobile users"
- "Review the requirements document and summarize key points"
- "What were the main decisions from the Q3 retrospective?"

**Quality Note**: Intent classification accuracy varies 60-85% depending on request clarity.

### 2. Command Line Interface (CLI)

Piper Morgan provides powerful CLI commands for content publishing and integration management:

#### Notion Integration Commands

```bash
# Check Notion integration status
python cli/commands/notion.py status

# List available Notion pages
python cli/commands/notion.py pages

# Search Notion content
python cli/commands/notion.py search --query "project planning"

# Create new Notion page
python cli/commands/notion.py create "New Project Page"
```

#### Content Publishing Commands

```bash
# Publish markdown file to Notion
python cli/commands/publish.py publish README.md --to notion --location parent-page-id

# Publish with custom format
python cli/commands/publish.py publish docs/guide.md --to notion --location parent-id --format markdown
```

**Features**:
- ✅ Automatic markdown to Notion conversion
- ✅ Real-time URL return after publication
- ✅ Comprehensive error handling with actionable guidance
- ✅ Environment-aware configuration management

### 3. Knowledge Base Integration

The system can:

- Ingest documents (PDF, DOCX, TXT, MD)
- Search organizational knowledge for context
- Reference historical decisions and documentation

**Quality Note**: Search relevance inconsistent and requires tuning.

### 3. Workflow Orchestration & Integrations

The system currently supports:

- **GitHub Integration**: Full issue creation, analysis, and content generation
- **Multi-step PM workflows**: Orchestration engine with workflow factory patterns
- **Slack Integration**: Advanced spatial metaphor system with attention algorithms
- **Document Analysis**: Multi-format document processing and knowledge extraction

**Status**: Core integrations operational with advanced spatial intelligence capabilities.

## Usage Patterns

### Document Upload and Knowledge Building

```bash
# Upload document (when web UI available)
# Currently requires manual file placement in knowledge base directory
```

### GitHub Issue Creation

```bash
# Request issue creation (GitHub integration active)
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Users report that the mobile app crashes when uploading photos larger than 10MB. This affects iOS and Android. Priority should be high since it blocks core functionality."
  }'
```

**Current GitHub Integration Features**:

- Professional GitHub issue titles and descriptions
- Structured acceptance criteria generation
- Automatic label and priority assignment
- Technical implementation guidance
- Issue analysis and content optimization
- Production-ready GitHub API client with error handling

**Example Output**: Creates properly formatted GitHub issues with comprehensive technical details and professional presentation.

### Slack Spatial Intelligence Integration

**Revolutionary Spatial Metaphor System**:

Piper Morgan's Slack integration uses advanced spatial metaphors to understand and navigate Slack environments:

- **Territories**: Workspaces as navigable buildings with spatial context
- **Rooms**: Channels with purpose detection and atmosphere assessment
- **Conversational Paths**: Threads with momentum and coherence analysis
- **Spatial Objects**: Messages with spatial relationships and placement
- **Attention Attractors**: @mentions with radius effects and priority scoring
- **Emotional Markers**: Reactions with valence and intensity tracking

**Advanced Features**:

- Multi-workspace navigation with intelligent territory switching
- Attention algorithms with temporal decay models
- Cross-session spatial memory and pattern learning
- OAuth 2.0 flow with automatic spatial territory initialization
- Real-time spatial event processing and workflow integration

**Usage**: Natural language interaction with Slack environments through embodied AI spatial awareness.

### Knowledge Queries

```bash
# Query organizational knowledge
curl "http://localhost:8001/api/v1/knowledge/search?q=mobile+login+architecture&k=3"
```

## Command Line Interface (CLI)

### Notion Integration

Piper Morgan provides a comprehensive CLI for managing your Notion workspace directly from the command line:

#### Getting Started with Notion CLI

1. **Check Integration Status**:

   ```bash
   python cli/commands/notion.py status
   ```

   Verifies your Notion API key and workspace connection.

2. **Test Connection**:

   ```bash
   python cli/commands/notion.py test
   ```

   Validates live connection to your Notion workspace.

3. **List Your Pages**:

   ```bash
   python cli/commands/notion.py pages
   ```

   Displays up to 20 pages from your workspace with titles, IDs, and URLs.

4. **Search Content**:

   ```bash
   python cli/commands/notion.py search --query "project requirements"
   ```

   Searches across your entire Notion workspace for relevant content.

5. **Create New Pages**:

   ```bash
   python cli/commands/notion.py create "New Page Title"
   ```

   Creates a new page with automatic parent selection.

   For specific parent pages:

   ```bash
   python cli/commands/notion.py create "Child Page" --parent-id "parent-page-id"
   ```

#### CLI Best Practices

- **Use Descriptive Titles**: Clear, specific page titles improve searchability
- **Verify Before Creating**: Use `status` and `test` commands to ensure connectivity
- **Smart Parent Selection**: Let the system choose parents automatically unless you need specific hierarchy
- **Error Handling**: The CLI provides clear error messages and troubleshooting guidance

#### Example Workflow

```bash
# 1. Verify integration is working
python cli/commands/notion.py status

# 2. List existing pages to understand structure
python cli/commands/notion.py pages

# 3. Search for specific content
python cli/commands/notion.py search --query "Q4 planning"

# 4. Create a new page for Q4 planning
python cli/commands/notion.py create "Q4 2025 Planning and Objectives"

# 5. Verify the page was created
python cli/commands/notion.py search --query "Q4 2025"
```

**Note**: The Notion CLI automatically handles authentication, rate limiting, and error scenarios, providing a robust interface for workspace management.

## Best Practices

### Writing Effective Requests

**Good Examples:**

- "Create a bug report for mobile app crashes during photo upload on iOS, affecting 15% of users"
- "Review the API documentation and identify missing authentication requirements"

**Poor Examples:**

- "Fix the app" (too vague)
- "Create ticket" (missing context)

### Knowledge Base Management

1. **Document Quality**: Upload well-structured documents with clear headings
2. **Metadata**: Include project, date, and document type information
3. **Regular Updates**: Keep knowledge base current with recent decisions
4. **Curation**: Remove outdated or contradictory information

### Workflow Optimization

1. **Context Provision**: Include relevant background in requests
2. **Specificity**: Be specific about requirements and constraints
3. **Verification**: Always review AI-generated content before use
4. **Feedback**: Provide corrections to improve future suggestions

## Troubleshooting

### Common Issues

1. **System Unavailable**: Check if Docker services are running
2. **Slow Responses**: AI processing can take 3-6 seconds for complex operations
3. **Search Quality**: Knowledge base search relevance may vary by content type
4. **Spatial Integration**: Slack spatial features require proper OAuth configuration

### Getting Help

1. Check system health: `curl http://localhost:8001/health`
2. Review Docker logs: `docker-compose logs`
3. Verify API keys in environment configuration
4. See [Deployment Guide](internal/operations/deployment/deployment-summary.md) for setup issues

## Future Capabilities

### Planned Features

- **Multi-user Support**: Team-based access and collaboration
- **Additional Integrations**: Jira, Azure DevOps, analytics platforms
- **Enhanced Learning**: Advanced pattern recognition and adaptation
- **Mobile Interface**: Native mobile app for PM workflows

### Long-term Vision

- **Strategic Insights**: AI-powered product recommendations
- **Predictive Analytics**: Timeline and risk prediction
- **Autonomous Operation**: Self-improving workflow execution
- **Organizational Learning**: Cross-team knowledge sharing

## Feedback and Support

### Providing Feedback

Current system limitations make user feedback collection manual:

1. Document specific issues encountered
2. Note accuracy of AI responses
3. Record time saved or lost using the system
4. Suggest specific improvements needed

### System Status

For current development status, see:

- One-Page Summary (coming soon) - Current capabilities and gaps
- [Roadmap](internal/planning/roadmap/roadmap.md) - Development timeline
- **Backlog** - GitHub is source of truth (`gh issue list`); `backlog.md` was deprecated and moved to trash

This user guide will be updated as system capabilities evolve and mature.

---

_Last Updated: July 28, 2025_

## Revision Log

- **July 28, 2025**: CRITICAL UPDATE - Corrected false claims about GitHub integration, added Slack spatial intelligence system, updated capabilities to reflect PM-074 completion
- **June 27, 2025**: Added systematic documentation dating and revision tracking
