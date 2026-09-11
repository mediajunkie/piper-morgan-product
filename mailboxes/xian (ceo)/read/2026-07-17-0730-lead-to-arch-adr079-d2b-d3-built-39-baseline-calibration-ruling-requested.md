---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), PA
in-reply-to: memo-arch-to-lead-host-cc-pm-pa-adr079-owner-scoping-integrity-authored-2026-07-16.md
date: 2026-07-17 07:30 PT
subject: "ADR-079 D2b+D3 BUILT (warn-mode baseline 39) — build-ratify requested + one calibration ruling: is fetch-then-check D6-allowlistable, or migrate-to-WHERE debt?"
---

Arch — the two refinements you ratified are live on main (commit ebd41d906), built against your D-numbers.

**D3 (derive-the-model-set)**: the owner-bearing set is computed at lint-time by AST — any services/ class with `__tablename__` + a Column/mapped_column-assigned `owner_id`/`user_id`. **30 models derived**, zero hand-listing (`--models` prints the set). A new owner-bearing table is auto-covered, per your make-drift-impossible-one-level-up framing.

**D2b (repo-read rule)**: a function that queries an owner model (`select(Model)`/`.query(Model)`) and never references that model's owner column (`Model.owner_id/.user_id/.session_id` — the predicate proxy) flags. `# global-ok: <how>` allowlists per the D4 names-how bar. **Warn-mode baseline: 39 hits**, frozen as ratchet key `unscoped_repo_reads=39` (growth-only, so it CI-gates safely pre-calibration; the rich-mode CI-flip stays gated on you). Documented under-detection, as you predicted: conditional scoping (`if session_id:` — the m-40 shims) passes D2b but violates D1; those are #1252's ratchet, not this one's false-negative.

**Calibration evidence (I read the archetypes; full 39 below).** Three classes:
1. **Fetch-then-check** (verified: `universal_list_repository.get_list_for_read:77`, `get_user_role:476`): requires user_id, fetches by id, verifies `owner_id == user_id or shared_with` on the INSTANCE before returning — cross-user data is never returned, but the scoping is post-fetch Python, invisible to a WHERE-predicate check. **The ruling I need: is this D6-allowlistable with named-how (\"fetch-then-check — ownership/sharing verified on instance before return\"), or is it migrate-to-WHERE debt under D1's \"structural, not conventional\" bar?** My lean: allowlistable for read paths that also evaluate *sharing* semantics (WHERE can't express shared_with-JSON checks cleanly), debt for plain owner-only reads. Your call.
2. **By-id-guarded-upstream** (verified: `document_repository.get_by_base_id:101` — the caller intersects with your named ADR-071 P2 `get_readable_base_ids` set; also the InsightDB/StandupConversationDB `get/update`-by-id family): the m-40 class. My lean: real D1 debt, stays IN the count as the ratchet backlog — annotating these would launder defense-out-of-depth as scoping.
3. **True-unscoped / to-verify** (the KG traversal family `find_neighbors/get_subgraph/find_paths`, `EthicsAuditLogDB.summarize_recent`, the todo/list item-relationship reads, `files.py` download/preview/bulk routes): not yet read; some may be class-1/2 on inspection, the KG ones are likely genuinely unscoped (same family as #1420's read-side).

**Asks**: (a) build-ratify D2b+D3 from the code (you said you'd run the ratchet yourself); (b) the class-1 ruling above; (c) confirm class-2 stays in-count. On your ruling I annotate the allowlisted set with named-how rationales and lower the ceiling in the same commit.

The 39, tagged by my current best-guess class:
- services/api/transparency.py:53 · repo-read ConversationDB (no owner predicate in _require_session_owner_or_admin)
- services/database/repositories.py:663 · repo-read ProjectDB (no owner predicate in get_user_role)
- services/database/repositories.py:708 · repo-read ProjectIntegrationDB (no owner predicate in get_by_project_and_type)
- services/database/repositories.py:717 · repo-read ProjectIntegrationDB (no owner predicate in list_by_project)
- services/database/repositories.py:791 · repo-read RepositoryDB (no owner predicate in list_by_project)
- services/database/repositories.py:1010 · repo-read KnowledgeEdgeDB (no owner predicate in find_neighbors)
- services/database/repositories.py:1040 · repo-read KnowledgeNodeDB (no owner predicate in find_neighbors)
- services/database/repositories.py:1087 · repo-read KnowledgeEdgeDB (no owner predicate in get_subgraph)
- services/database/repositories.py:1124 · repo-read KnowledgeEdgeDB (no owner predicate in find_paths)
- services/database/repositories.py:2141 · repo-read EthicsAuditLogDB (no owner predicate in summarize_recent)
- services/database/repositories.py:2234 · repo-read InsightDB (no owner predicate in get)
- services/database/repositories.py:2486 · repo-read InsightDB (no owner predicate in mark_surfaced)
- services/database/repositories.py:2559 · repo-read StandupConversationDB (no owner predicate in get_by_id)
- services/database/repositories.py:2615 · repo-read StandupConversationDB (no owner predicate in update)
- services/repositories/document_repository.py:101 · repo-read DocumentDB (no owner predicate in get_by_base_id)
- services/repositories/todo_repository.py:98 · repo-read TodoDB (no owner predicate in get_assigned_todos)
- services/repositories/todo_repository.py:135 · repo-read TodoDB (no owner predicate in get_subtodos)
- services/repositories/todo_repository.py:181 · repo-read TodoDB (no owner predicate in get_todos_by_knowledge_node)
- services/repositories/todo_repository.py:193 · repo-read TodoDB (no owner predicate in get_related_todos)
- services/repositories/todo_repository.py:519 · repo-read TodoDB (no owner predicate in get_user_role)
- services/repositories/universal_list_repository.py:77 · repo-read ListDB (no owner predicate in get_list_for_read)
- services/repositories/universal_list_repository.py:155 · repo-read ListDB (no owner predicate in get_shared_lists)
- services/repositories/universal_list_repository.py:476 · repo-read ListDB (no owner predicate in get_user_role)
- services/repositories/universal_list_repository.py:514 · repo-read ListItemDB (no owner predicate in get_item_by_id)
- services/repositories/universal_list_repository.py:521 · repo-read ListItemDB (no owner predicate in get_list_item)
- services/repositories/universal_list_repository.py:532 · repo-read ListItemDB (no owner predicate in get_items_in_list)
- services/repositories/universal_list_repository.py:546 · repo-read ListDB (no owner predicate in get_lists_for_item)
- services/repositories/universal_list_repository.py:586 · repo-read ListItemDB (no owner predicate in remove_item_from_list)
- services/repositories/universal_list_repository.py:625 · repo-read ListItemDB (no owner predicate in delete_items_for_list)
- services/repositories/universal_list_repository.py:637 · repo-read ListItemDB (no owner predicate in delete_items_by_item_id)
- services/todo_service.py:105 · repo-read TodoDB (no owner predicate in complete_todo)
- services/todo_service.py:132 · repo-read TodoDB (no owner predicate in reopen_todo)
- services/todo_service.py:160 · repo-read TodoDB (no owner predicate in set_priority)
- services/todo_service.py:192 · repo-read TodoDB (no owner predicate in get_todos_in_list)
- web/api/routes/files.py:568 · repo-read UploadedFileDB (no owner predicate in download_file)
- web/api/routes/files.py:653 · repo-read UploadedFileDB (no owner predicate in preview_file)
- web/api/routes/files.py:793 · repo-read UploadedFileDB (no owner predicate in download_bulk)
- web/api/routes/files.py:873 · repo-read ArtifactDB (no owner predicate in set_file_tags)
- web/api/routes/files.py:882 · repo-read UploadedFileDB (no owner predicate in set_file_tags)

— Lead
