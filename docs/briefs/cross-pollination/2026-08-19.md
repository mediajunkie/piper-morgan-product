
# Cross-Pollination Brief — August 19, 2026

Klatch hardened the two-phase recall API's test coverage by adding tiling tests — verifying that the full agent path (offer → retrieve by address) covers exactly what the offer promised, with no gap or overlap. Piper Morgan Comms found a memory pin whose general rule and worked example contradicted each other; the worked example carried the error, which is what Comms was actually following.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Testing an API's two-phase retrieval requires verifying that offer and retrieval tile — individual endpoint tests miss the gap

**From:** Klatch (Daedalus)  
**Relevant to:** Piper Morgan, any project with a two-stage search or retrieval API

The Klatch recall tool works in two phases: a search call (`renderExcerpt`) offers an address range, then a continuation call (`expand`) retrieves by that address. Tests had covered each call in isolation — but not the sequence an agent actually follows. In practice, `renderExcerpt` can offer a wider range than `expand` returns (the retrieval caps at 30 items, `:748`), so an agent following the offer gets a partial result without knowing it.

Three new tests close the gap: assert that the offered range's prose sentence and edge marker agree, and that the two sequential calls together tile the offer with no hole and no overlap (`round56-recall-expand.test.ts`, +3). The same commit also adds a guard that throws before the first row when an arm's parameters would exceed the filler list — verified by static enumeration of all 12 existing arms against the list lengths, since a live `--dry` run wasn't available in the sandbox.

**Suggested action:** In any project where one call offers a range and a second call retrieves by address, add an integration test that verifies the two tile: no row in the offered range is unreachable, and no rows are double-returned.

---

### A memory pin's worked example is more load-bearing than its rule text — both need independent verification

**From:** Piper Morgan (Comms)  
**Relevant to:** Klatch, any project maintaining memory surfaces with rule + example structure

PM Comms corrected a rule governing editorial footers and found a second, older error while doing so: the memory pin's general rule was correct, but its worked example used "Fri Ship" when the canonical publishing cadence is Wednesday. Comms had been following the worked example — which is the concrete, actionable part of the pin — not just the abstract rule. The inconsistency between the two parts was invisible unless you checked the example against the primary source (`reference_publishing_cadence.md`) independently of the rule text.

The practical implication: a memory pin can carry an error inside its worked example while the rule text remains correct. Because agents pattern-match to concrete examples, an error in the example is more likely to propagate than an error in a general rule. Verifying a pin's correctness by checking that the rule text is right doesn't catch this.

**Suggested action:** When writing or auditing memory pins that include worked examples, verify the example independently against the primary source — not against the rule text, and not by asking whether the two parts appear consistent with each other.

---

## Sources Read

- **Klatch** — `docs/logs/2026-08-18-*.md` (Calliope STOP rollup v54; Daedalus probe guard + tiling tests); commit log (August 18–19)
- **Piper Morgan** — `dev/2026/08/18/2026-08-18-0632-comms-code-log.md`; commit log (August 18–19)
- Secondary sources (one-job, globe, cookie-monster, weather, mediajunkie, nyt-crossword): delivery-only commits; no new narrative activity.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
