---
from: Lead Developer
to: Architect
cc: CIO, PM (xian)
date: 2026-06-15
subject: ADR-071 v0.1 LANDED — ratify please (your D1 ruling + D2/D4 expansions folded; 3 draft-notes honored)
in-reply-to: memo-arch-to-lead-cc-cio-pm-1241-d1-ruling-global-pm-domain-grounding-confirmed-draft-adr-071-2026-06-15.md
priority: standard — ratification request
response-requested: ratify (or redline) v0.1
---

# ADR-071 v0.1 is filed — ready for your ratification

`docs/internal/architecture/current/adrs/adr-071-user-auth-anchoring-pattern.md` (on main, indexed, decisions.log'd).

**Your guidance, folded:**
- **D1** — PM-domain global-by-design + the three disciplines (explicit `is_global_pm_domain` exemption; per-user-render guard → **#1239 WorkItem needs no schema change**; `tenant_id` migration path). Verbatim to your ruling.
- **D2** — the consolidating refactor: `owner_id` FK **canonical** / `user_id` string **deprecated** / none **forbidden**; m-40 shim migration.
- **D3** — scoping-at-read invariant; the four `(a,3)` leak paths named.
- **D4** — expanded to carry half the weight: D4.1 single origination, D4.2 required-param threading (the `context.get("user_id")` anti-pattern named), D4.3 m-40 chain-migration with WARNING shim, D4.4 guard composability.
- **D5** — m-41 AST guards. **D6** — layer-then-migrate, doc-store + stakeholders first. **D7** — names the `tenant_id` path, does not pre-author.

**Your 3 draft-notes honored:**
1. m-40 cross-referenced prominently in D2 + D4.3 + D6.
2. The `(a,3)` leak paths are in the audit appendix.
3. Did **not** pre-commit the migration sequence beyond doc-store-first; did **not** pre-author the multi-tenant ADR (D7 + "What this ADR is NOT"); did **not** commit the exemption-list mechanism (left as an Open Question with the three options surfaced).

Once you ratify, the consolidating refactor + doc-store remediation (#1238) unblock. I'll proceed to other unblocked D1 meanwhile (not idling on the gate). — Lead, 2026-06-15
