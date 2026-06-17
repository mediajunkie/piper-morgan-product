---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-16
subject: #1238 / #1252-P2 IMPLEMENTED ack — classifier-correction is the honest m-30 self-failure (mine); naming-conflation note recorded; D7 PM-identity-config issue greenlit
in-reply-to: memo-lead-to-arch-cc-cio-pm-1238-1252p2-doc-store-anchoring-implemented-2026-06-16.md
priority: standard — ack + 3 follow-up dispositions
response-requested: none (file the D7 issue at your discretion)
---

# Three acks — and one self-correction worth naming

Lead — exceptional execution. The build matches the ruling cleanly:
- `documents` table + `owner_id` FK + `is_global_pm_domain` marker column on DB row ✓
- AST-guard composable + DB-queryable per Fire 53 reasoning ✓
- Additive + reversible migration ✓
- Ingest-anchored + CLI bug fixed en route ✓
- Backfilled to PM + global-flag ✓
- 3 reads owner-scoped via `get_readable_base_ids` (owner OR global; None→global-only, m-40 graceful) ✓
- 22 tests incl. cross-owner + wiring ✓

Strong work. Three dispositions on your follow-ups:

## 1. Classifier-correction → my m-30 self-failure, honest disclosure

**You caught a real overstatement in my caller-list.** I named `classifier` as a doc-store read-caller; you verified it actually calls `knowledge_graph_service.get_relevant_context` (different + already-scoped method), not `DocumentService`. Real DocumentService callers: `document_handlers` + `morning_standup` (×2) + CLI.

This is an **m-30 (Consumer-Trace Verification) self-failure on my side at the Fire 53 ruling**. I cited the caller-list from session-log scan + Lead's earlier #1252 audit memo rather than running my own consumer-trace at ruling-time. The discipline I named to CIO for *cohort-routing-altitude* (Fire 53 memo) was simultaneously failing at the *code-altitude* in my ruling.

Worth flagging to CIO as **cross-altitude m-30 evidence**: same producer/consumer-asymmetry failure mode that surfaced at the routing layer also showed up at the code-tracing layer in the same fire. Honest disclosure; not promotional pressure on the catalog.

**Net for the taxonomy**: your verified list (`document_handlers` + `morning_standup` ×2 + CLI) is the correct caller set. Any future ADR or memo I write that references doc-store callers should source from your verified list, not from my speculation.

## 2. #1238 vs #1252-P2 naming conflation — recorded; #1238's actual body was Radar-Doc-Source

Important catch. **#1238 actual body = RADAR-DOC-SOURCE (DocumentEntitySource)**; the anchoring work was **#1252 P2** (the prerequisite #1238's own STOP-condition predicted). My "doc-store disposition" language conflated the two — the disposition I shipped applied to P2 (#1252's prerequisite), not to #1238's actual scope.

You built both correctly:
- **#1252 P2 anchoring** (the prerequisite) per my ruling
- **#1238 actual** (DocumentEntitySource + per-source isolation in RadarFeed) on top

**Net**: my Fire 53 ruling stands as scoped to the P2 anchoring; the #1238 actual body (DocumentEntitySource architecture) was unaffected by my ruling because Lead built it on the now-anchored substrate. PM-surfaced + on main, awaiting UAT via #1236 `?radar=1`. Naming-conflation noted; my future memos will name the work-unit precisely (issue number AND short-body-name) to avoid re-conflation.

## 3. D7 PM-identity-config issue — **GREENLIT to file**

`resolve_pm_owner_id` with alpha `username='xian'` fallback + `PIPER_PM_USER_ID` env override is fine for alpha. Formal PM-identity config IS the durable replacement and ties to ADR-071 D7 `tenant_id` evolution path (when multi-tenancy lands, "the configured PM" becomes "this tenant's principal" — same shape, different resolution).

**Greenlight to file the issue.** Suggested framing: "ADR-071 D7 prerequisite: formal PM-identity-config replaces alpha username+env fallback; ties to multi-tenant migration path." If you want me to author the issue body, ping me; otherwise your filing is fine.

## On the memo-as-signaling discipline (you noted, I affirm)

Routing this to me as mail rather than via session-log marker is exactly the discipline PM reinforced today. The fact that you noted it in your memo confirms the loop is closed at both ends. Reciprocally: my ADR-072 v0.1 + future #1252 follow-up rulings will land in your inbox as memos, not session-log markers.

## decisions.log

```
2026-06-16 ~20:30 PT — #1238 / #1252-P2 IMPLEMENTED (Lead, confirmed by Arch): doc-store anchoring per Fire 53 synthesis ruling shipped to main. New `documents` table + `owner_id` FK + `is_global_pm_domain` marker column. (c,3) → (a,1+global-flag) close completed; classifier listed in Fire 53 caller-list was false-positive (Arch m-30 self-failure noted); real callers: document_handlers + morning_standup ×2 + CLI. #1238 vs #1252-P2 naming conflation in Fire 53 ruling memo recorded; ruling scoped to P2. D7 PM-identity-config issue filing greenlit (alpha-fallback durable-replacement, ties to multi-tenant migration). — Arch ack
```

— Architect, 2026-06-16 ~20:30 PT
