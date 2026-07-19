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
- **v1.0** (2026-07-19, Lead Dev): Created from #1436 Tier-3 Families 1–3
  execution lessons, per the 7/18 memory-eval gap ("worth codifying if
  Tier-3-scale deletion recurs" — it recurred the next morning).
