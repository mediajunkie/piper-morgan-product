
Three findings today — all variations on the same failure shape: a guard, test, or probe that is aimed correctly but doesn't hit what it appears to target. One is a late-night production incident; the other two are test-harness defects caught before they caused live damage.

---

## Key Insights

### 1. A post-commit hook that calls a script that commits will recurse unless the hook can recognize its own output — Piper Morgan hooks pilot

**From:** Piper Morgan (Pard, hooks pilot incident — 2026-09-21 22:37–23:13 PT)
**Relevant to:** Any project using post-commit hooks that run scripts capable of committing

Piper Morgan's duty-cycle hooks pilot installed a post-commit hook that called `duty-cycle-heartbeat.sh`. The heartbeat script's "quiet path" — triggered when the seat had been idle long enough — commits a one-line marker file with a message like `hb-last-invoked(cio): suppressed …`. That marker commit fired the post-commit hook again. No re-entry guard existed in either file. Because the hook ran synchronously, the chain was a nested stack rather than a queue: `git commit` → hook → heartbeat → `git commit` → … one level approximately every three seconds. By the time it was discovered, the chain held 2,882 nested processes. The hook was disarmed manually at 23:10 PT; the chain was killed at 23:13. As the inner levels unwound after the disarm, the heartbeat's own delivery step — which pushes `HEAD:main` — ran and pushed 967 marker commits to `origin/main`.

Two defects, both required before re-arm:

1. **No re-entry guard.** The hook should skip when the triggering commit's message matches the marker prefix (`hb(` or `hb-last-invoked(`), or the hook and heartbeat should check a shared exported variable (`PIPER_IN_POST_COMMIT=1`) before committing. Either alone stops the loop.
2. **A hook that pushes.** The heartbeat's quiet-path delivery step pushes to origin from inside a post-commit context. Even with a re-entry guard, this races every real push on the belt. Quiet-path markers should not push from inside a hook; the fire's own delivery step should carry them.

The smoke test that ran before installation exited before reaching the guard — it ran on `main`, a path the guard never touches — and reported success. It was a test that could not have failed.

**Suggested action:** Before installing a hook that calls any external script, check whether that script can commit. If it can, add a message-prefix or environment-variable re-entry guard in both files before the first install. And smoke tests for hooks should exercise the actual guarded code path, not an alternate path that exits early.

---

### 2. `import.meta.url` names the file that is currently executing, not a fixed filename — Klatch Round 248

**From:** Klatch (Daedalus, Round 248)
**Relevant to:** Any project using `import.meta.url` to self-exclude a file from a population scan

Klatch's test coverage probe used `path.basename(fileURLToPath(import.meta.url))` to exclude itself from the set of files it was measuring. When the probe file is run from its tracked location, this works: the probe's own name is excluded, and the population is correct. But when a copy of the probe is run from a different filename — as happens when the round's author makes a working copy to experiment with — the exclusion uses the copy's name. The original tracked file has a different name and is not excluded: it re-enters the population the copy is supposed to be measuring. The guard was written assuming "the file currently executing" and "the file being excluded" are the same object; they are not when copies exist.

The result was that `probe-round223.mts` sat red for four days because its population count was pinned to `=== 21 + 2` (a hard equality, not a floor), and the actual population had grown to 28. The self-exclusion guard was not incorrect on its own terms — it excluded the running file — but the running file was a copy, and the original was silently included in the count.

**Suggested action:** Self-exclusion guards using `import.meta.url` are safe only when there is exactly one copy of the file. If a probe or script may be copied for experimentation, exclude by the tracked path (relative to the repo root, resolved at the time the tracked file was committed) rather than by the name of whatever is currently executing.

---

### 3. ANSI terminal escape codes corrupt regex matching against test output — Klatch Round 249

**From:** Klatch (Daedalus, Round 249)
**Relevant to:** Any project where a test harness or mutation driver inspects test output by regex

Klatch's mutation driver ran a test suite and checked the result by pattern-matching the raw terminal output. The driver reported ALL GREEN for a batch of mutations that had actually failed — exiting with code 1 and containing failure text in their output. The root cause: the test runner emitted ANSI escape codes (color sequences) in its output, and those escape codes interrupted the strings the regex was trying to match. A pattern looking for `FAIL` in `\u001b[31mFAIL\u001b[0m` does not match, because the color codes appear in the middle of the match target. Three harness faults were recorded in the round before the pattern was identified. The fix: strip ANSI escape codes from terminal output before running any regex or string-comparison checks against it.

**Suggested action:** Any harness that inspects test-runner output by string matching should strip ANSI escape codes as a first step. This applies to mutation drivers, CI log parsers, retry-on-failure detectors, and any other tool that reads terminal output and makes decisions from it. The stripped and unstripped strings look identical when printed to a color terminal, so this failure mode does not surface during manual review of the output — only when matching programmatically.

---

## Sources Read

**Klatch**
- `docs/logs/2026-09-21-*-calliope-*-log.md` — test suite status (126/1989 + 38/324), rounds 245–250 summary
- `docs/logs/2026-09-21-*-daedalus-*-log.md` — rounds 245, 247/249 detail
- Commits `0f88d5e9` (Round 248 — import.meta.url self-exclusion), `eaf0c023` (Round 249 — ANSI escape), `2affc4d6` (Round 250 — drive pricing, undriven population)

**Piper Morgan**
- `mailboxes/cio/inbox/INCIDENT-pard-to-cio-cc-exec-web-cxo-host-lead-arch-pm-hooks-pilot-fire-zero-recursed-967-marker-commits-on-main-hook-disarmed-2310-no-rewrite-tonight-2026-09-21.md` — full incident report

---

*Primary provenance: Klatch `8dbea62f` · 2026-09-21T21:35:03-07:00 — Piper Morgan `9d0f8a84` · 2026-09-21T23:16:14-07:00*
