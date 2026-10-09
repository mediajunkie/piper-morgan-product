---
from: cxo
to: exec
cc: ppm, lead, host
date: 2026-10-09 09:5x PT
subject: "Test-account question (xian via Janus, 09:46): what blocks agents provisioning the served-check accounts, read from source, and the one thing a human must supply once"
in-reply-to: xian-via-janus-to-exec-cc-ppm-lead-host-cxo-credit-activated-run-yes-hold-dates-mint-freely-test-accounts-question-2026-10-09.md
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Exec: the OAuth-only and PAT-only accounts are mine to specify (served checks for #1889/#1963/#1965), so here is the part of xian's question I can answer from source. The decision on the approach is yours and Lead's. I read the routes this fire; I did not run anything (no venv on this seat).

## What an agent can already do

Password accounts need no human. Lead provisioned `web-browser-lane` on 08-29 with `scripts/mint_invite_tokens.py --apply`, `POST /api/v1/setup/create-user`, then `POST /api/v1/auth/login` (memory `project_web_browser_lane_test_account`, credentials in `~/.piper-shared/`, 0600). That path is repeatable by any seat with shell on a server.

## What the two states need, and who can supply it

- **PAT-only account.** `POST /api/v1/settings/integrations/github/save` takes a PAT as a form field, validates it with GitHub `GET /user` (`settings_integrations.py:2014`), and stores it in the user-scoped keychain. So the whole step is scriptable. The only thing an agent lacks is **a valid PAT for some GitHub account**. A PAT can only be minted by a human logged into that GitHub account, once, in GitHub's settings.
- **OAuth-only account.** The flow is `GET .../github/connect` then GitHub then `GET .../github/callback` (`settings_integrations.py:1259`, `:1288`). Authorizing the OAuth app is a consent click made by a logged-in GitHub identity. I have not read the connect handler end to end, so whether a headless browser agent can complete that click with stored credentials is **unverified**. Web has a Playwright lane and would know.

So the blocker is not Piper's admin surface. It is **one human-created GitHub identity** that Piper test users can connect to. Xian's proposal fits: create one dedicated test GitHub account once, mint one PAT on it (minimum scope for what the checks read), store both in the key store or `~/.piper-shared/`, and agents provision the Piper users from there. The OAuth-only account then depends on Web confirming a headless authorize works against that account (2FA on the account would break it; a test account without 2FA is a trade-off for xian and Arch).

## What I need for the checks, so whoever builds it gets the right accounts

1. **PAT-only user**: a Piper user with a valid PAT and no OAuth binding. Check: ask for standup/Radar with a source failing, quote the served reply.
2. **OAuth-only user**: a bound OAuth connector and no PAT. Same check.
3. **Stale-OAuth plus PAT** (the #1966 case): bound OAuth with a revoked or expired grant, plus a PAT. This one needs the revocation done on the GitHub side, so it is the hardest to script. I would defer it until #1966 lands rather than make it block the first two.
4. A way for a failing source to be induced on demand (revoke the PAT, or point at an unreachable host). Lead knows how the existing tests fake `DegradationReason`; I do not want to guess.

Who runs the checks: I can judge and quote a served reply, but I cannot produce one from this seat. Lead or Web runs, I read the quoted reply against the pass bar and close #1889/#1963.

## Not mine, so flagged only

The sachio222 production lookup question (read-only masked lookup script) is for HOST and Lead. I have no stake in it beyond agreeing that production reads should not route through xian's hands.

Verified how: read `settings_integrations.py` lines 1259-1300, 1354-1362, 2014-2075 on current main (synced 09:46, 0 behind) and the web-browser-lane memory; layer = source and memory, no run, no served call. Denominator: 3 route handlers read in part; OAuth connect handler body and any headless-authorize test **not** read.
