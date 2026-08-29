# Citation census — methodology-core + patterns corpora (summary)

*Filed 2026-08-29. Mechanical pass per Exec's suggestion, feeding the phase-4 corpus disposition
(ADRs + methodology-core + patterns). Full per-doc tables, reproducible script, and complete
citer lists preserved in `citation-census/` (census-report-full.md, census.py, citers_full.json,
headers.json). Method: git-grep over tracked files, mailbox cc/sent/read copies deduped (2–6x
multiplication factor), corpus-own-INDEX citations excluded as structural, false-positive classes
audited (two-digit P-NN is the ANTI-pattern namespace — never conflate).*

## Headline results

**Methodology-core (64 files)**:
- **Zero-cited by the mechanical definition: 0** — but **4 docs are effectively index-only**
  (m-05, m-12, m-13, m-14): sole citer is a parent README untouched since 2025-09-21. Nothing
  outside index surfaces has ever referenced them. 7 docs total have no citation since 2025.
- **Clear generational split**: m-24 through m-49 are heavily, currently cited (most-recent =
  this week); m-03 through m-21 are cited mostly by 2025/early-2026 dev logs and each other.
- **Strongest liveness (cited from CLAUDE.md or a skill): 12 of 64** — CLAUDE.md directly: m-38,
  m-31, m-43, m-44. Skills: m-20, m-25, m-35, m-36, m-41, m-43, m-44, gameplan-template,
  HOW_TO_USE_MULTI_AGENT, MULTI_AGENT_INTEGRATION_GUIDE.
- **Cited from application code** (behavior-adjacent): m-43 (61 code files), m-44 (49), m-40 (26),
  m-41, m-30 — verified genuine by sampling.
- Top of the table: m-44 (375 deduped citers), m-30 (330), m-36 (299), m-41 (285), m-43 (252),
  gameplan-template (231), m-40 (217), m-31 (214), m-20 (202).

**Patterns (81 files)**:
- **Zero-cited: 0**; lowest is P-019 at 4. The corpus is healthier than methodology-core's tail.
- Same generational split: P-062–P-074 (the 2026 incident-derived patterns) dominate current
  citations; P-002–P-044 (the 2025 code-pattern generation) cite mostly from old dev logs and
  each other, recency clustering at generated-index sweep dates.
- **CLAUDE.md/skills-cited: 8 of 81** — CLAUDE.md: P-045, P-046, P-047. Skills: those three plus
  P-049, P-062, P-064, PATTERN-FAMILIES.md, patterns README.
- **Code-cited**: P-073 (32 code files), P-045 (9), P-072 (7), P-007, plus ~10 with 1–5.
- Top: P-073 (412), P-045 (403), P-062 (304), P-064 (225), P-063 (215).

## What the data means for the disposition (Arch's read, not the agent's)

1. **The two-axis rubric has its first axis filled mechanically.** Cited/uncited is now data. The
   second axis (effective/inert) still needs judgment — but only for the cited docs; the
   index-only four and the no-citation-since-2025 tail are disposition-ready as-is.
2. **The generational split mirrors Leg A1's era structure exactly**: the 2025 corpora (m-03–m-21,
   P-002–P-044) are era-2/3 artifacts cited by era-2/3 logs; the 2026 entries are the reckoning
   era's working vocabulary. The disposition question for the old generation is the same as for
   the old ADRs: absorb what survived into living docs, archive the rest with provenance.
3. **The load-bearing core is small and identifiable**: ~12 methodology + ~8 pattern docs carry
   the CLAUDE.md/skill/code citations. That's the candidate "surviving law" set — roughly 14% of
   the combined corpora.
4. **Caveats that carry** (agent's own, kept honest): recency for non-dated citers is
   git-last-commit of the citing file — an upper bound; mailbox dedup is by basename; a
   mid-census regex bug (leading-zero stripping) was caught and fixed — earlier intermediate
   counts undercounted P-046/P-047; prior art exists (`dev/2026/05/09/pattern-usage-analysis.md`)
   as a cross-check.
