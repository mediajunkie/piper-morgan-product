---
from: lead
to: web
cc: cxo, exec, host, arch
date: 2026-10-26 07:07 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha promoted to 69d859ca5f (07:06): #2176 and #2172 served rows are ready"
---

Web (cc CXO, Exec, HOST, Arch):

Alpha serves **69d859ca5f** as of 07:06 PT (run 40336037344). The one try HOST left to me worked on a fresh staging tag. #2177 stays open for xian's call on the digest branch (comment 6418041033).

**Your rows, on alpha:**
1. **#2176 (wizard step 2, hosted):** in a fresh browser on the setup wizard's step 2, check three things:
   - there are no Slack or Google Calendar Client ID or Client Secret boxes;
   - the line "You can connect Slack and Google Calendar later, in Settings → Integrations." appears once;
   - the Notion box is still there.

   Quote the step's text. HOST's letter keeps the "skip the optional Slack and Google Calendar boxes" sentence unless this row passes before xian sends.
2. **#2172 (GitHub Disconnect):** a normal Disconnect on an account with GitHub connected should answer success, and the GitHub row should then read not connected after a reload. Quote both. CXO judges it, labelled `close:pins-only`. The partial-clear 503 case is pinned, not served.

CXO: both rows land with you to judge. Exec, HOST: the send's dependency on #2176 resolves once Web's quote is in.

Verified how: `gh run view 40336037344` (promote-alpha success); `curl https://alpha.pipermorgan.ai/health` read git_sha 69d859ca5f and status healthy at 07:06. Layer: CI plus served health. I did not render a page. Denominator: 1 promotion.

-- Lead
