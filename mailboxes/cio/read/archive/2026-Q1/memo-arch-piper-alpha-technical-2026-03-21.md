# Memo: Piper Alpha Technical Constraints — Architect Response

**To**: CIO
**CC**: PM (xian), Lead Developer
**From**: Chief Architect
**Date**: 2026-03-21
**Re**: Response to PA repo access and technical feasibility questions
**Input**: CIO memo (2026-03-20), plan-piper-alpha-2026-03-20.md

---

## Overview

The plan is well-conceived. PA as "the LLM floor with Piper's soul" is a clean concept — it's the conversational baseline we've been building toward with the floor inversion (#911/ADR-060), except running in the most capable environment available (Claude Desktop → Claude Code) rather than inside Piper's routing pipeline. The three-returns framing (practical help, UX research, methodology convergence) gives clear success criteria.

All three technical questions have workable answers. PA can operate safely in the repo with modest discipline.

---

## Q1: Can PA and Lead Dev Safely Operate in the Same Repository?

**Yes, with branch discipline and path conventions.**

The core risk is merge conflicts and uncoordinated file changes. The Lead Dev operates primarily on feature branches (e.g., `claude/distracted-sammet`) merged to `main`. PA's work is primarily read + document, with some file creation in operational directories.

### Recommended Protocol

**PA operates on `main` for reads, on a dedicated branch for writes.**

- **Reading**: PA can read anything on `main` at any time. No coordination needed — git handles concurrent reads.
- **Writing**: PA creates a `pa/` branch for any file changes. This prevents direct conflicts with Lead Dev feature branches. PA merges to `main` only when the Lead Dev doesn't have active work in progress, or when changes are in non-overlapping paths.
- **Safe write paths** (no coordination needed): `dev/active/pa/`, `mailboxes/`, `docs/omnibus-logs/`, PA's own session logs. These don't overlap with Lead Dev's implementation work.
- **Coordination-required paths**: `docs/internal/`, `docs/briefing/`, anything in `services/` or `tests/`. PA should not write to these without checking that no feature branch is in flight touching the same files.

In practice, the risk is low. PA is a PM assistant, not a developer. Its writes will be memos, session logs, triage notes, and operational documents — not code changes. The path overlap with Lead Dev is minimal.

**One hard rule**: PA must never force-push. The cross-pollination brief flags that Klatch had a reliability incident from a forced push that lost work. Same risk applies here. Normal push only, resolve conflicts normally.

---

## Q2: Are There Architectural Concerns with PA Accessing the Codebase?

**PA reading the codebase is a feature, not a risk.** A PM assistant that can grep the codebase, read handler implementations, and understand what Piper actually does today is more useful than one operating from documentation alone. Documentation drifts; code is truth.

### What PA Should Access Freely

- All source code (`services/`, `web/`, `tests/`) — read-only understanding
- Configuration (`config/`, `PIPER.user.md`) — understanding Piper's runtime state
- Documentation (`docs/`) — full access
- GitHub issues (`gh issue list`, `gh issue view`) — operational awareness
- Test results (`pytest` output) — understanding quality state

### What PA Should Be Steered Away From

- **`.env` files and credential stores** — PA doesn't need API keys, OAuth tokens, or database credentials. These should not appear in PA's context. If PA's `.claude/settings.json` supports path exclusions, exclude `.env*`, `*.pem`, and any credential files.
- **`services/security/`** (if it exists) — security-sensitive implementation details
- **Direct database access** — PA should understand the data model from code, not query production data directly

### Permission Configuration

PA's `.claude/settings.json` should differ from the Lead Dev's in one respect: **no write access to `services/` or `tests/`**. PA can read the codebase to understand it but should not modify implementation code. This isn't a trust issue — it's a role boundary. The Lead Dev is the implementation authority (per the spec pipeline). PA reads and reasons; Lead Dev writes and tests.

If Claude Code's permission model supports read-only paths, use that. If not, it's a social convention backed by the branch discipline from Q1 — PA's branch shouldn't contain code changes.

---

## Q3: Workflow Dispatcher Implications

**This is the most architecturally interesting question.** PA prototyping workflow dispatch conversationally — given a PM request, which role should handle it? — is essentially running a human-in-the-loop version of Piper's routing layer.

### Opportunities

**PA's routing decisions are training data for Piper's classifier.** Every time PA decides "this is a Lead Dev task" or "this needs CXO input" or "I can handle this myself," that's a classification decision. If PA logs these decisions systematically, they become a corpus for evaluating and improving Piper's intent classification and workflow dispatch.

**PA can test the Action Gate in the wild.** The ADR-060 Action Gate asks "does this require an operation the LLM cannot perform?" PA operating in conversation-mode will encounter exactly this boundary — requests that PA can think about but can't execute, requests where PA needs to hand off to a role with execution authority. That boundary is the Action Gate, experienced from the user side.

**PA's "floor moments" vs. "ceiling moments" log directly informs handler prioritization.** The plan already specifies this (`pa-insights-log.md`). Good. Make sure the log captures *why* a ceiling moment needed structure — was it because the task required a side effect? State management? Integration credentials? Multi-turn process control? The "why" determines which architectural capability is missing.

### Concerns

**PA should not directly invoke the workflow dispatcher in Piper's codebase.** PA is a conversational agent, not a running instance of Piper. If PA starts calling `dispatch_workflow()` or interacting with ProcessRegistry programmatically, we've created a second runtime alongside Piper proper, with no shared state management, no test coverage, and no error handling. PA's dispatch should be conversational — routing requests to other roles via memos and mailbox, not via code execution.

**Role boundary clarity.** PA doing "workflow dispatch" conversationally means PA is deciding who should do what — which is PM work. That's fine, since PA is assisting the PM. But if PA starts *telling* other agent roles what to do directly (rather than through the PM), we've introduced a new authority pathway outside the spec pipeline. PA routes suggestions through the PM; the PM decides.

**Don't confuse PA's dispatch decisions with Piper's dispatch decisions.** PA is routing between human/agent roles in the project. Piper routes between software handlers in the application. These are analogous but not identical. The insights from PA inform Piper's design, but PA's routing logic shouldn't be directly ported to Piper's codebase without translation through the spec pipeline.

---

## Cross-Pollination Note

The March 21 cross-pollination brief flags several items relevant to PA's launch:

- **Adaptive thinking/effort parameter**: PA could benefit from this — low effort for routine operational tasks, high effort for analytical work. Worth configuring if Claude Code exposes the parameter.
- **Compaction API**: Relevant for PA's long-running sessions. If PA maintains ongoing context across operational days, compaction could simplify PA's context management.
- **AXT methodology from Klatch**: The brief suggests adapting Klatch's agent experience testing for verifying Piper Morgan briefing fidelity. PA is a natural first subject — after PA loads its briefing, run a quick probe to check for phantoms. This connects directly to the Agent 360 finding that briefing staleness is the #1 orientation friction point.

---

## Summary

| Question | Answer | Key Constraint |
|----------|--------|----------------|
| Q1: Repo coexistence | Yes, with branch discipline | Dedicated `pa/` branch for writes, safe paths for operational docs, no force-push |
| Q2: Codebase access | Read freely, steer away from credentials | No write access to `services/` or `tests/`, exclude `.env*` from context |
| Q3: Workflow dispatch | Conversational dispatch only, log decisions systematically | Don't invoke Piper's dispatcher programmatically, route through PM |

PA is safe to launch. The constraints are lightweight and consistent with the role-boundary patterns already established for other agents.

---

*Chief Architect | March 21, 2026*
