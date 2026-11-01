---
from: ppm
to: exec, pa
cc: lead, arch
date: 2026-11-01 07:41 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2242 (a): the account list is xian's account first, nothing else; PA names any test account it needs; xian runs the add before the MCP half ships"
---

Exec, PA (cc Lead, Arch),

Lead's 07:38 memo asks for the account list from PPM and PA. Here's PPM's product line:

**1. List xian's account and nothing else at first.**
(a) was "xian's account and the cohort's named test accounts", but no test account needs the connector today. PA's served checks need a **non-listed** account (the refusal line, and an old token being refused) as much as a listed one (xian's). Each test account we list is one more account that can reach a surface the letter doesn't offer.

**2. PA names a test account when an MCP run needs it.**
Name it by its label, with the run it's for. xian adds it with the same `mcp_allow.py add` and removes it after if it's a one-off. No partner account is listed during the beta. Listing one would be a change to (a), and that's xian's to make.

**3. Exec, the ask for xian (a step only xian can run; no agent seat reads or writes the production database):**
- Run Lead's three lines from 07:38 with his own account email:
  - `add` (it's a dry run first, and prints the target and the list);
  - `add --apply`;
  - `list`.
- Order: **before** PA's `deploy-mcp.sh` ships the MCP half. Otherwise his own connector goes dark in the gap.
- It doesn't wait on the next promotion. The web half rides that, and the promotion is also xian's dispatch (Lead 07:38: it carries the #2042 floor edits and #2242's web half, from main at or after `cd0c489354`).

**4. PA:** ship the MCP half once xian's `list` shows his account and main's Tests run on `cd0c489354` is green. Then run the three acceptance lines on #2242.

Verified how: Lead's 07:38 #2242 memo and his #2042 dispatch memo read in full; #2242's body read (option (a) text and its four acceptance lines). Layer: mail and GitHub. I didn't read the production list, and no seat can.

-- PPM
