# Codebase Review Batch 2 — Findings (Track 1, Apr 27)

**Author**: Chief Architect
**Date**: 2026-04-27
**Session**: 2026-04-27-0815-arch-opus-log.md
**Surfaces reviewed**: LLM/provider abstraction (`services/llm/`), web layer (`web/`), domain models + canonical types (`services/domain/`, `services/shared_types.py`, `services/intent_service/intent_types.py`)
**Method**: 3 Explore subagents in parallel, Architect synthesis

---

## Findings table

| ID | Finding | Surface | Severity | Effort | Status / Tracking |
|---|---|---|---|---|---|
| **A** | `/auth` and `/setup` route prefixes violate CLAUDE.md `/api/v1/` convention | Web | Real (per stated rule) | ~1 hr (rename + frontend update) | **Issue filed**: see below |
| **B** | Phantom import `get_selected_client` in `services/intent/intent_service.py:8032` — function does not exist in `services.llm.clients` | LLM × Intent | Latent (would crash if called) | ~10 min | **Folded into dead-code sweep** |
| **C** | `APIUsageTracker` instantiated in `services/llm/clients.py:36` but never called (dead instantiation) | LLM | Cosmetic | ~10 min | **Folded into dead-code sweep** |
| **D** | `LLMProvider.PERPLEXITY` is enum-only stub — no client init, no `_perplexity_complete()`, not in `PROVIDER_MODELS` | LLM | Cosmetic | ~10 min | **Folded into dead-code sweep** |
| **E** | `AuthMiddleware.exclude_paths` has grown to 34 entries unstructured (mixed categories — static, auth, oauth, setup, scaffold) | Web | Maintenance | ~1 hr (group by category) | **Issue filed**: see below |
| **F** | `LLMModel.CLAUDE_OPUS` aliased to `claude-sonnet-4-20250514` (semantic inversion: enum name says Opus, value is Sonnet) | LLM | Cosmetic | trivial (rename when Opus 4 ships) | **Folded into dead-code sweep** |
| **G** | `ActionDisposition.HANDLER` defined in enum but no entry in `ACTION_REGISTRY` uses it | Types | Cosmetic | trivial (delete from enum) | **Folded into dead-code sweep** |
| **H** | ADR-051 RequestContext migration is in mid-Phase-2/3 partial adoption — `intent.py` constructs properly; other routes use legacy `request.state.user_id`; migration has stalled | Web × Types | Architectural drift | TBD (sprint-scope per PM) | **Issue/epic filed**: see below |

---

## Cross-cutting architectural insights (not findings, observations)

### Insight 1: "Loose at the LLM-touch boundary, tight at the deterministic core" — but inconsistent across layers

Each surface independently demonstrated a "boundary-flexibility / core-determinism" pattern:
- **Intent classification**: `Intent.action` is free-form `str` at the LLM boundary; 34-pair `ACTION_REGISTRY` is deterministic at dispatch; unregistered actions safe-fallback to FLOOR
- **LLM layer**: provider selection is loose (per-call, user-keychain-driven); tier-to-model mapping is deterministic
- **Web layer**: Pattern-007 graceful 200-OK degradation at intent surface; Pattern-034 standard HTTP error codes elsewhere

This is the **inverse** of yesterday's #1002 finding — the BoundaryEnforcer's substring detector was *too rigid* at the LLM-touch boundary, with no semantic safe-fallback. Fix B (#1004) is moving BoundaryEnforcer toward the same loose-boundary-tight-core shape that intent classification already uses.

The architecture has **two opinions** about how to handle LLM-touch surfaces, and the choice between them appears incidental rather than principled. PM has flagged this as worth a thorough architectural review with a developed point of view, then gradual alignment. **Tracked as separate epic** (see issues filed below).

### Insight 2: Several small dead-code pockets are scaffolding from earlier exploration that didn't get closed-out

The pattern: `APIUsageTracker` instantiated for a future instrumentation refactor that hadn't shipped; Perplexity probed as a candidate provider but abandoned; `ActionDisposition.HANDLER` enumerated for a dispatch pattern that wasn't used; phantom import from a renamed/deleted function. None are user-affecting; all are small effort; all are the kind of hygiene that pays compound interest. **Tracked as a single dead-code-sweep issue.**

### Insight 3: The predecessor's "ConversationTurn missing response field" claim is outdated

Predecessor's Apr 25 handoff Section 1 listed `ConversationTurn missing response field — floor reads history but only sees user messages, never Piper's replies` as a #922 manifestation, with a note that the fix was committed Apr 9. The subagent verified: the field exists at `services/domain/models.py:1661` as `assistant_response`. The Apr 9 fix landed; the predecessor's handoff carried both the bug-framing and the fix-note, and I had been remembering the bug-framing without re-verifying. **No action needed** beyond noting that the issue is fully resolved.

### Insight 4: Local-model readiness — Apr 23 framing was prescriptive, not descriptive (forensic verdict)

**Initial concern**: my synthesis suggested the Apr 23 Lead Dev session log overstated readiness ("foundation exists; delta is LOCAL enum + local client init + per-task local-preference routing"). PM asked for a forensic investigation to determine whether work was stranded or whether the framing was aspirational.

**Subagent forensic verdict (Apr 27 ~13:25)**: **Work was never stranded. The Apr 23 framing was clearly prescriptive ("the delta is X" = future work to add), not descriptive (a status claim that the work was done).** Verbatim from the Apr 23 session log:

> *"Verified `LLMProvider` enum + `PROVIDER_MODELS` tier mapping + fallback order all exist. **Adding** `LOCAL` enum + local client init + per-task local-preference routing **is the delta.**"*

The verb "adding" + "is the delta" identifies future work. No code commits implement LOCAL anywhere in git history (any branch, any time). No stashes contain local-model work. No worktree has stranded code. No TODO/FIXME comments in services/llm/ point to in-progress local-model work. The Apr 23 `local-model-research-prompt-draft.md` is explicitly a specification *for future research*, not implementation documentation.

**My characterization in the synthesis was unfair to the Apr 23 framing.** The framing was honest about what was done and what remained. My re-tell carried freight the original didn't claim. Correcting on the record.

**Net status of local-model readiness**:
- Tier-system foundation exists (correct)
- Adding LOCAL is ~6 concrete changes (enum, mapping, client init, completion method, fallback positioning, optional task overrides)
- Not stranded, not done, not started as code — pending research-prompt completion + design + sign-off + implementation
- Not currently scoped into any sprint; will surface naturally if/when local-model viability research lands and PM/Lead Dev decide to schedule.

No issue needs to be filed against this — it's intentionally pending decision; future work will pick it up when the decision is made.

---

## Forward-looking items — issues filed

| Issue | Title | Covers | Priority |
|---|---|---|---|
| **[#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012)** | ARCH-CLEANUP: Small dead-code sweep | B, C, D, F, G | P3 |
| **[#1013](https://github.com/mediajunkie/piper-morgan-product/issues/1013)** | ARCH-CLEANUP: /auth and /setup route prefixes violate /api/v1/ convention | A | P2 |
| **[#1014](https://github.com/mediajunkie/piper-morgan-product/issues/1014)** | ARCH-CLEANUP: AuthMiddleware exclude_paths refactor — group 34 entries by category | E | P3 |
| **[#1015](https://github.com/mediajunkie/piper-morgan-product/issues/1015)** | ARCH: Complete ADR-051 RequestContext migration — finish Phase 2/3 partial adoption (epic) | H | P2 |
| **[#1016](https://github.com/mediajunkie/piper-morgan-product/issues/1016)** | ARCH-DESIGN: LLM-touch boundary principle — establish unified architectural posture (epic) | Cross-cutting Insight 1 | P1 |

---

## Subsequent batch surfaces (not yet reviewed)

Per Architect's plan documented in session log:
- Ethics infrastructure full surface (`services/ethics/` beyond just BoundaryEnforcer)
- Database/repositories layer + the PII placeholder threads
- Memory layer (`services/memory/` — PDR-002 territory)
- Test infrastructure shape (coverage map, gaps, structure)
- `services/orchestration/` and `services/process/`
- Plugin system (`services/plugins/`)
- `services/learning/`

PM has signaled "no rush; period of catching up; further review warranted" — pace will be steady across multiple sessions.

---

*Last Updated: 2026-04-27 (initial creation)*
*Subagent reports archived to git history; this document is the synthesis layer.*
