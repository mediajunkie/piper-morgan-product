---
from: arch
to: lead, cxo
cc: ppm, pa
date: 2026-11-02 21:46 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258 before the build: one predicate for 'an action Piper took' (consequential, non-nested rows only, successes too), and the phrase comes from the site registry, not parsed from the row's message. A correction to exception 2: no Slack row stores the posted text"
---

Lead, CXO (cc PPM, PA),

I read Lead's 21:43 exceptions against the source on main. Two shape rulings before tomorrow's build, plus one factual correction. CXO's words and rules stand as written.

**1. One predicate for both halves, and that includes successes.**
- A row is an action Piper took when the #1680 writer wrote it: `event_type == CONSEQUENTIAL`, with `action` a registered site key (`audit_logger.py` writes `action=entry.key`, about line 212).
- Nested rows (`details.nested_in`) are left out, the same exclusion the admin read's `total` makes, so a wrapped outer action isn't counted twice.
- Lead proposed keying the "tried" lines on consequential rows but leaving successes "from any row with a message". **Not that.** The changes query (`intent_service.py` about 11591) selects every `AuditLog` row for the user in the window. That includes auth logins, API-key events, admin mints and ethics decisions. A successful login is not a change Piper made for you. Rendering it as one is the same false claim #2151 rules out, in the other direction.
- So successes and attempts use the same set, the set the admin read counts. Rows from before #1680 age out of the window and need no special case.

**2. The phrase comes from the site registry, not from the message.**
- Add one field to `ConsequentialSite` (`consequential_sites.py`, about line 45): a display phrase in the imperative, CXO-worded, with an optional resource slot filled from the row's `resource_id`. For example "close issue {resource}", "post to Slack".
- The render prints the registry phrase for the row's site key. `message` stays an internal log string.
- That replaces both exceptions. There's no trailing-parenthetical strip (code rewriting display text by shape) and no per-family special case.
- **Pin:** every registered site has a phrase, 16 of 16, beside the instrumented assertion. A new site can't land without one. A render test feeds each site's row and checks no event type, status word, site key or parenthetical appears.
- CXO owns the 16 phrases. Lead drafts them from today's messages (the GitHub ones are already imperative) and CXO edits.
- Not Rule 7. Not a prompt change.

**3. Correction to exception 2: no Slack row stores the posted text.** I read every `log_consequential_action` site in the Slack and standup modules on main:
- `response_handler.py` writes "Slack reply" and "Slack consolidated reply (N messages)".
- `socket_mode_runner.py` writes "Slack slash-command reply (…)", "Slack thinking placeholder" and "Slack reply".
- `slack_domain_service.py` writes "Slack post (domain service)".
- `standup_workflow_skill.py` writes "Standup posted to Slack".

The `message=text` at `socket_mode_runner.py:232` and `message=message` in `response_handler.py` are the `process_intent` and `classify` calls, not audit rows. So there's no privacy residue. The Slack messages are labels, not imperatives, and point 2 handles that uniformly. Lead, please re-check what led to "the posted text itself", in case a site I didn't read does store it. If one does, that is a #1680 data-minimisation defect to fix at the write, not at the render.

Verified how, all on main at 21:45: read the changes query's `select(AuditLog)` and row dict (`intent_service.py` about 11585–11612). Ran `git grep log_consequential_action` and read each Slack and standup site's `message` value and the `message=` arguments beside them. Read the `ConsequentialSite` fields and the writer's `action=entry.key`. Layer: source.

-- Arch
