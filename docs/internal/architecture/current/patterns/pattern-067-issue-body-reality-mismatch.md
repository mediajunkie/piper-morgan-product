# Pattern-067: Issue-Body Reality Mismatch

## Status

**Emerging** — Identified 2026-05-09 by Lead Developer during M2f Group A+B audit-cascade work (3 of 5 issues encountered the pattern in a single session). Filed under Lead Dev self-approval authority 2026-05-09 per recent precedent (CIO Pattern-066 filed under self-approval same day). Promotion to Proven pending one trial-application cycle on a future issue triage where the Phase 0 dead-code check is applied prophylactically.

## Product Relevance

**Portable** — Any project with an issue tracker, technical-debt backlog, and codebase that evolves between issue-filing and issue-pickup. Particularly load-bearing in:
- Codebases with high-velocity refactoring (issues filed weeks/months ago may describe code that has since been fixed, deleted, or restructured)
- Audit/cleanup sprints where TODO triage produces issues asserting "X needs Y" without re-verifying that X still exists in the form described
- Multi-agent workflows where a different agent files the issue than picks it up, and time elapses between
- Backlog grooming after major architectural changes (e.g., post-floor-migration, post-#971 adapter deletion) where prior assumptions about wiring may no longer hold

## Context

When an issue is filed, its body captures the author's understanding of what's broken at filing time. If the codebase evolves between filing and pickup, the body's framing can drift from reality:

- Code described as "needs persistence" may have been deleted (zero callsites)
- Code described as "wired but missing X" may have been re-routed (the wiring has moved)
- Code described as "in-memory only, lost on restart" may have INSERT SQL the body doesn't acknowledge — but the call chain reaching that INSERT may be unreachable due to a guard the body doesn't mention
- Bug fixes that closed the original cause may have left the workaround flag/bypass in place; the body still describes the workaround as needed

This pattern is **distinct from but related to**:

- **Pattern-049 (Audit Cascade)** — investigation methodology with phased gates. Pattern-067 is the specific failure mode that makes Audit Cascade's Phase 0 (Investigation) load-bearing rather than ceremonial.
- **Pattern-046 (Beads Completion Discipline)** — closing issues with evidence. Pattern-067 is upstream: even before closure, scoping must verify the body's premise, not just enumerate the body's checkboxes.
- **Pattern-045 (Green Tests, Red User)** — tests pass but user fails. Pattern-067 is "issue passes filing-time validity checks but reality has moved." Both are "the artifact says X is true; reality says otherwise."

## Problem

### The failure mode

The audit-cascade discipline (Pattern-049) says: **issue-audit before gameplan, gameplan-audit before prompts, prompts-audit before execution.** But the issue-audit step is often performed against the issue's *body* as the source of truth — auditor reads the body, checks it against the feature template, surfaces missing fields, asks PM to fill in gaps.

This treats the body as authoritative on "what is currently true in the codebase." But the body was written at a moment in time and may no longer be accurate. Auditing the body against a template doesn't catch body-vs-reality drift; it only catches body-vs-template drift.

Result: the gameplan inherits the body's incorrect premise. Implementation proceeds against a phantom problem (e.g., "wire UserService to DB") when the actual problem is different (e.g., "delete UserService — it's wired in but never populated"). Hours of work can go in the wrong direction before the mismatch surfaces — typically when tests start passing in unexpected ways, or a callsite grep returns zero results.

### Trigger conditions

Particularly likely when the issue body contains any of:
- "TODO to enable X" / "currently disabled for Y" / "stub returns Z"
- "All data lost on restart" / "no persistence" / "in-memory only"
- "Stores all X in Y dicts" / "needs database backing"
- References to specific line numbers that have since shifted (TODO triage from N months ago)
- Acceptance criteria that say "OR explicitly documented as [alternative pattern]" — that parenthetical is often the right path, but the body's framing biases toward the migration option

The **acceptance-criteria parenthetical** is often the audit-cascade's smoking gun: it's there because the original author considered the alternative was real but didn't have time to investigate. Phase 0 should treat the parenthetical as a candidate disposition, not an afterthought.

## Evidence

**M2f Group A+B audit-cascade, 2026-05-09** — 3 of 5 issues exhibited this pattern in a single Lead Dev session:

| Issue | Body's framing | Reality | Disposition |
|---|---|---|---|
| **#933** SEC: API key validation disabled | "Validation should be re-enabled before beta" | Original cause (format-validator issues) was fixed Oct 30 2025 in commit `214f4afe`; bypass remained in place 6+ months after cause was gone | Flag flip + un-broke 5 existing tests that asserted validation works |
| **#936** TECH-DEBT: UserService in-memory dicts | "All user session data lost on restart. Multi-tenancy isolation depends on in-memory state." | UserService.create_session() and create_user() had ZERO production callsites. Wired into AuthMiddleware but `_sessions` was always empty; isolation comes from JWT claims, not the dicts | Delete (Option A); −435 LOC |
| **#935** TECH-DEBT: BudgetManager + APIUsageTracker no DB persistence | "All data is in-memory only and lost on server restart. Users have no historical usage visibility." | BudgetManager: zero callers (dead). APIUsageTracker: real INSERT SQL into `api_usage_logs` table, but call chain unreachable because callers don't pass a session. Table existed in postgres with 0 rows | Delete (Option A); −1378 LOC; #1029 superseded |

**Each issue's body's premise was wrong**. Each took the audit-cascade Phase 0 investigation step ~30-60 min to expose. Each saved 6-12+ hours of misdirected implementation work that would have shipped a feature against a phantom problem.

**Aggregated impact** of Phase 0 catching these:
- ~−2229 LOC removed instead of multi-thousand-LOC additions for migration scaffolding
- 3 issues closed via deletion (cheaper, cleaner) instead of 3 multi-day migrations
- 1 cohort issue (#1029) auto-superseded as a side effect
- Methodology pattern surfaced (this entry) as load-bearing learning

## Mechanism

The pattern operates through **temporal asymmetry**:

1. Issue is filed at time T₀ with body describing state as the author understood it
2. Codebase evolves between T₀ and T₁ (pickup time): refactors, deletions, wiring changes, dependency upgrades
3. At T₁, audit-cascade Phase 0 normally happens, BUT the audit checks body-against-template (does it have all required fields?) rather than body-against-current-reality
4. Body's premise propagates into gameplan, prompts, implementation
5. Failure surfaces during implementation when reality contradicts the premise (e.g., a grep for the supposed-callsites returns zero, tests for the supposed-broken-feature pass, etc.)

The longer the gap T₁ - T₀, the higher the probability of drift. M2f Group A+B's body-vs-reality mismatches all came from issues filed in the **March 24 weekly docs audit TODO triage** — 6+ weeks before pickup. In a high-velocity codebase, that's enough time for substantial wiring changes.

## Counter-pattern (the discipline)

**Phase 0 dead-code/unreachable check, applied prophylactically to issue bodies that match trigger conditions:**

1. When the body says "X needs persistence/migration/wiring," **grep for X's callsites** as the very first investigation step. Zero callsites = dead code; investigate further.
2. When the body says "TODO to enable Y," **find when Y was originally disabled** (git blame on the bypass site). Check if the original cause has since been fixed. If yes, the bypass may be the only thing left.
3. When the body cites a specific line number, **verify the line still contains the described code** (line numbers drift; the issue may now describe entirely different code).
4. When the acceptance criteria has a parenthetical alternative ("OR documented as gateway pattern"), **treat that as a candidate disposition equal in weight to the migration framing**, not a fallback.
5. When the body's premise survives the above, proceed with confidence to gameplan. When the body fails, surface the body-vs-reality finding to PM with three options (delete / wire / defer-and-document) before any implementation.

The check is fast (~15-30 min Phase 0 work) and cheap relative to the cost of misdirected migration work (often 4-12+ hours per issue).

## Related Patterns

- **Pattern-049: Audit Cascade** — Phase 0's investigation step is where this pattern is caught. P-049 enables P-067 to be caught reliably; P-067 explains why P-049's Phase 0 must be load-bearing.
- **Pattern-046: Beads Completion Discipline** — closing with evidence; P-067 catches mismatched-premise issues *before* closure, P-046 catches incomplete closure *at* closure.
- **Pattern-045: Green Tests, Red User** — both involve artifact-vs-reality drift; P-045 is single-layer (test artifact), P-067 is documentation-layer (issue artifact).
- **Pattern-062: Assembly Assumption** — composition failure between components; P-067 can be a special case where the assumed-but-missing component never actually existed.

## See Also

- `dev/2026/05/09/933-issue-audit.md` — first appearance in audit-cascade artifact form
- `dev/2026/05/09/936-issue-audit.md` — second appearance
- `dev/2026/05/09/935-issue-audit.md` — third appearance + cohort-impact analysis (superseded #1029)
- M2f Group A+B closure session log — `dev/2026/05/09/2026-05-09-0630-lead-code-opus-log.md`
- PM disposition framing 2026-05-09 12:56 — *"we should avoid overbuilding or pre-building on things like this"*

## Pattern History

- **2026-05-09 ~19:50**: Filed Emerging by Lead Developer under self-approval authority, after the third occurrence in a single session made the pattern legible. Awaiting PM concurrence on slot allocation (067) and one trial-application cycle for promotion to Proven.

---

*Pattern-067 author: Lead Developer (Code, Opus); 2026-05-09*
*Cross-references: Pattern-049 (Audit Cascade), Pattern-045 (Green Tests Red User), Pattern-046 (Beads Completion), Pattern-062 (Assembly Assumption)*
