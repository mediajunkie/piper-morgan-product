# Gameplan — RECONNECT WS-1: DB-backed connector-config store (#1226 + #1199)

**Author**: Lead Dev · **Date**: 2026-06-21 · **Sprint**: RECONNECT Phase-1
**Issues**: #1226 (umbrella — config has no stable home), #1199 (unify the two stores). **Epic**: RECONNECT (`connector-refactor-sprint-scope-2026-06-14.md` §1/§2b).
**Authority**: Arch build-order ruling 2026-06-21 (`memo-arch-…-1232-RATIFIED-plus-phase1-build-order…`) — WS-1 starts now, independent of #1185; order = **WS-9-collapse → WS-1 → ports**; build multi-tenant-READY (m-40).
**ADRs**: ADR-070 D4 (DB-backed config) · ADR-071 D2 (`owner_id`) + D7 (`tenant_id` path named-not-built) · ADR-058 (multi-tenancy isolation) · ADR-070 D3 (no creds in config — creds stay in keychain).

---

## Problem (verified live, 2026-06-21)

Connector config (the user's default repo etc.) has **no stable home** — it's scattered across **three disconnected stores**, and the DB-backed resolution paths are dead:

1. **`data/github_preferences.json`** — flat JSON, **bare relative path** (`settings_integrations.py:289` `GITHUB_PREFERENCES_FILE = "data/github_preferences.json"`) → resolves against **process cwd**. Present in the worktree, absent in the main checkout → "worked then broke." Written by the settings endpoint; read by `repo_resolver` path 4 (#1192a bridge).
2. **`UserPreferenceManager`** (`services/domain/user_preference_manager.py`) — **in-memory dicts**, doesn't survive restart. `set_default_repo` has **zero non-test callers** (nothing writes it) but **live readers exist**: `morning_standup.py:269` + `standup_workflow_skill.py:545` call `get_default_repo` → **silently get `None`** even when the user set a repo via the UI (which went to store 1).
3. **`services/integrations/github/config_service.py`** `get_default_repository()` — a third path (also `intent_service._get_default_repository`).

`repo_resolver.resolve_repo` (`repo_resolver.py:91-174`) has 6 paths; paths 2/3 (DB project-links) are **dead DB-wide** (0 rows). The failure is **silent** — generic "no open issues" instead of an honest "no repo configured" (M3 UAT: PM asked "what should I work on?" → wrong answer despite open issues + a valid token).

## Goal

One **DB-backed connector-config store** (`connector_configs`), anchored to the settled single identity (`owner_id` FK → `users.id`), that:
- replaces all three stores as the single source of truth for connector config;
- is **multi-tenant-READY** (owner_id now + a named-not-built `tenant_id` column, m-40 / ADR-071 D7) — generalizes without a re-stamp when #1185/public-BYOC lands;
- **honest-degrades** — an unresolved config surfaces "configure a repo," never silent `None`/generic (D5/WS-4 principle);
- holds **no credential material** (D3 — creds stay in keychain; config = default_repo, selected_repos, etc.).

## Schema (ADR-070 D4)

`connector_configs`:
| col | type | notes |
|---|---|---|
| `id` | UUID PK | |
| `owner_id` | FK → `users.id`, NOT NULL, indexed | the settled single identity (ADR-071 D2) |
| `tenant_id` | UUID NULL | **named, not built** (ADR-071 D7) — NULL = single-tenant; the multi-tenant path is documented but no logic uses it yet (m-40) |
| `connector` | str, NOT NULL | "github" / "slack" / "calendar" / "notion" |
| `config` | JSON, NOT NULL default `{}` | connector-agnostic blob; github = `{default_repository, selected_repositories}`. **No creds** (D3). |
| `created_at`/`updated_at` | tz-aware | TimestampMixin |

Unique: `(owner_id, connector)` (per-owner one config row per connector; the `tenant_id` generalization is the future composite — named in a comment, not enforced multi-tenant yet).

## Phases (TDD; audit-cascade between)

- **P0 — WS-9 collapse** (Arch step 1): unify PM's two records (`m1-test` 009afc8c + `xian` a25db09c) → one canonical `owner_id` (the active `m1-test`, 47 convs). Quick data migration: re-point `xian`'s rows (1 conv + any) to `m1-test`; settle the FK target. TDD: a migration test + a guard that the canonical id resolves. *(Light — PM's own test data; low-stakes per the WS-9 resolution.)*
- **P1 — schema + migration**: `ConnectorConfig` model in `services/database/models.py` + an **additive Alembic migration** (new table, no DDL on existing). TDD: model + table-exists + FK + unique-constraint tests.
- **P2 — repository + service**: `ConnectorConfigRepository` (get/upsert by `(owner_id, connector)`) + a thin `ConnectorConfigService` (`get_default_repo(owner_id)` / `set_default_repo`). TDD: upsert idempotency, per-owner isolation, missing→honest-miss.
- **P3 — wire readers + migrate data**: point `repo_resolver` path 4, the standup readers (morning_standup/standup_workflow_skill), `config_service`, and the settings GET/POST at the new service. **Backfill** `data/github_preferences.json` → DB (idempotent, owner-resolved). Behind a marker if needed for zero-downtime. TDD: each reader resolves from DB; the standup silent-None bug is fixed (real default now flows).
- **P4 — honest-degrade + retire the old stores**: unresolved config → the honest "configure a repo" surface (not silent/generic). **Comment-out/DEAD-mark** the in-memory `set/get_default_repo` + the flat-file helpers (don't delete yet — read-bridge safety), delete `data/github_preferences.json` once the backfill's verified. TDD: honest-degradation assertion (the #1226 UAT case: open issues → real answer or honest config-prompt, never "no open issues" when unresolved).
- **P5 — close**: close #1199 (stores unified) + #1226 (stable home) properly (evidence: tests + the live-resolution fix). #1226 is the umbrella — verify its ACs.

## Test strategy
- Unit: model/repo/service (TDD per phase).
- Integration: `resolve_repo` resolves from the DB store end-to-end; the standup path gets the real default (the silent-None regression test).
- The honest-degradation case (#1226's UAT failure) as an explicit test.

## Rollback
- Additive migration (new table) → `alembic downgrade` drops it cleanly; the old stores stay comment-marked (not deleted) through P3/P4 so a revert restores resolution. The flat file is deleted only after backfill verification (and backed up first).

## Multi-tenant-READY guardrail (m-40)
`tenant_id` column exists + is documented as the future composite-key path, but **no code branches on it** and no multi-tenant logic is built. Single-owner now; generalizes when #1185 lands. Do NOT hardcode single-user assumptions into the schema (the FK is `owner_id`, not a literal).

## Open question for Arch (non-blocking; flag at P1)
The `config` JSON-blob vs typed-columns choice: I lean JSON (connector-agnostic, extensible — github/slack/calendar configs differ). Confirm at the schema review if D4 intends otherwise.

---

## GAMEPLAN audit (vs template v9.6, 2026-06-21)

| Template area | Status | Note |
|---|---|---|
| Phase -1 infra-verify | ✅ | FastAPI / PostgreSQL(5433) / pytest / `users` table — verified live, not assumed |
| Phase 0 investigation | ✅ | #1226 + #1199 read; 3-store surface + dead DB paths verified live |
| Phase 0.5 FE↔BE contract | ⚠️→ noted | One UI touch-point: the settings GET/POST github-prefs endpoint (`settings_integrations.py:1821/1848`) re-points at the service in P3 — no new routes, so no path-mismatch risk; verify the endpoint still round-trips. |
| Phase 0.6 data-flow | ✅ added below | THE critical one — `owner_id` propagation (the #490 class) |
| Phase 0.7 conversation | ✅ N/A | not conversational |
| Phase 0.8 post-completion | ✅ | the downstream change is honest-degradation (P4) + the standup-default now flowing (P3) |
| Success criteria | ✅ added below | |
| Wiring tests | ✅ added below | |
| Rollback | ✅ | additive migration + comment-marked old stores |
| STOP conditions | ✅ added below | |

## Phase 0.6 — Data flow: `owner_id` propagation (the #490 lesson)

WS-1 is a multi-layer feature where one identity value must flow cleanly through every layer — exactly the shape that caused the #490 bugs (a value keyed/named differently per layer). The risk here: the current code passes the user identity in **several forms** (`current_user.sub` (JWT), `user_uuid`, `user_id` string) and the new store keys on the canonical `owner_id` (FK → `users.id`). They must all resolve to the **one** identity that WS-9-collapse settles.

| Layer | Needs owner_id | Current source | Pitfall |
|---|---|---|---|
| settings route (GET/POST prefs) | yes | `get_current_user().sub` | JWT sub → must map to `users.id` |
| `repo_resolver.resolve_repo` | yes | passed by caller (intent/standup) | caller passes a string today; must be the canonical id |
| `ConnectorConfigService` | yes | param from resolver/standup | single param, typed |
| `ConnectorConfigRepository` | yes | param from service | the FK value |
| standup readers (`morning_standup:269`, `standup_workflow_skill:545`) | yes | `user_uuid` they resolve | must hit the DB store, not the writer-less in-memory one |

**Mitigation**: a single resolve-to-`owner_id` helper at each entry, anchored to the WS-9-collapsed canonical id; one **wiring test** per reader proving the real value flows DB→reader (no mocked internals). State key = `(owner_id, connector)`; lookup-fail → honest-miss, never `None`.

## Success criteria (ACs — PM validates)
- [ ] `connector_configs` table exists (additive migration; `owner_id` FK, `tenant_id` named-not-built, `(owner_id, connector)` unique).
- [ ] `repo_resolver` resolves the default repo from the DB store (path 4 re-pointed); the flat `github_preferences.json` cwd-fragility is gone.
- [ ] The standup silent-`None` bug is fixed — a default set via the UI flows to `morning_standup` + `standup_workflow_skill` (regression test).
- [ ] Unresolved config → honest "configure a repo" surface, never silent `None`/generic (the #1226 UAT case: open issues → real answer or honest prompt).
- [ ] `data/github_preferences.json` backfilled to DB + removed; in-memory `set/get_default_repo` retired (comment-marked).
- [ ] No creds in `connector_configs` (D3); multi-tenant-READY (m-40) — `tenant_id` present, no logic branches on it.
- [ ] Tests: unit (model/repo/service) + integration (resolve end-to-end) + wiring (owner_id through real path) + the honest-degradation case.

## STOP conditions (WS-1-specific, atop the standard set)
- WS-9-collapse surfaces a non-trivial merge (PM's records have unexpected cross-references) → STOP, escalate (it was scoped as "trivial").
- An `owner_id`/`user_id` form can't be resolved to the canonical id at a call site → STOP, trace the source (don't guess — #490 lesson).
- The D4 schema (JSON vs typed) needs an Arch call → flag at P1 schema review (the open question above), don't proceed on a guess.
- A reader resolves config but the value disagrees across the three old stores → STOP, reconcile which is authoritative before backfill.

**Audit verdict: PROCEED** — gaps fixed in-place; build starts at P0 (WS-9-collapse).
