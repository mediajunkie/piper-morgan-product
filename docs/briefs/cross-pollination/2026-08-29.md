# Cross-Pollination Brief — August 29, 2026

Klatch's Round 112 (Theseus, 2026-08-28) established Rule 14 of the recall-arm standing rules: when you narrow a clause, you must recompute every number the old clause generated — in the same commit. Failing to do so leaves a stale number that defends itself with prose rather than arithmetic, and is harder to question than one that simply fails a check.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### When you narrow a clause, recompute every number it generated — in the same commit
**From:** Klatch (Theseus `round112`, Daedalus `round107`, 2026-08-28); codified in `recall-arm-standing-rules-2026-08-28.md` as Rule 14
**Relevant to:** piper-morgan, any project with evaluation criteria, test conditions, or selection predicates that get refined over time

In Round 112, Theseus verified Round 111's transcription and discovered that arm S's rule-12 number — stated as `0 of 10` — was computed under the *old* clause. The same commit that stated `0` also narrowed the clause. Under the narrowed clause, the actual number is `10 of 10`: a complete reversal. The old number survived because it was framed as a finding ("0 of 10 discriminating shapes") rather than a formula; prose framing made it harder to question than a script would have been.

Round 107 surfaced a companion failure: arm S's `sep 0` proxy (used as a stand-in for "unproductive query") fired on productive queries too — wrong 11 of 14 times in the new corpus — because it encoded an indirect signal for the clause's antecedent rather than the antecedent itself. A verifier built on a proxy misfires when reused on new data that the proxy doesn't match cleanly.

Klatch codified both as Rule 14: **"When you narrow a clause, recompute every number the old clause produced — in the same commit."** Corollary: encode the clause's precise antecedent, not a proxy for it. A committed script encoding a superseded predicate is worse than no script, because it looks authoritative.

**Suggested action:** Whenever you tighten a selection rule, acceptance criterion, test condition, or predicate — in evaluation, research, or product specifications — treat every number derived from the old version as stale and recompute before committing. If a number can survive clause-narrowing via prose framing alone ("we found X"), add the mechanic that would fail it loudly when the clause changes. A stale number that reads as a finding is more dangerous than a broken test, because it doesn't show up as red.

## Sources Read

- **Klatch:** `docs/research/round107-the-instrument-checks-its-own-denominator-and-arm-r-breaks-round-98s-ten-of-ten-2026-08-28.md`, `docs/research/round112-the-transcription-holds-and-the-zero-is-computed-from-a-clause-the-same-commit-repealed-2026-08-28.md`, `docs/research/recall-arm-standing-rules-2026-08-28.md` (Rules 1–14, all codified 2026-08-28)
- **Piper Morgan:** `dev/2026/08/28/2026-08-28-0717-cxo-code-log.md` (6 fires; trigger-time vs edit-time distinction for portfolio refresh, sync-before-mail ratified as standing rule); recent commits — dense operational day, no cross-pollination candidates
- **One Job:** session logs 2026-08-28 (Accoil tracking-skills install, instrumentation plan written, covenant 7 scoped as calm-UI not privacy); no cross-pollination candidates
- **Globe:** one commit — Tessera revived after ~2-week dormancy, stranded-memo noted, environment verified; no cross-pollination candidates
- **NYT Crossword:** automated status.json commits only — no narratable content
- **Mediajunkie:** operational/infrastructure day (network saga, TM backup, LaCie, Loom delegation) — no cross-pollination candidates
- **Atlas, Cuneo, Optilisten, Weather, Cookie Monster:** no commits in window (or brief-delivery commits only)

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

