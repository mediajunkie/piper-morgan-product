# ADR-066: Packaging-Layer Abstraction (BYOC Plugin Per-Host Deployment)

**Status**: v0.2 (amended 2026-06-14) — Architect-authored; companion to PDR-005 v1.0 §Open question 7; gated by ADR-065 v0.1 ✅.

- **v0.1** (2026-06-08): three-fire bursty-lane arc — Fire 3 (2026-06-06 PM) skeleton + plugin-packaging framing; Fire 6 (2026-06-07 AM) §Decision D1-D6 content; Fire 8 (2026-06-08 AM) polish + §Consequences refinement + v0.1 final. Same shape as ADR-065 three-fire arc validated earlier.
- **v0.2** (2026-06-14): added **D7: Configuration Ownership Convention** (server-owned + per-request host augmentation), grounded in the Cowork (2026-06-05) sandbox-runtime finding that meet-piper's host-filesystem config-write broke in non-Code runtimes. The constraint forced a cleaner shape than v0.1 imagined — the host doesn't package config; the server owns it and the host augments per-request. "Run anywhere" becomes a natural property rather than an aspirational claim. Companion cross-references: HOST trust-lens (2026-06-13, *"good-guest"* boundary realized structurally); methodology-41 architecture-boundary cure sub-shape (CIO 2026-06-13 acceptance with m-41↔m-36↔Pattern-070 confluence framing). Single load-bearing addition; no v0.1 sub-decision withdrawn.

**Date**: 2026-06-06

**Authors**: Chief Architect (Arch)

**Reviewers**: PPM (PDR-005 owner), Lead Dev (implementation lane), CIO (methodology), CEO (xian)

---

## Status

- **v0.1** filed 2026-06-08 (three-fire bursty-lane arc: 2026-06-06 skeleton + 2026-06-07 Decision content + 2026-06-08 polish + final)
- Gated by: ADR-065 v0.1 ✅ (canonical context-package format establishes the capability primitive D3 that this ADR organizes per-host)
- Gates: BYOC implementation rollout (plugin deployment to multiple host surfaces — Claude Desktop, ChatGPT, Slack, bespoke UI)
- Implementation-altitude ADR companion to PDR-005's decision-rule altitude per methodology-38 (PDR/ADR Tier Separation)

## Context

### What problem does this ADR solve?

PDR-005 v1.0 (Bring Your Own Chat, ratified 2026-06-05) commits Piper Morgan to plugin-based distribution (`config + CLAUDE.md + skills + MCP server` per PM's 2026-06-01 clarification). ADR-065 (just filed) specifies the **wire format** for what flows between the plugin's MCP server and connected hosts. This ADR specifies the **packaging-layer abstraction** that lets the same plugin deploy to multiple host surfaces with different capability profiles.

PDR-005 §Open question 7 routes the per-host capability map + deployment-layer concerns to this ADR.

The concrete need: the same Piper Morgan plugin, when deployed to Claude Desktop vs. ChatGPT vs. Slack vs. a bespoke UI vs. a sibling-project receiver (Klatch), must:

- **Detect its host surface** at handshake time (PDR-005 AC-1 surface-presence detection)
- **Claim the right capabilities** for that surface (ADR-065 D3 verb-enum + `surface_type` slot; EC-2 conditional-claim-per-host)
- **Implement the wire format** correctly against the per-host capability profile (no claiming capabilities the host can't fulfill; no withholding capabilities the host can)
- **Surface degradation gracefully** when the host lacks a claimed capability (ADR-065 D4 error envelope `CAPABILITY_UNAVAILABLE`)
- **Not require per-host bespoke code** — the abstraction layer is the place that handles per-host variance, not scattered through skills and MCP-server methods

### Why "packaging-layer abstraction"?

The "packaging layer" is the boundary between the plugin's components and the host. It is:

- **Above** the plugin's `config + CLAUDE.md + skills + MCP server` (those are the same artifacts regardless of host)
- **Below** the host's MCP client (the host is what it is; we don't control its shape)
- **The translation surface** where per-host variance is concentrated

Abstraction = the same plugin code path emits the right context packages and claims the right capabilities for whichever host it's deployed to, via configuration + handshake + capability map. Not via #ifdef-style branching in the MCP server methods.

### Format-decision space (inherits from ADR-065)

ADR-065 (companion ADR) settled:
- Wire format (D1: JSON + schema_version)
- Package structure (D2: envelope + body + extensions)
- Capability primitive (D3: verb-enum + `surface_type` slot, claim, conditions)
- Error envelope (D4: ADR-063 READ-side four-element principle)
- Versioning + Postel forward compat (D5)
- Plugin packaging declaration sites (D6: `config` declares versions, schema spec file is source-of-truth)

This ADR organizes those primitives into a deployment-time abstraction. Sub-decisions:

- **D1: Per-host capability map shape** — how the plugin's `config` declares the capability profile per host
- **D2: Surface-detection handshake** — what protocol the plugin runs at startup to identify its host (PDR-005 AC-1 mechanism)
- **D3: Capability-claim composition** — how the per-host map + the runtime host identity produce the capability claims the plugin emits
- **D4: Degradation policy** — when a claimed capability is unavailable at runtime (host limitation, transient failure), how the plugin surfaces it
- **D5: SDK helper layer** — the receiver-side complexity acknowledged in ADR-065 §Consequences/Negative (capability conditional-not-boolean) mitigated via SDK helpers; this ADR specifies the helper shape
- **D6: Sibling-project receiver shape** — Klatch and future systems consume capability claims; how they integrate at the packaging layer

### Klatch alignment context

Same context as ADR-065: Klatch paused 2026-05-20; in-house drafting proceeds per Pattern-064 Evolution-section convention HOST lifted 2026-05-24. Klatch refinements fold to §Evolution when alignment resumes.

### Prior art / cross-references

- PDR-005 v1.0 §Mechanism set #5 (context-package format) + §AC-1 (surface-presence detection) + §Open question 7 (routes to this ADR)
- **ADR-065** (Canonical Context-Package Format) — JUST FILED — establishes the primitives this ADR organizes
- ADR-061 (LLM-touch boundary four-element principle) — applies at every host-boundary surface
- ADR-063 (User-Facing Audit Envelope Read-Surface) — error envelope composability cross-host
- EC-2 conditional-claim-per-host ruling (2026-06-03 PPM synthesis) — the format-layer commitment this ADR operationalizes
- Pattern-072 (Registries that Grow into Architectural Shapes, 7+ applications) — the per-host capability map is likely the 8th application
- Pattern-073 (Documentation-Asserted-Behavior Drift) — doc-sync-sweep discipline at the packaging layer
- methodology-32 (Postel for Memo Headers) — Postel discipline applies cross-host at handshake time
- methodology-38 (PDR/ADR Tier Separation, Emerging) — this ADR is the implementation-altitude companion to PDR-005's decision-rule altitude
- **methodology-40 (Layer-Then-Migrate, Emerging, CIO-confirmed 2026-06-09)** — D1 per-host capability map is m-40 instance #4 in the catalog; the registry-as-source-of-truth + per-host-as-orthogonal-dimension shape inherits the same architectural primitive as ADR-065 D3
- **methodology-41 (Mechanism Displaces Unreferenced Discipline, Proven 2026-06-12)** — D7 (v0.2) is the architecture-boundary-altitude cure sub-shape (CIO 2026-06-13 acceptance with m-41↔m-36↔Pattern-070 confluence framing). v0.2 references the m-41 catalog entry as the methodological grounding for the configuration-ownership convention.
- **Pattern-070 (External validation refining design)** — D7 (v0.2) is a goodness-from-constraint instance: the Cowork 2026-06-05 sandbox-runtime constraint refined the design from "host packages config" (aspirational portability) to "server owns config" (structural portability).
- **HOST trust-lens / BYOC Phase 2 (2026-06-13)** — D7 (v0.2) is the architectural surface where the *good-guest* trust boundary is realized structurally. HOST identified two of five trust boundaries already surfacing as Phase-2 architecture; D7 records the architectural commitment for the good-guest boundary.
- **Skunkworks BYOC Phase 2 lens (2026-06-13)** — D7 (v0.2) implements the "minimal hosted shape that doesn't front-run production" lens commitment by making host-runtime-agnostic deployment structural.

---

## Decision

The packaging-layer abstraction is **a `config`-declared per-host capability map + a `surface.detect` handshake + pure-function claim composition + three-tier degradation + SDK helpers + same-shape sibling integration**. Sub-decisions D1-D6 inherit ADR-065 primitives (envelope+body+extensions; verb-enum+`surface_type` slot; error envelope; SemVer + Postel; spec-file source-of-truth) and organize them into a deployment-time abstraction the plugin runs at startup + per-request.

### D1: Per-host capability map shape

**Decision**: The plugin's `config` declares the per-host capability profile as a YAML map keyed on ADR-065 D3 `surface_type` values, mapping each verb to a claim + optional conditions set:

```yaml
# plugin/config (excerpt)
capabilities:
  claude_desktop:
    "tool.call":
      claim: available
    "resource.read":
      claim: available
    "prompt.complete":
      claim: conditionally_available
      conditions:
        requires_user_consent: true
        max_tokens: 4096
    "audit.read":
      claim: available
    "surface.detect":
      claim: available
  chatgpt:
    "tool.call":
      claim: available
    "resource.read":
      claim: unavailable        # GPT actions don't expose generic resource read
    "prompt.complete":
      claim: unavailable
    # ...
  slack_thread:
    "tool.call":
      claim: conditionally_available
      conditions:
        requires_app_install: true
    # ...
  unknown:                        # surface-detect fallback
    "tool.call":
      claim: unavailable          # safe default: claim nothing until identified
    # all other verbs default to unavailable for unknown surface
```

**Justification**:
- **Keyed on `surface_type`** (ADR-065 D3 enum values) so the map composes directly with the capability primitive — no translation layer
- **Verb-level granularity** (one entry per ADR-065 D3 verb) so each capability is independently declarable + the matrix is explicit rather than implicit
- **`conditions` is per-verb-per-host**, not global — same verb may have different conditions across hosts (e.g., `requires_user_consent: true` on Claude Desktop vs. `requires_app_install: true` on Slack)
- **`unknown` surface has explicit defaults** — Postel-ish degradation: claim-nothing-until-identified is the safe fallback (consistent with ADR-060 floor-first)

**Pattern-072 8th application**: this map IS a registry. Typed enum (verb × surface_type) + documented consumers (the MCP server's claim-composer + the receiving hosts) + register-time validation (config-load-time schema check) + default policy (unknown verb-or-surface → `unavailable`). 8th application after task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, action VERB enum, ADR-065 D3 capability primitive. CIO catalog flag at Day-7 findings memo.

**Alternatives considered**:
- **Per-host-per-verb code branching** (the antipattern) — rejected: scatters per-host variance across skills/methods, makes new-host onboarding O(N) of touched code
- **Verb-keyed (host as condition)** — rejected: makes `conditions` carry the per-host predicates explicitly, but the map shape becomes harder to read at a glance + harder to audit "what does Claude Desktop get?"
- **Three-tier hierarchy (cohort default → host group → host)** — rejected for v1.0 (overengineered for the current set of hosts); revisit at v2.0 if the host count grows substantially

### D2: Surface-detection handshake

**Decision**: At plugin startup (MCP server initialization), the plugin emits a `surface.detect` capability claim package (ADR-065 D3 shape) with `claim: unknown` to the connected host. The host responds with an ADR-065 capability-claim package identifying its `surface_type` and any host-specific extensions. The plugin caches the detected identity for the session and uses it for all subsequent claim composition.

```
Plugin → Host:  {envelope: {package_type: "capability_claim", source: {agent: "piper-morgan", host_surface: "unknown", ...}},
                 body: {verb: "surface.detect", claim: "unknown"}}

Host → Plugin:  {envelope: {package_type: "capability_claim", source: {agent: "host-mcp-client", host_surface: "claude_desktop", host_surface_version: "1.4.2"}},
                 body: {verb: "surface.detect", claim: "available", surface_type: "claude_desktop"}}

Plugin caches: host_identity = "claude_desktop" (session-scoped)
```

**Justification**:
- **Uses ADR-065 D3 primitive** — `surface.detect` is just another verb in the closed enum; the handshake is self-describing in the same format the rest of the protocol uses (no parallel "handshake protocol" to maintain)
- **Falls back to `surface_type: unknown`** if host doesn't respond or returns an unrecognized identity — degrades to the `unknown` surface's capability profile from D1 (which defaults all verbs to `unavailable`; ADR-060 floor-first inheritance)
- **Session-scoped cache** is the right TTL: host identity doesn't change mid-session; re-detect on session restart
- **PDR-005 AC-1 mechanism**: this is the implementation of "surface-presence detection" that PDR-005 v1.0 committed to as the host-aware capability map's predicate

**Alternatives considered**:
- **Plugin guesses from environment** (env vars, process tree, etc.) — rejected: host-side declaration is more reliable + extensible
- **Host-initiated handshake** (host asks "what are you?") — rejected: plugin-initiated is consistent with capability-claim flow direction (plugin is the claim source)
- **No handshake; only static config** — rejected: forces per-deploy config matching the deploy target, defeats the abstraction goal

### D3: Capability-claim composition

**Decision**: Claim composition is a **pure function** of the detected host identity (D2 output) and the config's per-host capability map (D1):

```python
def compose_capability_claims(
    host_identity: SurfaceType,           # from D2 handshake cache
    capability_map: dict[SurfaceType, dict[Verb, ClaimSpec]],  # from D1 config
) -> list[CapabilityClaim]:
    """Pure function — same inputs always produce same output; no side effects."""
    host_profile = capability_map.get(host_identity) or capability_map["unknown"]
    return [
        CapabilityClaim(
            verb=verb,
            surface_type=host_identity,
            claim=spec.claim,
            conditions=spec.conditions or {},
        )
        for verb, spec in host_profile.items()
    ]
```

**Justification**:
- **Pure function** = no #ifdef-style branching in MCP-server methods; per-host variance is concentrated in the capability map (D1), not scattered through implementation code
- **Same inputs → same output** = testable (unit test per host profile); auditable (one place to look for "what does host X get?")
- **`host_profile.get(host_identity) or capability_map["unknown"]`** = explicit fallback to the safe-default profile if D2 handshake returned an unrecognized identity (defense in depth)
- **Conditions carried verbatim** = the receiver evaluates them at request time (D5 SDK helper layer); the plugin doesn't pre-evaluate predicates that depend on per-request context

**Alternatives considered**:
- **Lazy composition** (compose on-demand per request) — rejected: handshake-time composition matches handshake-time cache TTL; per-request re-composition adds latency without value
- **Class hierarchy with per-host subclasses** — rejected: re-introduces the per-host code branching the abstraction is designed to prevent

### D4: Degradation policy — three tiers

**Decision**: When a capability claim's runtime evaluation diverges from the static claim, the plugin surfaces one of three responses via the ADR-065 D4 error envelope:

| Tier | Claim state | Runtime state | Response |
|---|---|---|---|
| **1: Static-unavailable** | `unavailable` (per D1 map) | (not evaluated) | Capability simply not advertised. Host receives no `capability_claim` package for that verb. **No error surface.** |
| **2: Static-conditional, runtime-degraded** | `conditionally_available` + `conditions` (per D1 map) | Predicate evaluation fails (e.g., `requires_user_consent: true` but consent absent) | ADR-065 D4 error envelope: `error_code: CAPABILITY_UNAVAILABLE`, `retry_hint: needs_user_action`, `human_message` explains the missing precondition. **User-visible.** |
| **3: Static-available, runtime-failed** | `available` (per D1 map) | Tool invocation fails (transient, host limitation, etc.) | ADR-065 D4 error envelope: `error_code: TOOL_FAILED` (or specific code), `retry_hint: transient | permanent` per failure mode. **User-visible.** |

**Justification**:
- **Three tiers cleanly separate the failure modes** the receiver needs to handle differently:
  - Tier 1: no error surface needed (cleanly out-of-scope; host filters the verb out of UI)
  - Tier 2: precondition-fixable (user can act to enable the capability)
  - Tier 3: runtime-failure (user can retry or accept the failure)
- **Composes with ADR-065 D4 error envelope** directly — no new error semantics; just clear mapping of degradation tier → envelope shape
- **No silent failure** — tiers 2 + 3 both surface a well-formed error envelope; tier 1 is silent because it's by design (the capability is simply not claimed)

**Alternatives considered**:
- **Two-tier (available vs. unavailable)** — rejected: collapses tier 2 + tier 3 into one error code; loses the actionable distinction between "fix a precondition" vs. "retry or fail"
- **Five-tier with finer-grained codes** — rejected: more codes ≠ more clarity; the three-tier split maps cleanly to user-facing semantics

### D5: SDK helper layer

**Decision**: Ship a per-language SDK helper library (initially Python + TypeScript) that receivers (MCP clients + sibling projects) consume to:

1. **Parse capability claims** — deserialize ADR-065 D3 capability_claim packages into typed objects matching the receiver's language idioms
2. **Evaluate `conditions` predicates** — given a parsed claim with `conditions`, evaluate against the receiver's runtime context (e.g., user consent state, app install state) and return `bool` + reason-if-false
3. **Generate well-formed error envelopes** — given a tier-2 or tier-3 degradation, produce an ADR-065 D4-conformant error envelope without the receiver having to know the schema details
4. **Handle the `surface.detect` handshake** — emit the response package + populate the surface_type field correctly

```python
# Python SDK (sketch)
from piper_morgan_sdk import CapabilityClaim, ConditionEvaluator, ErrorEnvelope

claim = CapabilityClaim.from_package(received_package)  # (1) parse
evaluator = ConditionEvaluator(runtime_context={"user_consented": True, ...})
result = evaluator.evaluate(claim.conditions)            # (2) evaluate predicates
if not result.ok:
    error = ErrorEnvelope.capability_unavailable(       # (3) generate error envelope
        verb=claim.verb,
        human_message=f"Cannot {claim.verb}: {result.reason}",
        retry_hint="needs_user_action",
    )
    return error.to_package()
# ...proceed with capability invocation
```

**Justification**:
- **Mitigates ADR-065 §Consequences/Negative** — the "capability conditional-not-boolean tradeoff" (D3 puts evaluation work on the receiver) is the cost ADR-065 acknowledged; SDK helpers absorb the evaluation complexity so receivers write business logic, not schema parsing
- **Per-language packages** (Python, TypeScript at v1.0; more as ecosystem demands) — published separately from the plugin so non-plugin consumers (sibling projects, third-party MCP clients) can integrate without needing the plugin source
- **Optional, not required** — receivers can implement ADR-065 directly if they prefer; SDK is convenience-layer, not a gated dependency

**Alternatives considered**:
- **Distribute helpers as plugin `skills`** — rejected: forces every receiver to depend on the plugin; sibling projects shouldn't need that
- **No SDK; receivers implement raw** — rejected: ADR-065's conditional-claim shape is non-trivial; absence of SDK means every receiver re-derives the parsing/evaluation/error-generation logic with inevitable inconsistencies

### D6: Sibling-project receiver shape

**Decision**: Sibling projects (Klatch primarily; future systems generically) consume Piper Morgan's capability claims through **the same SDK helper interface as MCP-client hosts** — no separate "sibling-project integration mode."

The sibling project:
- Implements the receiver side of ADR-065 wire format (envelope + body + extensions)
- Uses the D5 SDK helper for parse/evaluate/error-envelope (same package as MCP clients use)
- Identifies itself in the D2 handshake with `surface_type: "sibling_project"` (or a more specific value if a registered sibling-project identifier exists)
- Subject to the same per-host capability profile shape (D1) — `sibling_project` is just another `surface_type` key in the capability map

**Justification**:
- **Same interface across receiver types** = one SDK to maintain, one set of error semantics, one handshake protocol. Sibling projects don't get a special case.
- **`surface_type: sibling_project` is registered in D1's map** with explicit verb-by-verb claim settings — Klatch's profile lives there alongside `claude_desktop`, `chatgpt`, etc.
- **Klatch alignment naturally folds in** when Daedalus relays the L1-L5 layer model — adjustments live in §Evolution; primitives remain stable

**Alternatives considered**:
- **Separate "sibling-project protocol"** — rejected: same problems as separate handshake protocol — parallel-thing-to-maintain
- **Klatch-specific integration adapter** — rejected: forces per-sibling adapters; defeats the abstraction goal at the cohort-of-siblings layer

---

### D7: Configuration Ownership Convention — Server-Owned + Per-Request Host Augmentation (v0.2 addition)

**Decision** (v0.2): **Configuration durability lives behind the MCP server, not on the host's filesystem.** The host augments per-request with ephemeral context; it does not package or persist configuration state. The plugin's `config` artifact (D6 declaration sites) is consumed by the *server's* startup, not the host's. Configuration does not cross the host↔server boundary as durable state; only ephemeral per-request augmentation crosses.

This is a v0.2 amendment to v0.1's implicit model ("host packages config → server consumes"), driven by the **Cowork 2026-06-05 sandbox-runtime finding**: meet-piper's config-write to `~/.claude/` failed in Cowork because the sandboxed runtime ≠ host filesystem. The constraint forced a refinement: if config doesn't live on the host's filesystem, the host can be any runtime — Code, Cowork, Desktop, future ChatGPT plugin, future hosted-on-marketplace listing. The filesystem dependency that broke Cowork goes away by construction.

**The two roles, explicitly:**

| Surface | Owns | Examples |
|---|---|---|
| **Server (MCP server)** | Configuration durability — `config` artifact, user preferences, per-tenant settings, credential references | The schema spec file (ADR-066 D6) lives in plugin package; the *materialized config* at runtime lives in server-side storage (DB, server filesystem, KMS) |
| **Host** | Per-request ephemeral augmentation only | Current user-session context; transient operational state; nothing the server needs to recover after a session ends |

**Why this is a refinement, not a withdrawal of v0.1:**

v0.1 D1 (per-host capability map) + D6 (plugin packaging declaration sites) remain unchanged. What changes is the *operational* boundary: the `config` file at deployment time describes the capability profile (a *spec*); the runtime config-state (user preferences, deployed credentials, learned associations) lives behind the server. The plugin packaging at D6 specifies the schema; D7 specifies who owns the materialized state at runtime.

**The "run anywhere" property — natural rather than aspirational:**

PDR-005's BYOC commitment implies plugin portability across hosts. v0.1 imagined this as the host packaging config and the server consuming whatever the host could provide — which makes "run anywhere" an aspirational property contingent on every host runtime supporting filesystem write to a conventional location. D7's inversion makes "run anywhere" a **structural property by construction**: the host never has to write configuration durably, so no host-runtime-specific filesystem assumption can block plugin deployment. Cowork → server-owned-config converted a constraint into a cleaner architecture; the cleaner architecture composes with arbitrary host runtimes.

**Composition with v0.1 sub-decisions:**

- **D1 (capability map)**: unchanged. The map is still declared in the plugin's `config` schema; the *materialized* per-deployment instance lives behind the server (a hosted Piper instance reads its per-host capability profile from server-side config, not from host filesystem state).
- **D2 (surface-detection handshake)**: unchanged. The handshake protocol does not depend on where configuration lives; it identifies the host runtime regardless.
- **D3 (capability-claim composition)**: unchanged. The compose function takes (per-host map, runtime identity) → claims; both inputs come from server-owned state.
- **D4 (degradation policy)**: unchanged.
- **D5 (SDK helpers)**: unchanged. Receiver-side SDK is host-side ephemeral context; not affected by D7.
- **D6 (sibling-project receiver shape)**: unchanged. Same SDK interface; D7 specifies who persists what across the boundary.

**Composition with companion ADRs:**

- **ADR-065 (canonical context-package format)** v0.1 is data-shape-independent of where config lives. D7 does not amend ADR-065; if anything, D7 makes ADR-065 D2 (package contents) *simpler* because there is less metadata about configuration that the host might need to package. Net-positive for ADR-065's clarity.
- **ADR-058 (user-scoped credentials)** is the precedent: per-user credentials live behind the server, indexed by user identity. D7 extends the same convention to per-deployment configuration. When #1185 (per-user LLM keys) lands, D7's server-owned-config pattern naturally accommodates per-user key materialization through the same surface.
- **ADR-068 candidate (BYO-colleague Skill-Brokered Host Deputization)** is downstream of D7. A deputized Piper colleague accessed through a brokered host must not require the host to package configuration — D7 ensures this is true by construction. The HOST trust-lens (2026-06-13) framed this as the *good-guest* boundary realized structurally; D7 is the architectural surface where the good-guest property is enforced.

**Cross-link to methodologies + patterns:**

- **methodology-41 (Mechanism Displaces Unreferenced Discipline) — third sub-shape, architecture-boundary altitude**. The "don't write to host filesystem in non-Code runtimes" discipline was previously vigilance; D7 makes it impossible by construction (the host has no role to play in configuration durability). CIO accepted this as m-41's third instance 2026-06-13 with confluence-framing caveat (m-41 ↔ m-36 ↔ Pattern-070 confluence). D7 is the architectural artifact that records the cure.
- **Pattern-070 (External validation refining design) — goodness-from-constraint instance**. The Cowork sandbox constraint pushed us toward a cleaner architecture than we had designed unconstrained. Same shape as Pattern-070's canonical instance (External validation via Anthropic Dreams API spec read 2026-05-27). CIO catalog hook.
- **methodology-36 (mechanism-beats-vigilance, Class-2)** composes — the trust property (good-guest) that used to need watching now doesn't need watching because the structure forbids the failure mode. HOST trust-lens 2026-06-13 surfaced the m-36 framing alongside m-41.

**Counter-arguments considered:**

- **"D7 should be its own ADR rather than amending ADR-066."** Considered + rejected. D7 is operationally inseparable from D1-D6: configuration-ownership semantics are a property of the packaging-layer abstraction, not a separable concern. A standalone ADR would force readers to compose two artifacts mentally for what is one decision-space.
- **"D7 should withdraw v0.1's implicit host-packages-config assumption explicitly."** Considered + rejected. v0.1 never stated the implicit model; it just didn't constrain ownership. D7 fills the unconstrained slot rather than withdrawing a stated decision. Honest framing per m-30 (Consumer-Trace Verification) discipline — don't invent a v0.1 position to withdraw if v0.1 didn't state one.
- **"D7 should mandate specific server-side storage (DB / KMS / filesystem)."** Considered + rejected. Storage substrate is implementation-altitude; D7 specifies *who owns durability*, not *how it's stored*. ADR-058 user-scoped credentials sets the precedent: convention specifies ownership; substrate is downstream. D7 mirrors.

**Open question (D7-specific):**

- **D7 OQ-1**: When does the server-owned-config materialize relative to handshake (D2)? Initial lean: per-session at first request after handshake completes; cache through session end. Lead Dev consultation when first hosted Piper deployment scopes (Phase 2a per Skunkworks BYOC).

---

## Implementation sequencing (suggested)

Not gating decisions — sequencing notes for Lead Dev / implementation reviewers:

1. **D1 (capability map schema)** ships first — additive declaration; no runtime behavior change
2. **D2 (handshake)** + **D3 (compose function)** ship together — handshake produces input, compose produces output; testable as a pair
3. **D4 (degradation policy)** ships with the first tier-2-conditioned capability — until any verb has `conditions`, tier 1 + tier 3 are the only live paths
4. **D5 (SDK helpers)** ships in waves — Python first (Piper Morgan's own ecosystem); TypeScript when first non-Python receiver lands; one-language-at-a-time keeps the surface manageable
5. **D6 (sibling integration)** activates when first sibling project (likely Klatch) integrates — same SDK; just add their `surface_type` to D1's map
6. **D7 (configuration ownership)** ships with the first hosted-Piper deployment (Skunkworks BYOC Phase 2a) — the server-owned-config convention is validated when meet-piper-style host-filesystem-write is provably absent. v0.2 amendment landed 2026-06-14; first operational instance scheduled with Phase 2a build.

---

## Consequences

### Positive

- **Same plugin code paths deploy to multiple hosts without bespoke per-host code** — D3's pure-function claim composition + D1's per-host capability map concentrate per-host variance at the config layer, not in skills or MCP-server methods. Adding a new host = adding a `surface_type` entry to the D1 map + (if needed) a new value to ADR-065 D3's verb enum. No code branching.
- **Capability variance concentrated at the packaging layer** — exactly the "mechanism-not-vigilance" discipline the cohort applies elsewhere (Pattern-073 doc-sync-sweep at packaging; methodology-30 consumer-trace at boundary surfaces). One place to look for "what does host X get?"; one place to change when host X's capability profile changes.
- **Sibling-project integration mirrors host integration** — D6's same-SDK-interface decision means Klatch and future siblings consume the same parse/evaluate/error-envelope helpers as MCP-client hosts. No per-sibling adapter; no parallel integration mode.
- **Pattern-072 8th application confirmed** (per-host capability map) — the 8th in the catalog after task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, action VERB enum (ADR-060 amendment 6th), capability primitive (ADR-065 D3 7th), capability map (this ADR D1 8th). Three new applications in 48h validates the pattern's load-bearing role across the BYOC stack. CIO catalog awareness flag at Day-7 findings memo (~Jun 13).
- **ADR-060 floor-first inheritance preserved cross-host** — D1's `unknown` surface defaults all verbs to `unavailable`; D2's handshake fallback routes unrecognized identities to the `unknown` profile; D4 tier 1 (silent unavailable) is the cross-host shape of the same floor-first safe-fallback. The architectural principle (unknown → safe-default) is consistent from intent-classifier (ADR-060) → LLM-touch (ADR-061) → audit envelope (ADR-063) → context-package format (ADR-065) → packaging layer (this ADR). One discipline, five composing surfaces.
- **methodology-32 Postel discipline composes cross-host** — D1's `unknown` surface defaults + D2's handshake fallback + D4's degradation tiers are all Postel-ish (be conservative in what you send; be liberal in what you accept). The MCP-stdio binding is just the current transport; the same discipline applies to future WebSocket / HTTP bindings (ADR-065 D5 SemVer + transport-agnostic JSON-encoded text).
- **PM-as-catch-of-last-resort load-distribution gets relief at the packaging layer** — bilateral coordination between Piper Morgan and a connected host is no longer ambient/implicit; it's explicit at D2 handshake + D1 capability map. The HOST m-39-adjacent watch-item benefits indirectly: explicit cross-process coordination at the packaging layer means PM doesn't need to be the cross-host observer for "what does host X support?" questions.
- **"Run anywhere" becomes a structural property (v0.2 D7)** — by removing the host's role in configuration durability, no host-runtime-specific filesystem assumption can block plugin deployment. Cowork sandbox, Claude Desktop, ChatGPT plugin, future marketplace listings — all valid hosts by construction. This was an aspirational property in v0.1; it is a structural property in v0.2.
- **The HOST trust-lens "good-guest" boundary is enforced architecturally (v0.2 D7)** — Piper does not reach into the host's environment to persist anything. The trust property that was previously vigilance is now structure. m-41 architecture-boundary cure sub-shape (CIO 2026-06-13).

### Negative / Tradeoffs

- **Per-host capability map maintenance overhead** — the matrix grows with hosts × capabilities. Today's v1.0 set is small (~5 hosts × ~6 verbs = ~30 entries); a future v2.0 with 15 hosts and 20 verbs is 300 entries. Mitigations: (a) the `unknown` surface defaults catch the long tail of unsupported hosts; (b) Pattern-073 doc-sync-sweep keeps the map honest; (c) the three-tier hierarchy alternative (cohort default → host group → host) was rejected for v1.0 but remains the v2.0 refactor target if the matrix explodes.
- **Surface-detection handshake adds startup latency** — D2's handshake is one round-trip at MCP server initialization. Mitigation: session-scoped cache (one handshake per session, not per request). The latency cost is on session-start, not per-message; acceptable for the BYOC use case.
- **SDK helper layer is non-trivial work** (D5) — Python + TypeScript at v1.0; more languages as ecosystem demands. Each language requires: parse/serialize + condition-evaluator + error-envelope-generator + handshake-handler. Ships in waves (D5 sequencing note); not all-at-once.
- **Capability claim semantics inherit ADR-065 §Consequences/Negative complexity** — D3's `claim: conditionally_available` + `conditions` puts evaluation work on the receiver (acknowledged in ADR-065). D5's SDK helpers mitigate but don't eliminate; receivers must still implement `conditions` predicate evaluation against their runtime context. Acceptable: this is the cost of conditional-claim-per-host (EC-2 architectural input); a boolean-only claim would be simpler but architecturally wrong per the EC-2 reasoning.
- **Klatch alignment may arrive late** — same risk as ADR-065 §Consequences/Negative; same mitigation (§Evolution-section absorption per Pattern-064 convention; primitives stable across alignment refinements).

### Non-consequences

- **This ADR does NOT replace ADR-065's primitive decisions** — verb-enum + slot (D3), envelope+body+extensions (D2), error envelope (D4), SemVer + Postel (D5), spec-file-as-source-of-truth (D6) all come from ADR-065. This ADR organizes them into a deployment-time abstraction; doesn't redefine them.
- **This ADR does NOT mandate which specific hosts are supported at v1.0** — that's PDR-005 §Mechanism set scope. The capability map's keys are example values; the actual v1.0 host list is a PDR-005 decision.
- **This ADR does NOT specify the specific SDK languages beyond v1.0 lean** — Python + TypeScript at v1.0 are the lean (D5); the actual language matrix evolves with receiver ecosystem demand. Specific language packages are follow-up artifacts.
- **This ADR does NOT decide the wire transport** — D1 wire format is JSON-encoded text per ADR-065 D1; transport (MCP stdio, future HTTP/WebSocket) is separable. Current binding is MCP stdio.
- **This ADR does NOT specify the concrete D1 capability map content** for the v1.0 host set — that's a deployment-time artifact (the actual `plugin/config` file); this ADR specifies the schema the file must conform to.
- **This ADR does NOT decide per-platform persona-template content** — that's PDR-006 (post-1.0, per PDR-005 §Open question 5).

---

## Evolution

- **v0.2 amendment (2026-06-14)** — D7 added (Configuration Ownership Convention). Source incident: Cowork 2026-06-05 sandbox-runtime config-write failure. Source synthesis: Skunkworks BYOC Phase 2 Arch lens 2026-06-13; HOST trust-lens 2026-06-13; CIO m-41 third-instance acceptance 2026-06-13 with confluence framing. PA green-light to draft 2026-06-14 (PM directed: "while the reasoning is sharp").
- **Klatch-pause framing (carried from v0.1)** per Pattern-064 convention: when Klatch resumes and Daedalus relays packaging-layer feedback via Janus, fold into this section as dated entry.

---

## Open questions (v0.1)

1. **Per-host capability map source-of-truth location** — `config` declares per host (D1); is there a separate canonical "supported hosts + capability profiles" registry, or is `config` the registry? Initial lean: `config` is per-plugin-deploy declaration; a separate cohort-level registry of "what hosts are supported, with what default capability profile" lives elsewhere (likely `docs/`).
2. **Surface-detection handshake protocol** (D2) — what's the message shape? Initial lean: a `surface.detect` capability claim package with `claim: unknown` triggers the host to respond with its identity. Lead Dev consultation at Fire 4+.
3. **SDK helper distribution** (D5) — published as plugin's `skills` or as separate language packages? Initial lean: published as separate language packages (PyPI, npm) so non-plugin consumers can integrate too. Lead Dev consultation.
4. **Sibling-project integration depth** (D6) — does Klatch consume capability claims the same way an MCP client does, or does it consume a higher-level abstraction? Pending Klatch resumption + Daedalus feedback.
5. **Pattern-072 application count** — confirmed as 8th application if the per-host capability map becomes a typed registry. CIO catalog awareness flag at next cron-shape findings memo.

---

## What this ADR is NOT

- Not the canonical context-package format (that's ADR-065 — companion ADR)
- Not the wire transport choice (MCP stdio + future bindings; transport-agnostic per ADR-065 D1)
- Not the Klatch alignment outcome (lives in §Evolution when it arrives)
- Not a specific SDK implementation (the helper layer's shape is decided here; implementation is downstream)
