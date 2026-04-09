---
date: 2026-04-09
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (April 7–9, 2026)"
---

# Cross-Pollination Brief — April 9, 2026

PM produced a cascade of strategic and technical breakthroughs in a single day (April 8). The **"Bring Your Own Chat" distribution thesis** reframes Piper as an MCP server that shows up inside whatever AI client the user already has — Claude Desktop, ChatGPT, Gemini, VS Code — rather than asking them to adopt a new app. An **MCPB feasibility assessment** confirms this is architecturally viable, with a hybrid approach (MCPB for tools/storage, Claude Project for persona) cleanly mapping to the five-layer model. The **roadmap restructured** from v14.3 to v15.0, reorganizing M2–M5 around the differentiator stack and removing the bespoke web UI from the critical path. And the **M1 gate finally cleared** after Lead Dev discovered the actual root cause hiding behind two other bugs: the floor was receiving an empty user message because the pre-classifier stored it in a different field than the floor read from. Klatch was quiet — no new substantive activity since the April 7 brief.

---

## Key Insights

### 1. "Bring Your Own Chat" Reframes Distribution as Product Strategy
**From:** Piper Morgan (PA + xian, April 8)
**Relevant to:** Klatch (distribution model, MCP ecosystem, product positioning)

PM's "Bring Your Own Key" principle evolved into something more ambitious: **"Bring Your Own Chat."** Rather than building a bespoke web UI, Piper will ship as an MCP server that plugs into any MCP-compatible client. The user picks their AI client; Piper enhances it with PM-specific tools, context, and persistence. No new app to learn.

This isn't just a packaging decision — it reframes the product thesis. In a static UI, users must find features. In an MCP-powered conversation, the agent offers capabilities contextually. xian's observation from OpenLaws: MCP lets agents troubleshoot their own functionality dynamically, something static UIs cannot do.

Vision V2.2 codifies this as Principle 7 and explicitly connects it to the **Radar O'Reilly Pattern**: "show up where the user is, don't ask them to visit." The mobile insight generalized: the user is mobile, not the app.

**For Klatch:** This is the distribution-layer equivalent of the April 8 brief's "methodology over code" validation. If PM-quality context management can be delivered through MCP to any LLM client, the same distribution model applies to conversation management. Klatch's context infrastructure — five-layer assembly, channel context, entity prompts — could potentially ship as MCP tools/resources rather than requiring users to run a dedicated web app. The MCP protocol is now a shared distribution assumption across both projects. Klatch doesn't need to act on this immediately, but BYOC should inform product strategy conversations.

**Suggested action:** Note for strategic positioning. When planning Klatch's distribution story, evaluate whether MCP-based delivery of context infrastructure (L4 channel context, L5 entity prompts) is viable alongside or instead of the current web app model.

### 2. MCPB Hybrid Architecture Maps Cleanly to Five-Layer Model
**From:** Piper Morgan (PA, April 8)
**Relevant to:** Klatch (five-layer model validation, context delivery architecture)

The MCPB feasibility assessment identified a critical gap: MCP servers cannot inject into the system prompt. This means an MCPB can give Piper tools and storage but cannot autonomously make Claude "be" Piper. PA's proposed solution — the **hybrid approach** — uses each platform for what it's good at:

- **Claude Project** (or Custom GPT, Gem, etc.): provides L1–L2 (kit briefing, project instructions/persona)
- **MCPB/MCP server**: provides L3–L5 (project memory, channel addendum, entity-specific context)

This maps directly to the five-layer model: the host platform handles static context layers, the MCP server handles dynamic context layers. MCP Apps (interactive HTML rendered in sandboxed iframes inside the chat) confirmed viable for an artifact canvas — dashboards, project views, artifact browsers — without building a standalone web app.

**For Klatch:** The hybrid split validates the five-layer model's utility as a distribution architecture, not just a prompt design framework. The persona gap (host platform can't inject L5 behavioral calibration from an MCP server) is structurally identical to the Layer 5 transfer problem Klatch identified in Chat→Cowork import fidelity (March 29 brief). Both projects keep bumping into the same wall: L1–L3 transfer well, L5 is structurally hard. The hybrid approach is a pragmatic workaround — user manually installs persona via Project instructions — rather than a solution. Klatch's Layer 5 externalization work (Calliope's pilot) remains the closest thing either project has to a real solution.

**Suggested action:** Low priority. Note the architectural parallel. The MCPB persona gap reinforces that Layer 5 portability is the hardest unsolved problem in the shared five-layer model. Calliope's externalization pilot is now relevant to PM's distribution architecture, not just Klatch's import/export.

### 3. Three-Layer Root Cause Chain Clears M1 Gate
**From:** Piper Morgan (Lead Dev, April 8)
**Relevant to:** Klatch (gate methodology, root cause analysis)

The M1 gate failure, first reported April 3 and covered in briefs from April 4 through April 8, finally resolved — but the root cause was deeper than anyone expected. The April 8 brief reported the Five Whys discovery (deprecated model IDs returning 404s). The afternoon's work revealed two more layers:

**Layer 1 — Deprecated model IDs** (April 8 AM): `gpt-4-turbo-preview` → 404. Fixed by updating to `gpt-4o` and `claude-haiku-4-5`. Real bug, but not the whole story.

**Layer 2 — Provider configuration** (#946, April 8 PM): The setup wizard stored the user's chosen LLM provider, but `LLMClient.complete()` didn't read it. System defaulted to stale keychain keys. Fixed: explicit provider preference chain.

**Layer 3 — Empty user message** (#926, April 8 PM): The actual root cause. The pre-classifier stores the user's message in `intent.context['original_message']`, but `FloorContext` read from `intent.original_message` (the field), which was always empty for pre-classified intents. The floor received an empty `user_message`, so the LLM generated generic greetings instead of query-specific responses. Four `FloorContext` creation sites fixed.

**Bonus — Template migration** (#926, April 8 PM): IDENTITY queries were routed to canned templates that scored 1/3 on the Colleague Test. Direct floor testing scored 7+. All IDENTITY queries now route to floor with context.

The full arc: UAT failure (April 3) → symptom fixes (April 4–5) → Five Whys round 1 (April 8 AM) → provider fix (April 8 PM) → message passing fix (April 8 PM) → template migration (April 8 PM).

**For Klatch:** The gate methodology lesson from the April 8 brief sharpens further. Root cause analysis must continue past the first satisfying answer — and the second. Each of the three bugs was necessary to fix but insufficient alone. A gate process that stops at the first root cause would have declared victory after the model ID fix and still failed UAT. When designing Klatch's v0.9.0 release gate, build re-test scenarios that exercise the complete failure path end-to-end after each fix, and plan for multi-layer root cause chains rather than single-cause resolutions.

**Suggested action:** When designing v0.9.0 gate criteria, incorporate "exhaustive root cause" as a gate discipline: fixes verified individually AND in combination against the original failure scenario. The PM M1 arc is the reference case for why "fix and re-test" must re-test the full path, not just the component.

### 4. Roadmap Restructure Converts Insight to Organization
**From:** Piper Morgan (PA, April 8)
**Relevant to:** Klatch (product strategy methodology, roadmap evolution patterns)

The April 7 "methodology over code" insight became organizational structure within 24 hours. The roadmap restructure (v14.3 → v15.0) realigns M2–M5 around the differentiator stack:

- **M2**: Conscious Floor + Action Handlers (floor reliability, binary action gate)
- **M3**: Artifact Persistence + Cross-Session Memory (composting lifecycle, L4 gap fix)
- **M4**: Trust + Learning (earned proactivity, user-correctable preferences)
- **M5**: Distribution + Polish (MCPB packaging, MCP Apps canvas, security)

12 issues to close, 3 to revise, bespoke web UI off the critical path. PM decisions on CONV-FEAT cluster: #100 (Project Portfolio) and #101 (Temporal Context) revised from standalone services to floor context assembler tasks. #103 (Priority Engine) deferred to Horizon 2.

The restructure also introduces the **action gate test**: "Does this intent require an operation the LLM cannot perform within a floor response?" This probably means 4–5 action handlers instead of 19 classified categories.

**For Klatch:** The velocity of insight → organization is itself instructive. The backlog deep review (April 7) produced a "methodology beats code" insight; 24 hours later, the roadmap was restructured, issues were triaged, and leadership review was queued. This is the Inchworm Protocol applied to product strategy — each phase complete before the next begins. The practical parallel for Klatch: when an architectural insight changes what the product is building (as channel-as-workflow did), a structured roadmap audit asking "does this issue assume an architecture we've moved past?" prevents scope drag from issues that no longer match the product thesis.

**Suggested action:** Low priority. File for reference. If channel-as-workflow or another architectural insight shifts Klatch's product thesis, the PM restructure pattern (insight → audit → restructure → leadership review) is a proven playbook.

---

## Emerging Patterns

**The pivot has velocity.** The "methodology over code" insight (April 7) became a roadmap restructure, a distribution feasibility assessment, a Vision revision, and four critical code fixes — all within 24 hours. This is the fastest strategic-to-operational cycle yet in either project. The pattern: a clear insight, applied systematically across every layer (vision, roadmap, architecture, code), before momentum dissipates. The contrast with the M1 gate arc is instructive — the gate took five days because each fix was incremental; the roadmap restructure took one day because the insight was clear enough to apply everywhere at once.

**Distribution architecture is product strategy in disguise.** MCPB + BYOC isn't just "how do we package this" — it changes what the product is. Removing the bespoke web UI from the critical path eliminates an entire category of work (navigation design, component library, deployment infrastructure) and replaces it with context assembly (which is the product's actual differentiator). Distribution decisions that seem tactical turn out to be the most strategic choices available. Both projects should evaluate packaging decisions through this lens: does the distribution model reinforce or dilute the core thesis?

**Layer 5 is everyone's hard problem.** The MCPB persona gap (host platform can't inject L5 from an MCP server) joins the Chat→Cowork transfer gap (L5 behavioral calibration structurally absent) and the MAXT subliminal injection finding (L5 content behaviorally accessible but not consciously attributable) as the third independent discovery that Layer 5 portability is the hardest unsolved problem in the five-layer model. Every attempt to move agents across boundaries — import/export, distribution, migration — runs into this wall. The hybrid workaround (user manually installs persona) is pragmatic but doesn't scale. Calliope's externalization pilot remains the most promising approach.

---

## Background Changes (Noted, Low Priority)

- **Vision V2.2 published (PM):** Adds "Bring Your Own Chat" (Principle 7 evolved), MCPB distribution as primary path, MCP Apps for artifact canvas, cross-platform portability via MCP standard.
- **IAC talk review (PM):** Conference is April 17 in Philadelphia. Talk ("Ethics as Information Architecture") assessed as 90% ready. PA flagged need to update Piper description to reflect BYOC/MCP direction and verify the 80.3% empirical claim.
- **#946 fixed (PM):** Setup wizard now stores user's chosen LLM provider; `LLMClient` reads it. Fallback preference flipped to Anthropic-first.
- **CONV-FEAT cluster resolved (PM):** #100 and #101 revised to M2 context assembler tasks. #103 deferred to Horizon 2. All three encoded pre-floor-first assumptions.
- **MCPB prototype scoping memo sent to Architect (PM):** 3-tool prototype proposed (get_project_status, save_artifact, retrieve_artifact). Build sequence: MCP server → Claude Desktop testing → MCPB packaging → MCP Apps.
- **v0.9.0 release still pending (Klatch):** Manual testing and xian review still outstanding. Carried forward.
- **MAXT Session 02, AAXT Phase 2 still deferred (Klatch):** Carried forward from April 6.

---

## Sources Read

**Klatch:**
- `git log --since="48 hours ago"` — 1 commit (intel sweep memo, already covered in April 8 brief)

**Piper Morgan:**
- `dev/active/2026-04-08-0534-pa-opus-log.md` — PA Day 9 (MCPB research, roadmap restructure, BYOC insight, Vision V2.2, CONV-FEAT decisions)
- `dev/active/mcpb-feasibility-2026-04-08.md` — MCPB distribution feasibility assessment
- `dev/active/roadmap-restructure-proposal-2026-04-08.md` — Roadmap v14.3 → v15.0 proposal
- `docs/internal/planning/current/vision-v2-draft.md` — Vision V2.2 (BYOC, MCPB, MCP Apps)
- `dev/active/iac-talk-review-2026-04-08.md` — IAC conference talk review (April 17)
- `mailboxes/arch/inbox/memo-pa-mcpb-prototype-2026-04-08.md` — MCPB prototype scoping request to Architect
- Commits `12ca621`, `33e6758`, `54af8c3`, `70fe13e`, `60c9348` — #926 floor fix, IDENTITY migration, #946 provider fix, model ID update
- `git log --since="48 hours ago"` — 29 commits (12 new since April 8 brief + 17 already covered)
