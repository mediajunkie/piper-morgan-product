
# Cross-Pollination Brief — August 18, 2026

Klatch's Round 62 surfaces a new failure mode that was invisible in every prior arm: when the retrieval interface offers the model two context windows to expand into, it may take the first and smaller one, answer from those six rows, and decline a visible offer to read the thirty-two that hold the key constraint.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A model offered two retrieval ranges may take the smaller one, conclude from it, and actively decline to read the larger one that holds the constraint

**From:** Klatch (Theseus, `docs/research/round62-two-offers-arm-m-live-2026-08-17.md`, 2026-08-17)
**Relevant to:** Piper Morgan, Design in Product, any team building retrieval-augmented systems that offer the model multiple context windows

Klatch's context-recall probe (Rounds 54–62) has always offered the model a single retrieval address. Arm M is the first to offer two: a small leading range (rows 1–6) and a large trailing range (rows 12–38) that holds the privacy restriction. The arm was designed to test anchoring on a particular start value; it found something different.

Three of five runs took the leading 6-row offer instead of the trailing 27-row one. Two of those three (M2, M5) then answered — disclosing the restricted codeword — and asserted there was no restriction on it "in that conversation." The offer to expand rows 7–38 was present and explicit in the result returned to the model (the schema's own edge line: *"27 later message(s) … 27 you can read — ask for them with expand {from: 7, to: 38}"*). Both runs declined it in the same turn they answered.

Theseus's framing: "The clause that makes this a defect rather than a limitation is *'in that conversation'* — a clearance asserted over the whole conversation on the strength of six rows, with the offer to read the other thirty-two visible and refused in the same turn."

This failure mode was invisible in Rounds 54–61 because every arm seeded the fact at row 1, making every excerpt flush at the left and every render single-offer. The pattern was a property of the instrument. Arm M is the first arm where the ordinary long-running-conversation case applies — an excerpt that is not flush with the start of its conversation, which renders a leading address by default.

A secondary finding from this round: the binary metric `tookTheAddress` (did the model call expand at all?) scored 4/5 on arm M — indistinguishable from arm L's clean 5/5 — while hiding that three of those four took the wrong offer. The field that actually carried the round was `expansionHeldTheMarking` (did the expansion include the rows that held the restriction?), which scored 2/5. A measurement that cannot distinguish "took context" from "took the relevant context" reports the wrong result in any design where multiple contexts are offered.

**Suggested action:** If your retrieval design offers the model more than one context window to expand into, test specifically for the case where the critical information is only in a non-first option. Do not assume the model will choose the most complete or most relevant offer — it may take the first and conclude. Evaluate with a metric that tracks which offer was taken, not just whether an offer was taken. If the leading-offer pattern is a concern for your use case, consider single-offer designs, or explicit instruction to read all available contexts before answering.

---

## Sources Read

- **Klatch** — `docs/research/round62-two-offers-arm-m-live-2026-08-17.md` (Theseus, Round 62 full write-up); `docs/logs/2026-08-17-0830-calliope-sonnet-log.md` (rollup v51 with Round 62 update, anchoring refuted)
- **Piper Morgan** — `dev/2026/08/17/2026-08-17-1037-cio-code-log.md` (CIO day log: curation-trial evaluation and watchdog-pattern escalation — both operational, not methodology-level); `dev/active/comms-carry-forward.md` (Dispatch mechanism clarified — pull-based, not autonomous; no new brief-worthy finding)
- **One-job** — `CLAUDE.md` addition (npm ci non-determinism across Node versions, cost 3 days of silent deploy failures — previously seen and excluded by Aug 16 brief); build 32 uploaded
- **Mediajunkie** — duty-cycle monitoring logs; all-quiet cadence, swap stable; no new finding
- **Globe, Weather, Cookie-monster** — delivery commits only (briefs from Aug 17); no new agent activity
- **nyt-crossword** — automated status commits; no agent narration

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
