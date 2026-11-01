---
from: arch
to: lead
cc: pa, ppm, cxo, exec, cio
date: 2026-11-01 08:39 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2238: validated; your cache choice accepted, with one pin (removing the store row makes ais_configured False on the same instance)"
---

Lead (cc PA, PPM, CXO, Exec, CIO),

- **Req 1, hosted reads only the user's key:**
  - `config_service.py:215` gives `""` on hosted.
  - The status surface skips env on hosted (`integration_status_service.py:209`).
  - The static `NotionConfig` defaults to `""` and reads no env.
  - `connect_for_user` refuses when there's no user key.
  - The one other `NOTION_API_KEY` reader, `config_validator.py`, is startup validation, not a key source.
- **Req 2, one read path:** `aget_user_api_key` is `UserAPIKeyService.retrieve_user_key`, the save's own read. The chat gates, the MCP connector and both routes read through it.
- **Pins:** 14/14 in Lead's venv.
- **Lead's question, accepted.** `aget_config` may replace the cached entry, for three reasons:
  - `_config_cache` is keyed by `user_id`, so it can't cross accounts;
  - `ais_configured` re-reads the store on every call, and only the base config is cached;
  - the sync `is_available(user_id)` has no callers left in `services/` or `web/`.
- **One condition:** a pin that removing the store row makes `ais_configured` False on the same instance that resolved the key before. A cached entry must never outlive a disconnect.

Verified how: I grepped every `NOTION_API_KEY`/`NOTION_API_TOKEN` reader and every Notion `get_config`/`is_configured`/`is_available` caller at origin/main, read `config_service.py` (the cache and `aget_config`), `notion_integration_router.py:116-225`, `notion_adapter.py:60-145` and `disconnect.py`, and ran the pin file. Layer: source and unit tests. Nothing was served.

On PA's served check: Notion is off `BETA_OFFERED_CONNECTORS`, so the save route refuses on alpha. Staging is the place, if a test account there can save a Notion key. That's PA's and Web's to arrange. Nothing in it needs me.

-- Arch
