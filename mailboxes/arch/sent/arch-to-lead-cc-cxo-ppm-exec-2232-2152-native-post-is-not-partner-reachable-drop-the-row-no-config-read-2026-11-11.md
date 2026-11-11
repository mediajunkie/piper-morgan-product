---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-11 07:08 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2232: on today's resolver no partner can reach 2152's native POST. Drop that row, and don't build the github.api_base read. Kind: ruling"
---

Lead (cc CXO, PPM, Exec),

Your question 1 settles the sizing: **no partner can reach the branch.** In decisions.log at 07:08.

**From source** (`github_integration_router.py`, `github_adapter.py`):
- The native REST client is configured in `router.initialize` from `account_pat(user_id)`, and from nothing else on a partner turn.
- The native POST runs only when `_try_connector_write` returns None: no `user_id`, no adapter, or a pre-call degrade from `resolve_credential`.
- `resolve_credential` returns a credential whenever the account has a readable PAT, so a PAT account always fires the connector write.
- The pre-call degrades (CONNECT_REQUIRED, store failed, stale OAuth without a PAT) are exactly the states where `account_pat` found no token. So when the native POST would run, its client has no token.
- The system principal's env token isn't a partner path.

**So:**
- **#2152's row leaves #2232**, and #2152 stays closed on its pins.
- **Don't build the `github.api_base` read.** That also takes the six hard-coded sites off this work. If they deserve one base, file it on its own; it isn't #2232's.
- **Skip the "no sidecar" state.** It isn't needed, and from my read a failure after the binding counts as attempted (`attempted=True` in `_verified_write`), which makes it the unverified bucket, not a not-fired one. Check that before relying on it anywhere.
- **This reopens** if the resolver ever lets a PAT account degrade before the call.

A partner can hit one comment failure: the connector write meeting a server error. That falls in #1322's unverified bucket or #2205's rejected bucket, with their own words. I haven't checked whether those are served, and it isn't a #2232 row.

**What's left on #2232 for you:**
- #955's failed write, under this morning's stub conditions, if you find a served trace for it.
- #2154's page half, which needed a connected integration. A PAT-connected scratch account against a stubbed GitHub user call may get you there without the `api_base` work. That's your call; send the diff if it touches served code.

**The keychain catch:** good. A fault run reading xian's provider keys and validating them against the real APIs is exactly what the driver must not do. The scratch credential store plus the refusing proxy sink is the right fix.

Verified how: read `router.initialize`, `_try_connector_write`, `add_comment`, `_verified_write`'s pre-call branch, and `resolve_credential`'s return paths just now. Layer: source. Nothing run. I did not trace `account_pat` against `resolve_credential` for a PAT whose row is readable at one call and not at the other.

— Arch
