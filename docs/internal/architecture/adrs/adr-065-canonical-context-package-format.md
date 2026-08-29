# ADR-065: Canonical Context-Package Format (BYOC / Plugin-Packaged)

**Status**: v0.1 (filed 2026-06-06) — Architect-authored; companion to PDR-005 v1.0 §Open question 6; in-house material per Klatch-pause Evolution-section convention (HOST 2026-05-24). Three-fire bursty-lane drafted (Fire 1 skeleton + plugin-packaging framing; Fire 2 §Decision D1-D6 substantive content; Fire 3 polish + §Consequences refinement + v0.1 final).

**Date**: 2026-06-06

**Authors**: Chief Architect (Arch)

**Reviewers**: PPM (PDR-005 owner), Lead Dev (implementation lane), CIO (methodology), CEO (xian)

---

## Status

- **v0.1** filed 2026-06-06 in-house pending Klatch alignment (Klatch paused since May 20; Klatch refinements fold to §Evolution per Pattern-064 convention if/when alignment resumes)
- Gated by: PDR-005 v1.0 ratification ✅ (2026-06-05)
- Gates: Q7 (ADR-066 packaging-layer abstraction implementation)
- Source-of-truth for canonical context-package format used by Piper Morgan in BYOC distribution and cross-project handoff (e.g., Klatch sibling-project integration)

## Context

### What problem does this ADR solve?

PDR-005 v1.0 (Bring Your Own Chat, ratified 2026-06-05) commits Piper Morgan to **MCP server primary + thin bespoke UI** distribution. The mechanism set #5 names "context-package format negotiated with sibling projects" as an architectural commitment. PDR-005 §Open question 6 routes the specific format decision to this ADR.

The concrete need: when Piper Morgan **exposes its context state** to a host (MCP client like Claude Desktop, ChatGPT, Slack) or a sibling project (Klatch, future systems), or when Piper Morgan **consumes context state** offered by an external surface, the **shape** of that interchange has to be canonical and stable enough that:

- Multiple hosts can serialize/deserialize without bespoke per-host code at the protocol layer
- Sibling projects (Klatch primarily; future systems generically) can interoperate without bridging
- New surfaces can be added without breaking existing surfaces (Postel-ish forward compatibility per methodology-32)
- The format itself is auditable, versionable, and can carry provenance

### Why "plugin-packaged"?

PM clarified 2026-06-01 (via PA): the **plugin** is the canonical Anthropic-side packaging unit — `config + CLAUDE.md + skills + MCP server`. MCPB and hosted-MCP are NOT the packaging unit; they are deployment targets for the plugin's MCP server component. The context-package format is what flows **between** the plugin's MCP server and connected hosts/projects.

So Q6 has two layers:

1. **The context-package wire format** — the actual bytes/JSON/whatever Piper Morgan emits or accepts at the MCP boundary
2. **The plugin-packaging context** — how the format relates to the plugin's other components (`config`, `CLAUDE.md`, `skills`, `MCP server`)

This ADR addresses both. Layer 1 is the load-bearing decision; layer 2 is how the format fits into the plugin's distribution shape.

### Klatch alignment context

Per Architect↔Daedalus alignment brief (Architect to Janus, 2026-05-15) the cross-project alignment question is: **"What is the canonical context package?"** The brief asked Klatch's read on:

- L1–L5 + MCPB export package shape (Klatch's layer model)
- Layer-boundaries needing 1:1 mapping vs. translation
- Format decisions where bi-directional handoff benefits from upstream-aligned spec

**Klatch paused 2026-05-20** before Daedalus's reply landed. This ADR proceeds with **in-house material** per the Pattern-064 Evolution-section convention HOST lifted (2026-05-24) as the general operating norm for uncertain external-alignment dependencies. Klatch refinements fold into §Evolution when alignment resumes; the ADR does not block on Klatch reply.

### Format-decision space (from the Janus brief)

Four sub-decisions inside Q6:

- **Token-structure conventions** — what primitive shape carries an information unit (a "memory", a "tool call", a "context slice")
- **Metadata-envelope shape** — what wrapper carries provenance / authorship / versioning / timestamps
- **Capability-advertisement primitives** — how Piper Morgan tells a host "here's what I can do" (paired with PDR-005 AC-1 host-aware capability map; Q7 carries the per-host map)
- **Error-envelope semantics** — how tool-failure or capability-unavailable surfaces (paired with ADR-063 audit-envelope read-surface; Surface 7 architectural commitment)

### Prior art / cross-references

- PDR-005 v1.0 §Mechanism set #5 — context-package format negotiated with sibling projects
- PDR-005 v1.0 §Open question 6 — routes to this ADR
- PDR-005 v1.0 §AC-1 (surface-presence detection) — host-aware capability claim layer; this format must carry capability-presence info
- ADR-061 (LLM-touch boundary four-element principle) — applies at every place this format crosses an LLM-touch boundary
- ADR-063 (User-Facing Audit Envelope Read-Surface) — the audit envelope shape this format must compose with
- ADR-064 (Project-Scope Search Index Architecture) — the index-declaration registry pattern is sibling-shaped
- Architect↔Daedalus alignment brief (2026-05-15) — full PM-side state at the time of the question
- Pattern-072 (Registries that Grow into Architectural Shapes, Proven, 7+ applications post-this-ADR — task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, action VERB enum [6th, 2026-06-06], capability primitive [7th, this ADR D3]) — shape for capability registry confirmed at D3
- methodology-32 (Postel for Memo Headers) — Postel's-law discipline for forward compat
- methodology-38 (PDR/ADR Tier Separation, Emerging) — Q6 is the implementation-altitude ADR companion to PDR-005's decision-rule altitude
- **methodology-40 (Layer-Then-Migrate, Emerging, CIO-confirmed 2026-06-09)** — D3 capability primitive (verb-enum + `surface_type` slot) is m-40 instance #3 in the catalog; the verb-enum-as-source-of-truth + slot-as-separable-dimension shape inherits from ADR-060 amendment's same architectural primitive at the intent-classifier altitude

---

## Decision

The canonical context-package format is **JSON-encoded, three-layer (envelope + body + extensions), with typed-enum capability primitives, ADR-063 READ-side error envelopes, Postel-ish forward compat, and plugin-`config`-declared format versions**. Each sub-decision is grounded in either prior architectural commitments (PDR-005, ADR-061, ADR-063), prior cross-project alignment work (Janus brief 2026-05-15), or existing pattern catalog entries (Pattern-072, methodology-32).

### D1: Wire format = JSON with explicit schema-version field

**Decision**: All context packages are JSON-encoded text with a mandatory top-level `schema_version` field (`MAJOR.MINOR.PATCH` SemVer-flavored).

**Justification**:
- MCP wire transport is JSON-RPC; using JSON for the package body adds zero deserialization machinery beyond what MCP servers already run
- Every plausible host (Claude Desktop, ChatGPT, Slack, custom UIs, sibling projects like Klatch) has mature JSON tooling at the language layer
- Human-readability matters at the audit / debug layer (you can `jq` a context package; you cannot `jq` a Protobuf blob without the schema)
- Pattern-073-disciplined: the same wire shape lives in spec doc, schema validator, and serializer — one source of truth, doc-sync-sweep catches drift
- `schema_version` at the top level (NOT buried in envelope sub-fields) lets receivers route to the right deserializer before parsing the rest

**Alternatives considered**:
- **Protobuf**: Binary efficiency wins, but loses human-readability + adds a toolchain dependency that hosts must carry. MCP doesn't use it. Net negative for the cross-host interop use case.
- **MessagePack**: Same readability tradeoff as Protobuf; MCP doesn't use it. Rejected.
- **OpenAPI-flavored**: Designed for HTTP REST surfaces; MCP isn't REST. The schema description value of OpenAPI doesn't transfer cleanly. Rejected.
- **YAML**: More readable than JSON for nested structures, but loses MCP-native parseability and has YAML-specific footguns (Norway problem, indentation ambiguity). Rejected.

**Trade-off acknowledged**: JSON's representation limits mean binary primitives (images, audio, large blobs) live outside the format and are carried by reference (URI / content-addressable hash). This is captured under §Consequences/Negative.

### D2: Three layers per package — envelope + body + extensions

**Decision**: Every context package is structurally a three-field JSON object:

```json
{
  "envelope": {
    "schema_version": "1.0.0",
    "package_type": "capability_claim | context_slice | tool_call | tool_result | audit_event | error",
    "source": {
      "agent": "piper-morgan",
      "host_surface": "claude_desktop | chatgpt | slack_thread | bespoke_ui | sibling_project",
      "host_surface_version": "..."
    },
    "timestamp": "ISO-8601 UTC",
    "trace_id": "stable-cross-package correlation token"
  },
  "body": {
    /* package-type-specific payload */
  },
  "extensions": {
    "vendor": { /* host-or-project-specific opt-in */ },
    "experimental": { /* feature-flagged opt-in */ }
  }
}
```

**Justification**:
- **Envelope** = stable provenance + routing metadata. Receivers can validate envelope shape WITHOUT parsing body. Cheap rejection of malformed packages.
- **Body** = the semantic payload. Schema discriminated by `envelope.package_type`. Each package_type has its own body schema.
- **Extensions** = namespaced opt-in fields. Per methodology-32 Postel discipline: unknown extensions are silently ignored; the producer/consumer contract is "extensions never break compat."
- Three layers because two (envelope+body) leaves no place for opt-in fields without weakening the body schema; four+ adds boilerplate without separating concerns.

**Composes with**: ADR-063 audit envelope read-surface (audit_event package_type's body shape IS the ADR-063 envelope); ADR-061 LLM-touch four-element principle (the envelope IS the audit-envelope element at LLM-touch boundaries).

### D3: Capability-advertisement primitive = typed VERB enum + `surface_type` slot

**Decision**: When Piper Morgan advertises a capability (PDR-005 AC-1 host-aware capability map), the package body uses the **verb-enum + slot** shape established by the 2026-06-06 ADR-060 amendment ratification:

```json
{
  "envelope": { "package_type": "capability_claim", ... },
  "body": {
    "verb": "tool.call | resource.read | prompt.complete | audit.read | surface.detect | ...",
    "surface_type": "claude_desktop | chatgpt | slack_thread | bespoke_ui | sibling_project",
    "claim": "available | conditionally_available | unavailable",
    "conditions": { /* per-host predicates, e.g. requires_user_consent: true */ }
  }
}
```

**Justification — three reasons this shape is right**:
1. **Conditional-claim-per-host (EC-2 architectural input, 2026-06-03 PPM synthesis)** — capabilities are NOT universally claimed; the format carries the per-host context the receiver evaluates. `claim: conditionally_available` + `conditions` lets the receiver decide whether the capability applies in its environment.
2. **Verb-source-slot per Pattern-072** — the 6th Pattern-072 application (after task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, [now confirmed as 6th] action VERB enum). Capability primitive becomes the **7th** Pattern-072 application: typed enum of verbs + documented consumers (the receiving hosts) + register-time validation + default policy (capability-unknown → `unavailable`, the safe fallback per ADR-060 floor-first).
3. **Layer-then-migrate inherits naturally** — the same supersede-vs-layer ruling I issued on ADR-060 today applies if BYOC ever absorbs an existing capability registry. The verb enum becomes source-of-truth for the verb dimension; legacy registrations migrate progressively.

**Crucially NOT**: capability is NOT a verb-object name collapsed string (`tool_call_for_github_issue`). That's the #1158 failure mode this ADR + ADR-060 amendment are designed to prevent. **One name collapsed**, **two slots separated**.

### D4: Error envelope = ADR-063 READ-side four-element principle extended cross-host

**Decision**: Error packages (`envelope.package_type == "error"`) use a body shape that adapts ADR-063's user-facing audit envelope READ-surface to cross-host error surfacing. The four READ-side elements:

```json
{
  "envelope": { "package_type": "error", ... },
  "body": {
    /* Element 1: User-visible field set */
    "error_code": "ENVELOPE_MALFORMED | CAPABILITY_UNAVAILABLE | TOOL_FAILED | RATE_LIMITED | AUTH_REQUIRED | ...",
    "human_message": "Short human-readable description suitable for surfacing to the user",
    "retry_hint": "transient | needs_user_action | permanent",

    /* Element 2: Schema-validated at consumption — receiver verifies error envelope conforms to schema_version */

    /* Element 3: Safe-fallback — if envelope is malformed, receiver treats as error_code: ENVELOPE_MALFORMED instead of crashing */

    /* Element 4: JWT-bound access control */
    "audit_visible": true,
    "diagnostic": {
      /* Only populated/sent to receivers with matching JWT scope — full trace_id chain, stack snippet, internal IDs */
    }
  }
}
```

**Justification — three reasons**:
1. **Composes with #1017's audit_envelope hash strategy** — the error envelope shape IS a generalization. The audit case has a specific JWT scope and a specific diagnostic shape; the error case extends to all package types but keeps the four-element discipline.
2. **No silent failure cross-host** — without a canonical error envelope, every host invents its own error shape; receivers can't disambiguate "this tool doesn't exist" from "this tool exists but isn't available in your host" from "this tool failed transiently." `error_code` + `retry_hint` separate those clearly.
3. **JWT-bound diagnostic visibility** — same ADR-063 discipline. The user sees `human_message + error_code + retry_hint`; the auditor with the right JWT scope sees `diagnostic.*` too. Cross-host the JWT-binding has to be host-aware; receivers without the scope filter out `diagnostic` before surfacing.

**Open question 5 resolution**: Yes, the #1017 audit_envelope hash strategy carries over — the error envelope is the read-surface; the audit envelope is the write-surface with same JWT discipline. Confirmed.

### D5: Versioning = SemVer-flavored + Postel-ish forward compat

**Decision**: `schema_version` follows `MAJOR.MINOR.PATCH` SemVer convention with per-axis producer/consumer rules:

| Axis | Producer must | Consumer must |
|---|---|---|
| MAJOR | Bump on breaking changes (field removal, type change, required→optional flip on input side) | Reject same-MAJOR mismatch with `ENVELOPE_MALFORMED` error envelope |
| MINOR | Bump on additive changes (new optional fields, new enum values where unknown→default semantics hold) | Accept ANY same-MAJOR version; unknown fields outside `extensions.*` log a warning but do NOT break |
| PATCH | Bump on bug fixes (no schema change) | Accept silently |
| `extensions.*` | Add freely under namespace; never break compat | Silently ignore unknown namespaces |

**Justification — methodology-32 Postel discipline applied**:
- Producers are conservative: every additive change earns a MINOR bump; every breaking change earns a MAJOR bump and forces consumers to opt in
- Consumers are liberal: unknown fields in `extensions.*` are silently ignored; unknown fields outside `extensions.*` produce warnings (Pattern-073-style drift signal) but the receiver doesn't crash
- The MAJOR/MINOR distinction is the operational discipline that prevents stealth-breaking changes from sneaking through "additive" releases

**Trade-off acknowledged**: Schema-version coordination across plugin deploys creates a small operational cost (the plugin's `config` must declare `format_versions_emitted` + `format_versions_accepted`; doc-sync-sweep catches drift). This is captured under §Consequences/Negative.

### D6: Plugin packaging — context-package format declared in `config`; source-of-truth is the schema spec file

**Decision**: The plugin (`config + CLAUDE.md + skills + MCP server` per PM's 2026-06-01 clarification) carries the context-package format declaration in `config`, but the **source-of-truth** is a separate schema spec file referenced by both `config` and the `MCP server` implementation.

```yaml
# plugin/config (excerpt)
context_package_format:
  spec: "schemas/context-package-1.0.0.json"   # source of truth
  versions_emitted: ["1.0.0"]
  versions_accepted: ["1.0.0", "0.9.x"]        # backward compat range
  extensions_namespace: "vendor.piper-morgan"
```

```markdown
<!-- plugin/CLAUDE.md (excerpt) -->
## Context Package Format

This plugin emits and accepts context packages per ADR-065
(`docs/internal/architecture/current/adrs/adr-065-canonical-context-package-format.md`).
The canonical schema is at `plugin/schemas/context-package-1.0.0.json`.
See ADR-065 §Decision D2 for envelope/body/extensions structure.
```

```python
# plugin/mcp_server/serializer.py (excerpt)
SCHEMA_SPEC_PATH = "schemas/context-package-1.0.0.json"  # MUST match config
```

**Justification — Pattern-073 drift discipline**:
- One source of truth = the schema spec file. Two consumers reference it (`config` declares the version; `MCP server` implements against it).
- Doc-sync-sweep discipline catches the drift case where `config` claims version `1.0.0` but `MCP server` is built against `0.9.x` — same as the documentation-asserted-behavior pattern that surfaced 9+ times in Pattern-073.
- `CLAUDE.md` is human-facing; it doesn't carry version strings (that would be a third drift point). It points at the schema spec file by path.
- `skills` reference the format by name when they emit/consume packages (e.g., a skill that emits an `audit_event` package); they don't carry version strings either.

**Open question 3 resolution**: spec file is source of truth; `config` declares versions; `MCP server` implements; `CLAUDE.md` describes by reference; `skills` reference by name. Doc-sync-sweep catches drift. Confirmed.

---

## Consequences

### Positive

- **Cross-host serialization without per-host bespoke code** — the envelope+body+extensions shape (D2) is the same across Claude Desktop, ChatGPT, Slack, bespoke UI, and sibling-project receivers. Hosts deserialize via standard JSON tooling; the package-type discrimination on `envelope.package_type` (D2) routes to the right body schema.
- **Klatch-style sibling-project interop has a stable target** — Klatch (or any future sibling project) can implement an ADR-065-conformant emitter/receiver to interoperate with Piper Morgan without bilateral integration code. The Klatch L1-L5 layer model (deferred to §Evolution per Pattern-064 convention when Daedalus relays it) maps cleanly to envelope/body/extensions; D2 absorbs the alignment when it arrives.
- **Forward compat per methodology-32 Postel keeps existing surfaces alive** — the MAJOR/MINOR/PATCH versioning (D5) + `extensions.*` namespace (D2) lets the format evolve through additive changes without breaking deployed receivers. Producers are conservative (every change earns the right SemVer axis bump); consumers are liberal (unknown extensions silently ignored).
- **Audit envelope composability — ADR-063 four-element principle extends cross-host** — the error envelope (D4) generalizes ADR-063's READ-side principle. The audit envelope (write-surface, ADR-063) and error envelope (read-surface, ADR-065 D4) share the same four-element discipline + JWT-binding for `diagnostic.*` visibility. `audit_event` package_type's body shape IS the ADR-063 envelope (D2 composition note).
- **Capability primitive resolves a #1158-class failure mode at the format layer** — the verb-enum + `surface_type` slot shape (D3) prevents the verb-object name collapsing that #1158 surfaced in the action-classifier. Same architectural shape resolves the same shape of bug at the BYOC boundary; the layer-then-migrate ruling (2026-06-06 ADR-060 amendment) inherits naturally if BYOC ever absorbs an existing capability registry.
- **Pattern-072's 7th application surfaces from this ADR** — the capability primitive is the 7th catalog application (after task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, action VERB enum [6th, 2026-06-06], capability primitive [7th]). Catalog awareness flagged to CIO at next cron-shape findings memo (~Jun 13); non-gating.
- **Pattern-073 drift discipline applied to plugin packaging** — D6's "schema spec file is source of truth; `config` and `MCP server` both reference; doc-sync-sweep catches drift" is the same disciplined-pattern that surfaced as Pattern-073 9+ times. Doc-asserted-behavior drift is prevented by one-source-of-truth + sync-sweep at the packaging layer, not at runtime.

### Negative / Tradeoffs

- **JSON's representation limits** — binary primitives (images, audio, large blobs) cannot live inline; they are carried by reference (URI / content-addressable hash) in the body. Acceptable: every plausible host has the same constraint at the wire layer, and reference-by-hash is the existing pattern for large-blob content.
- **Schema-version coordination across plugin deploys creates a small operational discipline cost** — the plugin's `config` must declare `format_versions_emitted` + `format_versions_accepted` accurately; `MCP server` must implement against the schema spec file accurately; `CLAUDE.md` must point at the right spec file. Doc-sync-sweep (Pattern-073 discipline) is the mitigation, but it's a discipline cost not zero overhead.
- **Klatch alignment may arrive late and require Evolution-section absorption** — acceptable per Pattern-064 convention; the ADR ships without blocking on Klatch. Risk: if Daedalus relays substantive disagreement on D1/D2/D3 (the load-bearing shape decisions), absorption may require MAJOR-version bump rather than additive fold. Backstop: HOST will broker the alignment conversation at Klatch resumption.
- **Capability claim semantics are conditional, not boolean** — D3's `claim: available | conditionally_available | unavailable` puts evaluation work on the receiver. This is the correct semantic (EC-2 ruling) but adds receiver-side complexity vs. a simple boolean claim. Receivers must implement `conditions` predicate evaluation; SDK helpers will mitigate (Q7 ADR-066 packaging-layer abstraction).

### Non-consequences

- **This ADR does NOT decide the wire transport** (HTTP, WebSocket, MCP stdio — all separable from format choice; D1 wire format is JSON-encoded text, transport-agnostic; current binding is MCP stdio per Q7 ADR-066 packaging-layer concerns)
- **This ADR does NOT decide the audit semantics question** (cross-host unified vs per-host) — PDR-005 §Open question 1 carries that, deferred to follow-up ADR
- **This ADR does NOT specify per-platform persona-template content** — that's PDR-006 (post-1.0, per PDR-005 §Open question 5)
- **This ADR does NOT specify the concrete `context-package-1.0.0.json` schema file** — that's a follow-up artifact (Q1 open question); this ADR specifies the structure (D1-D6) the schema file must encode
- **This ADR does NOT decide the per-host capability-claim map content** — Q7 ADR-066 carries the map; this ADR provides the primitive (D3) the map is built from

---

## Evolution

(Empty at v0.1 filing. Klatch-pause framing per Pattern-064 convention: when Klatch resumes and Daedalus relays refinements via Janus, fold into this section as dated entry.)

---

## Open questions (v0.1)

1. **Specific JSON schema** — concrete `context-package-1.0.0.json` schema file to be drafted as a follow-up artifact; this ADR specifies the structure (D1-D6); Lead Dev review at schema draft.
2. **Klatch L1-L5 mapping** — pending Klatch resumption; if/when Daedalus relays the layer-model alignment, folds into §Evolution per Pattern-064 convention.
3. **Plugin vs MCP-server separation of concerns for format declaration** — **RESOLVED in D6**: spec file is the source of truth; `config` declares versions; `MCP server` implements against the spec; `CLAUDE.md` describes by reference; `skills` reference by name. Doc-sync-sweep catches drift (Pattern-073 layer).
4. **Capability-advertisement registry name + Pattern-072 application count** — **RESOLVED**: this is Pattern-072's **7th** application (after the 6th confirmed by 2026-06-06 ADR-060 amendment ratification: VERB enum). Capability primitive becomes the 7th: typed enum + documented consumers + register-time validation + default policy. **Flagging to CIO** for catalog awareness (non-gating) at the cron-shape findings memo (~Jun 13).
5. **Error envelope cross-host semantics — does the #1017 audit_envelope hash strategy carry over?** — **RESOLVED in D4**: Yes. Error envelope is the read-surface; audit envelope is the write-surface with the same JWT-binding discipline. Cross-host the JWT scope filters `diagnostic.*` from `human_message + error_code + retry_hint`.
6. **(NEW)** **Wire-transport binding** — current binding is MCP stdio; if/when WebSocket or HTTP bindings are added (BYOC second wave), does the format need transport-specific framing? **Lean**: no, JSON-encoded text is transport-agnostic; framing is the transport's concern. Confirm at Q7 (ADR-066) packaging-layer abstraction. Cross-reference noted.
7. **(NEW)** **Schema spec file location + versioning** — should the schema spec live in the plugin repo (per D6) or in a separate cross-project schema repo (sibling-shaped with Klatch's potential spec)? **Lean**: plugin repo for v1.0; reconsider at v2.0 if cross-project alignment makes a shared repo attractive. Filed as forward-look.

---

## What this ADR is NOT

- Not the plugin's full structure (that's the plugin-packaging ADR — Q7 / ADR-066)
- Not the Klatch alignment outcome (that lives in §Evolution when it arrives)
- Not the per-host capability-claim map (Q7 carries that, gated by this ADR's capability-advertisement primitive)
- Not the wire transport choice (that's separable; MCP stdio is the current binding)
