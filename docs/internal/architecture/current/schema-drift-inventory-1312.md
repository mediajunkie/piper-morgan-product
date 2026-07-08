# Schema Drift Inventory — #1312 (DB ↔ model reconciliation)

**Status**: AUDIT COMPLETE 2026-07-08 (Lead Dev). Remediation NOT started — deliberately, with
the alpha deploy pending the same day (no schema-touching on deploy day). This doc is the
classified inventory + proposed gameplan; remediation proceeds post-deploy, gated on the
Arch calls in §7.

**How generated**: `alembic revision --autogenerate` against a fresh `f1305encjson` head on the
local dev DB, **after** landing the env.py model-imports fix (§1) so the comparison is complete.
The generated migration (`5e592a84322d_drift_inventory_1312_DO_NOT_APPLY`) was classified and
**deleted** — it must never be applied; ~40% of its ops would destroy real indexes/columns.
241 ops total.

---

## 1. What landed now (safe, additive)

`alembic/env.py` now imports `services.database.models` + `services.persistence.models` so
`target_metadata` is complete at autogenerate time. Before this, `action_humanizations` (and
anything else registered only via persistence.models) read as false-positive "removed table"
drift. Verified: `alembic upgrade head` unaffected; autogenerate now sees the full divergence.

## 2. Root cause (supersedes the "two authorities" hypothesis)

The obvious suspect — `Base.metadata.create_all` racing alembic — is **innocent**:
`DatabaseConnection.create_tables()` (connection.py) has **zero callers** at runtime. Alembic is
the *sole live schema authority*. The drift accumulated the ordinary way: model edits shipped
without migrations (or migrations hand-written to a different shape than the model), on both
sides, over ~a year. The MUX phase-0 migration (`601_mux_multichat_phase0_conversation_graph`)
contributed a whole DB-side family whose model side never merged (§4-B, §4-C).

## 3. Headline finding — an orphaned 75%-complete domain (`todo_lists`)

The model defines `TodoListDB` (`todo_lists`, models.py:1742, "PM-081") + 5 indexes, and
`ListItemDB.list_id` / `ListMembershipDB` FK-point at it. **No migration ever created the
table** — it does not exist at alembic head. Live impact today: **none** — the mounted Todos
API (`web/app.py:264`) injects `TodoRepository → TodoDB → todo_items` (exists); #479's fix
explicitly routed injection *away* from `TodoListRepository → TodoListDB → todo_lists`
(broken). But the orphan is armed: any future code that uses `TodoListRepository` (or
universal_list_repository.py's compat wrapper, line 651) gets `UndefinedTable` at first query.
Disposition is a per-class judgment (§7): **finish it** (write the create migration) or
**excise it** (consolidate the todo-list concept onto the live `lists` table and delete the
orphan classes). The 75%-pattern rule says complete-or-remove, not leave-armed.

## 4. The classified buckets (all 241 ops accounted for)

### A. Model-only table (autogen: `create_table`)
| Object | Detail | Judgment needed |
|---|---|---|
| `todo_lists` + 5 indexes + `list_memberships`/`list_items` FK re-points | §3 | finish vs excise (Arch/PM) |

### B. DB-only table (autogen: `drop_table` — would DESTROY)
| Object | Detail | Judgment needed |
|---|---|---|
| `conversation_links` + 5 indexes | Created by MUX phase-0 migration 601; **no model anywhere, no code references** (only alembic files mention it) | MUX roadmap owns it — model it when MUX conversation-graph work resumes, or drop it with MUX's sign-off. Do NOT drop unilaterally. |

### C. DB-only columns (autogen: `drop_column` — would DESTROY)
| Column | Likely provenance | Judgment needed |
|---|---|---|
| `conversation_turns.parent_id` (+FK +index) | MUX phase-0 thread-graph | Same MUX gate as B |
| `features.lifecycle_state` | MUX Hard/Soft object lifecycle | Same MUX gate as B |
| `todo_items.lifecycle_state` | MUX Hard/Soft object lifecycle | Same MUX gate as B |
| `feedback.owner_id` (+named FK) | owner-scoping era; model uses `user_id` | model-vs-DB: which is canonical? Data check: is owner_id populated/distinct from user_id? |
| `personality_profiles.owner_id` (+named FK) | same | same |
| `personalization_contexts` `uq_..._owner` constraint | e441reset-era model change | verify the reset design intended constraint removal |

### D. Index churn (~60 ops — three DIFFERENT severities, do not treat as one)
- **D1 name-only** (`idx_foo` ↔ `ix_foo`, same columns): cosmetic. Fix **model-side** with
  explicit `Index(name=...)` matching the DB (or a one-time DB rename migration). Examples:
  `idx_conversations_owner` → `ix_conversations_owner_id`, `idx_uploaded_files_owner` →
  `idx_files_owner` (also reorders columns — check), `idx_standup_conversations_owner`,
  `idx_insights_owner`, `idx_cme_*` pairs.
- **D2 model-wants, DB-lacks** (autogen `create_index` — additive, safe): `audit_logs` +10
  single-column `ix_*`; `token_blacklist` +3 (incl. UNIQUE `token_id`); `feedback`
  ix_session_id/ix_user_id; `users` UNIQUE ix_email/ix_username (DB uniqueness currently via
  constraints? verify before adding); `conversations` topics GIN + user_session composite.
  These are real missing indexes IF the model's `index=True` flags reflect intent.
- **D3 DB-has, model-lacks** (autogen `drop_index` — would LOSE real indexes): the dangerous
  class. Composite/partial/GIN indexes the DB has that models never declared:
  `idx_conversations_user_created`, `idx_conversation_turns_conv_created` / `conv_intent` /
  `entities` (GIN) / `references` (GIN) / `turn_number` / `created_at`,
  `idx_feedback_user_status_date`, `idx_insights_user_not_deleted` (partial),
  `idx_projects_owner_archived` (partial), `idx_audit_logs_user_timeline`,
  `idx_users_role`, `idx_unique_list_item` (**UNIQUE — dropping changes semantics**),
  `idx_list_item_due` / `_priority` / `_position` / `_added_at`. Fix **model-side**: declare
  them in `__table_args__` so autogen stops proposing their destruction.

### E. FK churn
- Named-FK → unnamed recreation (`fk_*_owner_id` dropped, `create_foreign_key(None, ...)`):
  naming-convention churn on knowledge_edges/nodes, list_items, list_memberships, projects.
  Fix: adopt a `naming_convention` on MetaData (standard SQLAlchemy fix) or name FKs in models.
- **Dropped with NO recreation** (real semantic diffs): `audit_logs_user_id_fkey`,
  `user_api_keys_user_id_fkey`, `fk_uploaded_files_owner_id` — model genuinely lacks these FKs
  (or has them without constraint). Per-FK judgment: add to model (keep integrity) vs migrate
  DB (if the removal was intentional, e.g. audit rows outliving users).
- `ondelete` diffs ride the same per-FK pass.

### F. Type/nullable comparator noise (no DB change wanted)
- `feedback.context/conversation_context/categories/tags` + `lists.metadata`: DB `JSONB` vs
  model `sa.JSON` → declare `JSONB` in models (JSONB is the better type; keep it).
- `learned_patterns.pattern_data`: DB `JSON` vs model `EncryptedJSON` (#1305 TypeDecorator) —
  autogen can't see through the decorator. Fix: implement `compare_against_backend` /
  `coerce_compared_value`-style type comparison on `EncryptedJSON` (or set
  `impl`/`load_dialect_impl` so it compares as the underlying JSON). Without this, every
  #1305 column re-drifts in every future autogen.
- `projects.is_default/is_archived/created_at/updated_at`, `personality_profiles.created_at/
  updated_at`: DB `NOT NULL` (+server defaults) vs model nullable → tighten the **models**
  (`nullable=False`, `server_default=`); never loosen the DB.
- `personality_profiles` unique on `user_id`: model wants it; verify DB data allows, then add.

## 5. End state (unchanged from the issue)

`alembic revision --autogenerate` against a fresh head produces an **empty** migration, and a
CI guard keeps it that way (generate → assert no ops → delete; fails the build on re-drift).

## 6. Proposed remediation sequence (post-deploy)

1. **Model-side-only pass — ✅ DONE 2026-07-08 (Lead)**: D1 names, D3 declarations, F
   type/nullable tightening + the EncryptedJSON comparator (`compare_against_backend` +
   an env.py `compare_type` callback — alembic's default compares the dialect impl, so
   the hook alone never fires). E naming_convention deliberately EXCLUDED (Base-level
   blast radius — rides the judgment classes). Result: **241 → 89 total ops (41 in
   upgrade); zero type alters, zero index churn**. The residual is exactly §7's
   judgment classes + 2 deliberate D2 index wants (idx_conversations_user_session,
   idx_files_owner composite) + 2 ciphertext-GIN drops (correct DB-side, phase 3).
   Bonus finds: the model still declared f1305-dropped idx_conversations_topics_gin
   (removed); projects has a GENUINE duplicate index pair in the DB (idx_projects_owner
   + idx_projects_owner_id, both declared model-side for now — dedup is a phase-3 call).
2. **Arch rulings** (§7), then the judgment classes: A (todo_lists finish-or-excise),
   B/C MUX family, C owner_id family, E dropped-FKs.
3. **One reviewed reconciliation migration** for whatever DB-side changes survive step 2
   (D2 additive indexes ride here too).
4. **CI autogen-empty guard** (#1312's AC).

## 7. Open Arch calls (memo sent 2026-07-08)

1. **Multi-Base**: `services/personality/models.py` runs its own `declarative_base()` —
   unify onto shared Base vs register multiple metadatas with alembic. (Its tables are
   invisible to autogen either way today.)
2. **todo_lists**: finish (migrate the table in) vs excise (consolidate onto `lists`).
3. **MUX family** (conversation_links, parent_id, lifecycle_state ×2): park-with-model
   (declare models to stop the drift, table stays) vs defer-to-MUX-resume vs drop-with-sign-off.
