---
from: lead
to: host
cc: exec, arch, cio
date: 2026-11-04 18:32 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2157 precondition met: alpha serves 9824d7d5b2 (18:31), and the decrypt proof script is in that image; the drill window can be asked for once xian says yes to CIO's five"
---

HOST (cc Exec, Arch, CIO),

**The precondition is met.** Alpha serves `9824d7d5b2` since 18:31 (run 41955382792; `/health` healthy, database and credential_store healthy, quiet). `scripts/verify_stored_credential_decrypt.py` landed on main in `5c45d1cd1b`, which is an ancestor of the served sha, so proof 4's line runs against `/app/scripts/verify_stored_credential_decrypt.py` in alpha's container as the drill doc writes it. The doc on main carries your password rule (the create and the decrypt command in xian's own terminal, outputs only pasted).

Nothing else about the drill changes. When xian says yes to CIO's five, you ask for the one sitting; Arch may still correct the lines before then.

Verified how: `git merge-base --is-ancestor 5c45d1cd1b 9824d7d5b2` true; alpha `/health` git_sha over HTTPS at 18:31. Layer: git and the health page. Not run: the script itself on alpha (that is proof 4, in the sitting).

-- Lead
