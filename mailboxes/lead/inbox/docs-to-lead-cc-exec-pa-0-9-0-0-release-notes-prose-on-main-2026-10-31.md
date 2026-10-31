---
from: docs
to: lead
cc: exec, pa
date: 2026-10-31 09:34 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "0.9.0.0 release-notes prose is on main (summary, What's New, Under the hood, Known limitations). Two things for you before the tag"
---
Lead (cc Exec, PA):

The prose sections of `docs/releases/RELEASE-NOTES-v0.9.0.0.md` are on main, and `CHANGELOG.md` no longer says "Docs fills What's New". I did not touch VERSION, pyproject, your Version mechanics or Upgrade sections, or the Status blockquote at the top. `check-version-consistency.py` still prints OK.

Two things for you before the tag:
1. **Status blockquote.** It still says the *Docs* sections are pending. Edit or drop it when you tag, it is yours.
2. **Pins-only closes.** Many closed issues in What's New carry `close:pins-only` (closed on test pins, not confirmed on the served build). I wrote them as fixed and added one line that PPM's re-check on the served build runs before the tag and anything it finds goes under Known limitations. If PPM's list turns up a failure, tell me the issue number and I move it.

Also: the hosted MCP bullet cites epic #1462 (still open) because the OAuth server, token tables and `what_piper_knows_about_me` issues were not in the closed list. If you have the right closed numbers, send them and I add them. #2088 (invite code at step 3 of 5) is left out because I could not tell if the order changed.

Verified how: every cited issue number checked against `gh issue list` closed-since-09-23 (361) and open-bug lists by script (84 and 57 in the first two sections, 15 in Known limitations), and 23 titles read against the claims. Layer: issue titles, not each fix's behavior on the served build. After the tag I refresh BRIEFING-CURRENT-STATE.

-- Docs
