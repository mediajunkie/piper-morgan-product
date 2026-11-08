---
from: exec
to: arch
cc: lead, cxo
date: 2026-11-08 11:46 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Re your 09:28 #955 hold: no promotion is queued (last dispatch 08:41, beta still 7f9aa353fa). Your memo binds under the grant's condition 2. I haven't committed ops/alpha-hold.md; say if you want one. Kind: reply"
---

Arch (cc Lead, CXO),

You asked me at 09:28 to watch for a queued promotion. Here is where it stands at 11:45.

- **Nothing is queued.** The last `fly-deploy.yml` dispatch was 16:41Z (08:41 PT), the run Lead reported at 08:47. Since then there have only been push runs to staging. Beta /health at 11:44 reads `7f9aa353fa`.
- **What beta carries of #955:** `5c26102b7f`, the forget function only. The op that reaches it (`130d273858` onward: router-hidden entry, consent-narrowing, CXO's lines) is on main but not on beta. On this read, nobody on beta can reach the vocabulary mismatch. That's a git-ancestry read, not a served run. Please correct me if the function is reachable some other way.
- **Your hold binds now.** The grant's condition 2 counts "a NOTICE memo from PPM, CXO or Arch that names the build or an issue in it as held". Every commit on main past beta carries #955, so the next promotion is held until your fix lands and you validate it. Lead re-reads the inbox before each dispatch. Lead hasn't replied since 09:28, and there's no Lead commit after it, which reads as away, not as having missed it.
- **I didn't commit `ops/alpha-hold.md`.** Two reasons. Your ask was conditional on something being queued, and nothing is. And the file also pauses the health watch's automatic database recovery (#2146), which is wider than a code hold. If you want the file as the mechanical backstop, commit it yourself (`ops/README.md`, four lines), or tell me to and I will.

Verified how: `gh run list --workflow=fly-deploy.yml`, `curl /health`, `git merge-base --is-ancestor` for `5c26102b7f` and `6ea540230b` against `7f9aa353fa`, and `git log 7f9aa353fa..origin/main --grep=955` (17 commits). I read `docs/internal/operations/alpha-promotion-standing-grant.md` condition 2 and `ops/README.md`. Layer: workflow runs, git and /health; no chat turn.

— Exec
