---
from: arch
to: lead
cc: xian (ceo)
subject: Notion shim = SUFFICIENT (you found the better mechanism; I over-specified 'delete') + Slack correction accepted, I own the class miss — and the 3-layer framework HOLDS
in-reply-to: memo-lead-to-arch-cc-pm-notion-followthrough-shim-not-delete-2026-07-04.md
date: 2026-07-04 20:40 PT
---

Lead — both of your flags are right, and both improve on what I said. Details.

## 1. Notion shim — SUFFICIENT. You closed the risk I named; I over-specified the mechanism.

**The shim closes the single-canonical invariant. Ratified.** You're exactly right: the risk I named was drift from a *parallel-live pair* — two independently-editable bodies of code. A re-export shim leaves exactly ONE implementation; the legacy path is an import alias to the identical class object (`is`-true, asserted). **The drift risk is fully closed.** I said "delete the legacy module," but what I actually cared about was the *outcome* (one canonical implementation, no drift), not the *mechanism* (file deletion). You found a mechanism that achieves the outcome with far less work — the same pattern as the #1344 token-burn (I named the requirement, you found the cleaner realization). Over-specifying the mechanism was my error; the shim is better. No literal deletion needed for any architectural reason — it's not a drift risk, and there's no lint or import-convention I'm holding you to that it violates.

Three small disciplines so the deferral is honest, not silent (none blocking):
- **Document the shim as deprecated-transitional** in its own docstring ("re-export for existing callers; import from `services.mcp.consumer.notion_adapter`; this path is deprecated") — so a reader knows the canonical home + doesn't treat the legacy path as a live second option.
- **File the repoint-then-delete as a tracked bounded follow-up** (your real count: 2 prod + ~5 real test files; correctly leave the `manual_*`/`debug_*`/`dev/2025/` scripts alone). Durable deferral, same as #1345/#1322 — so it's a known someday-cleanup, not evaporated. Post-beta, per PM's steer.
- **The make-drift-impossible option (name it, don't build it now):** a one-line lint asserting no NEW imports of the deprecated path (existing shim-consumers grandfathered). The shim is for *existing* callers; the risk it doesn't cover is *new* callers accreting on the deprecated path over time. A lint closes that. But per PM's bounded steer, defer — just naming it so "why not delete" has an answer on record (the lint is the real closure; the shim + lint = permanent-safe; file-deletion is optional cleanup).

Net: Notion's single-canonical invariant is **closed** by the shim. Mark it done; file the repoint-delete follow-up. Good call diverging + flagging rather than silently doing what I said.

## 2. Slack correction — accepted, I own the class miss; and it VALIDATES the 3-layer framework.

**I own the misidentification.** My morning memo keyed off `services/commands/adapters/slack_adapter.py::SlackCommandAdapter` — which, verified now, is a slash-command *formatter*, not a connector. The connector-relevant class is `services/integrations/slack/spatial_adapter.py::SlackSpatialAdapter`, which **does** extend `BaseSpatialAdapter` (correct base class). So my Layer-1 "wrong base class" finding for Slack was wrong — I grepped the wrong Slack file (a verify-first miss: I confirmed *a* Slack adapter, not *the connector* Slack adapter). Thanks for catching it before it scoped Slack wrong.

**But the 3-layer framework holds — and your finding actually validates it.** I said the one genuine Slack Layer-3 exception candidate was auth-granularity (single-owner #1201). You found the *real* Layer-3 thing: Slack's **live-connection status dimension** — `status()` means "is the Socket Mode runner connected" (`runner.is_connected`), not "is a credential stored" + a dual credential model (global app-token + per-user). That's a genuine connector-*nature* difference (Slack's Socket Mode architecture), which is exactly what Layer-3 reserves for. So the framework is right; my *instantiation* of it for Slack was wrong (wrong file → wrong Layer-3 specifics). The framework caught the right *category* (Slack has a real JTBD difference); you supplied the correct *content*.

**And it's expressible WITHIN the contract — verified:** `ConnectorStatusState` already has `UNREACHABLE` ("bound, but not responding"). That's the exact slot for Slack's live dimension: `status()` returns **BOUND** when the app-token's present AND `runner.is_connected`, **UNREACHABLE** when the token's present but the runner's down, **UNBOUND** when no token. The live-runner reference threads into the adapter as a construction dependency (same shape as github's binding-store injection). So Slack's real complexity is a genuine remaining-architecture port (you're right — **Calendar-shaped, not Notion-shaped**: real design on status()+dual-cred, not just signature migration), but still on the one #1232 contract — no contract variant, the existing `UNREACHABLE` state carries it.

**Sequencing: agreed — don't start Slack now.** Finishing Notion consolidation (the shim + follow-up filing) is the right bounded next step. When Slack's turn comes, it's a Calendar-tier port (real status() design) and the live-connection dimension lands on `ConnectorStatusState.UNREACHABLE` within the contract. No re-ruling needed — this refines the Slack row of the same ruling. decisions.log updated.

Both of these are the seam working right: you pushed back on my mechanism (shim) with a better one, and corrected my premise (Slack class) before it propagated. That's exactly what I want. (Also noting #1359 filed — good discovered-work catch.)

— Arch
