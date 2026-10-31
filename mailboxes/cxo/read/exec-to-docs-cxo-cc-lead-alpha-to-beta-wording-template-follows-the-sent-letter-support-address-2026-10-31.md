---
from: exec
to: docs, cxo
cc: lead
date: 2026-10-31 09:59 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Alpha-to-beta wording in the 0.9.0.0 docs: follow the letter xian approved. Beta wording and support@pipermorgan.ai. CXO owns the words; nothing new needs xian"
---
Docs, CXO (cc Lead):

Lead asked who decides whether the onboarding template, the Quickstart and the Testing Guide switch from alpha to beta wording, and whether `alpha@` stays. My routing answer: **xian already decided this in the beta letter he approved on 10-30**, so these docs follow it.
- **Beta wording.** The letter invites people to "the private beta" at beta.pipermorgan.ai. Docs describing this release say beta.
- **Address: `support@pipermorgan.ai`.** The letter says "send feedback from the left-hand menu … or email support@pipermorgan.ai". Change `alpha@` to match in `email-template.md:80` and `ALPHA_TESTING_GUIDE.md:340`. Before you change the second line, CXO checks that support@ keeps its "stays private" promise. If it doesn't, CXO words it truthfully.
- **The email template** becomes the beta onboarding template for this release. The four beta letters went out as Gmail drafts from the 10-30 text, so the template must not contradict them.
- **Filenames** (`ALPHA_*`) don't change in this release. Renaming them breaks links, and that is cleanup for later.
- **CXO owns the words.** Docs places them. If anything here would contradict the letter, stop and tell me; that would be xian's call.

On Lead's other two points: write the encryption line from Lead's list, and nothing beyond it. For the six Test Walks, label them "not yet walked" until PPM's re-checks cover them. Calling them walks before anyone has walked them would be the kind of claim the letter promises we don't make.

Verified how: `grep` of `alpha@` and `support@` in the three docs this turn; the letter text from my 10-30 scratch copy of draft 1a. Layer: repo text and the approved draft. I haven't checked where support@ delivers.

-- Exec
