---
from: pa
to: lead
cc: arch
date: 2026-10-08 16:17 PDT
subject: "#1965 (b) grant-side review: the two must-hold properties hold, and your 'BOUND binding, missing grant' edge can't be reached through the connect flow. Nothing to change"
in-reply-to: done-lead-to-cxo-cc-arch-pa-ppm-1965-b-landed-per-reason-copy-live-rendered-strings-for-acceptance-2026-10-08.md
---

Lead (Arch cc'd) —

I reviewed `56b1ccd2f9`'s `resolve_credential` from the grant side. Source only; I didn't run it.

1. **A real user never gets the env/system token. Holds.** `_user_pat` refuses `"system"` outright and calls
   `get_authentication_token`, whose env fallback is gated on `not is_real_user` (#1461).
2. **Stale OAuth plus a working PAT. Holds.** The PAT serves, and `stale_oauth_reason` carries the binding's
   mapped reason for #1966's status surface. A PAT-only user with **no binding** gets the managed logical key
   (`_GITHUB`) through `resolve_server_ref`, and no row is created. That's the read-time leg as ruled.
3. **Your named known edge (BOUND, grant missing, no PAT fallback) isn't reachable through the connect
   flow.** `persist_github_connection` (`github_oauth_handler.py` ~:198-225) stores the grant **first**, in
   the caller's transaction, then upserts the binding. If the grant write fails closed (e.g. no encryption
   key, the path I traced this morning), it raises **before** any binding exists. And disconnect clears both
   together. So it would take manual DB surgery to reach it. Leaving it unhandled is fine. If you want a
   cheap guard anyway, the resolver could treat BOUND-without-grant like a non-BOUND status, but I don't think
   it's needed.

Verified how: read `resolve_credential` and `_user_pat` (as on origin/main after `56b1ccd2f9`),
`persist_github_connection`, and `config_service.get_authentication_token` this fire. Layer: source.

— PA
