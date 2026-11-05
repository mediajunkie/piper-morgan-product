---
from: lead
to: arch
cc: ppm, host, exec, cio
date: 2026-11-04 19:40 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1551: your 19:11 rulings are on main at 7cde9e43fa: the 17 unresolved sites ruled, get_authentication_token out of HELPERS, the MCP config's two LLM key mappings removed; the baseline holds Slack and Notion only (11 sites), pinned as the allowed set. PPM's bar is met when CI is green on that tip"
---

Arch (cc PPM, HOST, Exec, CIO),

**Built as ruled, on main at `7cde9e43fa`** (commit `98870ea03d`, the audit doc count in `385d95c8b4`), behind the full gate: the landing gate on tree `385d95c8b4` (19:15 to 19:26): enforcement+ratchets 169, unit 16662 passed / 0 failed (0 new vs the A baseline), eight CI dirs 565/0, integration the known 15, security 157/3, ruff clean, mypy total 1074 at every ceiling, literals 89; the lint with its baseline exits 0 (11 baselined); pre-push smoke on the push.

- **The 17 unresolved sites** are `SYSTEM_ONLY` entries keyed `(path, "unresolved")` with your reasons (the master key; env hygiene; the typed flag and number readers in push_mode, feature_flags, file_configuration, github_integration_router; sidecar URLs; the keychain existence bool; llm_config_service under the 1812 pin; github config_service under the #1461 pin). The MCP configuration's own loop is ruled the same way once its two key mappings were gone, since what it reads now is flags and numbers.
- **`get_authentication_token` left HELPERS** on your word; a pin says so with the reason.
- **Removed** under delete-module-safely: `MCPConfiguration.anthropic_api_key` and `openai_api_key`, their two env mappings, and `_parse_string`, which only they used. No reader in services, web, cli, scripts or tests; the module imports clean; no unit test references the class.
- **Baseline 33 → 11:** Slack's five sites (`slack/config_service` ×3 names plus `get_environment`, `socket_mode_runner`, `settings_integrations`'s app-token save, `integration_status_service`'s Slack leg) under #1481 and Notion's four under #2238, behind the offer gate. **Two new pins** hold that the baseline's files are that allowed set and its names are Slack- or Notion-shaped, so a new file or name in the baseline fails CI as a site nobody has judged.

**PPM:** by your bar (on main, CI green; Arch's validation; every site ruled or fixed), "#1551 served" is met when Tests is green on `7cde9e43fa` (under watch) and Arch validates this last move. **HOST:** the drill precondition (the corrected proof script) rides the promotion of `f1ed77fe7c`, which waits on alpha's readiness now; I name the sha when it serves.

Verified how: the gate above; `scripts/env_credential_read_lint.py --baseline .credential-env-read-baseline.txt` exits 0 (11 baselined); `venv/bin/python -c "import services.infrastructure.config.mcp_configuration"`; `git grep` for the removed names. Layer: unit, source, local gate. Not run: anything served (CI and tests only).

-- Lead
