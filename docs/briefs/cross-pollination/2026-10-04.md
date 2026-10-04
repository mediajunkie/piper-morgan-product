# Cross-Pollination Brief — October 4, 2026

Three findings today. Pard (Mediajunkie) diagnosed and documented a cloud UTC timezone trap that is quietly misdating files across the constellation. Piper Morgan's Lead Dev caught a pytest configuration leak that caused CI to surface only one test failure per run. Pard also produced a transferable pattern for making compliance checks over historical corpora useful by distinguishing acknowledged old violations from genuine new ones.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Cloud sessions run UTC with no timezone set — bare `date` returns tomorrow's PT date after 17:00 — Piper Morgan / Mediajunkie, Pard, commit `d789e3544`

Cloud containers have no `TZ` environment variable. A bare `date` call returns UTC regardless of any timezone intent baked into surrounding code or the agent's assumed context. After 17:00 PT, UTC is already in the next calendar day — so any filename, log entry, dateline, or session log stamped with `$(date '+%Y-%m-%d')` will carry tomorrow's PT date. It looks like a future-date error but is actually a timezone-of-execution error.

Pard diagnosed this after filing two 2026-10-03 memos under the date 2026-10-04 in a cloud session — then traced the same trap to 62 files in Piper Morgan alone, 27 in DinP, 8 in Klatch, across the past 7 days. Cairn (Optilisten) first identified this pattern on 2026-09-26.

The fix is one line in any context that produces dates: `TZ=America/Los_Angeles date '+%Y-%m-%d'`. Mediajunkie's `CLAUDE.md` now carries this as a standing rule; DinP's `convention-dates-are-pacific.md` has the full mechanic. A fleet detection arm (`check-datestamps.sh`) scans all repos in the constellation.

**Suggested action:** Any project running agents in cloud sessions should add `TZ=America/Los_Angeles date '+%Y-%m-%d'` everywhere a date string is constructed for filenames, log entries, or commit messages. A bare `date` in a cloud container is not a safe default. Check recent cloud-session commits for misdated files.

**From:** Piper Morgan, Pard memo `d789e3544`; Mediajunkie `CLAUDE.md` `convention-dates-are-pacific.md`

**Relevant to:** Every project in the constellation that runs agents in cloud sessions (all of them).

---

### 2. Local pytest fast-fail flags in `pytest.ini` leak to CI without an explicit override, surfacing only one test failure per run — Piper Morgan, Lead Dev, commit `88258f25d`

Piper Morgan's `pytest.ini` carries `-x --maxfail=1` — a developer convenience that stops a test run on the first failure, so local iteration is fast. These flags are part of the `addopts` setting and propagate to every `pytest` invocation, including CI smoke runs, unless the CI step explicitly overrides them.

The consequence: each CI run exposed exactly one failing test, required a fix, re-ran, exposed the next failure, and so on. The debugging loop stretched across multiple cycles because the true scope of breakage was hidden one failure at a time.

The fix: the CI smoke step now overrides `addopts` inline, stripping `-x` and `--maxfail=1` while keeping the flags that belong in CI (`--ignore` paths, `--import-mode=importlib`):

```
python -m pytest -m smoke -q --tb=short \
  -o addopts="--ignore=tests/archive --ignore=*/archive/* \
              --ignore=services/integrations/*/tests \
              --ignore=services/mcp/server/test_*.py \
              --ignore=dev/ --import-mode=importlib"
```

**Suggested action:** Any `pytest.ini` or `pyproject.toml` that sets `-x` or `--maxfail` in `addopts` will silently pass those flags to CI. Audit whether your CI invocations override `addopts`, or move the local fast-fail flags out of `addopts` into a developer-only config file (e.g., `pytest-local.ini`) that CI never loads.

**From:** Piper Morgan · Lead Dev; commit `88258f25d` (`.github/workflows/test.yml`)

**Relevant to:** Any project using pytest with convenience flags in `addopts` that has separate CI and local test invocations.

---

### 3. Compliance checks over historical corpora need an acknowledgment ledger keyed on full commit hashes — Mediajunkie, Pard, commit `8e1ee55`

Pard's datestamp-check arm ran against the Mediajunkie corpus and flagged historical misdated files created before the fix landed. The check turned red. But the important signal — "dispatch did it again tonight" — was now indistinguishable from "dispatch's old files are still in frame." The check was correct about the violations; it was useless for detecting recurrence.

The solution is an acknowledgment ledger (`docs/datestamp-acknowledged.tsv`) keyed on `repo + path + full commit hash`. Key design choices:
- **Full hash, not abbreviated:** git auto-sizes abbreviations as a repo grows; an `%h`-keyed row will stop matching once the repo outgrows it. Full hash only.
- **`notified` field mandatory:** any row without it is rejected and the artifact is still flagged. The check refuses to silently accept an incomplete acknowledgment.
- **No pre-authorization of future files:** a hash cannot exist before its artifact does — no row can acknowledge a violation that hasn't happened yet. A recurrence produces a new hash and goes red.
- **Acknowledged count printed on every run including green:** the green state carries evidence ("8 acknowledged, 1 note"), not just a clean exit.

The shape mirrors `cpu-exceptions.tsv` (for bounded, expiry-carrying exceptions), so the repo already had the idiom; the key difference is that history acknowledgments carry no expiry — the structural guard (hash keying) replaces the time limit.

**Suggested action:** Any project running continuous compliance checks against a corpus that predates the check will eventually hit this problem — the check turns red because of old artifacts it can't retroactively fix, and new violations become invisible. Before a check goes live, design its acknowledgment path: a separate ledger with immutable keys, a required `notified` field, and output that explicitly counts acknowledged entries rather than silently treating them as clean.

**From:** Mediajunkie · Pard; commit `8e1ee55` (`docs/datestamp-acknowledged.tsv`, `scripts/check-datestamps.sh`)

**Relevant to:** Any project maintaining automated compliance checks over a corpus that includes historical artifacts.

---

## Sources Read

**Primary (detailed scan):**
- Klatch: Rounds 321–326 (active; multi-root session scanner work — no brief-worthy findings this window)
- Piper Morgan: session logs, commit log, mailbox traffic (48-hour window)
- Mediajunkie: commit log and `8e1ee55` commit detail

**Secondary (commit log checked, not-brief-worthy or quiet):**
- Globe: active (render work, crash-resilient supervisor `render_supervised.sh`) — not brief-worthy this window relative to stronger findings
- Weather: 5 commits, no-ops and brief deliveries
- One Job: 7 commits, routine duty fire work
- NYT Crossword: 15 commits, routine status prints
- Atlas, Cuneo, Optilisten: no new commits in window

---

*Generated by the Cross-Pollination Intelligence Sweep · Design in Product*
