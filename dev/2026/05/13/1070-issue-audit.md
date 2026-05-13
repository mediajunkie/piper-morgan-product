# #1070 MULTI-TURN-HARNESS — Phase 0 audit

**Issue**: [#1070](https://github.com/mediajunkie/piper-morgan-product/issues/1070) — Multi-turn evaluation harness for canonical retest
**Scope**: M2-discovered (testing-infra cohort per #1064 P2 list)
**Branch**: `claude/1070-multi-turn-harness` (worktree `piper-morgan-product-1070`)
**Date**: 2026-05-13

---

## Pattern-067 check

- Existing harness: `dev/2026/05/09/canonical-retest-run7.py` (918 lines). Single-turn evaluation only — one HTTP POST per query, one judge call per response.
- `CANONICAL_QUERIES` corpus: 61 entries as 5-tuples `(query_num, query_text, category, expected_routing, known_issue)`. No multi-turn field.
- `JUDGE_SYSTEM_PROMPT` rubric assumes a single response. Q49 `/standup` returns "Good morning! Ready for your standup?" which is the **intended opening** of the #900 3-part flow — but the judge sees only the bare greeting and scores it R=1 C=0 T=1 = FAIL across Runs 4–7.

**Conclusion**: NEGATIVE for the helper. Issue body's "methodology limitation, not a bug in /standup" framing is accurate. Cleanly greenfield methodology work.

---

## Existing infra inventory

### `canonical-retest-run7.py` shape

- **L93**: `CANONICAL_QUERIES = [(query_num, query_text, category, expected_routing, known_issue), ...]`
- **L187**: `JUDGE_SYSTEM_PROMPT` — 60 lines of rubric + calibration examples; expects `Query: ... / Piper's response: "..."` shape
- **L257** `judge_response(query_text, response_text, anthropic_client)`: single-call evaluator
- **L473** `run_query(...)`: one HTTP POST to `INTENT_ENDPOINT` with `{message, session_id}`; one judge call
- **L796** `main()`: iterates corpus, runs each query, accumulates results
- **L508**: `session_id` is per-query namespaced `f"{SESSION_ID_PREFIX}-q{query_num}"` — session continuity ALREADY exists, just not exploited
- **Q49** (L162): `(49, "/standup", "Slack", "action", None)` — the canonical multi-turn surface

### Server-side multi-turn support

`/standup` is one of several existing multi-turn flows in the codebase:
- **#900 standup**: 3-part flow (greeting → mode-pick "quick" / "detailed" / "no" → standup content)
- Action-confirm flows: e.g. `close issue #123` → "yes, close #123" → confirmation
- Conversation-context queries: floor retains turn history via `session_id` already

The send-side already keeps a consistent `session_id` per query — server keeps state across turns within the same session. The harness just doesn't send follow-ups.

---

## Open design questions

### Q1 — Fixture format shape

Current corpus is a list of 5-tuples. Adding multi-turn requires either:

- **(a) 6-tuple with optional `follow_ups`**: backward-compatible if we default to `None` (`(49, "/standup", "Slack", "action", None, ["quick"])`). Simplest diff to the corpus.
- **(b) Migrate to `@dataclass CanonicalQuery`**: cleaner, named fields, easier to extend (judge-rubric-variant, multi-turn flag, etc.). Migration touches all 61 entries.
- **(c) JSON/YAML fixture file**: corpus moves out of Python; harness reads at runtime. Cleanest for non-Python authoring, biggest diff.

**Recommendation**: **(a) 6-tuple** for first ship. Smallest blast radius — `None` for the 60 single-turn queries; only Q49 gets a non-None follow-up. Dataclass migration (b) is the right *eventual* shape but not blocking — file as follow-up. (c) is over-engineered for our scale.

### Q2 — Replay step depth + branch coverage

`/standup` has 3 branches (quick / detailed / no). For first ship:

- **(a) Single follow-up "quick"**: minimum to make Q49 multi-turn — verifies the harness works + Q49 sees the full standup output
- **(b) All 3 branches as separate fixtures (Q49a/b/c)**: 3× the API cost but covers the branch matrix
- **(c) One per branch but only "quick" is asserted PASS; "no" expected as cancel-shaped, "detailed" expected as longer response**: more comprehensive but requires per-fixture verdict criteria

**Recommendation**: **(a) "quick" only** for first ship. Validates the methodology. (b)/(c) are follow-ups if user feedback says branch coverage matters.

### Q3 — Judge approach for multi-turn

- **(a) Single judge call with full transcript**: pass the entire `[U1, A1, U2, A2]` sequence; rubric evaluates the conversation as a whole. Simpler. Single judge call cost per multi-turn query.
- **(b) Per-turn judge calls + aggregation rule**: each (user, assistant) pair scored separately, combined verdict (min? avg?). More granular but harder to interpret + 2× cost.

**Recommendation**: **(a) single call with full transcript**. Multi-turn quality is emergent from the sequence; per-turn scoring loses coherence info. Lower cost. Rubric becomes "evaluate the conversation as a whole; PASS requires the user's INITIAL question was meaningfully answered through the exchange."

### Q4 — Script versioning: in-place upgrade vs new run

- **(a) Upgrade `canonical-retest-run7.py` in place**: extend it to optionally do multi-turn
- **(b) Spec a `canonical-retest-run8.py`** that supersedes run7
- **(c) New `canonical-retest-multi-turn.py`** as a separate harness that only runs multi-turn queries

**Recommendation**: **(b) `canonical-retest-run8.py`** — preserves run7 as the historical baseline (matches the v2/v3/run4/run5/run6/run7 lineage), introduces multi-turn as a new generation. Future runs build on run8. (c) splits the corpus and complicates aggregate reporting.

### Q5 — Scope minimum vs broader

The AC has 5 items. Sizing:

- **(I) Minimum viable** (~1.5 hr): fixture format extension (6-tuple) + replay loop in run8 + multi-turn judge prompt variant + Q49 fixture with "quick" follow-up + verify Q49 verdict on Q49 only
- **(II) AC-full** (~3 hr): Above + document fixture format in canonical-query-test-matrix-v3.md + add 1 conversation-continuity multi-turn fixture + 1 action-confirm flow fixture
- **(III) AC-full + run full corpus** (~5 hr): II + run the full 61-query corpus through run8 to verify no regressions on single-turn queries

**Recommendation**: **(I) minimum first**, then PM-decision whether to extend. Q49 verdict improvement is the success criterion stated in the AC.

### Q6 — Skip single-turn regression run?

Run8 supports single-turn (when `follow_ups is None`). If the harness is built right, run8 on the full corpus should match run7's output for the 60 single-turn queries.

- **(a) Skip the verification run** — trust the implementation + unit tests
- **(b) Spot-check 5 single-turn queries** with both run7 and run8, confirm output identical (~10 min)
- **(c) Full 61-query run** for regression baseline (~30 min + judge API cost)

**Recommendation**: **(b) spot-check 5**. Cheap, catches obvious bugs. Defer full run to a deliberate "Run 8 baseline" exercise.

### Q7 — Documentation

Per AC: "Multi-turn fixture format defined + documented in canonical-query-test-matrix"

- **(a) Add an `## Multi-turn fixtures` section to v3** (~10 min during Phase 1)
- **(b) Defer doc to follow-up** — code is the doc for now
- **(c) Spec a v4 of the matrix doc** if multi-turn is large enough to warrant version bump

**Recommendation**: **(a)** — small enough to do inline. Future agents reading the matrix doc need to know multi-turn exists.

---

## Suggested gameplan shape (conditional on PM picking recommended answers)

- **Phase 1** (~30 min): copy `canonical-retest-run7.py` to `canonical-retest-run8.py`; extend tuple format to 6-tuple with optional `follow_ups`; backward-compatible iteration (handles 5-tuples by treating missing 6th as `None`).
- **Phase 2** (~20 min): extend `run_query` to do send-receive loop for follow-ups, accumulate transcript with structured `[Turn N] User: / [Turn N] Assistant: ...` format.
- **Phase 3** (~20 min): multi-turn `JUDGE_SYSTEM_PROMPT_MULTITURN` (or a single rubric that adapts based on transcript length); update `judge_response` to take optional transcript instead of single response.
- **Phase 4** (~10 min): add Q49 `/standup` follow-up `["quick"]` in corpus.
- **Phase 5** (~10 min): spot-check 5 single-turn queries with run8 vs run7 to verify backward-compat.
- **Phase 6** (~15 min): run Q49 through run8 only, confirm verdict improves from FAIL toward PASS/MARGINAL.
- **Phase 7** (~10 min): add `## Multi-turn fixtures` section to `canonical-query-test-matrix-v3.md`.
- **Phase 8** (~5 min): commit + merge + close.

**Total**: ~2 hr (revising the 3-5 hr estimate down — once the existing structure is mapped, the extension is mostly mechanical).

---

## Risks

1. **Q49 might still FAIL after multi-turn**: if the 3-part standup output itself has quality issues independent of the methodology gap, Q49's verdict won't improve. We'd discover a real /standup bug masked by the methodology limitation. That's a useful discovery, not a fix-failure.
2. **Judge calibration**: the multi-turn rubric needs to NOT over-weight the opening turn vs the substantive turns. PM may want to spot-check the first multi-turn judge calls for calibration.
3. **Cost**: each multi-turn query is 2+ API calls instead of 1. With ~3 multi-turn queries in initial scope, cost impact is small (~$0.02 per retest run).
4. **Session-state leakage**: server-side session state is per-query (`session_id-q{N}`). Multi-turn queries reuse the same session_id. If a previous multi-turn run leaves state in the server, the next run sees it. Mitigation: rotate `SESSION_ID_PREFIX` per retest run (already the case via timestamp prefix).

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1070 |
| Pattern-067 check | ✅ NEGATIVE — body's framing accurate |
| Body-vs-reality | ✅ verified |
| Existing infra mapped | ✅ run7 structure + judge prompt + corpus shape |
| Server-side support verified | ✅ session_id already per-query; 3-part standup exists |
| Scope questions surfaced | ✅ Q1–Q7 |
| Risk assessment | ✅ Q49-might-still-FAIL, calibration, cost, state-leak |
| Recommended path | ✅ ~2 hr minimum viable (8 phases) |

---

## STOP — awaiting PM disposition on Q1–Q7

Most have clear recs. Most consequential: **Q1 (format shape)** and **Q5 (scope minimum vs broader)**.

— Lead Developer
