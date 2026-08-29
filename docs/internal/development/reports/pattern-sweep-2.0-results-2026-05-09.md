# Pattern Sweep 2.0 — Results — 2026-05-09

**Window**: 2026-03-17 to 2026-04-28 (6 weeks)
**Sweep**: #1025 (auto-generated 2026-05-06)
**Lead**: CIO (Chief Innovation Officer, Code instance, Opus) — per PM directive 2026-05-08 ("CIO leads with subagents; Lead Dev's attention is needed elsewhere; PM backs up")
**Methodology**: Pattern Sweep 2.0 framework (`dev/2025/12/28/pattern-sweep-2.0-framework.md`)
**Execution date**: 2026-05-09 (single session, ~3 hours wall-clock with subagents running parallel)

---

## Executive Summary

The window's pattern catalog was structurally shaped by **Pattern-062 (Assembly Assumption) family completion** — three sibling sub-patterns (063 vocabulary, 064 extension, 065 institutional-knowledge) formalized within 48 hours April 26-28, all promoted to Proven May 8. The 062 family alone accounts for **61% of all pattern citations in the window** (2,052 of 3,361 citations).

Anti-amnesia infrastructure operated as designed: **1 TRUE EMERGENCE** candidate (Pattern-066 Stacked Silent Failures, filed Emerging today) versus **8 NEAR-MISSES** correctly classified as evolution-not-novelty. The 1:8 ratio is the framework's discrimination machinery validated.

**Six new anti-pattern candidates** added to the index (last scanned 2026-02-03): A-12 Alive Scaffolding, P-12 Broad git-add multi-agent sweep, P-13 Commit-attribution drift, P-14 Silent rubric extension, P-15 Branch-collision, T-05 Activation-flag theater. Total indexed: 49 (was 43).

**Catalog hygiene findings**: 9 truly stale patterns flagged for next-cycle triage; Pattern-024 status corrected (Proven → Superseded); 65 → 66 patterns total.

**Methodology compounding rate** is now an observable Code-era operating tempo (5 fix-to-validation cycles closing within 24 hours during the window). Worth tracking as catalog-maturity metric across sweeps.

---

## Findings by Phase

### Phase 1: Pattern Library Index

**Output**: `dev/active/pattern-library-index.md` — 65 patterns indexed (excluding template-000)

**Side-benefit findings**:
- **Patterns 039 / 040** have unedited template literals in Status blocks (`**Emerging** | Proven | Experimental | Deprecated` left in place; bolded option indicates intent)
- **Patterns 031 / 034 / 036 / 037 / 038**: non-canonical "Active" status (vs. standard Proven / Emerging / Withdrawn)
- **Patterns 044 / 045 / 046 / 047 / 048 / 050-054**: different metadata block format (Status / Category / First Documented)
- **Patterns 055-060**: "Emerging | Proven in #NNN" hybrid format
- **Patterns 001-027** (mostly): no explicit origin date in any section; legacy catalog era

→ **Recommendation**: file a metadata-cleanup ticket as low-priority Docs work. Standardize Status vocabulary across all patterns. Not blocking; cosmetic + audit-trail benefit.

### Phase 2B: Usage Analyst

**Output**: `dev/active/pattern-usage-analysis.md` — 3,361 citations across 65 patterns

**Surface mix**: mail 65.2% (inflated 3-6× by sent/inbox/read mirroring) / session logs 24.5% / omnibus 6.5% / git commits 3.8%

**Top 5 most-cited**:
1. **Pattern-063 Parallel-Authoring Drift** — 933 citations (Apr 26-28 dominant, post-formalization)
2. **Pattern-062 Assembly Assumption** — 631 citations (central diagnostic vocabulary)
3. **Pattern-045 Green Tests, Red User** — 586 citations (generalized to memo-propagation Apr 19)
4. **Pattern-064 Extension Without Integration** — 488 citations (sibling sub-pattern, formalized Apr 28)
5. **Pattern-024 Methodology Patterns / Excellence Flywheel** — 200 citations (**RETIRED** Apr 28 commit `adfd453b`)

**27 patterns received at least one citation; 38 received zero** (after de-duplication of mail mirror).

**Cross-substrate applications observed**:
- Pattern-062 applied to omnibus synthesis (cross-layer to documentation)
- Pattern-045 generalized to memo-propagation (test-vs-real-infra → memo-vs-canonical-source)
- Pattern-049 used as verb-form ("begins #909 audit cascade")
- Pattern-053 frozen as load-bearing code convention (`format_warmth_guidance()`)
- Pattern-031 applied to LLM provider tier resolution (cross-domain from PM-tool plugins)

### Phase 2C: Novelty Detector

**Output**: `dev/active/pattern-novelty-candidates.md` — 1 TRUE EMERGENCE candidate, 8 NEAR-MISSES

**TRUE EMERGENCE candidate (TE-1)**: **Stacked Silent Failures**
- Named explicitly by CIO predecessor 2026-04-10 ("a new diagnostic pattern worth naming")
- Referenced 3+ times across the window (Apr 14 omnibus, Apr 17 M1 audit, Apr 23 handoff watch-list)
- FALSE POSITIVE TEST passed against P-041, P-042, P-043, P-045, P-060, P-062
- Closest neighbor P-045; CIO predecessor explicitly carved out distinction (multi-layer cascade vs. single-layer mismatch)
- → **Filed today as Pattern-066 Emerging** (CIO self-approval; PM concurrence on slot allocation recommended)

**NEAR-MISSES (8)**:
- NM-1, NM-2, NM-3: Pattern-063, -064, -065 (already canonical PATTERN EVOLUTION of P-062 family — anti-amnesia working)
- NM-4: "Alive scaffolding" (subsumed by Pattern-064)
- NM-5: PP-002 Load-Bearing vs. Commodity (already in PROTO-PATTERNS.md as active proto-pattern)
- NM-6: "Externalize before the seam" (subsumed by Pattern-065)
- NM-7: "Three-layer bugs" framing (supporting evidence for TE-1, not separate)
- NM-8: "Singleton → pair → many" (research-methodology framing, not operational pattern)

**Operational vocabulary on watch (proto-canonical)**: alpha catch-22, From Diagnosis to Discipline in 24 Hours, decreasing review-volume signal, spark vs holder, methodology-to-runtime latency, discipline-failure recovery — captured in `canonical-vocabulary-watch.md` (S1 deliverable, May 4).

### Phase 2D: Evolution Tracker

**Output**: `dev/active/pattern-evolution-report.md` — 13 evolution events, 6 anti-pattern candidates, 9 truly stale

**13 evolution events across 6 patterns**:
- Pattern-062 (7 events): intent-routing manifestation, product-architecture manifestation, layer-contract sketch, methodology-elevation (Flywheel 5th practice), omnibus-synthesis manifestation, comms-layer manifestation, family-table assembly
- Pattern-045 (1): gate-checklist absorption
- Pattern-049 (1): Step 2.5 protocol expansion
- Pattern-029 (1): operational refinement via Pattern-065
- Pattern-012, 051, 059 (incidental citations only)

**Pattern-062 family completion arc** is the structural headline:
- 062 (Proven, original) — component layer
- 063 (Emerging Apr 27 → Proven May 8) — vocabulary layer
- 064 (Emerging Apr 28 → Proven May 8) — extension layer
- 065 (Emerging Apr 27 → Proven May 8) — institutional-knowledge layer

All four now Proven. Family table convention added to Pattern-062 Evolution section.

**6 anti-pattern candidates → Phase 3 (executed)**:
- A-12 Alive Scaffolding (Architecture)
- T-05 Activation-flag theater (Testing)
- P-12 Broad git-add multi-agent sweep (Process)
- P-13 Commit-attribution drift (Process)
- P-14 Silent rubric extension (Process)
- P-15 Branch-collision in shared working tree (Process)

**9 truly stale patterns** (Emerging/Experimental status + zero in-window engagement):
- 029, 030, 035, 039, 055, 056, 057, 058, 060

→ **Recommendation**: triage cycle warranted. Disposition options per pattern: verify (still load-bearing in code, just rarely cited) / refresh (update for current state) / retire (Withdraw with rationale) / redirect (point at successor pattern). Not executed in this sweep — flagged for next cycle. Mirrors M1 audit B2 finding ("20 of 22 numbered methodology docs went zero-cited") at the pattern-catalog layer.

### Phase 2E: Meta-Pattern Synthesis (CIO direct)

**Output**: `dev/active/pattern-meta-synthesis.md` — 10 meta-observations integrating four lenses

**Headline meta-observations**:

1. **The 062 Family Completion is the window's structural event** — all four lenses converge from independent angles. Family alone accounts for 61% of citations.

2. **Pattern-062 graduated from pattern to methodology principle** — became Practice 5 in Excellence Flywheel v2.0 ("Audit the Composition"). Catalog convention has no explicit term for this transition; recommend "**Methodology-Elevated**" lifecycle stage. Likely retroactive candidates: P-045 (Green Tests Red User), P-049 (Audit Cascade).

3. **Anti-amnesia infrastructure is operating** — 1:8 TRUE-EMERGENCE-to-NEAR-MISS ratio is the framework working. Worth tracking as catalog-maturity metric across sweeps.

4. **Methodology compounding rate is a Code-era operating tempo** — 5 instances of 24-hour fix-to-validation in the window. Provisional name "Same-Cycle Validation" or "Methodology-to-Runtime Latency" — captured as Operational tier in CIO Innovation Backlog; promotion candidate at next sweep with ~5 more instances across multiple windows.

5. **Catalog has acquired self-instrumentation** — Pattern-063 slot conflict was itself a meta-instance of Pattern-063 at the catalog-management layer (the pattern diagnosed its own filing). Recommend adding to pattern-filing checklist: *"Does this pattern diagnose any aspect of its own emergence or formalization process?"*

6. **Pattern-066 Stacked Silent Failures candidacy validated** independently against four lenses. Filing today as Emerging.

7. **Catalog dead-weight signal real** — 9 truly stale + Pattern-024 retirement status drift + meta-pattern trio 036/037/038 zero-cited (possibly absorbed into P-049). Triage cycle warranted.

8. **Surface mix has shifted** — pattern citation flows through inter-agent memos (mail 65%) rather than document retrieval. Patterns operating as language rather than as documentation. Maturity signal.

9. **Cross-substrate pattern application is now common** — patterns migrating off original substrates (P-062 to documentation; P-045 to memo-propagation; P-053 to load-bearing code). Diagnostic-vocabulary maturity property.

10. **Methodology-doc-vs-pattern-catalog asymmetry persists** — both surfaces show ~60% zero-cited rates. Canonical-artifact proliferation outpaces canonical-artifact adoption. Distinct from vocabulary-drift problem (which the May 4 watch-file addresses); needs corpus-coherence cycle as a structural fix candidate.

### Phase 3: Anti-Pattern Index Update

**Updated**: `docs/internal/architecture/current/anti-pattern-index.md`

**6 new entries** (last scan 2026-02-03):
- **A-12 Alive Scaffolding** (Architecture) — Architect 2026-05-04 review canonical instance
- **T-05 Activation-flag theater** (Testing) — PPM Phase F v4 framing 2026-04-26
- **P-12 Broad git-add multi-agent sweep** (Process) — multiple in-window incidents
- **P-13 Commit-attribution drift** (Process) — consequence of P-12; cross-referenced
- **P-14 Silent rubric/canonical extension** (Process) — Pattern-063 precursor
- **P-15 Branch-collision in shared working tree** (Process) — 4+ in-window incidents

**Plus**: Pattern-024 status corrected (Proven → Superseded by methodology-00 v2.0; commit `fa0e71a3` reference; Apr 28 retirement of `excellence_flywheel_integration.py` commit `adfd453b` noted).

**Quick Reference category counts updated**: Testing 4 → 5; Architecture 11 → 12; Process/Methodology 11 → 15. Total indexed: 43 → 49.

**Reverse Index updated** with cross-references to pattern-063, pattern-064, methodology-24-BRANCH-OR-ANCHOR, CLAUDE.md "Git Worktrees" section, CLAUDE.md "Mailbox Discipline" section.

---

## Deliverables

### New canonical artifacts (commit this session)

| Path | Purpose | Status |
|---|---|---|
| `dev/active/pattern-library-index.md` | Phase 1 enumeration | NEW |
| `dev/active/pattern-usage-analysis.md` | Phase 2B usage frequency + surface mix | NEW |
| `dev/active/pattern-novelty-candidates.md` | Phase 2C TRUE EMERGENCE + NEAR-MISSES | NEW |
| `dev/active/pattern-evolution-report.md` | Phase 2D evolution events + anti-pattern candidates + stale list | NEW |
| `dev/active/pattern-meta-synthesis.md` | Phase 2E CIO meta-pattern synthesis | NEW |
| `docs/internal/development/reports/pattern-sweep-2.0-results-2026-05-09.md` | Phase 4 final synthesis (this document) | NEW |
| `docs/internal/architecture/patterns/pattern-066-stacked-silent-failures.md` | Pattern-066 Emerging filing | NEW |
| `docs/internal/architecture/current/anti-pattern-index.md` | 6 new entries + scan metadata + reverse index | UPDATED |
| `docs/internal/architecture/patterns/README.md` | Total count updated 64 → 66 | UPDATED |
| `docs/internal/architecture/patterns/pattern-024-methodology-patterns.md` | Status: Proven → Superseded | UPDATED |

---

## Recommendations for Next Cycle

### Immediate (next CIO session)

1. **PM concurrence on Pattern-066 slot allocation** — pattern filed Emerging under self-approval; PM concurrence recommended given recent slot-conflict precedent (Pattern-063 vs. Pattern-064)
2. **Distribute this report to leadership** — workstream-input shape; CC PM/exec primary
3. **Close GitHub issue #1025** with this report linked + acceptance criteria checked

### Near-term (next 2-4 weeks)

4. **Triage stale patterns**: 9 candidates (029, 030, 035, 039, 055, 056, 057, 058, 060) need disposition (verify / refresh / retire / redirect). ~1 session of CIO + Docs work.
5. **Metadata-cleanup ticket** for status-vocabulary inconsistency surfaced in Phase 1 (patterns 039/040 template-literal contamination + non-canonical Status across patterns 031/034/036/037/038/044-054)
6. **Methodology-Elevated lifecycle stage** discussion — formalize concept; identify retroactive candidates (P-045, P-049 likely qualify); update pattern-catalog README to recognize the stage

### Structural (post-M2 sprint)

7. **Corpus-coherence cycle** — proposed new audit cadence that addresses canonical-artifact-zero-citation rate at both pattern-catalog and methodology-corpus layers. Distinct from vocabulary-drift sweep (S1, watch-file shipped May 4). Could be a Phase 5 add to Pattern Sweep 2.0 framework, or a separate cadence triggered by audit-cascade. Worth surfacing for PM + exec discussion.
8. **Pattern-filing checklist update** — add: "*Does this pattern diagnose any aspect of its own emergence or formalization process?*" — captures the catalog self-instrumentation maturity property.
9. **1:N anti-amnesia ratio tracking** across sweeps — capture as catalog-discrimination maturity metric.

### Pattern Sweep 2.0 framework refinements (for next sweep)

10. **Phase 1 metadata fields**: add "Methodology-Elevated" to status taxonomy if/when stage is formalized; add "name-citations vs. number-citations dominance" field per Phase 2B feedback
11. **Phase 2B citation-counting refinement**: dedupe by content hash on mail traffic (3-6× inflation noted); flag bare `P1`/`P2` collision with priority labels; foundational patterns (001-018) marked "presumed-active in code; cite by number only"
12. **Phase 2D anti-pattern category expansion**: consider M-xx category for orphan-methodology drift (zero-cite phenomenon at catalog layer)

---

## Catalog State Snapshot (post-sweep)

| Metric | Value |
|---|---|
| Total patterns | 66 (was 65 pre-sweep; Pattern-066 Stacked Silent Failures filed today) |
| Patterns Proven | 60 (estimated; includes 062 family promotion May 8) |
| Patterns Emerging | 6 (includes Pattern-066 just filed; 062 family promoted out of Emerging today) |
| Patterns Superseded | 1 (Pattern-024, status corrected today) |
| Patterns truly stale (next-cycle triage) | 9 |
| Anti-patterns indexed | 49 (was 43; +6 this scan) |
| Citations in window (Mar 17 → Apr 28) | 3,361 |
| TRUE EMERGENCE this cycle | 1 |
| NEAR-MISSES this cycle | 8 |
| Anti-amnesia ratio (TRUE EMERGENCE : NEAR-MISSES) | 1:8 |

---

## Closing

The pattern catalog is operating as designed: anti-amnesia infrastructure correctly classifying evolution-vs-novelty; new patterns rapidly absorbing operational discipline; existing patterns migrating off original substrates as diagnostic vocabulary. The 062 family completion is the structural event that this window will be remembered for; the methodology-compounding-rate observation is the new property worth tracking forward.

The 9 stale patterns and 60%-zero-citation rate are real signals warranting next-cycle triage. The catalog has dead weight; that's normal at this maturity stage; the discipline is to surface and disposition it rather than let it accumulate.

— CIO, 2026-05-09

*Distribution: PM (CEO) primary; exec (Chief of Staff) for synthesis; Architect (Pattern-064 author + family-table convention author); CXO/PPM/HOST/Comms/Lead Dev/PA/Docs leadership cohort. Acknowledgment optional; substantive feedback welcome.*

*GitHub issue #1025 close-out commentary will reference this report.*
