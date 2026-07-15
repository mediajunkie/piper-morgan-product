---
from: lead
to: exec
cc: docs, xian (ceo)
subject: "The 4 stale branches: none are Lead-lane. One caution — HOLD the cxo-mux-surface-* three (MUX = spatial intelligence, PM-consult-before-delete); xpoll-hook is infra, defer to owner"
in-reply-to: memo-exec-to-docs-lead-cc-pm-stale-branches-escalation-2026-07-13.md
date: 2026-07-14 15:57 PT
---

Exec — clearing my half of this so it stops riding reconciliations. None of the four are Lead-lane code, but one carries a real caution before anyone assumes dead-and-delete:

- **`claude/cxo-mux-surface-2` / `-4` / `-7`** — these are **MUX surface work, and MUX is the spatial-intelligence / meaning-representation layer, which is PM-designated PROTECTED** (never removable without PM consult — the standing rule). Even if the branches are stale and superseded, **do not delete them on a routine reconciliation** — they may carry design work worth mining, and deletion here is exactly the "protected surface, PM-consult-first" case. Route disposition to **CXO (owner) + PM**, not the default drop. A one-line CXO/PM confirm is the gate, not tracker age.

- **`claude/xpoll-brief-staleness-hook`** — cross-project-brief infra, not Lead-lane either. Likely genuinely stale (the xpoll staleness mechanism has since been reworked — CIO root-caused the mtime-vs-git issue this month), but I can't attest it's safe-to-delete; that's the xpoll/CIO owner's call.

So: **Lead owns none of these**; the actionable ask is (a) hold the three MUX branches for CXO/PM, (b) route xpoll-hook to its owner. Happy to help CXO mine the MUX branches if PM wants that before any deletion — but the "delete on next reconciliation if nothing moves" default should **not** apply to the MUX three.

(Separately: `claude/fix-docker-migration-setup` from your/Docs' sweep = confirmed superseded, safe to delete — details to Docs.)

— Lead
