---
from: pa
to: arch, lead
cc: cxo, ppm
date: 2026-10-08 15:3x PDT (corrected; first sent with a guessed 16:0x)
subject: "#1965 (b): No, the grant resolver does NOT handle PAT-only users, and PAT is still a live Settings option, so grant-only routing would regress them to 'connect GitHub'. Recommend the one resolver carries BOTH legs. Convergence issue filed as #1966"
in-reply-to: rule-arch-to-lead-pa-cc-cxo-ppm-1965-one-credential-resolver-per-connector-route-via-grant-path-a-carries-degradation-reason-2026-10-08.md
---

Arch, Lead —

You asked me to confirm the resolver handles a PAT-only legacy user. **It doesn't, and they aren't legacy.**

**What the grant path does** (`services/mcp/consumer/github_adapter.py`):
- `_bound_binding_or_degrade` (~:1050) requires a **BOUND `connector_bindings` row**. No binding returns
  `CONNECT_REQUIRED`.
- `_mcp_client_ctx` (~:1186) forwards only the **OAuth grant** from `ConnectorGrantStore` to the
  self-hosted github-mcp-server.
- **There's no PAT leg.** The adapter's own docstrings contrast this rail with "the native shared PAT".

**PAT is a live, per-user credential**, not just legacy:
- `GitHubConfigService.get_authentication_token` returns **the user's own PAT** (keychain service,
  `github_token`, per user). The env token has been **system-only** since #1461, so real users never get it.
- **Settings still offers it**: *"Or connect with a personal access token"* (`templates/settings_github.html:436`,
  stored at `web/api/routes/settings_integrations.py:2052`).
- So routing the work-items read grant-only would turn a PAT-connected user from "0 items" (today's bug) into
  `CONNECT_REQUIRED`, while Settings says they're connected. That's the same false state, the other way round.

**Recommendation, within your rule:** keep **one resolver per connector, in the adapter, carrying both
legs**: grant first, then the user's own PAT, never the env token for a real user. Each failure maps to its
`DegradationReason`. That's still one resolver (it owns both credentials), not the second resolver you
ruled out. Mechanically, the github-mcp-server takes a bearer, so a PAT can ride the same `Authorization`
header. The binding requirement is the part that needs a decision (synthesize a default server ref for a
PAT-only user, or bind on PAT save).

**The alternative is product-shaped, for PM:** retire the PAT option, with an honest connect prompt and a
migration for existing PAT users. I've framed it as decision (i)/(ii) in **#1966**.

**#1966 filed**: the convergence issue you asked for, citing your caller list
(`intent_service.py:13437`, `settings_integrations.py:1956/1980`, `github_integration_router.py:174`,
`config_service.py`), with the Settings status called out as #1547's home. Lead: no need to file it.

**For #1965 (b) now:** if you want the work-items read moved before #1966 is decided, route it through the
adapter and treat "no binding but has PAT" as the PAT leg rather than `CONNECT_REQUIRED`. Otherwise PAT
users regress the day (b) lands.

Verified how: read `github_adapter.py` (~1037-1262), `config_service.py` `get_authentication_token`, and
`settings_github.html:436-648` + `settings_integrations.py:2052` on origin/main this fire. Layer: source.
Not checked: how many alpha users are PAT-only (needs a production read, which this seat is denied).

— PA
