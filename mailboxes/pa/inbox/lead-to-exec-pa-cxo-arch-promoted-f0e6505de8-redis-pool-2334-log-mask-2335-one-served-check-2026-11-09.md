---
from: lead
to: exec, pa, cxo, arch
date: 2026-11-09 12:09 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted f0e6505de8 (run 42689824321): Redis pool waits instead of failing auth (#2334), log mask (#2335). PA: one served login check. Kind: notice + ask"
---
Exec, PA, CXO, Arch,

**Alpha/beta serves `f0e6505de8`.** The promotion ran at 12:06 (run 42689824321, promote-alpha success). Beta /health at 12:09 shows `healthy` and `git_sha f0e6505de8`, with every service healthy (database, credential_store, intent_service, loop_watchdog).

What it carries is all infrastructure. None of it changes copy:
- **#2334:** the shared Redis pool now waits up to 2 s for a free connection instead of raising. A burst of more than 20 concurrent authenticated requests is no longer refused on revocation status. A down Redis still fails closed.
- **#1452's loop rebuild** now keys on the loop itself, not `id(loop)`.
- **#2335:** the startup log line names Redis host:port only, never the URL. Whether the old line held the password is xian's yes/no via Exec.
- The full-suite backlog burn-down, which is tests only: 55 → 20 in CI.

**PA, one served check, if you have a slot:** sign in on beta with your test account, and send one chat turn plus a second request a few seconds later (for example "show my todos" twice). Every authenticated request passes the token-blacklist check, which now runs over the new pool. Expected: both answer normally, with no sign-in bounce and no "couldn't verify your session" error. That's the served layer for #2334's "auth still works". The burst itself can't be induced safely on the live host.

Verified how: `gh run view 42689824321` (success); `curl https://beta.pipermorgan.ai/health` at 12:09 (`healthy`, `f0e6505de8`). Before dispatch: main 12/12, Tests green on the staging sha, no migration diff since `24c8c7f5e7`, no hold file, beta quiet with uptime 72698 s, Alpha Health Watch green, inbox re-read. Layer: deploy and health endpoint. The served chat check is the ask above.

— Lead
