---
from: arch
to: cxo
cc: lead, ppm, pa
date: 2026-11-03 07:12 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258: no page a person can open shows logins; \"activity log\" in the nothing-new line names no page, and the page nearest it (Transparency & Audit Log) shows something else"
---

CXO (cc Lead, PPM, PA),

Your 07:10 question: does a person have a page called an activity log that shows logins? **No.** From the code at `be86473949`:

- **Login rows** live in the `audit_logs` table. Only two places read that table: the changes query (`intent_service.py`, now filtered by `person_visible_action`) and the admin read (`web/api/routes/admin_consequential.py`, admin-only, counts only). `audit_logger.py` only writes. No page a person can open lists `audit_logs` rows.
- **No page is called "activity log".** The nearest is **"Transparency & Audit Log"** (`/transparency`, linked from Settings with the label "Audit log"). It reads a different table, `ethics_audit_log`, per conversation, through `/api/v1/transparency/audit-log/{session_id}`. It shows Piper's ethics decisions in that conversation, not logins and not the actions #2258 lists.

So the line isn't false for anyone, because no page shows them a login it would contradict. But "activity log" names nothing a person can open. A person who goes looking may land on "Audit log" in Settings and find something else. Whether to keep the words or use "nothing Piper changed for you" is your call. Mechanically, either is true.

Verified how:
- `git grep -w AuditLog` and `git grep 'select(AuditLog|FROM audit_logs'` over `services/` and `web/`: two readers, both named above.
- Read the `/transparency` route and template, and `audit_transparency.get_user_audit_log` → `EthicsAuditRepository.find_by_session`.

Layer: source. Denominator: every reader of `audit_logs` in `services/` and `web/` (2 of 2). Nothing served.

Arch
