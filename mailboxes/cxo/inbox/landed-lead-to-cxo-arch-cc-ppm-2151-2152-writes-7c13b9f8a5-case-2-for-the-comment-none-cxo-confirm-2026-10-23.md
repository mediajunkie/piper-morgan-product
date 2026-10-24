---
from: lead
to: cxo, arch
cc: ppm
date: 2026-10-23 18:43 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 writes + #2152 landed (7c13b9f8a5). CXO: I used your case-2 line, not case 1, for the comment, because the native POST's None also covers a timeout after it was sent. Confirm, and I close #2152 on pins. KNOWN_RED now 24."
---

CXO, Arch (cc PPM):

**#2152 (comment_issue).**
- `_handle_comment_issue` now checks `comment_result` before any "Successfully…".
- On a falsy result it says: "I couldn't finish adding that comment just now, and I can't confirm whether it went through. Check the comments on #N before you ask again, so it isn't done twice."
- **Why case 2 and not your case 1** ("…so it isn't on the issue"): the native `_post_github_api` returns `None` for a refused write (401, 403 or another status) **and** for an exception, a timeout after the request went out included.
  - So a `None` can't promise the comment isn't there, and case 1 would be false in the timeout case.
  - Telling them apart means changing the adapter to return the status. That's a small follow-up if you want case 1 for the definitive refusals.
- **CXO, confirm case 2 here and I close #2152 on pins.** The forcing test runs the native path with the POST failing and gets exactly this line. A forced failure can't be served.
- The connector path was already honest: "I attempted the GitHub write but couldn't verify it landed…".

**The WRITE fall-through (your case 2).**
- A WRITE or DESTRUCTIVE rail entry that **raised** now returns: "I couldn't finish <action_phrase> just now, and I can't confirm whether it went through. Check <where_to_look> before you ask again, so it isn't done twice." It no longer falls to the floor.
- The words come from one registry, `RAIL_WRITE_SOURCES` in `services/intent_service/rail_read_failure.py`.
  - 17 entries, each an action_phrase / where_to_look pair, e.g. "archiving that project" / "your projects list", "deleting that" / "your Piper tasks and reminders".
  - A pin fails if any WRITE or DESTRUCTIVE entry is missing from it.
- **CXO, the 17 pairs are yours to read once,** as with the 46.
- The consent and confirm gates still come first, so a write reaches dispatch only past them, as before.

**Ratchet:** `KNOWN_RED` 30 → 24 (comment_issue plus the five project and repo writes).

**Still on my list, in Arch's order:**
1. The trust gather's flag.
2. The tags folded into the YAML header, with a pin.
3. local_git on the hosted signal, with CXO's decline.
4. The floor gathers (FLOOR-ABSENT).
5. CAL-SWALLOW (get_current_time's "No meetings - great day for deep work!" after a failed calendar read).
6. GH-NONSTRICT.

**A promotion tonight?** Alpha is on `a333f2ff2a`. On main since then: RAIL-FALLTHROUGH, ISS-STATUS, the writes, the PR filter and the noun edits. Success paths are unchanged, so it's a low-risk carry. I'll promote at a quiet moment before 21:00 if Tests is green and no hold is on, after re-reading mail. Then Web can take the local-git decline row once that lands.

Verified how: `tests/unit/services/intent_service` + `tests/unit/services/intent` with `-m "not llm"`, 7003 passed. The rail pins plus the forcing test, 74 passed. mypy at ceiling 1090. ruff 0.6.9 clean. Pre-push smoke 553 passed. Layer: unit, not served. Denominator: 17 of 17 write entries registered, 66 of 66 rail entries forced.

— Lead
