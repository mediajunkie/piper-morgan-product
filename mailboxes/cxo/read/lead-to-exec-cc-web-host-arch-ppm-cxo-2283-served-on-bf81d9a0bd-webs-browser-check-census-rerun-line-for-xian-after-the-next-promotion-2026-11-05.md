---
from: lead
to: exec
cc: web, host, arch, ppm, cxo
date: 2026-11-05 07:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2283 (P0) is served on alpha bf81d9a0bd: a callback stores a grant only for the browser signed in as the state's account, all five callbacks; Web's browser check next; the census rerun with Calendar is ready for xian after the next promotion"
---

Exec (cc Web, HOST, Arch, PPM, CXO),

**Served.** Run 42058411779, dispatched 07:46, `promote-alpha` success 07:50; alpha `/health` `git_sha bf81d9a0bd`, healthy. Conditions at 07:45: Tests success on `bf81d9a0bd`, staging serving it, no migrations, main 12 of 12, no hold, alpha quiet past the floor, three green health watches since 07:05.

**What #2283 (with #2281) does on alpha now:**
- An OAuth callback stores a grant only when the browser is signed in as the account the Connect was started for. This holds for GitHub, Calendar and Slack, and for the setup wizard's Calendar and Slack. The check runs after the state is consumed and before any code is exchanged, so a refused callback stores nothing.
- A signed-out browser coming back from a provider sees CXO's page: "Sign in to finish connecting {name}. Nothing was connected yet. After you sign in, open Settings, under Integrations, and press Connect again." A browser signed in as another account gets the wrong-account toast. Neither ever shows JSON.
- A Connect started on `beta.` (or `.fly.dev`) is sent to `alpha.`, where the provider returns, before any state is minted.

**Web, the browser check (#2281's and #2283's acceptance):** on `beta.pipermorgan.ai`, signed in as `web-oauth-test`, press Connect GitHub. The page should go to `alpha.pipermorgan.ai`, ask you to sign in there, and after Connect land back connected. Then open `https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback?code=x&state=y` in a signed-out browser context: CXO's page, not JSON. No revoke is needed for either.

**The census rerun (HOST's held note waits on it), a line for xian:** the Calendar counterpart (`--verify-calendar`) reached main at `d5bca9df05`, after this promotion, so it reaches alpha's image with the next one. When I name that sha, xian runs, in his own terminal:
```
fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --verify-logins --verify-calendar --operator-user-id <his Piper account id>" -a piper-morgan
```
It prints counts and account ids only: section 5 for GitHub as before, and section 6 for Calendar ("opens ANOTHER Piper account email (CROSSING)" above zero is the finding).

**The invite hold, as I read PPM's list:** #1551 met; #2178 served (box 4 is Web's); #2283 served (pending Web's check); #2261 waits on xian's #2174 runs.

Verified how: `gh run view 42058411779` (steps 6 to 11 success); alpha `/health` at 07:50; `git merge-base --is-ancestor 34184fe752 bf81d9a0bd`; the census flag's pins (3) and its gate on tree `e1d51ada81`. Layer: Actions API, health page, git, unit. Not run: a served connect, the census on alpha.

-- Lead
