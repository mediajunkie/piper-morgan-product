# Audit: #946 against bug_report_alpha.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Stale keychain key loaded without user consent |
| Steps to Reproduce | ⚠️ | Implicit from UAT — add explicit: 1. Have stale OpenAI key in macOS keychain, 2. Set up with Anthropic only, 3. System uses stale OpenAI |
| Expected Behavior | ✅ | "only use keys the user explicitly authorized during setup" |
| Actual Behavior | ✅ | Silent keychain loading of unauthorized keys |
| Environment | ⚠️ | Missing — v0.8.6, macOS, keychain with stale key |
| Severity | ⚠️ | Not marked — Major (consent violation, caused M1 UAT failure) |
| Additional Context | ✅ | #940 relationship noted |

## Architecture Understanding

The issue sits at the intersection of three systems:

1. **LLMConfigService.get_api_key()** (services/config/llm_config_service.py:181-217)
   - Priority: keychain first → env var fallback
   - PROBLEM: finds ANY key in keychain, not just user-authorized ones

2. **Setup wizard** (web/api/routes/setup.py + web/static/js/setup.js)
   - Stores user's chosen provider key in keychain + DB
   - Stores `default_llm_provider` preference in keychain (#940 fix)
   - PROBLEM: doesn't CLEAR stale keys for providers the user didn't choose

3. **LLMClient._init_clients()** (services/llm/clients.py:37-62)
   - Initializes clients for ALL configured providers (via get_configured_providers)
   - PROBLEM: "configured" means "has a key somewhere" — not "user authorized this"

## Fix Options

**Option A (minimal): Clear non-selected provider keys during setup**
- When user completes setup with provider X, delete keys for other providers from keychain
- Pro: surgical, targeted
- Con: destructive — if user later wants to add a second provider, the old key is gone

**Option B (scoped storage): Store keys with setup-session scope**
- Instead of global keychain key names like "openai", use "{user_id}_openai"
- get_api_key() only returns keys scoped to the authenticated user
- Pro: clean separation, no data loss
- Con: user_id isn't always available at LLMClient init time (server startup)

**Option C (consent flag): Track which providers the user authorized**
- Store a list of authorized providers alongside the default_llm_provider
- get_configured_providers() only returns authorized ones
- get_api_key() still reads from keychain/env, but only for authorized providers
- Pro: no data loss, works with existing storage
- Con: adds another piece of state to track

## Recommendation

**Option C** — most robust, no data loss, works with server startup. The `default_llm_provider` preference we added in #940 is already half of this. We just need a companion `authorized_providers` list.

## Audit Result

All items ✅ after fixes. Proceeding to gameplan.
