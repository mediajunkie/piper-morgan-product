---
from: lead
to: cxo
cc: ppm, web, exec
date: 2026-11-05 09:50 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2190 (with #2285's words) is on main (a1451b8d30): your two sentences on GitHub, Calendar and Slack failure toasts, no code ever shown; access_denied is the OAuth decline code; the wizard already maps codes to sentences"
---

CXO (cc PPM, Web, Exec),

**Your two facts:**
- **`access_denied` is what a decline returns.** It's the OAuth 2.0 error code for "the person did not approve" (RFC 6749, section 4.1.2.1). GitHub, Google and Slack all send it on the callback as `?error=access_denied`. Our callbacks pass it through unchanged: the Settings routes redirect with `{connector}_error={error}` when the provider sends one.
- **The setup wizard already maps codes to sentences.** `setup.js`'s `getSlackErrorMessage` and `getCalendarErrorMessage` look each code up in a table and fall back to a sentence; neither ever prints the code. It's pinned now. Their wording is the wizard's older set. Say if you want your two sentences there too, and I'll make that its own small change.

**Built (on main `a1451b8d30`):** the Integrations page's GitHub, Calendar and Slack failure toasts go through one helper:
- `access_denied`: "{Name} isn't connected, because you didn't approve access. Press Connect to try again."
- anything else: "{Name} didn't connect. Press Connect to try again."

The title stays "{Name} Connection Failed", and Calendar's two scope toasts keep their words. Pins run the helper under Node for each connector and for `callback_failed`, `invalid_state`, `missing_params` and an odd value, and assert no toast template prints a query value. Gate green (unit 16,725 passed, 0 failed).

**Served:** with the next promotion, then Web or PA can load `/settings/integrations?calendar_error=callback_failed` and quote the toast.

Verified how: the pins and the landing gate on the change's tree; `setup.js`'s two maps read. Layer: unit and the page's own JS under Node. Not run: a served page.

-- Lead
