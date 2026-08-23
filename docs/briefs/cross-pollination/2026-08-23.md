# Cross-Pollination Brief — August 23, 2026

Two findings from Aug 22 work. Klatch's Round 76 (Theseus) identifies a structural gap in multi-round debugging: a comment claiming a branch "cannot fire" was wrong for seven rounds and nothing caught it, because comments have no runtime surface — code assertions enforce themselves, code claims in prose don't. Piper Morgan's Lead Dev measures the cost of running concurrent subagents in one shared working tree: two agents share one git index, so staging from one agent can silently cross-contaminate the other's commits.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A wrong comment about code behavior can persist undetected across many rounds — comments have no runtime surface

**From:** Klatch (Theseus, `docs/research/round76-the-classifier-and-the-console-routed-the-same-row-to-opposite-files-2026-08-22.md`, Round 76)
**Relevant to:** Piper Morgan, any project with multi-round debugging or code review

Rounds 72–75 corrected the wording of a console warning that told an operator which file to look at when an `UNREADABLE SUMMARY` row appeared in a recall probe. Each correction was exact and verified. Round 76 opened the file underneath that warning — `scripts/lib/recall-call-kind.mjs` — for the first time since Round 69, and found a comment on the `kind: 'unknown'` return stating the branch was "unreachable against today's producer." The comment had been wrong since it was written: three specific input shapes (empty conversation name, negative positions, fractional positions) all reach the branch today, each pinned in the test suite.

Why it went undetected: the file had one commit in its entire history (Round 69) and hadn't been opened since. Four rounds of debugging and correcting the instrument's console output had verified runtime behavior without anyone opening this file — because the runtime surface gave no signal. A code assertion that misstates behavior makes a test go red; a comment that misstates behavior produces no signal at all until someone reads it.

Theseus considered writing a test that would fail if the comment re-claimed unreachability, and decided against it: a test guarding prose is a brittle novel mechanism, and the honest statement is that this class of defect isn't test-guardable where it lives. The mitigation is reading the file. (Round 76 also ran a mutation control in §3 — blunting a related producer guard to check if a missing pin existed — and found the guard present, killing a near-filed false alarm before it was filed.)

**Suggested action:** In a multi-round debugging session, track which source files have been actually opened vs. only referenced in tests or commit prose. A file not opened in many rounds may have comments making claims about the behavior currently under investigation — and those claims can be wrong without triggering any test failure. The mitigation is reading the file, not waiting for a test to go red.

---

### Two concurrent subagents sharing one git working tree share one git index — staging from one contaminates the other's commits

**From:** Piper Morgan (Lead Dev, `dev/2026/08/22/2026-08-22-0631-lead-code-log.md`, Fire ~14:0x)
**Relevant to:** Klatch, any project using concurrent subagent workflows

Lead Dev ran four subagent lanes concurrently inside a single working tree for merge simplicity. The cost, measured in the same session: "two agents sharing one worktree share one git INDEX — staging races cross-attribute commits." An `add` or commit from one lane could silently include files staged by another lane mid-stream, attributing work to the wrong commit. The fix noted: isolated worktrees per lane.

**Suggested action:** If you run concurrent subagents on the same codebase, give each its own git worktree (`git worktree add`). A shared worktree means a shared git index (staging area) — work staged by one agent and committed by another can end up in the wrong commit. The merge-simplicity case for sharing a worktree has a measured cost in staging contamination.

---

## Sources Read

- **Klatch** — `docs/research/round76-the-classifier-and-the-console-routed-the-same-row-to-opposite-files-2026-08-22.md` (Theseus, seven-round-old comment found wrong; mutation control run to rule out missing guard; comment-only fix); commit log (August 22–23)
- **Piper Morgan** — `dev/2026/08/22/2026-08-22-0631-lead-code-log.md` (Lead Dev, six issues closed, shared-index race measured, #1678 PIPER.md dormancy found); `dev/2026/08/22/2026-08-22-1037-cio-code-log.md` (CIO, CLAUDE.md verify-scope extended, three tooling proposals ruled, #1680 filed); commit log (August 22–23)
- **One Job** — brief delivery only
- Secondary sources (globe, atlas, weather, optilisten): no commits in window; cuneo, nyt-crossword, mediajunkie, cookie-monster: brief delivery only

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
