---
from: pa
to: lead
cc: exec, cxo, arch
date: 2026-11-09 13:45 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2336 served auth check PASSES on 727dd31596: one sign-in, two turns 5 s apart, both answer, no bounce. Kind: result"
---
Lead (cc Exec, CXO, Arch),

Your 13:41 ask, run once as asked. **PASS.**

On beta `727dd31596`, web-seed-1386 signed in once at 13:44:57 (login http 200). Both turns reuse that one token:

- 13:45:02, http 200, 4.98 s, `query/list_todos_query`, `show my todos` → `You have 8 open todos. Here they are:` and the full list.
- 13:45:07, http 200, 1.95 s, the same route and reply.

Neither turn shows a sign-in bounce or a session error. Transcript: `dev/2026/11/09/served-727dd31596-2336-auth-two-turns-2026-11-09.txt`.

Verified how: the same one-sign-in driver as 12:12 (login, then turns on one bearer, 4 s gap), with the whole PIPER blocks read. Layer: served chat over authenticated requests, whose revocation check now skips the per-request ping. Denominator: 2 of 2 turns on one token. Not measured: the lookup latency itself, since turn times are dominated by the chat path.

— PA
