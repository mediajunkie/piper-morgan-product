# #1010 KG-REFACTOR + LEGACY BOUNDARY-ENFORCER — Phase 0 audit

**Issue**: [#1010](https://github.com/mediajunkie/piper-morgan-product/issues/1010) — Refactor knowledge_graph_service.py to domain layer; remove legacy boundary_enforcer.py
**Source**: Architect's Apr 27 review (first pass) + May 10 expansion comment
**Date**: 2026-05-14

---

## Pattern-067 verdict: POSITIVE (body materially stale)

Most of #1010's prescribed work is **already done**. Three of five ACs are no-ops. Two are still real. The body claims an import + 8 call sites that no longer exist. One additional AC (item 6 in the May 10 comment) was shipped yesterday as a side effect of #1019.

### Verification of body claims

| Body claim | Reality (May 14) | Status |
|---|---|---|
| `services/ethics/boundary_enforcer.py` is 441 LOC | **File doesn't exist** — already deleted | ✅ AC3 done |
| `knowledge_graph_service.py:14` imports `from services.ethics.boundary_enforcer import BoundaryEnforcer as EthicsBoundaryEnforcer` | Actual import is `from services.knowledge.boundaries import BoundaryEnforcer as KGBoundaryEnforcer` (different file, different concern — KG-internal not ethics) | ✅ AC1 done (different way) |
| KG service has 8 call sites (lines 60, 62, 121, 123, 297, 300, 379, 381) for `check_harassment_patterns` + `check_inappropriate_content` | Zero matches in KG service for those method names | ✅ AC2 done (different way) |
| `services/api/middleware.py` may have stale `EthicsBoundaryMiddleware` references | Zero hits across services/ web/ tests/ for `EthicsBoundaryMiddleware` or `EthicsBoundaryEnforcer` | ✅ AC4 done (per #990) |
| `boundary_enforcer_refactored.py:343-358` has dead-allocation commented-out adaptive-learn TODO (May 10 comment item 6) | Removed yesterday as side effect of #1019 — the entire adaptive_boundaries scaffolding is gone | ✅ Done as side effect of #1019 |
| `services/database/repositories.py:1008-1031` has placeholder "ready for BoundaryEnforcer integration" methods | **Confirmed real** — 2 methods (`get_nodes_with_privacy_check`, `create_node_with_privacy_check`) exist with `# Future:` placeholder comments and no-op pass-through bodies | ❌ AC5 not done |

### Origin of the stale body

The boundary_enforcer.py deletion + KG refactor likely happened during #992 (ETHICS-ACTIVATE) or one of the related cleanup passes between Apr 27 and today. #1010's body wasn't updated. Same shape as the "body-vs-reality dead-code check" pattern we've been catching repeatedly.

---

## The one real remaining issue: AC5

**Two methods in `services/database/repositories.py`** carry a `# ready for BoundaryEnforcer integration` claim with `# Future:` placeholder comments + no-op pass-through bodies:

### `KnowledgeGraphRepository.get_nodes_with_privacy_check` (lines 1011-1024)

```python
async def get_nodes_with_privacy_check(
    self, session_id: str, privacy_level: str = "standard"
) -> List[domain.KnowledgeNode]:
    """Get nodes with privacy considerations"""
    # This method is ready for BoundaryEnforcer integration
    # For now, it's a simple wrapper around get_nodes_by_session
    nodes = await self.get_nodes_by_session(session_id)

    # Future: Add privacy filtering based on content analysis
    # Future: Integrate with BoundaryEnforcer for content validation
    # Future: Add redaction for sensitive information

    return nodes
```

### `KnowledgeGraphRepository.create_node_with_privacy_check` (lines 1026-1038)

Same shape: takes `privacy_level` param, calls `create_node` unchanged, with `# Future:` comments.

### Why this matters

**The methods ARE called** — `KnowledgeGraphService.get_nodes_with_privacy(include_private=False)` (line 410) and `KnowledgeGraphService.create_node_with_privacy()` (line 424) both delegate to these repository methods.

Callers expecting privacy filtering silently get **unfiltered results**. The API surface implies a behavior the implementation doesn't provide. This is Pattern-067 (body-vs-reality) + Pattern-045 (tests pass, users fail) in the same file.

The `privacy_level` parameter is plumbed through (`"standard"`, "`strict"`, `"public"`) but never consulted. The `include_private=False` boolean in the service-layer call has no real-world effect — the underlying ops return identical data either way.

---

## Disposition options for AC5

### (a) Implement actual privacy filtering

Wire `KnowledgeGraphRepository.*_with_privacy_check` to `boundary_enforcer_refactored.check_inappropriate_content()` + `check_harassment_patterns()`:
- `get`: filter out flagged nodes from the result list (or redact their content fields)
- `create`: reject violations (or redact + persist)
- Honor `privacy_level` somehow ("standard" = no filtering, "strict" = full filter, "public" = redact-then-allow)

**Cost**: ~2 hr. Adds real privacy behavior. New tests needed.

### (b) Remove the misleading surface

Delete the `*_with_privacy_check` repository methods + the `*_with_privacy` service methods. Callers go directly to `get_nodes_by_session` / `create_node`. The "privacy-aware" claim is dropped from the API surface.

**Cost**: ~30 min. Clean removal; matches the discipline of #1019 (Path C — when something doesn't do what it claims, delete it).

### (c) Rename + de-claim

Rename `*_with_privacy_check` → `get_nodes_by_session_filtered` (or similar) and update docstrings to drop the privacy-aware claim. The `Future:` comments become a filed issue (privacy-aware operations as a real feature).

**Cost**: ~45 min. Preserves the call shape but accurately names what the code does.

### Recommendation: **(b) Remove**

Same shape as #1019 Path C: when implementation doesn't match the claim, deletion is cleaner than partial implementation. The methods carry zero real behavior beyond what `get_nodes_by_session` / `create_node` already do. Callers are 2 service-layer methods that also don't add value over direct calls.

If privacy-aware KG operations become a real requirement later, that's a designed feature (under #1016 or its own ticket) — not retrofitted onto these misleading placeholders.

If PM wants to preserve the surface for future implementation, (c) is the next-best.

---

## Suggested gameplan shape (conditional on Path b)

- **Phase 1** (~5 min): worktree setup; grep callers (done — confirmed only 2 service-layer callers + the repo methods themselves)
- **Phase 2** (~20 min): delete `get_nodes_with_privacy_check` + `create_node_with_privacy_check` from `services/database/repositories.py`; delete `get_nodes_with_privacy` + `create_node_with_privacy` from `services/knowledge/knowledge_graph_service.py`; sweep for stragglers
- **Phase 3** (~10 min): grep tests for these method names; remove or rewrite test cases that exercised them
- **Phase 4** (~10 min): merge + close #1010

**Total**: ~45 min. Much smaller than original audit body suggested (which prescribed a multi-file refactor).

---

## Risks

1. **Tests may assert on `get_nodes_with_privacy_check` shape**: Phase 3 sweep catches this; rewrite or delete.
2. **External callers**: if anything outside services/ uses the service-layer `*_with_privacy` methods, breaks. Mitigation: full grep before commit.
3. **Future privacy-aware feature**: removing the placeholders means re-introducing them later requires both the implementation AND the surface. That's the right cost: a real feature should land with real implementation, not aspirational comments.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1010 |
| Pattern-067 check | ✅ POSITIVE — body materially stale; 4 of 5 ACs already done |
| Body-vs-reality | ✅ verified; documented the 4 already-done items + 1 real remaining |
| Existing infra mapped | ✅ KG service + boundary_enforcer_refactored.py + repositories.py |
| Scope questions | ✅ AC5 disposition (a/b/c) |
| Risk assessment | ✅ tests + external callers + future-feature |
| Recommended path | ✅ Path (b) remove, ~45 min |

---

## STOP — awaiting PM disposition on AC5

Most consequential: implement (a) vs. remove (b) vs. rename (c). Recommendation: (b). Everything else in #1010's original AC is already done.

— Lead Developer, 2026-05-14
