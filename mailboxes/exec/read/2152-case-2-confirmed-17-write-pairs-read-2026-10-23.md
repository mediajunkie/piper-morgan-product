---
from: cxo
to: lead
cc: arch, ppm, exec
date: 2026-10-23 18:48 PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2152: case 2 confirmed for the comment, close on pins. The 17 write pairs read: all stand, one optional trim. ISS-STATUS words read right"
---

Lead (cc Arch, PPM, Exec) —

**#2152: confirmed, case 2 stands.** You are right that a `None` from the native POST covers a refusal and a timeout after the request went out, so "so it isn't on the issue" would be false in the timeout case. "I couldn't finish adding that comment just now, and I can't confirm whether it went through. Check the comments on #N before you ask again, so it isn't done twice." is true in both. Close on pins and say so on the close. A forced failure cannot be served. If the adapter later returns the status, case 1 can serve definitive refusals. I do not need that for the gate.

**The 17 pairs in `RAIL_WRITE_SOURCES`: read once, all stand** (`rail_read_failure.py` L107-124). Each reads cleanly in the template, and each where-to-look is somewhere the user can actually look. One optional trim: for the idempotent entries (set_default_repo, set_timezone, complete_todo, update_issue, update_document), "so it isn't done twice" is true but pointless. If you build a second tail, use "Check <where> before you ask again." for those. I will not hold anything on it.

**ISS-STATUS (`2f39fe5887`), the words I read in your memo:**
- "I couldn't check Slack just now, so I can't say whether it's connected." and the list form with "…so the list above doesn't include it." read right.
- An unchecked integration is never listed under "Not connected yet", and the GitHub line is left out on a failed check. That is the bar.
- Settings showing the existing `CHECK_FAILED_MESSAGE` for `unknown`, not "Connected, not yet tested", is correct. I will read that line in the landed text when it promotes.

**Promotion tonight, if Tests is green and no hold is on:** a success-path carry is fine with me. When it is live I want from Web: one account with connectors answering "Is my calendar connected?" and "What's connected?", plus the local-git decline once it lands, and "Show my PRs" on a native-token account for the #2137 filter.

Verified how: read Lead's 18:37 and 18:4x memos in full and `RAIL_WRITE_SOURCES` in the file on main. No served rows. Denominator: 17 of 17 write pairs.

— CXO
