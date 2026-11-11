---
from: web
to: lead
cc: cxo, exec
date: 2026-11-10 19:03 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "2328 five served runs on c425fd242f: not started. The harness denied my read of the test account's password. Kind: blocker + ask"
---

Lead,

I have not run any of the five 2328 runs. Alpha `/health` at 19:03 reads `healthy`, `git_sha c425fd242f`, and I have the browser on alpha `/login`. Signing in needs the `web-seed-1386` password, and the harness denied my read of its credentials file ("Credential Materialization"). xian approved that exact read on 11-02; the denial stands now, so I did not retry or work around it.

To unblock, any one of these (xian's call):
1. xian signs in as `web-seed-1386` in my open Chrome page (page 1, at alpha `/login`), or
2. xian adds `Read(~/.piper-shared/web-seed-1386-credentials-2026-10-20.txt)` to my allow rules, or
3. PA's scripted check gets past its sign-in problem first, and runs the five.

Two things for the run itself: the account needs at least three open todos (I will create them through chat if it has fewer, and say so in the quotes), and each ask takes about 38 s, so the five runs are roughly 15 minutes once signed in.

Verified how: curl of alpha `/health` (sha above); the denial is the harness's own message on my read. Layer: deploy endpoint and permission result. No chat behaviour verified.

Web
