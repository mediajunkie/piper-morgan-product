# Leg A1 — Forward Read of the Decision Trail: Era Analysis

*Filed verbatim-condensed 2026-08-29. Denominator: 78 numbered ADRs exist (067/068 never filed);
headers of all 78 read, Context+Decision of 72; all 9 PDRs; decisions.log = 1,723 lines / 194 dated
entries (2 from Aug 2025, 192 from 2026-06-13→08-29), all entry openings read, ~12 pivotal in full.
Codebase NOT read (by design).*

## Era timeline

| # | Era | Span | Records | Operative vision |
|---|---|---|---|---|
| 0 | Prehistory | May–Jun 2025 | none (retroactive refs in ADR-031/-034) | May 27–29 vision; Jun 3 "plugin architecture from day one" — recorded only inside later ADRs |
| 1 | Foundation Pragmatism | Jul 2025 | ADR-001–011 | working single-developer PM assistant on MCP |
| 2 | Visionary Expansion ("MCP Week exuberance") | Aug 2025 | ADR-000, 012–027 (mostly dated Aug 17 in one sweep) | Piper as meta-platform: orchestrated, federated, spatially-intelligent, autonomous |
| 3 | First Reckoning (completion discipline) | Sep–Oct 2025 | ADR-028–039, 052 | stop starting; finish, verify, lock the 75%-complete system that exists |
| 4 | Embodied Colleague + Alpha Hardening | Nov 2025–Feb 2026 | ADR-040–058; PDR-001/002/101/003 | conscious-feeling colleague with memory and trust, running safely for real alpha users |
| 5 | The Floor Inversion | Mar–May 2026 | ADR-059–064; PDR-004 | LLM floor is the default; handlers must prove specificity; every LLM-touch boundary architected for honesty |
| 6 | BYOC & Impossible-by-Construction | Jun–mid-Jul 2026 | ADR-065–079; PDR-005/006 | plugin distribution + server-owned per-user state where violations are unrepresentable, enforced by derived lints |
| 7 | Second Reckoning (fundamentals-first) | mid-Jul–Aug 2026 | **NO new ADRs after 079 (Jul 16)** — decisions.log only; PDR-007 | delete what lies, measure before claiming, "no optional complexity" |

## Era-ending triggers

- E2→E3: Sept 14 2025 retrospective — "original May 27-29 vision was 95% unrealized" (ADR-031);
  Sept 19 review: QueryRouter 75%-complete-and-disabled, OrchestrationEngine never initialized,
  ADR-005's "eliminated" dual repos both extant (ADR-035/036).
- E3→E4: success, not failure — attention returned to product; Nov 27 conceptual breakthrough
  (ADR-045's 10-hour sketch session).
- E4→E5: March 2026 manual QA — "worse than a generic ChatGPT wrapper for any request outside its
  pre-built handlers" (ADR-060); Mar 14 "Are we doing it backwards?" roundtable (PDR-004).
- E5→E6: strategic pivot, not failure — PDR-005 BYOC ratified 2026-06-05; PM's 06-14 connector
  ruling (native "dated and clunky").
- E6→E7: the reckoning it triggered — Finish-the-Unfinished sprint (PM-ratified 07-16); Tier-3
  census found the cold, fabricating remains of Era 2.

## Signature Era-7 events (all decisions.log)

Tier-3 fix-or-delete 07-18/19 (">half is FABRICATION-removal, not dead-code cleanup" — deletions
include `services/mcp/server/` and `services/orchestration/`, **the physical unwinding of Era 2**) ·
ADR-028 superseded 07-25/26 (methodology package deleted, ideas survive as prose) · ADR-038
Amendment A 07-30 ("the decision STANDS, the verification claims are corrected") · beta slipped a
month 08-08 (PM: "We clearly have a lot more work still to do than anyone ever reported to me") ·
Understanding-Layer Inversion ratified 08-09 · spatial disposal approved 08-15 · "no optional
complexity" named standing principle 08-26/27.

## Shift classification (selected; full table in report)

**Drift**: dual repos persisting post-"elimination" · QueryRouter disabled at 75% · decisions.log
dormant Aug 2025→Jun 2026 · ADR-067/068 never filed + numbering collision · Era-2 code retained cold
~11 months · ADR-038's stale verification claims · ADR-044's undocumented deviation (later
retro-ratified).
**Deliberate variance**: Era-2 expansion (chosen and recorded, but reasoned from unverified
metrics — 0ms/92%/7626x) · native→MCP-consumer (PM-ratified 06-14) · ADR-052-vs-070 explicitly
reconciled · "no optional complexity" as a chosen lens.
**Correction**: Era 3 (inchworm/verification pyramid) · ADR-013 spatial maximalism → ADR-038
pluralism · ADR-039 handler-surface → ADR-060 floor-first · inert ethics enforcer → ADR-061 ·
multi-tenancy retrofit ADR-058 · per-feature scoping → ADR-079 mechanical contract · ADR-028
superseded · beta slip + fundamentals-first.

## Assumption archaeology

**Still load-bearing across all eras**: MCP as substrate (transmuted 3×, never questioned) ·
intent classification as universal entry (rebuilt repeatedly, universality never questioned) ·
evidence-required verification (vehicle died, assumption stronger than ever) · the LLM floor
guarantee · complete-don't-duplicate (same lesson learned twice, 10 months apart) ·
single-PM-as-only-human (now explicitly fenced rather than silently assumed).

**Silently abandoned — no recorded decision to abandon** (all still read "Accepted"/"Proposed"):
1. Piper Protocol authorship (ADR-020 — code deleted 07-18, commitment never rescinded)
2. Multi-federation semantic bridge (ADR-021 — implementing code deleted as "fake federated-search")
3. Orchestration-everywhere (ADR-019 — `services/orchestration/` deleted; ADR-043 partially,
   unlabeledly superseded it)
4. Chain-of-Draft economics (ADR-016 — code deleted, ADR never amended)
5. Moment-type agents (ADR-046) + consciousness-expression MVC (ADR-056 "every output MUST contain
   an 'I' statement") — both still Proposed, neither ratified nor withdrawn; **flag for code-side:
   does any MVC validation exist at all?**
6. ADR-024 JSON-field preferences — functionally superseded by ADR-075, no supersession recorded
7. ADR-007's staging stack (Temporal/Prometheus/Grafana/Nginx) — never mentioned again; the Fly.io
   world has no recorded bridge
8. Spatial-as-signature-differentiator — the PARTIAL case: ~11 months of silent drift eventually
   converted to a recorded decision (07-18 review → 08-15 PM ruling). **It is the model for what
   items 1–7 never received.**

## Contradictions (reported, not resolved)

- ADR-015 vs ADR-022 (same day): 7626x is simultaneously the type-specimen of an unverifiable claim
  and "measured emergence."
- adr-index.md (last updated 2026-05-16): claims "Superseded: 0 / Deprecated: 0 / Total: 67" while
  ADR-013 has carried a deprecation notice since Oct 2025, ADR-028 is superseded, and 78 exist —
  **the index is itself a stale hand-maintained surface of exactly the kind ADR-077/079 forbid.**
- ADR-018 still reads "Implemented" (0ms coordination, dual-mode server) vs decisions.log 07-18
  characterizing that code as fabrication. Status never downgraded.
- Aug-2025 ADR numbers don't track decision order; ADR-034's decision (Jun 3) predates ADR-001.

## The meta-observation (verbatim)

The record has a clear two-cycle rhythm: expansion on unverified claims (Era 2) → reckoning (Era
3); expansion on vision (Era 4) → inversion/correction (Era 5); expansion on distribution (Era 6) →
reckoning (Era 7). Each reckoning produced stronger machinery than the last (prose discipline →
test locks → mechanical lints → "no optional complexity" as standing lens), and each was triggered
the same way: someone measured reality against the record and found the record ahead of it. The
assumptions that survived all seven eras (MCP, universal intent entry, evidence-required,
complete-don't-duplicate) are precisely the ones that were re-ratified *after* a reckoning rather
than only before one.

**Structural observation flagged for synthesis**: no numbered ADR filed since 079 (2026-07-16) —
six weeks of substantial rulings (Inversion, floor-honesty contract, ToolEffect enum) live only in
decisions.log. Deliberate cadence change or drift? Not recorded.
