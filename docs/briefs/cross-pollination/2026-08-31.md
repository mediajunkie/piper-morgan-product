
# Cross-Pollination Brief — August 31, 2026

A day after Klatch established that checks must be able to go red to prove they work, Round 124 revealed the inverse failure: check counts that grow while coverage shrinks. When an outer filter is widened to include more files, any inner filter anchored to the old population silently inherits new members it cannot classify — they land in the negative bucket and are indistinguishable from files that genuinely don't need the check.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Widening a filter without updating its inner filters makes new members silently disappear — and the count still goes up

**From:** Klatch (Theseus `round124`, 2026-08-30)
**Relevant to:** any project with composed verification layers, nested filters, or multi-stage set operations

In Round 123, Daedalus widened `verifiers` from a flat `readdirSync` to a recursive walk, so that nested verifier files could enter the outer population. This was the correct fix: the old approach missed files one directory down, and `M3` (an unguarded nested file) now dies by `§(b2)` as intended.

The cost of the widening was not priced: `importsTs = verifiers.filter(<regex anchored to '../'>)` was not updated. New members enter `verifiers` but their path depth does not match the anchored pattern, so they cannot clear the inner filter. Files that fall out of `importsTs` are treated as "does not import TypeScript" — not as "unclassifiable." A nested verifier that imports TypeScript, holds the guard, and wraps its import on a branch that never runs **exits 0 and reports a pass**.

Measured directly (`verify-r124-swallow-nested.mjs`):

```
M0 control (unmutated)                       PASS — all 44 checks passed
M2  swallow, top level                       FAIL — 2 of 48        §(c), both limbs
M1  swallow, one directory down              PASS — all 45 checks passed        SURVIVED
M3  unguarded, one directory down            FAIL — 1 of 46        §(b2) alone
```

M1 and M2 differ in exactly one variable — depth. M1 and M3 differ in exactly one — whether the catch swallows. The escape is the conjunction of both: depth ∧ swallowing, and each half alone is caught. The check count rose from 44 to 45 (one new file added by the wider sweep), which read as increased coverage while a whole new escape class appeared.

A second failure also reported: the *guard-detection* half of the check was depth-anchored too (`s.includes("from './lib/tsx-required.mjs'")`). A correctly-guarded nested file could not clear the red — a false positive that will get checks commented out by anyone who hits it under deadline.

Theseus's framing: **"a widening turns a previously-unreachable narrow filter into a live silent default."** The anchored inner filter was harmless when the outer set was flat; widening the outer set made the inner filter's gap reachable for the first time.

**Suggested action:** When you widen a set (a glob, a recursive scan, a broader query), enumerate what downstream filters operate on that set and verify each one handles the new members. A rising check count is not evidence of rising coverage. The discriminating probe is a member that the *outer* filter accepts but the *inner* filter cannot classify — if it exits 0, you have a silent gap. Anchor-based string matching in inner filters is a recurring culprit: the match breaks when the member's path changes in any way the anchor didn't anticipate.

## Sources Read

- **Klatch**: `docs/mail/theseus-to-daedalus-…-widening-made-a-latent-narrow-filter-reachable-2026-08-30.md` (Round 124 main report); `docs/logs/2026-08-30-1047-theseus-opus-log.md` (Round 122 tsx-guard enumeration + Round 120 sweep); `docs/logs/2026-08-30-0917-daedalus-opus-log.md` (Round 119–121 rulings + §6 cross-file sweep)
- **Piper Morgan**: CXO fire 6 log (`dev/2026/08/30/2026-08-30-0717-cxo-code-log.md`) — structured payload probe, live system tests; active work, no cross-relevant transferable pattern identified
- **One Job**: brief delivery + `log: 08-30 — brief applied: negative-control run proves collate script's guards can fire` — Coral applied the Aug 30 brief insight same-day; no new pattern
- **NYT Crossword**: automated status commits + Inker seat retirement noted; no narratable content
- **Mediajunkie**: all-quiet duty cycle; no commits with narrative content
- **Globe**: brief delivery + scrubber scoping continuation (WebGL Two.js + crossfade shader); project-specific, no cross-relevant innovation
- **Cookie Monster**: brief delivery only

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
