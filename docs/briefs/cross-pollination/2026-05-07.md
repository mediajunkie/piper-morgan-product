# Cross-Pollination Brief — May 7, 2026

PM's Wednesday evening was a discipline session: four issues shipped cleanly (#1054 prod bug, #1056 stale test, #1057 ContextAssembler backfill, plus #1053 audit-cascade prep), the Architect's 5-item soundness review punch list fully closed, and #1053 staged for tomorrow's subagent execution. A meta-finding emerged from the audit prep: six N/A flags in one audit pass is a template-drift signal — PM observation filed immediately as both a memory entry and a hygiene ticket (#1058). Ship #041 "The Methodology Closes Its Own Loops" published Wednesday evening — the largest Ship to date by HTML weight.

## Key Insights

### 1. Silent production bug caught while fixing a test: broad `except` swallows uninitialized logger

**From:** PM `dev/2026/05/06/2026-05-06-1904-lead-code-opus-log.md` (commit `a374ba3b`, #1054)
**Relevant to:** Klatch (silent-failure-via-broad-except class; multi-file cleanup regression discipline)

#1054 looked like test drift — `test_generate_standup_for_user` failing on a mock expectation. Root cause on inspection: `MorningStandupWorkflow.logger` was never initialized in `__init__`. #1042's cleanup had added `self.logger.warning(...)` at line 197 of `morning_standup.py` without wiring a logger. `AttributeError` hit at call time and was silently swallowed by a broad `except` in `_get_session_context`, causing it to return `{}` early — skipping `session_manager.get_session_context` entirely. In production the standup function appeared to work; in reality it had been skipping session context retrieval since #1042 merged.

**Why this matters:** The bug would not have surfaced without the test failure, and the test failure looked like drift rather than a production problem. The actual defect — broad `except` eating an `AttributeError` and returning a degraded value silently — is the hard-to-detect class. Lead Dev's note: "the #1042 cleanup added a logger call but no logger init."

**Suggested action:** Klatch — any multi-file cleanup commit that touches callsites (adds/removes calls) should include a quick scan of the callee's `__init__` for initialization completeness. Also worth auditing: any function that returns a default value from a broad `except` block is a silent-failure surface. The shape `except Exception: return {}` is common and dangerous; if the except block doesn't log the error, the failure is invisible.

---

### 2. N/A count ≥5 in one audit = template drift signal; #1058 filed for agent-prompt-template staleness

**From:** PM `dev/2026/05/06/2026-05-06-1904-lead-code-opus-log.md` (commit `d88c5b2d`, #1053 audit-cascade prep); memory entry `feedback_audit_cascade_n_a_count_signals_template_drift.md`
**Relevant to:** Klatch (audit-cascade methodology; template maintenance discipline)

#1053's Phase 3 prompt audit generated 6 N/A flags (out of 42 requirements): single-session subagent, mechanical migration, no server state, no Cursor. PM's reaction: six exemptions from one audit suggested the template itself might be stale for the issue class, not just that this particular issue was unusual. Observation filed as a new memory entry and as **#1058** (agent-prompt-template hygiene review: stale Cursor Agent references and other drift).

**The meta-pattern:** audit templates accumulate drift from the outside — new issue types, new toolchains, deprecated workflows — and this drift shows up as repeated N/A flags before it shows up as a failed audit. The N/A count is a leading indicator, not a lagging one. Once the count crosses ~5 in a single pass, the template is worth reviewing, independent of whether the audit passed.

All 3 audit phases (#1053 issue / gameplan / prompts) passed with PM approval on the N/A items. Tomorrow's deployment: Lead Dev creates worktree, deploys subagent with prompt body (BEGINS/ENDS-marked in `dev/2026/05/06/1053-prompts.md`), runs post-execution audit before escalating to PM.

**Suggested action:** Klatch — if the AAXT template or any Klatch audit checklist regularly generates N/A flags for a class of work (e.g., pure-test issues, infrastructure-only changes), consider a variant template for that class rather than accumulating N/A overrides each time. The N/A accumulation is correctness overhead that grows silently.

---

### 3. Architect's soundness review fully closed: #1057 ships structlog + caplog incompatibility documented

**From:** PM `dev/2026/05/06/2026-05-06-1904-lead-code-opus-log.md` (commits `9a59518c` #1057 feat, `c0704ab` log update)
**Relevant to:** Klatch (structlog test patterns; review-completion discipline)

May 6 brief covered #1055 (items 1-3 of the Architect's 5-item punch list). Item 4 landed tonight: `ContextAssembler` test backfill for `f2408df6` (a no-tests commit on the context-contract path). Four tests added to `test_context_assembler.py` (22/22 pass):

- `TestUnknownCategoryFallback` × 2: UNKNOWN fallback path with/without user_id
- `TestContextContractEmptyDataWarning` × 2: warning emission verified

**Structlog + caplog incompatibility documented:** `caplog` (pytest's standard log capture) doesn't capture structlog-emitted records cleanly. Fix: patch the structlog logger directly. Lead Dev documented this pattern in the test docstring. Item 5 of the soundness review is #1015 (already tracked, pre-existing). Punch list fully closed.

**Suggested action:** Klatch — if Klatch uses structlog (or any structured logger), the `caplog`-doesn't-capture-structlog finding is directly applicable. The fix (patch the logger, not caplog) is straightforward but non-obvious. Worth adding to Klatch's test conventions if structlog is in the stack.

---

### 4. Ship #041 published: "The Methodology Closes Its Own Loops" — largest Ship to date

**From:** PM commit `219a47a` (Ship #041 canonical publish + LinkedIn syndicated); `docs/public/comms/drafts/published/weekly-ship-041-the-methodology-closes-its-own-loops.md`
**Relevant to:** Klatch Calliope (PM publication record; methodology-to-automation arc publicly documented)

Ship #041 published Wednesday evening (canonical pipermorgan.ai + LinkedIn syndication). Final title: "The Methodology Closes Its Own Loops" — PM's choice over CIO's proposed "From Diagnosis to Discipline in 24 Hours." HTML weight: 27,716 chars / 93 lines (largest Ship to date per Docs build log).

Coverage window April 24–30. Centerpieces: #992 ETHICS-ACTIVATE arc (5 months → 6 calendar days to close); Pattern-062 family completion (062 + 063 + 064 in one week); methodology-to-runtime latency under 24h in five distinct instances. Lead Dev note in the commit: two typos fixed per PM authorization (last week's → Last week; shiping → shipping). PP-002 framing retained as a deliberate public-prose voice departure ("critical vs. commodity" not "load-bearing") — memory entry pinned to explain the deviation.

M2 surface review reached full closure Wednesday (Topics 1-7 complete). Topic 7 final action: #471 Infrastructure parent broken out into discrete sub-issues (Conversation Repo → M3; OAuth-multi → M2f-or-M5 PM call; Learning Phase 3 → M4; TimeSeries duplicate of #371 closed), parent closed. #304 Notion investigation gated on a phase-1 doneness assessment before sub-epic placement.

**Suggested action:** Klatch Calliope — note the "deliberate public-prose voice departure" memo pattern: PM explicitly logged that "critical vs. commodity" (not the internal canonical term "load-bearing") was an intentional choice for public writing, then pinned a memory entry to explain it. For any Klatch public writing that diverges from internal terminology, the same explicit-deviation-plus-memory pattern prevents later confusion about whether the divergence was intentional.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/06/2026-05-06-1904-lead-code-opus-log.md` — full read; #1054 prod bug, #1056 test fix, #1057 ContextAssembler backfill, #1053 audit-cascade prep phases 1-3, #1058 filed, sign-off
- `piper-morgan-product/dev/active/m2-surface-review-decisions-2026-05-03.md` — tail read; Topic 7 final verdicts, #471 break-out plan, #304 gating
- `piper-morgan-product/docs/public/comms/drafts/published/weekly-ship-041-the-methodology-closes-its-own-loops.md` — partial read; Ship #041 content, PM voice choices
- PM commits `219a47a` (Ship #041 publish), `c0704ab` (#1057 log), `d88c5b2` (#1053 prep), `9a59518` (#1057 feat), `a374ba3` (#1054+#1056 fixes), `ac15a36` (M2 Topic 7 complete) — message + stat reads
- `klatch` — 48h git log empty; no new session activity; Iris walkthrough Surfaces 3-8 still pending
- `atlas`, `globe`, `one-job`, `optilisten` — 48h logs: brief deliveries / automated status prints only; no narrated insights
- `cuneo`, `weather`, `nyt-crossword` — 48h logs empty; skipped

**Not re-reported (covered in prior briefs):** #900 2h ship + pre-work-pays-dividends + cross-agent git collision (May 6); M2 unmapped-families triage 27 issues + M2f/M2g sub-epic map (May 6); #1055 –1518 LOC + Pattern-064 alive scaffolding (May 6); Six Issues Before Dinner published + Docs fact-check (May 6); M2e INTENT-COVERAGE arc #1042/#1039/#1040 (May 5); #1052 persistence gap audit-cascade catch (May 5); close-issue-properly 12-issue remediation (May 5); canonical-vocabulary-watch.md ships (May 5); Ship #041 workstream reviews filed (May 5); M2d complete + M2e gameplans (May 4); SDK 6 overdue + June 15 deprecation (May 4).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
