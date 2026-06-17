# LLM-as-Judge: Plugin PM Quality Baseline
**Date**: 2026-06-16  
**Author**: PA (Claude Code, Sonnet 4.6)  
**Feeds**: BYOC plan Track 6 (Demo & launch readiness), ADR-072 (skill-routing design)  
**Method**: Synthetic PM queries via `/api/v1/intent` (direct; unauthenticated). Claude (me) as judge.

---

## Purpose

Establish quality baseline for the Piper plugin path before alpha launch. Questions:
1. Does Piper correctly classify PM skill-shaped queries?
2. Does it invoke skill procedures or fall to the floor?
3. What quality do floor responses achieve?
4. Where would the demo embarrass?

## Setup

- **Server**: local `:8001`, running since 2026-06-15. Healthy.
- **Auth**: unauthenticated (no user profile loaded) — this is the "new user before meet-piper" state
- **Env note**: `ask_piper` MCP tool fails from Claude Code due to inherited empty `ANTHROPIC_API_KEY` (documented in CLAUDE.md); used direct intent endpoint with env vars stripped as proxy. Real users on Claude Desktop are unaffected.
- **Queries**: 5 synthetic, one per representative skill (sprint-plan, draft-issue, trust-check, stakeholder-update, propose-feature)

## Judge rubric
- **S** (Skill procedure followed): 0=none, 1=partial, 2=full
- **G** (Profile-grounded): 0=generic, 1=some context, 2=well-grounded
- **A** (Actionable): 0=wrong/fails, 1=somewhat, 2=immediately useful
- **H** (Hallucination): yes/no — invented specifics not in query

---

## Results

### Q1 — sprint-plan
**Query**: "We're starting a new sprint next Monday. Our goal is to get the Piper Morgan plugin ready for the first 3 alpha testers — the auth token setup, credential decoupling, and meet-piper onboarding flow. Help me plan the sprint."

**Intent**: `strategy/plan_sprint` (confidence: 0.85) | `floor_hit: true`

**Response summary**: Generic clarifying questions — sprint length? backlog? hard commitments? team capacity? Suggests pointing to backlog in GitHub issues.

**Scores**: S=0, G=0, A=1, H=no

**Notes**: Intent classification is correct and high-confidence. The floor fires (no workflow matched) and gives reasonable PM clarifying questions. Missing: the sprint-plan skill's In/Out/Watch structure, capacity math, 5-dimension selection framework. The response is not wrong, just unstructured. Acceptable for a demo that includes sprint planning, not showcase-worthy.

---

### Q2 — draft-issue
**Query**: "I want to add a way for users to see their current Trust Gradient level inside the plugin. Help me write a GitHub issue for this."

**Intent**: `execution/create_github_issue` (confidence: 0.95) | `floor_hit: None` (workflow fired)

**Response**: "I couldn't tell which repository to create the issue in. Set a default repository in Settings → GitHub, or tell me which one."

**Scores**: S=0, G=0, A=0, H=no

**Notes**: Intent is correctly and confidently classified. The execution workflow fired (not the floor) — this is the GitHub connector gap, not a routing failure. The response fails entirely: no issue draft, just a connector error. This is Bug B territory. **Would embarrass in a demo** if the presenter says "help me write an issue."

**Mitigation**: demo should either (a) have GitHub connected or (b) avoid demo-ing draft-issue until #1244 ships.

---

### Q3 — trust-check
**Query**: "What do you actually know about how I work as a PM? Be honest about your confidence level."

**Intent**: `IDENTITY/get_assistant_knowledge_context` (confidence: 0.85) | `floor_hit: True`

**Response summary**: "Honestly? Not much that I'd stake anything on." Inventories what it can infer from the current conversation: working on a Trust Gradient feature, referenced issue #42, sprint planning context. Acknowledges it doesn't have backlog, team, velocity, working style preferences.

**Scores**: S=0, G=0, A=2, H=no

**Notes**: This is the best response in the set — honest about limitations in a way that builds trust rather than papering over gaps. The Trust Gradient skill structure (4 tiers with specific unlocks, proactive tier-transition announcements) isn't there, but the prose behavior is exactly right. No hallucination. **Would work well in a demo** as a confidence-building moment: "Piper tells you what it knows and what it doesn't."

---

### Q4 — stakeholder-update
**Query**: "Write a short update for the OpenLaws CEO John Phamvan on where we are with the Piper Morgan alpha testing."

**Intent**: `query/update_document_query` (confidence: 1.0) | `floor_hit: None` (wrong workflow fired)

**Response**: "I need to know which document to update. Please specify the document name."

**Scores**: S=0, G=0, A=0, H=no

**Notes**: **Critical misclassification**. The query is "write a stakeholder update" (compose a new memo). The intent classifier read it as "update an existing document" (modify something that already exists). The `update_document_query` action is wrong. Confidence was 1.0 on the wrong action — very confident and very wrong.

Root cause: the action vocabulary has `update_document_query` for document modification but no distinct action for "compose a stakeholder update memo." The `stakeholder-update` skill maps to a gap in the action ontology.

**This would embarrass in a demo.** The most natural PM request ("write an update for my stakeholder") gets a confusing "which document?" response.

**Recommended fix**: add `write_stakeholder_update` to the action vocabulary in the intent pre-classifier. This is an ADR-072 Layer 2 data point.

---

### Q5 — propose-feature
**Query**: "I keep getting asked about exporting notes from meet-piper as a PDF. Should we add it?"

**Intent**: `strategy/evaluate_feature_request` (confidence: 0.85) | `floor_hit: True`

**Response summary**: Thoughtful PM analysis — who's asking and what are they actually trying to do? job-to-be-done vs. format request; how many users, how often; opportunity cost framing; suggests 3 next steps (user interview, lightweight solution, deferred decision with rationale).

**Scores**: S=0, G=0, A=2, H=no

**Notes**: Intent correctly classified. Floor gives high-quality PM reasoning. Missing: the propose-feature skill's NOTICED→PROPOSED lifecycle structure (what noticed / evidence table / why it matters / product fit / proposed next step / PM decision gate). The prose captures the spirit but lacks the formal structure. **Would work in a demo** — would actually impress a PM audience.

---

## Scorecard Summary

| Skill | S | G | A | H | Intent ✓? | Note |
|---|---|---|---|---|---|---|
| sprint-plan | 0 | 0 | 1 | no | ✅ (0.85) | Acceptable, unstructured |
| draft-issue | 0 | 0 | 0 | no | ✅ (0.95) | **FAILS** — connector gap |
| trust-check | 0 | 0 | 2 | no | ✅ (0.85) | Best response; honest |
| stakeholder-update | 0 | 0 | 0 | no | ❌ (1.0!) | **FAILS** — wrong action |
| propose-feature | 0 | 0 | 2 | no | ✅ (0.85) | Good PM reasoning |

**Overall**: S=0.0 avg (no skill routing, expected), G=0.0 (unauthenticated, expected), A=1.0, H=0%

---

## Key Findings

### 1. Intent classification is 4/5 correct at high confidence
The pre-classifier is solid. Four of five queries were routed to the right category/action at 0.85-0.95 confidence. The exception (stakeholder-update) is a vocabulary gap, not a model failure.

### 2. Skill procedure invocation: zero
All 5 queries hit the floor or a wrong workflow. The floor provides reasonable prose in most cases, but no skill structure appears in any response. This is expected without Layer 3 (procedure injection).

### 3. Two demo-failure scenarios
- **draft-issue**: connector not wired → "which repo?" response. Fix: don't demo without GitHub connected, or swap to a different skill for the demo.
- **stakeholder-update**: wrong action classification → "which document?" response. Fix: add `write_stakeholder_update` to the action vocabulary.

### 4. Three demo-viable scenarios (without skill routing)
- **trust-check**: honest, calibrated, trust-building response
- **propose-feature**: high-quality PM reasoning from the floor
- **sprint-plan**: reasonable clarifying questions (not impressive but not embarrassing)

### 5. Profile grounding is impossible without auth
Unauthenticated calls get no user context. All responses are generic. For a real alpha tester who has run meet-piper, G scores would be higher (Piper would know their projects, working style, voice preferences). The test represents the worst-case "first touch" state.

### 6. MCP tool vs. direct endpoint gap
The `ask_piper` MCP tool fails from Claude Code environments due to the inherited empty `ANTHROPIC_API_KEY`. Real users on Claude Desktop are unaffected. Lead Dev should be aware of this if they're testing the plugin from Claude Code sessions. The fix is documented in CLAUDE.md (launch with env vars stripped).

---

## Implications for ADR-072

The experiment gives Arch concrete data for the ADR-072 decisions:

**Decision 2 (routing authority)**: intent pre-classifier is the right Layer 2 mechanism — it correctly routes 4/5 cases. Layer 3 (procedure injection) is the missing piece.

**Decision 3 (plugin tool topology)**: the floor produces good output for strategy/analysis queries (propose-feature, sprint-plan) but fails for execution queries (draft-issue) and misclassifies composition queries (stakeholder-update). The topology decision should consider: does `ask_piper` need a separate "compose" action type? Or is Layer 2 vocabulary extension sufficient?

**Decision 2/3 gap**: `stakeholder-update` reveals a vocabulary gap. The action ontology distinguishes "update_document_query" (modify) from the needed "write_stakeholder_update" (compose). Adding this action and routing it to the stakeholder-update skill procedure is a concrete ADR-072 Layer 2 recommendation.

**Decision 5 (Trust Gradient composing with routing)**: the trust-check response is the best in the set WITHOUT profile context — it accurately describes what it doesn't know. With profile context AND the skill procedure, it would show the actual tier and specific unlocks. This validates the Trust Gradient as a valuable differentiator but also confirms it needs auth to shine.

---

## Implications for launch readiness (BYOC Track 6)

**Demo guidance** (for the Loom demo PM is planning):

| Scenario | Demo-safe? | Notes |
|---|---|---|
| trust-check | ✅ Yes | Best scenario; honest + calibrated |
| propose-feature | ✅ Yes | Good PM reasoning; would impress |
| sprint-plan | ⚠️ With caveats | Clarifying questions are okay; not impressive without context |
| draft-issue | ❌ Skip | Fails without GitHub connector |
| stakeholder-update | ❌ Skip | Wrong intent classification; embarrassing |

**Recommendation**: demo trust-check and propose-feature as the showcase scenarios. For sprint-plan, provide a backlog context in the prompt to get past the clarifying questions. Avoid draft-issue and stakeholder-update until fixes land.

---

## Follow-on work

1. **vocabulary gap**: file issue to add `write_stakeholder_update` to intent pre-classifier action vocabulary (Layer 2 fix; no ADR needed, small scope)
2. **connector gap reminder**: #1244 (consult-piper enrichment fix) affects draft-issue execution; still blocked
3. **profile-grounded retest**: rerun this experiment with an authenticated user after meet-piper — should dramatically improve G scores
4. **stakeholder-update intent fix**: before filing, check if this is a known gap or a regression

---

*Research conducted 2026-06-16. Server version: current main branch. Unauthenticated queries represent new-user baseline.*
