# #1241 — Content-Anchoring Audit (working doc)

_Lead Dev · started 2026-06-15 · per Arch's confirmed framing (2-axis + auth-resolution sub-inventory). **Status: IN PROGRESS — ownership-at-write axis done + corrected; read-axis (scoping-at-read) + global-by-design determination + resolution sub-inventory pending. Loop Arch after the read-axis sample.**_

> **Correction note (07:2x):** an initial write-axis pass grepped only `user_id` and reported "~half the content tables unanchored." That was an **over-claim** — re-checking `owner_id` too (caught via the FK pass) shows **most content tables ARE owner-anchored**. Corrected classification below. The genuine finding is narrower + about *consistency*, not raw count.

## Framework (Arch's two axes)
- **Ownership-at-write**: (a) stamped at write · (b) post-hoc · (c) never. **Scoping-at-read**: (1) by principal · (2) post-hoc · (3) never.
- `(c,3)` = the actual privacy bug. Plus a separate **auth-resolution sub-inventory** (where the principal originates / degrades to `Optional`).

## Inventory
Content persistence = **`services/database/models.py`** (37 SQL tables) + the **ChromaDB `pm_knowledge` collection** (`services/knowledge_graph/`).

## Ownership-at-write axis — DONE + CORRECTED (user_id OR owner_id OR FK→users)

**Owner-anchored (a):**
- via `user_id`: `conversations`, `insights`, `feedback`, `learned_patterns`, `conversational_memory_entries`, `standup_conversations`
- via `owner_id`: `uploaded_files`, `artifacts`, `knowledge_nodes`, `knowledge_edges`, `todo_lists`, `lists`, `list_items`
- via both: `projects`

**Truly unanchored (c) — no `user_id`/`owner_id`, no FK→users:**
- **PM-domain cluster**: `products`, `features`, `work_items`, `intents`, `workflows`, `tasks` (FK only among themselves — no path to a principal). ⚠️ likely **global-by-design** (one-PM work objects) → Arch D1 call, may be correct-as-is, not a leak.
- **`stakeholders`** — no owner, no FK. Matters: this is a People-adjacent table; the People entity backend is unanchored.
- **`conversation_turns`** — no direct owner; **likely transitive** via `conversations` (verify the FK; probably scoped-via-parent).
- **ChromaDB doc store** — no owner, global collection → the #1238 case, the clearest **(c,3)**.

## Finding (corrected — answers PM's "how systematic is it")
**Not "half the tables are unanchored" (retracted). The real, systemic problem is INCONSISTENCY:** anchoring is done three different ways — `user_id` on some tables, `owner_id` on others, and **absent** on the PM-domain cluster + the doc store. There's **no single enforced ownership invariant**, so a new content type inherits no pattern and re-litigates ownership each time — exactly the recurrence PM named ("not our first attempt"). That inconsistency is the load-bearing motivation for **ADR-071** (one canonical, enforced anchoring pattern), more than any single gap count.

**Genuine gaps (real, fewer than first claimed):**
1. **ChromaDB doc store** — clearest `(c,3)`; the #1238 blocker. Worked-example for ADR-071's first migration.
2. **`stakeholders`** — unanchored; the People-entity backend has no owner. Relevant to the Radar People source (#1240).
3. **PM-domain cluster** — unanchored; **needs Arch's D1 global-by-design ruling** (single-PM work objects may not need user-anchoring; ADR-058 handles per-tenant config).

## KEY FINDING — `user_id` vs `owner_id` are semantically distinct (→ ADR-071 must canonicalize)
This is the crux of the recurrence (and what tripped the initial over-claim). The two are **not interchangeable**:
- **`owner_id`** — consistently `Column(UUID, ForeignKey("users.id"))`. A domain-ownership link to the internal `users` row. Read-scoping = **join through `users`**.
- **`user_id`** — the **external auth-principal** identifier, and *itself inconsistent*: often `Column(String(255))` (a JWT-`sub` / connector user-id string, **NOT** a FK), sometimes UUID. Read-scoping = **filter by the principal string**.
- `projects` carries **both** (`owner_id` for ownership + uniqueness; `user_id` in the share-permission path) — proof they mean different things.

**Implication**: there's no canonical "anchor content to the principal" field or read-scoping mechanic — three coexisting styles (`user_id`-string, `owner_id`-FK, none). That's the structural reason new content types re-derive ownership. **ADR-071 must**: (1) name THE canonical principal-anchoring field + type, (2) state when `owner_id`-FK vs `user_id`-string is correct (or standardize one), (3) specify the read-scoping mechanic per style. Related existing docs to reconcile: ADR-044 (lightweight RBAC), `artifact-model-design-952.md`. **PM raised "document this distinction" 2026-06-15 → ADR-071 is the home.** **PM 2026-06-15 endorsed "an architectural decision AND a consolidating refactor"** → ADR-071 + a consolidation refactor are PM-blessed. **Refactor scope = consolidate `user_id`/`owner_id` to the one canonical principal-anchoring pattern AND anchor the (c) gaps (doc store, stakeholders, + global-by-design ruling on the PM-domain cluster)** — sequenced as ADR-071's migration (m-40 layer-then-migrate), doc store first (#1238).

## Scoping-at-read axis — DONE (fanned-out sweep; 2 high-severity findings verified by hand)

| Store | owner | read-scoping | evidence |
|---|---|---|---|
| `conversational_memory_entries` | user_id | **(1) clean** | `conversational_memory_repository.py:57` filters user_id |
| `uploaded_files` | owner_id | **(1) clean** | `file_repository.py:66/97/112` filter owner_id |
| `lists` | owner_id | **(1) clean** | `todo_repository.py:40/64` require owner_id |
| `conversations` | user_id | **(1) … but a (3) path** | list/search/get_latest filter user_id (`repositories.py:1415/1447/1491`); **`get_by_id():1544` is UNSCOPED** — `session.get(ConversationDB, id)` by PK, no owner check ✅verified |
| `insights` | user_id | **(1) … but a (3) path** | `list_for_user:2209`/`get_unsurfaced:2323` filter user_id; **`get_for_object():2316` is UNSCOPED** — `where(object_id==…)` only ✅verified |
| `knowledge_nodes` | owner_id | **(1) but OPTIONAL** → (3) risk | owner filter only applied when `owner_id` passed (`repositories.py:913/925`); `None` → unscoped |
| `artifacts` | owner_id | **(2) post-hoc** | `get_by_id:2674` fetches by PK then filters in Python (`:2686`); `list_for_owner:2690` is (1) |
| `stakeholders` | NONE | **(3)** | no owner column; all reads global |
| ChromaDB doc store | NONE | **(3)** | `document_service.py:78/202/273` query by timeframe / empty `where={}`; no principal |

## Auth-resolution sub-inventory (Arch refinement B) — the biggest finding
- **Origination (correct)**: `services/auth/auth_middleware.py:177` (`request.state.user_id` from JWT) + `:316` `get_current_user`→`JWTClaims`. The principal IS resolved at the host boundary.
- **Degradation epidemic**: the pattern `user_id = intent.context.get("user_id") if intent.context else None` recurs **40+ times** — `classifier.py:199/252`, `conversation_handler.py:97/157`, `intent_service.py:3163` (+ ~40 handlers), `:5926`. A missing/empty context **silently degrades the principal to `None`** mid-chain; some paths then proceed unscoped. **The principal is resolved at the boundary but NOT threaded as a required parameter** — it's re-fetched opportunistically from mutable context and degrades to None. This is the structural read-side leak vector (ADR-071 **D4**).

## SYNTHESIS → ADR-071 grounding (audit analytical phase COMPLETE)
1. **Inconsistency** (user_id-string / owner_id-FK / none) → **D2** canonical field + **the consolidating refactor** (PM-blessed).
2. **(c,3) store gaps**: ChromaDB doc store + `stakeholders` → **D2/D6** (anchor + migrate; doc store = first instance, #1238).
3. **(a,3) leak PATHS** in owner-stamped stores (`conversations.get_by_id`, `insights.get_for_object`, `knowledge_nodes` optional, `artifacts` post-hoc) → **D3** scoping-filtered-at-read invariant + **D5** AST guard (a read method on a content store must take + apply a principal).
4. **Resolution degradation (40+ sites)** → **D4** principal-resolution-at-the-boundary (thread as required param, not re-fetched-from-context). Arguably the highest-leverage fix.
5. **Global-by-design**: PM-domain cluster (products/features/work_items/intents/workflows/tasks) → **D1** over-anchoring guard (Arch's call — likely correct-as-global in single-PM).

## Remaining (post-Arch-loop)
- [ ] Arch's **D1 global-by-design ruling** on the PM-domain cluster.
- [ ] `conversation_turns` transitive-FK confirm (minor).
- [ ] **ADR-071 draft** (Lead-author / Arch-ratify) grounded in the above.
- [x] **Loop Arch** — done (memo 2026-06-15) with this evidence.
