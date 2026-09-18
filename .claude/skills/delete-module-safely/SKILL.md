---
name: delete-module-safely
description: Delete a dead/fabricated module (or module family) without stranding importers, tests, CI jobs, or docs. Use for any fix-or-delete execution, Tier-3-style dead-code removal, or retiring a superseded subsystem. Encodes the Finish-the-Unfinished sprint's deletion lessons (Families 1-3, 2026-07-18/19).
scope: cross-role (Lead/Arch lanes primarily)
version: 1.0
created: 2026-07-19
updated: 2026-07-19
---

# delete-module-safely

Deletion is fabrication-removal, not tidying: a dead module that LOOKS live
(imported, tested, CI-enforced) manufactures false confidence. This skill makes
the removal itself trustworthy. Born from three executed deletion families
(#1436 Tier-3, 2026-07-18/19) whose lessons repeated verbatim across days —
and from the near-misses each one caught.

## Rule 0 — ruling before cutting
A module not already ruled deletable by Arch (or PM) gets a proposal memo with
FRESH caller evidence first. Protected representations (spatial intelligence)
are NEVER deleted without the PM-directed review completing, regardless of
coldness. When a sweep surprises you mid-execution (an unruled orphan appears),
flag it in the execution memo — precedent: riders whose sole purpose is the
deleted thing may ride, but say so explicitly.

## The sweep (before EVERY cut) — enumerate the whole space
A sweep blind to part of its space gives false confidence (the blind-sweep
class, 6 instances named by Arch). For module `pkg.mod`:

1. **Both import styles** — absolute AND relative:
   `from pkg.mod import` · `from pkg import mod` · `import pkg.mod` ·
   `from .mod import` · `from ..sub.mod import`
   (Family-1 near-miss: absolute-only grep missed a live RELATIVE importer;
   caught only by test collection.)
2. **Init re-exports** — `pkg/__init__.py` re-exporting the module's classes
   creates a second import path (`from pkg import ClassName`); sweep the CLASS
   names from the package, not just the module name.
3. **Precise patterns** — an over-broad regex INVENTS importers (the inverse
   blind spot: a `from \.$mod` pattern matched other packages' relatives and
   nearly kept a dead module alive). Anchor patterns to the real package path.
4. **Function-local imports** — module-level grep misses `import` statements
   inside functions (two dead scripts survived a Family-2 sweep this way).
   Sweep the module NAME repo-wide, then classify each hit.
5. **Non-code referents** — CI workflows (a deleted directory was still a
   `--cov` target and an inline-python import in test.yml), scripts/, docs
   that describe the module as live, config files listing its paths.
6. **ALL python roots, not just services/+web/+tests/** — sweep `cli/`,
   `coordination/`, `rag/`, `shared/`, `skunkworks/`, `suggestions/`,
   `tools/`, `alembic/`, `scripts/` too. `cli/` is pytest-invisible
   (testpaths=tests) and was outside the 2026-08 census denominator; it held
   a live importer of a Batch-3 target AND a broken import of a Batch-1
   deletion that nothing surfaced for a day (#1700, 2026-08-30). A root no
   collector touches is exactly where a stranded importer hides silently.
   And don't `| head`-truncate sweep output — truncation hid two dedicated
   test files in the same batch; use `grep -rl` file-level output instead.

## Deleting a WRITE, not a module — enumerate the slot's READERS first
*(Added v1.1, 2026-09-18, Arch — from #1810/#1814, and it is MY ordering error being
codified, not a lane's.)*

The sweep above is **module-shaped**: it enumerates importers of a thing that is
going away. **A write-deletion is the sibling case and the sweep above cannot see
it** — the module stays, the slot stays, only the *producer* goes. Nobody greps for
"who reads this slot," so nothing fails.

**The rule: before deleting a write, enumerate every reader of that slot and NAME
each one's post-deletion source.** Not "the readers still resolve whatever is
there" — true, and worthless the moment the slot empties. An actual list:
reader → where it gets the value once this write is gone.

**The worked case**: #1810 deleted a global LLM-key write (a real cross-user
credential leak — the right call). The readers were left pointing at the
now-permanently-empty slot, so a BYOC user's key was stored and never read: every
substantive query hit a false "not configured" wall (#1814). **A billing leak was
converted into a functionality wall, and it landed the day an external tester's
invite was ready.** The ruling that ordered the deletion had the reader/writer
picture in front of it and gated only the write.

**Two tells that you are in this case and not the module case**:
- the thing you are deleting is a *statement*, not a file;
- the grep that would reassure you ("who imports this?") returns the same answer
  before and after your change.

**And the reader enumeration is evidence, not narration** — it goes in the ruling
or the issue, with each source named, so a reviewer can check it. If a reader has
no post-deletion source, that is a precondition to fix first, not a follow-on to
file.

## The cut
- `git rm` explicit paths only. Family tests (dedicated test files) ride the
  same commit; live-subject test files get SURGERY (excise the coupled
  fixtures/tests, keep the file) — read the file's structure first, never
  wholesale-delete a mixed file.
- Package `__init__` edits preserve surviving exports.
- Stale docstrings/comments in SURVIVING files that name the deleted module
  get corrected in the same commit (a doc claiming a deleted reader is live
  is a small fabrication).

## Verify AFTER each excision (not just at the end)
- py_compile every edited file (a dangling kwarg from an incomplete
  old-string is a real occurrence).
- Full test COLLECTION (`--collect-only`) — collection catches live importers
  the sweep missed.
- Run the surgered test files.
- **Full ratchet suite after every delete batch** — deleted modules carry debt
  instances (TODO markers, silent-death sites, mypy errors); shrink-locks fire
  and ceilings lower in the SAME commit. Selective re-runs missed drops twice.
- If CI enforces anything about the deleted paths (coverage targets, perf
  baselines, import-based jobs), fix the workflow in the SAME push or CI goes
  red at the tip.

## The record
- decisions.log entry: WHAT IT EXISTED FOR (one line of history), the ruling
  reference, the evidence (importer sweep result, collection count), and any
  supersessions (an issue obviated by deletion closes as superseded with the
  paper trail — description-first per close-issue-properly).
- Preserve genuinely-novel design thinking as a design-record doc BEFORE
  deleting (PM-033d precedent) — git history holds code; it doesn't surface
  ideas.

## Anti-patterns
| Don't | Because |
|---|---|
| Absolute-only import grep | Relative importers stay live and break at runtime/collection |
| Trust "N importers" from a loose regex | Over-broad patterns invent importers; under-broad hide them |
| Delete a mixed test file for one dead class | You just deleted live coverage |
| Skip the ratchet suite "because it's a delete" | Deletes SHRINK counts; unlocked ceilings fail the next run |
| Leave CI enforcing the deleted thing | A gate about deleted code is a false-gate — worse than none |
| Batch the decisions.log entry "for later" | The record rides the commit or it doesn't exist |

## Changelog
- **v1.1** (2026-09-18, Arch): Added the write-deletion case (enumerate the
  slot's READERS with each one's post-deletion source named). The module-shaped
  sweep is structurally blind to it. Source: #1810 → #1814, an ordering error in
  my own ruling — a credential leak correctly closed, converted into a
  functionality wall because only the write was gated.
- **v1.0** (2026-07-19, Lead Dev): Created from #1436 Tier-3 Families 1–3
  execution lessons, per the 7/18 memory-eval gap ("worth codifying if
  Tier-3-scale deletion recurs" — it recurred the next morning).
