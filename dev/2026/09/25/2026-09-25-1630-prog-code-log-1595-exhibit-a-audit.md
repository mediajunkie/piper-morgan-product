# Session Log — Coding Agent (prog), 2026-09-25 16:30

**Role**: Coding Agent (prog)
**Model**: Sonnet
**Dispatched by**: Lead Developer
**Task**: #1595 Exhibit-A completeness audit — Phase-0 inversion corpus
**Worktree**: /Users/xian/Development/piper-morgan-worktrees/lead (branch claude/lead-cycle)
**Constraints**: NO commit/stage/index touches (Lead owns commit). NO LLM calls anywhere.

## Task summary

Audit whether the 8 Exhibit-A catalog issues (#1471, #1490, #1521, #1527, #1492-partial,
#1529, #1530, #1488-class) and every `pin:` row in `tests/fixtures/routing_corpus_1283.yaml`
are covered by the generated Phase-0 corpus (`tests/fixtures/inversion_corpus_phase0.yaml`,
built by `scripts/build_inversion_corpus_phase0.py`). Add missing HAND_ROWS entries with
citations, regenerate, verify dry-run scripts + tests.

## Work log

- 16:30 Session log created. Starting with proposal doc read (confirmed 8-issue catalog) and
  gh issue view for each of the 8 issues.
- 16:50 Full body+comments dump for #1471/#1490/#1521/#1527/#1492/#1529/#1530/#1488 pulled via
  `gh issue view N --json body,comments`. Searched `dev/2026/08/08/` for the literal 13:19-13:24
  transcript (`git grep -ln "13:19\|13:2[0-4]" -- dev/2026/08/*`) — the only hits were unrelated
  duty-cycle fire timestamps (PPM/Comms 13:20/13:22 cron fires, not the PM chat transcript).
  FINDING: no dev/ session log carries the literal Exhibit-A transcript text; the GH issue
  comments are the only extant record (PM live T4/T5/T6 timestamps cited directly in comments
  on #1492/#1529/#1530, matching 13:19/13:22 2026-08-08 v38 exactly).
- 17:10 Built the coverage table against tests/fixtures/inversion_corpus_phase0.yaml (564 lines)
  and its two structured sources (routing_corpus_1283.yaml, surface1-counterfactual-results doc).
  Confirmed "what reminders do I have?" present at line 213 (source probe-row-11, expected REVIEW).
  Found the real `pin:` construct is services/intent_service/chat_pointers.py's CHAT_POINTERS
  dict ("pin:reminder-query", 1 row total) — task's grep target `test_routing_corpus*.py` doesn't
  exist (actual file: test_routing_vocabulary_1283.py, no "pin" hits); routing_corpus_1283.yaml
  has 2 explicit "regression pin" comment rows, both present in generated corpus. Identified 8
  missing/mislabeled Exhibit-A phrasings (see report) across #1490, #1492 (x3), #1529 (x2),
  #1530, #1488.
- 17:35 Added 8 HAND_ROWS entries to scripts/build_inversion_corpus_phase0.py with citations.
  #1488's literal PM phrase is redacted in the issue (genuinely unrecoverable) — used the real,
  measured, non-fabricated phrase from #1677's probe table instead ("add todo buy oat milk",
  pinned in test_inversion_write_allowlist_1677.py:101), citation makes clear it's the mechanism
  probe, not PM's exact words.
- 17:50 `ruff format` (1 file left unchanged) + `ruff check --fix` (all checks passed) on the
  builder. Regenerated: `venv/bin/python scripts/build_inversion_corpus_phase0.py` → 108→116
  rows (59 REVIEW). `git diff --stat` confirmed exactly 40 insertions, 0 deletions — purely
  additive, only the 8 new rows changed.
- 18:00 Ran both dry-mode validators (env-stripped per CLAUDE.md): `inversion_phase1_shadow_score.py
  --dry-run` → "dry-run complete: corpus + grammar + selections validated, no LLM calls." and
  `inversion_phase2_gate.py --dry` → "phase0 corpus: 116 rows (untouched)... dry run complete...
  No LLM calls made." Both confirm the corpus loads clean and no LLM calls occurred.
- 18:05 Searched for tests pinning the corpus per the task's grep target
  (`git grep -ln "inversion_corpus_phase0" -- tests`) — only the two yaml fixtures matched, no
  .py file. Broadened to `phase0|phase_0` across tests/ and found
  tests/unit/test_inversion_phase2_gate_1595.py, which loads the real phase0 corpus via
  `inversion_phase0_baseline.load_corpus()` in `test_phase0_corpus_is_untouched_by_extension`.
  Ran it: `pytest tests/unit/test_inversion_phase2_gate_1595.py -q -p no:cacheprovider` →
  **22 passed in 0.53s**, exit 0. Also spot-checked `load_corpus()` directly in a REPL:
  116 rows, all 8 new phrases present verbatim.
- 18:10 Session complete. Handing back to Lead. NOT committing/staging per constraint — all
  changes left in the worktree for Lead to review and commit.

## Discovered work / issues filed

None — this was a completeness audit of test fixtures, not implementation work. No new
tracking issues warranted; findings (mislabeled citation on the pre-existing "what projects
do I have?" row; missing dev/-log transcript record) are reported inline to Lead, not filed
as separate GH issues, since they're corpus/documentation-accuracy notes the Lead can fold
into #1595's own closure rather than standalone bugs.

## Memory & briefing surfaces referenced this session

**Referenced**:
- CLAUDE.md server-launch env-var stripping guidance — used verbatim for the dry-run/test
  invocations (`env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
  -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433`).
- CLAUDE.md "name the layer, state the denominator" (m-43/m-44) — shaped how findings are
  reported below (per-category before/after counts, explicit "no test file found" honesty
  rather than silently skipping step 6).

**Loaded but not referenced**: the mailbox/worktree/sign-off discipline sections (no mailbox
or sign-off work in scope — prog subagents doing quick fixture edits report back via
SubagentHandback per the dispatch instructions, not mail).

**Wanted but not found**: a dev/ session log carrying the literal 2026-08-08 13:19-13:24
PM transcript text — does not exist; the GH issue comments are the only record. Worth flagging
to Lead/Docs as a documentation gap if the transcript is ever needed verbatim again.
