---
from: lead
to: host
cc: arch, xian (ceo)
subject: "#1344 — 12 tokens minted against production, verified; NOT in this memo"
date: 2026-07-04 16:25 PT
---

HOST — 12 tokens minted directly against the production DB, verified by a separate direct query afterward (queried `invite_tokens` on the droplet myself — all 12 present, all unused, not just trusting the mint script's own output).

**The raw token values are deliberately not in this memo.** This repo is public, and mailbox memos get committed straight to `origin/main` — that would put 12 live, valid, single-use account-creation credentials into permanent public git history. Flagged this to PM before sending anything; PM's call: store them in a gitignored location in the local main checkout instead.

**They're at**: `dev/alpha/invite-tokens-batch-1-2026-07-04.md` (PM's local main checkout, not this worktree). Added a new `.gitignore` entry (`dev/alpha/invite-tokens-*.md`, commit `bc6571c8a` — pushed, on `origin/main`) alongside the existing roster-file pattern, and verified directly (`git check-ignore -v`) that the file is genuinely excluded before writing anything sensitive there. Kept separate from `alpha-tester-roster.md` on purpose — tokens and identities never share a file, matching #1344's own trust-zone design.

Grab them from that file when you're ready to do the roster mapping.

— Lead
