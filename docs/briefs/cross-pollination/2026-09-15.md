
# Cross-Pollination Brief — September 15, 2026

Three projects this window hit failures rooted in unexamined defaults: a fan-out that silently inherited the dispatcher's model tier and exhausted a shared usage ceiling; a test assertion whose subject defaulted to empty when the defect was fixed, producing a vacuous green; and a stale git clone whose `git add -A` staged 1,683 deletions before anyone noticed. Klatch also landed a discipline worth carrying: retire test arms by re-aiming them at behavioral invariants rather than deleting — the arm you're about to delete may be the only integration-level observer of its path.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. In multi-agent fan-out, subagents silently inherit the dispatcher's model tier unless you set it explicitly

**From:** Piper Morgan (CIO session log `dev/2026/09/14/2026-09-14-1037-cio-code-log.md`)
**Relevant to:** Any project using multi-agent task dispatch

Lead Dev dispatched 30 subagents on Saturday without specifying the `model` parameter. Each inherited Lead's Fable tier by default. Together they exhausted the shared Fable usage ceiling — and the cost fell on Architect and Web, who dispatched nothing that day. Neither knew why their work was blocked until the CIO traced it.

PM ruling: *"dispatch tier should be stated, not inherited."* Codified in PM's `docs/CLAUDE.md` (Subagents section) and `audit-cascade` skill v1.2 (Step 1b). The guidance: Haiku for fully-specified mechanical work; Sonnet for bounded implementation; Fable only when the reasoning inside the unit genuinely warrants it. Reaching for the dispatcher's own top tier is a signal to look at the prompt first — underspecified prompts grow to fill the model they're given.

**Suggested action:** Audit fan-out dispatch calls. If `model` is unset, the dispatcher's tier silently applies. Pass it deliberately on every dispatch.

---

### 2. A test assertion whose subject defaults to empty passes vacuously the moment the defect is fixed

**From:** Klatch (research log `docs/research/round209-…-2026-09-14.md`)
**Relevant to:** Any project with automated testing

Klatch's probe suite had an assertion checking that field `notes[0]` did not contain a specific bad value. The field was only populated when the defect was present. When a fix changed the output format so the defect disappeared, `notes[0]` became absent — and the assertion's subject resolved via `notes[0] ?? ''` to an empty string. The check passed: `''` didn't contain the bad value. Vacuously green.

The R209 log marks this as distinct from the "check can't see its target" failure reported on 9/13: here the subject exists and resolves, but resolves to an empty default rather than to the meaningful value the assertion was written around. The fix removes the evidence; the assertion applauds the absence.

Fix: make subject *existence* part of the assertion. Don't just check the value when present — assert the field exists and holds the expected value, or explicitly assert it is absent. An assertion that can pass vacuously is indistinguishable from one that verified something.

**Suggested action:** Audit assertions that guard against "this field should not contain X." If the check can pass when the field is absent (via `?? ''`, `.length === 0`, or similar defaults), it will produce a false green whenever the fix works by removing the field. Add an existence assertion alongside the value assertion.

---

### 3. A stale clone plus `git add -A` stages the deletion of every file added to origin since the last pull

**From:** Mediajunkie (Pard session log `logs/2026-09-15-pard-log.md`)
**Relevant to:** Any project where multiple agents commit to shared repos

Pard's clone of the dispatch repo was significantly behind `origin/main`. Running `git add -A` staged not just Pard's new files but also the deletion of 1,683 files that had been added to origin since the last pull. The push went through; 1,683 files disappeared from the main branch.

The mechanics: `git add -A` diffs the working tree against the *local index*, not against `origin`. Files that exist in `origin/main` but not in the local clone appear as deletions to the local index, and `git add -A` stages them as such.

Response: Pard wrote `check-clones.sh`, which detects clones behind origin where a broad add would stage deletions. The discipline: pull before broad adds, or use `git add <specific paths>` when operating in a shared repo with concurrent committers.

**Suggested action:** Before any `git add -A` in a multi-agent repo, run `git fetch origin && git status` to confirm the clone is current. If behind, pull first. Treat stale-clone awareness as a pre-commit discipline, not an assumption.

---

### 4. Before retiring a failing test arm, verify it is not the only integration-level observer of its path

**From:** Klatch (research log `docs/research/round211-…-2026-09-14.md`)
**Relevant to:** Any project with integration or probe test suites

Two of Klatch's end-to-end probe arms were failing and flagged for retirement. On inspection: both were the *only* integration-level observer of their respective operator-facing CLI paths. Deleting them would leave those paths with zero coverage at the integration layer — the 1,785 unit tests would stay green while the CLI's refusal explanation silently broke.

Decision: re-aim rather than delete. Arm C1 was redirected to pin a behavioral condition (`plan.summary.apply === 0`) rather than the CLI output branch. Arm B2 was redirected to pin the underlying function (`ambiguousNameNote()`) rather than the formatted sheet. The R211 log verified by mutation: deleting the operator's refusal explanation left all 1,785 suite tests green but failed exactly arm B2, the one marked for deletion.

**Suggested action:** Before deleting any failing test arm, ask whether it is the only integration-level observer of the path it covers. If so, re-aim it at a behavioral invariant (a function, a condition, a return value) that survives the output-format change that caused the original failure. Retire the old assertion; preserve the coverage.

---

## Sources Read

**Primary:**
- Piper Morgan — `dev/2026/09/14/2026-09-14-1037-cio-code-log.md`; `docs/CLAUDE.md` (Subagents section, audit-cascade skill v1.2)
- Klatch — `docs/research/round209-a-check-whose-subject-can-be-empty-goes-green-when-the-defect-is-fixed-2026-09-14.md`; `docs/research/round211-retired-is-not-deleted-and-the-sheet-had-exactly-one-observer-2026-09-14.md`
- Mediajunkie — `logs/2026-09-15-pard-log.md`

**Secondary:** globe, weather, one-job, nyt-crossword had activity in the window; none cleared the brief-worthiness bar. cuneo and atlas had no commits in the window. See `secondary_provenance` in front matter.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
