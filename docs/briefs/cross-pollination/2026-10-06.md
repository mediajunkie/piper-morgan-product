
# Cross-Pollination Brief — October 6, 2026

Two tool-behaviour traps that produce clean exits and wrong results: a macOS `sed` flag that silently becomes a filename suffix, and a CI health script that reports green while a gating check runs red for five days undetected.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. On macOS/BSD, `sed -i -E` silently uses `-E` as a backup-file suffix — the extended-regex flag is never applied, and the command exits 0 — Mediajunkie / Piper Morgan, Pard, commits `517ae03` · `ad6a6475a5`

**From:** Mediajunkie, surfaced to Piper Morgan via Pard's restart-gate sweep  
**Relevant to:** any project running shell scripts on macOS or a BSD host

Pard found an untracked file named `decisions.log-E` in a PM seat's working tree while running a binary-restart readiness check. The filename is the diagnostic: on macOS/BSD, `sed -i` takes a backup-suffix as its *argument*, not as a standalone flag. So `sed -i -E 's/…/…/' file` is read as *"edit in place, use `-E` as the backup suffix"* — the backup `file-E` is created, the `-E` extended-regex flag is never applied, and the regex runs as basic regex (BRE) instead of ERE. The command exits 0, produces no error, and the result looks like a success.

The safe forms on macOS are `sed -i '' -E '...' file` (empty-string suffix = no backup, then the flag) or `sed -E -i '' ...` (flag first). On Linux/GNU, `sed -i -E` works as expected.

Three related BSD-vs-GNU differences surfaced in the same week: `cat -A` output format, `\?` in a BRE, and this. If a script was written and tested on Linux, its `sed` calls are worth auditing before it runs on macOS.

**Suggested action:** Audit any cross-platform shell script using `sed -i` — check that the backup argument is explicit (or `''`) and that `-E` appears as a separate argument with no suffix between `-i` and `-E`. The `file-E` backup artifact is the fingerprint if you're checking existing repos.

---

### 2. A CI health script that hardcodes one workflow name misses every other gating check — Piper Morgan, CIO, commit `6c0116cb2b`

**From:** Piper Morgan, CIO  
**Relevant to:** any project with multiple CI workflows gating `main`

PM's duty-cycle Step 1e checked exactly one workflow (Code Quality / `lint.yml`) as the CI health signal. The Architecture Enforcement ratchet — a separate workflow that enforces structural constraints — ran red for 41 consecutive runs from 2026-10-01 to 2026-10-05 with nobody looking: the health script never read it.

The fix (`scripts/main-ci-status.sh`) derives the workflow list dynamically from `.github/workflows` by parsing each workflow file for `push` triggers that include `main`. Any new gating workflow is automatically covered the day it lands. The script also prints its denominator on every run: `"N workflows: G green, R red, U unmeasured"` — so a partial result is distinguishable from a full one.

The lesson generalises: a CI health check that hardcodes a name is a coverage claim for one file, not for "CI." Two fixes together close the gap: derive the list from the actual trigger config, and always state the denominator.

**Suggested action:** Audit your CI health checks for hardcoded workflow names. If you have more than one push-to-main workflow, the check should enumerate all of them — or at minimum, document explicitly which ones it omits and why.

## Sources Read

- **Klatch** — `docs/mail/` (30+ round-coordination memos, Oct 4–5); `.scratch/` restart-gate resolution (Pard's memo); probe rounds 333–338. No new transferable insights from probe work (Klatch-internal methodology); restart-gate resolution covered under Mediajunkie.
- **Piper Morgan** — `mailboxes/docs/inbox/` (Pard's BSD-sed memo); `scripts/main-ci-status.sh` (CIO fix `6c0116cb2b`); day-close session logs Oct 5.
- **Mediajunkie** — `logs/2026-10-05-pard-log.md` (BSD-sed discovery, restart-gate re-run; commit `517ae03`).
- **Globe** — `scripts/fire_check.sh` added (Oct 5, `9ffed27`): health block as a script with brief-age threshold derived from the delivery record. Application of 10-05 insight; not a new insight.
- **Weather** — session log (Oct 5); fire-prompt trim confirmed. Operational. Not brief-worthy.
- **One Job** — build 40 → 1.1.1 archived, ASC-verified, upload deferred to xian session. Operational. Not brief-worthy.
- **NYT Crossword** — automated status/remarkable prints. Not brief-worthy.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
