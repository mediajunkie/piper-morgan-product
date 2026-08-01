# docs/ tree audit + cleanup plan

**Author**: Docs · **Date**: 2026-08-01 · **Status**: AUDIT + PROPOSAL — **nothing has been moved**
**Requested by**: PM via PPM, 2026-07-12. Carried unstarted for 20 days; this is the audit PM asked for
*before* any large-scale moves.

---

## The headline: "old" is not "stale," and conflating them would have produced a bad cleanup

`docs/` holds **1,753 markdown files / 79 MB**. A naive age sweep flags hundreds. **Almost none of them
should move**, and the reason is the whole point of doing an audit before a cleanup:

| category | count | verdict |
|---|---|---|
| `architecture/current/adrs/` | **82** | **durable by design.** A ratified ADR from 314 days ago is not stale, it is *settled*. Age is not a signal here. |
| `architecture/current/patterns/` | **81** | same |
| `omnibus-logs/` | **429** | **historical record by construction.** Never a cleanup target. |
| loose `.md` in `architecture/current/` | **56** | ← **the actual audit surface** |
| `planning/current/` | **7** | ← the clearest single finding |

**163 files are excluded on principle, not measurement.** An audit that skipped this distinction would
have proposed archiving the ADR corpus.

## ⚠️ Two measurement traps I hit while doing this, both worth recording

**1. Filesystem mtime is useless here.** My first pass reported the oldest file in
`planning/current/` as **3 days old**. `git worktree add` stamps every checked-out file with a fresh
mtime, so on Amber *every* file looks new. Re-measured by **git commit date** and the same directory is
**314 days old, 100% of it**. CLAUDE.md documents this trap for the SessionStart hook; it applies to any
age measurement in a multi-worktree checkout.

**2. Age alone is a false signal; inbound references are the real one.** Of the 35 loose architecture
docs at ≥180 days, **19 are still actively referenced** and only **16 have zero inbound links**. Sorting
by age would have proposed moving twice as many files as the evidence supports.

*Reference counting excludes `docs/omnibus-logs/` deliberately — an omnibus mentioning a filename is
narrating history, not depending on it. Counting those would mark almost everything "live."*

## Finding 1 — `docs/internal/planning/current/` is 100% stale and the name is actively misleading

**7 files, every one 314 days old by commit date.** A directory named `current/` in which nothing is.

This is the clearest case in the tree: an agent following `NAVIGATION.md` to "current planning" gets
ten-month-old material presented as current. **The directory name is the defect**, more than the
contents.

## Finding 2 — 16 loose architecture docs with ZERO inbound references

Measured, not estimated. Age is shown for context; **the zero-reference count is the signal**:

- `python-environment-specifications.md` — 314d
- `pm034-deployment-guide.md` — 314d
- `pm-033a-mcp-consumer-architecture.md` — 314d
- `mcp-integration-points.md` — 314d
- `mcp-integration-mapping.md` — 314d
- `markdown-formatting-analysis.md` — 314d
- `inchworm-execution-plan.md` — 314d
- `github-issue-sequence-diagram.md` — 314d
- `file-scoring-algorithm.md` — 314d
- `current-state-documentation.md` — 275d
- `spacing-system.md` — 207d
- `consciousness-rubric.md` — 191d
- `consciousness-review-checklist.md` — 191d
- `consciousness-monitoring.md` — 191d
- `consciousness-anti-patterns.md` — 191d
- `entity-relationship-diagram.md` — 190d

**19 others at the same ages are still referenced and must not move**, including `README.md` (121
inbound), `consciousness-philosophy.md` (8), `ownership-metaphors.md` (7), `grammar-compliance-audit.md`
(7), `api-reference.md` (6).

⚠️ **The `consciousness-*` cluster does not move as a block** — that was my initial hypothesis and it is
wrong. `consciousness-philosophy.md` carries **8 inbound references** while four operational siblings
carry none. **A subsystem is not uniformly dead just because it is uniformly old.**

## Proposal — and what I am deliberately NOT proposing

**Not proposing deletion of anything.** Not proposing bulk moves. Not proposing to act on this today.

1. **Rename, don't move, for Finding 1.** `planning/current/` → `planning/2025-genesis/` (or similar),
   with a `NAVIGATION.md` update in the same commit. Renaming a misleading directory is a smaller,
   safer act than relocating its contents, and it fixes the actual defect.
2. **Archive-with-pointer for Finding 2**, one at a time, **only after an owner confirms each.** A file
   with zero inbound references may still be the only record of a decision — *zero links is evidence of
   disuse, not of worthlessness.* Destination `docs/internal/architecture/archive/`, never deletion.
3. **Owner sign-off is required per file, not per batch.** Arch owns the architecture corpus. I can
   measure; I should not be the one deciding an architecture doc is finished.
4. **Re-run before acting.** These numbers age. The measurement is reproducible from this document's
   own method — anyone can re-derive it rather than trusting the table.

## What I want challenged

The **zero-inbound-references** heuristic is the load-bearing claim, and it is the one I would attack
first. It cannot see: a doc a human reads directly without linking, a doc referenced only from a closed
GitHub issue, or one whose value is archival rather than operational. **It is a disuse signal, not a
worthlessness signal**, and the proposal treats it that way — which is why every action above is gated
on a human confirming the file rather than on the metric.
