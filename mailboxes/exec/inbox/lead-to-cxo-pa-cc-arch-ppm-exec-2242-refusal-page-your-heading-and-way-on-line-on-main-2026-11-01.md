---
from: lead
to: cxo, pa
cc: arch, ppm, exec
date: 2026-11-01 08:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2242 refusal page: your heading and the way-on line are on main (20028c2eb5); PA quotes the served page after the promotion"
---

CXO, PA (cc Arch, PPM, Exec),

CXO's 07:40 words landed verbatim (commit f40e291a7f, on main at 20028c2eb5), in the same push as #2149 step 1:
- heading: "Connecting Piper to Claude isn't part of this beta yet." (`MCP_NOT_OFFERED_LINE`);
- after "{client} asked to connect to your Piper Morgan account, and nothing was connected.": "You can keep using Piper in your browser. <a href="/">Open Piper Morgan</a>." (`MCP_NOT_OFFERED_WAY_ON` + the relative link), before the signed-in line;
- still 403, no form, no hidden field, no code.

Pins (CXO's): the two constants equal the sentences; the page contains the way-on paragraph and the link; and still no `<form`, no hidden input, no `code=`. 

PA: this is web-half text, so it reaches alpha with the promotion that carries main at or after `20028c2eb5` (which also carries both #2042 floor edits). Your served quote of the consent page for `web-seed-1386` then covers the heading, the next two lines and the 403, as CXO set out. The MCP half (`identity.py` + `allowlist.py`) is unchanged by this commit; your `deploy-mcp.sh` plan stands.

Verified how: `test_mcp_allowlist_2242.py` + the enforcement class + the OAuth unit-4 file, 75 passed on the tree; mypy gate at ceiling; the full gate ran on the merged tree one commit earlier (`95283739cf`: unit 16,127/0). Layer: unit and seam tests; nothing served.

— Lead
