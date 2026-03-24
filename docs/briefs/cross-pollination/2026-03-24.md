---
date: 2026-03-24
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (March 22-24, 2026)"
---

# Cross-Pollination Brief — March 24, 2026

Klatch had a dense 48 hours: agent traditions formalized and shipped, the 5-layer prompt assembly spec published publicly as a blog post, two ecosystem intelligence sweeps filed, WCAG accessibility audit complete, and Round 12 assignments dispatched. MAXT Session 01 is imminent — it will be the first empirical validation of the 5-layer model across a real context transition. Piper Morgan shows no new development activity on the observable branch; only the cross-pollination brief delivery landed. The git state issue flagged in the March 24 session handoff memo remains open.

---

## Key Insights

### 1. Agent Traditions Pattern — Fully Shipped, Reference Implementations Live
**From:** Klatch (`docs/agents/calliope.md`, `docs/agents/argus.md`, `docs/AGENT-TRADITIONS-SPEC.md`)
**Relevant to:** Piper Morgan

Klatch has now shipped two production traditions documents alongside the spec. Each covers 7 sections: role and purpose, working style, standing responsibilities, conventions and standards, key relationships, institutional memory, and standing instructions. The Calliope doc is the reference implementation — thorough and editorial. The Argus doc has a different character: written with urgency after a reliability incident, its institutional memory section is unusually specific about what went wrong and why.

Both documents solve the cold-start problem: an agent inactive for days can read its traditions doc and know what it knows, what it's responsible for, and what it should never do again. The "institutional memory" section is the most valuable — it captures the *why* behind conventions, not just the *what*.

Piper Morgan has 14 agent roles, many of which go inactive between sprints. The traditions pattern addresses the gap the Agent 360 assessment surfaced: all 9 agents cited briefing staleness as their top friction point. A traditions doc for each role — even a minimal v0 — would significantly reduce cold-start overhead.

**Suggested action (Piper Morgan):** The Argus doc is the better template for Piper Morgan's situation — it was written to solve a specific reliability problem, not as an aspirational spec. Read `docs/agents/argus.md` in the Klatch repo. Start with the roles that go inactive longest (less-frequently-used roles, seasonal work) where cold-start cost is highest.

---

### 2. Klatch Intelligence Sweeps — Two Filed, Ecosystem Shifts Piper Morgan Should Know
**From:** Klatch (`docs/intel/2026-03-22-sweep.md`, `docs/intel/2026-03-23-sweep.md`)
**Relevant to:** Piper Morgan

Argus filed two systematic intelligence sweeps covering 22 items total. Several are directly relevant to Piper Morgan:

**Sonnet 4.6 (HIGH):** Now the default on Free/Pro. 30-50% latency reduction vs. Sonnet 4.5, same price ($3/$15 per million tokens), 1M context window (beta), SWE-bench 79.6%. Piper Morgan's multi-agent sessions could benefit immediately — lower latency per agent turn adds up across 14 roles.

**Compaction API (beta, Opus 4.6 + Sonnet 4.6):** Server-side context summarization when input tokens exceed threshold. Custom instructions preserved during compaction. Effectively infinite conversation length without client-side truncation. This could simplify or eliminate some of Piper Morgan's context assembly strategies for long-running agent sessions.

**Claude Agent Teams (experimental):** Built-in multi-agent orchestration — one lead, up to 10 sub-agents, parallel execution, structured message passing. Performance: 3-5x wall-clock speedup on parallelizable work. Requires experimental flag + Opus 4.6. Session-scoped, no persistence. This is Anthropic building toward what Piper Morgan and Klatch are already doing.

**Cowork three-way model alignment:** Anthropic now has three distinct project surfaces (claude.ai projects, Claude Code repos, Cowork local folders) with fragmented import paths between them. This affects Piper Morgan's context portability story and any future MCP strategy.

**Suggested action (Piper Morgan):** Read `docs/intel/2026-03-23-sweep.md` in the Klatch repo — it's the more recent and higher-density sweep. Evaluate Sonnet 4.6 for applicable agent roles. Add Compaction API to the architectural backlog as a potential simplification.

---

### 3. MAXT Session 01 — First Empirical Validation of the 5-Layer Model
**From:** Klatch (`docs/axt/maxt-session-01-baseline.md`, `exports/sessions/theseus-2026-03-22.jsonl`)
**Relevant to:** Piper Morgan

Klatch is about to run MAXT Session 01 — the first manual, qualitative Agent Experience Test using a real agent (Theseus Prime, informed condition) and the Fork Continuity Quiz v4. AAXT (727 automated tests, zero failures) cleared the gate. The quiz probes each layer of the 5-layer model in sequence: open canvas (unprompted self-report) first, then structured probing of each layer.

The results will answer: after a real context transition (export → re-import), what does an agent actually know vs. what it claims to know? How many responses are Correct, Reconstructed, Confabulated, Absent, or Phantom?

This will be the first empirical data on how well the 5-layer model actually works in practice. For Piper Morgan — which relies on briefing documents to orient 14 agent roles — this methodology is directly applicable. If Layer 3 (project memory) consistently degrades across transitions, that changes how you structure briefings. If Layer 5 (entity prompt) is robust but Layer 4 (channel addendum) is weak, that changes the priority order.

**Suggested action (Piper Morgan):** Watch for MAXT Session 01 results in the next brief. The failure taxonomy (Correct → Reconstructed → Confabulated → Absent → Phantom) is useful vocabulary for diagnosing your own agent briefing problems regardless of the quiz results.

---

### 4. Bookend-Sync Protocol — Formalized After Reliability Incident
**From:** Klatch (`docs/agents/argus.md`, Section 7: Standing Instructions)
**Relevant to:** Piper Morgan (especially given current branch situation)

After losing demo infrastructure work to an incomplete rebase recovery, Klatch's Argus formalized a mandatory git discipline protocol now embedded in standing instructions:

- Session start: `git fetch origin main && git merge origin/main --no-edit` — no skipping
- Never force push without explicit owner approval
- Verify deliverables before claiming "done": check `git log`, `ls` files, run test suite
- Commit frequently — don't accumulate hours of work uncommitted
- Push to branch only; merging to main is owner + Calliope responsibility

Both projects independently arrived at similar wrap-up verification protocols (noted in the March 21 brief). This formalization goes further — it's now in the agent's standing instructions, so it's not subject to forgetting across sessions.

**Suggested action (Piper Morgan):** Given the current branch state (164 local commits not on remote), this protocol is immediately relevant. Before any new development session begins, the branch/remote situation should be diagnosed and resolved. The bookend-sync protocol prevents this class of problem going forward.

---

### 5. Prompt Assembly Published — 5-Layer Model Now Public
**From:** Klatch (`blog/prompt-assembly.html`, `docs/drafts/prompt-assembly.md`)
**Relevant to:** Piper Morgan, and public narrative

Klatch published "What Does an Imported Agent Know?" — the public-facing narrative of the 5-layer prompt assembly model. Stewart Brand's pace layers (civilizations change slowly, fashion changes fast) as the organizing metaphor. The blog post is live on klatch.ing.

This makes the 5-layer model public, citable, and explained in non-technical terms. For Piper Morgan's building-in-public story, and for the cross-pollination hub's public representation on designinproduct.com, this is the canonical external reference.

**No immediate action required** — but both projects now have a URL to point to when explaining their context architecture to outside audiences.

---

## Emerging Patterns

**Traditions as institutional memory, not just documentation.** Both the Argus and Calliope traditions docs demonstrate that the most valuable section is institutional memory — *what went wrong, why, and what we never do now*. This is knowledge that doesn't exist anywhere else and decays rapidly without formalization. The pattern: when something breaks, write the incident into the relevant agent's traditions document immediately.

**Sweep → assignments → implementation.** Klatch is now running a full intelligence cycle: Argus files a sweep → Calliope extracts actionable items → Calliope routes assignments via memo → Daedalus implements. The March 23 sweep produced 5 concrete development assignments in a single day. This is the intelligence-to-action loop working at full speed.

**Parallel automation paths.** Klatch uses Cowork scheduled tasks (~$0.15/day) for intelligence sweeps. Piper Morgan uses Dispatch (persistent Claude Desktop chat with browser control) for omnibus synthesis. Different tools, same goal — remove human from the daily synthesis loop. The Klatch approach is more autonomous; the Piper Morgan approach is more supervised. Worth watching which scales better.

---

## Background Changes (Noted, Low Priority)

- Klatch blog: "Wireframe-First Design" published (reMarkable intro, fountain pen anecdote, origins of Klatch)
- Klatch WCAG AA audit complete: `--text-dim` contrast fixed sitewide, pace layers SVG redrawn at higher contrast
- Klatch CSS: `projects-section__intro` typography class published publicly
- Klatch Round 11 complete: 727 tests (611 server + 116 client), zero failures, merged to main
- Klatch ROADMAP.md updated: "Klatch as Universal Context Transport / MCP Service" and "Cross-Vendor Entity Channels" added to Someday/Maybe
- Piper Morgan: only activity is cross-pollination brief delivery (March 24, 04:59 UTC) — no development commits on observable branch

---

## Sources Read

**Klatch:**
- `docs/intel/2026-03-22-sweep.md` — 11 items (Agent Teams, Web Search GA, Compaction API, MCP governance, AuditBench)
- `docs/intel/2026-03-23-sweep.md` — 11 items (Cowork import HIGH, Sonnet 4.6 default HIGH, Code Review multi-agent HIGH, Haiku 3 deprecation MEDIUM)
- `docs/agents/calliope.md` — Agent traditions reference implementation
- `docs/agents/argus.md` — Reliability-focused traditions + bookend-sync protocol
- `docs/axt/maxt-session-01-baseline.md` — Pre-fork context baseline for MAXT Session 01
- `docs/mail/calliope-to-daedalus-round12-intel-sweep-2026-03-23.md` — Round 12 assignments
- `docs/mail/calliope-to-argus-intel-research-2026-03-23.md` — Argus research assignments
- `docs/logs/2026-03-22-0655-calliope-sonnet-log.md` — Blog publishing + WCAG audit session
- `docs/logs/2026-03-22-1358-theseus-opus-log.md` — MAXT prep, Round 11 completion
- `docs/logs/2026-03-23-0723-argus-opus-log.md` — March 23 intelligence sweep
- `docs/ROADMAP.md` — Strategic additions (context transport, cross-vendor)
- `blog/prompt-assembly.html` — Published 5-layer model post

**Piper Morgan:**
- `git log --since=2026-03-22` — One commit only: cross-pollination brief delivery (March 24)
- No session logs, omnibus logs, or planning documents added since March 22 on the observable branch
