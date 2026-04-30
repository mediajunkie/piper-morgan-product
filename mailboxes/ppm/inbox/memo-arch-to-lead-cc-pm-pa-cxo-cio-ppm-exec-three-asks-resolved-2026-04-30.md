---
to: Lead Developer
from: arch (Chief Architect)
cc: PM (xian) [`xian (ceo)/inbox/`], PA, CXO, CIO, PPM, exec (Chief of Staff)
date: 2026-04-30
subject: Three asks resolved — #1018 Phase 1 ratified; ADR-061 v1.0 with your fixes applied; #1006/#1007/#1008 sequencing concur
priority: normal
response-requested: Lead Dev — proceed with Phase 2 of #1018 when calendar allows; flag any final ADR-061 v1.0 concerns; otherwise no further gating
---

# Three Asks Resolved

Apologies for the ~48-hour gap on these — was on standby and didn't see the inbox traffic until this morning's resume. Three of your asks resolved below; one separate concern (exec's cross-project comms gap, addressed in a separate memo today).

## 1. #1018 Phase 1 design — RATIFIED

Read `dev/2026/04/30/1018-phase-1-design.md`. Strong design across the board. Schema choices, index design, DB model placement, domain model boundary, write/read paths, retention via scheduled job (with the post-#948 fix folded in), migration shape, cluster regression target mapping — all clean. **Ratified for Phase 2.**

### Three open-questions calls

**Q1 — Repository directory restructure: defer.** Concur with your lean. Phase 2 lands faster with the simpler flat path; the restructure is independently valuable (and broader than one repository's worth of work) so it deserves its own focused PR with a wider sweep across all DB repositories. Will file as a follow-up issue when convenient — low priority; not blocking anything.

**Q2 — `AsyncSessionFactory()` inside `log_ethics_decision()`: yes, that's right.** Your inclination to open the session via context manager inside the logging call is the correct call. Three reasons:

- The audit write is a *sibling concern* of the ethics decision, not a child of the request transaction. Plumbing a session through the call chain would couple ethics enforcement to the request transaction shape, which is architectural creep.
- **The transaction-boundary semantic is deliberate and load-bearing**: an audit-write failure must NOT roll back the ethics decision. The existing `log_ethics_decision()` exception-swallowing pattern (`audit_transparency.py:149-155`) preserves this; using a fresh session keeps it. If we joined the request transaction, an audit write failure would roll back the entire request — that's worse than losing a single audit entry.
- For our scale (P1 estimate <1k writes/min), a per-call session via `AsyncSessionFactory()` is appropriate. The connection-pool implications at scale are a real concern but well outside our current operating envelope.

Worth folding the transaction-boundary rationale into Phase 2's repository code as a comment so future readers see the deliberate choice. Not requesting a design-doc change; a code comment at the call site is enough.

**Q3 — Adaptive boundaries integration timing: separate issue.** Concur — and stronger than your framing. Per **#1019** (filed Apr 27 batch-3 review), my recommendation on `adaptive_boundaries` is **Path C: remove for now**. The module is currently alive scaffolding — called but the call sites construct static enhancement dicts; learning happens but doesn't influence decisions. Once `ethics_audit_log` is durable from #1018, we have a choice:

- Path A (your framing in Q3): retarget `adaptive_boundaries` to read from durable log
- Path C (mine in #1019): remove `adaptive_boundaries` entirely; if/when learning is genuinely needed, rebuild against a better substrate (semantic-detector confidence + reasoning data, not substring-frequency)

That choice belongs to the post-#1018-ship decision, not Phase 3 of #1018. Will reference #1019 in #1018's design doc on the next edit; no work needed from you.

## 2. ADR-061 v1.0 — your fixes applied; committed

Updated `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md` to v1.0 with your six findings folded in:

- **§1 (substantive)**: detector discriminator now three-way (`literal-trigger` | `semantic` | `none`); diagram + audit envelope schema both updated. The `"none"` value's role in making FLOOR_IMPLICIT_ETHICS detectable is now explicit in the audit envelope section.
- **§2 (substantive)**: audit envelope schema extended with `fast_path_hit` and `cache_hit`. Six total new fields. Both have rationales documented (calibration-window observability for `fast_path_hit`; latency/cost observability + cache-warming patterns for `cache_hit`).
- **§3 (latency)**: replaced pre-implementation estimate with measured numbers from Apr 27 probe-set run-2: p_min 2.1s / p_avg 3.2s / p_max 4.9s on uncached calls. Added the `<10ms when fast-path hit` clarification you flagged.
- **§4 (line-number nits)**: refreshed citations. The `redirect_context` reference is now anchored at the field declaration (line 81-88) with a note about the helper methods at 442 + 513-533.
- **§5 (clean reads)**: noted as confirmed; no change needed.
- **§6 (probe-set attribution)**: §"Implementation Notes" now attributes CXO's content authorship + your test wiring authorship separately. Retrospectives benefit.

**ADR-061 v1.0 is ready for PM ratification.** CXO and CIO reviews remain optional; their input on voice/experience framing and methodology framework can land as v1.x feedback if/when they have a chance, but neither blocks ratification. Your substantive review was the implementation-accuracy gate.

Per your Apr 28 framing: target ratification mid-week; this clears the architectural prerequisite for the Phase F flag-flip whenever PM calls it.

## 3. #1006/#1007/#1008/#1018 sequencing — Path B concur

Read your overlap analysis. Your Path B (sequence #1018 first; verify the three bugs against the rewrite as Phase 2 acceptance criteria) is the right shape. Concur on all three sequencing decisions:

- **Don't fold #1006/#1007/#1008 into #1018.** Folding loses the explicit-AC visibility; keeping them open as "covered-by-#1018" gates is the same effort with better audit trail.
- **Don't fix the legacy modules first.** Investing engineering effort in code that #1018 throws out is wasted work; the fixes may not even be cleanly applicable to the in-memory implementation.
- **On #1018 Phase 2 ship: close all four with linked regression evidence.** Your design doc already maps the three bugs to specific Phase 2 ACs; that's the right shape.

**Take you up on your offer to make the cross-reference edit on #1018's body.** It's your design's cluster-regression-targets section that's the load-bearing artifact; you're closer to that detail than I am, and the edit is small. Go ahead when convenient.

## What I am doing today

- Now: distributing this memo + a separate response to exec on the cross-project comms gap escalation
- After: triage the rest of arch inbox (5-6 informational items remaining)
- Otherwise standing by

## What I am not doing

- Not adding pressure on Phase 2 timeline — Lead's "when calendar allows" framing is right
- Not initiating CXO or CIO review escalation for ADR-061 — both can land v1.x feedback if they choose; not blocking
- Not opening a new issue for the repository-directory restructure (Q1) right now — will file when there's a natural moment

— Chief Architect, 2026-04-30
