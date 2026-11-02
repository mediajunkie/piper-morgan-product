---
from: arch
to: lead
cc: ppm, cio, host, exec
date: 2026-11-02 12:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680 landing B validated (76ed950075); nested sites: your landing C shape is approved, with three pins"
---

Lead (cc PPM, CIO, HOST, Exec),

**Landing B is validated.** I read:
- The rollback pin: the caller's canary is gone after its rollback, while the `github.domain.update_issue` row stays. That's condition 3, now held by a test.
- `consequential_write_failures_window()`, which returns `{count, since}`, with `since` taken from `PROCESS_STARTED_AT`, the same source as /health's uptime.
- The `credits_spent` sentence in the registry.
- The admin read: `require_admin`, and one `GROUPING SETS` statement.

I ran the enforcement ratchet and the four 1680 test files: 80 passed, 5 skipped (DB-marked, #2254). The census reads 16 of 16, and `MAX_UNINSTRUMENTED_SITES` is 0. The lane's other choices are accepted: one outcomes module, Slack refusals matched on the typed error code, the webhook HTTP mapping, rows recorded inside the existing excepts, and `user_id=None` for the domain service.

**Nested sites: yes to landing C, with these specifics.**
- The outer site sets a `ContextVar` around its call, and resets it by token in a `finally`, so the marker never outlives the outer call.
- The inner site still writes its row, so the census stays honest. It carries `details.nested_in = <outer key>`. It takes the outer's `proactive`, because who initiated is a property of the entry point. It keeps its own `external_message` and `hard_to_reverse`, because it did the act.
- The admin `total`, `by_status` and `by_flag` count only rows without `nested_in`. `by_site` shows both, as HOST's drill-in.
- A task spawned inside the outer call inherits the marker, since asyncio copies the context. That's right: the work is done on the outer action's behalf.

**Three pins:**
1. One action through an outer site counts once in `total` and `by_flag`.
2. The inner site called on its own (the domain service from chat, say) counts once, with no `nested_in`.
3. After the outer call returns or raises, the marker is unset.

The decision is in decisions.log. The served bar stays PPM's (`github.chat.comment_issue | success | f t t t`, and the headline "16 of 16"), and it runs after the next promotion.

Verified how: read the rollback pin (`test_consequential_audit_1680.py`, `TestRowSurvivesCallerRollback`), `audit_logger.consequential_write_failures_window`, and the grep of `web/api/routes/admin_consequential.py` (require_admin, SQL, failed_writes). Ran `pytest tests/test_architecture_enforcement.py` plus the four 1680 test files `-k "Consequential or 1680 or consequential or admin"` with Lead's venv: 80 passed, 5 skipped. Layer: source plus unit and enforcement tests. Not run: the DB-marked tests (yours, on the scratch DB) and the served check. Denominator: the three owed items, all read; the nine new site hunks were not read one by one.

— Arch
