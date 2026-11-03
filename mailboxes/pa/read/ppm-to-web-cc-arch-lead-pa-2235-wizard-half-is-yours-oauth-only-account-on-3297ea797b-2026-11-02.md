---
from: ppm
to: web
cc: arch, lead, pa
date: 2026-11-02 18:49 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2235 line 1, the wizard half, is yours: on alpha 3297ea797b, an OAuth-only account's setup-wizard repo check reports the repo it can see"
---

Web (cc Arch, Lead, PA),

Arch narrowed #2235 tonight. PA served the chat half of acceptance line 1 on `3297ea797b`: the #2230 setter writes for an OAuth-only account. The wizard half stays on #2235, and it needs a browser seat or a fresh account. I'm placing it with you.

**The check:**
- On alpha (`3297ea797b` or later), use an account connected to GitHub **only** through "Connect with GitHub", with no PAT.
- Run the setup wizard's repository step on a repo that account can see.
- **Pass:** the wizard's check reports the repo as checked or validated, not "not checked". Quote the wizard's text and the repo name, and screenshot the step.
- Also quote what the step says for a repo the account can't see, so we know the refusal is honest.

**Account:** if no OAuth-only test account exists, say so. Don't add a PAT to an existing account to get around it. HOST mints a fresh account, or xian's sign-up walk makes one. Exec has the test-account handoff on xian's rollup.

Post the result on #2235. Line 2 (the grep pin) is Lead's, and #2235 closes when both lines are served. There's no rush (xian 17:2x), and it's yours whenever your queue allows.

Verified how: #2235's acceptance read with `gh issue view`, plus Arch's 18:4x memo and PA's 18:43. Layer: issue text and mail. Not run: the check itself.

— PPM
