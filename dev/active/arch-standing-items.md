# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.6 (reframed standing-items tracker per Architectural Decision 1).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-day or end-of-week.

**Last refreshed**: 2026-05-27 09:50 PDT (Day-1 of Architect v0.6 cycle adoption)

---

## Active

- [x] **worktree-as-cycle-default v0.7 concur/dissent** — DONE Day-2 Fire 1 (May 28 ~07:50). Strong concur (Mode 2 concurrent-rebase-churn is architectural, not discipline-fixable); 4 refinements (frequent-merge-to-main is load-bearing invariant; batch mailbox per-fire; **merge at per-fire-completion offset-staggered NOT batched-at-STOP** to avoid relocating clash to merge-boundary; worktree cleanup). Filed to CIO + Lead Dev + CEO + Docs + HOST. PM ratifies reversal.
- [x] **#1016 LLM-touch boundary boundary-map closing document** — DONE Day-2 Fire 3 (May 28). Filed `docs/internal/architecture/current/llm-touch-boundary-map.md` v0.1 (Phase 2 matrix 23 surfaces × 4-element + governing ADR/Pattern + Phase 4 alignment status) + commented #1016. Dominant gap: schema-validation + audit-envelope (P+F widely present via floor). Close criteria: fresh per-surface verification pass [P1 scores] + #1089 ship remain. #1117 named as llm_classifier Phase-4 instance.
- [x] **Pattern-070 Evolution-section entry** — DONE Day-2 Fire 1 (May 28). Filed `## Evolution: 2026-05-27 — External validation (Anthropic Dreams API)` + 4-invariant table + reframed-promotion-criterion note (external-validation evidence class; CIO methodology call on whether it satisfies Proven) + ADR-054 forward-state note. **methodology-34 8b unblocked.**
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
