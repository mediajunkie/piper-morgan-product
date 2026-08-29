# Leg A3 — Scope Inflections: from "an assistant xian truly owns" to "enterprise multi-tenant SaaS"

*Filed verbatim-condensed 2026-08-29. Denominator: all 80 ADR headers (~15 in full), all 8+ PDRs,
multi-tenancy audit, requirements.md, founding vision doc, roadmap v18.8 + CORE/ tree,
beta-blockers, decisions.log, release notes v0.8.1–11, targeted git archaeology on the
19,236-commit history. Session logs NOT read.*

## The inflection table (11 inflections)

| # | Inflection | Where/when | Scope decision or technical default? |
|---|---|---|---|
| 0 | "NFR-020: multi-tenancy for team isolation" + RBAC/audit/enterprise-phase boilerplate | requirements.md, **2025-06-06 — day 5 after bootstrap** | **Technical default.** No alternatives, no buyer, no debate. |
| 1 | Founding vision written in market voice ("Sarah, a junior PM"; "For Product Organizations… at scale") | vision-v1, 2025-06-21 | **Genre default.** Single-owner framing appears NOWHERE in the founding written corpus. |
| 2 | 8-service production-grade staging (Prometheus/Grafana/Nginx) | ADR-007, 2025-07-20 | Technical default; never scoped to a user. |
| 3 | JWT/standards auth for "enterprise adoption… multi-tenant and federated deployments… SSO… marketplace" | ADR-012, 2025-08-10 | **Technical default wearing strategy language** — weighs auth options, never the product question. |
| 4 | The SaaS/platform commitment: 3 revenue streams; "1000+ active PM users by Q4 2026 *(Target: Based on SaaS growth benchmarks)*"; federation | ADR-000 (status: **Proposed, never Accepted**) + ADR-014–022, 2025-08-17 | **Closest thing to an explicit scope decision** — but no cost accounting, no bet-shape, buyers derived from benchmarks not people. ADR-021 records "5 platforms federated" incl. Jira/Linear; neither survives in the current integration set — aspiration recorded as achievement. |
| 5 | Multi-user alpha machinery (users table, JWT live #162, key rotation, team-keys "Target: Enterprise customers") | commits Oct–Nov 2025; alpha v0.8.1 ships 11-24 | **Never recorded as a scope decision.** NO ADR/PDR/log entry decides "alpha = multiple external users" — the conversion arrived implicitly as launch prep. |
| 6 | RBAC (VIEWER/EDITOR/ADMIN, is_admin) | ADR-044, 2025-11-22 | **Mixed**: implementation was an explicit anti-enterprise choice (JSONB, 5 hrs vs 2–3 wks) — a genuine counter-inflection — but its drivers ("1000+ users," "SOC2") inherited unexamined from day-5 defaults. |
| 7 | Multi-tenancy isolation retrofit (owner_id everywhere + speculative workspace_id/TenantContext) | ADR-058, #734, 2026-01-30 | **Forced** — real testers leaking into each other; the scope question answered by facts on the ground, not weighed. |
| 8 | Hosted service (alpha.pipermorgan.ai droplet) | #1162, 2026-06; v0.8.8 | Operational necessity (local installs defeating non-dev testers); SaaS-operator consequences surfaced AFTER (06-25: `create_user` had NO registration gating — "removing the gate = OPEN PUBLIC REGISTRATION"). |
| 9 | SaaS-operator cascade: per-user keys #1185, encryption-at-rest ADR-074, invite codes #1344, anonymous BILLING fallback #1343, usage caps ADR-076, password/email lifecycle | Jun–Jul 2026 | Individually well-reasoned; **collectively the unchosen arrival of a hosted-identity-provider-plus-billing operation.** |
| 10 | Enforcement era: audit verdict "retrofitted one surface at a time, reactively"; ADR-079 + lints | Jul 2026 | Corrective — the cost of #0–8 crystallizing into standing enforcement infrastructure. |
| 11 | Standing Enterprise tier: GitHub milestone dated **Jul 4 2027**; team-keys "Target: Enterprise customers" | since 2025-10 | Speculative tier still on the books. |

**Counter-inflections (for fairness)** — the corrective instinct appeared repeatedly, but always
locally and late: ADR-044's lightweight implementation · ADR-051 amendment (refused
RequestContext-everywhere as "stylized ceremony") · ADR-071 D1 (PM-domain global-by-design;
"anchoring them now is premature schema cost") · PDR-006 (hosted MCP dissolves the server-side-LLM
problem) · "no optional complexity" formalized only 2026-08-27 — which itself found two of three
"MCP connectors" are shims with zero real MCP calls.

## Costs (compressed)

- **#3 JWT**: 26 files across security/middleware; token blacklists, refresh rotation, key mgmt.
  Foreclosed cookie-session/no-auth localhost simplicity. Bought (late, part luck): the identity
  substrate PDR-006's fail-closed owner_id boundary now anchors to. **None of ADR-012's Phase 3/4
  (OAuth provider, federation, SSO, marketplace) was ever built.**
- **#4 meta-platform**: carried as posture — every 2025 ADR after it justifies itself against
  platform framing. The "pure tool" option was explicitly REJECTED in ADR-000's alternatives
  ("misses platform economics and industry leadership").
- **#5+#7 (the expensive one)**: owner_id on 9+ tables; 67+ ownership-checked methods; 26 protected
  endpoints; THREE inconsistent principal-anchoring styles (ADR-071); 40+ principal-degradation
  sites still draining; two standing lints + allowlists; JobContext/TenantContext/RequestContext +
  an all-zeros DEFAULT_WORKSPACE_ID for workspace features that don't exist. Brittleness receipts —
  bug classes that only exist because N>1 users share state: #734, #1366, dinp provider-pin, C1–C4
  (PM's config silently overriding every tester's settings), S1/S2, the sender-impersonation bug
  found 4 days before beta. Bought: ~10 real alpha testers + first-contact findings only outsiders
  produce.
- **#8–9 hosted cascade**: encryption service + backfill + 2 deferred decisions; usage-cap
  middleware + Redis dependency; invite machinery; billing fallback; email lifecycle. **A material
  share of distance-to-beta WAS the SaaS shape** (beta-blockers epics named "Multi-tenancy & data
  protection" and "External-tester auth/account lifecycle"). Aggregate: 595 Python files, ~201k
  lines, 80 migrations; beta target moved again 08-08. **Six of the ten most recent ADRs (071, 074,
  075, 076, 078-D1a, 079) are ownership/tenancy/hosted-load architecture** — the tail of the
  decision record is dominated by paying for the earlier inflections.

## The buyer question

**Named buyer at decision time**: ADR-058 (real leaking testers), ADR-074 (keychain-less droplet),
ADR-076 (PM-ratified caps), #1344 — all *remediations*: real buyers, buying repairs on the earlier
unnamed-buyer purchases.

**No named buyer (speculative complexity)**: NFR-020/015/014 (June 2025, zero users) · ADR-012's
enterprise/SSO/marketplace (zero users, no customer named) · ADR-000's "1000+ PMs by Q4 2026"
(sourced to benchmarks; Q4 2026 is now, count is ~a handful) · ADR-021 Jira/Linear federation (no
team named; neither survives) · workspace_id/TenantContext (buyer still unnamed, still zero-UUID) ·
sharing roles (no named collaborator; no sharing use case in any doc) · team keys ("Target:
Enterprise customers" verbatim) · the Jul-2027 Enterprise milestone · Slack breadth (no proven case,
per the 08-26 gate review).

**The structural finding (verbatim)**: the one decision that would have converted all later buyers
from speculative to real — *"we will recruit external alpha testers, therefore this is a multi-user
product"* — is the one decision with **no artifact**. It was never made AS a decision anywhere
findable; by ADR-058 it appears as a settled fact ("alpha users already multi-tenant"). Everything
downstream then had a real buyer, because the unexamined step had already manufactured one.

## The counterfactual spine (REASONED COUNTERFACTUAL — labeled inference, not evidence)

Held single-owner vision (one human principal, BYOC/PDR-006 as eventual distribution):
- **Exists essentially unchanged**: intent stack + floor-first routing, knowledge/RAG,
  GitHub/Calendar/Notion connectors, conversational floor + persona, cross-session
  memory/composting, domain models, LLM client, Postgres, honest-degradation discipline. None is
  tenancy-derived.
- **Would not exist**: users table, auth lifecycle, JWT+blacklists, RBAC/sharing, owner_id threading
  (67+ methods), both scoping lints, ADR-058's nine phases, workspace_id, invite codes, usage caps,
  billing fallback, per-user key plumbing, encryption-at-rest Dim A. And the entire bug CLASS those
  manage cannot occur with one principal. ~Six of the last ten ADRs would have no reason to exist.
- **Still hard regardless** (honesty about what single-owner does NOT buy): routing integrity,
  confabulation control, connector depth, most of Epic F's correctness bugs.

**The bridge that makes it sting (verbatim)**: PDR-006's ratified model is, functionally, a
rediscovery of "the user brings their own everything; the server holds one person's tools and
memory" — the shape a single-owner architecture would have grown toward directly. The project is
now converging on a model most of the multi-tenant SaaS purchases were not needed for — the
strongest available evidence that the June-2025→June-2026 inflections were scope loans, and 2026
has been the year of paying interest. Eleven inflections; only one (ADR-000) even *shaped* like a
scope decision; none cost-boxed.
