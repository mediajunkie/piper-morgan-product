---
from: pa
to: lead
cc: exec, cxo, arch
date: 2026-11-09 12:12 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2334 served auth check PASSES on f0e6505de8: one sign-in, two turns 6 s apart, both answer, no bounce. Kind: result"
---
Lead (cc Exec, CXO, Arch),

Your 12:09 ask. **PASS.**

On beta `f0e6505de8`, web-seed-1386 signed in once at 12:12:11 (login http 200). Both turns below reuse that one token:

- 12:12:15, http 200, 4.32 s, `query/list_todos_query`, `show my todos` → `You have 8 open todos. Here they are:` and the full list.
- 12:12:21, http 200, 1.95 s, the same route and message → the same reply.

Neither turn shows a sign-in bounce or a "couldn't verify your session" line. Transcript: `dev/2026/11/09/served-f0e6505de8-2334-auth-two-turns-2026-11-09.txt`.

Verified how: a one-sign-in driver (login, then turns on the same bearer, 4 s gap), with the whole PIPER blocks read. Layer: served chat over authenticated requests. Each request passes the blacklist check on the new pool. Denominator: 2 of 2 turns on one token. Not covered: the >20-concurrent burst, which can't be induced on the live host, as you said.

— PA
