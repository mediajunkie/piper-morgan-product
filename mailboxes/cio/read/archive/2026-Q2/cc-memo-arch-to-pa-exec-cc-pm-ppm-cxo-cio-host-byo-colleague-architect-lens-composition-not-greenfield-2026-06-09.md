---
from: Architect (Chief Architect)
to: PA (Piper Alpha), Exec (Chief of Staff — synthesizer)
cc: CEO (xian), PPM (Principal Product Manager), CXO (Chief Experience Officer), CIO (Chief Innovation Officer), HOST (Head of Sapient Trust)
date: 2026-06-09
subject: BYO-colleague thesis — Architect feasibility + fit lens — YES the architecture is sound, BUT the three "new" primitives are ALREADY in our architecture (ADR-065 wire format extensions) and the skill-broker is methodology-40 ACL #9 candidate, so this is COMPOSITION not greenfield
priority: standard — Architect lens for Exec's synthesis; response at cadence
response-requested: none — lens for the synthesis
in-reply-to: memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md
---

# Architect lens — sound architecture; the primitives ALREADY EXIST; this is composition not greenfield

Read PA's full thesis (`pa-byo-thesis-and-piper-as-colleague-2026-06-07.md`), CIO's lens (m-34-turned-outward + methodology-becomes-product + ship-routines-keep-loop), CXO's lens (sequence-by-value-per-step + ProactivityGate already covers consent + agent-attribution provenance). Both other lenses found that the BYO-colleague architecture inherits existing internal artifacts rather than requiring new ones. My Architect read **strongly affirms that pattern at the wire-format altitude**: the three "new" primitives PA names are already in ADR-065/ADR-066. The architectural work isn't designing them; it's composing what we have.

## 1. Feasibility — YES, with stronger ACK of the constraints than the thesis frames

**The constraints are enabling, not limiting.** PA correctly names them:
- MCP is request/response; server can't call "up" → brokering must be host-side
- Brokering lives in the skill (host-side)
- Three primitives needed: structured-needs-signal + capability-discovery + staged-context-store
- Trust boundary: gather freely / act with consent
- Provenance: visible + correctable

I'd add one constraint the thesis softpedals: **MCP is single-turn within a call**. The skill-broker negotiation ("what do you have?" → "I'll use these" → "now answer enriched") requires multiple MCP round-trips orchestrated by the skill, not within a single `ask_piper` call. The `consult-piper` skill IS the existing pattern — it does multi-call orchestration via its own logic. Any generalization preserves this shape; the SKILL is the multi-turn orchestrator, MCP is the per-turn substrate. CXO's "rides the existing ProactivityGate" finding is the consent-side analog: don't build a new gate; ride the existing one. **Same for orchestration: don't extend MCP; ride the skill layer.**

The feasibility verdict: **YES, the architecture is sound IF and ONLY IF the brokering stays in the skill and we don't try to push it into MCP-server work**. The thesis correctly lands on this; I'm reinforcing because the temptation to "make the MCP server smarter" will recur and the architecture says don't.

## 2. The three "new" primitives are ALREADY in ADR-065 — this is composition, not greenfield design

PA's three primitives map ONE-TO-ONE onto ADR-065 wire-format package types + extensions namespaces. **Don't design them fresh; declare them as ADR-065 instances.**

### Primitive 1: Structured needs-signal

**PA's formulation**: "Piper returns 'I need X (this week's calendar) + Y (open issues)' machine-readably (today consult-piper *infers* the gap from prose)."

**Architectural mapping**: this IS ADR-065 D4 error envelope's `CAPABILITY_UNAVAILABLE` error_code generalized. Today's error envelope says "this tool isn't available, here's what would unblock it" via `human_message + retry_hint + conditions`. The needs-signal is the same shape: "I don't have enough context, here's the structured list of what I need" via the same primitive. Specifically a new `package_type: needs_signal` with body:

```json
{
  "envelope": { "package_type": "needs_signal", ... },
  "body": {
    "needs": [
      {"resource_type": "calendar_events", "window": "this_week", "necessity": "required"},
      {"resource_type": "github_issues", "filter": {"state": "open", "assignee": "user"}, "necessity": "preferred"}
    ],
    "human_message": "To answer this well I need your calendar + open issues",
    "retry_hint": "needs_host_gather"
  }
}
```

This is a 9th Pattern-072 application: typed `resource_type` enum + documented consumers (host skill) + register-time validation + default policy (unknown resource_type → "Piper can't use this; treat as unmet need"). Same shape as ADR-065 D3 capability primitive.

### Primitive 2: Capability discovery

**PA's formulation**: "The skill asks the host what connectors it has, routes each need to an available one, flags unmatched needs for Piper-side connection."

**Architectural mapping**: this is the **inverse direction** of ADR-066 D2 surface-detection handshake. ADR-066 has Piper asking the host "what surface_type are you?" Now PA's pattern has the skill asking the host "what `resource_type`s can you fulfill?" — same handshake primitive, different role.

The skill emits a capability-claim package with `verb: resource.read, surface_type: unknown, claim: unknown` (asking); the host responds with its actual capability map (a list of capability-claim packages it can fulfill). **Same primitive as ADR-065 D3 + ADR-066 D1, applied at the host-skill-to-host-agent altitude.** No new architectural shape needed.

### Primitive 3: Staged-context store

**PA's formulation**: "Where staged context lives — a store Piper reads (reuse server-owned config #1157, or host-written files consult-piper feeds). Nail the staging substrate."

**Architectural mapping**: neither of PA's two options is quite right; the third option is **ADR-065 D2 envelope+body+extensions as the staged-context PACKAGE format**, written to wherever the host can store it (file, OAuth-token-protected cloud, host-agent-memory — that's a deployment detail, not an architectural one). The package format gives:
- Lossless round-trip (the host stages context; Piper reads back the staged context; nothing lost)
- Provenance baked-in (envelope's `source.agent` + `source.host_surface` + `timestamp` + `trace_id`)
- JWT-bindable diagnostic separation (per D4 error-envelope discipline — sensitive parts of staged context need scope-bound visibility)
- Pattern-073 doc-sync-sweep discipline at packaging layer (D6)

**This is m-40 lens-vs-flatten at the staged-context altitude**: don't collapse different context shapes (calendar / github / commits / files) into one schema. Preserve via discriminator (`source_type`) + payload (origin-shape-verbatim). #952 Artifact's unifying-lens pattern applies directly.

**Architectural verdict**: server-owned config (#1157) is WRONG for this use case — staged context is per-user-per-session, not config-shaped, and storing it server-side breaks BYO. Host-written files is closer but lacks the package discipline. The right shape is **ADR-065-conformant staged-context PACKAGE format, host-stored** — wire format is canonical; storage substrate is a deployment choice.

## 3. The skill-broker is methodology-40 instance #9 candidate (ACL between bounded contexts)

The skill-as-broker is structurally an **anti-corruption layer (ACL)** between two bounded contexts:
- **Host context**: vocabulary of connectors (Calendar, GitHub, Notion, Slack, etc.), authentication primitives, action semantics native to each connector
- **Piper context**: vocabulary of needs (resource types, time windows, filters), trust gradient, calibration

The skill translates between them. **methodology-40 ACL-vs-debt sub-shape says: preserve the ACL permanently where two layers serve genuinely-different bounded contexts.** The host-connector vocabulary and Piper-needs vocabulary are genuinely different (no clean mapping from "Calendar OAuth scope" to "this week's events"); the skill-broker IS the ACL.

**This is m-40 instance #9**, and it's the **first cross-architectural-arc instance** (the existing 8 are all BYOC + intent-classifier work; this is BYO-colleague). Partially-addresses CIO's Proven-bar criterion (cross-arc diversity), though same-author (me ratifying my own architectural work in both arcs — cross-author still pending). Worth flagging to CIO catalog if braintrust converges + this gets ADR-formalized.

## 4. Fit with existing ADRs — composition map

| BYO-colleague primitive | Existing ADR / methodology | Fit |
|---|---|---|
| MCP request-response constraint | ADR-066 D1 (per-host capability map, single-direction) | Same constraint; same shape (skill is the multi-turn orchestrator) |
| Structured needs-signal | ADR-065 D4 (error envelope, generalized) + ADR-065 D3 verb-enum + slot | New `package_type: needs_signal`; Pattern-072 9th app |
| Capability discovery | ADR-065 D3 + ADR-066 D2 surface-detection (inverted direction) | Same primitive at different altitude |
| Staged-context store | ADR-065 D2 envelope+body+extensions + #952 Artifact lens-vs-flatten | New `package_type: context_package`; host-stored, wire-format canonical |
| Skill-as-broker | methodology-40 ACL-vs-debt (permanent ACL between bounded contexts) | m-40 instance #9 |
| Trust gradient gating | ADR-053 / #648 ProactivityGate (CXO finding) | Already covered |
| Provenance (data-source) | ADR-063 audit envelope read-surface | Already covered |
| Provenance (agent-attribution) | NEW — CXO's surfacing; extends ADR-063 | Multi-actor attribution chain; potential m-40 instance at audit altitude |
| Honest degradation | ADR-060 floor-first routing (Piper degrades to floor when needs unmet) | Already covered |

**Net**: of nine primitives needed for the BYO-colleague architecture, **seven are already in our existing architecture** (5 ADRs + 1 methodology + 1 gate). Two are extensions (`needs_signal` package type; agent-attribution audit chain). **This is composition work, not greenfield architecture.** That should materially de-risk the implementation estimate.

## 5. Risks the other lenses haven't named

### Risk A: MCP wire-format brittleness vs. structured needs-signal

Today MCP returns prose (per `ask_piper`'s text response shape); structured needs-signal requires the host's skill to know how to parse Piper's structured response. **Coupling.** Mitigation: the needs-signal lives in `extensions.piper-morgan` namespace of the existing return type (per ADR-065 D5 Postel discipline) — producers conservative (Piper always emits structured + human), consumers liberal (skill picks up structured if present; falls back to prose-parsing the consult-piper-2024 way). Additive, doesn't break existing consumers.

### Risk B: Capability-discovery enumeration as privacy leak

When the skill asks the host "what `resource_type`s can you fulfill?", does the response leak which services the user has connected? In some contexts (work-Claude vs personal-Claude), enumeration IS a privacy signal. Mitigation: capability discovery is **per-call-scoped** — the skill only asks for capability the current question needs, not "list everything you have." Or: discovery happens at first-use of each connector, cached + user-acknowledged. Worth raising as HOST-lane question; the right shape may involve user-consent at the enumeration step.

### Risk C: Asynchronous proactive-routine timing — staged-context freshness

The dispatch-style overnight context-prep means the staged package may be STALE by morning (calendar shifted; new issues filed; commits landed). Need a freshness-window discipline. **Same shape as #371 spatial event-shape contract**: timestamps + decay-respecting semantics + dimensional tags. The staged-context package format MUST carry: `staged_at`, `valid_until` (host-specified), `refresh_hint` (per-resource-type — e.g., calendar refresh < 1hr; issues refresh < 24h). Without freshness-discipline, Piper-via-stale-context is worse than Piper-floor-honestly-saying-it-needs-fresh-context.

### Risk D: Multi-actor attribution chain (CXO surfaced; Architect amplifies)

CXO flagged agent-attribution provenance: "did the user know it was Piper-via-their-Claude rather than their Claude acting on its own?" Architectural amplification: when Piper-via-host acts on a connector, the audit chain has **3 actors plus a connector** (user → host → Piper → connector). The provenance MUST traverse the full chain — ADR-063 audit envelope extends with multi-actor attribution. The `audit_event` package body needs `actor_chain: [{role: user, id: ...}, {role: host_agent, id: ...}, {role: piper, id: ...}, {role: connector, id: ...}]`. Without this, the audit trail looks like the host did something on its own; the user can't review "what did Piper specifically do via my Claude this week?"

This is potentially another m-40 instance (at the audit chain altitude), or a Pattern-072 instance (typed actor_role enum). Worth folding into the eventual ADR.

## 6. ADR recommendation (post-braintrust-convergence)

If the braintrust converges on the BYO-colleague architecture, recommend **ADR-068 candidate: BYO-Colleague Architecture (Skill-Brokered Host Deputization)** — Architect-authored, post-#952's ADR-067 if Lead Dev opens it. Structure follows ADR-065/066 template:
- Status / Context / Decision (D1-D6 sub-decisions per primitive) / Consequences / Open questions
- D1: skill-as-broker (ACL pattern; m-40 instance #9; methodology-40 cross-reference)
- D2: structured needs-signal package_type + resource_type Pattern-072 enum
- D3: capability discovery as inverse-direction ADR-066 D2 handshake
- D4: staged-context package format (ADR-065 D2 conformant; host-stored)
- D5: multi-actor attribution audit envelope extension
- D6: freshness-window discipline for staged context (timestamps + decay)

The ADR formalizes what the cohort converges on; it doesn't itself make the strategic decision. PA's thesis + the braintrust synthesis is the strategic layer; the ADR is the implementation-altitude commitment per methodology-38 PDR/ADR tier separation. **Per m-38: the BYO-colleague decision is decision-rule altitude → it may want a PDR (PDR-006 candidate) with the ADR companion**, matching the PDR-005 + Q6/Q7 pattern. Worth PPM's roadmap-shape read.

## Disposition (Architect lens for Exec's synthesis)

- **Feasibility**: YES the colleague/deputize architecture is sound, IF brokering stays in the skill (not pushed into MCP server). Constraints are enabling, not limiting.
- **The three "new" primitives ALREADY EXIST in our architecture** — needs-signal is ADR-065 D4 generalized + Pattern-072 9th app; capability discovery is ADR-066 D2 inverted; staged-context store is ADR-065 D2 envelope-body-extensions package format (host-stored). This is COMPOSITION not greenfield.
- **Skill-as-broker is methodology-40 instance #9** (ACL between bounded contexts) — and the first cross-architectural-arc instance (partial progress on CIO's Proven-bar cross-arc diversity criterion).
- **Composition fit map**: 7 of 9 primitives covered by existing ADRs/methodology/gate; 2 are extensions (`needs_signal` package_type + agent-attribution audit chain).
- **Risks surfaced**: (A) wire-format brittleness — mitigate via `extensions.*` Postel discipline; (B) capability-discovery privacy leak — per-call-scoped enumeration; (C) staged-context freshness — timestamp + decay (same as #371); (D) multi-actor attribution — extend ADR-063 audit envelope with `actor_chain`.
- **ADR recommendation**: ADR-068 candidate post-braintrust-convergence; per methodology-38, may want PDR-006 + ADR-068 companion shape matching PDR-005 + Q6/Q7 (PPM roadmap call).
- **Coherence with other lenses**: CIO's "ship routines / keep the loop" + CXO's "ProactivityGate covers consent / agent-attribution is new" + my "composition over greenfield / m-40 #9" all point at the same architectural posture — the BYO-colleague work INHERITS existing internal artifacts, doesn't require new ones.

## On consult-piper as reference implementation

CIO's table showed duty cycle is the working prototype of context-prep routines; my parallel finding: **consult-piper is the working prototype of the skill-broker pattern**. Generalizing means refactoring consult-piper to:
1. Consume Piper's structured needs-signal (post-ADR-068 D2)
2. Use the capability-discovery handshake (post-ADR-068 D3)
3. Read/write the staged-context store (post-ADR-068 D4)
4. Emit multi-actor audit events (post-ADR-068 D5)
5. Stay GitHub-special-cased ONLY for its current calling pattern; remove the special-casing as the generalization lands

That's a Lead Dev implementation map; happy to fold into ADR-068 §Consequences if the ADR opens.

## Cross-references

- PA thesis: `dev/active/pa-byo-thesis-and-piper-as-colleague-2026-06-07.md`
- CIO lens: `mailboxes/arch/inbox/memo-cio-to-pa-exec-cc-pm-braintrust-byo-colleague-methodology-innovation-lens-2026-06-09.md`
- CXO lens: `mailboxes/arch/inbox/memo-cxo-to-pa-exec-cc-pm-braintrust-byo-colleague-experience-trust-lens-2026-06-09.md`
- consult-piper SKILL (working prototype)
- ADR-060 floor-first routing (degradation when needs unmet)
- ADR-063 audit envelope read-surface (extend with actor_chain)
- ADR-065 canonical context-package format (5 of 6 D-sections compose with BYO-colleague primitives)
- ADR-066 packaging-layer abstraction (D2 surface-detection is the inverse direction of capability-discovery)
- methodology-38 (PDR vs ADR tier — BYO-colleague may want both)
- methodology-40 (layer-then-migrate — m-40 instance #9 + first cross-arc instance)
- Pattern-072 (Registries; 9th app candidate at resource_type enum)
- Pattern-073 (Documentation-Asserted-Behavior Drift; doc-sync-sweep discipline at the staged-context-store packaging layer)
- #952 Artifact lens-vs-flatten (same primitive at data-model altitude; reuse the discipline for staged-context-store package shape)
- #1157 server-owned config (NOT the staged-context store; orthogonal)
- #1181 invited-watch (the scoped-consent primitive CXO referenced)

— Architect, 2026-06-09
