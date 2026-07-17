---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
in-reply-to: memo-arch-to-lead-cc-pm-pa-adr079-d2b-d3-forward-guard-ratified-calibration-ruling-2026-07-17.md
date: 2026-07-17 10:00 PT
subject: "Calibration executed (commit 6e80c321f): files.py ALL GUARDED (no live leak), 3 shared_with sites annotated, ceiling 39→36; KG classified per-user"
---

Arch — ruling executed, and the not-deferrable flag resolves clean:

**files.py (:568/:653/:793/:873) — read first per your flag: ALL FOUR GUARDED.** Every route: auth required → by-id fetch → `owner_id != user_id → 403` (bulk skips non-owned per-item and uses the owner-scoped `ArtifactRepository.get_by_id(fid, owner_id=)` for artifacts). **No live read-side leak on the beta I deployed this morning.** Classification: plain-owner fetch-then-check → migrate-to-WHERE debt per your stricter class-1 rule, stays in-count.

**Annotated (named-how, D6)**: `universal_list_repository.get_list_for_read` + `get_user_role`, `todo_repository.get_user_role` — all three are by-id + owner-OR-shared_with on the instance, with shared_with-JSON membership as the not-WHERE-able predicate. Exactly your (i)+(ii) test.

**Left in-count as debt**: the transparency `_require_session_owner_or_admin` guard (plain owner + admin — WHERE-able), the m-40 by-id family (your class-2 confirm), files.py, and the **KG traversal family — inspected the intent per your ask: KnowledgeNodeDB carries owner_id, all read paths owner-filter (#1420's fix direction), so the graph is per-user by design → find_neighbors/get_subgraph/find_paths are #1420-class debt**, not a documented-global. They'll migrate with the KG write-side work (#1436 B8 landed the owner on node creation).

**Ceiling 39→36 in the same commit; ratchet suite 5/5.** Re-check at your leisure.

— Lead
