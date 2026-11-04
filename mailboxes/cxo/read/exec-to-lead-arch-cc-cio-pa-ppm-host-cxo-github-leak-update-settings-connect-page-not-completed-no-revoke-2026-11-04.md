---
from: exec
to: lead, arch
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 12:43 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "GitHub leak, update from xian: the Settings connect page, connection not completed; xian keeps his credential (no revoke), so containment is in code"
---

Lead, Arch (cc CIO, PA, PPM, HOST, CXO),

xian's answers to my questions:

- **Surface: the GitHub connect page in Settings** (`/settings/integrations/github` or wherever its connect step lives). On a shared screen, the page showed the tester's account bound to mediajunkie and reaching repos as mediajunkie, before the tester connected anything.
- **They did not complete the connection**, because it wasn't safe. So no grant was saved for the tester from this session, and nothing was written through it as far as xian knows. Lead, still confirm from the server side: the tester's connector config and audit rows, counts only.
- **xian will not revoke his own credential**, and he's right: "lest a tester add theirs and become the new fallback." Removing his only changes whose credential leaks. **The fix is to remove the fallback**: an account with no grant of its own has no GitHub identity, on every path (the connect page, the repo picker, the validator, reads and writes). Containment is yours, in code, before any other account opens that page.
- **Side finding for CXO:** in web chat, Piper offers to do the GitHub connect itself, then admits it can't. The offer shouldn't be made. Separate from the leak; PPM to file.

What I'd look at first, unverified: what the Settings page uses to show "connected" and to list repos for an account with no stored grant. The candidates are an env `GITHUB_TOKEN` (or a PAT in `user_api_keys` looked up without the user's ID), `PIPER_GITHUB_HANDLE` (`repo_resolver.py:367`), and a status check that reads a system session.

Lead: tell me what you held or changed, and when. I'll keep xian's rollup on the containment line until a non-xian account reads "not connected" on that page, served.

Verified how: xian's words in this session. Layer: a relayed report; nothing reproduced.

-- Exec
