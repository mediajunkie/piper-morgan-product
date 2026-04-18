# Cross-Pollination Brief — April 18, 2026

Three threads closed in the last 24 hours. PM's ethics activation path cleared when CXO delivered voice guidance for Mode-2 decline responses — `#992 ETHICS-ACTIVATE` is now implementation-ready after weeks as a blocked P1. PM formally closed M2c with routing at 95.1% and quality at 72.1%, a +9.8 point improvement since the M2a baseline; M2d (MUX lifecycle) is next. And both Klatch and PM added `DECISIONS.md` files on the same day — a convergent infrastructure move explicitly designed to make the daily brief more reliable.

---

## Key Insights

### 1. Ethics activation unblocked — CXO voice guidance received, #992 ready for implementation

**From:** PM Lead Developer + CXO, `dev/2026/04/16/964-findings-memo.md`, CXO inbox memos Apr 16 evening
**Relevant to:** Klatch (behavioral guardrails, entity response surfaces); both projects as ethical response architecture matures

When `#964 FLOOR-ETHICS-VERIFY` closed April 16, the P1 finding was `ENABLE_ETHICS_ENFORCEMENT=false` in production — BoundaryEnforcer wired since October 2025 but switch off by default. Activation was blocked on CXO voice input for Mode-2 decline copy (how Piper says no). That input arrived the same evening.

CXO delivered three structured decline templates, anti-patterns to avoid, a Colleague Test auto-fail rule (Tone=0 = auto-fail, not MARGINAL), and a false-positive ceiling: 2-3% before beta, validated against the canonical retest corpus. The acceptance criteria are now fully specified in `#992`. The path to production: implement the voice layer, run canonical probes, validate false-positive rate, then flip the flag.

CXO also weighed in on the P2 question (post-generation response content check) — non-binding Option A preference but deferred the architectural decision to PM.

**Suggested action:** Klatch: as entity conversations deepen and Phase 4 transports mature, a guardrail that exists but defaults-off is a liability. Track the state of any behavioral gates (not just ethics — content shape, response scope, floor prohibitions) as a named bit, not implicit code behavior. "Is enforcement on?" should be checkable at a glance. PM: the Colleague Test Tone=0 auto-fail criterion is new and affects scoring across the whole rubric, not just ethics probes. Flag this for Argus before the next AAXT run against the full canonical suite.

---

### 2. Evaluation instrument taxonomy settled — Colleague Test stays R/C/T, fabrication separate

**From:** PM CXO (via cross-pollination), Architect; `docs/end-of-day mail sweep` Apr 16, `#994`, `#995`
**Relevant to:** Klatch (AAXT design, evaluation methodology); both projects

Three evaluation-methodology decisions landed April 16 evening, all traceable to cross-pollination inputs from Klatch's Architect:

- **#994 AAXT scorer vocabulary**: Adopt the six-failure-mode taxonomy (filed as a PR for the AAXT scoring protocol). CXO endorsed. If the vocabulary is still mutable in the current scoring spec, now is the time to adopt it — it becomes the shared language for failure analysis across projects.

- **#995 Standalone fabrication probe set**: Architect proposed 5–10 probes across 5 absence categories as a regression fence for the `#960` guardrail. CXO endorsed. This becomes the fabrication instrument — structurally separate from the Colleague Test rubric.

- **Colleague Test rubric stays R/C/T**: CXO explicitly ruled against adding a fabrication dimension to the Colleague Test. The argument: fabrication and conversational quality are distinct failure modes that need distinct instruments. Mixing them muddies both. Rubric stays three-dimensional; fabrication gets its own harness.

The generalizable principle: evaluation instruments should be specialized. Combining orthogonal concerns (tone quality vs. knowledge hallucination) into a single rubric optimizes for compactness but degrades diagnostic resolution. This is the same "separate the concerns" principle that Pattern-062 diagnosis applied to context assembly.

**Suggested action:** Klatch AAXT team (Argus, Daedalus): before the next major AAXT run, confirm whether the current scorer implements the six-failure-mode vocabulary and whether a standalone fabrication probe set exists. If PM is building `#995` in parallel, there may be a shared probe set worth coordinating on — same absence categories, same failure taxonomy.

---

### 3. DECISIONS.md added to both repos on the same day — coordination infrastructure

**From:** Klatch (commit `04a0f36`), PM (commit `f8fdc29`), both Apr 18
**Relevant to:** Both projects; cross-pollination sweep reliability

Both Klatch and PM added `DECISIONS.md` files today. The format: append-only, one line per decision, `DATE | DECISION | PARTICIPANTS`, with major ADRs as the full artifact and this as the greppable index underneath. The stated motivation on both commits: "anti-zombie brief checks" — giving the daily sweep something machine-readable to scan for decisions that crossed repo boundaries.

This is a convergent infrastructure move that emerged independently in both projects at the same time. The Klatch `DECISIONS.md` already has six entries (April 10–17); the PM version has four. Both capture decisions that were previously scattered across commit messages, memos, and session logs.

**Suggested action:** Both projects: commit to a session discipline of appending to `DECISIONS.md` whenever a project-level call is made — especially decisions that affect the other project or surface methodological choices. The brief can then do a targeted grep rather than full log scan. Longer term: the format could be the seed of a lightweight ADR index.

---

### 4. M2c closed — routing 95.1%, quality 72.1%, M2d next

**From:** PM Lead Developer, `docs/internal/planning/m2-structure.md`, Apr 16
**Relevant to:** Klatch (project milestone context; floor + quality arc)

M2b (test infrastructure: 5/5) and M2c (conversational depth: 6/6) both formally closed April 16. M2c closed at canonical retest Run 5: 95.1% routing (vs. 93% at M2a), 72.1% quality (+9.8 points from the 62.3% M2a baseline). The gap to the aspirational 80% quality ceiling is primarily a fresh-account context problem tracked in `#989` — users with no projects or history can't receive anchored responses, so Context scores stall at 1.

M2d (MUX lifecycle) is next. Fourteen follow-up issues filed during M2c are organized by family (context assembler, ethics, LLM infrastructure, testing, hygiene) — none block M2d start.

**Suggested action:** Klatch: the fresh-account ceiling is a variant of the cold-start onboarding gap surfaced in Klatch's own Alpha tester work (April 2026 brief). Both projects have the same structural problem: high-quality responses require anchoring context, but new users have none. Worth comparing approaches — PM's solution involves explicit user-anchoring fields in the context assembler; Klatch's will likely involve channel bootstrapping and entity initialization.

---

## Sources Read

- Klatch: `DECISIONS.md` (new, Apr 18)
- Klatch: `docs/mail/memo-janus-to-calliope-apr15-brief-redacted-2026-04-16.md`
- PM: `docs/internal/planning/m2-structure.md` (M2b/M2c closure, Apr 16)
- PM: commit body `a6b3a6d` — #964 ethics verification findings summary
- PM: commit body `d9f9b3f` — #950 Five Pillars floor prompt evolution
- PM: commit body `52059b3` — end-of-day mail sweep, #993–995 filed, CXO voice guidance
- PM: commit body `4f5ee41` — canonical retest iter 2 (44/61 PASS, 72.1%)
- PM: `DECISIONS.md` (new, Apr 18)
- PM: `docs/omnibus-logs/2026-04-15-omnibus-log.md`

---

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
