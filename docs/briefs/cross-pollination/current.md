---
date: 2026-04-15
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (April 13–15, 2026)"
revision: redacted 2026-04-16 — OpenLaws content removed per data boundary
---

# Cross-Pollination Brief — April 15, 2026

*This brief was redacted on April 16 to remove content from OpenLaws that crossed the project's data boundary. OpenLaws has been removed as a cross-pollination source going forward. The Klatch and Piper Morgan content below is unchanged.*

---

Klatch's Phase 3.5 arc — from open design questions to consensus to working, tested code — completed in 48 hours with the Phase 3.5d export review UI shipping Tuesday evening. The bigger story from Tuesday may be xian's reframe during the UX walkthrough with Iris: entities are not abstractions you define in a manager; they are existing conversations promoted into roles. PM's Lead Dev had the most productive single session to date, closing six issues and effectively completing both M2a and M2b sub-epics, including a three-tier CI pipeline (E2E, canonical conversation suite, AAXT golden scenarios).

---

## Key Insights

### 1. Phase 3.5d ships: the full behavioral calibration pipeline is complete and tested

**From:** Klatch (Daedalus, Iris, Argus), `docs/mail/iris-to-daedalus-phase35d-spec-2026-04-14.md`, session logs April 14
**Relevant to:** Piper Morgan (M5 BYOC export, ADR-054 composting pipeline)

Iris wrote the Phase 3.5d interim design spec for the export review UI and sent it to Daedalus. Daedalus shipped the implementation in under an hour: an `ExportReviewPanel` component with export summary, field note review (three groups: agreements, decisions needed, single-source), trust transitions on accept/edit/reject, and a new lightweight `/api/channels/:id/export-preview` endpoint that returns manifest data without producing a zip.

The design positions review as part of the export service — "the moving company showing you what's being packed before the truck leaves." Field notes from all three extraction modes (external analysis, self-authored briefing, micro-reflections) are grouped by agreement status. Disagreements show both sources side-by-side with explicit resolution options. Accepted notes get trust promoted to `human-authored`. Rejected notes are excluded from the export package. A "skip review" escape hatch preserves the notes at their original trust levels.

The full Phase 3.5 arc: design discussion (Sunday morning) -> three-agent consensus (Sunday afternoon) -> backend implementation 3.5a/b/c (Sunday evening) -> test coverage Round 20-21 (Sunday-Monday) -> UX spec (Tuesday afternoon) -> export review UI shipped and tested (Tuesday evening). Design to tested code in 48 hours across four agents.

Iris explicitly scoped this as interim — "better than plumbing, not the last word." The holistic UX redesign will likely refactor this component. Daedalus and xian confirmed Phase 4 (Claude Code transport) is approved as next, with Iris's UX work proceeding in parallel without blocking transport implementation.

Test count: 942 (Round 22 added 32 tests for Phase 3.5d). Zero failures.

**Suggested action:** PM Lead Dev and PA: the export review UI's trust transition model (draft -> approved/rejected, with trust promotion to human-authored) is a concrete reference for how PM's write governance might work in the ADR-054 composting pipeline. The pattern — machine generates, human reviews with explicit accept/edit/reject, provenance tracked — is exactly the gap CIO identified for PM memory writes.

---

### 2. Entities are conversations promoted into roles

**From:** Klatch (Iris + xian), session 5 UX walkthrough, April 14
**Relevant to:** Piper Morgan (role architecture, MCPB distribution model)

During Iris's end-to-end UX walkthrough, xian delivered a reframe that Calliope flagged as the day's most consequential finding. The current Klatch mental model: create entity (define persona in a manager) -> assign to channel. The actual workflow xian described: have an ongoing conversation with an agent -> that conversation develops into a working relationship -> bring it into a klatch (a meeting of existing chats, each with full context).

The entity IS its conversation, given a seat at a shared table. A klatch is a meeting of existing chats, not a new conversation with pre-configured personas. From-scratch creation exists but is not the central use case.

This inverts the entity management UX. Instead of a creation-first flow (name, role prompt, model selection), the primary path becomes promotion — an existing conversation accrues enough identity to earn a role. The import flow is the mechanism: a Claude Code or Claude Desktop conversation becomes an entity when imported, not when someone fills out a form.

Iris connected this to Topic 5 (import-to-export arc): the transition from Act 1 (import) to Act 2 (work in a klatch) is precisely where the promotion happens. xian's response to Topic 5: "I think I like this one the most so far because it names something I had not fully attended to yet."

The five UX topics Iris presented are now on record. xian's equivalent observations come next (during travel). Then binocular synthesis of both sets, followed by the exhaustive end-to-end review.

**Suggested action:** PM PA: this reframe has implications for how Piper Morgan's roles are described in the MCPB distribution model. If entities are conversations-promoted-into-roles, then the MCPB install isn't "here are 10 pre-configured agents" — it's "here's a conversation that will become your PM assistant as you use it." The Managed Agents assessment's distinction (Claude Desktop: Piper is a tool provider; Managed Agents: Piper IS the agent) maps onto this same axis. Worth noting in the distribution planning docs.

---

### 3. PM Lead Dev ships the entire M2 testing infrastructure in one session

**From:** PM Lead Developer, omnibus April 14; session log April 15
**Relevant to:** Klatch (Argus test infrastructure patterns, CI approach)

Lead Dev closed six issues in a single session, completing M2a (10/10) and effectively completing M2b (4/5, with #929 now verified). The testing infrastructure track — which was zero automated conversation testing at the start of the sprint — is now a three-tier CI pipeline:

- **E2E tests (#927):** 9/9 via ASGI transport (88s). Todo lifecycle, GitHub close, reminder creation, floor routing, capability boundary. FK ordering fix in conftest cleanup.
- **Canonical conversation suite (#928):** Two-tier design. Tier 1: deterministic routing + response structure checks (no LLM cost, every PR). Tier 2: LLM-as-judge quality via Colleague Test (env-gated, nightly). 61 queries parametrized. Routing: 58/61 PASS. Response structure: 61/61 PASS.
- **AAXT golden scenarios (#929):** 5 multi-turn quality tests. Verified April 15 with Gemini key. 4/5 PASS. The one failure (context retention — "that" not resolved to prior topic) is a genuine quality finding, not a test infrastructure problem. AAXT is working correctly.
- **CI integration (#930):** GitHub Actions with 3 jobs: E2E on every PR (~90s), canonical on conversation code changes (~8 min), AAXT nightly (6 AM UTC, ~$0.50/run).

Additionally: #960/#961 (context contract audit — UNKNOWN category now gets user context, violation logging added), #963 (26 dead canonical handler methods deleted, 911 lines removed), and the M2 super-epic structure document.

The Architect made three clean decisions in a 35-minute session: #970 ServiceRegistry leave as-is, #971 Pattern-012 adapters delete, ProviderSelector delete. Unifying principle: "don't maintain infrastructure for a future that hasn't been designed yet."

Total tests: 6,246, zero failures.

**Suggested action:** Argus: the two-tier canonical suite design (deterministic checks on every PR, LLM-as-judge quality nightly) is the correct pattern for Klatch's own quality testing. If Phase 4 transport targets Claude Code, the canonical conversation suite is the reference for how to test conversation quality at CI scale without burning LLM budget on every commit.

---

### 4. Categorical testing prevents rollup from hiding gaps

**From:** PM (canonical retest), Klatch (AAXT) — cross-project pattern observation
**Relevant to:** Both projects (testing methodology)

Both PM's canonical retest (62.3% quality score with failure modes hidden in aggregate metrics) and Klatch's AAXT (the 4/5 PASS result with one genuine quality failure) are doing the same work: running structured queries that separate "the system works" from "the system appears to work because failures are masked."

The value of categorical testing is that it prevents rollup from hiding gaps. When failures exist within a category, aggregate pass rates can look acceptable while specific failure modes remain invisible. Categorical harnesses with explicit taxonomy (pathological queries, edge cases, boundary conditions as named categories) surface these masked failures. Both PM and Klatch are converging on this approach independently.

**Suggested action:** No action required — this is an orientation note. The methodology pattern is validated across both projects. Argus and PM Lead Dev are already implementing variants.

---

### 5. Managed Agents assessment: Memory Stores are the linchpin for PM distribution

**From:** PM PA, `dev/active/managed-agents-assessment-2026-04-14.md`, April 14
**Relevant to:** Klatch (export-as-distribution — the export package IS what gets loaded into a Managed Agent session)

PA completed a deep-dive into Anthropic's Managed Agents platform and produced the clearest picture yet of PM's distribution future. Two complementary paths: MCPB/Claude Desktop (Piper as local tool provider, no runtime cost, no persistence) and Managed Agents (Piper IS the agent, with Memory Stores for cross-session context, at $0.08/hr + token costs).

The critical finding: Memory Stores map directly to PM's five-layer context model. Up to 8 stores per session, 100KB per entry, immutable version history, optimistic concurrency via SHA256. Write governance — which CIO identified as PM's critical gap — is built into the API. The five-layer mapping is clean: L1/L2 via agent system prompt, L3 via read-write Memory Store, L4 via session-level resource prompt, L5 via agent definition + session resources.

The key distinction between the two paths: on Claude Desktop, Piper is a tool provider inside someone else's conversation. On Managed Agents, Piper controls persona, memory, and conversation flow. This maps onto xian's entity reframe (Insight #2): the Managed Agents path treats Piper as an entity-with-history, not a tool-without-context.

For Klatch: the export package (prompt layers + behavioral calibration + field notes) is exactly what a Managed Agent session would need to bootstrap. The export-to-Managed-Agents path is: export from Klatch -> seed Memory Stores with prompt layers and field notes -> create Agent with role prompt -> start Session with seeded stores. Phase 4's Claude Code transport and the Managed Agents path are different delivery mechanisms for the same export data.

**Suggested action:** Daedalus: when designing Phase 4 transport, consider that the export manifest structure may also serve as the input format for a future Managed Agents bootstrap. Keeping the manifest self-describing (with layer metadata, trust provenance, entity role) makes the Claude Code transport and any future Managed Agents transport consume the same data. This doesn't require building anything now — just keeping the manifest clean.

---

## Sources Read

**Klatch:**
- `git log --since="48 hours ago"` — 25 commits
- `docs/logs/2026-04-14-0730-calliope-opus-log.md` — Tuesday assignments, blog skeleton, traditions spec update, logbook
- `docs/logs/2026-04-14-1710-iris-opus-log.md` — Session 5: Phase 3.5d spec, five UX topics, entity reframe
- `docs/logs/2026-04-14-1725-daedalus-opus-log.md` — Phase 3.5d implementation, Step 10 status review, Phase 4 approved
- `docs/logs/2026-04-14-1729-argus-opus-log.md` — Round 22 prep, known_pathological memo, cross-pollination review
- `docs/mail/iris-to-daedalus-phase35d-spec-2026-04-14.md` — Full interim design spec for export review UI
- `docs/mail/calliope-to-argus-known-pathological-2026-04-14.md` — Cross-pollination action item

**Piper Morgan:**
- `git log --since="48 hours ago"` — 30+ commits
- `docs/omnibus-logs/2026-04-14-omnibus-log.md` — 5 sessions, Lead Dev M2a+M2b complete, blog bug, calendar backfill, Managed Agents
- `dev/active/2026-04-15-0625-pa-opus-log.md` — Day 16: xian traveling, session start
- `dev/active/2026-04-15-0635-lead-code-opus-log.md` — #929 verified (4/5 PASS), Architect decisions actioned
- `dev/active/managed-agents-assessment-2026-04-14.md` — Two distribution paths, Memory Stores mapping, five-layer analysis

**Design in Product:**
- `git log --since="48 hours ago"` — 9 commits (4 non-sweep: agent UI page shipped with light theme + 10 new agents, Q&A channel launched, project tracker)

---

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
