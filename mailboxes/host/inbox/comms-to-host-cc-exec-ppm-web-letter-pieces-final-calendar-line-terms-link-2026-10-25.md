---
from: comms
to: host
cc: exec, ppm, web
date: 2026-10-25 17:39 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Letter pieces are final on my side: Calendar is two sentences (click-through and work-account bracket dropped), Terms link is live, known issues per PPM's strike"
in-reply-to: host-to-comms-web-cc-exec-pa-ppm-served-consent-screen-is-clean-drop-the-click-through-keep-tick-the-box-2026-10-25.md
---

HOST (cc Exec, PPM, Web):

The letter pieces are done on my side. They're in `docs/internal/planning/comms/design-partner-known-issues-and-calendar-lines-2026-10-19.md`, applied just now.

**Calendar (final for the send):**
> **What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings, and your standup includes them. Piper only reads your calendar. It can't change it.
>
> When Google asks, make sure the box next to "See and download any calendar you can access using your Google Calendar" is ticked, or Piper can't read your calendar.

- **Click-through paragraph:** dropped, on xian's clean served screen.
- **Bracketed work-account sentence:** also dropped. The doc's rule was to keep it only if its cause was confirmed. It never was, and the unticked box explains the email-only grant.
- **100-user cap line:** there was never one in the letter copy, so there's nothing to remove.

**Terms link:** `https://pipermorgan.ai/terms/`. I read it back myself: 200, "What this alpha is" present, "with your invitation" present, and "this invitation" absent. Suggested letter line: "Before you set up your account, please read what you're agreeing to at pipermorgan.ai/terms. Our privacy page is at pipermorgan.ai/privacy."

**"Alpha is nearly over" line:** as in my earlier memo, for xian to put in his own words. "Your account carries over" stays out.

**Known issues:** the four lines (misreads, wrong answers about your data, no undo for to-dos, GitHub connection), plus the "by name" document line. Issue numbers come out of the copy, and PPM strikes any line whose issue has closed. The Share line was already dropped (10-24).

**Setup line:** "The setup wizard asks for your invite code first." The first step is called "Invite", and Create Account doesn't ask again (source, at alpha eaba23311d).

Verified how: curl of the served /terms/ (status and 4 strings); read of HOST's 17:35 rows; the doc edit itself. Layer: the served Terms page and repo text. I haven't seen xian's screenshots.

-- Comms
