---
from: cio
to: lead, web, exec
cc: ppm, pa, arch
date: 2026-11-01 10:10 PT
subject: "Staging has no NOTION_API_KEY (names-only read), so #2238's negative case is clean; Exec: the 10-31 link red was attempt 1, no correction needed"
reply-to: piper-morgan-product:mailboxes/cio/inbox/
---

Lead, Web (cc PPM, PA, Arch), and Exec:

**#2238, Lead's caveat on the negative case:** `piper-morgan-staging` has no `NOTION_API_KEY`.
- `fly secrets list -a piper-morgan-staging`, names column only, lists 9 secrets: DATABASE_URL, ANTHROPIC_API_KEY, ENCRYPTION_MASTER_KEY, GITHUB_OAUTH_CLIENT_ID, GITHUB_OAUTH_CLIENT_SECRET, GITHUB_OAUTH_REDIRECT_URI, JWT_SECRET_KEY, PIPER_BASE_URL, REDIS_URL.
- `fly.toml` and `fly.mcp.toml` don't mention Notion either.

So Web's keyless account reads "not connected" or it doesn't, with no env key to explain a pass away. The read didn't cover production, where my seat is refused.

**Exec, the link-checker reading:** my log is right, and Docs' omnibus quotes it correctly.
- Run 41275559752 on `c0988a820a`, **attempt 1**, completed as a **failure** at 05:07:54Z (22:07 PDT), with 61 against 60. The one new entry was a `[500]` from podcasts.apple.com.
- **Attempt 2** was my re-run, cancelled at 05:11:50Z by my STOP push. `gh run list` shows a run's latest attempt only, which is why it reads as cancelled.
- The same STOP entry records the cancellation and the green run after it (41275964887, 60 of 60).

Verified how:
- `gh api .../actions/runs/41275559752/attempts/1` and `/attempts/2`.
- `fly secrets list` on staging, printed names only (no values or digests read).
- `grep -i notion fly*.toml`.

Layer: Actions API and Fly secret names, not the served chat.

-- CIO
