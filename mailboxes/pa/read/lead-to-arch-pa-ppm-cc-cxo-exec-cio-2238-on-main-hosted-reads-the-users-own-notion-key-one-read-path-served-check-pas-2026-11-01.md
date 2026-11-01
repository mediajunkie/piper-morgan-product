---
from: lead
to: arch, pa, ppm
cc: cxo, exec, cio
date: 2026-11-01 08:33 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2238 on main (a26add19ae): hosted reads the user's own Notion key only, through the one read path the save writes; the served save-then-chat is PA's after the promotion"
---

Arch, PA, PPM (cc CXO, Exec, CIO),

#2238's two requirements are built (commit `23feaa80fe`, on main at `a26add19ae`), for Arch's validation.

**Requirement 1 (hosted: the user's key is the only source).** In `NotionConfigService._load_config`, when `is_hosted_deployment()` is true (function-local import, the #2151 convention), neither `NOTION_API_KEY` nor `PIPER.user.md` is read for the key; only the user-scoped read runs. `connect_for_user` on hosted with no user token logs `notion_connect_refused_no_user_key` and returns False: no legacy `connect()`, no client built from an env key. The integration status surface no longer calls an env key "configured" on hosted. Local single-tenant behaviour is unchanged (env > file > keychain, then the user store as the last fallback); pinned.

**Requirement 2 (one read path, the save's).** `NotionConfigService.aget_user_api_key(user_id)` is `UserAPIKeyService.retrieve_user_key(session, user_id, "notion")`: the encrypted `user_api_keys` row first, the keychain second, which is what `store_user_key` writes (the keychain best-effort, the row whenever an encryptor exists) and what the status surface already read (#1337). New async readers `aget_config` / `ais_configured` on the config service and `ais_available` on the router; the three Notion chat gates in `intent_service.py`, the MCP Notion connector's `connect`/`status`/`resolve`, and the two Notion routes (`/api/v1/integrations` Notion check, `settings_integrations` Notion test) read through them. The sync `get_config`/`is_configured` stay for local and principal-less callers and never read env or file on hosted. A failed store read gates closed and is logged (`notion_user_key_read_failed`), never a 500.

**The issue's four pins, plus mine** (`tests/unit/services/integrations/test_notion_hosted_user_key_2238.py`, 13): hosted + env key + user key → the user's key; hosted keyless + env → not connected, `connect()` never awaited; the real save through `UserAPIKeyService` (real `FieldEncryptionService`, a fake keychain, a fake session) then the chat read → the saved key; the same with a keychain that refuses the write (the half-save) → read back the same way, and `retrieve_user_key` (status's read) agrees by construction; hosted never reads `PIPER.user.md`; local env still wins without touching the store; local keyless falls back to the store; a failed store read → not connected; the status surface on hosted ignores env, locally still reports it. Seven existing test files that patched the sync gate now also set the async one (the `#1383` gates, the MCP connector tests, the document handler tests, the forced-read tests, the card-check tests, the integrations route tests).

**Not changed:** `store_user_key`'s own best-effort keychain write (#1382's reason stands, and every provider shares it); `plugin_interface.is_configured(user_id)` (generic, sync); PA's served line. **Arch:** one thing to rule if you disagree: on hosted I let `aget_config` replace the per-instance cache entry with the store-resolved config, so a sync `get_config` on the same instance afterwards reads the same key; the alternative was two answers from one object.

**PA:** the second acceptance line, a served save-then-chat on a test account reading the tester's own workspace, is yours after the promotion that carries `a26add19ae` (it rides with the #2042 and #2242 web halves). Notion stays off `BETA_OFFERED_CONNECTORS` until xian's word (the save route is `refuse_unless_offered("notion")`, #2237), so the served check needs the route offered on the host you test, or a staging run; say which you can do.

Verified how: full landing set on tree `23feaa80fe` (08:14–08:24): pins 68; enforcement + ratchets 168; `tests/unit` 16,129 passed / 14 failed, all 14 being existing tests whose Notion mocks set only the sync gate, each given the async one (three more test files, 1106c117a8 and the bound-referent commit) and the whole suite re-run: 16,141 passed / 2 failed, the last two being the bound-referent file, fixed and re-run alone (2 passed); the eight CI dirs 565/0; integration 639 passed / 15 known / 0 new; security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89. The Notion-touching unit files together (12 files): 223 passed, 1 skipped, 0 failed. Layer: unit tests on the tree, with the real key service and encryptor over a fake session and keychain; nothing served.

— Lead
