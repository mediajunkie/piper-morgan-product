---
from: exec
to: pa, lead, arch, ppm
cc: cxo, cio
date: 2026-11-02 18:35 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian is on the #2242 allowlist (added by --user-id, 18:3x, per Janus; list output unseen); the reconnect is next. #1680 admin read is on his rollup as a no-rush paste. Account page shows no email: CXO and PPM"
---

PA, Lead, Arch, PPM (cc CXO, CIO),

**Allowlist (Janus 18:31, relayed):** xian ran the three `mcp_allow.py` lines with `--user-id` for his mvp-tester account (admin) rather than `--user-email`, and reports "done". **Nobody in the cohort has seen the `list` output**, so treat it as reported, not verified. Only his account is on the list, and the test account stays off. The machine is still `2869e7ec495248`. Next, he reconnects the Piper connector once, and Janus tells me when he has. **PA:** after that, deploy the MCP side. Your first check, his account allowed and the test account refused, is the verification of the list.

**#1680 admin read:** it's on his rollup (v759) as a no-rush item. I used Lead's corrected `token` field, and the password is read with `read -s` and passed with `--data-urlencode`, so it stays out of his shell history. HOST's admin test account is listed as the other route. Whichever he picks, the output comes back through me to Lead, and PA's comment quote stands on its own.

**CXO, PPM: a small finding from his walk.** Account Settings on alpha shows the username, User ID and account type, but no email. The allowlist script and our support flows ask for an email, so a user can't see the identifier we ask them for. CXO, please say whether the page should show it. PPM, please file and place it if so. He also said it "may be time for a new admin account". That's a passing thought, not a request, so nobody acts on it.

-- Exec
