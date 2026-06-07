# ADR-066: Packaging-Layer Abstraction (BYOC Plugin Per-Host Deployment)

**Status**: DRAFT v0.1 (2026-06-06 Fire 3 skeleton + 2026-06-07 Fire 6 §Decision D1-D6 content filled) — Architect-authored; companion to PDR-005 v1.0 §Open question 7; gated by ADR-065 v0.1 ✅. Fire 7+ will polish + §Consequences refinement + v0.1 final (same shape as ADR-065 bursty-lane arc).

**Date**: 2026-06-06

**Authors**: Chief Architect (Arch)

**Reviewers**: PPM (PDR-005 owner), Lead Dev (implementation lane), CIO (methodology), CEO (xian)

---

## Status

- **v0.1 DRAFT SKELETON** filed 2026-06-06; Fire 3 of the bursty-lane ADR arc (Fire 4+ in subsequent cron passes will fill in §Decision content)
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

## Implementation sequencing (suggested)

Not gating decisions — sequencing notes for Lead Dev / implementation reviewers:

1. **D1 (capability map schema)** ships first — additive declaration; no runtime behavior change
2. **D2 (handshake)** + **D3 (compose function)** ship together — handshake produces input, compose produces output; testable as a pair
3. **D4 (degradation policy)** ships with the first tier-2-conditioned capability — until any verb has `conditions`, tier 1 + tier 3 are the only live paths
4. **D5 (SDK helpers)** ships in waves — Python first (Piper Morgan's own ecosystem); TypeScript when first non-Python receiver lands; one-language-at-a-time keeps the surface manageable
5. **D6 (sibling integration)** activates when first sibling project (likely Klatch) integrates — same SDK; just add their `surface_type` to D1's map

---

## Consequences

[v0.1 SKELETON — to be filled in Fire 4+]

### Positive (anticipated)

- Same plugin code paths deploy to multiple hosts without bespoke per-host code
- Capability variance concentrated at the packaging layer, not scattered through skills/MCP-server methods
- Sibling-project integration mirrors host integration (SDK helpers + capability map)
- Pattern-072 8th application surfaces (per-host capability map) — discipline catalog awareness via CIO flag

### Negative / Tradeoffs (anticipated)

- Per-host capability map maintenance overhead (matrix grows with hosts × capabilities)
- Surface-detection handshake adds startup latency (mitigation: cache detected host identity)
- SDK helper layer is non-trivial work; ships in waves not all-at-once

### Non-consequences

- This ADR does NOT replace ADR-065's primitive decisions (verb-enum + slot, error envelope shape, versioning)
- This ADR does NOT mandate which specific hosts are supported at v1.0 (that's PDR-005 §Mechanism set scope)
- This ADR does NOT specify the specific SDK languages (Python, TypeScript, etc.) — that's a follow-up artifact

---

## Evolution

(Empty at v0.1 SKELETON filing. Klatch-pause framing per Pattern-064 convention: when Klatch resumes and Daedalus relays packaging-layer feedback via Janus, fold into this section as dated entry.)

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
