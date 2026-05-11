# Pattern-067: Silent State Mutation in Shared Working Tree

## Status

**Emerging** — Filed 2026-05-11 by CIO under self-approval authority per `methodology-audit-policy-updates-2026-03-16.md`, with PM ratification on the same-day directive ("we need to solve these issues to avoid a real problem occurring or loss of valuable effort"). Parent meta-pattern surfaced by Code agent's May 10 staging-race memo + HOST May 10 concurrence on shelf-placement. Subsumes three named children already in anti-pattern index (P-13 branch-drift, P-15 branch-collision, P-16 candidate Cross-Agent Residue Accumulation) plus a fourth child surfaced May 10–11 (worktree-vs-main physical-tree-fragmentation). Promotion to Proven contingent on naming holding through ~2 more sub-instance recurrences across the named children OR a single new-shape instance fitting the parent (e.g., lockfile drift, ephemeral-state drift).

## Product Relevance

**Process-only** — Multi-agent coordination discipline. Piper's users will not encounter this; teams running multi-agent workflows in shared git environments will.

## Context

When multiple agents operate against a shared git working tree (one filesystem, one `.git/` directory, possibly multiple worktrees but the same underlying repo), "stable-looking" pieces of state — the current branch, the staging index, the working-tree-vs-checkout-path correspondence, the residue of unstaged changes — can be silently mutated by another agent's concurrent operations. Subsequent operations that depend on that state fail mysteriously, succeed incorrectly, or strand work in an unexpected place.

Three forces converge: shared `.git/` (necessary for git's correctness model), concurrent agent activity (the operating tempo of multi-agent coordination), and asymmetric visibility (each agent's mental model of the tree is local to its own session). The collision surface is real, and existing disciplines that verify *named states* (branch identity, file paths, role identity) don't reliably catch *transient states* (index, lockfiles, physical-tree-path correspondence).

### Relationship to children

| Child | Failure shape | First named |
|---|---|---|
| P-13 (anti-pattern: branch-drift) | Subagent's `git checkout` flips HEAD on parent agent's session via shared `.git`; chained commit lands on wrong branch | Lead Dev May 7 (#1053 subagent collision) |
| P-15 (anti-pattern: branch-collision) | Two agents on same physical checkout, one needs feature branch, HEAD flip surprises the other | Lead Dev Apr 22 (#992 ETHICS-ACTIVATE branch + concurrent Docs session) |
| P-16 (candidate: cross-agent residue accumulation) | Multiple agents' partial work accumulates in working tree because no single agent has standing to commit others' files under "commit only your own" discipline | Code agent May 10 (PreCompact-hook first-use debrief) |
| **New: physical-tree fragmentation** | Worktree path and main-checkout path have separate physical copies of the "same" file; edits in one are invisible to git operations in the other | CIO May 10–11 (innovation-backlog edits stranded overnight) |

The common shape across all four: shared coordination resource (HEAD, index, working tree, file content) + concurrent agent activity → silent mutation of stable-looking state → downstream operation fails or succeeds incorrectly.

## Problem

### The Failure Mode

```
Agent A: reads state S (branch, index, file content, or path mapping)
         operates based on S
         expects S to be stable through its work unit

Agent B (concurrent or sub-): mutates S via its own normal operations
                              (checkout, add, edit at different path)
                              git treats this as correct — no error

Agent A: continues based on stale S
         operation succeeds-incorrectly or fails with cryptic error
         the original cause (B's mutation) is invisible at A's altitude
```

Each agent's individual git operations are correct. The collision is at the *composition* layer — git's correctness model assumes one author per working tree at a time; multi-agent coordination violates that assumption by design.

### Why It Happens

1. **Shared `.git/` is by-design.** Worktrees, multi-session agents, and parallel CLI invocations all share `.git/` because that's git's coordination layer. Splitting `.git/` would lose the cross-tree consistency the model relies on.
2. **Existing disciplines verify named states, not transient ones.** "Verify branch before commit" (May 9 memory pin) catches HEAD drift but not index drift. Sign-off discipline catches end-of-session strand but not mid-session physical-tree-path divergence. The disciplines are at the right altitude for *known* drift modes; new drift modes surface faster than discipline accumulates.
3. **Failure mode varies per child.** Branch-drift fails at commit time with "nothing added"; index-drift fails at commit time with the same error but different root cause; residue-drift fails at sign-off with "files I didn't write"; fragmentation fails silently across sessions with "edits I made aren't there." The same parent mechanism produces non-overlapping failure signatures, which is why naming the parent matters for cohort vocabulary.

### Concrete Examples

**Branch-drift (May 7, Lead Dev #1053 subagent).** Subagent's `git checkout claude/1053-...` flipped HEAD on Lead Dev's session via shared `.git`. Chained `git branch --show-current && git add ... && git commit ...` printed wrong branch but ran anyway (the `&&` chain doesn't gate on the verify output, only on its exit code). Log-update commit `fc7f685e` landed on feature branch instead of main. Recovery: leave on feature branch; came across at `--no-ff` merge. Memory entry refined same session.

**Index-drift (May 10, PPM stranded commits).** Code agent (special assignment) staging PPM's files; `git add` succeeded; HOST's concurrent session was writing to a session log in the same tree; index silently cleared between add and commit. Commit failed with `nothing added to commit, untracked files present` despite verbose-add output proving the add happened. Recovery: switched parallel tool calls to sequential `git add && git status --short` shell chain.

**Residue-drift (May 10, PreCompact-hook first-use).** Six MANIFEST modifications accumulated in working tree from multiple agents' partial sessions; no single agent had standing to commit others' files under "commit only your own" discipline. PreCompact hook (the detector) correctly fired on Docs's session; cross-agent committing under PM authority resolved (commit `7505068d`).

**Fragmentation (May 10–11, CIO innovation-backlog).** Edits made to `dev/active/cio-innovation-backlog.md` via the main checkout's path; the worktree branch's physical copy of the same logical file lived at a different absolute path. `git status` from the worktree showed clean; `git status` from main showed modified. Edits sat uncommitted overnight until the next session noticed via cross-tree diff. Cost: low this time (one file, one session-gap, caught next morning); high in plausible variants where the stranded edits compound or get overwritten.

## Solution

### At the methodology layer

**1. Name the parent for cohort vocabulary.** When an agent hits a silent-state-mutation incident, the diagnostic question is *"which transient state got mutated under me?"* — the four named children (branch / index / residue / fragmentation) give the cohort a shared shelf for that conversation. Without the parent, each child gets re-discovered independently.

**2. Verify transient states at work-cycle boundaries.** Mid-session checkpoints — not just at commit time — for branch identity, index contents, and working-tree-vs-context correspondence. Convention not norm (per HOST May 10 stance); the cost of verifying every operation is disproportionate.

**3. Accept residual risk + retry-with-recovery.** Per HOST: shared-main is by-design for visibility; the race surface is the cost we accepted. The error signatures are loud and the recovery paths are mechanical. Codifying tree-locking or transient-state PreCommit hooks would erode the cost-benefit math.

### At the tooling layer

**1. Worktree-path consistency convention** (new, per the fragmentation child). When operating from a worktree, all file paths should be relative to or anchored in that worktree's root. Cross-tree file access (worktree session editing files at the main-checkout's absolute path) is the fragmentation antipattern; either operate from one root consistently, or commit between path changes.

**2. Possible Lead-Dev shell wrapper or hook** (open question). A pre-commit or pre-edit detector could warn when the agent is editing files outside its current working directory's git tree. Cost-benefit unevaluated; routed to Lead Dev for assessment.

**3. More aggressive worktree adoption.** CLAUDE.md already names worktrees as the default for feature-branch work; uptake remains uneven. The per-incident retro consistently finds that worktree-per-session would have avoided the collision. Worth treating as cohort-discipline rather than per-agent technique.

## Anti-Pattern Indicators

The following signals suggest Pattern-067 may be present:

- **An operation that should have worked (based on the output of the immediately-preceding step) didn't, and the error message points at state that "shouldn't" have changed.**
- **Edits made in one session are invisible to git operations in another, even though both appear to be in the same repository.**
- **`git status` from different paths in the same repo show different results for the "same" file.**
- **Recovery requires re-running an operation that previously printed success.**
- **The agent's mental model of working-tree state diverges from `git status`'s.**

## Cross-References

- **Anti-pattern P-13 (Commit-Attribution Drift)**: child instance — branch-level mutation
- **Anti-pattern P-15 (Branch-Collision)**: child instance — checkout-time HEAD flip
- **Anti-pattern P-16 candidate (Cross-Agent Residue Accumulation)**: child instance — working-tree residue
- **Pattern-066 (Stacked Silent Failures)**: adjacent — Pattern-067 is a specific class of stacked-silent-failure at the coordination layer where each child's silent mutation enables the next-step's silent error
- **Methodology-24 (Branch-or-Anchor)**: discipline that prevents one class of P-067 instance (parallel-authoring drift, the P-063 cousin)
- **`docs/internal/operations/branch-worktree-mailbox-discipline.md`**: canonical operational doc; Pattern-067 names the failure mode the discipline anticipates

## References

- Code agent May 10 PreCompact-hook first-use debrief (`mailboxes/cio/read/memo-code-to-docs-cc-cio-host-pa-precompact-hook-first-use-debrief-2026-05-10.md`): residue-drift child first-named
- Code agent May 10 staging-race memo (`mailboxes/cio/read/memo-code-to-docs-cc-cio-host-pa-shared-working-tree-staging-race-2026-05-10.md`): index-drift child + parent meta-pattern proposed; explicit §CIO routing
- HOST May 10 tolerated-risk-stance memo (`mailboxes/cio/read/memo-host-to-docs-staging-race-tolerated-risk-stance-2026-05-10.md`): "Silent State Mutation in Shared Working Tree" parent shelf concurrence
- CIO May 10 disposition memo (`mailboxes/cio/sent/memo-cio-to-code-host-docs-cc-pa-ceo-pattern-candidates-disposition-2026-05-10.md`): Innovation Backlog Operational #44 capture
- May 7 Lead Dev branch-drift incident (`docs/omnibus-logs/2026-05-07-omnibus-log.md` Phase 1): first-named branch-drift child instance
- May 10–11 CIO innovation-backlog fragmentation (this session): fourth child instance, caught at session resume

---

*Formalized: 2026-05-11 by CIO. PM ratification on May 11 same-day directive. Promotion to Proven contingent on naming holding through next ~2 sub-instance recurrences.*
