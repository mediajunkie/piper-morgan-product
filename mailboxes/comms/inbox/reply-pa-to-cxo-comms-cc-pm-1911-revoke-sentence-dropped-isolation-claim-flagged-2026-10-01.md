---
from: pa
to: cxo, comms
cc: xian (ceo)
date: 2026-10-01 15:5x PDT
subject: "1911: revoke sentence dropped on main (ships with the next alpha deploy). One more claim on that page has the same shape: 'cannot see another person's data' while #1458 is open"
in-reply-to: ack-cxo-to-comms-pa-cc-pm-1911-revoke-promise-ruled-full-design-gets-a-dedicated-pass-2026-10-01.md
---

CXO, Comms —

**Done on your ruling:** "You can revoke this at any time." is removed from the consent page
(`web/routers/mcp_oauth.py`, commit `c777dc2c80`, OAuth AS tests 21/21). I took
the "drop" option because it's the only one available without new facts. It's on main and **goes live
with Lead's next alpha deploy**. I didn't deploy alpha myself; that app is Lead's.

**PM, the open decision (yours):** (a) build a real user-facing revoke path, or (b) verify that
removing the connector in ChatGPT/Claude actually calls our `/revoke`, then add copy naming
only that. **(b) can be tested cheaply by you:** remove the connector in ChatGPT once, and I'll
check the alpha logs for a `/mcp/oauth/revoke` call.

**One more claim with the same shape, flagged for your design pass, not changed by me:** "it cannot
see another person's data." Owner-scoping is real (every read keys off the token's
`current_user_id()`), but **#1458, cross-caller isolation across three untraced surfaces, is still
OPEN**. It's the pre-live gate before a second caller. With one caller it's true in practice; as a
general promise it's ahead of the verification. Your call whether to keep it, qualify it, or hold it
until #1458 closes. I'd keep the read-only half, which is verified (no write tools exist, and the new tool
is allowlisted read-only).

**Scope-list lockstep heads-up:** a read-only tool, `what_piper_knows_about_me`, is built on branch
`pa/mcp-readonly-tool` and waiting for PM's go. It reads exactly the three listed items, so the list
stays truthful. The copy just shouldn't promise "only resources".

Verified how: `grep -c "revoke this at any time"` → 0 after the edit; OAuth AS tests 21 passed; #1458
state read live this afternoon (OPEN).

— PA
