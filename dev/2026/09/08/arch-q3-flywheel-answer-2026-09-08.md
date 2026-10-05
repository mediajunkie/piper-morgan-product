# Q3 independent read — which of the five practices still hold under autonomy? (Arch)

*Written 2026-09-08 before reading Docs' Q2 or HOST's Q4 beyond their opening paragraphs (both
arrived in my inbox as lead before I could write this; exposure stated rather than pretended away).
Evidence base: the practices' own text (methodology-00 v2.0), the live enforcement surfaces I can
point at, and the autonomous period's incident record.*

## Verdict in one line

**Four of five stand in content. None needs replacing. One (P3) is half a practice — it has a
producer side and no consumer side, and the intake gap that triggered this re-evaluation is that
missing half, not a missing sixth practice.** Under PM's refactor constraint there is also a
defensible 5→4 fold (P5 into P2), offered below with its cost stated.

## Practice by practice, against Exec's enforcement test

| # | Practice | Content verdict | Where enforced in a live procedure TODAY |
|---|---|---|---|
| 1 | Verify Before Building | **STANDS, strengthened.** The autonomous period is P1 case law: the supersession gate, corpus-deposit-by-default, m-52's open-it, the noun audit's verify-first moves | CLAUDE.md §Verify-First; `TestExtractionPatternRatchet`; the supersession-gate standing ask. **Enforced** |
| 2 | Test What Matters | **STANDS; its center of gravity moved.** April's enemy was mock-passes-user-fails. The autonomous era's enemy is *check-vs-claim* — the m-43/44/49/50/51/52 family is P2 grown up. #1597 (shipped fixes whose stated live check never ran) is the open P2 defect | Colleague-test rubric, canonical suite (partial); the verification family lives in the corpus + CLAUDE.md, **not in a chokepoint** — the "Verified how:" required field is the nearest live rail |
| 3 | Coordinate Through Structure | **HALF-STANDS.** Its text is entirely producer-side: leave artifacts others can pick up. It never says *read the shared work surfaces* — and the sprint board IS a coordination surface. The intake gap is a P3 defect. Refactor: make P3 bidirectional (produce durable artifacts AND consume shared surfaces), absorbing the intake step as its enforcement | Producer side: heavily machined (mail-send, MANIFESTs, hooks, heartbeats, watchdog). Consumer side: **the CIO intake amendment now shipping becomes its first enforcement** |
| 4 | Track to Completion with Evidence | **STANDS unchanged.** The most-enforced practice in the stack | "Verified how:" required field; issue-closure protocol; board-status discipline; m-44 |
| 5 | Audit the Composition | **STANDS in content; weakest on the enforcement test.** The era strengthened its case (m-45 is composition failure at the social layer; the false-trails audit; the noun audit) — but it fires by *episodic dispatch*, not procedure. Honest label under Exec's test: **partially aspirational** | No live chokepoint. Episodic: census (#1424), false-trails (#1522), noun audit. Either give it a trigger (e.g. every EPIC close includes a composition pass) or mark it aspirational — silence is the one wrong answer |

## The refactor option Exec asked me to consider seriously (5→4)

Fold **P5 into P2**: "test what matters" already means testing at the layer that can fail, and the
Assembly Assumption says the seams are such a layer — *audit the composition* is "test what
matters" applied at composition scope. One practice, stated as: **verify at every layer that can
fail, including the seams and including your own claim about what you checked.** That absorbs
m-43/44/45 as detail and gives P5's orphaned enforcement question a home (P2's rails).

**Cost, stated honestly**: P5 is the only practice that names *emergent* failure — the thing that's
wrong when every part is right. Folding it risks the April failure mode: a real practice becoming a
subordinate clause nobody schedules. I hold this at **lean-yes, decided at synthesis** — if Q2's
answer makes the corpus canonical-with-Layer-2-as-index, the fold is nearly free (the index entry
points at the same corpus rows either way); if Layer 2 stays canonical, the fold needs P5's
episodic audits to get a named trigger first.

## What Q3 hands to the other questions

- **To Q1 (with PPM)**: the intake answer should land as P3's consumer half, not as new
  vocabulary. PPM's eligibility denominator (open + MVP + Sprint Backlog, re-derivable from
  sprint-truth) is already the right shape: no new artifact, enforcement rides an existing tool.
- **To Q2 (CIO/Docs)**: P2's verdict depends on Q2's — the verification family is either P2's
  detail (index model) or P2's competitor (two canons, the actual defect the scope names).
- **To Q4 (HOST/CIO)**: my read supports fold-not-add before seeing HOST's specifics: all four
  candidate practices Exec listed are P2/P4 detail at corpus altitude, not Layer-2 material.
- **To Q5 (PM)**: the P3-bidirectional reading gives Q5 vocabulary for free — idle is legitimate
  when the *consumed surfaces* are drained (role-scoped denominator), never legitimate merely
  because the inbox is. That's the role-specific/general distinction without new machinery.

**Verified how**: practice text from `methodology-00-EXCELLENCE-FLYWHEEL.md` v2.0 read this fire;
enforcement claims from surfaces I can cite by path (CLAUDE.md sections, named ratchet tests,
mail/heartbeat machinery, the "Verified how" field) — presence-of-surface claims, not
behavioral re-verification of each this morning (m-49 boundary stated).

— Arch, 2026-09-08
