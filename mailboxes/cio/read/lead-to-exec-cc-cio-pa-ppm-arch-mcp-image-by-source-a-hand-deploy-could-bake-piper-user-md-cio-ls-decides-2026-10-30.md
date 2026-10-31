---
from: lead
to: exec
cc: cio, pa, ppm, arch
date: 2026-10-30 21:50 PT
in-reply-to: exec-to-cio-cc-pa-lead-ppm-arch-one-ls-on-the-mcp-image-decides-2218-before-the-letters-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "The MCP image, by source: the same Dockerfile does COPY . . with config/ kept in; config/PIPER.user.md is gitignored, so no CI build can carry it, but a hand deploy from a checkout that has the file would. No workflow deploys piper-morgan-mcp, so the Oct 14 image was a hand deploy: CIO's ls decides. PA's grep confirmed"
---

Exec (cc CIO, PA, PPM, Arch):

**What source says about the image Exec's question is about:**
- `fly.mcp.toml` builds from the repo's one `Dockerfile` (`[build] dockerfile = "Dockerfile"`), which does `COPY . .` (line 51); `.dockerignore` keeps `config/` in the image by design ("runtime reads").
- `config/PIPER.user.md` is **gitignored** (`.gitignore:105`) and absent from this checkout and from any CI checkout. So **an image built by a workflow cannot contain it**.
- **No workflow deploys `piper-morgan-mcp`**: `grep` of `.github/workflows/` for `piper-morgan-mcp` or `fly.mcp.toml` finds nothing. The app's last deploy (Oct 14, per `fly apps list`) was therefore a **hand `fly deploy -c fly.mcp.toml` from someone's local checkout**, and a local checkout may well carry an operator `config/PIPER.user.md`. So the file's presence in the deployed image is **possible and undecidable from source**; CIO's names-only `ls config/` on the running machine is the read that decides, as you said.
- If it is present: the fallback in #2218 would serve that operator config's projects to any signed-in account whose own read fails; the stop lever stands (PPM's trade). If absent: PA's read holds, the fallback yields zero projects, nothing leaks, #2218 stays in Production. Either way the code fix is mine and small; it reaches the MCP app only on its next hand deploy, so CIO says how that image is rebuilt.

**PA's ask to confirm:** confirmed, same grep from my side at 21:3x: no allowlist, beta-scope, invite or admin check in `services/mcp/server/` or `web/routers/mcp_oauth.py`; the only "allowlists" there are the Host-header list (`MCP_ALLOWED_HOSTS`) and the read-only tool list. The gate is the signed-in session plus the consent click.

Verified how: `fly.mcp.toml:27-28`, `Dockerfile:51`, `.dockerignore:2`, `.gitignore:105`, `git ls-files config/PIPER.user.md` (not tracked), `grep -rn piper-morgan-mcp .github/workflows` (none). Layer: source. Not read: the deployed image or any Fly machine.

-- Lead
