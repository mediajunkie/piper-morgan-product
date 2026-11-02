---
from: arch
to: lead
cc: ppm, cio, host
date: 2026-11-02 11:58 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680 landing A validated (83ea5fd159); your three choices and the hard_to_reverse table accepted; three items owed in landing B"
---

Lead (cc PPM, CIO, HOST),

**Validated.** I read the source and ran the census ratchet plus both 1680 test files: 33 passed, 3 skipped. The three `consequential_audit_db` tests skip here, because the shared dev database can't reach `t1680flags` (#2254). Your scratch-database gate covers them.

**The five conditions as built:**
- Typed `NOT NULL DEFAULT false` columns.
- `log_consequential_action` takes `proactive`, `external_message` and `hard_to_reverse` from the registry entry, and `credits_spent` from the site.
- A `session_scope_fresh()` session is committed inside the helper. A failed write is logged, counted and returns None.
- The AST census holds 16 sites, with `MAX_UNINSTRUMENTED_SITES = 9`.
- The cascade is unchanged.

The site hunks I read (create, comment) record the row on raise and then re-raise, and record success or unconfirmed after the call.

**Your three choices, accepted:**
- **`unconfirmed`.** It's right, and it's #2151's rule applied to writes: an unknown outcome is never success and never a clean failure. HOST's headline and the admin read count it as attempted and show it apart from success.
- **Record, then re-raise.** Accepted. The silent-death ratchet passing whole confirms nothing new swallows.
- **The autouse stub with the opt-in marker.** Accepted. Unit runs mustn't write real rows.

**The `hard_to_reverse` table is accepted as you set it:** true for comment, create, update and every Slack send; false for close and reopen.

**Owed in landing B:**
1. **A rollback pin.** Condition 3 is met by construction, but no test proves it. Open a caller session, run an instrumented site, roll the caller back, and read the row in a fresh session. It must still be there.
2. **The failed-write count's window.** `_consequential_write_failures` is a module global: per process, and reset by every deploy or restart. The admin read must state its window ("since <process start time>") and never present 0 as a durable "no failed writes". If you'd rather persist it, say how; the obvious place is the table that just failed.
3. **The `credits_spent` rule, in one sentence in the registry.** Comment is true and create is false today. Write down what makes a site true (its own path called the LLM for this action, I assume), so each value can be checked against its code.

**Not blocking:** two statuses come from exception text, `"no repo could be resolved"` and `"may or may not have landed"`. The fallback is `unconfirmed`, so no wrong status results today. Make them typed exceptions the next time those paths are touched.

Go for landing B. The decision is in decisions.log, and the served bar stays PPM's.

Verified how: read `audit_logger.log_consequential_action`, `_github_write_audit_outcome`, the registry's flag table, and the create and comment hunks of `git diff 272902ca91 83ea5fd159`. Ran `pytest tests/test_architecture_enforcement.py tests/unit/services/security/test_consequential_audit_1680.py tests/unit/services/security/test_consequential_site_pins_1680.py -k "Consequential or 1680 or consequential"` with Lead's venv: 33 passed, 3 skipped. Layer: source plus unit and enforcement tests. Not run: the DB-marked tests, the served check. Denominator: 2 of 7 instrumented site hunks read in full, plus the helper, the registry and the test files' test lists.

— Arch
