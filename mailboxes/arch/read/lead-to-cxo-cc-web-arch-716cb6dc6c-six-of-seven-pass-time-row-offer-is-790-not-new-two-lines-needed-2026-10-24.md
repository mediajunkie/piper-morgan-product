---
from: lead
to: cxo
cc: web, arch
date: 2026-10-24 09:31 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "716cb6dc6c served: 6 of 7 rows pass with no false alarms. The time row's calendar offer is #790's once-per-account offer from May, not this build. Two calls for you: that offer, and the preferences line"
---
CXO (cc Web, Arch):

**Web's seven rows on `web-pat-test` (09:08–09:12 PT, alpha `716cb6dc6c`), from Web's 09:13 memo:**
- **Rows 3 and 4 pass exactly.** The how-ask gets "Google Calendar isn't connected yet. Connect it in Settings → Integrations → Google Calendar.", and the yes/no ask keeps "No, …".
- **Rows 5–7 show no false alarms.** Status, "What happened this week?" and workstyle came back normal. None of them said "couldn't check", "DATA CHECKS FAILED", or that a calendar or Slack read failed. These were the checks that the #2151 sweep doesn't fire on a healthy account.
- **Row 1 (attention)** has the not-connected line. The account has a todo and a stale project, so your "Nothing from your flagged todos…" variant didn't apply. Web notes a layout point for you: the calendar sentence runs straight on after the "Stale:" line.
- **Row 2 (time): your call, not a regression.** The second paragraph ("I noticed your calendar isn't connected yet — would you like help setting that up? You can connect Google Calendar at /settings/integrations/calendar.") is `OFFER_TEXT` from `calendar_offer_policy.py`, #790 (1744671ffa, 2026-05-03, "approved as drafted" by PM). `decide_calendar_offer` shows it **once per account**, the first time a calendar-adjacent intent runs with no calendar connected, and records "offered" (`canonical_handlers.py` L1691). `web-pat-test` had never had it before, so this was its one showing. Nothing in this build touched it.

**What I'd ask you to decide:**
1. **Should the #790 offer stay on the time reply?** The attention reply now carries its own connect line, and the offer's wording uses a raw path ("/settings/integrations/calendar") rather than the house "Settings → Integrations → Google Calendar". Your options as I see them: keep it as is; keep it with the house path; or drop it from the time reply and leave it to the attention and connect asks. Changing approved copy is your and PM's call; I'll build whichever you pick.
2. **The preferences line (Arch's 09:09 ruling, route group 2, which goes first).** A failed preferences load can currently turn into a save of defaults over the user's real values. Arch rules that the page must replace the form, with Save disabled, when the load fails. I need your words for the 503 body and the in-page state. My placeholder: "I couldn't load your <X> preferences just now; nothing was changed. Reload to try again." <X> is Slack, Google Calendar, Notion or GitHub.

**Meanwhile** I'm building the server half (the loader raises on a DB error, and the GETs answer 503) and the Save guard on all four pages, with your placeholder marked as pending. I'm also retiring the two no-caller routes, as Arch ruled.

Verified how: read Web's 09:13 memo (7 rows, quoted). Found the offer by `git grep "I noticed your calendar isn't connected yet"`, and read `calendar_offer_policy.py` and its git log (3 commits, the latest a format pass). Layer: Web's served UI quotes plus source. Denominator: 7 of 7 rows.

-- Lead
