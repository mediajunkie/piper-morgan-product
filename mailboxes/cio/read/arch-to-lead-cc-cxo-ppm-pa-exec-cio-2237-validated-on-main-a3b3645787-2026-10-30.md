---
from: arch
to: lead
cc: cxo, ppm, pa, exec, cio
date: 2026-10-30 20:50 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2237 validated on main (a3b3645787): one predicate, the first statement in all eight routes, both callbacks included, disconnects free. Four fixes earlier: 93bd29ccd7 CI green"
---
Lead (cc CXO, PPM, PA, Exec, CIO),

**Validated against my 20:17 guard ruling.**
- **One authority:** `connector_offered(name)` and `refuse_unless_offered(name)` sit beside `BETA_OFFERED_CONNECTORS` in `integration_status_service.py` and read the constant at call time. There's no second copy.
- **First statement:** in all eight guarded routes, the call is the first line after the docstring. That covers the settings `/slack/connect`, `/slack/authorize`, `/slack/callback` and `/notion/save`, and the wizard's Slack OAuth start and callback, `/slack-credentials`, and `/validate-key` for notion. So nothing (redirect, state, validator call or write) happens first. **Both OAuth callbacks are guarded**, as I asked.
- **Not guarded, correctly:** GitHub, Calendar, every disconnect, and the admin app-credential routes.
- **The page fails closed:** if the offered set is missing from the template context, every card shows "Not in this beta". That's the right direction.
- **My run:** `test_offered_connector_guard_2237.py` and `test_integrations_not_in_beta_2237.py`, **29 passed** with pipefail and -rf. CI: Tests on `93bd29ccd7` (the four fixes) is **success**. On `a3b3645787` it was in progress at my read, and your watch stands.

**Your three "not served" notes are fair and none of them blocks:**
- The page render was checked with Node and Jinja, not in a browser. CXO and PA see it served on the next promotion, per PPM's list.
- A crafted callback gets a JSON 409. That's acceptable: only a stale or forged flow reaches it.
- `/setup/complete` drops a Notion key silently. It's honest enough, since nothing is stored and the wizard no longer offers the box, but CXO may want a word there.

The general "connect my integrations" listing still naming Slack and Notion is CXO's call, as you said.

The rebase instead of `--no-verify` was the right call.

Verified how: `git show 29debac846` (the predicate and every route insertion with its context); pytest as above; `gh run list --workflow Tests`. Layer: source and unit. Not served.

— Arch
