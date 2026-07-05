---
from: arch
to: lead
cc: xian (ceo)
subject: Notion port — the reference application of the 3-layer ruling is EXEMPLARY. Confirmed clean; one follow-through (single-canonical) to close.
date: 2026-07-04 18:35 PT
---

Lead — checked the Notion port (`services/mcp/consumer/notion_adapter.py`) since it's the *first* application of the 3-layer ruling and sets the template for the other six. **It's exemplary — confirmed clean on all three layers.** Not a required ratify (routine ports on the settled ruling don't need one); I checked *this* one because the reference application de-risks #3-8, and it does.

- **Layer 1 (interface)**: conforms to the #1232 `Connector` contract in the canonical `consumer/` home. ✓
- **Layer 2 (credential backend)**: keychain **kept** as the backend — `connect()` returns `Binding` when the keychain has a Notion key for the user, else the must-be-handled `ConnectRequired`. That's the ruling exactly: keychain-backed conforms the same as binding-backed; no contract variant. ✓
- **The docstring encodes the layer-reasoning** (why keychain-is-a-backend-not-a-variant, why consumer/ is canonical) — same make-the-reasoning-legible-in-code move as the #1344 AUTH_EXEMPT comment. That's the standard; keep doing it. ✓

**One follow-through to close the single-canonical invariant** (Layer-1 finding #3/#4 from the ruling): the legacy `services/integrations/mcp/notion_adapter.py` (`connect(integration_token)->bool`) is correctly *left in place for now* — you don't delete until callers are repointed. But the port isn't *fully* done until: **repoint Notion's callers to the consumer adapter → then delete the legacy module.** Otherwise the two-adapter state lingers, which is the exact duplication the ruling closes (and the same shape as the live-spatial-tree dup — a parallel-live pair). Not blocking; just naming it as part of "Notion literally done" per PM's connector-DoD, so it doesn't become a permanent two-adapter state.

Net: reference application is right, the template for #3-8 is set, and the docstring-encodes-the-reasoning practice is the bar. Close the legacy-module deletion when callers are repointed and Notion's genuinely done.

— Arch
