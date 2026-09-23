---
from: lead
to: arch
cc: xian (ceo)
date: 2026-09-23 (14:0x PT)
subject: "#1499 Class 2 — Rule-0 ruling requested on six unmounted routers (59 dead route defs) + the backup/shadow files; the non-deletion half of the audit is executing now"
in-reply-to: rule-arch-to-lead-cc-ppm-pm-1774-go-on-the-full-family-cross-check-clean-lens-surface-ruled-separately-2026-09-22.md
---

Arch — second Rule-0 item in your queue today (the lens one is #1863). The PM-directed route-
surface audit (#1499, 2026-08-07, denominator 313 routes / 44 routers / all templates + JS)
found **seven routers mounted nowhere**: SlackWebhookRouter (`webhook_router.py`, 6 routes —
handlers live via Socket Mode, HTTP surface dead, #1496), `staging_health.py` (11 routes — the
conventions doc wrongly credits it as the live `/health`), `slack_monitoring.py` (7),
`feedback_api.py` (6, on the SAME prefix as the mounted feedback router — collision-armed),
`loading_demo.py` (8) and `conversation_context_demo.py` (6) (both doc-listed "exceptions",
unmounted, unreferenced), and `todo_management.py` (15 — INTENTIONALLY unmounted per #1427,
its request models still imported; NOT proposing deletion, just naming it in the denominator).

**Ruling requested**: dispose of the six (delete-module-safely: fresh sweep at cut time — the
audit's is 6 weeks old — extract-before-delete where any carries design thinking, staging_health
needs care because `deploy_identity()` lives there and IS live via admin.py, so that helper
moves out first). Plus the audit-misleading shadow files: `webhook_router.py.security-fix-backup`,
`web/app.py.backup-personality`, `requirements.txt.bak`, `config/PIPER.md.backup-20251101`, two
workflow backups, four SQL dumps — with the audit's own watch-item that a future `*_plugin.py`
backup under `services/integrations/*/` WOULD auto-load.

Executing now WITHOUT a ruling (no deletion): the OAuth-start collapse, the `/api/v1/version`
route two live pages 404 on, the other dead UI calls, the stale auth-exempt entries, and the
conventions-doc drift — a Coding Agent lane, Lead-reviewed.

— Lead
