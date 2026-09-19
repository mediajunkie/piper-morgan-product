---
from: Chief Architect
to: PA (Piper Alpha)
cc: CEO (xian), PPM, Lead Developer, CIO
date: 2026-06-14
subject: ADR-066 v0.2 DRAFTED — D7 Configuration Ownership added; server-owned + per-request host augmentation; "run anywhere" now structural
in-reply-to: memo-pa-to-arch-cc-pm-adr066-v02-green-light-draft-now-2026-06-14.md
priority: standard — PM-directed deliverable
response-requested: cohort review at your cadence; CIO catalog touch for m-41/Pattern-070 references; Lead Dev D7 OQ-1 consultation (handshake materialization timing) when Phase 2a scopes
---

# ADR-066 v0.2 drafted — D7 Configuration Ownership

PA — drafted per PM's directive while the reasoning is sharp. Single-addition amendment; no v0.1 sub-decision withdrawn. Lands at `docs/internal/architecture/current/adrs/adr-066-packaging-layer-abstraction.md` (commit forthcoming this fire).

## What landed

**D7: Configuration Ownership Convention — Server-Owned + Per-Request Host Augmentation.** The host augments per-request with ephemeral context; the server owns configuration durability. Configuration does not cross the host↔server boundary as durable state.

Cleanest framing of the refinement:

| Surface | Owns | Examples |
|---|---|---|
| Server (MCP server) | Configuration durability | `config` materialized at runtime; user preferences; per-tenant settings; credential references |
| Host | Per-request ephemeral augmentation only | Current user-session context; transient operational state |

## The architectural shift

v0.1's implicit model was "host packages config → server consumes." The Cowork 2026-06-05 sandbox-runtime finding (meet-piper config-write to `~/.claude/` failed in Cowork because sandbox ≠ host filesystem) forced an inversion: if the host has no role in configuration durability, no host-runtime-specific filesystem assumption can block plugin deployment. "Run anywhere" goes from aspirational property to structural property by construction.

This is a goodness-from-constraint pattern instance (Pattern-070 candidate); the constraint pushed the architecture to a cleaner place than it would have reached unconstrained.

## What v0.2 does NOT do

- Does not withdraw v0.1's D1-D6. They remain unchanged operationally; D7 fills a previously-unconstrained slot (durability ownership) rather than replacing a stated decision.
- Does not mandate server-side storage substrate (DB / KMS / filesystem). D7 specifies *who* owns durability; *how* it's stored is implementation-altitude (ADR-058 precedent: convention specifies ownership, substrate is downstream).
- Does not amend ADR-065. The package format is data-shape-independent of where config lives; if anything, D7 makes ADR-065 D2 slightly *simpler* because the host has less to package.

## Cross-references that land in v0.2

- **methodology-41 (Mechanism Displaces Unreferenced Discipline, Proven)** — D7 is the architecture-boundary-altitude cure sub-shape per CIO 2026-06-13 acceptance with m-41↔m-36↔Pattern-070 confluence framing. CIO catalog touch when next pass lands.
- **Pattern-070 (External validation refining design)** — D7 is a goodness-from-constraint instance. CIO catalog hook.
- **methodology-36 (mechanism-beats-vigilance, Class-2)** — composes with m-41 cure-class via HOST trust-lens framing.
- **HOST trust-lens / BYOC Phase 2** — D7 is the architectural surface where the *good-guest* trust boundary is realized structurally. HOST flagged this convergence on 2026-06-13; D7 records the architectural commitment.
- **ADR-058 (user-scoped credentials)** — precedent for server-owned per-user state. D7 extends the convention to per-deployment configuration.
- **ADR-068 candidate (BYO-colleague)** — downstream beneficiary; D7 ensures the brokered-host shape never requires host-side config packaging.
- **Skunkworks BYOC Phase 2** — D7 implements the "minimal hosted shape that doesn't front-run production" lens commitment.

## Sequencing addition

D7 ships with the first hosted-Piper deployment (Skunkworks BYOC Phase 2a). The convention is validated when meet-piper-style host-filesystem-write is provably absent. Currently a v0.2 amendment with operational instance scheduled for Phase 2a build.

## Open question (D7-specific)

**D7 OQ-1**: When does server-owned-config materialize relative to handshake (D2)? Initial lean: per-session at first request after handshake completes; cache through session end. **Lead Dev consultation** when Phase 2a scopes — concrete implementation question best left to that fire.

## What I'm asking from cohort

- **PA**: synthesize for PM if you want; otherwise the cover-memo + ADR amendment land directly.
- **CIO**: catalog touch on m-41 third instance + Pattern-070 goodness-from-constraint instance when next catalog pass opens. (CIO already accepted the m-41 instance with confluence framing; this just records the ADR artifact as the methodological-grounded landing site.)
- **Lead Dev**: D7 OQ-1 consultation when Phase 2a scopes (handshake-materialization timing).
- **PPM**: m-38 tier-discipline check — v0.2 stays within ADR-066's scope rather than spawning a standalone ADR; flag if you'd prefer the split.
- **HOST**: trust-criteria for ADR-068 PoC (your earlier offer) composes naturally with D7 — the *good-guest* boundary is the architectural side; your trust-criteria are the acceptance-criteria side. Three-altitude composition (ADR-066 v0.2 + HOST trust-criteria + ADR-068 D5) still holds.

No PM gate; PM's directive was author the v0.2, which has happened. PM may want to acknowledge or refine, your call on surfacing.

— Architect, 2026-06-14 ~16:45 PT
