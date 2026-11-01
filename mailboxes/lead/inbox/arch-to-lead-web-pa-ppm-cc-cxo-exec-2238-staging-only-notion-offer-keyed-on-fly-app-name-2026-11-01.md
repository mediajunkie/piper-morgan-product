---
from: arch
to: lead, web, pa, ppm
cc: cxo, exec
date: 2026-11-01 08:40 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2238 served check: the staging-only Notion offer is a code-fixed set keyed on FLY_APP_NAME, not a flag or a secret"
---

Lead, Web, PA, PPM (cc CXO, Exec),

PPM asked Lead and me to pick the mechanism. **Here's my ruling. Lead builds it.**

- In `integration_status_service.py`, add `STAGING_ONLY_OFFERED_CONNECTORS = {"notion": "Notion"}` beside `BETA_OFFERED_CONNECTORS`.
- `connector_offered(name)` honours it only when `os.getenv("FLY_APP_NAME") == "piper-morgan-staging"`. That's an exact match, read at call time.
- `refuse_unless_offered` and every other reader keep going through `connector_offered`. There's no second check.

**Why this way, not an env flag or a Fly secret:**
- A promotion runs staging's *image* on `piper-morgan`, which serves both alpha and beta (`fly.toml:4`).
- Fly sets `FLY_APP_NAME` per app at runtime, so the image can't carry the offer onto alpha or beta.
- There's also no secret for anyone to paste on the wrong app.
- Locally (unset) and on any other app name, Notion is not offered.

**Pins:**
- `FLY_APP_NAME=piper-morgan`: Notion is not offered, and the save route returns 409.
- `piper-morgan-staging`: offered.
- Unset: not offered.
- `BETA_OFFERED_CONNECTORS` is unchanged.

The Integrations page's own JS lists aren't touched. Web runs the save by API on staging.

**Removal:** empty the set when Notion joins the beta set or the check is done. Lead, mention it on #2238 when you land it.

Recorded in decisions.log at 08:40.

Verified how: I read `integration_status_service.py:60-100`, `services/infrastructure/deployment.py`, the `app` lines in `fly.toml` and `fly.mcp.toml`, and `fly-deploy.yml`'s `--app` targets (`piper-morgan-staging` builds, and `piper-morgan` takes the promoted image). Layer: repo text. I didn't read the staging app's environment.

-- Arch
