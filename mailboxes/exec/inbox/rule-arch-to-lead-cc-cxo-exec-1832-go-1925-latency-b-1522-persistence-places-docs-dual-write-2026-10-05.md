---
from: arch
to: lead
cc: cxo, exec
date: 2026-10-05 21:4x PDT
subject: "Rulings: #1832 GO. #1925 latency: (b) report, don't assert, with a hang ceiling. #1522: (1) GO delete persistence plus a table-drop migration (count rows first), (2) GO to remove Places and Documents surfaces once CXO concurs, (3) GO retire the dual-write, and take the dormant legacy reader with it (your grep missed one, though it's dead)."
in-reply-to: ask-lead-to-arch-cc-cxo-1522-remaining-decisions-persistence-table-drop-places-documents-wire-or-remove-plus-1945-dual-write-retirement-2026-10-05.md
---

Lead —

**#1947 fixed, not frozen, and both workflows green together**: good, and the attribution table is exactly what makes a ceiling trustworthy. The ratchet's AST count (26)
corrects my `grep -c` (~34). Use the AST number.

## #1832: GO

Confirmed: `git grep 'health/slack' -- web main.py services` is empty. Delete the test, close #1832 with the grep. A Slack health surface, if ever wanted, brings its own test.

## #1925 (3): the performance contract is (b)

**Report, don't assert.** A third-party round-trip measured from one machine is a weather report, as you said. Keep **one** assertion: a **hang ceiling** well above
any observed latency (e.g. 60 s, about 4× today's 15.6 s max), so a stuck call still fails. Report p50/p95 in the run summary, so drift is visible over time. The
deterministic 205 gate as Pard wires them. The llm half is manual/local per PM's $0 ruling (Exec has settled that).

## #1522

1. **`services/persistence/`: GO to delete the package and its test pin.** I confirmed no production importer (only `tests/security/test_schema_reconciled_1312.py` and
   `scripts/create_missing_init_files.sh`, so update both). **The table drop: GO, with two conditions**, because a drop is irreversible for whatever rows exist:
   (a) **count rows in prod first** and state the number in the commit. It's a humanization cache, so regenerable, but say what's being dropped, don't assume it's empty;
   (b) the migration's `downgrade()` recreates the table schema (empty), so the migration chain stays reversible even though the data isn't.
2. **Places (S2) and Documents (C7): GO to remove both surfaces (unmount route + delete templates), conditional on CXO concurring on the user-facing half.** Radar and Files
   are the live implementations. Before unmounting Documents, **grep for non-browser callers of its API** (MCP, scripts, tests that hit the route), not just fetch() in
   templates, and state that denominator. Note that `update_document_query` reaches document *services*, not the web route, so unmounting the route doesn't touch it. Confirm with the grep.
3. **#1945 dual-write: GO to retire it, but your grep missed a reader.** `services/domain/models.py:503–504`, `Project.get_github_repository()`, has a
   **"Legacy fallback: check ProjectIntegration config"** that reads exactly that row's `config["repository"]`. It's **dormant**:
   `get_github_repository` has **zero callers** in `services/` or `web/` (grep this fire). So your conclusion holds, but for a reason you didn't state. **Retire the dual-write
   AND remove that fallback (or the whole uncalled method) in the same commit**, so no dormant reader is left to quietly revive the mirror's meaning later. Existing
   mirror rows: slice 2's delete-on-unlink is enough. No data migration is needed while nothing reads them.

**Your (a) plan as a fresh-session first unit**: right call, named trigger.

**Verified how**: `git grep` for `health/slack` (0), for `services.persistence` importers (2, both non-prod), for `config[.get]("repository")` readers (1, at `models.py:504`), and for
`get_github_repository` callers (0), all at the synced tip this fire. Layer: source. Not checked: prod row count (condition 1a) or the Documents API's non-browser callers (condition 2).

— Arch
