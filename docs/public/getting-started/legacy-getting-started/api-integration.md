# API Integration Quick Start

This guide helps you integrate Piper Morgan's APIs into your existing systems and workflows. Whether you're building custom tooling or integrating with third-party services, this guide provides everything you need to get started.

## API Overview

Piper Morgan provides several APIs for different use cases:

### Core APIs
- **Issue Intelligence API**: Analyze and classify GitHub issues
- **Query Router API**: Route natural language queries to appropriate handlers
- **Conversation API**: Manage conversational AI interactions
- **Workflow API**: Orchestrate multi-step processes

### Integration Points
- **GitHub Webhooks**: Real-time issue processing
- **Slack Integration**: Team notifications and interactions
- **MCP Protocol**: Model Context Protocol for AI agent coordination

## Quick Integration

### 1. Authentication

All API requests require authentication via API key:

```bash
# Set your API key
export PIPER_API_KEY="your-api-key-here"

# Test authentication
curl -H "Authorization: Bearer $PIPER_API_KEY" \
     https://api.piper-morgan.com/v1/health
```

### 2. Basic Issue Analysis

Analyze a GitHub issue using the Issue Intelligence API:

```python
import requests

url = "https://api.piper-morgan.com/v1/issues/analyze"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "issue_url": "https://github.com/owner/repo/issues/123",
    "analysis_types": ["classification", "priority", "complexity"]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
```

### 3. Natural Language Queries

Use the Query Router for natural language processing:

```python
query_data = {
    "query": "What are the high-priority bugs in the backend repository?",
    "context": {
        "repository": "owner/backend-repo",
        "filters": ["bug", "high-priority"]
    }
}

response = requests.post(
    "https://api.piper-morgan.com/v1/query",
    headers=headers,
    json=query_data
)
```

### 4. Webhook Setup

Configure GitHub webhooks for real-time processing:

```json
{
  "name": "web",
  "active": true,
  "events": ["issues", "issue_comment", "pull_request"],
  "config": {
    "url": "https://api.piper-morgan.com/v1/webhooks/github",
    "content_type": "json",
    "secret": "your-webhook-secret"
  }
}
```

## SDK Options

### Python SDK
```python
from piper_morgan import PiperClient

client = PiperClient(api_key="your-api-key")
analysis = client.analyze_issue("https://github.com/owner/repo/issues/123")
```

### JavaScript SDK
```javascript
import { PiperClient } from '@piper-morgan/sdk';

const client = new PiperClient({ apiKey: 'your-api-key' });
const analysis = await client.analyzeIssue('https://github.com/owner/repo/issues/123');
```

### CLI Tool
```bash
# Install CLI
pip install piper-morgan-cli

# Configure
piper-morgan config set api-key your-api-key

# Analyze issue
piper-morgan issues analyze https://github.com/owner/repo/issues/123
```

## Integration Patterns

### Continuous Integration

Integrate issue analysis into your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Analyze Issues
  uses: piper-morgan/github-action@v1
  with:
    api-key: ${{ secrets.PIPER_API_KEY }}
    analysis-types: 'classification,priority,complexity'
```

### Slack Notifications

Set up automated Slack notifications:

```python
# Configure Slack webhook
slack_config = {
    "webhook_url": "your-slack-webhook",
    "channel": "#development",
    "triggers": ["high-priority", "critical-bug"]
}

client.configure_slack_integration(slack_config)
```

### Custom Workflows

Build custom workflows using the Workflow API:

```python
workflow = {
    "name": "Issue Triage",
    "steps": [
        {"action": "analyze", "params": {"types": ["classification"]}},
        {"action": "prioritize", "params": {"strategy": "impact_effort"}},
        {"action": "notify", "params": {"channels": ["slack", "email"]}}
    ]
}

client.create_workflow(workflow)
```

## Rate Limits and Best Practices

### Rate Limits
- **Standard**: 1000 requests/hour
- **Premium**: 10000 requests/hour
- **Enterprise**: Custom limits

### Best Practices
- Use batch operations when possible
- Implement exponential backoff for retries
- Cache results when appropriate
- Use webhooks instead of polling

### Error Handling

```python
try:
    result = client.analyze_issue(issue_url)
except RateLimitException:
    # Handle rate limiting
    time.sleep(60)
    result = client.analyze_issue(issue_url)
except APIException as e:
    # Handle API errors
    logger.error(f"API error: {e.message}")
```

## Monitoring and Observability

### Health Checks
```bash
curl https://api.piper-morgan.com/v1/health
```

### Metrics Endpoint
```bash
curl -H "Authorization: Bearer $PIPER_API_KEY" \
     https://api.piper-morgan.com/v1/metrics
```

### Logging
Enable detailed logging for troubleshooting:

```python
import logging
logging.getLogger('piper_morgan').setLevel(logging.DEBUG)
```

## Next Steps

- Explore the [complete API reference](../../../internal/architecture/current/api-reference.md)
- Check out [integration examples](../../../internal/development/tools/issue-intelligence-integration-examples.md)
- Review [webhook documentation](../../../internal/architecture/current/api-specification.md#webhooks)
- Join our [developer community](https://discord.gg/piper-morgan)

## Support

- **API Documentation**: [Full API Reference](../../../internal/architecture/current/api-reference.md)
- **Status Page**: [Service Status](../status/)
- **GitHub Issues**: Report bugs and request features
- **Community Discord**: Real-time support and discussions

---

*For production deployment considerations, see the [Production Guide](production.md). For development environment setup, see [Developer Quick Start](developers.md).*
