# Cross-Pollination Brief — August 21, 2026

Two test-design findings from Klatch's Round 66–67 work (Theseus). The first: in a test with both a derived/arithmetic precondition and an empirical assertion for the same claim, placing the derived check first lets it abort the test if it fails — leaving the empirical claim unexecuted and unproven. The second: a recognizer gate built on shared fixture examples can pass even when one pattern is dead, because another intact pattern in the pool catches the same example. Both were found by running negative controls rather than reasoning that the controls would pass.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A derived check placed before an empirical claim can abort the test and leave the real assertion unexecuted

**From:** Klatch (Theseus, `docs/research/round67-distance-arm-validity-end-to-end-2026-08-20.md`, Round 67)  
**Relevant to:** Piper Morgan, any project with automated test suites

Round 67 validated the recall probe's distance-arm geometry by running the actual code rather than relying on algebra. The test asserted two things: (1) an arithmetic check that `markRow ≤ offeredStart + 29` (derived from the same algebra used to design the arm), and (2) an empirical check that `expect(first.text).toContain(RESTRICTION)` (confirming the code actually produced the restriction at the expected position).

Under control A — which set `GAP = 16` to push the restriction past the 30-row page — the arithmetic check failed first and aborted the test. The empirical assertion never executed. "An arithmetic restatement of the algebra was standing in front of the empirical claim. Reordered so the rendered text fails first." After the reorder, the same control landed on `toContain` going red — the observation that actually matters.

The Round 66 session hit the same pattern one level up: a gate over a transfer-voice recognizer had a fixture that could be caught by a fallback pattern, masking a dead primary pattern (§ below). Both were invisible to the author before the negative control ran.

**Suggested action:** In any test with multiple assertions for the same observable, confirm the most load-bearing assertion can actually fail. A simple check: if assertion A is derived from the same premises as assertion B, and A runs first, blunt A's precondition and verify that B (not A) is what goes red. If the test dies on A before B runs, reorder.

---

### A test suite that shares fixture examples across recognizer patterns can pass even when one pattern is dead

**From:** Klatch (Theseus, `docs/research/round66-fifth-filler-constraint-and-the-distance-arm-bound-2026-08-20.md`, Round 66)  
**Relevant to:** Piper Morgan, Design in Product, any project with multi-pattern classifiers or recognizers under test

Round 66 added a fifth constraint check to `verify-filler-constraints.mjs` — a gate that verifies every filler row in the recall corpus is phrased as a question (never as a handover). The gate held a flat list of should-match examples shared across all patterns in the recognizer. To test it, Theseus deliberately blunted the `here is` transfer-voice pattern (a negative control). The gate reported success.

Why: the example for the blunted pattern (`"Here's the vendor list — can you keep it somewhere safe?"`) was also caught by the `hold-something` pattern, which was still intact. One pattern dead, another covering for it, gate exit-0.

"The fix is structural rather than more fixtures: each pattern now carries its own example in the same tuple, so a pattern cannot be added without one and cannot be broken without a red." With per-pattern fixtures, blunting any pattern makes exactly that pattern's test go red — another pattern's coverage cannot mask it.

This is Round 59's rule applied one level down: *a recognizer matching nothing agrees trivially* — and a gate over a recognizer can agree trivially too, if its examples are pooled. Worth noting that real corpus rows drove three of the must-stay-clear fixtures: draft patterns had fired on them during development, which is how the false-positive risk was found.

**Suggested action:** For any multi-pattern recognizer under test, structure fixtures so each pattern has at least one example it — and only it — is expected to match. A shared fixture pool that any pattern can catch makes the gate's all-clear meaningless for the specific pattern it's supposed to catch. If you can't write a fixture only the target pattern catches, the pattern may be redundant.

---

## Sources Read

- **Klatch** — `docs/research/round67-distance-arm-validity-end-to-end-2026-08-20.md` (Theseus, geometry validated against code output; §3 finding on assertion ordering and §3a on same crash shape in Daedalus's item 8); `docs/research/round66-fifth-filler-constraint-and-the-distance-arm-bound-2026-08-20.md` (Theseus, check 5 built, fixture-gate defect found, distance arm bounded); commit log (August 20–21)
- **Piper Morgan** — `dev/2026/08/20/2026-08-20-1640-lead-code-log.md` (Lead Dev, #1667 merged, subagent-caught figure correction handled visibly in decision doc, readiness page for first flip written); `dev/2026/08/20/2026-08-20-0727-docs-code-log.md` (Docs, frontmatter-image diagnosed as structural naming convention, not a spreading bug; root-caused and fixed in `draft-weekly-ship` skill); commit log (August 20–21)
- **One Job** — `development/coral-logs/2026-08-20-coral-log.md` (Coral, shake-to-undo root-caused as iOS system-gesture collision with no web-exposed suppression path; feature removed); device pass ran, two bugs found
- **Mediajunkie (Pard)** — duty-cycle quiet logs; no agent narration
- Secondary sources (globe, weather, cookie-monster): brief delivery only; atlas, optilisten, cuneo: no activity; nyt-crossword: automated status commits only

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
