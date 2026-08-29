# CORE-USERS-API: Production API Key Management

## Context
Alpha users need secure API key management for LLM services and integrations. Current implementation uses plaintext config files unsuitable for production.

## Current State
```yaml
# Current: config/llm.yaml (plaintext)
openai_api_key: "sk-..."
anthropic_api_key: "sk-ant-..."
```

## Scope

### 1. Secure Storage
- OS keychain integration (primary)
  - macOS: Keychain
  - Linux: Secret Service
  - Windows: Credential Manager
- Encrypted file fallback
- Environment variable support
- Never store in plaintext configs

### 2. API Key Service
```python
class APIKeyManager:
    async def store_key(self, service: str, key: str, user_id: str):
        """Store API key securely"""

    async def retrieve_key(self, service: str, user_id: str) -> str:
        """Retrieve API key for service"""

    async def rotate_key(self, service: str, old_key: str, new_key: str):
        """Rotate API key with zero downtime"""

    async def validate_key(self, service: str, key: str) -> bool:
        """Validate key works with service"""
```

### 3. User Experience
- Setup wizard prompts for keys
- Validation on entry
- Clear error messages for invalid keys
- Key rotation reminders
- Multi-user key isolation

### 4. Supported Services
- OpenAI
- Anthropic
- GitHub (tokens)
- Notion
- Slack
- Custom endpoints

## Acceptance Criteria
- [ ] OS keychain integration working
- [ ] Encrypted fallback for unsupported systems
- [ ] API keys never in plaintext files
- [ ] Validation for all key types
- [ ] Multi-user key isolation
- [ ] Key rotation supported
- [ ] Migration from current configs
- [ ] Tests for all storage methods

## Security Requirements
- Keys encrypted at rest
- Keys isolated per user
- No keys in logs
- No keys in error messages
- Secure key transmission
- Audit trail for key access

## Time Estimate
1-2 days

## Priority
High - Blocking for Alpha users

## Dependencies
- CORE-USERS-ONBOARDING (for setup wizard integration)
