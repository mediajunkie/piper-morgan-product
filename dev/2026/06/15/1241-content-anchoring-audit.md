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

**Implication**: there's no canonical "anchor content to the principal" field or read-scoping mechanic — three coexisting styles (`user_id`-string, `owner_id`-FK, none). That's the structural reason new content types re-derive ownership. **ADR-071 must**: (1) name THE canonical principal-anchoring field + type, (2) state when `owner_id`-FK vs `user_id`-string is correct (or standardize one), (3) specify the read-scoping mechanic per style. Related existing docs to reconcile: ADR-044 (lightweight RBAC), `artifact-model-design-952.md`. **PM raised "document this distinction" 2026-06-15 → ADR-071 is the home.**

## Caveats / still to do
1. **Read-axis (scoping-at-read) NOT yet sampled** — the leak *severity* lives here. An anchored table (`owner_id` present) can still be `(a,3)` if reads don't filter. Sample read paths for the anchored majority + confirm the `(c,3)` gaps.
2. **Global-by-design**: the PM-domain cluster — Arch D1.
3. **`conversation_turns` transitive** — verify FK→conversations.
4. **Auth-resolution sub-inventory** — where `user_id` originates (host boundary) + where it goes `Optional` mid-chain (the `conversation_handler.py` `intent.context.get("user_id")` shape Arch flagged).

## Next (across fires)
- [ ] Read-axis sample (anchored stores: do reads filter by owner? + confirm the (c,3) gaps).
- [ ] Resolve transitive (`conversation_turns`) + flag global-by-design cluster for Arch D1.
- [ ] Auth-resolution sub-inventory.
- [ ] **Loop Arch** with the corrected 2-axis table → scope ADR-071 D1–D7 on this evidence.
