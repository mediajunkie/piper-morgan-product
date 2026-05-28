# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.6 (reframed standing-items tracker per Architectural Decision 1).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-day or end-of-week.

**Last refreshed**: 2026-05-27 09:50 PDT (Day-1 of Architect v0.6 cycle adoption)

---

## Active

- [ ] **worktree-as-cycle-default v0.7 concur/dissent** (NEW May 28; HIGH — cohort converging now) — CIO cohort synthesis recommends reversing v0.6 decision 3 (no per-day cycle branch) toward worktree-as-cycle-default, per PM's worktree-as-rule instinct + Docs shared-main clash root-cause (29 commits/8hr to shared main; autostash conflict accumulation). CIO asks Architect cross-cutting-infra concur/dissent; PM ratifies. Connects to my discipline-reminder memo + the Fire-3 clash. Drive next fire.
- [ ] **#1016 LLM-touch boundary boundary-map closing document** (PM-approved triage routed to Arch lane May 28) — Phase 2 matrix (23 surfaces × 4-element score) + Phase 4 alignment status + which ADR/Pattern governs each. Closes the Architect side of #1016; epic closes when #1089 ships. ~30-60 min.
- [ ] **Pattern-070 Evolution-section entry** (CIO-disposed → me; remaining item for methodology-34 8b refresh) — date-stamped `### 2026-05-27: External validation — Anthropic Dreams API` entry + 4-row invariant-mapping table + sovereignty-stays-PM-side note. Pattern-064 Evolution template. ~15-20 min.
- [x] **GitHub Actions operational refactor sanity-check** — DONE Fire 1 (May 27 11:15 PDT). Filed sanity-check memo: concur paths-allow-list direction; one filter addition (`scripts/`); concurrency-group pattern OK; Docker `cancel-in-progress: false` refinement; Pattern-073-prevention via workflow-purpose comments. Lead Dev cleared to land Phase 1+2.
- [ ] **#973 MEM-CACHE-AUDIT Phase 1 audit** — PM-ratified ship-now-as-prep May 19. ~1-2 hr Architect drive + ~2-3 hr Lead Dev support. STABLE/DYNAMIC labeling + pipeline reorder + per-method TTL suggestions, no behavioral change. Needs Lead Dev coordination — focused session, not fire-driven.
- [x] **Dreams API spec read** — DONE Fire 2 (May 27 ~12:00 PDT). Filed findings memo: verdict Pattern-070 stays standalone; API validates the 4 invariants externally; Type 1 / Type 2 framing sharpened (Type 1 API-substratable when timing right; Type 2 stays PM-side). Three concrete proposals surfaced (Pattern-070 Evolution entry; ADR-054 forward-state note; methodology-corpus refinement).
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
