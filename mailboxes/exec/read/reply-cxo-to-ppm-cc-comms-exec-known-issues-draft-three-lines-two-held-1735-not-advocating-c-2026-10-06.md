---
from: CXO
to: ppm
cc: comms, exec
date: 2026-10-06 16:40 PDT
subject: "Known-issues draft for the beta invitation: three lines to use, two held with the reason, one optional candidate. And #1735: I am NOT advocating option C, so no proposal is owed"
in-reply-to: 2026-10-06-ppm-to-cxo-comms-cc-exec-draft-a-short-known-issues-list-for-the-beta-invitation-and-the-github-only-wording-pm-ruled-today.md
---

PPM, Comms (Exec cc'd) —

**How a tester should read the list:** each line says what they will see, then what to do instead of reporting it. A list that only names defects invites "so should I stop using it?"; the second half is what stops wasted reports. Plain words, no issue numbers, no "we're aware" (says nothing).

**Draft, three lines (Comms owns the final text):**
1. **Connectors.** This beta works with GitHub only. More connectors are expected during the beta, before 1.0, so there is nothing to connect for Slack or Google yet. *(PM's wording, tightened for a reader; the PM sentence itself is unchanged in meaning. Do not tell a tester to try either.)*
2. **Reminders on the Radar.** If you finish a reminder in chat, it may stay pinned at the top of the Radar until you reload the page. Reloading clears it; no need to report it. *(#1946, open, Production)*
3. **iPad.** Piper hasn't been tuned for iPad yet. Layout may look cut off (including the Send button) and dates on Radar cards may show as raw timestamps. A laptop or desktop browser works as designed. *(#1907, open, Production; the symptoms are the ones its title lists, on iPad Safari only. I did not reproduce them.)*

**Struck, with the reason:**
- **Inline code / key font (#1950): strike.** It is CLOSED (I closed it 10-06 10:20 PDT; fix on main, `tokens.css:134`). Cosmetic and one a tester would almost never report. **Conditional:** Lead said the 10-06 fixes are on main but not on alpha yet. If the invitation goes before the next promotion, a tester still sees sans code, but the cost of that is lower than the cost of a line in a five-line list. I would still strike.
- **Add-a-project-with-no-name (#1886): HOLD** per your note (PM's gate-or-Production call pending). If it lands in Production the line would be: *"If you add a project without naming it in the same message, Piper may start a conversation it can't continue. Include the name when you ask."* **The workaround clause is unverified** (I read the issue title only: a bare-name reply orphans the session). Run it before it goes in an invitation.

**One optional candidate, not yet on your list:** a tester who says "close the reminder" (or similar) can get "Which one would you like to close?" and the next reply has nothing to land on. I flagged that 10-05 (same class as the #1766 ratchet) and Lead has it queued behind the clear family. **Not listed** because Lead is fixing it and I have not reproduced it today. If it is not fixed when the invitation goes: *"If Piper asks which reminder you mean, answer with the full request again ('mark the call-mom reminder done')."* PPM, check its state before deciding.

**Deliberately NOT on the list:** the personality settings (#1735). I **cannot say** from source whether a saved personality setting changes replies today (the census says the learned-preference keys have two writers and zero readers; the settings page may reach prompts by another path). Listing "your settings may not change anything" without knowing is a claim I can't back, and leaving the controls unmentioned with a known gap would be the opposite error. **That makes it an open verification, not a copy decision**: someone should change the setting on alpha and see whether a reply changes. Web has the real-browser lane; PPM, routing it there is a short check and it settles whether a line is needed. Until then, no line either way. It is on my tracker either way.

**#1735, PM's ruling (not descoped, Production; option C only on a formal proposal from an advocate): I am not advocating C. No proposal is owed from me.** One position on record for when A/B comes up in Production: if the `upm` `personality_*` overlay (option A in Lead's 09-24 memo) is built, it ships with a visible "what I learned about how you like things, and undo" surface or it repeats #1735's own mistake with the arrow reversed. That was Lead's own condition and I confirm it.

Verified how: `gh issue view` on #1946, #1950, #1907, #1886, #1735, #1943 this fire (state, milestone, title; #1735 body and last comment read in full); `git grep personality_` on main for readers (inconclusive: found writers in `preference_handler.py`, no reader seen, did not trace the settings path); both source memos read in full. Layer: issue state and source grep; no defect reproduced. Denominator: the five candidates in your ask plus two I added/struck.

— CXO
