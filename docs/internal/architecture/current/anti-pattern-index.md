# Anti-Pattern Index

**Purpose**: Cross-reference index of anti-patterns documented throughout the codebase. Links to source documents without duplicating content.

**Last Scan**: 2026-05-09 (Pattern Sweep #1025 Phase 3 update; prior scan 2026-02-03)
**Documents Scanned**: 65 patterns, 12+ ADRs, methodology-00/24/25/26, 28+ omnibus logs Mar 17 → Apr 28, recent CIO/Architect/CXO/PPM memos in `mailboxes/`

---

## Quick Reference by Category

| Category | Count | Key Sources |
|----------|-------|-------------|
| Grammar/Consciousness | 12 | grammar-transformation-guide, consciousness-philosophy, ownership-metaphors |
| Testing | 5 | pattern-045, pattern-049, Phase F catch-22 reframe |
| Architecture | 12 | ADR-006, ADR-010, ADR-039, ADR-040, ADR-043, ADR-051, Pattern-064 |
| Process/Methodology | 15 | pattern-046, pattern-047, systematic-excellence, omnibus-logs, multi-agent commit hygiene Apr 26-May 5, Pattern-063 precursor |
| Integration | 5 | pattern-035, pattern-054 |

**Total Indexed**: 51 anti-patterns (43 prior + 6 added 2026-05-09 + 2 added 2026-05-11). P-13 / P-15 / P-16 / P-17 are now cross-referenced as child sub-instances of [pattern-068 Silent State Mutation in Shared Working Tree](patterns/pattern-068-silent-state-mutation-shared-working-tree.md).

---

## Grammar & Consciousness Anti-Patterns

Anti-patterns related to the MUX grammar ("Entities experience Moments in Places") and preserving consciousness in responses.

| ID | Anti-Pattern | Source | Recommended Pattern |
|----|--------------|--------|---------------------|
| G-01 | Query language in responses | [grammar-transformation-guide.md#anti-pattern-1-query-language-in-responses](../../development/grammar-transformation-guide.md#anti-pattern-1-query-language-in-responses) | [Pattern-052](patterns/pattern-052-personality-bridge.md) |
| G-02 | Timestamps without context | [grammar-transformation-guide.md#anti-pattern-2-timestamps-without-context](../../development/grammar-transformation-guide.md#anti-pattern-2-timestamps-without-context) | [Pattern-053](patterns/pattern-053-warmth-calibration.md) |
| G-03 | IDs instead of names | [grammar-transformation-guide.md#anti-pattern-3-ids-instead-of-names](../../development/grammar-transformation-guide.md#anti-pattern-3-ids-instead-of-names) | EntityProtocol |
| G-04 | Config strings as Places | [grammar-transformation-guide.md#anti-pattern-4-config-strings-as-places](../../development/grammar-transformation-guide.md#anti-pattern-4-config-strings-as-places) | PlaceProtocol |
| G-05 | Mechanical error messages | [grammar-transformation-guide.md#anti-pattern-5-mechanical-error-messages](../../development/grammar-transformation-guide.md#anti-pattern-5-mechanical-error-messages) | [Pattern-054](patterns/pattern-054-honest-failure.md) |
| G-06 | Status codes instead of states | [grammar-transformation-guide.md#anti-pattern-6-status-codes-instead-of-states](../../development/grammar-transformation-guide.md#anti-pattern-6-status-codes-instead-of-states) | MomentProtocol |
| G-07 | Raw data dumps | [grammar-transformation-guide.md#anti-pattern-7-raw-data-dumps](../../development/grammar-transformation-guide.md#anti-pattern-7-raw-data-dumps) | [Pattern-052](patterns/pattern-052-personality-bridge.md) |
| G-08 | Treating NATIVE as cache | [ownership-metaphors.md#part-3](ownership-metaphors.md) | Mind/Senses/Understanding model |
| G-09 | Losing place context | [ownership-metaphors.md#part-4](ownership-metaphors.md) | [Pattern-051](patterns/pattern-051-parallel-place-gathering.md) |
| G-10 | Hiding uncertainty | [ownership-metaphors.md#part-5](ownership-metaphors.md) | [Pattern-054](patterns/pattern-054-honest-failure.md) |
| G-11 | Third-person system language | [consciousness-philosophy.md#pillar-1](consciousness-philosophy.md) | First-person presence |
| G-12 | Alert/warning spam tone | [consciousness-philosophy.md#part-5](consciousness-philosophy.md) | Supportive reframing |

---

## Testing Anti-Patterns

Anti-patterns related to testing strategy and verification.

| ID | Anti-Pattern | Source | Recommended Pattern |
|----|--------------|--------|---------------------|
| T-01 | Mocked dependencies hiding integration issues | [pattern-045](patterns/pattern-045-green-tests-red-user.md) | Integration testing requirements |
| T-02 | Schema/model drift not caught by tests | [pattern-045](patterns/pattern-045-green-tests-red-user.md) | Schema validation on startup |
| T-03 | Type mismatches only enforced at DB level | [pattern-045](patterns/pattern-045-green-tests-red-user.md) | Dataclass field validators |
| T-04 | Skipping audit "just this once" | [pattern-049](patterns/pattern-049-audit-cascade.md#anti-patterns) | Audit cascade discipline |
| T-05 | **Activation-flag theater** — Feature flag controls a code path the system never exercises (flag-on and flag-off produce indistinguishable behavior) | PPM Phase F recommendation v4 ("category-conditional theater") + Lead Dev #1003 diagnostic 2026-04-26; ADR-061 calibration reframe; [pattern-064](patterns/pattern-064-extension-without-integration.md) sibling family | Verify flag actually changes behavior before activation; "where does this data come from?" diagnostic question |

---

## Architecture Anti-Patterns

Anti-patterns related to system architecture, configuration, and design decisions.

| ID | Anti-Pattern | Source | Recommended Pattern |
|----|--------------|--------|---------------------|
| A-01 | Dual repository implementations | [ADR-005](adrs/adr-005-eliminate-dual-repository-implementations.md) | Single repository per entity |
| A-02 | get_session() anti-pattern | [ADR-006](adrs/adr-006-standardize-async-session-management.md) | Async session factory |
| A-03 | Direct environment access in domain layers | [ADR-010](adrs/adr-010-configuration-patterns.md#avoid-direct-environment-access) | Configuration service injection |
| A-04 | Mixed configuration patterns in same service | [ADR-010](adrs/adr-010-configuration-patterns.md#avoid-mixed-patterns) | Consistent access patterns |
| A-05 | Database stored procedures for app logic | [ADR-043](adrs/adr-043-application-layer-stored-procedures.md) | Application layer logic |
| A-06 | Shared database across environments | [ADR-040](adrs/adr-040-local-database-per-environment.md) | Local database per environment |
| A-07 | **LLM-for-Everything** - Using LLM for deterministic operations | [ADR-039](adrs/adr-039-canonical-handler-pattern.md) | Canonical handlers for simple queries |
| A-08 | **Keyword-Only Matching** - Pure keyword matching without LLM capability | [ADR-039](adrs/adr-039-canonical-handler-pattern.md) | Hybrid approach |
| A-09 | **Shared Dev Database** - Multiple environments sharing one database | [ADR-040](adrs/adr-040-local-database-per-environment.md) | Local database per environment |
| A-10 | **Thread-Local Injection** - Implicit context via thread locals | [ADR-051](adrs/adr-051-unified-user-session-context.md) | Explicit parameter passing |
| A-11 | **Verification Theater** - Process without actual verification | [ADR-028](adrs/adr-028-verification-pyramid.md) | Evidence-based verification pyramid |
| A-12 | **Alive Scaffolding** — try/except masking inactive paths that *appear* live but never execute (e.g., `Optional[Dependency]` accepted, never instantiated in production DI; if-guarded paths permanently dead) | Architect 2026-05-04 architectural-soundness-review (KnowledgeGraphService legacy `BoundaryEnforcer` import; `boundary_enforcer_refactored.py:343-358` adaptive-learn TODO); [pattern-064](patterns/pattern-064-extension-without-integration.md) | Sweep-style cleanup; phantom-method-call detection; remove dead allocation + commented call together |

---

## Process/Methodology Anti-Patterns

Anti-patterns related to development workflow and agent behavior.

| ID | Anti-Pattern | Source | Recommended Pattern |
|----|--------------|--------|---------------------|
| P-01 | 75% complete then abandoned | [pattern-046](patterns/pattern-046-beads-completion-discipline.md) | Beads completion discipline |
| P-02 | Rationalizing incomplete work as "optional" | [pattern-046](patterns/pattern-046-beads-completion-discipline.md) | Explicit PM approval for deferrals |
| P-03 | Proceeding with uncertainty (completion bias) | [pattern-047](patterns/pattern-047-time-lord-alert.md) | Time Lord Alert escape hatch |
| P-04 | Silent escalation avoidance | [pattern-047](patterns/pattern-047-time-lord-alert.md#anti-patterns-it-prevents) | Explicit uncertainty signals |
| P-05 | **"Good Enough" Trap** - Shipping code that "works" without considering maintainability | systematic-excellence.md *(proposed; doc TBD)* | Define "done" to include excellence |
| P-06 | **"Refactor Later" Lie** - Promising cleanup that never happens | systematic-excellence.md *(proposed; doc TBD)* | Refactor as you go |
| P-07 | **"Deadline" Pressure** - Sacrificing quality for speed | systematic-excellence.md *(proposed; doc TBD)* | Negotiate scope, not quality |
| P-08 | **80% Completion Trap** - Declaring done without evidence | [the-completion-discipline-draft.md](../../../public/comms/drafts/superseded/the-completion-discipline-draft.md) | Completion matrix with evidence |
| P-09 | **"Should Have Known" Syndrome** - Reactive discovery of obvious requirements | [2025-10-29-omnibus-log.md](../../../omnibus-logs/2025-10-29-omnibus-log.md) | Comprehensive upfront audit |
| P-10 | **Escalation Timing Failure** - Debugging too long before seeking help | [2025-11-16-omnibus-log.md](../../../omnibus-logs/2025-11-16-omnibus-log.md) | Escalate after first untested commit |
| P-11 | **Comment-Only Close** - Closing issues with comments but no evidence or unchecked acceptance criteria | [2026-01-25-omnibus-log.md](../../../omnibus-logs/2026-01-25-omnibus-log.md) | Update description checkboxes, provide evidence |
| P-12 | **Broad git-add multi-agent sweep** — `git add -A` or `git add <directory>` on `main` while other agents have unstaged work; sweeps up other agents' files into your commit | Multiple incidents: CXO commit `8a8a8a9d` swept CIO files Apr 27; Docs commit `11225a69` swept CIO files May 4; Lead Dev incident Apr 27 swept 17 PPM moves | Surgical staging — explicit file paths only; `git add foo bar baz` not `git add .` or `git add mailboxes/`; `git diff --cached --name-only` verify before commit |
| P-13 | **Commit-attribution drift** — commit message describes one scope but changeset includes broader work (consequence of P-12; the broad git-add picks up adjacent agents' work into a commit titled around the originator's intent). **Sub-instance of [pattern-068 Silent State Mutation](patterns/pattern-068-silent-state-mutation-shared-working-tree.md)** at the branch-drift layer | CXO commit `8a8a8a9d` "ship-040 feedback" but contained CIO Ship #040 feedback + CIO MANIFEST update; Docs commit `11225a69` "close May 3 log + open May 4 log" but contained 19 CIO inbox renames + S1 watch-file concur + audit table A3 update; Lead Dev May 7 `fc7f685e` log-update landed on feature branch via subagent HEAD-flip | Pair with P-12 fix; commit message should match committed scope; if scope expanded mid-commit, retitle; see [pattern-068](patterns/pattern-068-silent-state-mutation-shared-working-tree.md) for parent-meta-pattern context |
| P-14 | **Silent rubric/canonical extension** — extending a canonical reference (rubric, schema, term, principle, slot allocation) without anchor-or-branch decision; new artifact uses canonical's label with shifted criteria | Apr 26 Phase E rubric C-axis incident (precursor to [pattern-063](patterns/pattern-063-parallel-authoring-drift.md)); Pattern-063 slot-conflict between predecessor Architect Mar 19 informal reservation + CIO Apr 26 independent claim | [methodology-24 Branch-or-Anchor Discipline](../../development/methodology-core/methodology-24-BRANCH-OR-ANCHOR.md); explicit anchor (cite + use) or branch (rename + version); never silent extension |
| P-15 | **Branch-collision in shared working tree** — two agents' work intersects on `main` because one agent checked out a `claude/*` branch in the same working tree another agent was using; HEAD flips out from under the other agent's edits. **Sub-instance of [pattern-068 Silent State Mutation](patterns/pattern-068-silent-state-mutation-shared-working-tree.md)** | Lead Dev → Docs collision Apr 22 (`claude/992-ethics-activate` checkout); PA branch-drift incident Apr 29 (`78010627` v1.0 commit landed on foreign feature branch); Apr 22 omnibus log Lead Dev wrap | CLAUDE.md "Git Worktrees" section; `git worktree add ../piper-morgan-product-{suffix} {branch}` for parallel agent work; `git branch --show-current` at work-cycle boundaries; see [pattern-068](patterns/pattern-068-silent-state-mutation-shared-working-tree.md) for parent-meta-pattern context |
| P-16 | **Cross-agent residue accumulation in shared working tree** — multiple agents' partial-session uncommitted edits accumulate in working tree because no single agent has standing to commit others' files under "commit only your own files" discipline; residue persists across sessions and is at risk of session-end loss. **Sub-instance of [pattern-068 Silent State Mutation](patterns/pattern-068-silent-state-mutation-shared-working-tree.md)** | May 9 evening Docs session with stranded session log + Janus memo (PreCompact-hook first-use catch); May 10 PreCompact-hook first-incident debrief | PreCompact hook as detector; cross-agent committing under PM authority as resolver; routine sign-off-discipline `git status` inventory in session-end blocks per Docs precedent |
| P-17 | **Working-tree-path fragmentation** — agent operates from a worktree path but edits files at the main-checkout's absolute path (or vice versa); the same logical file has two separate physical copies in different trees; `git status` from each shows different results; edits made in one tree are invisible to git operations in the other. **Sub-instance of [pattern-068 Silent State Mutation](patterns/pattern-068-silent-state-mutation-shared-working-tree.md)** | CIO May 10–11 innovation-backlog edits stranded overnight (main-checkout edit not visible to worktree session next morning) | Worktree-path consistency convention: file paths always relative to or anchored in current working-directory's root; commit between cross-tree path changes; see [pattern-068](patterns/pattern-068-silent-state-mutation-shared-working-tree.md) for full discussion |

---

## Integration Anti-Patterns

Anti-patterns related to external service integration.

| ID | Anti-Pattern | Source | Recommended Pattern |
|----|--------------|--------|---------------------|
| I-01 | Silent failures / swallowed exceptions | [pattern-054](patterns/pattern-054-honest-failure.md) | Honest failure with suggestion |
| I-02 | Generic error messages ("Something went wrong") | [pattern-054](patterns/pattern-054-honest-failure.md) | Specific diagnosis + remediation |
| I-03 | **Forgetting initialize()** - Using adapter without async initialization | [pattern-035](patterns/pattern-035-mcp-adapter-methods.md) | Lazy init pattern |
| I-04 | **Non-Idempotent Init** - Initialize that breaks on repeat calls | [pattern-035](patterns/pattern-035-mcp-adapter-methods.md) | Make initialize() idempotent |
| I-05 | **Sync Init for Async Ops** - Synchronous initialization for async operations | [pattern-035](patterns/pattern-035-mcp-adapter-methods.md) | Async initialization |

---

## Reverse Index: Pattern → Anti-Patterns Addressed

| Pattern/Document | Anti-Patterns Addressed |
|------------------|------------------------|
| [Pattern-045](patterns/pattern-045-green-tests-red-user.md) | T-01, T-02, T-03 |
| [Pattern-046](patterns/pattern-046-beads-completion-discipline.md) | P-01, P-02 |
| [Pattern-047](patterns/pattern-047-time-lord-alert.md) | P-03, P-04 |
| [Pattern-049](patterns/pattern-049-audit-cascade.md) | T-04 |
| [Pattern-051](patterns/pattern-051-parallel-place-gathering.md) | G-09 |
| [Pattern-052](patterns/pattern-052-personality-bridge.md) | G-01, G-07 |
| [Pattern-053](patterns/pattern-053-warmth-calibration.md) | G-02 |
| [Pattern-054](patterns/pattern-054-honest-failure.md) | G-05, G-10, I-01, I-02 |
| [ADR-005](adrs/adr-005-eliminate-dual-repository-implementations.md) | A-01 |
| [ADR-006](adrs/adr-006-standardize-async-session-management.md) | A-02 |
| [ADR-010](adrs/adr-010-configuration-patterns.md) | A-03, A-04 |
| [ADR-040](adrs/adr-040-local-database-per-environment.md) | A-06 |
| [ADR-043](adrs/adr-043-application-layer-stored-procedures.md) | A-05 |
| [consciousness-philosophy.md](consciousness-philosophy.md) | G-11, G-12 |
| [ownership-metaphors.md](ownership-metaphors.md) | G-08, G-09, G-10 |
| [grammar-transformation-guide.md](../../development/grammar-transformation-guide.md) | G-01 through G-07 |
| [pattern-035](patterns/pattern-035-mcp-adapter-methods.md) | I-03, I-04, I-05 |
| [ADR-028](adrs/adr-028-verification-pyramid.md) | A-11 |
| [ADR-039](adrs/adr-039-canonical-handler-pattern.md) | A-07, A-08 |
| [ADR-051](adrs/adr-051-unified-user-session-context.md) | A-10 |
| systematic-excellence.md *(proposed; doc TBD)* | P-05, P-06, P-07 |
| [the-completion-discipline-draft.md](../../../public/comms/drafts/superseded/the-completion-discipline-draft.md) | P-08 |
| [2025-10-29-omnibus-log.md](../../../omnibus-logs/2025-10-29-omnibus-log.md) | P-09 |
| [2025-11-16-omnibus-log.md](../../../omnibus-logs/2025-11-16-omnibus-log.md) | P-10 |
| [2026-01-25-omnibus-log.md](../../../omnibus-logs/2026-01-25-omnibus-log.md) | P-11 |
| [pattern-063](patterns/pattern-063-parallel-authoring-drift.md) | P-14 (precursor; the structural fix is methodology-24 Branch-or-Anchor) |
| [pattern-064](patterns/pattern-064-extension-without-integration.md) | A-12 (canonical instance), T-05 (sibling family) |
| [methodology-24-BRANCH-OR-ANCHOR.md](../../development/methodology-core/methodology-24-BRANCH-OR-ANCHOR.md) | P-14 (structural fix) |
| CLAUDE.md "Git Worktrees" section *(proposed; doc TBD)* | P-15 |
| CLAUDE.md "Mailbox Discipline" section *(proposed; doc TBD)* | P-12, P-13 (per-memo commit-and-push + surgical staging norms) |

---

## Scan Methodology

### Documents Scanned (Pilot)

**Patterns** (10):
- pattern-045-green-tests-red-user.md
- pattern-046-beads-completion-discipline.md
- pattern-047-time-lord-alert.md
- pattern-048-periodic-background-job.md
- pattern-049-audit-cascade.md
- pattern-050-context-dataclass-pair.md
- pattern-051-parallel-place-gathering.md
- pattern-052-personality-bridge.md
- pattern-053-warmth-calibration.md
- pattern-054-honest-failure.md

**ADRs** (8):
- adr-005-eliminate-dual-repository-implementations.md
- adr-006-standardize-async-session-management.md
- adr-010-configuration-patterns.md
- adr-015-wild-claim.md
- adr-039-canonical-handler-pattern.md
- adr-040-local-database-per-environment.md
- adr-043-application-layer-stored-procedures.md
- adr-044-lightweight-rbac-vs-traditional.md

**MUX Design Docs** (4):
- grammar-transformation-guide.md
- consciousness-philosophy.md
- ownership-metaphors.md
- grammar-onboarding-checklist.md

### Keywords Searched

- `anti-pattern`, `Anti-Pattern`, `antipattern`
- `❌`, `Bad:`, `Flattened`
- `avoid`, `don't do`, `mistake`

---

## Phase 2: Emergent Anti-Pattern Detection (Completed)

**Experiment Executed**: 2026-01-21

**5 Detection Strategies Used**:
1. **Negative language clustering** - "should not", "avoid", "never" proximity scoring (50% precision)
2. **Contrast pattern detection** - "instead of X, do Y" structures (38% precision)
3. **Code comment mining** - WARNING, CAUTION, HACK, XXX markers (50% precision)
4. **ADR rejected alternatives** - ❌ options in decision docs (28% precision, highest volume)
5. **Session log lessons learned** - "lesson learned", "should have", "root cause" (60% precision, **best**)

**Results**:
- Candidates scanned: ~80 passages
- TRUE EMERGENT: 14 (added to index above)
- VARIATION: 6 (related to existing)
- FALSE POSITIVE: 8
- **Overall Precision**: 63%

**Automation Recommendations**:
- Session log mining: HIGH feasibility (clear markers)
- Code comment mining: HIGH feasibility (regex patterns)
- ADR rejected sections: MEDIUM (section parsing)
- Negative language: LOW (needs ML/proximity)

See `dev/active/anti-pattern-phase2-experiment-results.md` for full analysis.

---

## Update Protocol

**Triggers**:
1. Weekly documentation audit (FLY-AUDIT) - quick refresh
2. Pattern sweep (6-week cadence) - comprehensive scan
3. After major documentation sprints

**Process**:
1. Run keyword scan against target directories
2. Compare to existing index
3. Add new anti-patterns with stable IDs (never renumber)
4. Update "Last Scan" date
5. Mark superseded patterns if any

**Next Pattern Sweep**: Feb 3, 2026 (per staggered-audit-calendar-2026.md)

---

## Coverage Gap Analysis

**Current Coverage**: 17 of 60 patterns (28.3%)

### Patterns WITH Coverage

035, 045, 046, 047, 049, 050, 051, 052, 053, 054, 055, 056, 057, 058, 059 (+ 035, 049)

### Priority Gaps (Next Sweep Focus)

| Priority | Category | Patterns | Est. Anti-Patterns |
|----------|----------|----------|-------------------|
| P1 | Core Architecture | 001-008, 014-015, 017, 034 | 10-15 |
| P2 | Data & Query | 013, 016, 023, 025, 026 | 5-8 |
| P3 | AI & Intelligence | 012, 019-020, 022, 028-029, 055-058 | 8-12 |

**Target**: 50% coverage (29 patterns) by end of Q1 2026

See `dev/active/anti-pattern-coverage-gap-analysis.md` for full breakdown.

---

## Related Documentation

- [Pattern Catalog README](patterns/README.md)
- [ADR Index](adrs/adr-index.md)
- [Grammar Transformation Guide](../../development/grammar-transformation-guide.md)
- [Consciousness Philosophy](consciousness-philosophy.md)
- [Staggered Audit Calendar](../../operations/staggered-audit-calendar-2026.md)
- Coverage Gap Analysis *(proposed; doc TBD)*

---

*Index created: 2026-01-21*
*Last updated: 2026-02-03 (Pattern Sweep - added P-11, updated coverage to 28.3%)*
*Maintainer: Documentation Management Agent*
