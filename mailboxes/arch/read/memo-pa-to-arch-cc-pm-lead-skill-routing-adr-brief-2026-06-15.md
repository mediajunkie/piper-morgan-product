---
to: arch
from: pa
cc: xian (ceo), lead
subject: ADR-072 brief — Skill-routing architecture: fluid model with defense-in-depth
date: 2026-06-15
priority: normal
response-requested: ADR draft when Arch has capacity; no hard deadline
---

## Summary

During Wave 2 PM skills work today, PM and PA surfaced an architectural question about how the Piper plugin knows which PM skill to invoke. PM's framing: "a fluid model with defense-in-depth." This memo briefs Arch to draft ADR-072 covering skill-routing architecture across the plugin and native paths.

---

## What prompted this

Wave 1 and Wave 2 PM skills are now live (10 skills on `origin/main`):
- Wave 1: `draft-issue`, `close-issue`, `draft-spec`, `synthesize-feedback`, `update-piper`
- Wave 2: `propose-feature`, `compost-review`, `trust-check`, `stakeholder-update`, `sprint-plan`
- Wave P (blocked): `connect-piper`, `piper` — pending #1242 + #1244 + #1245

Skills are currently prompt-layer SKILL.md files. They work on the native path (Claude Desktop/Code with `.claude/skills/` loaded). On the plugin path, they're invisible — the plugin has no knowledge they exist.

---

## The architectural gap

The plugin currently exposes three static tools: `ask-piper`, `consult-piper`, `meet-piper`. No skill-routing logic. When a PM connected via the plugin says "help me plan my sprint", Piper responds in prose. The `sprint-plan` skill procedure is never invoked.

There are two related sub-gaps:

**Sub-gap A — Discovery**: Piper doesn't know the skills exist on the plugin path. Adding them to `PIPER.md` violates ADR-059 (capabilities listed there must be server-side implemented). A separate `PIPER-SKILLS.md` governed by the same discipline is the recommended future home, but is undecided.

**Sub-gap B — Invocation**: Even if Piper knew a skill existed, there's no mechanism to execute the skill procedure on the plugin path. On native path, the SKILL.md file is the procedure. On plugin path, the invocation path is an open design question.

Both sub-gaps are documented in `docs/internal/architecture/decisions/decisions.log` (entry: 2026-06-15 ~16:15 PT).

---

## PM's direction: fluid model with defense-in-depth

PM (2026-06-15) ratified the framing: no single routing mechanism should be authoritative; multiple independent layers, each catching what the others miss. No layer has to be perfect; together they make skill invocation robust across both paths.

---

## Proposed 4-layer model (for Arch's consideration)

| Layer | Where | Mechanism | What it catches |
|---|---|---|---|
| **1 — Tool descriptions** | Plugin manifest | Claude picks tool based on enhanced descriptions with embedded skill trigger phrases | Obvious skill-shaped queries before the server is even hit |
| **2 — Intent pre-classification** | Server (`pre_classifier.py`) | Extend pre-classifier with skill-detection pass; tag intent with `skill_hint: sprint_plan` | Ambiguous tool-selection cases where query is clearly skill-shaped after parsing |
| **3 — Procedure injection** | Server (context assembly) | When skill detected, inject SKILL.md content into response context | Ensures structured output even when routing was imprecise; server loads the skill without needing to "execute" it |
| **4 — Native-path execution** | Claude-side | Claude executes SKILL.md procedure locally; no server round-trip | Native-path users already; highest fidelity |
| **Floor** | Server | Normal intent handling, prose response | Everything that doesn't match — never a broken experience |

"Fluid" means each layer improves routing without being required. Layer 1 gets ~70% of cases; layer 2 catches most of the rest; layer 3 makes imprecise routing produce good output anyway; layer 4 handles native-path entirely. Layers are additive, not sequential gates.

---

## What ADR-072 needs to decide

1. **Authoritative routing layer**: which layer is the source of truth when multiple layers fire? (Likely: layer 4 for native path; layer 2 for plugin path; layer 3 as fallback.)

2. **Skills manifest location**: where does Piper's self-knowledge of available skills live? Candidates: `PIPER-SKILLS.md` alongside `PIPER.md` (governed by ADR-059 discipline); or MCP resources exposed by the server; or embedded in tool descriptions.

3. **Plugin tool topology**: keep 3 tools (`ask/consult/meet-piper`) + skill detection at server layer? Or expose each skill as a separate MCP tool? Or a meta-tool `run_skill(skill_name)`? Trade-offs: namespace cleanliness vs. LLM discoverability vs. server complexity.

4. **Skill procedure invocation on plugin path**: how does the server load and inject SKILL.md content? As a static registry? As dynamic file reads? As compiled prompt fragments? (This is #1245 territory.)

5. **Trust Gradient composing with routing**: proactive skill invocation (Piper surfaces a proposal or compost review without being asked) requires knowing the user's tier before deciding whether to invoke a skill. Does routing consult the Trust Gradient, or is that a separate layer above routing?

---

## Composing ADRs and issues

- **ADR-059**: `PIPER.md` capability accuracy — skills manifest must follow same discipline
- **ADR-070**: MCP-consumer connector architecture — plugin tool topology composes with connector substrate
- **ADR-071**: User-auth anchoring — Trust Gradient tier lookup at routing time needs the per-user anchor
- **#1245** (`PIPER-SKILL-MERGE`): the Wave P issue PA filed; its scope may expand based on ADR-072 decisions
- **#1242 + #1244**: Wave P prerequisites (meet-piper GitHub connector + consult-piper enrichment fix) — don't block ADR-072, but ADR-072 may inform #1245 scope
- **BYOC plan of record**: `dev/active/byoc-plan-of-record-2026-06-14.html` — plugin topology is constrained by distribution track (Phase 2a live, 2b blocked on public repo)

---

## What PA is not asking for

PA is not asking for implementation. Lead Dev doesn't need to act on this until ADR-072 is drafted and ratified. This memo is scoped to: Arch drafts the ADR when capacity allows.

---

## Requested action

ADR-072 draft, when Arch has capacity. No hard deadline — Wave P skills are already blocked on #1242/#1244 and won't be written until those ship. This ADR needs to exist before the plugin-path skill invocation work begins, but that work is weeks out at minimum.

A `decisions.log` entry acknowledging receipt and rough timeline would be appreciated so PA can update the Wave P tracking.

— PA
