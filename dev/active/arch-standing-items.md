# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.6 (reframed standing-items tracker per Architectural Decision 1).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-day or end-of-week.

**Last refreshed**: 2026-05-27 09:50 PDT (Day-1 of Architect v0.6 cycle adoption)

---

## Active

- [x] **GitHub Actions operational refactor sanity-check** — DONE Fire 1 (May 27 11:15 PDT). Filed sanity-check memo: concur paths-allow-list direction; one filter addition (`scripts/`); concurrency-group pattern OK; one refinement candidate (Docker `cancel-in-progress: false`); Pattern-073-prevention via workflow-purpose comments. Lead Dev cleared to land Phase 1+2.
- [ ] **#973 MEM-CACHE-AUDIT Phase 1 audit** — PM-ratified ship-now-as-prep May 19. ~1-2 hr Architect drive + ~2-3 hr Lead Dev support. STABLE/DYNAMIC labeling + pipeline reorder + per-method TTL suggestions, no behavioral change. Worth driving in a focused session.
- [ ] **Dreams API spec read** — Anthropic Dreams API characterization per CIO May 18 platform-productization memo. Window closes Sun May 31. ~30 min read; decision point on whether Pattern-070 stays standalone or becomes Dreams API consumer.
- [ ] **v0.6 duty cycle Day-1 adoption** — substrate up; cron `:52` planned but not yet launched (awaiting PM go-autonomous). Mutual-assessment Day-1 memo to CIO after first 4-6 fires.

## Blocked / waiting on external

- [⏸] **Q6 ADR (canonical context-package format)** — Architect-lane; gated by PDR-005 v1.0 ratification (PPM lane; not yet); Klatch-pause framing means Q6 can proceed in-house with Daedalus-refinement-as-Evolution-section convention when Klatch resumes
- [⏸] **Q7 ADR (packaging-layer abstraction implementation)** — Architect-lane; gated by PDR-005 v1.0 ratification + Lead Dev MCP server packaging build start

## Watch surfaces (not work; observation only)

- **Pattern-073 spec-layer corollary** — my May 17 #1089 Q3 thinko was Pattern-073-adjacent at the spec layer (caught by Lead Dev May 23). File as a Pattern-073 instance if a second spec-layer case surfaces.
- **External-alignment-Evolution-amendment pattern** — HOST May 24 generalization of my Klatch-pause framing as candidate general operating norm. File as methodology corpus entry if second external-dependency-uncertainty case surfaces.

## Mutual-assessment exchange commitments (per CIO May 27 welcome)

- [ ] Day-1 "what surprised me" memo to CIO + HOST after first 4-6 fires
- [ ] Day-3/4 comparative observations (cross-role)
- [ ] Day-7 synthesis to PM
