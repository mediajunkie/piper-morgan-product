# PDR Scoping Outline: Bring Your Own Chat (BYOC) Distribution Model

**Author**: PPM
**Date**: 2026-04-26
**Status**: Scoping outline — not the PDR itself; structures the work needed to produce it
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3 — "the most consequential strategic decision since ADR-060 lacks formal PDR treatment"
**Distribution intent**: PA + Architect + CXO + PM for input on scope and division of labor before drafting starts

---

## Why this PDR is needed

BYOC is currently embedded in Vision V2.3 (`docs/internal/planning/current/vision.md` §"Bring Your Own Chat" + Pillar 7 + Strategic Pivot). Vision adoption Apr 11 made it canonical strategic direction, but vision-level treatment doesn't substitute for PDR-level codification:

- Vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity.
- BYOC determines downstream product decisions in a way that other vision pillars don't currently determine — delivery surface, packaging, persona delivery, what "Piper" means to a user.
- ADR-level decisions (e.g., MCPB packaging, server architecture, persona portability) need a product anchor to refer back to. Without a PDR, those ADRs end up either (a) re-litigating product direction inside architecture decisions, or (b) accepting product direction implicitly without traceable rationale.
- Predecessor identified this as the most-flagged PPM carry-forward in their final handoff. Two PPM instances now agree it's overdue.

## What the PDR needs to answer

These are the decision-rule questions the PDR should resolve. Not all of these have one right answer — the PDR's job is to commit to specific rules so downstream work has constraints to design against.

### 1. The core decision rule

What is the binding product commitment? Candidate framings:

- **(a)** "Piper is delivered via the user's preferred MCP-compatible client; there is no Piper-specific UI in the v1.0 scope."
- **(b)** "Piper is primarily delivered via MCP; a thin web UI exists for Piper-specific functions that don't fit the chat client model."
- **(c)** "Piper is delivered via *any* surface that supports the protocol; client choice is user-driven and the server is invariant."

Vision V2.3 leans (c) but doesn't formally close (a)/(b). The PDR should pick.

### 2. Persona portability scope

Vision V2.3 says "the persona layer adapts per platform (Claude Project instructions, Custom GPT instructions, Gem instructions); the server stays the same." Open questions:

- What's the scope of "adapts" — variant prompt templates, or deeper persona divergence per platform?
- Who owns persona templates per platform? PPM? CXO? Distinct per-platform owners?
- What's the consistency contract — must a user feel "this is the same Piper" across clients, or is per-platform feel acceptable?

### 3. What's in scope for the MCP server vs. out of scope

The server holds: tools, context assembly, persistence, trust-graduated experience. The chat client holds: the LLM, the conversation surface, the user's history with that client. The boundary needs explicit decisions:

- Where does the conversation history live (client-side, server-side, both, neither)?
- What happens when the user switches clients mid-project — do they see the same artifacts? The same Piper-specific context?
- Does Piper-as-server attempt to remember the user's preferred client, or treat each connection independently?

### 4. The "no bespoke UI" commitment depth

The strongest version of BYOC says no bespoke web UI ever. The weakest says bespoke UI for things chat can't do. Specific test cases:

- Setup/onboarding: chat-only or wizard?
- Artifact browse/retrieve at scale: chat-only or list/grid UI?
- Trust-level configuration: chat-only or settings panel?
- Integration setup (GitHub PAT, Slack OAuth, Calendar OAuth): chat-only or web setup?

The PDR should resolve at least the "what about X" cases that have already been built differently than BYOC implies (e.g., the existing setup wizard).

### 5. The standards-evolution hedge

Vision V2.3: "Anchor on the model, not the standard. MCP is the current best expression of the thin-wrapper-to-API model, but standards evolve. Build the server cleanly enough that the packaging layer is swappable."

The PDR should commit to:
- A specific abstraction layer between Piper-server-logic and MCP-protocol-binding.
- A criterion for when to consider supporting a successor standard (and who decides).
- An acceptable per-platform variance budget (how different can Claude Desktop and ChatGPT Piper feel before we've broken the "same Piper" promise?).

### 6. The user-facing language commitment

"Bring Your Own Chat" is internal language; vision V2.3 calls it externally too but it's not user-facing copy. The PDR should commit to (or explicitly defer):

- How do we describe Piper to a new user in one sentence?
- How do we describe the Piper/client relationship in two sentences?
- What's the marketing-stable name for the model? (BYOC has the right shape but is jargon-y.)

This question is partially CXO/Comms territory; the PDR should at least name the decision and route it.

## Tier placement question (resolution needed before drafting)

Predecessor framed this as **PDR-005** alongside foundational PDRs 001–004. The PDR catalog README places "Integration Patterns" in the **2xx tier (reserved for future use)** — and BYOC is essentially the integration pattern with chat clients.

**Two cases**:

- **PDR-005 (Tier 0xx, Foundational)**: BYOC determines the delivery surface for everything Piper does — it shapes what "Piper" means to users at the most fundamental level. Foundational tier is the right home.
- **PDR-201 (Tier 2xx, Integration Patterns)**: BYOC is structurally an integration pattern (Piper integrating with chat clients via MCP) and the catalog reserves 2xx for exactly this class. Opening the 2xx tier with this PDR establishes the pattern.

**My PPM lean**: PDR-005 (Foundational). The "what Piper is" question is foundational; the "how Piper integrates with X" question is downstream of that. But this is genuinely 50/50 and the PM call.

## Suggested division of labor for drafting

Per the spec pipeline (CXO → PPM → Architect → Lead Dev) and the PDR template (Context → Decision → Consequences → Alternatives Considered):

| Section | Primary | Secondary input |
|---|---|---|
| **Context** (what's the product situation, why now) | PPM | PA (cross-pollination from Klatch/Janus on similar distribution patterns), Predecessor PPM handoff §1 |
| **Decision** (the binding product commitments) | PPM | PM ratification |
| **Consequences for product** (what we now must / can't do) | PPM | CXO (experience implications), PA (operational implications) |
| **Consequences for architecture** (what the server must support) | Architect | PPM frames product-side requirements |
| **Consequences for experience** (what users will feel) | CXO | PPM, PA |
| **Alternatives considered** (bespoke web UI, hybrid, native apps) | PPM | Architect (technical feasibility of each), Mobile-skunkworks-paused context |
| **Open questions deferred to follow-up PDRs** | PPM | All |

## Suggested sequence

1. **PM call on tier placement** (small, fast — 005 vs. 201). Unblocks naming.
2. **PA cross-pollination scan** — what have Klatch, Janus, Vergil, Piper Open done about similar BYOC-shape decisions? Predecessor's Apr 16 cross-pollination absorption discipline applies (principle-level convergence, not vocabulary-level import).
3. **Architect feasibility check** on the most ambitious version of BYOC (no bespoke UI, hot-swappable persona templates per client, swappable packaging layer). Identifies which PDR commitments would force expensive architectural changes.
4. **CXO experience review** on what users actually feel across Claude Desktop / ChatGPT / Gemini — is "same Piper" achievable, or do we have to commit to per-platform feel?
5. **PPM drafts PDR** incorporating inputs from steps 2–4. Distribution to leadership for review per the standard PDR cycle.
6. **PM ratifies** (or sends back for revision).

## What this scoping outline is *not*

- Not the PDR itself. Decisions in this document are PPM proposals or open questions, not commitments.
- Not a prescription for the engineering work. The "Consequences for architecture" section in the eventual PDR is Architect's territory.
- Not a request for immediate action — Phase E + #1002 + #1003 take precedence in the near term. This outline holds until that thread closes.

## Standing offer

If PA, Architect, CXO, or PM see scoping questions I've missed (or scoping questions that don't belong here), file a follow-up. The PDR's quality depends on the scoping work being honest about what it doesn't yet know.

---

*Scoping outline | PPM | 2026-04-26*
*Source: predecessor PPM handoff §1 + Agent 360 §8.3; Vision V2.3 §"Bring Your Own Chat" + Pillar 7 + Strategic Pivot; PDR catalog README*
