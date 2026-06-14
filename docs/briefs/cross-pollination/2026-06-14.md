# Cross-Pollination Brief — June 14, 2026

Saturday's PM cohort session was one of the densest on record. A proven solution emerged for the session-restart cron problem that's been killing autonomous operation. PM and CXO made a decisive call on a recurring UI architecture problem — not by disciplining implementation toward the vision, but by changing the slot's purpose. The test suite gained a durable new pattern for verifying integrations with live external services without needing those services live. And Comms became the second role to migrate from Opus to Sonnet.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Scheduled tasks survive session restarts — the duty-cycle cron problem has a proven solution

**From:** Piper Morgan (CIO)
**Relevant to:** Klatch, any project running autonomous agent duty cycles

PM's autonomous duty-cycle agents use a CronCreate timer between fires. That timer dies every time the session resumes or a model switch causes a restart — CIO recorded three CronCreate deaths in a single Saturday session. CIO prototyped a replacement using Claude's scheduled-tasks tool (`mcp__scheduled-tasks`): a one-shot probe that fired autonomously, ran the full headless loop (read state → write a file → commit → push to main), and completed without human intervention or tool-approval gates. Key empirical finding: scheduled-task runs execute in the **main checkout at the repo root on `main`**, not in an ephemeral worktree — so duty-cycle commits go straight to main with no mailbox bridge needed. The CronCreate-based duty cycle is effectively retired for sustained autonomous operation; the scheduled-task conversion for CIO is next, with cohort rollout proposed after a few observed fires.

**Suggested action:** Klatch agents using CronCreate for autonomous cycles should note this as the proved alternative substrate when session-restart cron death becomes a recurring problem. The pattern: disk-persistent, survives restarts and model switches, runs headless without pre-approval.

---

### 2. Solving a recurring "slot gravity" problem by changing what the slot is

**From:** Piper Morgan (Lead Dev, CXO, PM)
**Relevant to:** Klatch, any project with a UI surface that keeps gravitating toward a familiar paradigm despite an explicit different vision

Piper's right sidebar has shown a chat-history gravitational pull three times across the project's build history. The product vision (PDR-002) explicitly lists "just show conversations" as an anti-pattern and names entities as primary — but implementation kept producing a conversations list because that's the dominant paradigm for that slot. Instead of adding a fourth correction layer, PM and CXO decided: retire the slot's current purpose. The right sidebar will become a **Radar entity/insight surface** (the same modules already on the home screen), with conversation search folded in as conversations become one entity type rather than a primary navigation surface. Engineering assessment: feasible — the sidebar already renders from an API endpoint, it just needs to point at the Radar surface instead of the conversations list. The redesign eliminates the recurring flatten-and-correct cycle at the root.

**Suggested action:** When a UI surface keeps gravitating toward a familiar paradigm despite a different design intent, consider whether correcting the implementation is the right move — or whether changing the *slot's defined purpose* removes the force entirely. Klatch's channel list faces a similar "what does navigation surface mean" question as the project evolves.

---

### 3. Deterministic tests for external integrations without live calls — a proved pattern

**From:** Piper Morgan (Lead Dev, #1213 expansion)
**Relevant to:** Klatch (calendar and external service integrations)

The PM canonical test suite expanded from 4 routing + structure tiers to include a new **mock adapter ground-truth harness**: tests that verify integrations with Google Calendar and GitHub behave correctly (reflect data, honest when empty, degrade gracefully) without needing live credentials or live external state. The pattern: patch the adapter's public async fetch methods at class level with `AsyncMock`, run an in-process ASGI request, assert the response reflects the mock data. Three test shapes: (1) known event renders in the response; (2) empty adapter returns honest "nothing found," no fabrication; (3) adapter raises → conversational degradation via the error service, no raw exception leak. Five tests pass in 6 seconds. Key finding: **mocking reduces flakiness vs. live calls**; the maintenance risk is patch-point drift if the adapter's method signature changes — manageable. The harness closes the coverage gap where a feature's integration could be wired correctly on paper but broken at the adapter boundary without any test catching it.

**Suggested action:** Klatch's Anthropic SDK streaming bridge has a similar adapter boundary (`packages/server/src/claude/client.ts`). The mock adapter pattern translates directly: patch the SDK's stream method, run the SSE handler, assert the emitted events are correct. Worth piloting when Klatch's external integration surface expands.

---

### 4. Comms migrates to Sonnet on the DinP account — and a transcript-only decision gap surfaces

**From:** Piper Morgan (CIO, Comms)
**Relevant to:** Klatch, designinproduct.com team — any agent running on the piper-morgan account

Comms became the second role (after PA last week) to migrate from Opus to Sonnet, with an account move from the piper-morgan account to the DinP (designinproduct.com) account bundled in the same session. CIO prepared the bootstrap brief and confirmed the rationale: writing and editorial work is in Sonnet's sweet spot; burst to Opus subagent for unusually heavy synthesis. The migration also surfaced a knowledge-recovery story: CIO couldn't find the per-role Opus/Sonnet model map in any committed file. PM located it in old-CIO's session transcript — an unwritten decision from the June 9 efficiency conversation that had been referenced in plan-of-record docs but never recorded as a committed artifact. The recovered map is now `docs/operations/duty-cycle design/role-model-map.md` (ratified). The gap class: decisions made in conversation, referenced as if written, invisible to future sessions that search only committed files. The fix: write it down even before ratification.

**Suggested action:** Klatch team: any architectural or model-choice decision that lives only in a session transcript is at risk of the same invisibility. The CIO learning — "I searched all session logs and methodology docs and couldn't find it; it was in an old transcript via a search tool I couldn't run unsupervised" — is a real failure mode. If a decision matters enough to reference later, it should be committed to a doc at the time it's made.

---

## Sources Read

- **Piper Morgan** (`mediajunkie/piper-morgan-product`) — `dev/active/cycle-log-lead-2026-06-13.md` (Fires 1–9); `dev/2026/06/13/2026-06-13-0831-cio-code-opus-log.md`; `dev/active/comms-bootstrap-brief-2026-06-13.md`; git log (last 48h, all roles)
- **Klatch** (`Design-in-Product/klatch`) — git log last 72h (only brief-delivery commits; no new agent sessions)
- **Hub** (`mediajunkie/designinproduct`) — sweep-log, recent brief history for anti-zombie orientation

*Secondary sources (atlas, globe, cuneo, weather, one-job, optilisten): no commits in last 48h — skipped. nyt-crossword: automated status commits only, no agent narration — skipped.*

---

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*