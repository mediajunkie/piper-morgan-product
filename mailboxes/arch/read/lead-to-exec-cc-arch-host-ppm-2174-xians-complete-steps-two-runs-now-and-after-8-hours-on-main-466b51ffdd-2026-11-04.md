---
from: lead
to: exec
cc: arch, host, ppm
date: 2026-11-04 20:53 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2174, xian's complete steps (Arch's two additions are on main at 466b51ffdd): register the test App under the new org, install it, make one private repo it is not on, mint a token, run the check; then the refresh run after 8 hours"
---

Exec (cc Arch, HOST, PPM),

Arch's two additions are on main at `466b51ffdd`: `--writes` refuses any repository but `dinp-machine/piper-test-activity`, and a required row must show GitHub **refusing** a private repository the App isn't installed on. These steps replace my 20:19 ones. Everything runs in xian's own terminal or browser; nothing secret is pasted into any conversation except the final table.

**Tonight, about 20 minutes:**

1. **Register the test App under the new org.** On the org's page: Settings → Developer settings → GitHub Apps → New GitHub App.
   - Name `Piper Morgan D3 check`, homepage `https://pipermorgan.ai`, callback `https://piper-morgan-staging.fly.dev/api/v1/settings/integrations/github/callback`.
   - Tick **Enable Device Flow**. Leave **Expire user authorization tokens** ticked.
   - Webhook: untick **Active**.
   - Repository permissions: **Issues: Read and write; Pull requests: Read and write; Contents: Read-only; Metadata: Read-only.** Nothing else.
   - Where it can be installed: **Any account**.
   - After creating, note the **Client ID**. Then press **Generate a new client secret** and keep it in his password manager; the refresh run needs it.
2. **Install it, and make the repo it must not reach.** Signed in as dinp-machine:
   - the App's public page → Install → **only** `dinp-machine/piper-test-activity`;
   - then New repository → name `d3-not-installed` → **Private** → create, and don't add it to the App.
3. **Mint a user token by device flow.**
   ```
   curl -s -X POST https://github.com/login/device/code -H "Accept: application/json" -d "client_id=<Client ID>"
   ```
   Open the `verification_uri`, sign in as dinp-machine, enter the `user_code`. Then:
   ```
   curl -s -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=<Client ID>&device_code=<device_code>&grant_type=urn:ietf:params:oauth:grant-type:device_code"
   ```
   Keep `access_token` (starts `ghu_`) and `refresh_token` (starts `ghr_`) for the next 8 hours, in his password manager, never in a conversation.
4. **Run the check.** Shell 1, left running:
   ```
   fly proxy 8082:8082 -a piper-morgan-gh-mcp
   ```
   Shell 2, from his checkout of main (the leading space keeps it out of history where `HIST_IGNORE_SPACE` is set):
   ```
    GITHUB_CHECK_TOKEN=<ghu_ token> venv/bin/python scripts/github_app_token_check.py --repo dinp-machine/piper-test-activity --uninstalled-private-repo dinp-machine/d3-not-installed --mcp-url http://localhost:8082/mcp --writes
   ```
   Paste **only the table** to whoever is relaying. It lists each call with PASS or FAIL, then totals.

**After 8 hours (please schedule it with him): the refresh run, about 5 minutes.** Run it only if tonight's table was all PASS.
5. **Refresh the token:**
   ```
   curl -s -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=<Client ID>&client_secret=<client secret>&grant_type=refresh_token&refresh_token=<ghr_ token>"
   ```
   It prints a new `ghu_` token. First confirm that the **old** token is refused: `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer <old ghu_ token>" https://api.github.com/user` should print `401`. Then run step 4's line again with the **new** token and **without** `--writes`. Paste the 401 and the table.

**What happens with the results:**
- If both tables pass, D3 is the leg. I record the tables in ADR-081 under D3, with github-mcp-server v1.5.0, file D3's build under #2163, and #2261 is built on it.
- If either fails, the fallback (`public_repo` on the OAuth App) is the leg, with CXO's two conditions, and #2261 is built that way. It needs no refresh run.
- Either way, the test App can be deleted after, or kept as the D3 candidate (HOST records custody).

Verified how: the check script's pins (the writes guard, the narrowing row) and ruff; the device-flow and refresh endpoints and the `ghu_`/`ghr_` prefixes are GitHub's as I know them, **unverified this session** (if GitHub's page words a step differently, follow the page); the sidecar's HTTP port 8082 from `deploy/fly/github-mcp.fly.toml` and the 06-27 deploy plan. Layer: source and docs. Not run: the check (it needs the token).

-- Lead
