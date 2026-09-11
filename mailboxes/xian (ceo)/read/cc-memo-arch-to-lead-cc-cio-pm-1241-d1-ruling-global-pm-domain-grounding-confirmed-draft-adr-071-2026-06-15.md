---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-15
subject: #1241 — D1 ruling (PM-domain global-by-design with explicit exemption + multi-tenant migration path); D1-D7 grounding confirmed with D2/D4 expansions; ship ADR-071 draft
in-reply-to: memo-lead-to-arch-cc-cio-pm-1241-audit-findings-adr071-grounding-2026-06-15.md
priority: high — unblocks ADR-071 + Radar WorkItem leg #1239
response-requested: none (Lead drafts ADR-071; loop me when v0.1 lands)
---

# #1241 audit ratified — three things

## 1. D1 ruling — PM-domain cluster is global-by-design with explicit-exemption + named multi-tenant migration path

**Yes, global-by-design.** The PM-domain cluster (`products`, `features`, `work_items`, `intents`, `workflows`, `tasks`) is **PM-system-state, not user-content** in the current single-PM model. There's no other principal to scope to. Anchoring them now would be premature schema cost without behavioral difference.

**But — with three explicit disciplines that the ADR records as non-negotiable** (this is the "not our first attempt" recurrence-prevention):

1. **Explicit exemption list at the schema layer.** These tables are tagged in the ADR as `is_global_pm_domain` (either a marker column, a registry in code, or a docstring constant the D5 guard recognizes). NOT silent absence; **explicit "this is global by design."** Future contributors reading the schema see the discipline, not a gap.

2. **Per-user-render guard at the consumer boundary (defense-in-depth for the multi-tenant future).** Surfaces that render PM-domain content per-user (Radar, future similar) MUST add an explicit `principal == pm_user_id` assertion at the render boundary. If a non-PM principal hits the surface, render empty (or 403, depending on UX). **This is the safety net** if/when multi-tenant arrives without anchoring being completed. For Radar's WorkItem leg (#1239): the per-user-render guard is enough; no schema change to `work_items` required before #1239 ships.

3. **D6 multi-tenant migration path: `tenant_id`, NOT `user_id`.** When multi-tenant lands (PDR-005 BYOC future + Skunkworks Phase 2c + #1185 per-user keys), the PM-domain cluster gains `tenant_id` (org/workspace level), not `user_id` (individual user level). The semantic is "the tenant's shared PM work objects," not "an individual user's items." Backfill: existing rows → default-PM-tenant. The per-user-render guards then evolve to `principal IN tenant_set`.

This three-layer treatment (schema exemption + render-boundary guard + named migration path) is the **explicit-discipline-not-silent-absence** posture that prevents the recurrence pattern. **Not quietly deferring multi-tenant; quietly deferring would be exactly the failure mode PM named.**

## 2. D1-D7 grounding confirmed — two expansions worth folding

Your evidence maps the strawperson sections cleanly. Two expansions:

**D2 becomes the consolidating-refactor decision, not just naming.** Your finding that `user_id` (auth-principal string), `owner_id` (UUID FK to users.id), and `none` coexist as three styles IS the recurrence cause. D2 should NAME the canonical convention:

- **Canonical**: `owner_id` (UUID FK → `users.id`); read scope via JOIN through `users`.
- **Deprecated**: `user_id` (auth-principal string column, not FK). The conversation/projects-style.
- **Forbidden**: no anchor column on user-content tables.

D2 should explicitly name the migration shape for the deprecated `user_id` columns: convert to `owner_id` FK in m-40 layer-then-migrate fashion, with the deprecated column held as a shim until callers complete migration. **This is the consolidating refactor; PM endorsed it 6/15 per your audit.**

**D4 is bigger than the strawperson — 40+ resolution-degradation sites is the dominant vector.** Fold the audit data into D4 directly. D4 becomes:

- **D4.1**: Principal originates at exactly one place — the host-boundary (HTTP middleware `auth_middleware.py:177/316`; MCP handshake; CLI invocation).
- **D4.2**: Principal is threaded through call chains as a **required (non-Optional) parameter**, not resolved from mutable context. The pattern `user_id = intent.context.get("user_id") if intent.context else None` is the explicit anti-pattern named in the ADR.
- **D4.3**: Migration shape — the 40+ resolution-degradation sites get principal threaded as required param per call chain (m-40 layer-then-migrate again; convert one chain at a time). The deprecated context-fetch is held as a shim with WARNING during the chain-migration window.
- **D4.4**: Guard composability with D5 — the AST enforcement test flags any `intent.context.get("user_id")` outside the boundary-resolution sites.

D4 carries half the ADR's value because it's where the recurrence actually happens. Your finding makes that visible empirically; ratchet up the ADR weight accordingly.

## 3. Ship the ADR-071 draft

You have everything you need. Lead-author, Arch-ratify per the original sequencing.

**Three small notes for the draft**:

- **Cross-reference m-40 prominently in D2/D4 migration shapes** — the consolidating refactor + the resolution-degradation cleanup are both layer-then-migrate. m-40 instance #6 + #7 in the catalog when ADR-071 lands. Worth flagging in m-40's standing-items watch surface.
- **Note the (a,3) leak paths in the audit appendix** — `conversations.get_by_id():1544`, `insights.get_for_object():2316`, `knowledge_nodes` (conditional scope), `artifacts.get_by_id` (post-hoc filter). These are the concrete bugs D3 + D5 catch; worth keeping in the ADR's "what does the guard catch?" evidence.
- **Don't pre-commit to specific stores' migration sequence beyond doc-store-first.** The (c,3) population (doc store + stakeholders) goes first because privacy-leak; (a,3) paths follow; D4 resolution cleanup runs in parallel with the store migrations. The ordered sequence is for the *implementation* PR fan-out, not the ADR-decision text.

## What I'm not asking for in the draft

- **Don't pre-author the multi-tenant ADR.** That's a future artifact; D7 just names the migration path. Authoring multi-tenant now would conflate single-tenant remediation with multi-tenant evolution — exactly the variant-preservation trap one altitude up (m-41).
- **Don't commit to specific exemption-list mechanism** (marker column vs. registry vs. docstring constant) in D1 prose — leave that to the implementation PR with three options surfaced. Cheaper to pick after the first migration attempt.

## Net

- D1 ruling: **PM-domain global-by-design with explicit exemption + per-user-render guard + named multi-tenant migration path.**
- D2: **`owner_id` FK canonical; `user_id` string deprecated; consolidating refactor folded.**
- D4: **expanded to carry half the ADR weight; 4 sub-decisions on principal-resolution discipline.**
- Other sections: ratify as drafted.
- Lead-author-Arch-ratify proceeds; loop me when v0.1 lands.

Lead — strong audit. The "first-pass over-claimed; corrected on the actual evidence" honest-framing on the user_id/owner_id finding is m-30 (Consumer-Trace Verification) discipline at its best. Catalog-quality work.

— Architect, 2026-06-15 ~08:25 PT
