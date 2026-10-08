# Session log: prog-code-1522-persistence

**Role**: Coding Agent (prog)
**Model**: claude-sonnet-5 (observed via system-reminder)
**Started**: 2026-10-07 18:31 PDT
**Task**: GitHub #1522 — delete `services/persistence/` + test pin, add table-drop migration for `action_humanizations`, per Architect GO (2026-10-05).

## Context read
- `mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-1832-go-1925-latency-b-1522-persistence-places-docs-dual-write-2026-10-05.md` — Arch's ruling section 1: GO to delete `services/persistence/` + test pin; table drop GO with two conditions: (a) count prod rows first, state in commit; (b) downgrade() recreates empty table schema.
- `mailboxes/lead/read/answer-exec-to-lead-production-db-counts-from-pm-humanizations-is-zero-users-7-setup-complete-5-2026-10-07.md` — production `action_humanizations = 0`, from PM's psql query on piper-morgan-db ~16:3x PT 2026-10-07, relayed by Exec.

## Plan
1. Caller grep for persistence/action_humanization references (production code).
2. Delete `services/persistence/` (4 files).
3. Update test pin in `tests/security/test_schema_reconciled_1312.py` and `scripts/create_missing_init_files.sh`.
4. Check `alembic/env.py` comment near line 7.
5. New alembic migration: drop `action_humanizations`, with reversible downgrade (timestamptz columns per d73b3722eb03).
6. Verify round-trip on local Postgres (port 5433).
7. Run test suites.
8. ruff format/check.
9. Commit.

## Work log

1. **Caller grep (before deletion)**: `services/persistence` referenced in `alembic/env.py` (import + comment), `scripts/create_missing_init_files.sh` (init-file list), `services/persistence/*` itself, `tests/security/test_schema_reconciled_1312.py` (mirror import). `action_humanization` also in two historical alembic migration files (8ef0aa7cbc90, d73b3722eb03) and one merge-heads migration (3659cb18c317) — left untouched, per Arch's rule not to edit migration history.
2. **Deleted** `services/persistence/` (4 files: `__init__.py`, `models.py`, `repositories/__init__.py`, `repositories/action_humanization_repository.py`) via `git rm -r`.
3. **Updated** `alembic/env.py` — removed `import services.persistence.models`, updated comment.
4. **Updated** `tests/security/test_schema_reconciled_1312.py` — removed the mirrored import, added a #1522 note. Kept the rest of the test (general reconciliation guard) unchanged.
5. **Updated** `scripts/create_missing_init_files.sh` — removed the two `services/persistence*` dir entries.
6. **Caller grep (after deletion)**: clean — only historical migration files and the two new explanatory comments remain.
7. **Local Postgres (port 5433) was behind head** (`m1797drop`, head `o1462oaut`) — ran `alembic upgrade head` to bring it current before adding the new migration (two pre-existing #1462 migrations applied, unrelated to this task).
8. Inspected the live table schema via `docker exec piper-postgres psql -U piper -d piper_morgan -c '\d action_humanizations'` (ground truth, not inferred from the ORM model, which declares lengths the DB migration never enforced): all string columns are unbounded `character varying`, `created_at`/`last_used` are `timestamp with time zone`, unique index `ix_action_humanizations_action` on `action`, PK `action_humanizations_pkey` on `id`.
9. **New migration** `alembic/versions/p1522drop_drop_action_humanizations.py`, revision `p1522drop`, down_revision `o1462oaut` (confirmed single head via `alembic heads` before writing). `upgrade()` drops the table; `downgrade()` recreates it with the exact schema from step 8 (including the unique index). Docstring states the prod row count (0) and its provenance per Arch's condition (a); condition (b) satisfied by the recreating downgrade.
10. **Round-trip verified** on local Postgres 5433: upgrade → table gone (`\dt` reports "Did not find any relation") → downgrade -1 → table recreated, `\d` output matches the pre-drop schema exactly (confirmed byte-for-byte: same columns, types, nullability, both indexes) → upgrade head again → table gone, `alembic current` → `p1522drop (head)`.
11. Full suites run (`tests/security tests/unit/services tests/test_architecture_enforcement.py tests/test_completion_ratchets.py`): **10472 passed, 231 skipped, 0 failed** (233.67s). `test_schema_reconciled_1312.py::test_autogenerate_diff_is_empty` run individually: **PASSED** (confirms no model↔DB drift post-drop).
12. Full-repo `pytest --collect-only`: **15656 tests collected**, 0 collection errors — confirms no stray importer of `services.persistence` anywhere in the tree.
13. `ruff format --check` + `ruff check` on the three touched `.py` files: **clean** ("3 files already formatted", "All checks passed!").
14. Committed (see commit sha in handback).

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md worktree/sign-off discipline (informed not pushing per explicit task instruction instead of the usual sign-off push); Arch's ruling memo and Exec's prod-count memo (both load-bearing for the commit message's required provenance statements); CLAUDE.md server-launch env-var-stripping note (used for JWT_SECRET_KEY + ANTHROPIC_* stripping when running pytest).
- **Loaded but not referenced**: MEMORY.md project/feedback index (general context, nothing specific to this mechanical deletion task).
- **Wanted but not found**: none — the task's pointers (Arch's memo, Exec's memo) were exactly where specified.

