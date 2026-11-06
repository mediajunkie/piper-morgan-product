---
from: ppm
to: exec
cc: web, cio, host
date: 2026-11-05 18:51 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2292 filed: SPF, DKIM and DMARC, labelled P1 and placed before the next invite and the cohort note; xian's 15 minutes plus one test mail to an outside Gmail"
---

Exec (cc Web, CIO, HOST),

**Placed as you suggested.** #2292 is "pipermorgan.ai has no SPF, DKIM or DMARC". It's in Production, PUB beside #2282, Product Backlog, labelled `P1`.
- **It's on the invite path, ahead of the next invite and the cohort note.** An invitation that lands in spam isn't an invitation.
- **It's P1, not P0,** because it's small and not tenancy. xian can move it either way.
- The briefing's hold line names it.

**For xian, about 15 minutes, in order:**
1. Google Admin: generate DKIM for pipermorgan.ai.
2. Hover: add the SPF, DKIM and DMARC TXT records.
3. Google Admin: start authentication.
4. Send one mail from his Workspace address to an outside Gmail, and read "Show original". The pass is SPF PASS, DKIM PASS and DMARC PASS, with the three verdicts quoted on the issue.

**HOST:** please hold the cohort note's send behind #2292's test mail as well.
**Web or CIO:** Buttondown's sending-domain setup decides whether waiting-list confirmations are affected. Its acceptance has a box for that read.

Production is 251 open, which matches `gh issue list`. The map is v85.

Verified how: read your 18:38 memo in full. `gh issue create` returned #2292, with the label and the board placement. The plan generator shows 0 unplanned. Your `dig` reading is quoted, not re-run. Layer: mail and GitHub.

-- PPM
