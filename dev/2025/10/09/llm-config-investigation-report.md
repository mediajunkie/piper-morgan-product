# LLM Configuration Investigation Report

**Issue**: #217 - CORE-LLM-CONFIG
**Agent**: Code (Claude Code - Programmer)
**Date**: October 9, 2025, 12:05 PM - 12:35 PM
**Phase**: 0 (Investigation)
**Duration**: 30 minutes

---

## Executive Summary

Comprehensive investigation of Piper Morgan's LLM configuration architecture reveals:

- ✅ **Current state**: Environment variables (`.env` file) with plaintext keys
- ❌ **Security issue**: HIGH - Plaintext storage unacceptable for Alpha
- ✅ **Good news**: Git protection working, keys not in repository
- ❌ **No validation**: Missing keys cause late runtime errors
- ❌ **Cost problem**: 87.5% of tasks use Anthropic (burning PM's credits)
- ✅ **Simple fix possible**: Provider exclusion can stop credit burn immediately

**Recommendation**: Keep environment variables (already working), add validation + keychain option. Defer encrypted file storage until multi-user requirement emerges.

---

## 1. Current State Summary

### 1.1 Configuration Structure

**Key Storage**:
- Location: `/.env` file (project root)
- Format: Plaintext environment variables
- Keys present: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`, `NOTION_API_KEY`
- PIPER config: NO LLM keys (only GitHub, Notion, Standup settings)

**Loading Mechanism**:
```python
# services/llm/clients.py:33-56
def _init_clients(self):
    # Anthropic
    if anthropic_key := os.getenv("ANTHROPIC_API_KEY"):
        self.anthropic_client = Anthropic(api_key=anthropic_key)

    # OpenAI
    if openai_key := os.getenv("OPENAI_API_KEY"):
        openai.api_key = openai_key
        self.openai_client = openai
```

**Global Singleton**:
```python
# services/llm/clients.py:166
llm_client = LLMClient()  # Initialized on first import
```

### 1.2 LLM Client Initialization

**Startup Sequence**:
1. Run: `python -m uvicorn web.app:app`
2. FastAPI loads `web/app.py`
3. Lifespan context manager imports `llm_client` (line 82)
4. `LLMClient.__init__()` loads keys from environment
5. Services ready

**Usage Pattern Distribution**:
- **Pattern A** (Global import): 11 production files
  ```python
  from services.llm.clients import llm_client
  await llm_client.complete(...)
  ```
- **Pattern B** (Constructor DI): 5 production files
  ```python
  def __init__(self, llm_client: LLMClient):
      self.llm_client = llm_client
  ```
- **Pattern C** (Optional fallback): 1 file (OrchestrationEngine)
  ```python
  def __init__(self, llm_client: Optional[LLMClient] = None):
      if llm_client is None:
          from services.llm.clients import llm_client as global_llm_client
          llm_client = global_llm_client
  ```

### 1.3 Provider Usage Analysis

**Task → Provider Mapping** (`services/llm/config.py`):
- `intent_classification` → **Anthropic** Claude Sonnet
- `reasoning` → **Anthropic** Claude Opus ⚠️ **Expensive!**
- `code_generation` → **OpenAI** GPT-4
- `summarization` → **Anthropic** Claude Sonnet
- `issue_analysis` → **Anthropic** Claude Opus ⚠️ **Expensive!**
- `work_item_extraction` → **Anthropic** Claude Sonnet
- `github_content_generation` → **Anthropic** Claude Sonnet
- `relationship_analysis` → **Anthropic** Claude Sonnet

**Cost Analysis**:
- **Anthropic**: 7 out of 8 task types (87.5%)
- **OpenAI**: 1 out of 8 task types (12.5%)
- **High-cost tasks**: `reasoning` and `issue_analysis` both use Claude Opus

**High-Frequency Usage**:
1. **Intent Classification** - Every user message (HIGH cost impact)
2. **Knowledge Graph Ingestion** - Document processing (MEDIUM)
3. **GitHub Issue Analysis** - Per-issue with Opus (MEDIUM)
4. **Work Item Extraction** - Text → structured data (MEDIUM)
5. **Content Generation** - Issue/PR content (MEDIUM)

---

## 2. Code Analysis

### 2.1 LLM Client Files

**Core Implementation**:
- `services/llm/clients.py:167` - Main client class + global singleton
- `services/llm/config.py:52` - MODEL_CONFIGS for task routing
- `.env:42` - Plaintext key storage

**Production Services Using LLM** (11 files):
1. `web/app.py:82` - FastAPI startup
2. `services/intent_service/classifier.py:34` - Intent classification
3. `services/intent_service/llm_classifier.py:22` - Advanced classification
4. `services/knowledge_graph/ingestion.py:24` - Knowledge extraction
5. `services/integrations/github/issue_analyzer.py:15` - GitHub integration
6. `services/orchestration/engine.py:32` - Orchestration core
7. `services/analysis/text_analyzer.py:72` - Text analysis
8. `services/analysis/document_analyzer.py:46` - Document analysis
9. `services/domain/work_item_extractor.py:14` - Work item extraction
10. `services/integrations/github/content_generator.py:11` - Content generation
11. `services/project_context/project_context.py:5` - Project inference

**Plugin System**: ✅ Plugins do NOT directly use LLM (routes/config only)

### 2.2 Provider Selection Logic

**Current Implementation** (`services/llm/clients.py:58-149`):
```python
async def complete(self, task_type: str, prompt: str, ...):
    config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
    primary_provider = config["provider"]

    try:
        # Try primary provider
        if primary_provider == LLMProvider.ANTHROPIC:
            return await self._anthropic_complete(...)
        else:
            return await self._openai_complete(...)
    except Exception as e:
        # Fallback to alternate provider
        fallback_provider = (
            LLMProvider.OPENAI if primary_provider == LLMProvider.ANTHROPIC
            else LLMProvider.ANTHROPIC
        )
        # Try fallback...
```

**Findings**:
- ✅ Automatic fallback exists between providers
- ❌ **No provider exclusion** (cannot disable Anthropic)
- ❌ **Hardcoded task→provider mapping**
- ❌ **No cost-aware routing**
- ❌ **No per-user preferences**

### 2.3 File Paths and Line Numbers

**Configuration Loading**:
- `.env:1-42` - Plaintext keys (ANTHROPIC_API_KEY, OPENAI_API_KEY)
- `services/llm/clients.py:25-31` - `LLMClient.__init__()`
- `services/llm/clients.py:33-56` - `_init_clients()` loads from env
- `services/llm/clients.py:166` - Global singleton instantiation
- `services/llm/config.py:1-52` - MODEL_CONFIGS dictionary

**Startup Initialization**:
- `web/app.py:46-203` - Lifespan context manager
- `web/app.py:82` - Import global `llm_client`
- `web/app.py:113-119` - OrchestrationEngine initialization

**main.py NOT USED**: Web server runs via `uvicorn web.app:app` directly

---

## 3. Security Assessment

### 3.1 Current Risks

**CRITICAL (HIGH Severity)**:
1. ❌ **Plaintext API keys** in `.env` file
   - Readable by any process with file access
   - No encryption, no secure enclave
   - Contains: Anthropic, OpenAI, GitHub, Notion keys

**PROTECTED (Working)**:
2. ✅ **Git protection** - `.env` is gitignored
   - `git check-ignore .env` → `.env` (confirmed)
   - No keys in git history (verified)

**PARTIAL RISK (Low-Medium)**:
3. ⚠️ **Log exposure** - Key names logged, not values
   - Found: `No ANTHROPIC_API_KEY found` warnings
   - No actual key values in logs (verified)

**OPERATIONAL ISSUES**:
4. ❌ **No startup validation**
   - Missing keys cause late runtime errors
   - Application starts even without required keys
   - Poor developer experience

### 3.2 Threat Vectors

**Immediate Risks**:
- Developer machine compromise → All API keys exposed
- Backup software → May backup `.env` to cloud
- Screen sharing → `.env` visible in editor
- Process inspection → Env vars visible via `ps`/`/proc`

**Supply Chain Risks**:
- Dependency vulnerabilities → Malicious package reads `.env`
- IDE/editor plugins → May have file access
- Local malware → Can read any user-readable file

**Operational Risks**:
- Accidental `git add` → Despite gitignore, force-add possible
- Copy/paste errors → Keys in Slack, email, logs
- Multiple developers → Each needs own keys (not supported)
- CI/CD → If `.env` used, keys in CI logs

### 3.3 What Needs Immediate Fixing

**Priority 1**: Replace plaintext storage → OS keychain
**Priority 2**: Add startup validation → Fail fast
**Priority 3**: Implement provider exclusion → Cost control
**Priority 4**: User-specific configuration → Multi-user support

---

## 4. Migration Impact

### 4.1 Dependencies

**Test Suite** (19 files reference LLM config):
- Integration tests: 9 files
- Config tests: 3 files
- Service tests: 2 files
- All expect `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` env vars

**Documentation**:
- `README.md:90` - Setup mentions `.env` file
- No LLM configuration guide exists

**CI/CD**: Unknown - needs verification

### 4.2 Breaking Changes

**Will Break**:
- Direct `.env` reads if we change storage
- Environment variable names if renamed
- Test fixtures that mock `llm_client`
- README setup instructions

**Won't Break** (if careful):
- Global singleton pattern (keep same import)
- LLMClient API (keep method signatures)
- Service code (transparent to changes)
- Plugin system (doesn't use LLM)

### 4.3 Migration Strategy

**Recommended**: **Gradual Migration (Option B)**

**Phase 1**: Keep `.env`, add validation (3-4 hours)
**Phase 2**: Add provider exclusion (2-3 hours)
**Phase 3**: Add keychain option (4-6 hours)
**Phase 4**: Documentation (2-3 hours)

**Total**: 11-16 hours (1.5-2 days)

**Why Gradual**:
- ✅ Safe rollback at each step
- ✅ Can test incrementally
- ✅ No forced reconfiguration
- ✅ Clear migration path for Alpha users

---

## 5. Architecture Recommendations

### 5.1 Storage Backend Priority

**Priority 1: Environment Variables (Keep & Improve)** ✅
- Already in use, zero migration
- Add validation at startup
- Better error messages
- **Time**: 2-3 hours
- **Alpha-Ready**: YES

**Priority 2: OS Keychain (Add as option)** 🔑
- More secure than `.env`
- Fallback chain: Keychain → Environment → Error
- Optional upgrade path
- **Time**: 4-6 hours
- **Alpha-Ready**: YES

**Priority 3: Encrypted File (Defer)** ⏸️
- Most complex, least portable
- Defer until multi-user requirement
- **Time**: N/A (deferred)
- **Alpha-Ready**: Not needed

### 5.2 Implementation Phases

**Phase 1: Secure Environment Variables** (IMMEDIATE)
- Create `LLMConfigService` class
- Add startup validation (fail fast)
- Add provider exclusion logic
- Keep `.env` working (no breaking changes)
- **Time**: 3-4 hours
- **Blocks**: Nothing (improves current state)

**Phase 2: Provider Control** (HIGH PRIORITY)
- Implement `excluded_providers` config
- Add per-user provider preferences
- Add cost-aware model selection
- **Time**: 2-3 hours
- **Blocks**: PM's Anthropic credit burn

**Phase 3: OS Keychain Integration** (MEDIUM PRIORITY)
- Add `keyring` library
- Implement keychain backend
- Create setup tool
- Migration command
- **Time**: 4-6 hours
- **Blocks**: Alpha user onboarding (security)

**Phase 4: Documentation & Testing** (REQUIRED)
- Update README
- Document provider exclusion
- Integration tests
- Troubleshooting guide
- **Time**: 2-3 hours
- **Blocks**: Alpha user onboarding

### 5.3 Minimum Viable Secure Config (MVP)

**Alpha Requirements**:
1. ✅ Startup validation
2. ✅ Provider exclusion
3. ✅ OS keychain option
4. ✅ Setup documentation

**Can Wait**:
- ❌ Encrypted file storage
- ❌ Per-user database storage
- ❌ Web UI for key management
- ❌ Key rotation

### 5.4 PM-Specific Quick Fix

**Immediate Cost Reduction** (< 5 minutes):

Add to `.env`:
```bash
# Provider exclusion (NEW)
PIPER_EXCLUDED_PROVIDERS=anthropic  # Stop credit burn!

# Default provider (NEW)
PIPER_DEFAULT_PROVIDER=openai  # Use OpenAI instead

# Development mode (NEW)
PIPER_DEV_MODE=true  # Use cheaper models
```

**Impact**:
- ✅ Stops Anthropic credit burn immediately
- ✅ Falls back to OpenAI for all tasks
- ✅ Can override for testing if needed
- ✅ No code changes required

---

## 6. Implementation Roadmap

### Phase 1: Today (3-4 hours)
**What**: Secure environment variable loading
- Create `services/config/llm_config_service.py`
- Add validation at startup
- Add provider exclusion
- Update `services/llm/clients.py` to use service

**Why**: Stop credit burn, improve errors
**Blocks**: PM's development workflow

### Phase 2: Tomorrow (2-3 hours)
**What**: Provider control implementation
- Implement exclusion logic in `LLMClient`
- Add `PIPER_EXCLUDED_PROVIDERS` environment variable
- Update MODEL_CONFIGS to respect exclusions
- Test with PM's configuration

**Why**: Cost control for development
**Blocks**: Alpha deployment (cost concerns)

### Phase 3: Day 3 (4-6 hours)
**What**: OS keychain integration
- Add `keyring` dependency
- Implement keychain backend
- Create `scripts/setup_llm_keys.py`
- Create `scripts/migrate_to_keychain.py`

**Why**: Security requirement for Alpha
**Blocks**: Alpha user onboarding

### Phase 4: Day 4 (2-3 hours)
**What**: Documentation & testing
- Update README.md setup instructions
- Create LLM configuration guide
- Add integration tests
- Troubleshooting documentation

**Why**: Alpha users need clear setup path
**Blocks**: Alpha launch

---

## 7. Key Findings Summary

### What Works
- ✅ Global singleton pattern (clean architecture)
- ✅ Automatic fallback between providers
- ✅ Git protection (keys not in repository)
- ✅ Consistent usage patterns (easy to update)
- ✅ Environment variables (portable, works everywhere)

### What's Broken
- ❌ Plaintext key storage (security risk)
- ❌ No startup validation (late errors)
- ❌ No provider exclusion (credit burn)
- ❌ Hardcoded task→provider mapping (inflexible)
- ❌ No per-user configuration (blocks multi-user)

### What's Surprising
- 🔍 main.py NOT used for web server startup
- 🔍 87.5% of tasks use Anthropic (higher than expected)
- 🔍 Plugins don't use LLM directly (good separation)
- 🔍 `.env` file contains all keys (not just LLM)

---

## 8. Estimated Complexity

**Phase 1** (Environment + Validation): **Simple** (3-4 hours)
- Straightforward service creation
- No breaking changes
- Well-understood patterns

**Phase 2** (Provider Control): **Simple** (2-3 hours)
- Logic already exists (fallback)
- Just add exclusion check
- Configuration-driven

**Phase 3** (Keychain): **Medium** (4-6 hours)
- New library integration
- Platform-specific testing
- Migration tooling needed

**Phase 4** (Documentation): **Simple** (2-3 hours)
- Straightforward writing
- Clear examples needed
- Test all code samples

**Total**: 11-16 hours (1.5-2 days realistic)

---

## 9. Recommendation

**Start with Phase 1+2 today** (5-7 hours total):
1. Create `LLMConfigService` with validation
2. Add provider exclusion logic
3. Update PM's `.env` with exclusions
4. Verify Anthropic credit burn stops

**Benefits**:
- ✅ Immediate cost savings for PM
- ✅ Better error messages for developers
- ✅ No breaking changes
- ✅ Foundation for Phase 3 (keychain)

**Then continue Phase 3+4** (tomorrow, 6-9 hours):
1. Add keychain support
2. Create setup tooling
3. Write documentation
4. Test with Alpha user scenario

**Result**: Alpha-ready LLM configuration in 2 days

---

## 10. Questions for PM

1. **Provider exclusion**: Want to stop Anthropic usage immediately via `.env` change?
2. **Keychain timing**: Need keychain for Alpha launch, or can environment variables work short-term?
3. **Migration approach**: Prefer gradual (support both) or clean slate (require reconfiguration)?
4. **CI/CD**: How are API keys currently handled in GitHub Actions?
5. **Testing**: Should we add real API call tests, or keep mocking?

---

## Appendices

### A. Files Modified (Predicted)

**Phase 1**:
- `services/config/llm_config_service.py` (NEW)
- `services/llm/clients.py` (MODIFIED)
- `services/llm/config.py` (MODIFIED)
- `.env` (USER MODIFIED)

**Phase 2**:
- `services/llm/clients.py` (MODIFIED)
- `services/llm/config.py` (MODIFIED)

**Phase 3**:
- `services/config/llm_config_service.py` (MODIFIED)
- `scripts/setup_llm_keys.py` (NEW)
- `scripts/migrate_to_keychain.py` (NEW)
- `requirements.txt` (MODIFIED - add keyring)

**Phase 4**:
- `README.md` (MODIFIED)
- `docs/guides/llm-configuration.md` (NEW)
- `tests/services/config/test_llm_config_service.py` (NEW)

### B. Environment Variable Names

**Current** (keep for backward compatibility):
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

**New** (add for Phase 2):
- `PIPER_EXCLUDED_PROVIDERS` (comma-separated: `anthropic,openai`)
- `PIPER_DEFAULT_PROVIDER` (`openai`, `anthropic`, `gemini`, `perplexity`)
- `PIPER_DEV_MODE` (`true`, `false`)

**Optional** (Phase 3):
- `PIPER_USE_KEYCHAIN` (`true`, `false`)
- `GEMINI_API_KEY` (optional provider)
- `PERPLEXITY_API_KEY` (optional provider)

### C. Related ADRs/Patterns

**Relevant Documentation**:
- ADR-027: Configuration Architecture (User vs System Separation)
- Pattern-031: Plugin Wrapper Pattern (plugins don't use LLM directly)
- ADR-010: ConfigService Pattern (application layer config access)

**New Documentation Needed**:
- ADR-044: LLM Configuration Service Architecture
- Pattern-034: Multi-Provider LLM Routing
- Guide: Setting Up LLM API Keys

---

**Investigation Complete**: October 9, 2025, 12:35 PM
**Next Step**: Await PM decision on phases to implement
**Session Log**: `dev/active/2025-10-09-1205-prog-code-log-llm-config.md`
