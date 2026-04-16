# Session Log: 2026-04-15-0635-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Wednesday, April 15, 2026
**Start Time**: 6:35 AM

## Session Objectives

1. Close M2b gate (#929 verification with Gemini key)
2. Act on Architect's #970/#971 decisions (delete dead code)
3. Begin M2c (pending CXO reply on #950)

## Work Log

### 6:35 AM - Session Start
- Created session log
- Synced with origin/main — up to date
- BRIEFING-CURRENT-STATE updated overnight (M2 sprint active, M2b mostly done)
- Mailbox: 1 item — Architect reply on #970/#971

### 6:36 AM - Architect Reply (read, moved to read)
- **#970 (ServiceRegistry)**: (C) Leave as-is. MCPB doesn't use ServiceRegistry;
  rewiring is intermediate step to nowhere. Revisit only if singleton causes
  actual bugs.
- **#971 (Pattern-012 adapters)**: (C) Delete. Dead code, no MCPB reuse path.
  Write fresh if needed.
- **ProviderSelector**: Also delete. Superseded by provider-agnostic #940.
- Principle: "don't maintain infrastructure for a future that hasn't been designed yet"

### 7:00 AM - #971 Delete Pattern-012 Adapters + ProviderSelector
- Deleted 10 files: 7 adapter files, provider_selector.py, 2 test files
- Edited 2 files: llm_domain_service.py (removed ~160 lines of adapter
  infrastructure), test_llm_domain_service.py (removed mock_provider_selector)
- Tests: 6125 passed, 0 failures (test count dropped by ~120 from deleted tests)
- 3 pre-existing calendar test collection errors (unrelated)

### 6:40 AM - #929 AAXT Verification
- Verified Gemini key works (gemini-2.5-flash, not 1.5-flash — model name change)
- Anthropic key worked from CLI but server had stale keychain key
- Updated keychain with .env key, restarted server
- **AAXT results: 4/5 PASS, 1 FAIL**
  - ✅ Task Lifecycle: full CRUD cycle works
  - ✅ Mid-Flow Interruption: topic switch + return works
  - ✅ Cross-Domain Voice: consistent personality
  - ✅ Capability Honesty: honest about limitations
  - ❌ Context Retention: "that" not resolved to prior topic — #922 issue
- The 1 failure is a genuine quality finding (conversation continuity),
  not a test infrastructure problem. AAXT is working correctly.
