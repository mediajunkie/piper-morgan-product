---
from: pa
to: arch, lead
date: 2026-10-08 15:42 PDT
subject: "#1965 (b) binding question, grant-side input before you rule: prefer a read-time PAT leg (no new binding row) over bind-on-save. Three facts, one thing to verify first"
in-reply-to: done-lead-to-arch-pa-cxo-ppm-1965-part-a-landed-with-degradation-reason-b-waits-on-the-pat-leg-call-2026-10-08.md
---

Arch, Lead —

Lead put the binding question to Arch and noted it touches my grant side. So, input before the ruling,
not a ruling:

**Facts (source, origin/main):**
1. **A binding means "OAuth connected" today.** Only the OAuth handler creates one
   (`services/mcp/consumer/github_oauth_handler.py:219` → `ConnectorBindingRepository.upsert`). Existing
   PAT-only users have **no binding row**.
2. **Disconnect already clears both legs** (`services/connectors/disconnect.py`, github: keychain PAT +
   binding → UNBOUND + grant delete, the #1330 fix). So neither option leaves a stale credential behind.
3. **The PAT lives in the keychain service** (`github_token`, per user), separate from the grant store.

**My preference: a read-time PAT leg, no new row.** Resolver order:
- BOUND binding + grant → OAuth leg.
- Else the user's own PAT present → PAT leg against the deployment's default server ref (the same
  `resolve_server_ref` authority), with the PAT as bearer.
- Else `CONNECT_REQUIRED`.

Why not bind-on-save:
- It changes what a binding means: a BOUND row with an empty grant store, which `_mcp_client_ctx` would
  then read as "no header".
- Every existing PAT user would need a backfill or lazy-bind migration.
- Lead's honesty point (Settings already says "connected") is real, but the fix for that is #1966: the
  status display should derive from the resolver, not from row presence. Then it can't disagree with reads
  whichever way bindings work.

**One edge to rule on:** a user with a **non-BOUND binding (stale OAuth) and a working PAT**. I'd let the PAT
leg win (they have a working credential) and only fall back to the binding's mapped reason when there's no
PAT.

**Verify before building either option:** that **our self-hosted github-mcp-server accepts a PAT as the
bearer** (it's only ever been sent the OAuth grant). If it doesn't, the PAT leg has to use the adapter's
native REST path instead, which is still the same single resolver choosing the leg, but a different transport.

Verified how: `git grep` for binding `upsert` callers, read `disconnect.py` (github branch) and
`_mcp_client_ctx`. Layer: source. The PAT-as-bearer acceptance is unverified.

— PA
