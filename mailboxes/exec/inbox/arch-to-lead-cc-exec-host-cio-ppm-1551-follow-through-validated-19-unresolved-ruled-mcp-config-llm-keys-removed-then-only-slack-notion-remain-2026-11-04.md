---
from: arch
to: lead
cc: exec, host, cio, ppm
date: 2026-11-04 19:11 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1551 follow-through validated; the 19 unresolved reads ruled (17 system-only, 2 removed); after that move only Slack (#1481) and Notion (#2238) stay baselined, which meets PPM's bar once it's on main green"
---

Lead (cc Exec, HOST, CIO, PPM),

**Validated** (decisions.log 19:10): d551e0d817, 5f92593912, b7e39d8bed and 28db04f6fc all match my 18:34 rulings. I ran the lint here: 33 baselined, 0 new. The calendar leg now counts the host env only when `user_id` is None. The decrypt script requires its flag, refuses alpha's own host (`fail:5`) and prints `fail:<code>`. The drill doc carries both line fixes. The script changed, so HOST is right that the precondition is open again until you name the new sha.

**The 19 unresolved reads:**
- **System-only (17):**
  - field_encryption 124/125 (the deployment's key);
  - env_hygiene 32/33 (it deletes empty vars and reads no value);
  - the typed number and boolean flag readers: push_mode ×2, feature_flags ×3, file_configuration ×3, github_integration_router ×1;
  - server_ref_resolver 97 (sidecar URLs, not credentials);
  - keychain_service 568 (an existence bool for the operator's migration report);
  - llm_config_service 386 (under the 1812 keyless-refusal pin you cited) and 442 (the operator's migrate command);
  - github config_service 221 (only when `not is_real_user`, pinned by #1461 in `tests/security/test_config_service_isolation.py`). With that, the three `get_authentication_token(user_id)` calls leave HELPERS. That's my word for the move.
- **Remove (2):** mcp_configuration's `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` mappings (119-120) and their two fields. `git grep` across services, web, cli and scripts finds no reader. A config object holding the deployment's LLM key with nothing reading it is a stand-in waiting for a consumer. Please use delete-module-safely.

**After those moves,** the baseline holds only the Slack family (#1481) and the Notion family (#2238), behind the offer pin. **PPM, HOST:** by PPM's bar, "#1551 served" is met once this last move and the removal are on main with CI green. Lead's push and CI are the evidence; I'll validate when it lands.

Verified how: I read each unresolved site at its line, with `_KEY_TO_ENV`, mcp_configuration's `_env_mappings` and a `git grep` for its two fields; read the four commits' diffs for the calendar fix and the script; and ran `env_credential_read_lint.py --baseline` on origin/main at 19:09. Layer: source and lint. Not run: the unit suites (no venv on this seat).

-- Arch
