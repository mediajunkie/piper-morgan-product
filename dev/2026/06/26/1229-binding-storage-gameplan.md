# #1229 (RECONNECT WS-2) — binding-storage foundation gameplan

**Author**: Lead Dev · **Date**: 2026-06-26 · **Design source**: ADR-070 D3/D4 (ruled) · **Template**: WS-1 #1199 `connector_configs`
**Scope**: re-scoped per the #1229 comment — build the per-user MCP-server-binding storage foundation (NOT the superseded raw-cred unification). Per-connector cred cleanups fold into the ports (#1317).

## Why this is low-drift (audit-cascade self-check)
- Design is fully specified: ADR-070 D3 (bindings not raw creds; the binding's contents) + D4 (DB-backed, owner-scoped) + ADR-071 D2 (owner_id FK) / D7 (tenant_id named-not-built) / ADR-058 (user isolation).
- Implementation mirrors an existing, shipped, reviewed pattern: `ConnectorConfig` model (`models.py:598`) + `ConnectorConfigRepository` + migration `000baa96d800`. Same table shape, different columns.
- No new architecture invented; no cross-cutting consumer yet (the ports populate it later).

## Phases (TDD)
1. **Model** — `ConnectorBinding(Base, TimestampMixin)` in `services/database/models.py`: `id`, `owner_id` (FK users.id, NOT NULL, index), `tenant_id` (nullable, index), `connector` (String(50)), `mcp_server_ref` (String(255), nullable — set on connect), `status` (String(32), default "unbound"), `capability_profile` (JSONB/JSON cross-dialect, default {}), `is_native_legacy` (Boolean, default False), `UniqueConstraint(owner_id, connector)`.
2. **Migration** — additive `create_table connector_bindings` (down_revision `000baa96d800`), mirroring the WS-1 migration; cross-dialect (`with_variant` JSON, `sa.false()`). Indexes on owner_id + tenant_id. ADDITIVE ONLY (exclude the pre-existing #1312 drift, like the WS-1 migration did).
3. **Repository** — `ConnectorBindingRepository(session)` in `services/connectors/binding_repository.py`: `get(owner, connector)` (graceful None on bad owner), `upsert(owner, connector, **fields)` (strict owner, replace-in-place), `set_status(owner, connector, status)`. Mirror `ConnectorConfigRepository` read/write asymmetry.
4. **Tests** — `tests/unit/connectors/test_binding_repository.py`: round-trip; per-owner isolation (owner A can't read owner B's binding); upsert idempotency on (owner,connector); status transition; bad-owner graceful-None on read / raises on write.

## Acceptance criteria
- [ ] `connector_bindings` table + model, owner-stamped (ADR-071 D2) + tenant-named (D7), no raw-cred fields (D3 — bindings only).
- [ ] Additive migration applies clean on Postgres (5433) + SQLite; `alembic upgrade head` green; ADDITIVE (no drift drops).
- [ ] Repository get/upsert/set_status with per-owner isolation; bad-owner read→None, write→raise.
- [ ] Unit tests pass; no regressions in the connectors suite.
- [ ] #1229 closed-properly with evidence; per-connector cred-cleanup fold noted (→ #1317).

## Out of scope (folds to #1317 ports / superseded)
- The connect() flow that POPULATES bindings (WS-5 ports). The typed raw-cred wrapper (superseded by D3). The stale-github-reader + Notion-disambiguation cleanups (fold per-connector into ports). The `connector_configs.mcp_server_binding_id` FK wiring (wire when ports create bindings).
