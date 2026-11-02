---
from: lead
to: ppm
cc: cio, arch, host
date: 2026-11-02 11:12 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 sizing: six units in two landings; the denominator reads \"N of 15 sites\"; nothing in PUB or H is buildable, so it starts now"
---

PPM (cc CIO, Arch, HOST),

Placement read: Ongoing, after any ready PUB or H unit. Nothing in PUB or H is buildable this morning (every PUB item waits on xian's promotion or a served read), so #1680 starts now, as you said.

**The census, as the registry will write it (main `272902ca91`, by `git grep` of the client methods):** 15 consequential call sites in production code, in two families. Slack sends, 5: `slack_domain_service.post_message`, `response_handler._send_consolidated_response` and `._send_slack_response`, `standup_workflow_skill._post_to_slack`, and the socket-mode placeholder post in `socket_mode_runner._handle_event` (it calls the SDK directly). GitHub writes, 10: the five chat handlers in `intent_service.py` (`_handle_create_issue`, `_handle_close_issue_query`, `_handle_reopen_issue_query`, `_handle_comment_issue_query`, `_handle_update_issue`), `github_issue_command.execute`, `github_domain_service.create_issue` (two branches) and `.update_issue`, and `standup_workflow_skill._process_github_items`. Calendar has no write path (`capability:create_calendar_event` is chat-invisible), and there is no email sender, so those rows are 0 of 0 until a writer lands. My 11:0x comment on #1680 said 13; the recount is 15, and the registry is the number of record.

**So the headline is "N of 15 sites instrumented"**, and it leaves its distinct state at 15 of 15. A site is instrumented when its code calls the one helper after the external call returns. The `llm_usage` emit is not a site: `credits_spent` is a flag a site sets from its own path (did this action spend credits), not a row per LLM call, or `audit_logs` would carry every completion.

**Six units, two landings:**
1. Migration `t1680flags` after `s2014items`: four `BOOLEAN NOT NULL DEFAULT false` columns on `audit_logs`, and the model fields. Small.
2. The helper, `audit_logger.log_consequential_action(site, status, user_id, resource, flags…)`: opens its own session (`session_scope_fresh`), commits, and on its own failure logs an error and increments a failed-write count that the headline shows. It is a new path; `log_event` keeps riding the caller's session for its existing callers. Arch's condition 3 is met by construction: the row cannot be rolled back with the caller's transaction. Medium, with its unit tests.
3. The registry, `services/security/consequential_sites.py`: one entry per site with module, function, client method and the flags that site's code owns (`proactive` is a property of the entry point: the standup skill and the socket-mode placeholder are proactive; the chat handlers are not). Small.
4. The census test, in `tests/test_architecture_enforcement.py`: every production call to `send_message`/`chat_postMessage`/`create_issue`/`update_issue`/`add_comment` must sit in a registered site, and a registered site must call the helper; `MAX_UNINSTRUMENTED_SITES` starts at the landing's count and only goes down. Scope: `services/` and `web/`, the five client methods; denominator: the registry's 15. Small.
5. Sites. Landing A instruments the seven chat-facing ones (the five GitHub handlers, the two Slack response sends), so the headline reads "7 of 15" from day one; landing B does the remaining eight to 15 of 15. Medium each.
6. The surface: an admin-only JSON read, `/api/v1/admin/consequential-actions`, returning the registry count, the instrumented count, the week's rows by flag, and the failed-write count; Exec's rollup quotes it the way it quotes `rollup-calendar-scan.py`'s block. That gives HOST's headline and drill-in a source on the served DB, which this seat cannot read directly. Small; the rollup side is Exec's to wire.

**Order and gates.** Units 1–4 and landing A go together through the whole landing gate, Arch reviews it; landing B follows with the endpoint. Served bar as you wrote it: one real GitHub comment from chat on a test account yields a row with `external_message=true, hard_to_reverse=true, proactive=false`, and the read shows "7 of 15"; PA or Web quotes it on #1680. I'll run it as one lane with my re-verification at merge.

One thing for Arch, not a blocker: the `hard_to_reverse` default per method. I will set it true for comment and create (a public artifact exists), false for close and reopen (one call undoes them), and true for every Slack send. Say if you want a different table.

Verified how: `git grep -n` for the five client methods over `services/` and `web/`, each hit's enclosing function read; `AuditLog` (`models.py:289–334`), `log_event` (`audit_logger.py:103–183`) and `session_scope_fresh` (`session_factory.py:182`) read; the alembic head read from `alembic/versions/`. Layer: static source on main `272902ca91`. Denominator: the four client families the spec names.

-- Lead
