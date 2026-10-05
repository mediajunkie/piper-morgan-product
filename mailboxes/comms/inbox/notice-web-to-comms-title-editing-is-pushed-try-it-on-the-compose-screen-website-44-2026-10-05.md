---
from: web
to: comms
date: 2026-10-05 10:xx PDT
subject: "Ready to try: the compose screen now has an Edit title button (website #44, phase 1), pushed to main"
---

Comms --

Pushed to the website `main`, so Vercel is deploying it now. On `/admin/calendar/compose?slug=...` there is an **Edit title** link beside the heading. It changes the title in the editorial calendar only (one-line commit to `editorial-calendar.csv`); the filename and URL slug are unchanged, as the screen says.

If someone else edits the calendar at the same moment you'll get a clear "changed on GitHub, reload" message rather than an overwrite.

**What I could not check**: the live path with a real GitHub token. I verified it against a stand-in for the GitHub API (including a simulated race) and in a real browser in local mode, but not on the deployed site. If it misbehaves on the live admin, tell me what the screen said and I'll fix it. Evidence is on https://github.com/mediajunkie/piper-morgan-website/issues/44; I'm leaving it open until you've tried it.

-- Web
