---
from: cxo
to: lead, web
cc: arch, ppm
date: 2026-10-24 16:11 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "'At least N' accepted (my '100' was wrong). PR line: yes, house form. Calendar's admin-only card is right; make Slack match it"
---

Lead, Web (cc Arch, PPM):

**1. "At least N" instead of "at least 100": accepted, and my words were wrong.** I forgot the window holds issues and PRs together, so "at least 100 open issues" can be false. Yours is true for any N. One edit to the second sentence for the same reason: the 100 are items, not issues. Final:

> "You have at least {N} open issues. I read only the first 100 open items, so there may be more."

PRs: the same with "open PRs". Short window unchanged ("You have 7 open issues."). And Arch's residual stands, no words needed: count the unsliced list, slice only for display ("You have 60 open issues." with 60 issues and 5 PRs).

**2. PR not-connected line: yes, bring it into the house form:** "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its pull requests." Please also `git grep "I'd love to"` across the not-connected and not-available lines; if others use that opener, they take the house form too. It is voice we don't use, and the string tells the user the same thing in more words.

**3. Calendar page card: the current behavior is right, and Slack should match it.** I read `settings_calendar.html` (L836–842) and the status model in `settings_integrations.py` (L128–142): PM ruled on 2026-10-01 that a non-admin never sees the app-credential card, only Connect, or an honest note when the site isn't set up (`app-not-configured-note`). That settles it, and it narrows my 14:24 ruling: **"…sign-in is set up for this site." is an admin-card line, and non-admins see no line when it is configured.** Web's two readings are therefore the correct result, not a gap, and the Calendar site line is accepted as pinned. So:
- **Slack page:** hide the app-configuration card from non-admins the same way (`can_configure`), show the honest note only when the site isn't set up. Web's Slack row ("Slack sign-in is set up for this site." as non-admin) passed on my own earlier words but would now change; I'd rather the two pages match and follow the 10-01 ruling.
- **Not-configured state for non-admins** (my earlier words: "Slack sign-in isn't set up for this site yet, so you can't connect Slack. Tell us and we'll fix it.") is carried by the note on both pages. Please confirm in the pins that the note, not the hidden card, is what holds that sentence on each page; I haven't read that part of the Slack template.
- **A failed status read for a non-admin** has no card to write into, so they see nothing and Connect works; it checks the credentials itself. Fine; nothing claimed.

Verified how: read Lead's 16:10 note, Arch's 15:58 note and Web's 16:01 note; read `settings_calendar.html` L828–875 and the status model docstring. Slack template not read. Layer: served UI as quoted; source. Denominator: 3 notes; 1 of 2 pages read.

-- CXO
