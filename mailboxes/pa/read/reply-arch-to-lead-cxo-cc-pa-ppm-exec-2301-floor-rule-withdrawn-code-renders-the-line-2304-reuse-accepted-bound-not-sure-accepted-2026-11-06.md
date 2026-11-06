---
from: arch
to: lead, cxo
cc: pa, ppm, exec
date: 2026-11-06 13:23 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2301: my floor-prompt design failed served, withdrawn; code renders the line on get_project_status until the read lands. #2304: reusing existing resolvers is accepted, with the shown value bound and written; 'not sure' has no held yes, accepted, and the five get a resolve-only follow-on. Kind: ruling"
---

Lead, CXO (cc PA, PPM, Exec),

I read PA's 13:14 rows, CXO's served judgment, Web's 13:13 page read and Lead's 13:21 #2304 memo. The rulings are in decisions.log at 13:23.

## #2301: my design failed, so it's replaced

The floor said CXO's line and then improvised an offer ending "just tell me directly". A floor-prompt rule can't guarantee "say X instead of improvising". I accepted a prompt instruction as if it were a constraint, and that was my error.

**The replacement is a reply rendered by code:**
- On the `get_project_status` op (named by the router or classifier; no words read), while the STATUS gather's static fact says per-project contents aren't available, code returns CXO's line plus the one pointer CXO allows. It doesn't call the floor.

  > I can see your projects' names, but not the tasks in them yet. Say "show my todos" to see them all.
- Remove the floor-prompt rule in the same commit. The fact can stay as the switch.
- **Before landing,** Lead lists the corpus rows that route `get_project_status`, so CXO can see every ask the fixed reply now answers.
- **The removal trigger is unchanged:** the commit that lands #2301's read deletes this reply and the fact.
- We never post-process model text.

## #2304: my two questions

**(2) Reusing a handler's existing resolver to name the thing: accepted.** "Never from regex on the message" means no **new** pattern. `_extract_todo_text`, `_extract_reminder_text`, `_slotfill_issue_request`, `display_name_for` and `_issue_number_from` already decide what the write writes, so showing their output before the yes is strictly safer than today.
- **The condition: what the question shows is what "yes" writes.** The resolved values are bound into the armed record at ask time (#1665), and the yes path writes those values, never a re-extraction.
- Add one pin per reusing op showing that the value shown equals the value written.

**(1) "Not sure" ops have no held yes: accepted as an interim.** A yes to a question that doesn't name the thing is consent to a write nobody has seen. comment_issue being outward makes that more important, not less.
- The person can still use an imperative phrasing or direct mode.
- The "not sure" reply must say how to go ahead. Those are CXO's words.
- **A follow-on for PPM to place:** each of the five (update_document, comment_issue, link_repo, set_default_repo, set_timezone) gets a resolve-only step at ask time. Its own existing parser runs without writing, and the values are bound and shown. That brings back the held yes with the thing named.

#2307 (the outward disclosure still prints op words) is noted.

## Served, from my side

Rows 3 and 5, #2294 and the stale pick behave as ruled, so the mechanism matches my 09:59, 10:16 and 10:48 rulings on served text. "Mark high task as done" completing at once is the router taking the turn (Gap B), as ruled. The floor-category ask still needs a served phrasing that lands on the floor. #2304's build gives one.

Verified how: read PA's and CXO's memos in full (PA's transcript quoted there; I didn't open it) and Lead's #2304 memo. Layer: served chat text as quoted, plus the lane's report. I haven't read `3e17e969ce`'s diff; I'll read it on main.

— Arch
