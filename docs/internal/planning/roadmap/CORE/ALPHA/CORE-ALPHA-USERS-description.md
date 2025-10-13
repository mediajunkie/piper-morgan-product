# CORE-ALPHA-USERS: Alpha User Onboarding Infrastructure

## Context
Alpha testing requires users to self-onboard with minimal friction. Currently, configuration is developer-focused with manual file editing. Alpha users need a guided setup experience.

## Current State
- Configuration requires manual editing of YAML/JSON files
- API keys scattered across different config files
- No first-run experience
- No preference management UI
- No validation of user setup

## Scope

### 1. Configuration Wizard
**First-run experience for new users:**
```
Welcome to Piper Morgan Alpha!

Let's get you set up:
1. API Keys (Required)
   - OpenAI/Anthropic key: [____]
   - GitHub token (optional): [____]
   - Notion key (optional): [____]
   - Slack token (optional): [____]

2. Basic Preferences
   - Default LLM model: [Claude/GPT-4]
   - Response style: [Concise/Detailed]
   - Auto-save conversations: [Y/N]

3. Integration Setup (Optional)
   - Connect GitHub repositories
   - Link Notion workspaces
   - Configure Slack workspace
```

### 2. API Key Management
- Secure storage (not plaintext in configs)
- Validation of keys on entry
- Clear error messages for invalid keys
- Ability to update/rotate keys
- Per-service key management

### 3. User Preferences System
```python
# ~/.piper/preferences.yaml
user:
  name: "Alpha User"
  email: "user@example.com"

llm:
  default_model: "claude-3-opus"
  temperature: 0.7
  max_tokens: 4000

behavior:
  response_style: "detailed"
  auto_save: true
  confirmation_required: ["delete", "publish"]

integrations:
  github:
    default_repo: "user/repo"
  notion:
    default_workspace: "workspace-id"
```

### 4. Validation & Health Checks
- Test each integration on setup
- Clear status dashboard
- Diagnostic commands
- Troubleshooting guide

### 5. Documentation
- Alpha quickstart guide
- Video walkthrough
- Common issues FAQ
- Discord/Slack community setup

## Acceptance Criteria
- [ ] New user can complete setup in <5 minutes
- [ ] All API keys validated on entry
- [ ] Preferences persist across sessions
- [ ] Clear error messages for all failure modes
- [ ] Health check command shows system status
- [ ] Documentation covers 90% of setup issues
- [ ] No manual file editing required for basic setup
- [ ] Rollback to manual config still possible

## Implementation Strategy

### Phase 1: Config Wizard CLI (Simplest)
```bash
piper setup
# Interactive CLI wizard
```

### Phase 2: Web-based Setup (Optional)
```bash
piper setup --web
# Opens localhost:8001/setup
```

### Phase 3: Preferences Management
```bash
piper config set llm.model claude-3-opus
piper config get llm.model
piper config list
```

## Technical Considerations
- Use existing config system, just add UI layer
- Store sensitive keys in OS keychain where possible
- Validate but don't test integrations (avoid API costs)
- Support both interactive and non-interactive setup

## Success Metrics
- Time to first successful query: <5 minutes
- Setup completion rate: >90%
- Support tickets for setup: <10%
- User satisfaction: >80%

## Time Estimate
2-3 days for basic CLI wizard
+1 day for web interface (optional)
+1 day for documentation

## Priority
High - Blocking alpha launch

## Notes
Keep it simple - this is alpha, not production. Focus on the critical path: getting users from zero to first successful interaction quickly.
