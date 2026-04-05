# Gameplan: #940 — LLM Config Single-Provider Setup

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing LLM config: `services/llm/config.py` with hardcoded task→provider mapping
- [x] Existing setup wizard: `web/api/routes/setup.py` + `web/static/js/setup.js`

**Task**: Fix three interconnected problems:
1. Setup UI mandates OpenAI — should let user choose any provider
2. Task configs hardcode providers — should use user's configured provider
3. No runtime key failure handling — should detect and surface errors clearly

**Current state**:
- `services/llm/config.py`: 5 task types, 4 pinned to Anthropic, 1 to OpenAI
- `services/config/llm_config_service.py`: OpenAI marked `required=True` (line 106)
- `web/static/js/setup.js`: OpenAI validation gates "Next" button
- `services/llm/clients.py`: 2-tier fallback (primary ↔ swap), RuntimeError if both fail
- `services/intent_service/conversational_floor.py`: catch-all returns canned fallback

### Part A.2: Worktree Assessment

- [x] Single agent, sequential work
- [x] Tightly coupled files requiring atomic commits
- **SKIP WORKTREE** — single agent, 6-8 files, sequential edits

### Part B: PM Verification

This is a fix-broken-functionality task. The scope is clear from #940 and the UAT findings.

### Part C: PROCEED

---

## Phase 0: Investigation (DONE — from UAT root cause analysis)

Already completed during April 3 UAT session. Key findings documented in:
- `dev/active/memo-cxo-pm-to-lead-dev-uat-findings-2026-04-03.md`
- Session log `dev/active/2026-04-03-2200-lead-code-opus-log.md`

---

## Phase 0.5: Frontend-Backend Contract

Applies — setup UI changes + backend config changes.

| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| validate-key | /validate-key | /setup | /setup/validate-key |
| complete | /complete | /setup | /setup/complete |
| check-keychain | /check-keychain/{provider} | /setup | /setup/check-keychain/{provider} |

No new endpoints needed — we're modifying existing ones.

---

## Phase 0.6: Data Flow

Provider selection flows through:
1. **Setup UI** → user picks provider, enters key
2. **`/setup/validate-key`** → validates key against provider API
3. **`/setup/complete`** → stores key in user_api_keys table + global keychain
4. **`LLMConfigService`** → reads keys from keychain/env at startup
5. **`LLMClient`** → uses config to route task types to providers
6. **`ConversationalFloor`** → calls `LLMClient.complete(task_type="conversation")`

Change needed: Steps 1-3 become provider-agnostic. Step 5 uses user's provider instead of hardcoded mapping.

---

## Phase 1: Remove Hardcoded Provider Assignments

**Files**: `services/llm/config.py`, `services/llm/clients.py`

### Changes:
1. **`config.py`**: Remove `provider` field from task configs. Keep model preferences per-provider but don't assign tasks to providers.
2. **`clients.py`**: `complete()` method should use `LLMConfigService.get_default_provider()` instead of reading provider from task config. Fallback chain already exists.

### Acceptance Criteria:
- [ ] No task type is pinned to a specific provider
- [ ] `LLMClient.complete()` uses the user's configured/default provider
- [ ] Fallback still works if primary provider fails
- [ ] Tests pass: `pytest tests/unit/services/llm/ -v`

---

## Phase 2: Single-Provider Setup UI

**Files**: `web/static/js/setup.js`, `web/api/routes/setup.py`, `services/config/llm_config_service.py`

### Changes:
1. **`setup.js`**: Replace OpenAI-mandatory gating with "validate any one provider to proceed"
   - Any validated provider (OpenAI OR Anthropic) enables the Next button
   - Provider selection is a choice, not a hierarchy
2. **`llm_config_service.py`**: Remove `required=True` from OpenAI config (line 106). All providers are optional; system requires at least one.
3. **`setup.py`**: `/setup/status` endpoint (line 241) currently checks only OpenAI keys — change to check any active key.

### Acceptance Criteria:
- [ ] User can complete setup with only an Anthropic key (no OpenAI)
- [ ] User can complete setup with only an OpenAI key (no Anthropic)
- [ ] "Next" button enables when ANY provider is validated
- [ ] `/setup/status` checks for any active key, not just OpenAI

---

## Phase 3: Key Failure Handling

**Files**: `services/intent_service/conversational_floor.py`, `services/llm/clients.py`

### Changes:
1. **`conversational_floor.py`**: Differentiate LLM errors in the catch block (line 366):
   - Auth/key errors → "My API key seems to have expired. Please check Settings."
   - Connection/timeout → "Service temporarily unavailable, please try again."
   - Unknown → current graceful fallback
2. **`clients.py`**: Catch specific exception types (401/403 = auth, timeout = transient, 404 = config) instead of generic Exception.

### Acceptance Criteria:
- [ ] Auth failure produces user-actionable message (not canned template)
- [ ] Transient failure produces retry-suggesting message
- [ ] Floor responses are distinguishable by failure type
- [ ] Tests: add unit tests for each error path

---

## Phase Z: Verification & Handoff

### Evidence Required:
- [ ] All unit tests pass: `pytest tests/unit/ -v`
- [ ] Manual test: setup with only Anthropic key → floor responds with LLM
- [ ] Manual test: setup with only OpenAI key → floor responds with LLM
- [ ] Manual test: invalid key → user-actionable error message
- [ ] No regressions in existing setup flow

### Documentation:
- [ ] Session log updated with evidence
- [ ] #940 updated with implementation evidence
- [ ] PR or direct commit to main

---

## STOP Conditions
- If setup wizard has undocumented dependencies on OpenAI
- If LLMClient fallback chain has side effects not covered by investigation
- If existing tests rely on hardcoded provider assignments in ways that require redesign
