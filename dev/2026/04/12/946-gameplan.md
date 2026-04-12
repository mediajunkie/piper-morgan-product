# Gameplan: #946 — LLM keychain consent fix

## Phase -1: Infrastructure Verification

**Task**: Ensure the system only uses LLM API keys the user explicitly authorized during setup. Stop silently loading stale keys from the macOS keychain.

**Approach**: Option C (consent flag) — store an `authorized_providers` list in the keychain. `get_configured_providers()` filters to only authorized providers. No data loss, works at server startup.

**Worktree**: SKIP — single agent, 3-4 files, sequential.

## Phase 1: TDD

Write tests for:
1. `get_configured_providers()` only returns providers in the authorized list
2. Provider with key but NOT authorized → not returned
3. Provider with key AND authorized → returned
4. No authorized list stored → legacy behavior (all configured providers returned) for backwards compatibility

## Phase 2: Store authorized providers during setup

**File**: `web/api/routes/setup.py`

In `complete_setup()`, after storing the user's key:
- Build authorized list from which keys were provided (openai, anthropic, or both)
- Store as `authorized_llm_providers` in keychain (comma-separated string)

## Phase 3: Filter by authorized providers at runtime

**File**: `services/config/llm_config_service.py`

Update `get_configured_providers()`:
- Read `authorized_llm_providers` from keychain
- If present, filter the configured list to only include authorized providers
- If absent (legacy/migration), return all configured (backwards compatible)

## Phase 4: Verify

- Restart server
- Confirm only the authorized provider is initialized
- Confirm stale keys from other providers are ignored

## STOP Conditions

- If clearing authorized_providers list would break existing installs → ensure backwards compat
- If server startup needs both providers (e.g., for classification vs conversation) → document the constraint
