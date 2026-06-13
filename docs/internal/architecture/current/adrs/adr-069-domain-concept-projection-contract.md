# ADR-069: Domain Concept Projection Contract — System of Record vs. In-Process Working State

**Status**: v0.1 (filed 2026-06-12) — Lead-Dev-authored from the #1207 implementation; **Architect ratification of the carve received** (memo 2026-06-12 ~19:35 "strong concur"); Architect to review-ratify this ADR artifact.

**Date**: 2026-06-12

**Authors**: Lead Developer (implementation context from #1207)

**Reviewers**: Chief Architect (ratify — carve already concurred), CIO (methodology), CEO (xian)

---

## Status

- **v0.1** filed 2026-06-12, born from #1207 (conversation-context unification).
- The *carve* it documents is **ratified** (Architect memo 2026-06-12, "Q1 — Strong concur"); this ADR makes the pattern reusable so the next instance isn't re-litigated from scratch.
- Cross-references: **ADR-029** (parent — domain-service mediation, the *what*); **ADR-005** (eliminate dual implementations — the anti-pattern this resolves); **methodology-30** (Consumer-Trace Verification — what surfaced the dead code); **methodology-41** (mechanism-displaces-vigilance — the guard pattern).
- Companion altitude per **methodology-38** (PDR/ADR Tier Separation): ADR-029 is the mediation *pattern*; this is the *how, when the domain concept also carries a projection responsibility*. Standalone, not an ADR-029 amendment (Architect Q2).

---

## Context

A single domain concept can carry **two responsibilities with different lifecycles**: a durable **system of record**, and a transient **in-process working state** used to shape behavior. When those two are allowed to drift into two parallel implementations, the result is the #1207 failure mode:

- Two classes named `ConversationContext` (one in `services/intent_service/conversation_context.py`, one in `services/conversation/conversation_manager.py`) with different field names (`message`/`response` vs `user_message`/`assistant_response`).
- Turns persisted to the DB through one path (`ConversationManager`, #563) **never flowed back** into the other (the in-memory registry the floor read), so antecedent resolution saw empty history (#1122) and persistence felt "hinky."
- Two reference-resolution mechanisms; a one-way data flow; and a dead hydration block (#953) hidden behind a shadowed import + `except: pass`.

This is **ADR-005's dual-implementation anti-pattern, one altitude up**: not two repositories for one entity, but two *aggregates* for one concept — one masquerading as the durable record, the other as the working state, neither owning the boundary.

The concept generalizes. The next instance is almost certainly **`Intent`** (intent_service holds working state on top of the domain `Intent` aggregate — same shape, same trap waiting), and after that possibly **`Artifact`** (#952). Without an ADR-shaped artifact, each future application re-litigates the carve, and the projection-contract pattern stays implicit until the next trap surfaces.

---

## Decision

When a domain concept has **both** a durable record responsibility **and** a transient working-state responsibility, split it into **three layers** with explicit contracts between them.

### D1 — When does a domain concept need a projection?

Introduce a projection (a distinct working-state type) **only** when the working state has at least one of: a **different lifecycle** (in-process/per-session transient vs. durable), **different update semantics** (fields mutated by discourse/UX flow, not by domain events), or **different invariants** (the working state can be *reconstructed from* the domain state, but not vice-versa). If the working state has none of these — if it is just the domain entity in memory — do **not** create a projection; use the domain entity. (This guard prevents projection-proliferation: not every in-memory use of a domain object is a projection.)

The reconstructability test is the sharpest: **working state is derivable from the system of record; the system of record is not derivable from working state.** That asymmetry is what makes one durable and one disposable.

### D2 — The three-layer carve (worked example: `Conversation`)

| Layer | `Conversation` instance | Role | Lifecycle |
|---|---|---|---|
| **Domain** | `Conversation` + `ConversationTurn` (`services/domain/models.py`) | System of record | Durable (DB) |
| **Application (mediation)** | `ConversationManager` (ADR-029) | The single access path to persisted turns (`get_recent_turns`, `save_conversation_turn`) | Per-request |
| **In-process working state (projection)** | `intent_service.ConversationContext` | Recent-turn window + lens stack + last offer + floor flags + provenance sidecar | Per-session, in-process |

The projection stays **out of** the mediation layer (folding it in re-creates the deleted anemic aggregate one altitude up) and its discourse-time fields stay **out of** the domain entity (mixing transient fields into the durable aggregate violates DDD invariant-protection — Architect Q1, both alternatives rejected).

### D3 — Single mapping point invariant (one hydrate, one persist)

There is **exactly one** place that maps domain records → working state (the anti-corruption-layer seam) and **exactly one** outbound persist seam. For `Conversation`: `hydrate_turns_from_db()` (in) at the `process_intent` boundary, and `save_conversation_turn` (out) at the same boundary. New consumers extend the single mapping point; they do **not** add their own domain→projection mapping. The projection itself performs **no I/O**.

### D4 — Single prompt-shaped reader invariant

There is **exactly one** place that reads working state into outputs (prompts, responses). For `Conversation`: `build_recent_history()`. The 7 hand-copied history-builder blocks that #1207 collapsed — two carrying a silent `[:-1]` bug — are the canonical evidence for why this invariant is load-bearing: copies drift, and a drifted copy is a behavior bug.

### D5 — Guard pattern (mechanism over vigilance)

Pin D2–D4 with a guard test (m-41), so the dual implementation cannot silently regrow: assert no second aggregate reappears in the mediation module, no inline working-state iteration in the consumer, no consumer bypassing the single mapping point. For `Conversation`: `tests/unit/services/conversation/test_context_unification_guard.py`.

### D6 — Evolution (what we are hedging against)

The next domain concept with mixed responsibility applies D1–D5 without re-deriving them. **`Intent`** is the named next candidate (working state layered on the domain `Intent`); **`Artifact`** (#952) is a possible third. When that work lands, the carve is a lookup, not a debate — which is the entire point of recording it.

---

## Consequences

**Positive**
- One source of truth per concept; the projection is provably reconstructable from it (D1), so a process restart / cache prune is recoverable, not lossy.
- The mediation layer keeps the narrow ADR-029 contract (persistence access only).
- Future mixed-responsibility concepts (`Intent`, `Artifact`) inherit a vetted carve + guard shape.

**Negative / cost**
- A projection is a real type to maintain; D1's gate is what keeps it from being introduced gratuitously.
- The single-mapping-point and single-reader invariants are discipline the guard test must enforce, or they erode (the #1207 history exactly shows the erosion when they aren't enforced).

**Neutral**
- This ADR documents a carve already shipped + ratified; it changes no running code. Its value is preventing the next re-litigation.

---

*v0.1 — Lead Dev, 2026-06-12, from the #1207 implementation. Architect carve-ratified; ADR-artifact review pending.*
