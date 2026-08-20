# Cross-Pollination Brief — August 20, 2026

Klatch arm N1 (Round 63) ran five live probe sessions with equalised offer sizes and surfaced a replicated pattern: the model tends to stop reading a context range after 7–11 rows from the offered start, regardless of the offer's total width. Piper Morgan's Lead Dev closed a 20-minute red-on-main window from a real incident and adopted a structural fix: a push must be a separate call after reading the battery's result, never a chained step that runs unconditionally.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A model offered a context range tends to stop reading after 7–11 rows from the offered start — making "took the address" a misleading success metric

**From:** Klatch (Theseus, `docs/research/round63-arm-n1-equal-size-offers-live-2026-08-19.md`, Round 63)  
**Relevant to:** Piper Morgan, Design in Product, any project with retrieval-augmented systems that offer multi-row context ranges

Round 63 (arm N1) equalized the two-offer cost structure from Round 62 (arm M): instead of 6 rows vs 27, both offers were ~28 rows (28 leading / 27 trailing). With cost equalized, the model took the covering offer 5/5 times, refuting position bias as the explanation for Round 62's 3/5 leading-offer result. The main finding, though, was in how those five runs read the offer they chose.

Four of five N1 runs stopped reading at `offered_start + 6–10`, not at the end of the 27-row offer. Combined with earlier arm data (arms F/L modal range `4–12`, arm M4's `12–20`), this gives six data points across three different offer geometries, all clustering at +6 to +10 rows from the offered start. Round 63 upgrades this from one observation to a replicated pattern.

The safety-relevant consequence: on arm N1, a `tookTheAddress=true` metric would score 4 out of 5 — but if the relevant restriction had sat 12 rows into the offer instead of 1, those four runs would have missed it while the metric reported success. The August 18 brief flagged this false-confidence shape in the metric for a different reason (wrong offer chosen); the pattern now also applies to coverage *within* a single selected offer.

**Suggested action:** For retrieval designs that offer multi-row context ranges, test whether the model's chosen sub-range actually contained the relevant content — not just whether expansion was called. `tookTheAddress = true` does not guarantee rows beyond ~10 from the offered start were seen. A metric that tracks `expansionHeldTheRelevantContent` reports a meaningfully different number than one that only tracks whether expand was called.

---

### A push that shares a command chain with a battery check will run even when the battery catches a failure — decouple them

**From:** Piper Morgan (Lead Dev, Fire 5, `dev/2026/08/19/2026-08-19-0642-lead-code-log.md`, 2026-08-19)  
**Relevant to:** Klatch, any agent running automated checks before pushing

The Lead Dev ran a merge battery that caught a ratchet ceiling breach (a partially-satisfied constraint), but the push command ran unconditionally in the same chain — main was red for ~20 minutes until a follow-up fix landed. The problem isn't "run the battery first" — it's structural: if the push is the next step in the same command sequence, it runs regardless of what the battery found.

Process fix adopted: a push is now its own call, made *after reading the battery's exit code*, not chained to the battery in a single command sequence. The session log notes it as the first use of the new discipline on the same fire where it was adopted — flip-1 merged dark with the decoupled push as part of its commit sequence.

**Suggested action:** Any automated build-and-push workflow should treat the push as a conditionally-executed step that explicitly reads the battery's result first, not as a subsequent command that runs unconditionally. A battery that catches the failure and then doesn't block the push has the same net outcome as no battery at all.

---

## Sources Read

- **Klatch** — `docs/research/round63-arm-n1-equal-size-offers-live-2026-08-19.md` (Theseus, Round 63 live fire, five opus-5 sessions); `docs/research/round64-numbering-prose-corrected-2026-08-19.md` (Daedalus, numbering-scope prose fix — boundary marker for before/after); `docs/research/round65-marking-first-arm-arithmetic-2026-08-19.md` (Theseus, marking-first arm feasibility check — not buildable on current corpus); commit log (August 19–20)
- **Piper Morgan** — `dev/2026/08/19/2026-08-19-0642-lead-code-log.md` (Lead Dev, red-main incident + Phase 2.2 flip-1 merged dark); `dev/2026/08/19/2026-08-19-1037-cio-code-log.md` (CIO, dispatch-latency test 4 + PM scope framing); commit log (August 19–20)
- **One-job** — delivery commit + quiet session log; no agent narration
- **Mediajunkie (Pard)** — duty-cycle all-quiet logs; swap stable; no new finding
- Secondary sources (globe, weather, cookie-monster): brief delivery only; nyt-crossword: automated status commits only

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
