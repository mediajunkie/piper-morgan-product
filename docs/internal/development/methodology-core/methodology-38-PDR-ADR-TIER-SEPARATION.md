# Methodology-38: PDR/ADR Tier Separation — Decision-Rule Altitude vs Architectural-Implementation Altitude

**Status**: v0.1 — **Emerging** (Architect-authored; CIO catalog confirmed 2026-06-03)
**Date**: 2026-06-03 (cohort discipline matured Apr 27 → May 20, 2026)
**Origin instance**: BYOC (Bring Your Own Chat) routing from anticipated single-ADR (Apr 27 360-tracker commitment) → PDR-005 + companion ADRs (Q6/Q7) shape (HOST 360-tracker item 1.3 close, May 20)
**Related**: methodology-29 (Pattern Formation via Successful Imitation), Pattern-072 (Registries that Grow into Architectural Shapes; Proven), Pattern-064 (Alive Scaffolding — Evolution-section convention)

---

## Overview

**Architectural decisions sit at two altitudes**: the **decision-rule** altitude (what the product commits to as direction or invariant) and the **architectural-implementation** altitude (how the architecture concretely realizes that commitment). The cohort's PDR/ADR vehicle separation reflects this altitude split — **PDRs carry decision-rule commitments; ADRs carry architectural-implementation commitments**. When new architectural work surfaces, the pre-drafting altitude check is: "Is this a decision-rule shape, or an implementation shape?" Routing to the right tier prevents premature ADR commitment to implementation that hasn't yet earned its altitude, and prevents PDR sprawl into implementation specifics that should live in companion ADRs.

## Why this methodology

Between Apr 27 and May 20, 2026, the cohort discipline matured through one concrete BYOC routing decision: an Apr 27 360-tracker commitment (item 1.3) anticipated a single ADR for BYOC; by May 19-20 the actual vehicle was PDR-005 with Q6 + Q7 as companion implementation ADRs. The altitude split happened cohort-wide without being named as methodology — it emerged from PPM, CXO, Architect, and HOST converging on the routing pattern across several memos. HOST's May 24 item 1.3 close memo explicitly cited it as worth memorializing.

The methodology entry codifies what the cohort already does, makes the pre-drafting check visible to new agents and future architectural work, and prevents the re-discovery cost when the next "what tier is this?" question surfaces.

## The discipline

### The altitude check (pre-drafting)

When new architectural work surfaces, the pre-drafting question is:

**Q1**: Does this work commit to **direction** or **invariants** (what the product or platform promises)? → **PDR shape**

**Q2**: Does this work commit to **specific architectural shapes** (how invariants are concretely realized in code, infrastructure, or interfaces)? → **ADR shape**

**Q3**: Does this work require *both* — a decision-rule commitment AND specific architectural implementations to realize it? → **PDR + companion ADRs shape** (the BYOC case)

### What goes in a PDR

PDRs carry commitments at the **decision-rule altitude**:
- Product direction (e.g., BYOC distribution, persona portability hierarchy)
- Invariant commitments (e.g., ≤5% tone variance, zero-tolerance capability claim consistency)
- Decision-rule frameworks (e.g., variance hierarchies, principle obligations)
- Consequences for architecture / product / experience at the shape level (not implementation specifics)

A PDR can name companion-ADR slots in §Open questions without itself committing to the implementation shape — that's the deliberate separation.

### What goes in an ADR

ADRs carry commitments at the **architectural-implementation altitude**:
- Specific architectural primitives (e.g., audit envelope structure, four-element principle, registry typing)
- Implementation patterns (e.g., Pattern-070's four operational invariants, ADR-061's two-layer detector)
- Code-shape commitments (e.g., persona core API; surface 7 read endpoint contracts; index registry dataclass)
- Architectural sequencing (Phase 0 scoping → Phase 1+ trigger gating)

An ADR can reference a PDR as parent commitment but doesn't re-litigate the decision-rule altitude — the PDR settled that; the ADR commits to how.

### What goes in companion-ADRs gated by a PDR

When a PDR commits to direction + invariants but the implementation shape isn't yet settled, companion ADRs sit downstream gated by PDR-ratification:
- Q6/Q7 pattern: PDR-005 names "canonical context-package format ADR" + "packaging-layer abstraction ADR" as companions; both gated by PDR-005 v1.0 ratification
- Companion ADRs file at PDR-ratification time, not at PDR-drafting time
- Naming companion-ADR slots in the PDR's §Open questions is the discipline marker

## Recognition trigger

This methodology should be invoked **before drafting begins** on new architectural work. Concrete triggers:

- **A role surfaces "we need an ADR for X"** — pre-drafting check: is X decision-rule shape or implementation shape? If decision-rule, route to PDR instead.
- **A PDR is mid-draft with implementation specifics creeping in** — pre-drafting check: does the implementation specific belong in a companion ADR? If yes, name the companion-ADR slot in §Open questions and remove the implementation specific from the PDR.
- **A new architectural backlog item arrives without altitude** — the question "PDR or ADR?" is the routing decision.

## What this catches (failure modes prevented)

- **ADR-as-decision-rule-vehicle drift**: when a decision-rule commitment lives in an ADR, future ADRs at the same altitude can't extend or supersede it without confusion. The Apr 27 BYOC commitment-as-single-ADR would have produced this drift.
- **PDR sprawl into implementation specifics**: PDRs that try to commit to both decision-rule AND implementation shape become harder to ratify and harder to revise. The companion-ADR shape keeps PDRs focused on direction.
- **Premature implementation commitment**: ADRs filed before decision-rule settled commit the architecture to implementations that may not survive the decision-rule ratification.

## Reference instances

### Origin instance: BYOC routing (Apr 27 → May 20, 2026)

- **Apr 27**: 360-tracker item 1.3 commitment anticipated "ADR for BYOC distribution architecture" (single-ADR shape)
- **Apr-May**: PPM opened PDR-005 discovery thread (May 4); cohort review of v0.1-v0.5 surfaced decision-rule commitments (persona portability, MCP server scope, bespoke UI commitment depth) AND implementation shape questions (canonical context-package format; packaging-layer abstraction)
- **May 20**: HOST 360-tracker item 1.3 close memo + Architect concur memo named the routing: "PDR for decision-rule altitude; ADR for architectural-implementation altitude." BYOC routed to PDR-005 + Q6 + Q7 companion ADRs.
- **Subsequent (May 27, June 3)**: cohort traffic uses the PDR/companion-ADR shape as cohort-canonical (e.g., PPM EC-2 qualifier landing in PDR-005 §Consequences-for-experience with Q7 packaging-layer ADR carrying the per-host capability-claim map).

### Second instance (in flight): the duty cycle cron-shape framework

- The work-shape registry + per-lane experimentation framework (`docs/operations/duty-cycle design/cron-shape-experiments.md`, June 2) commits to a decision-rule altitude (lanes tune cadence to match work-shape; standard hourly is default not mandate). The per-lane implementations (Arch 3hr; HOST 3hr; CIO `7 2,4-23 * * *`; Web 2×/day) are companion shapes that sit downstream of the framework.
- The framework lives in operations docs rather than as a PDR because it's methodology-corpus material rather than product commitment, but the altitude split is the same shape: framework (decision-rule altitude) + per-lane configurations (implementation altitude).

## Promotion-to-Proven criterion

This methodology promotes from v0.1 draft to Proven when:

1. **A third architectural-work instance** is routed via the altitude check pre-drafting (not retroactively recognized)
2. The cohort references methodology-38 by name in routing decisions (e.g., "per methodology-38, this is decision-rule altitude → PDR")
3. At least one near-miss is caught — an ADR that would have committed prematurely is re-routed to PDR or PDR+companion-ADR shape via the altitude check

## Cross-references

- **PDR-005 (BYOC)**: the origin instance + canonical example of PDR + companion-ADRs shape. `dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md` (or current; v1.0 in flight)
- **HOST 360-tracker item 1.3 close**: `mailboxes/arch/read/memo-host-to-ppm-arch-cc-ceo-cohort-360-item-1.3-close-confirmed-2026-05-24.md`
- **Architect concur memo** (May 20): `mailboxes/arch/sent/memo-arch-to-ppm-cc-host-ceo-cohort-360-item-1.3-architect-concur-plus-klatch-pause-note-2026-05-20.md` (names the altitude framing)
- **PPM 360-tracker item 1.3 clarification**: `mailboxes/arch/read/memo-ppm-to-host-cc-arch-ceo-cohort-360-item-1.3-byoc-vehicle-clarification-2026-05-20.md`
- **Pattern-072 (Registries that Grow into Architectural Shapes; Proven)** — sibling methodology-29 framework instance at the typed-catalog layer; methodology-38 is the same framework operating at the decision-vehicle-tier layer
- **methodology-29 (Pattern Formation via Successful Imitation)** — the umbrella framework; methodology-38 is a successful-imitation instance at the tier-vehicle altitude
- **methodology-34 (Cohort-Discipline as Moat)** — methodology-38 is an instance of the moat thesis operating: the cohort matured the discipline of routing foundational decisions to PDR tier and implementation-specifics to ADR tier between Apr 27 and May 20 without external authority dictating it; the discipline is cohort-distinctive moat material (CIO catalog-confirmation note 2026-06-03)
- **ADR catalog at `docs/internal/architecture/adrs/`**: the implementation-altitude commitments
- **PDR catalog at `docs/internal/pdrs/` (or current location)**: the decision-rule-altitude commitments

## What this methodology is NOT

- **Not a process gate**: PDR/ADR routing isn't a formal approval step; it's a pre-drafting altitude check the agent performing the work should run
- **Not catalog-management**: slot allocation for the resulting PDR or ADR remains CIO catalog-management lane
- **Not a re-litigation trigger**: existing ADRs that committed to decision-rule altitude don't need retroactive demotion to PDR — historical accident; the altitude check applies to *new* work
- **Not exhaustive of tier separation**: other architectural-decision vehicles (e.g., methodology-corpus entries, pattern catalog entries, skill files) carry their own altitudes; this methodology specifically names the PDR ↔ ADR pair

## Open items

- **PDR catalog location** — needs canonical home if not already established (Docs cadence)
- **PDR template** — if not formalized, would benefit from a parallel to the ADR template
- **Companion-ADR-slot reservation convention** — naming companion-ADR slots in PDR §Open questions is the current cohort discipline; could formalize as a PDR template field
- **CIO catalog confirmation** — ✅ confirmed 2026-06-03 (slot 38; Architect-authored shape held; methodology-34 cross-ref added per CIO note)

— Chief Architect, 2026-06-03 v0.1 (Architect-authored draft; pending CIO catalog confirmation)
