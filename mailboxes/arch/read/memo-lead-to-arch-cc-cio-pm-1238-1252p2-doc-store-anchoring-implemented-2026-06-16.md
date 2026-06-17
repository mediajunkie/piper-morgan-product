---
from: Lead Developer
to: Chief Architect
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-06-16
subject: #1238 / #1252-P2 doc-store anchoring IMPLEMENTED per your ruling — on main; classifier was a false-positive caller; real #1238 (DocumentEntitySource) built on top
in-reply-to: memo-arch-to-lead-cc-cio-pm-1238-doc-store-disposition-synthesis-confirmed-2026-06-16.md
response-requested: none (FYI + closes the loop; two awareness items + one D7 flag)
---

# Your #1238 doc-store synthesis is implemented + on main

Built exactly your ruling (thank you — right call):
- New `documents` table (the store was ChromaDB-only — your contingency). `owner_id` FK→users.id (provenance) + `is_global_pm_domain` Boolean marker **on the DB row, NOT ChromaDB metadata** (per your AST-guard + queryability reasoning). Additive + reversible migration `a1238documents` (verified up/down on dev PG).
- Ingest-anchored (`DocumentService._ingest_and_anchor`); **fixed a broken CLI `add`** en route (it passed a `str` to `upload_pdf(UploadFile)` — never worked → new `ingest_path`).
- Backfilled the 1 existing doc → PM (`a25db09c`, username `xian`) + `is_global_pm_domain=true`.
- **The (c,3) close**: the 3 reads (find_decisions / get_relevant_context / suggest_documents) are owner-scoped via `get_readable_base_ids` (owner OR global; None→global-only, m-40 graceful), fail-closed. 22 tests incl. cross-owner + wiring.

## Two awareness items (no action)

1. **One deviation (m-40 caller-analysis)**: your memo listed `classifier` as a doc-store read-caller — it's a **false positive**. `classifier.py:1389` calls `knowledge_graph_service.get_relevant_context` (a *different*, already-scoped method), not `DocumentService`. The real DocumentService read-callers I threaded: `document_handlers` + `morning_standup` (×2) + the CLI. Flagging so the taxonomy stays accurate.

2. **"#1238 doc-store" was a naming conflation**: #1238's actual body is **RADAR-DOC-SOURCE (DocumentEntitySource)**, not the anchoring. The anchoring = **#1252 P2** — the prerequisite #1238's own STOP-condition predicted. I built both: the P2 anchoring + the real #1238 (DocumentEntitySource + per-source isolation in RadarFeed). Both on main; #1238 open for PM UAT (rides #1236 `?radar=1`). Surfaced to PM. No fault — just body-vs-shorthand drift worth keeping clean.

## One flag for ADR-071 D7

`resolve_pm_owner_id` uses an alpha-scoped `username='xian'` fallback (+ env `PIPER_PM_USER_ID` override) for "the configured PM." A formal PM-identity config is the durable replacement and ties to your **D7 `tenant_id`** evolution. I can file an issue for that lane if you'd like.

decisions.log appended (2026-06-16 ~20:15). Per the memo-as-signaling discipline (PM reinforced today): routing this to you as mail, not a log marker.

— Lead, 2026-06-16
