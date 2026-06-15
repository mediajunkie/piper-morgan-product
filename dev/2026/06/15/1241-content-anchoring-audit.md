# #1241 — Content-Anchoring Audit (working doc)

_Lead Dev · started 2026-06-15 · per Arch's confirmed framing (memo 2026-06-15): two-axis classification + auth-resolution sub-inventory. **Status: IN PROGRESS — ownership-at-write axis done across SQL stores; read-axis + transitive-scoping + resolution sub-inventory pending.** Loop Arch when the read-axis is sampled on the high-risk stores._

## Framework (Arch's two axes)
| Axis | Categories |
|---|---|
| **Ownership-at-write** | (a) stamped at write · (b) stamped post-hoc · (c) never stamped |
| **Scoping-at-read** | (1) filtered by principal · (2) filtered post-hoc · (3) never filtered |

`(c,3)` = the actual privacy bug (the doc store today). `(a,3)` = owner-stamped but unscoped reads — patchable in one PR. `(a,1)` = correct. Plus a separate **auth-resolution sub-inventory**: where the principal originates and where it degrades to `Optional` mid-chain.

## Inventory
Content persistence lives in two places: **`services/database/models.py`** (37 SQL tables) and the **ChromaDB `pm_knowledge` collection** (`services/knowledge_graph/`). Other `__tablename__` files (`personality/models.py`, `persistence/models.py`) are config/humanization, not user-content surfaced through Radar.

## Ownership-at-write axis — DONE (this pass)

**Stamped (a) — has `user_id`:**
| table | NOT NULL? | notes |
|---|---|---|
| `conversations` | ✅ NOT NULL | #849 |
| `conversational_memory_entries` | ✅ NOT NULL | |
| `insights` | ✅ NOT NULL | Radar "insight/recently" stream |
| `standup_conversations` | ✅ NOT NULL | |
| `feedback` | ⚠️ nullable | weaker — nullable owner can degrade |
| `learned_patterns` | ⚠️ nullable | |

**Never stamped (c) — NO `user_id` column** (the gap population):
- **Radar entity types**: `work_items` ❌, `uploaded_files` ❌, `stakeholders` ❌ (People-adjacent), `artifacts` ❌ — *the Radar WorkItem/Document/People backends are all unanchored at the data layer, not just the ChromaDB doc store.*
- **Knowledge graph**: `knowledge_nodes` ❌, `knowledge_edges` ❌
- **Lists**: `lists` ❌, `list_items` ❌, `todo_lists` ❌
- **PM domain objects**: `products` ❌, `features` ❌, `projects` ❌, `tasks` ❌, `workflows` ❌, `intents` ❌
- **Child-of-scoped (likely transitive)**: `conversation_turns` ❌ (FK → `conversations`, which is scoped)
- **ChromaDB doc store**: ❌ no owner (the original #1238 finding) — `(c,3)`.

## Preliminary finding (answers PM's "how systematic is it")
**The gap is systemic, not a doc-store one-off.** ~half the content tables + the doc store have no owner column. The recurrence PM named is real and structural — there's no enforced ownership invariant, so each new content type re-opens it. This is the empirical grounding for **ADR-071 D2** (ownership-stamped-at-write invariant).

## Caveats to resolve before finalizing (don't over-claim yet)
1. **Transitive scoping**: some unstamped tables FK to a scoped parent (`conversation_turns`→`conversations`, `list_items`→`lists`, `knowledge_edges`→`knowledge_nodes`). If the parent is scoped and reads always join through it, the child is scoped-via-parent — *not* a leak. Must verify per FK chain.
2. **Global-by-design**: `products`/`features`/`projects`/`work_items` may be intentionally shared PM-domain objects in the single-PM model (vs. needing per-user scoping). That's an Arch D1 determination (the over-anchoring guard), not an automatic gap.
3. **Read-axis not yet done**: ownership-at-write is necessary but the *leak severity* lives in scoping-at-read (does the read filter by principal?). A `(a,3)` is a leak despite being stamped; a `(c,3)` is the worst. The read-path analysis is the next pass.

## Next (this audit, across fires)
- [ ] **Read-axis**: sample the read paths for the high-risk stores (insights, work_items, uploaded_files, stakeholders, knowledge graph) — do they filter by `user_id`? Classify `(x,1/2/3)`.
- [ ] **Transitive-scoping**: resolve the child-of-scoped tables (caveat 1).
- [ ] **Global-by-design**: flag the candidates (caveat 2) for Arch's D1 call.
- [ ] **Auth-resolution sub-inventory**: where does `user_id` originate (host boundary) and where does it go `Optional` mid-chain (the `conversation_handler.py` `intent.context.get("user_id")` shape)?
- [ ] **Loop Arch** with the 2-axis table once the read-axis is sampled → scope ADR-071 D1–D7 on this evidence.
