# ADR-066: Packaging-Layer Abstraction (BYOC Plugin Per-Host Deployment)

**Status**: DRAFT v0.1 SKELETON (2026-06-06, Fire 3) — Architect-authored; companion to PDR-005 v1.0 §Open question 7; gated by ADR-065 v0.1 ✅ (just filed in this fire). Skeleton frames the problem space; Fire 4+ fills §Decision content.

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

[v0.1 SKELETON — to be filled in Fire 4+. Sub-decisions D1-D6 named above.]

### D1: Per-host capability map shape

[How the plugin's `config` declares the capability profile per host. Initial lean: YAML map keyed on `surface_type` values from ADR-065 D3, mapping to claim+conditions sets per verb. Pattern-072 8th application candidate.]

### D2: Surface-detection handshake

[Plugin startup protocol: emit a `surface.detect` capability claim package (ADR-065 D3 shape), receive host's identity response. Falls back to `surface_type: unknown` if host doesn't respond — degrades gracefully via floor (ADR-060 inheritance).]

### D3: Capability-claim composition

[Runtime composition: detected host identity + config's per-host map → emitted capability claims. Pure function; no #ifdef branching in MCP-server methods.]

### D4: Degradation policy

[Three tiers: (1) claimed capability unavailable at runtime → `CAPABILITY_UNAVAILABLE` error envelope (ADR-065 D4); (2) capability degraded but partially available → `claim: conditionally_available` + `conditions` predicate; (3) capability unclaimed → no error surface, capability is simply not in the map.]

### D5: SDK helper layer

[Receiver-side helpers for parsing capability claims + conditions, evaluating predicates, generating well-formed error envelopes. Mitigates the conditional-not-boolean complexity acknowledged in ADR-065 §Consequences/Negative.]

### D6: Sibling-project receiver shape

[Klatch and future sibling projects: same SDK helper interface as MCP-client hosts; integration is at the packaging layer not at code-modification.]

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
