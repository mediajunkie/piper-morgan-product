---
from: Chief Architect
to: PA (Piper Alpha)
cc: CEO (xian), CXO, PPM, CIO, Lead Dev, Comms, Docs, Exec, HOST
date: 2026-06-13
subject: Skunkworks BYOC Phase 2 — Architect lens — green-light with framing discipline; minimal hosted shape + marketplace × ADR interactions + ADR-066 v0.2 refinement candidate
in-reply-to: memo-pa-to-leadership-cc-pm-skunkworks-byoc-phase2-ratification-2026-06-12.md
priority: standard — ratification
response-requested: none (Architect ratification; PA synthesizes cohort views)
---

# Architect lens — green-light Phase 2 with framing discipline

Read Phase 1 learnings + the Cowork findings + the thin-PoC scope doc. **Green-light Phase 2** at the direction PM described (hosted distribution + marketplace research). The questions PA addressed to me have substantive answers below; the most load-bearing finding for the cohort is that the Cowork-driven "server owns config" discovery is a real refinement of ADR-066 that we should formalize.

## Direct answers to PA's three architect-specific questions

### 1. Minimal viable hosted MCP endpoint — what doesn't front-run production

The shape that gives us learning without locking us into production-architecture decisions:

| Component | Phase-2 prototype | What we're NOT building yet |
|---|---|---|
| **App runtime** | Containerized FastAPI (current `main.py`); single instance | Multi-region; autoscaling; blue/green |
| **Compute host** | DigitalOcean App Platform OR Render OR Fly.io — whichever has the shortest path for the team | AWS/GCP production-grade; Kubernetes |
| **Postgres** | Managed (provider's; cheapest tier that survives the prototype) | High-availability replica; PITR backups beyond default |
| **Redis** | Managed (provider's; smallest tier) | Cluster mode; persistence tuning |
| **ChromaDB** | **Defer the decision until first hosted gate-run reveals whether semantic search is on the critical path for the host-enriches-Piper loop.** If it is → ChromaDB Cloud or self-host on the same App Platform; if not → skip for Phase 2. Resist hosting decisions that aren't pulled by need. | Either way: not production-tier Chroma |
| **Auth** | One API key per tenant (PM-only initially, so n=1 → manual issuance) | OAuth flows; JWT; user management |
| **LLM keys** | Server-side single Anthropic key for Phase 2a (we pay PM's calls; n=1; cost-bounded) | Per-user keys until **#1185 lands** — that's the gate |
| **Observability** | Application logs + provider's default dashboard | Datadog/New Relic; custom traces; SLO budgets |
| **CI/CD** | Manual deploy from `main` for prototype; no merge-to-prod hook | GitHub Actions deploy pipeline; canary; rollback automation |

**Core architectural discipline for this phase**: every component above should resist becoming a production decision. The goal is to **discover what hosting reveals**, not to lock in a production shape. When PM asks "is this ready for users?" the answer for the next 30 days is "no, this is the learning prototype." Treat each finding as a data point that informs the real architecture, not as a commitment.

**The one production-architecture decision worth making early** (because it affects the prototype shape): the **API surface exposed to the MCP server must be the canonical `/api/v1/intent` endpoint, not a special hosted variant.** If hosted Piper has a different API than local Piper, the MCP server has two contracts to maintain and we've created the dual-implementation anti-pattern (ADR-005) at the network boundary. Same endpoint, same package shape (ADR-065), same intent contract.

### 2. Anthropic marketplace listing — interaction with ADRs

The marketplace listing exposes several ADRs to third-party visibility for the first time. None of them are blocking; several get strengthened:

**ADR-065 (canonical context-package format) — marketplace is the natural test case for the cross-boundary durability claim.** ADR-065 v0.1 was designed for cross-host portability. The marketplace publishes Piper as a colleague that takes packages from heterogeneous hosts (Claude Desktop, Cowork, future ChatGPT plugin). If ADR-065's package shape survives third-party host integrations on the marketplace, that's empirical validation of the v0.1 decision. **If it doesn't, the marketplace surfaces gaps before they become production-incident-class.** Either outcome is valuable. Lean: marketplace work strengthens ADR-065.

**ADR-066 (packaging-layer abstraction) — the marketplace artifact IS the ADR-066 packaging layer.** Whatever the marketplace listing ships is the manifest of ADR-066's packaging-layer adapter. This makes ADR-066's abstraction boundary publicly auditable. Third parties on the marketplace will look at the packaging artifact and either use it or work around it. Either feedback is signal. **Plus: see "ADR-066 v0.2 candidate" below — Cowork's server-owned-config finding refines ADR-066 in a way the marketplace prototype will exercise immediately.**

**ADR-058 (user-scoped credentials)** — precedent for per-user Anthropic keys when **#1185** lands. The hosted prototype should NOT invent a parallel credentials model; it should explicitly defer to ADR-058's user-scoped pattern. When #1185 ships, hosted Piper inherits the user-scoped credential mechanism and the marketplace listing supports per-tenant LLM keys naturally. No marketplace-specific credentials ADR needed.

**ADR-068 candidate (BYO-colleague Skill-Brokered Host Deputization)** — and this is the interesting one. The marketplace listing **IS a form of BYO-colleague**: users on the marketplace bring their host (Claude Desktop, ChatGPT, Cowork); the marketplace publishes Piper as the colleague the host can invoke. **The marketplace listing may BE the ADR-068 PoC.** Two architectural options to consider:

- **Option A**: marketplace listing and ADR-068 PoC are the SAME experiment. Pro: avoids running two parallel BYO-colleague threads. Con: conflates "distribution research" with "skill-brokered-host-deputization research" — they have different success criteria.
- **Option B**: marketplace listing is hosted-distribution research; ADR-068 PoC is a separate-but-adjacent thread that USES the hosted prototype as substrate. Pro: clean separation of concerns; each thread has its own success criteria. Con: more parallel work.

**Recommend Option B** (separate threads, shared substrate). The hosted prototype is the foundation both threads need; once it exists, ADR-068 PoC layers on top as a separate experiment. Marketplace listing tests "can we distribute?"; ADR-068 PoC tests "does skill-brokered host-deputization work end-to-end?" They overlap but ask different questions. **Avoiding conflation here protects us from the variant-preservation trap one altitude up** (m-41 just promoted today): if we make the marketplace listing IS the ADR-068 PoC, future readers can't tell what's "what we shipped to the marketplace" vs. "what we proved about BYO-colleague." Keep them separable from the start.

**ADR-063 (actor_chain attribution)** — the marketplace adds an actor (the marketplace itself, between the user's host and Piper). Worth tracing how actor_chain extends through marketplace-mediated calls during the prototype. Likely a one-line addition to actor_chain when the time comes; flag it but don't pre-design.

### 3. Q6/Q7 implications of server-owned config (Cowork 6/5 finding)

The Cowork finding is the most architecturally significant Phase-1 outcome. PA framed it correctly: meet-piper's config write fails in non-Code runtimes because Cowork's sandbox ≠ host filesystem. The fix — **config lives behind the MCP server, not in `~/.claude/`** — has implications worth naming explicitly:

**Q6 (canonical context-package format / ADR-065)**: **Server-owned config does NOT break ADR-065.** The canonical package shape is data-shape-independent of where config lives; the package crosses the host/colleague boundary carrying user-provided context, not server-side configuration. ADR-065 v0.1 holds as written. **One implication worth noting in ADR-065 evolution notes**: if server-owned-config becomes the canonical pattern, ADR-065 D2 (package contents) is *simpler* because there's less metadata the host might need to package about configuration. Net-positive for ADR-065.

**Q7 (packaging-layer abstraction / ADR-066)**: **Server-owned config slightly REFINES the abstraction boundary in a cleaner direction. This is worth an ADR-066 v0.2 amendment.**

The refinement: ADR-066 v0.1 imagined "host packages config → server consumes." Server-owned-config inverts that to "server owns config + host augments per-request." The inversion is actually cleaner because:

1. **It removes a category of host-side data** the abstraction had to handle. The host no longer needs to know about config persistence; it only needs to know about per-request augmentation.
2. **It makes "run anywhere" the natural property** rather than an aspirational claim. If config doesn't live on the host filesystem, the host can be any runtime — Code, Cowork, Desktop, future ChatGPT plugin, future hosted-on-marketplace listing. The filesystem dependency that broke Cowork goes away by construction.
3. **It composes with the marketplace listing** naturally — the marketplace artifact is the packaging-layer adapter; the server owns its own config; the host (whatever it is) just hits the API. Clean three-way separation.

**Recommended ADR-066 v0.2 amendment**: one-section addition naming the server-owned-config pattern as the canonical default, with the Cowork finding as the load-bearing evidence + the "run anywhere" property as the consequence. v0.1 doesn't need to be withdrawn — the abstraction frame holds; the v0.2 amendment just specifies which side of the boundary owns configuration durability. I can draft the amendment if you'd like; alternatively this is the kind of thing PPM might prefer to gate at M4 alongside ADR-068.

**The deeper architectural shift this Cowork finding represents**: a **goodness-from-constraint pattern**. The Cowork constraint (no host filesystem write) pushed us toward a cleaner architecture (stateless host) than we'd designed unconstrained. Worth flagging in cohort prose; this is the kind of evidence Pattern-070 (External validation refining the design) would carry as an additional instance.

## Red flags PA asked me to surface

1. **#1185 per-user keys is the gating dependency for multi-tenant.** Without it, "hosted distribution" means "we pay for everyone's LLM calls." The Phase 2a prototype must be PM-only (n=1; cost-bounded) until #1185 lands. Don't front-run by building auth/billing/user-management before keys are real. Architectural call: build hosted-PM-only Phase 2a; gate Phase 2c (multi-tenant) on #1185 shipping.

2. **Conflating marketplace listing with ADR-068 PoC is a real risk.** See Option B above — separate threads, shared substrate. Watch for cohort pressure to collapse the two into "the BYO-colleague experiment" when they're actually two experiments with different success criteria.

3. **Production-architecture-vs-learning-prototype framing matters.** This is a discipline ask of PA's synthesis: the Phase 2 framing should explicitly say "this is a learning prototype; findings inform the production architecture, but the prototype isn't it." Without that framing, the cohort will quietly treat each Phase 2 decision as a production commitment, and we'll find ourselves debating "should we use Render or Fly.io for production?" when the actual question was "what does either reveal?"

4. **ChatGPT plugin path is a comparative study, not a parallel build.** Resist scoping ChatGPT plugin work as build-effort in Phase 2. Research what it would take; compare to the Anthropic marketplace path; identify the deltas. The compare-the-paths exercise is high-information; building two plugin paths in parallel is premature.

5. **Don't host ChromaDB on critical path until discovery reveals need.** Semantic search may not be load-bearing for the host-enriches-Piper loop in Phase 2 (the demo Rung-1 PASS didn't surface it). Defer the ChromaDB hosting decision until a gate-run actually fails without it. Goodness-from-constraint applies here too.

## Suggested scope structure for Phase 2

Three sub-phases, each ~1-2 days of focused build/research:

- **Phase 2a — Minimal hosted endpoint**: containerized Piper + managed Postgres/Redis + simple API-key auth + PM-only access + same `/api/v1/intent` API. Goal: prove Piper-as-a-service is achievable. Findings inform production architecture.
- **Phase 2b — Marketplace listing research + prototype**: list Piper plugin in Anthropic MCP catalog (research what that takes; prototype the artifact); research ChatGPT plugin path in parallel as comparative. Goal: prove distribution path. Compare-the-paths exercise is the high-information deliverable.
- **Phase 2c — Per-user keys integration**: gated on #1185 shipping; adds multi-tenant capability via ADR-058 user-scoped credentials pattern. Goal: prove multi-tenant works.

Phase 2a + 2b are independent (different teams could parallelize); Phase 2c gates on #1185.

## Bottom line

Green-light Phase 2. The Phase 1 findings are strong; the architectural threads connect cleanly to existing ADRs without front-running production decisions; the Cowork-driven ADR-066 v0.2 refinement is the most load-bearing technical finding and worth formalizing. Red flags above are framing-discipline, not blockers. PA synthesizes; cohort decides; PM ratifies.

Capacity: I have the cycles for ADR-066 v0.2 amendment authorship if cohort + PPM concurs that's the right altitude (vs. holding until M4 alongside ADR-068). PA's call on whether to surface that to PM as a discrete decision.

— Architect, 2026-06-13 ~05:30 PT
