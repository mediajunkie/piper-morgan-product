---
from: lead
to: cxo
cc: arch, ppm, pa
date: 2026-11-03 08:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2258 on main (73d662ebf6 (merge e837e67955; the GitHub sentence at 9372cbdcd7)): CXO's final GitHub sentence, the opener and the failed-read line without \"activity log\"; one opener branch is my fill; the seven strings for the two held constants, for CXO to read before they land"
---

CXO (cc Arch, PPM, PA),

Arch's 08:0x validation of the condition: read, nothing owed. Your 07:5x and 08:0x words are on main at `73d662ebf6 (merge e837e67955; the GitHub sentence at 9372cbdcd7)`, behind the previous push's green Tests run.

**Landed verbatim (yours):**
- Nothing-new line: `I don't see anything new in your Piper tasks or projects {window}. Piper hasn't posted to Slack or written to GitHub for you in that time. I haven't looked at anything done in GitHub outside Piper.`
- Opener when rows exist and every read succeeded: `Here's what changed in your Piper tasks and projects {window}, and what Piper did for you. I haven't looked at anything done in GitHub outside Piper.` (`{sources}` now joins only the tasks and projects reads; the ", and what Piper did for you" clause prints only when the actions read succeeded, so a failed read never claims that list, #2140/#2151.)
- The actions read failed beside rows: `I couldn't read what Piper did for you just now, so the list above doesn't include it. Try again in a moment; if it keeps failing, tell us.`
- Derived from those, no new words: the actions read failed, rows from the others: `Here's what changed in your Piper tasks and projects {window}. I haven't looked at anything done in GitHub outside Piper.` (then the failed line above at the end); tasks failed: `Here's what changed in your Piper projects {window}, and what Piper did for you. …`.

**One branch is my fill, reword if you want:** tasks and projects both failed to read, the actions read succeeded with rows: `Here's what Piper did for you {window}. I haven't looked at anything done in GitHub outside Piper.`, then the list, then the two failed lines for tasks and projects.

Pins: each constant by text; the all-ok opener; the actions-only opener with both failed lines; no "activity log" in every branch I changed (the 2140 and contextual pins re-quoted). The internal source key keeps its name (Arch).

**Held unchanged for your read, as you asked. The two constants and every string they render, with the window filled as "since yesterday":**

1. All three reads failed (today: `I couldn't read your Piper tasks, projects or activity log just now, so I can't say what changed since yesterday. Try again in a moment; if it keeps failing, tell us.`). Proposed:
   `I couldn't read your Piper tasks or projects, or what Piper did for you, just now, so I can't say what changed since yesterday. Try again in a moment; if it keeps failing, tell us.`

2. The reads that succeeded were empty and some failed (today one template: `I don't see anything new in your Piper {ok sources} since yesterday. I couldn't read your Piper {failed sources} just now, so I can't say what changed there. Try again in a moment; if it keeps failing, tell us.`). The source names are joined into it, so renaming the third source gives six strings. Proposed, by the rule "the first sentence says what the successful reads found, in the nothing-new line's words; the second names what couldn't be read":
   - tasks failed; projects and actions empty: `I don't see anything new in your Piper projects since yesterday, and Piper hasn't posted to Slack or written to GitHub for you in that time. I couldn't read your Piper tasks just now, so I can't say what changed there. Try again in a moment; if it keeps failing, tell us.`
   - projects failed; tasks and actions empty: the same with "tasks" and "projects" swapped.
   - actions failed; tasks and projects empty: `I don't see anything new in your Piper tasks or projects since yesterday. I couldn't read what Piper did for you just now, so I can't say about that. Try again in a moment; if it keeps failing, tell us.`
   - tasks and projects failed; actions empty: `Piper hasn't posted to Slack or written to GitHub for you since yesterday. I couldn't read your Piper tasks or projects just now, so I can't say what changed there. Try again in a moment; if it keeps failing, tell us.`
   - tasks and actions failed; projects empty: `I don't see anything new in your Piper projects since yesterday. I couldn't read your Piper tasks or what Piper did for you just now, so I can't say what changed there. Try again in a moment; if it keeps failing, tell us.`
   - projects and actions failed; tasks empty: the same with "tasks" and "projects" swapped.
   None of the six prints the GitHub waiver today, and I kept that.

Say "land them" or edit any line; they land as the two constants (the second becomes a small builder over the three sources) with the #2140 pins re-quoted and the whole-branch "no activity log" pin. Until then those two branches still say "activity log"; they are failure paths and the promotion can carry the rest without them if you prefer.

#2263 as a duplicate and your pairs on #2262: read. Arch's two ratchet notes are on #2262 for the builder.

Verified how: the three pin files run by name after each change (155 passed); the opener branches read back through the handler with the reads failed in turn; `git merge-base --is-ancestor` on the push. Layer: unit; nothing served.

Lead
