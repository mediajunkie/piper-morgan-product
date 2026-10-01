# Cross-Pollination Brief — October 1, 2026

Three findings this window. Klatch's probe system surfaced a subtle class of test that passes vacuously when the tool being tested never runs. Piper Morgan measured actual CI push composition and found the stated reason for an unfiltered trigger had a hole. And Piper Morgan's Docs seat found that prompt generators which enumerate resources by name silently go stale — detection from the filesystem is the fix.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A "zero errors" assertion passes vacuously when the tool never runs — Klatch, Theseus, Round 306

**From:** Klatch (Theseus) · commits `e69808b9`, `34193c0f`
**Relevant to:** any project with test probes or CI checks that verify tool output by asserting an empty error list

Klatch's probe for Round 303 checked that a TypeScript compiler pass produced zero TS errors (`wErrs.length === 0`). The probe was a restatement of an earlier arm that had asserted exactly `wErrs.length === 2` — a specific count expected from a known-failing case. Theseus discovered this window in Round 306: when the compiler binary is absent or the child process is killed before producing output, `wErrs` is empty not because the program is clean, but because no output arrived at all. The zero-count assertion passes in all three cases.

The original arm was accidentally protected. An assertion of `=== 2` cannot be satisfied by a non-run (a non-run produces zero lines, not two), so the specific count was silently guarding against the "tool never ran" class of failure. When restated to "zero errors," that accidental guard was removed.

Theseus's summary of the general shape: *"repairing a pin from 'N of a bad thing' to 'none of the bad thing' removes whatever liveness the nonzero count was silently providing."* It is not the familiar `0 of 0` all-quantifier trap — it is a plain equality against zero, failing the same way.

Fix: pair the zero-count assertion with a process exit-status check (`status === 0`). Also add a known negative (a spawn of a binary that does not exist) so the exit-status guard is exercised, not just present.

**Suggested action:** Audit test arms that assert "no errors" or "empty output" from an external tool. For each, check whether the arm also asserts the tool's process exit status. If not, add a known-negative test case (a call with a missing binary or a provably invalid input) to confirm the arm would red when the tool does not run.

---

### 2. 85% of CI builds rebuilt a byte-identical image because non-code commits triggered them — Piper Morgan, Pard, commit `c2c31c695`

**From:** Piper Morgan (Pard)
**Relevant to:** any team deciding whether to add path filters to a CI trigger

Pard measured a 90-minute window of pushes to PM's `origin/main` and found 46 commits: 7 touched application code; 39 were docs, mail, logs, and heartbeat files. With an unfiltered push trigger, each of the 39 non-code commits produced a full container rebuild of a byte-identical application.

The prior argument for keeping the trigger unfiltered was that `paths-ignore` would "quietly break" the parity invariant: staging's attested sha should equal main's tip. Pard identified the hole: PM's parity check (`check-release-parity.sh`) compares product-path content, not sha labels. A docs-only push would lag the staging sha label while leaving the artifact itself identical — so the invariant that actually matters (the code running on staging is the code on main) would still hold. The sha label and the code content are two different things that can drift independently under path filtering.

The decision is open — Arch rules on whether imprecise sha labels are an acceptable cost. But the composition measurement and the sha-vs-content distinction are the load-bearing pieces before that decision is made.

**Suggested action:** Before deciding whether to add or remove path filters from a CI trigger, measure the actual composition of your recent pushes (code-touching vs. non-code). Separately, clarify which parity invariant your system actually enforces — sha-label parity or code-content parity — because they behave differently under `paths-ignore`.

---

### 3. Prompt generators that list resources by name produce prompts that go stale; detect from the filesystem instead — Piper Morgan, Docs, commit `098bfd2` (Pard log), `798fe73`

**From:** Piper Morgan (Docs, Pard)
**Relevant to:** any project generating per-seat or per-role prompts from a shared template

PM's per-seat prompt generator emitted a prompt for Docs that named only one of its two worktrees (product and website). Docs caught this, but named why "the skill handles it anyway" is not sufficient: a differently-primed instance, or one post-compaction with thinner context, might take the literal prompt and skip the second worktree.

Two changes shipped:

1. **Detect, don't enumerate.** The second worktree is now discovered from the filesystem at generation time rather than listed by name. A generated list goes stale silently; a detection always reflects current state.

2. **Extras in a tracked file, not inline.** Per-seat configuration extras live in `docs/seat-prompts/extra/<role>.txt`, which the generator reads. An inline hand-edit to a generated file is erased the next time the generator runs — Pard's note: *"a hand-edit would be erased the next time the generator ran, which is the defect class this fleet keeps finding."*

The fix was also wider than Docs: `comms` and `web` both have website worktrees and are both upcoming cascade seats, so a Docs-only repair would have left the same trap in two more seats.

**Suggested action:** In any system that generates per-role or per-seat config or prompts, prefer detecting dynamic properties from the filesystem over enumerating them by name. Store per-role extras in a file the generator reads rather than as hand-edits to generated output.

## Sources Read

- **Klatch:** `docs/logs/2026-09-30-1947-theseus-opus-log.md` (Round 306 — vacuous zero, compiler-never-ran finding and repair); commits `e69808b9`, `34193c0f`
- **Piper Morgan:** `mailboxes/arch/inbox/pard-to-exec-arch-cc-xian-the-composition-number-and-a-hole-in-my-own-reason-2026-10-01.md` (push composition 7/46; sha-label vs content parity)
- **Mediajunkie/Pard log:** `logs/2026-09-30-pard-log.md` (Docs's one-worktree assumption in the generator, fix via detection and `extra/` tracked files)
- **Globe** (commits present: pre-commit gate for `explore/index.html`): same structural pattern as the 9/30 brief's Klatch finding; not separately reported
- **Weather** (commits present: KPAO station switch, UTC timestamp labeling): operational fixes, not cross-pollination-worthy
- **One Job, nyt-crossword:** brief deliveries and automated prints; not brief-worthy
- **Atlas, Cuneo, Optilisten:** no commits in window

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
