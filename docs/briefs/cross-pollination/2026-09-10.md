
# Cross-Pollination Brief — September 10, 2026

Two enforcement patterns surfaced in yesterday's work: Klatch found that validating *known* flag values is not the same as rejecting *unknown* flags — and paid for it in a live operation. Piper Morgan independently solved the "invisible third copy" problem by making the test read the source code itself.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Validating known CLI flags is not the same as rejecting unrecognized ones — and for destructive operations, the difference is the whole protection

**From:** Klatch (Rounds 180–181, Daedalus + Theseus)  
**Relevant to:** Any project with a CLI for irreversible or scoped operations

Klatch's entity backfill CLI validated that `--channels` received a valid value when present. But when a user misspelled it — `--channel=`, `--chanels=`, `--Channels=`, `-channels=` — the parser returned `undefined`, the filter was silently treated as absent, and the CLI applied the operation to the full corpus at exit 0. In a live probe: 4 of 8 in-scope channels moved where 1 was approved, with no indication anything had gone wrong.

Round 180 tightened empty-value rejection. Round 181 found the deeper structural gap: the parser can't protect against what it doesn't know to reject. The fix is one rule at the parse boundary — reject any flag in `argv` that isn't in the recognized set, before any validation of flag values. One rule, not one guard per flag.

The companion user-facing signal: the CLI now emits a `Candidates:` line that names the `--channels` filter when the filter took (`Candidates: 2 of 8 in scope`) and a bare count when it didn't (`Candidates: 8`). Reading that line before `--apply` is a check that survives every spelling and spacing variant — it's not dependent on the error path being right, only on the success path being honest about what it matched.

**Suggested action:** For any CLI that gates a destructive or scope-limited operation behind flags, confirm the parser rejects unrecognized flags explicitly — not only that it validates the values of recognized ones. And if there's a filter that narrows scope, make the "filter took" state visible in normal output, not only in an error message the user only reads when something goes wrong.

---

### 2. An AST-parsing test can make hand-maintained copies of a registry test-visible — for when you can't centralize, only enforce

**From:** Piper Morgan (Lead Dev + CXO, #1717 registry refactor)  
**Relevant to:** Klatch and any codebase where a data structure necessarily appears in multiple code locations

Piper Morgan's floor renderer had a list of "source-failed" flags that appeared in three places: the render sites (topically placed in their sections, which is structurally correct — you can't move them without breaking the format), a gating tuple, and the test's own dictionary. A new flag added to the render sites but missed in the gate would render a `FAILED` line and escape the scope directive check — exactly the report-failures-that-didn't-happen leak the gating exists to prevent. Two of the three copies were hand-maintained with no test link between them.

The fix: `SOURCE_FAILED_FLAGS` is now a single ordered tuple at module level. The gate iterates it. The test derives its own dictionary and denominators from it. The render sites stay hand-placed (topical placement is required), but a new test (`test_source_failed_registry_1717.py`) parses the renderer's source using Python's `ast` module and fails if any `domain_context.get("*source_failed")` key-set or order diverges from the registry — banning any reborn literal tuple and pinning the prefix convention the denominators depend on. A drift probe verified red-then-green: an injected unregistered sixth site fails the derivation test; removed, all green.

This is distinct from Protocol typing (reported here on September 7): Protocol typing surfaces dead code paths at compile time. The AST-registry approach handles the complementary case — when the data *must* appear in multiple places (centralization would break the format), but all appearances must be *consistent*. The test becomes the consistency constraint, and it runs from source, not from imports.

**Suggested action:** Klatch's backfill CLI has a structurally similar property — flag validation is distributed across a few sites. When the same data (a flag list, an enum, a set of recognized values) reappears in rendering, gating, and testing, consider whether a registry + an AST-level test could make divergence structurally impossible before an error path catches it downstream.

## Sources Read

- `docs/logs/2026-09-09-calliope-log.md` (Klatch) — narrative rollup of Rounds 175–181; backfill CLI fixes
- `docs/research/round181-unrecognised-flags-and-the-undo-record-validator-2026-09-09.md` (Klatch) — Round 181 probe findings
- `git log origin/main --since="48 hours ago"` (Piper Morgan) — commit scan, ~130 commits
- commit `3215e64e5` (Piper Morgan) — registry + AST derivation refactor commit message and diff summary
- `src/internal/briefs/2026-09-07-brief.md`, `2026-09-08-brief.md`, `2026-09-09-brief.md` (hub) — anti-zombie orientation

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
