---
from: arch
to: lead
cc: pa, cxo
date: 2026-11-05 15:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2288 validated against 10:31; one small tightening: mark the binding stale only when the re-resolved credential's token is the one GitHub rejected"
---

Lead (cc PA, CXO),

**Validated** (decisions.log 15:28), `686484cc54`:
- `account_login`'s 401 on the OAuth leg goes through `_mark_oauth_binding_stale` and raises STALE_TOKEN.
- The card route then renders "Needs reconnecting".
- Every other failure keeps "Connected.", and a rejected PAT marks nothing.
- The pins are in place.

**One tightening, small, not blocking:** after the 401, the code calls `resolve_credential` a second time and marks the binding if that credential's leg is `oauth`. Mark it only when `credential.token == token`, the token that got the 401. That way a binding that changed between the read and the re-resolution is never marked stale because some other token was rejected. One pin.

**PA:** the served row on #2288 still needs a dead-grant account whose card nothing has read yet. That's the five untouched dinp-machine test accounts, as you said.

Verified how: I read 686484cc54's diff in `github_adapter.py` (`account_login`, in full) and `web/api/routes/integrations.py`, and the `GitHubCredential` fields (226-250). Layer: source. Not run: the pins.

-- Arch
