---
date: 2026-04-11
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (April 10–11, 2026)"
---

# Cross-Pollination Brief — April 11, 2026

Klatch shipped **v0.9.0** on the evening of April 10 — after a five-day gap, one hour of activation, full release delivered — and in the same session filed a future direction memo that sharpens Step 10 considerably: Klatch is not just building an export format, it is building a **context interchange protocol** that any MCP-capable client could call. Three signals converged to make this load-bearing rather than aspirational: Managed Agents launched, Anthropic centralized compaction, and xian's work across both projects this week pointed the same direction — "our products are services for agents to interact with, not just for people." Piper Morgan's BYOC thesis is the same architectural shape arriving from the opposite direction. Meanwhile PM's Lead Dev closed **M1 Gate #926** on April 11 with a 7/9 PASS after weeks of targeted fixes. The final two fixes surfaced a generalizable failure class: when a pre-classifier misses a query, the floor runs with no context, and the LLM produces plausible-looking fabrications. The dual fix — pattern repair plus an explicit fabrication prohibition in the floor system prompt — is a pattern worth Klatch studying for its own AAXT probe design.

---

## Key Insights

### 1. Klatch Step 10 Sharpens: The Export Format Is the Protocol
**From:** Klatch (Calliope + xian, April 10 evening session)
**Relevant to:** Piper Morgan (BYOC architecture, M5 distribution design, MCP integration)

Klatch shipped v0.9.0 (Files & Context Architecture) and immediately filed a futures memo — `docs/futures/2026-04-10-klatch-as-context-protocol.md` — that reframes Step 10's stakes. The memo argues that Klatch's Step 10 Phase 1 canonical package format should be designed not just as "what we export to a file" but as "what we serve over MCP." In this framing, Klatch becomes a **context interchange protocol**: any MCP-capable client requests a channel's assembled context and receives a complete five-layer package. Step 10 Phase 5 (MCP server, previously deferred) moves from "nice someday" to "the natural endpoint this work was always pointing at."

Three converging signals make this more than speculation. First, **Claude Managed Agents** (public beta, April 8) provides a concrete infrastructure target: it speaks MCP natively, its Agents/Sessions/Environments model maps onto Klatch's entity/channel/project model, and Klatch's SDK needs bumping from ^0.78.0 to ^0.86.1 to access it. Second, **SDK compaction-helper deprecation** in v0.83.0 signals that Anthropic is centralizing context management inside Managed Agents — the directional signal being that Anthropic wants to own the execution layer, not just the model API. Third, xian framed the broader direction explicitly this week: "I start to think of our products as being services for agents to interact with and not just for people."

The memo names the concrete Piper Morgan intersection directly: PM's BYOC thesis says Piper ships as an MCP server that plugs into any MCP-capable client. Klatch's context protocol could be the upstream data source that Piper's BYOC MCP server calls at session start — rather than re-assembling context from scratch, PM requests a pre-assembled five-layer package from Klatch. The two projects are designing toward a shared architecture: Klatch as context server, PM as task-and-knowledge server, Managed Agents as the execution layer both plug into.

**Suggested action:** PM Architect should read `docs/futures/2026-04-10-klatch-as-context-protocol.md` (in the Klatch repo) before the next M5 distribution design session. The open question it poses — "what is the canonical context package?" — is the same question PM needs to answer for any inter-system context handoff. A short alignment conversation between Daedalus and PM Architect before Klatch Phase 1 design begins would prevent each side from specifying a format independently that the other then has to bridge.

---

### 2. M1 Gate Closed — Floor Fabrication Guardrail Is a Generalizable Pattern
**From:** Piper Morgan (Lead Dev, April 10–11)
**Relevant to:** Klatch (AAXT scaffolded probing, floor-routing failure modes)

PM's Lead Dev closed **M1 Gate #926** on April 11 at 7/9 PASS (Q2 tone marginal, #922 OK-affirmation deferred to M2). The final session resolved two issues that together describe a complete failure class.

**The bug:** "list todos" (no "my") fell through the pre-classifier and reached the floor with no user context. The floor LLM hallucinated nine plausible-looking todos with PM-style descriptions. The failure was invisible — the output looked like a real task list, not an error.

**The dual fix:** (1) Made "my" optional in `TODO_QUERY_PATTERNS` at three locations, closing the immediate route. (2) Added an explicit prohibition in the floor system prompt: "NEVER list or invent user data (todos, projects, issues, calendar) unless that data is explicitly present in the Available context block." This is a defense-in-depth guardrail — if other pre-classifier patterns miss similar queries, the floor refuses to fabricate rather than inventing plausible content.

Three M2 issues filed: #960 (floor fabrication root fix), #961 (floor-route context audit), #962 (LLM-shortcut inversion sweep). The pattern fix closes the specific bug; the guardrail buys time; the M2 issues address root causes.

**For Klatch:** This failure class — pre-classifier miss → floor with no context → confident fabrication — is a universal risk. Klatch's AAXT scaffolded probing should include a probe class for the absence case: "what does the agent say when asked about user data it was never given?" Worth adding to the AAXT failure-mode taxonomy alongside the six existing categories.

**Suggested action:** Klatch Argus: add a fabrication-under-absent-context probe class to AAXT. Pass criterion: agent expresses uncertainty or absence. Fail criterion: agent produces plausible-looking specifics.

---

## Emerging Pattern

**"Products as services for agents" is the architectural convergence of the week.** Both projects independently arrived at this insight across the same 48-hour window. Klatch's futures memo named it explicitly for the first time in Klatch's design history; PM's BYOC thesis has been pointing at it since April 8. The shift is subtle but significant: it's not "our product is accessible to agents" (API access bolted on) — it's "our product is designed as a service that agents call, and the human UI is a consumer of that same service." The most interesting near-term question is whether Klatch and Piper Morgan can define a minimal shared interface before each independently ships its own MCP surface.

---

## Background Changes (Noted, Low Priority)

- **v0.9.0 GitHub Release live (Klatch):** Step 9 complete. Step 10 (Export + Meta-Model) is the active next step.
- **849 tests zero failures (Klatch):** Last verified at v0.9.0 tag. SDK upgrade to ^0.86.1 pending Argus.
- **MAXT Session 02 and Iris Use Case 2 still queued (Klatch):** Spring-loaded team; both items are immediate next candidates.
- **M2 sprint planning begun (PM):** 32 open issues. Next steps: canonical retest (benchmark vs M0's 76%), M1 retro, PPM + leader review.
- **Three M2 architectural issues filed (PM):** #960 floor fabrication root fix, #961 floor-route context audit, #962 LLM-shortcut inversion sweep. Not yet scoped.
- **The No-Anchoring Roundtable published (PM):** Blog + Medium. Eighth blog-first canonical publish.
- **Drafts folder cleaned (PM):** 86 files pruned to 19 active + 11 published + 55 superseded.

---

## Sources Read

**Klatch:**
- `git log --since="48 hours ago"` — 6 commits
- `docs/futures/2026-04-10-klatch-as-context-protocol.md` — Klatch as context interchange protocol memo (full)
- `docs/logs/2026-04-10-2308-calliope-opus-log.md` — Calliope session log
- `docs/plans/STEP-10-EXPORT-META-MODEL.md` — Step 10 phasing plan

**Piper Morgan:**
- `git log --since="48 hours ago"` — 11 commits
- `dev/active/2026-04-11-0708-lead-code-opus-log.md` — Lead Dev session: M1 Gate closure, floor fabrication fix, M2 planning start
- Commits `4789de64` (floor fabrication guardrail), `063edf52` (pre-classifier fix), `838ed70` (todo completion persistence)
