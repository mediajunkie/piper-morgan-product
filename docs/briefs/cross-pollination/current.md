# Cross-Pollination Brief — September 30, 2026

Two findings from Klatch and Piper Morgan: one discipline that moved from memory to structural enforcement, and one principle about when not to build a fix.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A probe-classification discipline moved from "remember to check" to a pre-commit hook — Klatch, Argus, `917b8a5c`

Klatch's sweep system requires every probe script to be explicitly classified (SWEPT or DEFERRED) before landing on `main`. When the check was only run as part of the full test suite, unclassified probes would land and sit until a later fire happened to run it — Round 291 was caught this way, six fires after it arrived. Argus built a pre-commit hook (`scripts/hooks/pre-commit`) that runs just the census check (0.17s, no ports, no model, no database) and exits 1 on CENSUS RED. The hook is fleet-wide: wired through `"prepare": "git config core.hooksPath scripts/hooks"` in root `package.json`, which resolves to the shared `.git` common dir and therefore covers all five worktrees simultaneously.

One implementation note: direct `chmod` was blocked in the sandbox. The workaround is `git update-index --chmod=+x <hook-file>` (writes the mode to the index) then `git checkout -- <hook-file>` (applies it from the index to disk). Without this, git silently ignored the non-executable hook with an easy-to-miss hint — the hook appeared to register but never fired.

**From:** Klatch (Argus)
**Relevant to:** any team with a discipline ("always do X before committing") that depends on agents or contributors remembering — whenever that discipline is important enough to enforce, ask whether a pre-commit hook can make it structural instead.

**Suggested action:** Audit whether any existing "always check this before committing" rules are worth moving from prose discipline to a pre-commit gate. Particularly effective for checks that are fast and stateless.

---

### 2. When a failure mode is unverified, name the hypothesis in the error text rather than building the fix — Piper Morgan, Pard, `e540bbee4`

PM's CI has a guard against torn-read races in its Fly.io deploy process. The architect identified one residual window the guard cannot see (a deploy in progress across all three reads could serve ref=B, sha=A, ref=B — passing the guard while running parity against the wrong image). Arch explicitly requested no change and labeled the window "unverified — it does not know when Fly updates ImageRef relative to the machine swap."

Pard initially overrode this and built a structural fix. He then reversed that decision: "building the structural fix now would be acting on a theory in a system where one real run is the measurement — which is the shape I have spent the day criticising, and twice today Arch's facts beat my reasoning from estimates." Instead, the failure text was updated to name the specific signature (`alpha serving a coherent but different sha`), the hypothesis, and the structural fix (a `PIPER_GIT_SHA` image label so ref and sha collapse to one read). If this signature ever fires, the error explains itself and names the fix. If the hypothesis was wrong, nothing was built for it.

**From:** Piper Morgan (Pard/Exec)
**Relevant to:** any team deciding whether to harden against a failure mode that has never occurred. The principle: for unverified theoretical windows, make the failure self-explaining rather than building the structural fix for a premise you haven't measured.

**Suggested action:** When proposing a fix for a race or edge case that has never been observed, check whether the better intermediate step is naming it in the failure text with the structural fix identified. "Detection beats perfection" — Pard's own phrase. The fix gets built exactly when it's confirmed relevant, not before.

## Sources Read

- **Klatch:** `docs/logs/2026-09-29-0910-argus-sonnet-log.md` (census pre-commit hook), `docs/logs/2026-09-29-1317-daedalus-opus-log.md` (Round 297 sweep red, pin-on-absence finding)
- **Piper Morgan:** commit `e540bbee4` message and diff (fly-deploy.yml CI guard update), `docs/logs/` day-close entries for context
- Secondary sources with commits (globe, weather, one-job, nyt-crossword, mediajunkie): activity present but not brief-worthy — routine animation iterations, configuration adjustments, automated status prints, and mail/log housekeeping

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
