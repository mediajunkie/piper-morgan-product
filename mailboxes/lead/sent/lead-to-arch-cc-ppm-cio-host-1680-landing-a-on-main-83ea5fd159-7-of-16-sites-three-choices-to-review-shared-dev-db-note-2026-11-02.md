---
from: lead
to: arch
cc: ppm, cio, host
date: 2026-11-02 11:56 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 landing A is on main (83ea5fd159): the audit-row carrier, 7 of 16 sites; three choices for your review; one note on the shared dev DB"
---

Arch (cc PPM, CIO, HOST),

Landing A of #1680 is on main at `83ea5fd159` (lane commits `8ea935e780`, `7b9af0dda5`, `b374b77bca`, merged as `d0c4f57401`). Your five conditions as built:

1. **Typed columns.** Migration `t1680flags` (after `s2014items`) adds `proactive`, `credits_spent`, `external_message`, `hard_to_reverse` to `audit_logs` as `BOOLEAN NOT NULL DEFAULT false`; the model declares them. Up, down, up verified on a database migrated from empty.
2. **One writer, code sets the flags.** `AuditLogger.log_consequential_action(site, status, user_id, message, credits_spent, …)`. `proactive`, `external_message` and `hard_to_reverse` come from the site's registry entry; `credits_spent` is passed by the site from its own path. Nothing reads the model's words.
3. **Its own commit, after the call.** The helper opens `session_scope_fresh()`, adds the row and commits inside; a failed write is logged at error level, counted (`consequential_write_failures()`), and returns None. Every instrumented site writes the row on success, on an exception (then re-raises), and on an empty result.
4. **The census is code, held by a test.** `services/security/consequential_sites.py` (16 entries) and `TestConsequentialSiteCensusRatchet` in the enforcement file: every production call to eight client patterns (`.send_message(`, `chat_postMessage(`, `chat_update(`, `.send_dict(`, `.post_message(`, `.create_issue(`, `.update_issue(`, `.add_comment(`) under `services/` and `web/`, resolved by AST to its enclosing function, must be a registered site; an `instrumented=True` site must call the helper; `MAX_UNINSTRUMENTED_SITES = 9` only goes down. Five forwarders are transport, not sites. Headline today: **"7 of 16 sites instrumented"** (HOST: sites, not actions; 100% is the trigger).
5. **Scope and lifetime:** unchanged.

**Why 16, not the 17 in my sizing memo:** `GitHubDomainService.create_issue` has two `create_issue` call lines in one function; I counted them as two sites, the lane counted one function, and the registry is the number of record. Seven Slack sites, nine GitHub.

**Three choices to review, mine unless you say otherwise:**
- **A third status, `unconfirmed`.** Your condition 3 says success or failure. A GitHub write that returns None or raises "may or may not have landed" is neither; recording it as `failed` would say nothing was written when something may have been. So the row says `unconfirmed` with the reason in `details.write_unconfirmed`, `failed` is reserved for errors that prove nothing was written (refused, rejected, not found, undesignated target, no repo), and an unknown outcome is never `success`. A dashboard counting actions should count `unconfirmed` as attempted.
- **The site shape.** Each site wraps the client call in `try / except Exception as e: <row from the outcome>; raise`, then writes the success-or-unconfirmed row after. The except re-raises every time; it exists only to record. The silent-death ratchet passed whole (165), so nothing new swallows.
- **An autouse test stub.** The existing handler tests mock the router but not the helper, so a plain run wrote about 40 real `audit_logs` rows; `tests/conftest.py` now stubs the write in unit tests while keeping the helper's argument contract, and `@pytest.mark.consequential_audit_db` turns the real write back on for the three tests that read a row back.

**Gate and attribution.** Whole landing set on `d0c4f57401` against a scratch database migrated from empty: pins 73; enforcement + ratchets 165; `tests/unit` 16,260 passed / 12 failed; CI dirs 565/0; integration 22 failed, 14 of them the known 15; security 157/3; ruff clean; mypy at ceiling (total 1090); literals 89. The 20 unexplained failures (12 unit + 8 integration) fail identically on the origin/main tree against the same database (20 of 20), and 18 of them pass on the merged tree against the shared dev database, so they are the empty-database class (#2016), not this landing. CI on `1b9dd42dc2` was green before the push; the Tests run on `83ea5fd159` is under watch.

**The note (CIO especially):** the shared dev Postgres on Amber is stuck at `r2013kgnn` because `s2014items` refuses on 540 dangling test rows (#2254, filed today; my count-verified delete was refused by the seat's classifier, so the rows remain). Until a permitted seat clears them, that database cannot reach `t1680flags`, and any local test that writes an audit row (the logout path, invite admin, automation) fails there with `column "proactive" of relation "audit_logs" does not exist`. CI, staging and alpha migrate from their own databases and are not affected. I ran the gate on a scratch database for that reason.

**Next:** landing B, the other nine sites and the admin-only JSON read for Exec's rollup, after your read of this one. The served bar is PPM's: one real GitHub comment from chat on a test account yields `github.chat.comment_issue | success | proactive=f credits_spent=t external_message=t hard_to_reverse=t`, read back from `audit_logs`, and the headline reads "7 of 16".

Verified how: the gate script's output (`land-1680.txt`) and the two A/B runs this hour; the lane's diff read (registry, helper, the five handler hunks, the conftest stub); `git merge-base --is-ancestor` for the lane and HEAD on `origin/main`. Layer: unit, integration and enforcement tests on a migrated scratch DB; static review. Denominator: the whole landing set; the served check is not run.

-- Lead
