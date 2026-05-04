# Cross-Pollination Brief — May 3, 2026

PM's Saturday session covered two distinct arcs: first, shipping #1018 Phase 2 (audit_transparency durable PostgreSQL storage) and closing three cluster regressions (#1006/#1007/#1008) in one merged commit; then running the audit-cascade skill against four M2d MUX Lifecycle issues and finding the gate NOT PASSED — two issues carrying stale "pending discovery" framing from March when the discovery completed in late March. Restructure yielded four new focused issues and a conceptual-integrity gate added to the M2d completion criteria. PM also published "The Drift You Don't Notice" — fully syndicated to pipermorgan.ai, Medium, and LinkedIn. Klatch is quiet; Iris walkthrough Surfaces 3-8 + Pass 2 still pending after the Surfaces 1-2 session paused May 1.

## Key Insights

### 1. PM: audit_transparency durable storage ships — transaction-boundary isolation pattern

**From:** PM commits `fd338c8` + `fc79de3` (May 2, 16:15 UTC); `dev/2026/05/02/2026-05-02-1555-lead-code-opus-log.md`
**Relevant to:** Klatch (any future durable audit/session storage design)

#1018 Phase 2 merged in one commit closing 4 issues: the `audit_transparency` service's in-memory `audit_logs` list replaced with a `EthicsAuditRepository` backed by PostgreSQL (`ethics_audit_log` table, 4 indexes, 6 repo methods). Cluster regressions closed together: #1006 (TIMESTAMPTZ throughout, timezone-aware datetime test), #1007 (phone PII pattern added to redactor — prior pattern matched SSN format 3-2-4 but missed common 3-3-4 phone format), #1008 (AsyncMock vs Mock in tests for await-on-list). `EthicsAuditCleanupJob` ships with post-#948 cancellation hygiene (`asyncio.current_task()` captured at start, cancel-and-await in stop). 17/17 audit-transparency tests pass.

The architecturally notable design decision: **Q2 transaction-boundary isolation** — `AsyncSessionFactory.session_scope()` is called per-audit-write rather than sharing the request's transaction. This means an audit-write failure swallows without rolling back the user-facing request. The explicit tradeoff: audit reliability is subordinate to request reliability. Verified by a dedicated test (`db_failure_does_not_propagate`).

**Suggested action:** Klatch — if Daedalus or Mnemosyne designs any durable storage for session logs, audit trails, or MCP server write-backs, the transaction-boundary question is live: should a storage failure surface to the user or swallow silently? PM's choice (swallow, isolate) is appropriate for audit sidechannel infrastructure but not necessarily correct for primary-path writes. Name the boundary posture at design time.

---

### 2. Audit-cascade catches discovery-phase staleness: issues filed during a discovery phase don't automatically update when discovery completes

**From:** PM `dev/2026/05/02/m2d-audit-cascade-findings.md`; `dev/2026/05/02/2026-05-02-1555-lead-code-opus-log.md`; commits `0b88e93` (findings), `d1c54dd` (restructure)
**Relevant to:** Klatch (any issue backlog backed by design-phase research; MUX-Lifecycle analog items in the Klatch backlog)

Lead Dev ran audit-cascade on 4 M2d MUX Lifecycle issues before writing gameplans. Issue gate **NOT PASSED** on first read.

**Two stale-placeholder findings:**
- **#707 (MUX-INSIGHT-SURFACING)**: body said "TBD pending #706 discovery." Discovery completed 2026-03-24 — over a month earlier. The decisions exist (`insight-surfacing-rules.md`, `objects-catalog.md`, `views-objects-roadmap.md`): Insights are soft objects, not lifecycle objects; three surfacing modes (Pull/Passive/Push) with different infrastructure and trust-gating requirements. Implementing from the stale body risked flattening all three modes into one ticket and ignoring the Stage 3+ trust gate on Push.
- **#714 (MUX-LISTS-LIFECYCLE-UI)**: body treated "lifecycle vs staleness" as open; source docs already answered (Lists have no lifecycle state; staleness is a distinct concept needing its own design pass). Body and GitHub milestone disagreed (body: Post-MVP; GitHub: MVP). Implementing as written risked treating staleness as a lifecycle stage — conceptual flattening.

**One silent-omission finding:**
- **#703 (MUX-LIFECYCLE-UI)**: COMPOSTED state — the most distinctive MUX UX concept ("I learned that..." + "filing dreams" framing) — not explicitly required in acceptance criteria. The MVP child issues could ship DEPRECATED → ARCHIVED without ever surfacing the COMPOSTED experience phrase.

**Restructure result:** 4 new issues filed (#1030 MUX-INSIGHT-PULL, #1031 MUX-INSIGHT-PASSIVE, #1032 MUX-INSIGHT-PUSH, #1033 MUX-COMPOSTED-EXPERIENCE), #707 reframed as tracking parent, #714 rewritten (staleness-spec-first scope; "Lists are non-lifecycle" decision folded in), #869 relocated to M2e (IA work, not MUX). New conceptual-integrity gate added to M2d completion criteria.

**Lead Dev's process observation** (worth quoting): "Issues filed during a discovery phase become stale once the discovery completes, and the staleness isn't always reflected back into the issue bodies. This is a normal product-management drift signature. The audit-cascade catches this exactly when it should — between issue and gameplan."

**Suggested action:** Klatch — this pattern is directly transferable. If any Klatch backlog issue contains "TBD pending [research/design/RFC] completion" language, check whether that dependency is still open. If the referenced research is done (e.g., any closed RFC or completed design doc), the issue body needs to fold in the conclusions before it becomes a gameplan. The audit-cascade skill's job is exactly this: verify that live decisions are reflected in implementation-facing artifacts before any code runs.

---

### 3. "The Drift You Don't Notice" published — PM's first insight post, fully syndicated

**From:** PM commits `47998de` (editorial calendar), `6b41ca5` (Medium/LinkedIn URLs added, May 2)
**Relevant to:** Klatch Calliope (PM's publication channels + narrative arc; topic resonance with methodology discipline)

PM published "The Drift You Don't Notice" on May 2 at `pipermorgan.ai/blog/the-drift-you-dont-notice`. Full syndication confirmed: canonical site, Medium, and LinkedIn (all three in same session). Calendar description: "methodology erosion through imitation" — the image description captures the metaphor: a ghostlike clerk feeding "yesterday's" page into a copier while the original spec sits unused, with copies becoming progressively degraded.

**Publication context:** This is PM's first `insight` category post (vs. `ship` newsletter or `building-piper-morgan` narrative). The editorial calendar's insight backlog dates to February 2026; this post unlocks what may become a third publication track alongside the Ship newsletters and the Building Piper Morgan Medium series.

**Topic resonance:** The underlying concern — implementing from yesterday's artifact rather than returning to the current source doc — is directly what the M2d audit-cascade finding (Insight 2) caught in practice this week. The two are related: #707 and #714 were both drifted copies of earlier thinking that weren't updated when the original spec moved. "The Drift You Don't Notice" names the class of problem; the M2d audit is a live instance.

**Suggested action:** Klatch Calliope — note PM now has three distinct public channels: weekly Ship newsletters (`pipermorgan.ai/shipping-news/`), longer narrative arcs on Medium (Building Piper Morgan series), and insight posts (`pipermorgan.ai/blog/`). If Klatch ever develops an analogous publication program, the three-track model separates operational cadence (Ship), narrative depth (building story), and standalone methodology insights — each with a different audience posture.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/02/2026-05-02-1555-lead-code-opus-log.md` — full read; #1018 Phase 2 + cluster, M2d audit-cascade, restructure decisions
- `piper-morgan-product/dev/2026/05/02/m2d-audit-cascade-findings.md` — full read; per-issue audit matrix, conceptual drift findings, recommendations
- PM commit `fd338c8` (#1018 Phase 2 feat), `fc79de3` (merge), `0b88e93` (audit findings), `d1c54dd` (restructure + m2-structure.md), `47998de` + `6b41ca5` (editorial calendar + publication) — message/stat reads
- `klatch` — 48h git log: 3 commits, all brief-delivery; no substantive session activity; Iris walkthrough resume still pending
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `weather`, `nyt-crossword` — 48h logs: brief delivery + automated status prints only; no narrated insights

**Not re-reported (covered in prior briefs):** Iris walkthrough Surfaces 1-2 (May 2); Ship #040 published (May 2); Phase F ENABLE_ETHICS_ENFORCEMENT=true live + alpha catch-22 (May 1); Iris session 6 composition gap (May 1); The Floor Comes Alive published (May 1); verify-before-assuming methodology + Pattern-064 (Apr 30); branch-discipline synthesis v1.0 (Apr 30).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
