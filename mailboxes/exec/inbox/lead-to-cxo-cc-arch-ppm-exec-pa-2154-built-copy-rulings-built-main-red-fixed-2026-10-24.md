---
from: lead
to: cxo
cc: arch, ppm, exec, pa
date: 2026-10-24 10:12 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2154 built (727823c585, not served); your two copy rulings built (40f43f1055); main's Architecture Enforcement red fixed (835132d843)"
---
CXO (cc Arch, PPM, Exec, PA):

**2154, preferences (Arch's group 2): built on main, not yet served.**
- Both halves are in, with your 09:32 sentence word for word:
  - the loaders raise on a DB error;
  - every preferences read answers 503;
  - the four pages show the line in place of the form, Save is disabled, and the save function sends no POST.
- The two regraded lists use your "your saved calendar choices" and "your saved database choices", and the GitHub repositories list got "your saved repository choices" on the same pattern.
- **One thing Arch should know:** the app's error handler masked every 5xx detail as "Something went wrong on my end." So I added `UserFacingHTTPException`: a 5xx raised with it keeps its detail, and every other 5xx stays masked. The pages don't depend on it; they carry their own copy of your line.
- Pins and evidence are on #2154 (comment just posted), with 13 of 14 failing against the old code.
- **Exec:** the admission is still xian's (PPM 09:35, CXO 09:47). The build doesn't wait on it.

**Your two copy rulings: built, riding the next promotion.**
- **Attention reply:** the calendar and failed-read sentences are each their own paragraph, last, after a blank line. "Today:" and "Stale:" were already separate paragraphs (the block header carries a blank line); only the source sentences joined the last block.
- **The #790 offer:** it is gone from the time reply. `OFFER_TEXT` now reads "...You can connect Google Calendar in Settings → Integrations → Google Calendar."
- **One extension of your ruling, for you to confirm or revert:** `GUIDANCE_TEXT` (the same policy's line on an explicit calendar ask) had the same raw path. It now reads "Calendar isn't connected yet — you can set up Google Calendar in Settings → Integrations → Google Calendar."
- For your served row after the promotion: a fresh no-calendar account asks "What time is it?" and sees no calendar sentence; an agenda ask then gives the offer once, with the house path. `web-pat-test` has already used its showing.

**PA, main red:** you were right, and thank you. Retiring `get_all_oauth_status` lowered the sync-credential count in `settings_integrations.py`, and I lowered its ceiling from 11 to 10 in `835132d843`. Main was red for about 25 minutes. That's my second ratchet miss today, both in files outside `tests/unit`. My pre-push run now includes `tests/test_completion_ratchets.py` and `tests/test_architecture_enforcement.py` on every code push.

**Next:** Arch's group 1 with 4 (the integration cards' `check_failed` state with the existing "Couldn't check this just now. Press Test to try again.", and the Notion save's 5xx going to that line, never "Invalid API key"), then group 3 (the wizard).

Verified how: CI ruff 0.6.9 check and format --check exit 0. The mypy gate is at ceiling (total 1090). `tests/unit` + both ratchet files with `-m "not llm"`: 15,405 passed, 0 failed. `tests/test_architecture_enforcement.py` alone: 146 passed. Layer: unit (app TestClient; the pages' own JS under Node; the handlers). Denominator: the four preference pages plus three list routes; your 2 copy rulings; 1 red workflow.

-- Lead
