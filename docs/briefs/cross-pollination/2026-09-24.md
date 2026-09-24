
# Cross-Pollination Brief — September 24, 2026

Three findings today. Two from Klatch's ongoing mutation-test work, on the subtle difference between tracking assertions that force action versus those that go quietly stale — and on a test perturbation that the subject itself cancels out. One from Piper Morgan and Pard: a lesson about capturing which keys an external API response actually contained, learned when the Anthropic usage endpoint briefly served a completely different document shape.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A tracking assertion cleared by updating a count goes stale silently; one cleared by taking action proves the obligation was met — Klatch Round 261

**From:** Klatch (Daedalus, Round 261)

**Relevant to:** Any project that pins test counts, coverage numbers, or obligation registries.

Building a probe fleet that sweeps every round's script, Daedalus identified a structural difference between two kinds of pinned count:

- **A fuse** encodes a historical fact ("the population at commit X was 137"). A new commit that changes the population reddens it, but clearing the red only requires restating the number — it goes stale with no forcing function.
- **A gate** encodes an open obligation ("every probe file has been classified"). A new probe file reddens it because that file hasn't been classified yet. Clearing the red requires *making a decision*, not updating a count.

Same underlying mechanism (a pin comparing a census), opposite meaning. The difference is only legible from what clears it. Daedalus's sweep gate caught its own drive probe (`probe-round261`) on the first run — the system immediately detected the new entry and demanded a classification before proceeding.

**Suggested action:** When you add a tracking assertion, ask: what specific action clears this red? If the answer is "restate the count," you have a fuse; consider redesigning it to enumerate items explicitly so additions require a decision, not a number update. (Klatch probe sweep, `scripts/sweep-probes.mjs`; drive `probe-round261-…mts`, commit `92f780da`.)


### 2. A test that stubs something the subject re-applies internally measures the subject against itself — Klatch Round 262

**From:** Klatch (Theseus, Round 262)

**Relevant to:** Any project writing perturbation-based or isolation tests.

Theseus built an arm to verify that a code-masker's behaviour changes when stripped of its masking logic. He stubbed the masker from *outside* — wrapping the subject's input — and the arm returned the same result as the unmodified case. Close read: the subject called the real masker *internally*, so the external stub was silently bypassed. The test was consistent with an arm that simply cannot go red.

> **A perturbation the subject re-does is not a perturbation.**

This is a cousin of the same finding his own team diagnosed one round earlier (Round 260): "an arm never shown to go red is consistent with an arm that cannot." The fix was to make the substitution inside the module text, where the subject cannot re-apply the original.

**Suggested action:** When writing a test arm intended to catch a specific defect, confirm it *can* go red by injecting the defect manually before verifying the fix holds. An arm that only ever passes is not necessarily a working test. (Commit `e88a9b31`, probe arm B2, Round 262.)


### 3. Recording which keys an external API response contained makes a shape change distinguishable from a transient auth failure — Piper Morgan / Mediajunkie

**From:** Piper Morgan (Pard + PA, 2026-09-23/24)

**Relevant to:** Any project reading from undocumented or external API endpoints and logging failures for later review.

Pard built a usage reader against the Anthropic CLI's internal endpoint — undocumented, subject to silent shape changes. PA suggested an improvement: rather than logging a generic `UNMEASURABLE` on any non-standard response, emit the response's actual top-level key names alongside the HTTP status. The distinction: `AUTH-REFUSED · keys=[error]` vs `SHAPE-CHANGED · keys=[amber_cistern, amber_gauge, …]`.

The value of the improvement was demonstrated within 12 hours: the endpoint served a completely different document shape on one account and not the other, self-resolving in ~3 hours. With the old logging, this would have been logged as `UNMEASURABLE`, re-checked after the fact as working, and filed as transient — a false conclusion. With the new logging, `SHAPE-CHANGED` made the event legible to Pard without re-running anything, and the triage took seconds.

PA's framing (which earned the implementation): *"a transient reads `401 keys=[error]` and a rename reads `200 keys=[...]`, and whoever triages can tell which they're looking at without re-running anything."*

**Suggested action:** For any external API reader, emit the response's actual key names alongside the HTTP status in any non-successful branch. The cost is trivial; the diagnostic value is proved. Keep a manual-paste fallback when reading undocumented endpoints — a shape change is real, not theoretical. (Mediajunkie `usage-read.sh`; finding memo `b345a93bdf`, commit `0309472`.)


## Sources Read

- **Klatch** — `docs/research/round261-…md`, `docs/research/round262-…md`; git log 48h (commits `92f780da`, `e88a9b31`)
- **Piper Morgan** — mailbox finding `finding-pard-to-pa-…-2026-09-24.md`; git log 48h
- **Mediajunkie** — `usage-read.sh` commit `0309472`; Pard session log (`7227154`)
- **Globe** — Phase 1 scrubber shipped (prequel range expanded, 20 keyframes); not brief-worthy by innovation bar
- **One Job** — testing-plan restructured (planning docs); not brief-worthy
- **Weather, nyt-crossword** — automated/no-op fires only
- **Atlas, Cuneo** — no commits in window (last activity March 2026)

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
