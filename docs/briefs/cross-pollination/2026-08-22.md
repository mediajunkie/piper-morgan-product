
# Cross-Pollination Brief — August 22, 2026

Two findings from sibling projects' Aug 21 work. Klatch Rounds 68–69 (Theseus, Daedalus) demonstrate that fixing an error response can shift rather than remove the failure mode — the replacement behavior may be quieter and require its own dedicated detector, with blind spots asserted in code rather than described in prose. Piper Morgan's Lead Dev filed a pattern for neutralizing a latent event-bus hazard before it triggers: add a test now that fails the moment a subscriber appears, converting a future runtime surprise into a build-time conversation.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Fixing an error can shift the failure to a quieter mode — verify what replaces it, then build a detector for that

**From:** Klatch (Theseus, `docs/research/round68-error-copy-fix-verified-and-the-quieter-failure-2026-08-21.md` and `docs/research/round69-empty-tail-detector-built-and-its-two-blind-spots-2026-08-21.md`, Rounds 68–69)
**Relevant to:** Piper Morgan, any project where fixing an error changes what the failure looks like

Round 67 identified that an error message accidentally contained a parseable address (the "loud" failure — a model following it would receive an error that pointed back at addressing). Daedalus fixed this. Round 68 verified the fix was correct but found what replaced the loud failure: a malformed expand call now routes through the search branch, producing `Searched own conversations: ` with an empty query — an artifact byte-identical to a genuine empty search, sitting in the same column the recall arm is scored from. Louder artifact replaced by a quieter one.

The fix was right and kept. The quiet failure needed its own detector. Round 69 built it (`scripts/lib/recall-call-kind.mjs`, `scripts/verify-empty-tail-detector.mjs`) and then did one thing worth noting: both of the detector's blind spots are asserted in code rather than documented in prose. Blind spot 1: a genuine empty search (`{query: ''}`) produces an identical artifact — the detector cannot distinguish it from a dropped expand without the raw wire tap. Blind spot 2: a dropped expand that carried a non-empty query leaves no empty tail at all and is recorded as an ordinary search (`Searched own conversations: depot cipher`). Both cases are in the verifier's test table with asserted verdicts, so if either becomes distinguishable in the future the verifier goes red and the change is forced to be deliberate, not silent.

**Suggested action:** When fixing a defect that changes an error's response behavior, verify what the new behavior is — not just that the old one is gone. If the new failure is harder to observe than the old one, build a detector for it. Where the detector has known blind spots, assert them in the test suite so any future change that closes a blind spot is forced through a deliberate update rather than accruing silently.

---

### Code that emits on an event bus with no subscriber yet carries a latent hazard — add a test now that fails when one appears

**From:** Piper Morgan (Lead Dev, `dev/2026/08/21/2026-08-21-0631-lead-code-log.md`, Fire 2, issue #1672)
**Relevant to:** Klatch (uses EventEmitters throughout the streaming path), any project with shared event buses

While repurposing Piper Morgan's shadow classifier into a flip-safety instrument (#1668), Lead Dev noticed a separate hazard: `classify()` emits `intent.classified` on the event bus. Today no subscriber exists — the code works fine and the emission is inert. But when a subscriber is eventually attached, it will silently inherit all shadow classifier outputs as real classified intents, with no warning that the signal source changed. The bug's signature would surface far from `classify()`.

The fix, filed as #1672 and closed the same fire: a services-wide sweep asserting that no production `IntentClassifier` carries an `event_bus`. The test enumerates the five known sites as a baseline and includes a vacuity check (per methodology-44) so a misconfigured test doesn't pass by measuring nothing. The failure message tells whoever trips it what to do instead of deleting the test. The hazard is now latent by construction: attaching a subscriber becomes a build-time conversation, not a runtime discovery.

**Suggested action:** When code emits on a shared event bus but the subscriber doesn't exist yet, the missing subscriber is invisible — there is no test failure and no runtime warning. The cheap fix is a test that asserts "no subscriber currently exists" and fails the moment one is attached. This converts the future discovery (likely confusing and far from the source) into a build-time conversation at the point of change.

---

## Sources Read

- **Klatch** — `docs/research/round68-error-copy-fix-verified-and-the-quieter-failure-2026-08-21.md` (Theseus, fix verified by control, quiet replacement failure identified); `docs/research/round69-empty-tail-detector-built-and-its-two-blind-spots-2026-08-21.md` (Theseus, detector built, two blind spots asserted in verifier); `docs/research/round70-the-probe-side-tap-built-and-what-a-wrong-join-costs-2026-08-21.md` (Theseus, probe-side SSE tap built, uniqueness requirement for joins established — instrument-specific, not surfaced as a Key Insight); commit log (August 21–22)
- **Piper Morgan** — `dev/2026/08/21/2026-08-21-0631-lead-code-log.md` (Lead Dev, #1668 shadow repurposed, #1672 event-bus sentinel filed and closed, flip-1 deployed live); `dev/2026/08/21/2026-08-21-1037-cio-code-log.md` (CIO, watchdog threshold found already cadence-relative, relay-dwell-time identified as the larger lever, fires-label field added to alert output); commit log (August 21–22)
- **One Job** — `development/coral-logs/2026-08-21-coral-log.md` (Coral processed Aug 21 cross-pollination brief and checked test suite for applicability; neither pattern applied to One Job's current structure)
- Secondary sources (globe, weather, nyt-crossword, optilisten, atlas): brief delivery only; mediajunkie, cuneo: brief delivery only; cookie-monster: automated status commits only

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
