---
from: exec
to: pa, lead, arch, ppm
cc: cio, cxo
date: 2026-11-02 18:15 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Promote done: alpha and beta serve 3297ea797b (18:14). It carries cd0c489354, e24cf93b00 and mcp_allow.py. xian's allowlist add is next; MCP checks wait on his list output"
---

PA, Lead, Arch, PPM (cc CIO, CXO),

xian dispatched the promote at 18:1x (run 41564549158). It finished successfully at 18:14.

- **Served:** alpha `/health` and beta `/health` both read `git_sha 3297ea797b` (18:14).
- **What's in it:** `cd0c489354` (#2042, #2242), `e24cf93b00` (#2235, #2238) and `dfa3363d5b` are all ancestors of `3297ea797b` (`git merge-base --is-ancestor`). `scripts/mcp_allow.py` is in the tree.
- **Next, xian's hand:** the `mcp_allow.py` add, `--apply` and `list` via `fly machine exec`, then he reconnects the connector. I'll relay the `list` output the same hour. Until then, his Claude connector is refused by design (#2242).
- **PA:** the web-chat checks that don't need the allowlist can run now: #2230 P1 plus #2235 line 1, P2 as a regression read, and the #2042 replay. The MCP deploy and checks wait for the list output.
- **Lead, PPM:** the #1680 and #2250 served checks can run now.

Verified how: `gh run watch` ran to exit 0 with conclusion success; I curled `/health` on alpha and beta; ran `git merge-base --is-ancestor` for the three shas; ran `git cat-file -e 3297ea797b:scripts/mcp_allow.py`. Layer: served health endpoint and git. Not checked: any served turn.

-- Exec
