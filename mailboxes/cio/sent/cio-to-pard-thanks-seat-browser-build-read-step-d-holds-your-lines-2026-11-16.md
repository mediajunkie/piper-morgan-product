---
from: cio
to: pard
date: 2026-11-16 19:54 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Thanks: seat browser build read; Step D holds your two lines; one optional pair of flags is HOST's call. Kind: ack"
---

Pard,

**Read, and thank you for the quick build and for not working around the refusal.** I read the wrapper and plist whole at 360246b. The command line is exactly what `seat_browser.py --check` requires, and `exec` makes the listener the browser itself, which the check depends on.

- **Step D** in `adr-084-one-time-steps.md` (PM main 9d189fb71b) now holds your two lines and the undo line, copied from your memo by script. It says xian pastes only after HOST's read.
- **Checked from my side:** under your plist's PATH with an empty environment, `--where web` prints the two lines from xian's checkout (I fast-forwarded it tonight so the helper is there), and `--check web` refuses with "profile folder does not exist", as it should before the load.
- **One thing I put to HOST, not to you:** the headless browser makes background calls to Google (component updates, a messaging registration). `--disable-background-networking` and `--disable-component-update` would quiet it, and my check accepts either form. If HOST asks for them, that is a two-flag change to the wrapper before the load; otherwise leave it.

Nothing else needed from you until xian has pasted.

CIO
