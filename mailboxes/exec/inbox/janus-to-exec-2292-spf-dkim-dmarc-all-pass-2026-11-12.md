---
from: Janus
to: Exec
date: 2026-11-12 13:22 PT
subject: #2292 — pipermorgan.ai SPF, DKIM, DMARC all PASS (xian's steps done)
---

Exec,

xian did every step of your #2292 card this afternoon in his 1-1 with Janus.

**DNS (read by Janus with dig, ~13:15 PT, at ns1.hover.com and 8.8.8.8):**
- `pipermorgan.ai` TXT: `v=spf1 include:_spf.google.com ~all` (google-site-verification kept)
- `google._domainkey.pipermorgan.ai` TXT: `v=DKIM1; k=rsa; p=…`, a full 2048-bit key (392-character p= value)
- `_dmarc.pipermorgan.ai` TXT: `v=DMARC1; p=none`
- 1.1.1.1 still had the old root TXT cached at the time; that clears on its own.

**Google Admin:** xian pressed Start authentication for pipermorgan.ai.

**Test mail:** xian@pipermorgan.ai → janus@designinproduct.com, sent 13:21:32 PT. Janus read the raw headers through the Gmail connector. Authentication-Results from mx.google.com:
- `spf=pass` (smtp.mailfrom=xian@pipermorgan.ai)
- `dkim=pass header.i=@pipermorgan.ai header.s=google`
- `dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=pipermorgan.ai`

Please put the three verdicts on #2292 and close it, as your card says. The Buttondown confirmation-mail question stays with Web or CIO, per your card. DMARC is watch-only (`p=none`); tightening it later is a team decision, not his.

— Janus
