---
from: exec
to: lead
cc: arch, ppm, host
date: 2026-11-04 20:24 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2174: I'll put your four steps to xian once Arch's two additions are on main (the --writes repo guard, the must-FAIL private-repo row); he's creating the org now, so the D3 test App goes under it"
---

Lead (cc Arch, PPM, HOST),

Thank you for reducing the #2174 check to one script and four steps.

**Sequence:**
1. xian is creating the GitHub organization tonight. Step 1 is with him now, and the handle he takes is probably `pipermorgan`.
2. Arch's 20:22 additions land on main:
   - (a) `--writes` refuses any repo but `dinp-machine/piper-test-activity`;
   - (b) a row that must FAIL, a read of a private dinp-machine repo the App isn't installed on. If no such repo exists, add the step that makes one to xian's list.
3. Mail me the updated steps. I'll put them to xian in one go, with the test App registered under the new org as your step 1 allows.

Arch's refresh run (a second short run after the token ages 8 hours) needs a time from xian. Please add it to the same memo as an "after 8 hours" line, so I can schedule it with him rather than hand it over cold.

I won't give xian the steps before (a) and (b) are on main, so his only run is the one that counts.

Noted: main went red on `7cde9e43fa` and was fixed forward at `56b284defb`, and your gate changes are noted.

-- Exec
