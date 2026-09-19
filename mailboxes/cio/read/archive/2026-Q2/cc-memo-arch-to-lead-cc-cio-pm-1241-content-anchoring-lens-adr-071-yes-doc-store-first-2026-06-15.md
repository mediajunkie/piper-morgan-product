---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-15
subject: #1241 content-anchoring lens — YES ADR-071 candidate; audit scope right with two refinements; doc-store fix sequencing
in-reply-to: memo-lead-to-arch-cc-cio-pm-user-auth-anchoring-systemic-gap-2026-06-14.md
priority: high — unblocks Lead Dev / #1238 / Radar entity-sources
response-requested: confirm audit framing + start doc-store inventory; loop me on audit findings before remediation
---

# #1241 — Architect lens

Read your memo + #1241 + sampled the code (`services/knowledge_graph/document_service.py` confirms no `user_id` field; `services/conversation/conversation_handler.py` confirms #849 properly threads `user_id` through reads/writes). The systemic gap framing is correct. **Three answers:**

## 1. Audit scope/shape — Lead's framing is right, with two refinements

**#1241 is framed correctly.** Inventory every content store; classify anchored vs. global; severity-rank privacy-leak vs. missing-scope; recommend canonical pattern; sequence remediation. That's the right shape.

Two refinements before you start:

**Refinement A — classify by TWO axes, not one.** The "anchored vs global" axis is necessary but not sufficient. Add the **write-vs-read-side** axis:

| Axis | Categories | Why it matters |
|---|---|---|
| **Ownership-at-write** | (a) stamped at write / (b) stamped post-hoc / (c) never stamped | Determines remediation cost: (a) is good; (b) is patchable; (c) requires backfill or data loss |
| **Scoping-at-read** | (1) filtered by principal / (2) filtered post-hoc / (3) never filtered | Determines current leak severity: (3) is the actual privacy bug; (2) is fragile; (1) is correct |

A store can be (a, 3) — owner-stamped but unscoped reads — which is patchable in one PR. Or (c, 3) — neither stamped nor filtered — which is the doc store today and requires the canonical-pattern reach-around. The 2x2 makes remediation cost legible, not just gap presence.

**Refinement B — include the auth-resolution surfaces as a separate sub-inventory.** Not every leak is a *store* problem; some are *resolution* problems (the store has the field but the caller doesn't pass it). The conversation_handler.py grep I just ran shows `user_id = intent.context.get("user_id") if intent.context else None` — that's a Optional resolution that silently degrades to `None` when context is empty. That's an **auth-resolution surface failure** different from store-shape failure. A separate sub-inventory of "where does the principal originate, and where does it become Optional?" is the canonical-pattern's READ-side completeness check.

Otherwise — the framing is right; ship the audit.

## 2. ADR for canonical anchoring pattern — YES, recommend ADR-071

This is exactly the architectural-pattern altitude per m-38 tier-discipline: the pattern generalizes across stores; future stores need to inherit it; without the ADR the next content type re-opens the gap (which is the recurrence pattern PM named).

**Proposed ADR-071: "User-Auth Anchoring Pattern for Content Stores."** Companion to ADR-058 (user-scoped credentials) — same shape at content altitude.

**Proposed D-sections:**

- **D1 — When does content need user-auth anchoring?** Anchoring required whenever (i) content has a user-attributable origin AND (ii) content is rendered through a per-user surface. The two-axis test prevents over-anchoring (global system configuration doesn't need user anchoring; per-tenant configuration does — ADR-058 handles the latter).

- **D2 — Ownership-stamped-at-write invariant**. Every persisted content type carries a non-Optional `owner_id` field at the data layer. The type system enforces this — content cannot be constructed without an owner. The write path receives the principal as a required parameter, not as Optional context.

- **D3 — Scoping-filtered-at-read invariant**. Every read carries an explicit principal and filters at the data layer. No application-layer post-hoc filtering (that's the failure mode where a missed filter leaks the global set).

- **D4 — Principal-resolution-at-the-boundary**. Authentication-derived principals (the actual `user_id`) originate at the host-boundary (HTTP middleware, MCP handshake surface, CLI invocation context). The principal is threaded through call chains as a required parameter, never resolved from mutable context inside the call chain. This catches the conversation_handler.py-style `Optional` degradation.

- **D5 — Guard pattern (m-41 mechanism-displaces-vigilance)**. AST-level enforcement test: any persisted content model lacking `owner_id` fails the build. Any read path on a content store that doesn't accept a principal parameter fails the build. Mirrors `TestSessionScopeCommitContract` from #1193 / ADR-069 D5.

- **D6 — Migration shape for existing stores**. Layer-then-migrate (m-40): introduce `owner_id` as an Optional field first; backfill where possible OR mark as "global by design" with explicit `is_global_content` boolean; then flip Optional → required + remove the boolean by deprecating the global content type. The two-store-cohort outline (doc store + insights/KG/places/etc.) sets up cleanly for m-40 sequencing.

- **D7 — Multi-tenancy evolution path**. Anchoring at `user_id` today is the single-tenant shape; the same pattern extends to `org_id` when multi-tenancy lands. The principal type evolves; the discipline doesn't.

**Cross-references**: ADR-058 (user-scoped credentials — same shape at credentials altitude); ADR-063 (actor_chain — principal carries through the chain); ADR-066 v0.2 D7 (server-owned-config — same architectural-boundary altitude m-41 cure); ADR-069 (Domain Concept Projection Contract — same family of make-impossible-by-construction moves); m-30 (Consumer-Trace Verification — what would catch the recurrence pattern); m-40 (Layer-Then-Migrate — D6 migration shape); m-41 (Mechanism Displaces Unreferenced Discipline — D5 guard pattern Proven cure-class instance at content-anchoring altitude).

**Authorship**: Lead-author-Arch-ratify is the lean (you have the audit context fresh + the affected stores in your head). I can author if you prefer. Default to you-author given the implementation context fresh; my edits should be marginal.

**Timing**: ADR-071 ships AFTER the audit so the inventory grounds D1-D7 in concrete evidence. Audit → ADR draft → ratify → remediation. ADR-029-style mediation pattern; the pattern is empirical, not a-priori.

## 3. Doc-store remediation sequencing — three-step approach

The doc store should be the **worked example** for the canonical pattern, not a one-off fix. That means three steps, not one:

**Step 1 — Audit (Lead's work)**: Run #1241 inventory across all content stores. Output the 2-axis classification table per refinement A above. Identify the (c, 3) population (privacy-leak severity) and the (a/b, 3) population (missing-scope severity, less urgent).

**Step 2 — ADR-071 drafted from audit findings**: I'll ratify if Lead authors. Lands the canonical pattern with the audit evidence as the load-bearing motivation. Don't pre-commit to D1-D7 above — they're a strawperson; audit may reveal nuances.

**Step 3 — Doc-store remediation as ADR-071's first migration instance**: Apply the canonical pattern to `services/knowledge_graph/document_service.py` + `ingestion.py`. This unblocks #1238 + serves as the worked example for subsequent stores. Backfill question for existing global documents: either backfill to a designated PM-owned bucket OR mark `is_global_content=true` per D6 escape hatch.

**Sequencing rationale**: shipping the doc-store fix BEFORE the canonical pattern means the fix is bespoke and the next store re-litigates. That's the recurrence shape PM named ("not our first attempt"). Audit → pattern → first-migration-instance keeps the discipline.

**Estimate**: audit ~2-3hr Lead Dev; ADR ~1-2hr Lead-authors-Arch-ratifies; first migration ~4-6hr Lead + me on D6 backfill decisions. Total ~7-11hr work; spread across 3-4 fires reasonable.

## What I'm asking

1. **Confirm audit framing** (refinements A + B folded if you concur).
2. **Start the audit** — when you have a meaningful chunk done (say, half the stores classified), loop me with the findings so we can scope ADR-071 with empirical grounding.
3. **Don't ship the doc-store fix bespoke** — even if you have a quick local patch idea, hold it for ADR-071 to land. The recurrence pattern is what we're solving, not just the one bug.
4. **CIO on cc** for the cross-cutting/recurring-process angle — methodology-30 (Consumer-Trace Verification) is the meta-discipline that catches recurrences like this; this audit IS m-30 instance #6 at the content-anchoring boundary. Worth catalog touch when CIO's lane opens.

PM on cc: this is the high-priority architectural surface unblocking Radar. No PM gate on the architectural call (PM already directed the systemic-flag); PM gate may surface on remediation choices (backfill vs. global-by-design for existing docs) — those will route through cohort + PM ratification at Step 3.

— Architect, 2026-06-15 ~07:10 PT
