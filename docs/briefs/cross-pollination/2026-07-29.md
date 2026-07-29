
# Cross-Pollination Brief — July 29, 2026

Two findings from Piper Morgan worth carrying across the ecosystem. First, a non-obvious bash trap that caused a verification guard to report "no match" even when it had matched — caught while verifying yesterday's m-44 heartbeat fix, and independently reproduced by Globe on the same day. Second, a structural finding about project-instruction files: CLAUDE.md should hold the operative rules agents need at session load, not the investigation records that produced them — HOST found 12.8% of PM's file was hooks-investigation prose containing neither of the two rules the investigation yielded.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### `grep -q` in a pipeline under `set -o pipefail` reports no-match even when it matched

**From:** Piper Morgan (CIO session log `dev/2026/07/28/2026-07-28-1037-cio-code-log.md`, Fire 2). Independently corroborated by Globe the same day (Tessera session log, `.venv` build step).

**Relevant to:** Any project using shell scripts, hooks, or automation with `set -o pipefail`

`grep -q` is designed to exit the moment it finds its first match — which is exactly what makes it efficient and exactly what bites you under `pipefail`. When `grep -q` exits early on a match, the still-writing producer (e.g. `git log`) receives a **SIGPIPE** and also exits non-zero. Under `set -o pipefail`, the pipeline's exit status is the non-zero status of the first failed stage — which is the producer, not `grep`. So the whole pipeline exits non-zero, and `$?` reads as "failure" (= "no match") even though `grep` found what it was looking for.

In the CIO's case, the guard `git log --format="%s" | grep -q "($ROLE)"` was meant to check whether the current fire had already committed work. It reported NO MATCH because it had matched — timing-dependent, because the race between producer output and `grep -q`'s early exit only manifests when the producer writes fast enough to be mid-write when SIGPIPE arrives. The guard passed in isolation and failed inside the script. Had it shipped, ten agents would have received an idempotence guard that wrote duplicate entries under the exact condition it was meant to suppress.

Globe hit the same shape the same evening: a build command piped into `tail` masked a build failure behind `tail`'s own exit code (0). Globe's log notes this as "the exact exit-code-masking gotcha" — a related but distinct manifestation of pipe exit codes hiding what actually happened.

**The fix:** never pipe into `grep -q` when you need the match verdict. Capture the output into a variable, then test against the variable:
```bash
out=$(git log --format="%s" --since=...)
echo "$out" | grep -q "($ROLE)" && ...
```
This avoids the SIGPIPE race entirely. The same principle applies to any `... | grep -q` under `pipefail` — or any `... | head -N` pattern where you need the producer's exit code.

**Suggested action:** Audit shell scripts and hooks for `... | grep -q` patterns under `set -o pipefail`. Where found, refactor to capture-then-test. Pay particular attention to idempotence guards and pre-commit hooks — these are high-stakes, rarely manually tested once deployed, and may appear to work in isolation while failing under script conditions.

---

### Project-instruction files (CLAUDE.md) should hold operative rules, not investigation records

**From:** Piper Morgan (HOST session log `dev/2026/07/28/2026-07-28-0707-host-code-log.md`, Pass 3)

**Relevant to:** Klatch, DinP, any project with a growing CLAUDE.md

HOST ran a completeness pass on PM's CLAUDE.md and found it 26% heavier than a recent refactor had left it — with 6,923 bytes (12.8% of the file) occupied by a single hooks investigation. The investigation record was scrupulously honest: four refuted models, strikethrough corrections, and a "what is actually established" section. **The file contained neither of the two operative rules the investigation produced.** An agent loading the file at session start gets a thorough reasoning record and no actionable guidance; the rules that actually govern hook behavior were filed elsewhere.

Six of eight currently-active behavioral norms were absent from the file entirely. HOST added the two safety-critical ones directly (memory deletion is irreversible; hooks are advisory not a control) and proposed a compaction that recovers ~11% of the file by replacing the investigation record with a pointer to the memory pin that carries the full reasoning.

The structural recommendation: CLAUDE.md's primary job is session-load orientation — it needs to carry rules an agent must follow at the moment it wakes, not the history of how those rules were reached. Investigation records, refuted models, and reasoning chains belong in a separate surface (memory, a linked doc, or a dedicated findings file). The pattern of separating load-time content from record content already exists in PM's memory architecture (index file pointing to topic files) and in session logs vs. session log summaries — CLAUDE.md is the one loaded surface that hasn't adopted it.

**Suggested action:** When a CLAUDE.md grows, run a quick audit: for each section, ask whether an agent *needs this at session load* or merely *benefits from being able to trace how the rule was established.* If the latter, the content belongs in a linked reference (memory pin, methodology doc, separate findings file) — with a one-line summary and pointer in CLAUDE.md, not the full record. The signal that this has happened: a section describes a complex investigation but doesn't end with a clear "the rule is X" statement. Test by reading only the section header and the last paragraph — if the operative guidance isn't there, it isn't load-time content.

---

## Sources Read

- **Piper Morgan** — 56 commits in 48h. Key reads: CIO session log `dev/2026/07/28/2026-07-28-1037-cio-code-log.md` (three fires: threshold-was-a-no-op self-correction; heartbeat shipped with `grep -q` guard bug caught pre-release; migration-checklist Rule 0 from PM trust conversation). HOST session log `dev/2026/07/28/2026-07-28-0707-host-code-log.md` (freeze-check dead-belt incident; CLAUDE.md Pass 3 finding; tester silence is not a measurement). Two insights elevated.
- **Globe** — 10 commits in 48h. Key read: Tessera session log `logs/2026-07-28-tessera-log.md` (Amber migration day; pip build failure masked by `| tail`; m-44 applied to render summary output and to PNG integrity check). Corroborating instance for pipe-exit-masking finding.
- **Klatch** — 2 commits: cross-pollination brief deliveries only. No new Klatch-internal methodology.
- **DinP (hub)** — Brief deliveries, no new session logs.
- **One Job** — 5 commits: git identity convention adopted; TESTING.md correction; REQUIREMENTS.md update; ATTENTION-ROLLUP. Operational; no cross-project methodology.
- **Mediajunkie** — 10 commits: Coral and Tessera migrations coordinated; ezone deployed; Rackspace rescue gate. Operational coordination; no cross-project methodology.
- **Atlas, Cuneo, Optilisten, NYT-Crossword** — no commits in 48h window.
- **Cookie Monster** — brief deliveries only.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
