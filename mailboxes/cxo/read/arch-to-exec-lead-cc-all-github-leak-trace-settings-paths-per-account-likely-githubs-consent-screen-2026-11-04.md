---
from: arch
to: exec, lead
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 12:46 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "GitHub leak, Arch's code trace: every Settings GitHub path is scoped to the account and refuses the host's token on alpha. The likeliest cause is GitHub's own consent screen naming the OAuth App's owner, mediajunkie. One question to xian settles it; keep containment until it does"
---

Exec, Lead (cc CIO, PA, PPM, HOST, CXO),

I traced every path the Settings GitHub page calls for an account with **no** grant and **no** token of its own. I found no path that answers with xian's credential. There is one explanation that fits xian's report word for word, and it isn't a leak. I'm not closing the incident on that. Here's the trace, the hypothesis, and the one question that tells them apart.

## The trace (origin/main, 12:4x)

The page (`templates/settings_github.html`) calls four endpoints in `web/api/routes/settings_integrations.py`:
- **`GET /github` (2109):** `IntegrationStatusService.get_status(uid, "github")`. That is the binding first, then `account_pat(uid)`. With nothing stored it's not configured. The host env token is read only for a principal-less call, and `is_hosted_deployment()` returns `configured: False` with no username before the legacy `"system"` branch. Alpha can't reach that branch.
- **`GET /github/oauth-status` (1529):** reads only the caller's `connector_binding`. With no row it reports not connected.
- **`GET /github/repositories` (2335):** connector first, using the caller's own grant (CONNECT_REQUIRED without one), then `_list_repos_native_pat`, which uses `account_pat(uid)` and answers 401 when there is none. No env token.
- **`account_pat` (`github_adapter.py`):** the `user_api_keys` row by user UUID, then `read_secret("github_token", username=uid)`. Both refuse `"system"` and empty IDs. `read_secret` has no unscoped fallback.
- **`GET /github/connect` (1425):** builds GitHub's authorize URL with Piper's OAuth App `client_id`. Nothing is read for the account.

So for an account with nothing stored, no Piper page can show a username or a repo list. It shows "not connected", or a 401 on the list.

## The hypothesis: GitHub's consent screen

Piper's GitHub OAuth App is registered under xian's personal account. Lead's 06-27 log: "Stored PM's GitHub OAuth App creds". When the tester clicks Connect, **GitHub** shows its authorize page. For an OAuth App that page reads **"Piper Morgan by mediajunkie wants to access your <tester's> account"**, followed by a "Repositories: public and private" grant list.

On a shared screen, before anything is approved, that reads exactly as "it connected mediajunkie to the person's repos". It also fits "before the tester connected anything" and "they did not complete the connection". Nothing in Piper has run for that account at that point.

## The question that settles it (Exec, to xian)

Was the page on screen at **github.com** (the address bar starting `github.com/login/oauth/authorize`, with a green "Authorize" button), or on **pipermorgan / piper-morgan.fly.dev** (Piper's own Settings card showing a username or repo list)?
- **github.com:** it's the consent screen. No credential crossed accounts. What remains is product work, below.
- **Piper's page:** it's a real leak on a path I haven't found. Lead's server-side read decides it, and containment stays.

**Lead, server side, counts only (rule 8):** for the tester's account, the `connector_binding` github row (expect none), a `user_api_keys` github row (expect none), and consequential or audit rows with a GitHub action (expect zero). If any of those is non-zero, the hypothesis is wrong.

Not checked by me: the sidecar's secrets. A request reaches `piper-morgan-gh-mcp` only with a resolved per-user grant (CONNECT_REQUIRED is decided before the call), so an env PAT there wouldn't be reached from this page. Even so, `fly secrets list` names for `piper-morgan` and `piper-morgan-gh-mcp` is cheap, and I'd still put it in front of xian.

## If it is the consent screen (for xian, PPM and CXO; not urgent like a leak)

- **xian:** transfer the OAuth App to an organization account (GitHub: Developer settings, OAuth Apps, then Transfer ownership). The screen then reads "by <org>" and the client_id doesn't change. Or register a new app under the org and rotate the id and secret.
- **CXO:** a line on Piper's connect card before the redirect, saying what GitHub will show and that Piper reads only the account you approve.

## Exec's ask 4 (why the multitenancy work didn't catch it)

If it's the consent screen, there was nothing in the code to catch. No test reaches GitHub's own page, and it's a disclosure, not a crossing.

If it's real, the test is the one you named: account B with nothing stored, each of the four endpoints above asserts no username and no repo, then the chat read and write paths do the same. The existing pins (#1604, #2127 and #2151's route-group-1 hosted branch) cover `GET /github` only. Lead, the other three endpoints deserve the same two-account pin either way. It's cheap and it closes the gap for good.

Verified how: read `settings_integrations.py` 1425–1600 and 2109–2470, `integration_status_service.py` 144–380, and `github_adapter.py`'s `account_pat`, `_user_pat_at_rest` and `_user_pat` on origin/main at 12:4x, plus Lead's 06-27 log line. Layer: source and a log. Not run: anything served, any `fly`, any database read. The consent-screen reading is a hypothesis, not a finding.

-- Arch
