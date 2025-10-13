# CORE-LLM-CONFIG #217: User Configuration for LLM API Keys

**Priority**: P0 - Blocks Alpha users
**Epic**: Sprint A1 - Critical Infrastructure
**Estimated Time**: 1-2 days
**Date**: October 9, 2025

---

## Problem Statement

### Current State
- LLM API keys are hardcoded or stored in plaintext configuration files
- No user-specific key management
- No secure storage mechanism
- Cannot easily switch between LLM providers
- PM's Anthropic credits being consumed during development

### Impact
- **Blocks Alpha users**: Cannot onboard users without secure key management
- **Security risk**: Plaintext key storage is unacceptable
- **Development cost**: Burning Anthropic credits unnecessarily
- **Flexibility**: Cannot test multiple LLM providers easily

---

## Goals

### Primary Goals
1. **Secure Key Storage**: Never store API keys in plaintext
2. **User-Specific Configuration**: Each user manages their own keys
3. **Multi-Provider Support**: Support multiple LLM providers (OpenAI, Anthropic, Gemini, Perplexity)
4. **Development Efficiency**: Exclude expensive providers during development

### Secondary Goals
5. **Easy Setup**: Clear onboarding for new users
6. **Key Validation**: Verify keys work before saving
7. **Migration Path**: Smooth transition from current config
8. **Documentation**: User-friendly setup instructions

---

## Current Configuration Structure

**Location**: `config/PIPER.user.md`
**Format**: Markdown configuration file
**Issue**: Keys likely stored in plaintext or not properly isolated

---

## Requirements

### Phase 1: Infrastructure - Secure Key Storage

**Objective**: Build foundation for secure, user-specific key management

#### 1.1 Configuration Service
Create `services/config/llm_config_service.py` with:
- User-specific configuration loading
- Multiple storage backend support
- Key validation on load
- Clear error messages for setup issues

#### 1.2 Storage Backends (Priority Order)
Implement with fallback chain:

**Priority 1: Environment Variables** (simplest, works everywhere)
```bash
export PIPER_OPENAI_API_KEY="sk-..."
export PIPER_ANTHROPIC_API_KEY="sk-ant-..."
export PIPER_GEMINI_API_KEY="..."
```

**Priority 2: OS Keychain** (most secure, OS-native)
- macOS: Keychain Access
- Linux: Secret Service API / gnome-keyring
- Windows: Credential Manager
- Library: `keyring` Python package

**Priority 3: Encrypted File Storage** (fallback)
- Encrypted JSON file in `~/.piper/credentials.enc`
- User-specific encryption key (derived from system info or user password)
- Never store plaintext

#### 1.3 Key Features
- **Read-only in production**: Keys loaded at startup, never modified
- **Write operations**: CLI tool or setup script for adding/updating keys
- **Validation**: Test API call before accepting key
- **Clear errors**: Tell user exactly what's missing/wrong

---

### Phase 2: Multi-Provider Support

**Objective**: Support multiple LLM providers with intelligent routing

#### 2.1 Provider Configuration
```python
LLM_PROVIDERS = {
    "openai": {
        "env_var": "PIPER_OPENAI_API_KEY",
        "keychain_service": "piper-openai",
        "required": True,  # Must be configured
        "validation_endpoint": "https://api.openai.com/v1/models",
    },
    "anthropic": {
        "env_var": "PIPER_ANTHROPIC_API_KEY",
        "keychain_service": "piper-anthropic",
        "required": False,  # Optional during development
        "validation_endpoint": "https://api.anthropic.com/v1/messages",
    },
    "gemini": {
        "env_var": "PIPER_GEMINI_API_KEY",
        "keychain_service": "piper-gemini",
        "required": False,
        "validation_endpoint": "https://generativelanguage.googleapis.com/v1/models",
    },
    "perplexity": {
        "env_var": "PIPER_PERPLEXITY_API_KEY",
        "keychain_service": "piper-perplexity",
        "required": False,
        "validation_endpoint": "https://api.perplexity.ai/models",
    },
}
```

#### 2.2 Provider Selection Logic
- Default provider per user (configurable)
- Fallback chain if primary unavailable
- Development vs production provider preferences
- Cost-aware routing (cheap providers for dev)

---

### Phase 3: PM Configuration (xian/@mediajunkie)

**Objective**: Set up PM's development environment with cost-efficient providers

#### 3.1 Required Keys for PM
- ✅ **OpenAI**: Primary provider for development (gpt-4o, gpt-4o-mini)
- ✅ **Gemini**: Secondary provider for testing (gemini-pro, gemini-flash)
- ⚠️ **Perplexity**: Optional for search/research features
- ❌ **Anthropic**: EXCLUDED during development (save credits)

#### 3.2 Development Configuration
```yaml
# PM's development settings
default_provider: openai
development_mode: true

provider_preferences:
  general: openai        # Use OpenAI for general queries
  coding: openai         # Use OpenAI for code generation
  research: gemini       # Use Gemini for research (if available)

excluded_providers:
  - anthropic           # Don't use during development

fallback_chain:
  - openai
  - gemini
  # Anthropic excluded from fallback
```

#### 3.3 Setup Script for PM
Create `scripts/setup_pm_keys.py`:
1. Interactive prompt for each key
2. Validate each key with test API call
3. Store in OS keychain (preferred) or encrypted file
4. Configure development preferences
5. Verify Piper can load all keys
6. Show cost estimates per provider

---

### Phase 4: Exclusion Logic

**Objective**: Prevent accidental use of expensive providers during development

#### 4.1 Provider Exclusion
```python
class LLMConfigService:
    def get_available_providers(self) -> List[str]:
        """Return only non-excluded providers"""
        all_providers = self._load_configured_providers()
        excluded = self._get_excluded_providers()
        return [p for p in all_providers if p not in excluded]

    def _get_excluded_providers(self) -> List[str]:
        """Check both config and environment for exclusions"""
        # Priority 1: Environment variable
        if os.getenv("PIPER_EXCLUDE_PROVIDERS"):
            return os.getenv("PIPER_EXCLUDE_PROVIDERS").split(",")

        # Priority 2: User config
        return self.user_config.get("excluded_providers", [])
```

#### 4.2 Safety Checks
- **Startup validation**: Log which providers are active/excluded
- **Request-time check**: Block requests to excluded providers
- **Clear errors**: Tell user if they try to use excluded provider
- **Override capability**: Allow explicit override for testing

---

## Implementation Phases

### Phase 0: Investigation & Planning (30-60 min)
**Agent**: Code Agent
- [ ] Examine current config structure (`config/PIPER.user.md`)
- [ ] Find where LLM clients are initialized
- [ ] Document current key loading mechanism
- [ ] Identify all places that need updates
- [ ] Recommend storage backend priority order

### Phase 1: Core Infrastructure (3-4 hours)
**Agent**: Code Agent
- [ ] Create `LLMConfigService` class
- [ ] Implement environment variable storage (Priority 1)
- [ ] Implement OS keychain storage (Priority 2)
- [ ] Implement encrypted file storage (Priority 3)
- [ ] Add key validation for each provider
- [ ] Write unit tests for config loading

### Phase 2: Multi-Provider Support (2-3 hours)
**Agent**: Code Agent
- [ ] Define provider configurations
- [ ] Implement provider selection logic
- [ ] Add fallback chain support
- [ ] Update LLM client initialization to use config service
- [ ] Add provider exclusion logic
- [ ] Write integration tests

### Phase 3: Setup Tooling (2-3 hours)
**Agent**: Code Agent
- [ ] Create setup script for adding keys
- [ ] Add validation for each provider's API
- [ ] Build interactive CLI for key management
- [ ] Create migration script from current config
- [ ] Write user documentation

### Phase 4: PM Configuration (1 hour)
**Agent**: Code Agent (with PM guidance)
- [ ] Run setup script to configure PM's keys
- [ ] Verify OpenAI key works
- [ ] Verify Gemini key works
- [ ] Verify Perplexity key (optional)
- [ ] Confirm Anthropic is excluded
- [ ] Test Piper with new configuration

### Phase 5: Testing & Validation (1-2 hours)
**Agent**: Both agents
- [ ] Run full test suite with new config
- [ ] Verify no plaintext keys in any files
- [ ] Test provider fallback logic
- [ ] Verify exclusion logic works
- [ ] Test cost-efficient routing
- [ ] Document setup for Alpha users

---

## Acceptance Criteria

### Security ✅
- [ ] No API keys stored in plaintext anywhere
- [ ] Keys stored in OS keychain or encrypted file
- [ ] Git-ignored credential files (if used)
- [ ] No keys in logs or error messages

### Functionality ✅
- [ ] Multiple providers configured and working
- [ ] Provider fallback chain operational
- [ ] Key validation on setup
- [ ] Clear error messages for missing/invalid keys

### PM Configuration ✅
- [ ] PM's OpenAI key configured and working
- [ ] PM's Gemini key configured and working
- [ ] Anthropic provider excluded during development
- [ ] Piper successfully makes requests with new config

### User Experience ✅
- [ ] Simple setup process (< 5 minutes)
- [ ] Clear documentation for Alpha users
- [ ] Migration from current config works
- [ ] Helpful error messages

### Development ✅
- [ ] Cost-efficient provider selection working
- [ ] Excluded providers respected
- [ ] Easy to override for testing
- [ ] Logging shows which provider is being used

---

## Success Validation

```bash
# 1. Security check - no plaintext keys
grep -r "sk-" config/ | grep -v ".example" | grep -v ".gitignore"
# Expected: No results (or only in .example files)

# 2. Config service loads successfully
python -c "from services.config.llm_config_service import LLMConfigService; svc = LLMConfigService(); print(f'Loaded {len(svc.get_available_providers())} providers')"
# Expected: Shows configured providers

# 3. Anthropic excluded during development
python -c "from services.config.llm_config_service import LLMConfigService; svc = LLMConfigService(); print('anthropic' not in svc.get_available_providers())"
# Expected: True

# 4. OpenAI works
python -c "from services.config.llm_config_service import LLMConfigService; svc = LLMConfigService(); print(svc.validate_provider('openai'))"
# Expected: True

# 5. Piper runs with new config
python main.py
# Expected: Starts successfully, logs show OpenAI as primary provider
```

---

## STOP Conditions

- If OS keychain integration is blocked by platform issues
- If provider API validation is too complex
- If migration from current config breaks existing functionality
- If encrypted file storage has security concerns

In any STOP condition: Document the issue, implement simpler fallback, and escalate.

---

## Related Issues

- **Blocks**: Alpha user onboarding
- **Enables**: Multi-provider LLM routing
- **Reduces**: Development costs (Anthropic credits)
- **Security**: Proper credential management

---

## Documentation Requirements

### For Users
- [ ] Setup guide: "Getting Started with Piper"
- [ ] How to add/update API keys
- [ ] Supported providers and costs
- [ ] Troubleshooting common issues

### For Developers
- [ ] Architecture: How config service works
- [ ] Adding new LLM providers
- [ ] Testing with different providers
- [ ] Provider selection logic

---

## Time Estimate

**Total**: 10-13 hours
- Phase 0: 0.5-1 hour (investigation)
- Phase 1: 3-4 hours (infrastructure)
- Phase 2: 2-3 hours (multi-provider)
- Phase 3: 2-3 hours (setup tooling)
- Phase 4: 1 hour (PM config)
- Phase 5: 1-2 hours (testing)

**Realistic Schedule**: 1.5-2 days with breaks and meetings

---

## Notes

- **Start with simplest storage**: Environment variables, then add keychain
- **Security first**: Never compromise on plaintext storage
- **User experience**: Make setup as simple as possible
- **Cost awareness**: Development should use cheap providers
- **Testing**: Validate with real API calls, not mocks

---

**This is the main course.** 🥩 Take time to do it right.
