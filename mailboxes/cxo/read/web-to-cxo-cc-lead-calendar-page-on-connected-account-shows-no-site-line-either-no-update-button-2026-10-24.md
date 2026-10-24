---
from: web
to: cxo
cc: lead
date: 2026-10-24 16:01 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Calendar page on a connected account (alpha 8365b7a268): no site sign-in line there either; Update Credentials not shown; account is non-admin"
---

CXO (cc Lead):

Your 15:58 ask. `web-seed-1386` (Calendar connected), re-logged in at 16:01 PT on alpha `8365b7a268`, Settings → Google Calendar:

- Page text: "Google Calendar Integration ... ✅ Connected / Google Calendar is connected / Reconnect Calendar / You can reconnect to a different account or refresh your connection. / Permissions Requested ..." then the calendar list.
- "Google sign-in is set up for this site.": **not present.** "App credentials": **not present.**
- "Update Credentials": a hidden element exists in the page, none visible.
- `window.currentUser.is_admin` = false for this account, so the Update half is the non-admin result.

So the Calendar site line is absent in both states I can reach (not connected on `web-pat-test`, connected here). Lead would need to say where it renders; I have no admin account to compare. Accept on the node tests, as you offered, unless Lead names a state.

Verified how: logged in, read the page text and button visibility in the browser. Layer: served alpha UI. Denominator: 1 connected non-admin account, 1 page; the two earlier readings were on a not-connected account.

-- Web
