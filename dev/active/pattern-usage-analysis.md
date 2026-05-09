# Pattern Usage Analysis — Phase 2B

**Built**: 2026-05-09
**Window**: 2026-03-17 → 2026-04-28 (closed-closed, 43 days)
**Phase**: Phase 2B of Pattern Sweep #1025 — usage/citation analysis
**Builder**: Usage Analyst sub-agent under CIO orchestration
**Source index**: `dev/active/pattern-library-index.md` (65 patterns)

## Methodology

A "citation" was counted from these surface types and forms:

- **Explicit number form**: regex `[Pp]attern[-_]0*N\b` (e.g. `Pattern-062`, `pattern-62`, `pattern_062`). Bare `P1` / `P2` / `P062` excluded — they collide with priority labels and Phase markers in this codebase.
- **Signature term**: case-insensitive substring match against a curated 1–3 term list per pattern derived from the Phase 1 index. Terms were narrowed (e.g. "Excellence Flywheel" rather than "methodology" alone) to avoid generic-vocabulary noise.

Citations are summed across:

- **Omnibus logs** in `docs/omnibus-logs/2026-{03-17..04-28}-omnibus-log.md` — 42 files
- **Session logs** under `dev/2026/03/` and `dev/2026/04/` (in-window by directory date) — 409 files
- **Mailbox files** under `mailboxes/**/*.md` whose filename contains an in-window YYYY-MM-DD — 971 files. Note: the same memo often appears 3–6 times (sender's `sent/`, multiple recipient `inbox/` and `read/` mirrors), which inflates raw mail counts but reflects real cross-agent visibility.
- **Git commit messages** for `git log --since=2026-03-17 --until=2026-04-29` — single concatenated text body.

Total citations counted across all 65 patterns: **3,361**. **27 patterns** received at least one citation; **38 patterns** received zero. Surface mix:

| Surface | Citations | % |
|---|---:|---:|
| Mail (with mirror duplication) | 2,190 | 65.2% |
| Session logs | 824 | 24.5% |
| Omnibus logs | 218 | 6.5% |
| Git commit messages | 129 | 3.8% |

Mailbox dominance is partly real (memos drive cross-agent diffusion) and partly artifact (each memo lives in 3–6 places). Deduplicated, mail probably accounts for ~22% of distinct citations and session logs become the primary surface — meaning **patterns are being used most heavily in lived working narrative, not in distilled methodology references**. That is the desired profile.

## 1. Frequency table — patterns with at least one citation

Sorted by total citations (combined surfaces). Surface columns: omni / session / mail / git. **27 of 65 patterns received at least one citation during the window.**

| # | Pattern | omni | session | mail | git | TOTAL | Primary surfaces (top 2 by hit count) |
|---|---|---:|---:|---:|---:|---:|---|
| 063 | Parallel-Authoring Drift | 39 | 139 | 703 | 52 | **933** | Mail dominant (slot-conflict broadcast + PM concurrence + Methodology-24/25 filing); omnibus 4/27 (22), 4/28 (8) |
| 062 | Assembly Assumption | 49 | 187 | 372 | 23 | **631** | Session logs + mail (M1 audit, omnibus drift, Apr 16 Flywheel formalization as 5th practice) |
| 045 | Green Tests, Red User | 28 | 141 | 408 | 9 | **586** | Mail + session logs (canonical-retest discipline, memo-propagation analogy) |
| 064 | Extension Without Integration | 28 | 87 | 354 | 19 | **488** | Apr 28 omnibus (16); Apr 26 Arch slot-conflict memo (12); ADR-061 review memo (12) |
| 024 | Methodology Patterns (Excellence Flywheel) | 18 | 65 | 110 | 7 | **200** | Apr 16–17 reformulation arc; Apr 28 **retirement** commit (`adfd453b`). All citations are signature-term ("Excellence Flywheel"); zero number-form. See §4. |
| 049 | Audit Cascade | 41 | 89 | 37 | 9 | **176** | Mar 21 Lead Dev quality-audit-cascade run (4 cascades in one session); Apr 17 methodology audit; Apr 21 review-week cadence |
| 028 | Intent Classification | 6 | 42 | 115 | 1 | **164** | Apr 23–25 Gemma local-model triage (intent-classification as candidate task); Apr 26–27 1002/1003 boundary work. Attribution caveat: most cites the runtime task, not the pattern-as-design. See §4. |
| 065 | Continuity Memo Before The Seam | 3 | 13 | 36 | 3 | **55** | Apr 17 methodology audit (5); Apr 23 migration-experience confer; filed under self-approval Apr 27 |
| 012 | LLM Adapter | 3 | 9 | 10 | 3 | **25** | Apr 14–16 Gemini wiring + ethics-classifier work referencing `services/llm/` abstraction |
| 031 | Plugin Wrapper (GREAT-3A) | 0 | 2 | 20 | 0 | **22** | Apr 26 Arch 1002-scoping memo: "Pattern-031 (Provider-Agnostic) pairs naturally" for ethics LLM client |
| 053 | Warmth Calibration | 0 | 14 | 6 | 1 | **21** | Apr 16 #950 floor-prompt issue body — calibration retained as load-bearing code convention. See §4.D. |
| 047 | Time Lord Alert | 0 | 10 | 0 | 1 | **11** | Mar 28 Piper Alpha briefing v0.1/v0.2 escape-hatch language; Apr 25 Arch Chat-to-Code handoff |
| 006 | Verification-First | 0 | 5 | 6 | 0 | **11** | Apr 16 CIO Flywheel audit + Excellence Flywheel archaeology; Apr 25 Agent 360 response |
| 043 | Defense-in-Depth | 0 | 4 | 3 | 1 | **8** | Apr 17 methodology audit; Apr 14 #960/#961 context-contract audit |
| 029 | Multi-Agent Coordination | 0 | 1 | 4 | 0 | **5** | Mar 30 docs-audit findings; Apr 22 host-to-docs briefing-correction |
| 035 | MCP Adapter Methods | 1 | 3 | 1 | 0 | **5** | Mar 22 omnibus; Mar 30 docs audit + CIO weekly + Arch workstream review |
| 046 | Beads Completion Discipline | 0 | 0 | 4 | 0 | **4** | Apr 27 CIO briefing-correction routing |
| 059 | Leadership Caucus | 1 | 1 | 1 | 0 | **3** | Apr 22 docs welcome-and-ack + omnibus |
| 007 | Async Error Handling | 0 | 2 | 0 | 0 | **2** | Apr 27 codebase-review batches (architecture-review mention, low-confidence) |
| 013 | Database Session Management | 0 | 2 | 0 | 0 | **2** | Apr 12 Docs-to-Janus memory-prior-art memo |
| 021 | Development Session Management | 0 | 2 | 0 | 0 | **2** | Mar 23 audit cross-ref fixes; pattern doc edit |
| 061 | Human-AI Collaboration Referee | 0 | 2 | 0 | 0 | **2** | Mar 30 Docs audit; pattern README touch |
| 004 | CQRS-lite | 1 | 1 | 0 | 0 | **2** | Residual after false-positive removal — query-architecture commentary in #964 findings |
| 030 | Plugin Interface | 0 | 1 | 0 | 0 | **1** | Cross-ref in pattern README touch |
| 034 | Error Handling Standards | 0 | 1 | 0 | 0 | **1** | Cross-ref in API-route audit |
| 051 | Parallel Place Gathering | 1 | 0 | 0 | 0 | **1** | Single architecture mention |
| 056 | Consciousness Attribute Layering | 0 | 1 | 0 | 0 | **1** | Single grammar-cluster mention |

## 2. Top 10 most-cited patterns

| Rank | # | Pattern | Total | One-line context |
|---:|---|---|---:|---|
| 1 | **063** | Parallel-Authoring Drift | 933 | Dominates Apr 26–28 traffic. Slot conflict + PM concurrence + Methodology-24/25 Branch-or-Anchor + Colleague Test v2.3 inclusion. The Apr 26 Arch→CIO slot-conflict memo and PA-routed PM concurrence filing (`a5d82e82`) drove cross-agent broadcast. |
| 2 | **062** | Assembly Assumption | 631 | Dominant in Apr 16–22 omnibus-drift remediation, M1 audit, and Excellence Flywheel "Audit the composition" 5th-practice formalization. By Apr 22 Pattern-062 was being applied recursively to the omnibus-synthesis surface itself. |
| 3 | **045** | Green Tests, Red User | 586 | Stable through-line citation across Lead Dev (canonical retest), Architect (memo-propagation analogy), and PPM (eval harness sign-off). Apr 19 omnibus generalizes it from "good code, wrong infra" to "good memo, wrong source." |
| 4 | **064** | Extension Without Integration | 488 | Apr 25 sketch → Apr 28 formalization. Sibling sub-pattern of 062. Concentrated in Architect's ADR-061 work and the 062/063/064 family-table memos. |
| 5 | **024** | Methodology Patterns (Excellence Flywheel) | 200 | Heavy meta-discourse: 8 distinct formulations archaeology'd, three-layer canonical resolution, then the Flywheel itself **retired Apr 28** (`adfd453b`). Citation count is high but Pattern-024 may need its own status disposition in Phase 2D. |
| 6 | **049** | Audit Cascade | 176 | Operationally healthy. Cited as a verb (Lead Dev "begins #909 audit cascade") and as a methodology unit (Apr 17 audit). Pattern-049 broken-link fix landed Apr 11 (`6759b912`). |
| 7 | **028** | Intent Classification | 164 | Mostly attributable to the **task name** (intent classification as a runtime function in the local-model Gemma triage Apr 23–25), not the pattern as design discipline. Real but ambiguous attribution — see §4. |
| 8 | **065** | Continuity Memo Before The Seam | 55 | Filed Apr 27 under self-approval; cited primarily in Apr 17 methodology audit (predicting it as Emerging candidate) and Apr 23 migration-experience confer. New pattern entering active use. |
| 9 | **012** | LLM Adapter | 25 | Mid-window references to the existing `services/llm/` abstraction in Apr 14–16 Gemini-wiring discussions and ethics-classifier scoping. Foundational architecture, not novel work. |
| 10 | **031** | Plugin Wrapper (GREAT-3A) | 22 | Apr 26 Arch 1002-scoping memo cites Pattern-031 explicitly to argue the new ethics LLM client should reuse the floor's `model_tier` resolution rather than introduce a new tier. Pattern-031 is functioning as an architectural constraint. |

## 3. Patterns with **zero citations** during the window

**38 of 65 patterns** received zero attributable citations 2026-03-17 → 2026-04-28. Listed by category:

**Core Architecture (legacy, foundational)**: 001 (Repository Pattern), 002 (Service Pattern), 003 (Factory Pattern), 005 (Transaction Management), 008 (DDD Service Layer), 011 (Context Resolution), 014 (API Error Contract), 015 (Internal Task Handler), 016 (Repository Context Enrichment), 017 (Background Task Error), 018 (Configuration Access)

**Methodology**: 009 (GitHub Issue Tracking — practice is omnipresent but never named-as-pattern), 010 (Cross-Validation Protocol)

**AI & Intelligence (legacy)**: 019 (LLM Placeholder Instruction), 020 (Spatial Metaphor / PM-074), 022 (MCP+Spatial 8-D), 023 (Query Layer / Circuit Breaker), 025 (Canonical Query Extension), 026 (Cross-Feature Learning), 032 (Intent Pattern Catalog)

**Integration & Platform**: 027 (CLI Integration), 033 (Notion Publishing), 040 (Integration Swappability), 044 (MCP Skill Testing)

**Investigation & Root Cause**: 041 (Systematic Fix Planning), 042 (Investigation-Only Protocol), 060 (Cascade Investigation)

**Methodology meta-patterns** (Nov 2025 trio + Jan 2026 prioritization): 036 (Signal Convergence), 037 (Cross-Context Validation), 038 (Temporal Clustering), 039 (Feature Prioritization Scorecard)

**Core Architecture (recent)**: 048 (Periodic Background Job)

**Grammar Application** (2026-01-20 cluster, partial): 050 (Context Dataclass Pair), 052 (Personality Bridge), 054 (Honest Failure with Suggestion)

**AI & Intelligence (Jan 2026 cluster)**: 055 (Multi-Intent Decomposition), 057 (Grammar-Driven Classification), 058 (Ownership Graph Navigation)

### Full zero-citation pattern list (verbatim)

`P001, P002, P003, P005, P008, P009, P010, P011, P014, P015, P016, P017, P018, P019, P020, P022, P023, P025, P026, P027, P032, P033, P036, P037, P038, P039, P040, P041, P042, P044, P048, P050, P052, P054, P055, P057, P058, P060`

### Phase 2D Evolution Tracker handoff signals

- **"Alive in code, silent in discourse"**: Patterns 001 (Repository), 002 (Service), 003 (Factory), 005 (Transaction Management), 008 (DDD Service Layer), 011 (Context Resolution), 013 (Database Session Management — only 2 cites), 014–018. These are foundational architectural patterns presumed-active in the codebase but receive zero or near-zero diagnostic-vocabulary citation. Phase 2D should distinguish "alive in code, dormant in discourse" from "dormant in both" by sampling actual `services/` code or git-blame on canonical exemplars before recommending retirement.
- **Possibly absorbed**: Pattern-024 (Methodology Patterns / Excellence Flywheel) was **retired Apr 28** (`adfd453b`). Its 200 citations are entirely the reformulation-then-retirement arc; zero number-form citations. Phase 2D should mark Pattern-024 status as Withdrawn (or Superseded by CLAUDE.md operational principles).
- **Recently born, no traction yet**: 055 (Multi-Intent Decomposition), 057 (Grammar-Driven Classification), 058 (Ownership Graph Navigation) — all born 2026-01-21, all zero citations. 050 (Context Dataclass Pair), 052 (Personality Bridge), 054 (Honest Failure with Suggestion) all born 2026-01-20, all zero or single-cite. Either too new for vocabulary diffusion or not matching real failure modes during the window.
- **Meta-patterns dormant**: 036 (Signal Convergence), 037 (Cross-Context Validation), 038 (Temporal Clustering) — the November 2025 meta-pattern trio — all received zero citations. Worth checking if they've been absorbed into Pattern-049 (Audit Cascade) practice or simply not used.
- **Likely absorbed by 062 family**: 060 (Cascade Investigation) — only README cross-references during window. The 062/063/064 family-table emergence may have functionally replaced its diagnostic role.
- **Pattern-039 (Feature Prioritization Scorecard)**: zero citations despite the M1/M2/Phase F decision-arc throughout the window using ad-hoc scoring. Either the scorecard is being applied without naming, or it's not being used. Worth checking against actual prioritization decisions in the window.

## 4. Unusual applications

Five instances where a pattern was applied in a context notably different from its origin:

### A. Pattern-062 (Assembly Assumption) applied to omnibus synthesis

**Origin context**: M0 sprint, code-layer integration (individually-passing slices fail to compose).
**Window application**: 2026-04-22, Docs files `feedback_omnibus_source_drift.md` after the Apr 16 omnibus was found to have been synthesized from an incomplete source set. The Pattern-062 lens — "individually-correct components producing collectively-incomplete outcomes" — was applied to the omnibus-synthesis layer itself, with the diagnostic "if omnibus content mentions a role without citing that role's own session log in Sources, the omnibus is probably partial."
**Why notable**: Cross-layer transposition from code integration (composition of feature slices) to documentation synthesis (composition of session-log inputs). The Apr 16 omnibus drift, the HOST handoff missing from worktree, and the branch collision were all named as "the same Pattern-062 failure mode in three substrates in one day." This recursion is the strongest signal in the window that Pattern-062 has become organizational vocabulary rather than a procedural template.

### B. Pattern-045 (Green Tests, Red User) applied to memo propagation

**Origin context**: Code-layer testing — unit tests pass against mocks while real users hit infrastructure failures.
**Window application**: 2026-04-19, Architect generalizes Pattern-045 to "good memo, wrong source": LLM-polished output (whether AI or well-written colleague) can mask gaps the reader doesn't notice. Apr 19 omnibus: *"Same failure, six independent agents, ninety minutes — this is Pattern-045 at the methodology layer."*
**Why notable**: Pattern moves from code-test-vs-real-infra to written-claim-vs-canonical-source. The same discipline (verify against canonical source before propagating) is shown to apply to PDR-004 principles, workstream memos, and architectural cross-agent summaries. Pattern's substrate expanded from infrastructure-correctness to source-fidelity.

### C. Pattern-049 (Audit Cascade) applied as a verb-form workflow

**Origin context**: Multi-step methodology gates between handoffs (audit-and-correct between phases).
**Window application**: 2026-03-21 Lead Developer "begins #909 audit cascade", "begins #910 audit cascade", "begins #898 audit cascade" — running four audit-cascade *units* in a single session as a unit of bug investigation, not as a methodology phase-gate.
**Why notable**: Pattern's grammatical role shifts from noun (methodology gate) to verb (action one performs on a specific issue). Diagnostic vocabulary becoming workflow vocabulary — agents using "let's run an audit cascade on this" as natural-language scheduling.

### D. Pattern-053 (Warmth Calibration) load-bearing in code architecture

**Origin context**: Grammar-application cluster, January 2026 — feedback feeling hollow when emotional tone doesn't match observed data.
**Window application**: 2026-04-16 #950 issue body, Lead Dev's floor-prompt evolution work cites `format_warmth_guidance()` as the calibration substrate to **retain unchanged** during the floor rewrite — explicitly listing "warmth calibration via formality_baseline retained" as an acceptance criterion.
**Why notable**: Pattern-053 has crossed from a methodology guideline into a load-bearing code convention — the function `format_warmth_guidance(formality_baseline)` is now treated as canonical and is protected from rewrite. The pattern has materialized into structural debt-on-purpose.

### E. Pattern-031 (Plugin Wrapper) applied to ethics-detection LLM client

**Origin context**: GREAT-3A plugin architecture — vendor-agnostic PM-tool integrations.
**Window application**: 2026-04-26 Arch 1002-scoping memo: *"Pattern-031 (Provider-Agnostic) pairs naturally — same `model_tier` resolution as the floor uses."* The pattern is invoked to argue against introducing a new model tier for the ethics-boundary LLM detector, instead reusing the floor's existing tier-resolution machinery.
**Why notable**: Pattern crosses domain — from PM-tool plugin (Linear / Jira / Notion adapters) to LLM-provider tier resolution inside ethics enforcement. The vendor-agnosticism principle generalizes from "swap PM tool" to "swap model provider," which is a different abstraction altogether but shares the contract-not-implementation logic.

## 5. Surface mix observation

The 65.2% / 24.5% / 6.5% / 3.8% mail / session / omni / git split (raw, before mail-mirror dedup) tells two distinct stories:

**Mail dominates raw counts because the per-memo commit-and-push norm replicates each memo across 3–6 mailbox locations** (sender's `sent/`, each recipient's `inbox/` and post-triage `read/`). This is real visibility — every recipient sees the citation when they triage their inbox — but it inflates citation volume by roughly 4×. Deduplicated, mail's share probably falls to ~22%, putting **session logs on top at ~38%** of distinct citations.

**Session logs are the right primary surface for methodology adoption**. They're where agents work out their own diagnoses, where they cite a pattern as a way of explaining what just failed, and where the pattern enters the agent's working vocabulary. Pattern-062's 187 session-log hits across the window — substantially higher than its 49 omnibus-log hits — means agents are reaching for "Assembly Assumption" as their own diagnostic phrase, not just inheriting it from omnibus synthesis.

**Omnibus citations (218) are the strongest signal of cross-day pattern fluency**, since omnibus synthesis is itself a Pattern-062-vulnerable activity (composing individually-correct session-log inputs into a collectively-correct daily narrative). The fact that the top three omnibus-cited patterns (062, 045, 049) all have explicit recursive applications to the synthesis surface itself is a feature, not a coincidence — the patterns most-cited in omnibus are the ones that omnibus authors are using to audit their own work.

**Git commit messages (129, 3.8%) are the lightest surface but the most authoritative** — when a commit message says "Pattern-063," that's a load-bearing claim the author is making about what the commit does. The 062/063/064 family generates 94 of the 129 git citations (73%), reflecting that pattern-filing was a major Apr 26–28 activity.

**Temporal concentration**: Pattern-062-family citations (062 + 063 + 064) in omnibus logs spike in the second half of the window — Apr 17 (6 cites), Apr 22 (7), Apr 26 (8), Apr 27 (14), Apr 28 (14). The first three weeks of the window saw 1–2 cites per omnibus; the family arc is concentrated in a 12-day burst Apr 17–28.

**Implication for Phase 2C/2D**: novelty detection should weight session-log appearances over omnibus appearances (omnibus tends to amplify already-known patterns); evolution tracking should weight recurring session-log diagnostic phrases (Pattern-062 said-as-noun across 14+ files per the Apr 17 PA reference audit) over omnibus repeats. Mail traffic is informative for measuring cross-agent visibility but should be deduplicated by content hash before being treated as citation density.

## Phase handoff notes

### Patterns flagged for follow-up (Phase 2C Novelty / 2D Evolution)

- **Pattern-024 status disposition**: retired Apr 28; needs Withdrawn / Superseded marker. Status currently Proven in index.
- **Pattern-062 → 063 → 064 family arc**: filing dates and inter-citation density form a clear evolution line. Phase 2D should map the family-table emergence as a single arc rather than three independent patterns.
- **Pattern-065 (Continuity Memo)**: just-filed during window; insufficient citation history to assess uptake. Re-check Phase 2D after May–June window.
- **Pattern-053 → code-substrate transition** (§4.D): a Grammar Application pattern crossed into structural code convention. May warrant a dedicated note that the pattern is now de-facto-frozen.
- **Pattern-028 attribution ambiguity**: 164 citations, but most reference the runtime task name (intent classification function), not the pattern as design discipline. Phase 2D may want to split future tracking by attribution form.

### Data gaps for Phase 1 index refinement

- **Mailbox file-date heuristic**: 971 mailbox files matched by in-name YYYY-MM-DD; some real Apr–Mar memos have different naming and were missed. Phase 1 (or a pre-Phase-2C pass) could index mailbox files by git-add-date for a more reliable in-window filter.
- **Mail-mirror deduplication**: same memo counted 3–6× because it lives in sender + recipient inbox + recipient read. Phase 2D evolution tracking should dedupe by content hash before computing per-pattern velocity.
- **`P1` / `P2` / `P3` collide with priority labels**: had to tighten regex to require literal `pattern[-_]` prefix. Patterns 001–005 lost most of their apparent citations; the residual is real. Phase 1 index could note the false-positive risk for low-numbered patterns explicitly.
- **"Pattern N — " section-heading false positives** in memos (sections "Pattern 1", "Pattern 2" used as observation labels) — same regex tightening fixed.
- **Signature-term false positives**: "circuit breaker" matches PA-as-circuit-breaker metaphor (not Pattern-023); "RICE" matches accidental letter sequences (e.g., "**Apr**ICE"); "8-dimensional" is from pre-window MCP+Spatial era. Future passes should use multi-word signatures (e.g., `Pattern-023 (Query Layer)` only) for foundational patterns where common-word noise is high.
- **Pattern-024 vs. Excellence Flywheel attribution**: nearly all Pattern-024 hits are signature-term ("Excellence Flywheel") not number-form. Phase 2D should decide whether a content-name citation counts equivalently to a number citation — some patterns (like 024) are essentially never cited by number.

---

*Built by Usage Analyst sub-agent under CIO orchestration. Pattern-062 (Assembly Assumption) recursively applies to this analysis itself: verify pattern_scan results haven't dropped a surface (git history checked, mailbox scan checked, session logs verified by sample). Total citations 3,361 across 27 patterns receiving at least one hit; 38 patterns at zero.*
