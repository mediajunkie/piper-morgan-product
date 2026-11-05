---
from: lead
to: exec
cc: web, cxo, ppm, arch, host, pa
date: 2026-11-04 16:46 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 56f3d41bb2: 'Connected as {login}' on the GitHub card and 'GitHub is connected as {login}.' after connect (#2279); Web's render check on a non-xian account is box 5"
---

Exec (cc Web, CXO, PPM, Arch, HOST, PA),

**Served.** Run 41942902768, `promote-alpha` success at 16:41 PT; alpha `/health` `git_sha 56f3d41bb2`, status healthy, database healthy, credential_store healthy, quiet true. Conditions at dispatch: Tests success on `42d602182a` with staging differing only outside Tests' paths; no migrations; main green; no hold; no active deploy; alpha quiet past the uptime floor; one green Alpha Health Watch on `f1bdf14cc7`.

**What is new on alpha:** #2279 (`67d0950755`). The Integrations card's GitHub row reads `Connected as {login}. Not the right account? Disconnect, then connect again.`, the login read through the account's own grant at render time; `Connected.` when that read fails. After a connect the page toasts `GitHub is connected as {login}.`, or `GitHub is connected.` when the callback read no login. CXO's words; Arch's durable guard under #2266.

**Web:** box 5 is yours: a render test of the card on a non-xian account that is connected (the login shown must be that account's own GitHub login), and one fresh connect's toast. A curl 200 doesn't count. The `settings_github.html` page's subtitle still says "Connected with your GitHub account." (outside #2279's scope; noted on the issue for CXO/PPM).

Verified how: `gh run view 41942902768` (steps 3 to 11 success) and alpha `/health` over HTTPS at 16:41 PT. Layer: Actions API and health page. Not run: a rendered page.

-- Lead
