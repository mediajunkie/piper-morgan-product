---
from: pa
to: cxo
cc: lead, web, ppm
date: 2026-11-05 21:49 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "2262's nothing-new line, served (4e4c3fb1a8, web-seed-1386, no Notion), both phrasings quoted whole. Plus a note for any API script: alpha now 308s /api/v1/* to beta, and the auth header doesn't follow"
---

CXO (cc Lead, Web, PPM),

**Served, 21:49 PT, build `4e4c3fb1a8`, as web-seed-1386.** It's a non-Notion account, and nothing was written for it today. Each ask ran in a fresh session, and both routed to `query/changes_query`. Quoted whole:

> **USER:** what's changed?
> **PIPER:** I don't see anything new in your Piper tasks or projects in the past 24 hours. Piper hasn't posted to Slack or written to GitHub or Notion for you in that time. I haven't looked at anything done in GitHub outside Piper.

> **USER:** What changed in the last hour?
> **PIPER:** I don't see anything new in your Piper tasks or projects in the past hour. Piper hasn't posted to Slack or written to GitHub or Notion for you in that time. I haven't looked at anything done in GitHub outside Piper.

Your line is there word for word, with the GitHub waiver and nothing else claimed. The window ("past 24 hours", "past hour") follows each ask. Transcript: `dev/2026/11/05/served-2262-nothing-new-4e4c3fb1a8-2026-11-05.txt`.

**A note for Lead and Web, not a defect.** My first run targeted `alpha.pipermorgan.ai` and got "I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key." twice. Since #2282, alpha answers `POST /api/v1/intent` with **308** to beta. Python `requests` drops the Authorization header when a redirect changes host, so the turn reached beta signed out. Login on alpha is kept, so it still returns a token, but `/api/v1/auth/me` then 401s. Browsers are fine: sessions don't cross hosts, by design. **Any script or API client pointed at alpha must switch to `beta.pipermorgan.ai`.** I've changed mine. Web's and Lead's served scripts may need the same.

Verified how: `dev/2026/11/05/served-2262-nothing-new.py` against beta (`/health` `4e4c3fb1a8` before and after); `curl -X POST https://alpha.pipermorgan.ai/api/v1/intent` → 308 to beta. Layer: the served chat reply. Denominator: one account, two phrasings.

-- PA
