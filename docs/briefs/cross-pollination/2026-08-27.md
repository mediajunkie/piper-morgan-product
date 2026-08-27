
# Cross-Pollination Brief — August 27, 2026

Klatch's research pair (Daedalus and Theseus) closed Rounds 99 and 100 yesterday, surfacing a discipline gap that applies to any project maintaining long-lived shared research artifacts: correcting a claim in a narrative document does not reach the artifact that originally asserted the claim.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Retractions need to travel to their source, not just their narrative
**From:** Klatch (Daedalus `round99`, Theseus `round100`, 2026-08-26)
**Relevant to:** piper-morgan, any project with multi-author research artifacts or long-lived specification documents

In Rounds 98 and 99, both agents explicitly conceded a factual error and filed retractions in their round docs and mail. By Round 100, Theseus discovered the original wrong claim was still sitting in arm R's own docblock — under the word "measured" — unchanged, because nobody had gone back to edit the source file.

Two rounds of documented retraction, zero correction at the point of assertion.

The same window also surfaced a related failure: four separate in-code warnings (code comments, console output tags, arm docblock caveats, and a committed research doc all named the specific trap) did not prevent both researchers from independently falling into it in Rounds 94, 96, and 97. Daedalus's Round 99 conclusion: "this failure mode is not addressable by warnings, because four were in place." The fix the harness already points to — structurally distinguishing the two incompatible prediction types in the JSON schema rather than labeling them in adjacent prose — would make the mistake mechanically impossible rather than documented.

Both failures share a root cause: **corrections made downstream from an error don't fix the error at its source.** A warning in a comment is not a structural constraint. A retraction in a later document is not a change to the earlier document.

**Suggested action:** When you retract or correct a claim — in any shared artifact — search for and explicitly update every file that contains the original wrong assertion, not just the current document. For research infrastructure, prefer structural disambiguation (schema-level separation of incompatible types) over prose warnings; if a mistake requires a comment to prevent, consider whether the data model itself can make the mistake impossible.

## Sources Read

- **Klatch:** `docs/research/round99-four-warnings-were-in-place-and-the-trap-caught-us-both-2026-08-26.md`, `docs/research/round100-the-retracted-claim-was-still-in-the-arm-and-the-null-was-registered-against-the-wrong-denominator-2026-08-26.md`, `docs/COORDINATION.md` (current status)
- **Piper Morgan:** `dev/2026/08/26/2026-08-26-0712-pa-code-log.md` (BYOC architecture conversation, mail-send.sh false-positive fix); recent commits — quiet day across most roles
- **One Job:** `development/coral-logs/2026-08-26-coral-log.md`; README stat correction (two unsourceable statistics replaced with plain first-person claims)
- **NYT Crossword:** automated status.json commits only — no narratable content
- **Atlas:** no commits in window
- **Optilisten:** no commits in window

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
