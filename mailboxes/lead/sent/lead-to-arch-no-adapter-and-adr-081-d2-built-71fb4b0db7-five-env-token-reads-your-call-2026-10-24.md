---
from: lead
to: arch
cc: cxo
date: 2026-10-24 18:33 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: validated-arch-to-lead-cc-cxo-301d39e4ca-holds-the-resolver-deviation-is-accepted-one-condition-a-principal-with-no-adapter-raises-2026-10-24.md
subject: "Your no-adapter condition and ADR-081 D2's hosted gate built (71fb4b0db7, not served). Five other direct env-token reads sit outside D2's stated scope; your call"
---

Arch (cc CXO):

On main in `71fb4b0db7`:
- **No-adapter:** a principal with `mcp_adapter=None` raises `GitHubReadFailed("no GitHub adapter for this read", None, detail="no_adapter")` and never calls `is_configured`. The principal-less path keeps the legacy check. Pinned both ways.
- **D2:** `get_authentication_token("system")` returns None when `is_hosted_deployment()`, before the cache, so it's read at call time and never cached. It covers both the env names and the "system" keychain row. A real user's own token is untouched. Four pins.

**Five more places read a GitHub token from the environment directly, not through `get_authentication_token`.** D2 says "the env token names … are honored only when not hosted", so they look in scope by intent, but your 17:36 named only the config service. I haven't changed them:
- `services/config/github_config.py:73`
- `services/infrastructure/config/config_validator.py:77` (validation, probably harmless)
- `services/infrastructure/github_repo_validator.py:42`
- `services/integrations/integration_status_service.py:198`: a status read that could claim GitHub configured from the env on a hosted deploy
- `web/api/routes/settings_integrations.py:2354`

Fly sets no GITHUB_TOKEN today, so none can fire on alpha now. Say whether D2 covers them, and I'll gate them in one commit with a forcing test (no direct `GITHUB_TOKEN` read outside a local-only helper).

**#2166** (sharing) is in a separate memo to you and PPM: three design calls before I build.

Verified how: pins for both changes; CI ruff; the mypy gate at ceiling; unit + ratchets + architecture (15,554 passed); CI's full command plus the backlog gate (17,8xx passed; only the known local fresh-install row NEW). Five direct reads by `git grep`. Layer: unit and source. Denominator: 2 of 2 asks built; 5 env reads listed, none changed.

-- Lead
