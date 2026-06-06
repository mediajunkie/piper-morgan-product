# ADR-065: Canonical Context-Package Format (BYOC / Plugin-Packaged)

**Status**: DRAFT v0.1 (2026-06-06) — Architect-authored; companion to PDR-005 v1.0 §Open question 6; in-house material per Klatch-pause Evolution-section convention (HOST 2026-05-24)

**Date**: 2026-06-06

**Authors**: Chief Architect (Arch)

**Reviewers**: PPM (PDR-005 owner), Lead Dev (implementation lane), CIO (methodology), CEO (xian)

---

## Status

- **v0.1 DRAFT** filed 2026-06-06 in-house pending Klatch alignment (Klatch paused since May 20; Klatch refinements fold to §Evolution per Pattern-064 convention if/when alignment resumes)
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
- Pattern-072 (Registries that Grow into Architectural Shapes, Proven, 5+ applications) — likely shape for capability registry
- methodology-32 (Postel for Memo Headers) — Postel's-law discipline for forward compat
- methodology-38 (PDR/ADR Tier Separation, Emerging) — Q6 is the implementation-altitude ADR companion to PDR-005's decision-rule altitude

---

## Decision

[v0.1 SKELETON — to be filled in Fire 2 (next cycle pass)]

### D1: Wire format = JSON with explicit schema-version field

[Justification, alternatives considered (Protobuf / MessagePack / OpenAPI-flavored), and trade-offs]

### D2: Three layers per package — envelope + body + extensions

[Envelope carries provenance/version/timestamps; body carries the semantic payload; extensions carry namespaced opt-in fields]

### D3: Capability-advertisement primitive = typed enum + slot

[Per PDR-005 AC-1 + my June 3 EC-2 architectural input — capabilities are conditionally-claimed-per-host; the format carries the verb+slot shape rather than verb-object name collapsing; Pattern-072 applied at the capability registry layer]

### D4: Error envelope = ADR-063 READ-side principle extended cross-host

[Four READ-side elements adapted for cross-host error surfacing: user-visible field set / schema validation at consumption / safe-fallback / JWT-bound access control]

### D5: Versioning + Postel-ish forward compat

[Schema-version pinned per package; consumers must accept forward-compatible additions in `extensions` namespace; producers must not break backward compat without schema-version bump]

### D6: Plugin packaging — context-package format declared in `config`

[Plugin's `config` file declares the format-version this plugin emits/accepts; `CLAUDE.md` carries human-facing description; `skills` may reference the format; `MCP server` implements the format at the wire boundary]

---

## Consequences

[v0.1 SKELETON — to be filled in Fire 2]

### Positive

- Cross-host serialization works without per-host bespoke code
- Klatch-style sibling-project interop has a stable target to align against
- Forward compat per Postel keeps existing surfaces alive across format evolution
- Audit envelope composability — ADR-063's four-element principle extends naturally cross-host

### Negative / Tradeoffs

- Bound to JSON's representation limits (no binary primitives at the format layer; MIME-attached blobs via reference)
- Schema-version coordination across plugin deploys creates a small operational discipline cost
- Klatch alignment may arrive late and require Evolution-section absorption (acceptable per Pattern-064)

### Non-consequences

- This ADR does NOT decide the wire transport (HTTP, WebSocket, MCP stdio — all separable from format choice)
- This ADR does NOT decide the audit semantics question (cross-host unified vs per-host) — PDR-005 §Open question 1 carries that, deferred to follow-up ADR
- This ADR does NOT specify per-platform persona-template content — that's PDR-006 (post-1.0, per PDR-005 §Open question 5)

---

## Evolution

(Empty at v0.1 filing. Klatch-pause framing per Pattern-064 convention: when Klatch resumes and Daedalus relays refinements via Janus, fold into this section as dated entry.)

---

## Open questions (v0.1)

1. **Specific JSON schema** — to be drafted in Fire 2 + reviewed by Lead Dev
2. **Klatch L1-L5 mapping** — pending Klatch resumption
3. **Plugin vs MCP-server separation of concerns** for format declaration — does `config` declare it, does `MCP server` implement it, do both reference the canonical spec file? Initial lean: spec file is the source of truth; `config` and `MCP server` both reference; doc-sync-sweep discipline catches drift
4. **Capability-advertisement registry name** — is this Pattern-072's 6th application (after task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel, [now] capability)? Worth flagging to CIO
5. **Error envelope cross-host semantics** — does the same audit_envelope hash strategy from #1017 carry over? Lead Dev consultation

---

## What this ADR is NOT

- Not the plugin's full structure (that's the plugin-packaging ADR — Q7 / ADR-066)
- Not the Klatch alignment outcome (that lives in §Evolution when it arrives)
- Not the per-host capability-claim map (Q7 carries that, gated by this ADR's capability-advertisement primitive)
- Not the wire transport choice (that's separable; MCP stdio is the current binding)
