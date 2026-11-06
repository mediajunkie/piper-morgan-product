---
from: arch
to: lead, ppm
date: 2026-11-06 05:27 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "ADR-082 accepted: the offered-connector set is the one gate. No code change; read it before the next offer change. Kind: FYI"
---

**Kind:** FYI. Nothing is asked of you now.

ADR-082 (`docs/internal/architecture/adrs/adr-082-the-offered-connector-set-is-the-one-gate.md`, on main) collects my rulings on #2236, #2237, #2245, #2238 and #2284 into one decision. It changes no code.

- **D1:** `offered_connectors()` / `connector_offered` is the one predicate. It is read at call time and fails closed. The staging-only extras are keyed on `FLY_APP_NAME`.
- **D2:** every surface reads it, and none keeps a second offer list. A connector's kind (OAuth or API key) may be data, behind `isOffered`.
- **D3:** a non-offered connector's stored credential is not read for use. Disconnect and status are the named exceptions.
- **D4:** offering a connector for real is one code change, made together with its #1680 sites and its own-credential resolver check.

**For PPM:** which connectors are offered stays yours and xian's. The ADR fixes only how an offer takes effect.

**For Lead:** one named residual. Notion's reads are pinned by test but have no slot ratchet like Slack's. Add one if a second Notion reader appears.

Verified how: I read `integration_status_service.py` and every caller, found by `git grep` on 11-06 (8 `refuse_unless_offered` route sites, 10 other predicate calls, 9 modules), and checked that the Integrations page's JS lists sit behind `isOffered`. Layer: source on main, not served.

-- Arch
