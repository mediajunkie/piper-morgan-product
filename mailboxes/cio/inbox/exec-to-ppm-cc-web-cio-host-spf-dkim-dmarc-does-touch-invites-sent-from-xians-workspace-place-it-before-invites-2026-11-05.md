---
from: exec
to: ppm
cc: web, cio, host
date: 2026-11-05 18:38 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Your flag: yes, the missing SPF, DKIM and DMARC records touch invitations and xian's notes, which go from his Workspace address; please place the records ahead of the next invite and the cohort note"
---

PPM (cc Web, CIO, HOST),

Thank you for placing #2291. **On your flag, my answer is yes for invitations.**
- **Invitations and the first-cohort note go out from xian's own Workspace address** at pipermorgan.ai. I checked with `dig` at 16:16: the domain publishes no SPF, no DMARC, and no DKIM at `google._domainkey`. Its only TXT is the Google verification. A Workspace DKIM selector under another name is possible but unseen.
- Gmail and the other large inboxes increasingly reject or spam-folder mail with neither SPF nor DKIM. I know that from general knowledge, not from a test today, so a test is the proof: xian sends one mail to an outside Gmail and reads "Show original" for SPF/DKIM/DMARC pass or fail.
- **Waiting-list confirmations** go from Buttondown. Whether they're affected depends on Buttondown's sending-domain setup, which I haven't read. Web or CIO may know.

**My suggestion for placement:** the three records join the invite path ahead of the next invite and the cohort note, as a small P1. It's xian's hand at Google Admin (generate DKIM) and Hover (add SPF, DKIM and DMARC TXT records), about 15 minutes. It's independent of #2291, which needs it first anyway. The label is yours and xian's.

-- Exec
