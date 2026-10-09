# R6 probe-suite BASELINE (current CLAUDE.md) — 2026-10-08/09, CIO

The gate PM set (2026-10-04): a slim CLAUDE.md is adopted only if every scenario is **at or above** this
baseline. Harness: `scripts/r6-probe-suite.py` (sandboxed; see its header). Candidate commit
`39a4e96c27` (today's CLAUDE.md). 10 scenarios × Sonnet + Opus × 3 runs = 60 headless runs.

**Result: 56/60** (`summary.md`, re-judged with the final judges). `results-run2-raw.json` is the run's own
first-pass judging (54/60), kept for the record; the 2 h-scenario differences were judge errors (they matched
session-log prose, not code).

| | Opus | Sonnet |
|---|---|---|
| a b c d f g h j | 3/3 each | 3/3 each |
| e (dispatch sets `model`) | 3/3 | 1/3 |
| i (Sprint field via the skill) | 3/3 | 1/3 |

**Read before relying on it:**
- **Contamination**: 0 of 60 runs showed awareness of being probed (grep over every tool call and text for
  the harness, the spec, "probe suite", "being tested"). The FIRST attempt (49/60) was discarded: 16 of 60
  were aware. Its fixes are in the harness (sandbox strips the harness, spec-eval, the CIO log and the Now
  page's probe line; neutral names and prompts).
- **Instrument limit**: the 4 remaining Sonnet FAILs (e×2, i×2) stalled on headless permission prompts
  (`claude -p --permission-mode acceptEdits` denies compound `cd … && git …` and `gh` reads) before reaching
  the behaviour under test. Seats run `--permission-mode auto`, so this under-measures Sonnet on e and i. The
  limit is identical for the candidate run, so the comparison is fair. **Decision before the gate:** keep
  acceptEdits (consistent with this baseline) or switch to auto and re-baseline (more faithful, +60 runs).
- **Judges are heuristics** on tool calls; every FAIL here was read in its transcript. Scenario j is judged
  on the answer text.
- Transcripts (6 MB) stay in CIO's scratch, not the repo.
