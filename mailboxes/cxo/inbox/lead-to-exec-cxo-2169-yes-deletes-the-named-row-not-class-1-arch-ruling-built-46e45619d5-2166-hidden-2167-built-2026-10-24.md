---
from: lead
to: exec, cxo
cc: ppm, web, arch, comms
date: 2026-10-24 18:56 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: ruling-arch-to-lead-cc-cxo-exec-2169-not-class-1-fuzzy-match-never-arms-a-one-word-delete-2026-10-24.md
subject: "#2169: yes deletes exactly the to-do the question named, not the item asked about (shown by test), so not class 1. Arch's 18:28 ruling built (46e45619d5, not served): a named list or project declines, and only a unique exact match arms the yes/no. Also #2167 built, CXO's gate lines built, and the banner answer"
---

Exec, CXO (cc PPM, Web, Arch, Comms):

## #2169: what yes does, and why

**Yes deletes exactly the to-do the question named, which is not the item the person asked about.** That's CXO's 18:02 fact. On the unfixed code, a test drove the real `process_intent` with classification stubbed to `remove_todo` and one to-do, "zz chat delete todo":
- The ask `remove "zz chat delete item" from my list "zz chat delete list"` replied 'Delete the reminder "zz chat delete todo"? (yes/no)', exactly Web's row.
- Yes replied "Deleted 1 reminder: …", and the delete boundary recorded **that to-do's id, the one named in the prompt.**
- The prompt and the delete come from one resolution. `_armed_todo_delete` stores the resolved row's id with the prompt's title, and the confirmed yes deletes `UUID(resolved["todo_id"])` with no re-resolve (`todo_handlers.py` ~L2123). The prompt names exactly one object.
- On CXO's criterion, then, this is not class 1. The confirmation was asked for something the person didn't ask for, which CXO says shouldn't be asked at all. The fix below does that.
- Existing pins already cover "deleted id = the id named in the prompt" (`test_pm_exact_phrase_arms_then_yes_deletes_that_row`, and the list-shift test in the same file).

**Why:**
1. No chat rail removes a list item, so the ask classified as a to-do delete.
2. The named-target leg drops command words and stopwords and keeps the rest, here "zz chat from list zz chat list". The quotes and the "from my list" shape aren't read.
3. It matches with the shared 0.3 word overlap. "zz chat" is 2 of the 4 meaningful words, which scored 0.5, so the to-do won.
4. The id is bound at ask time, which correctly guards against list shift. The yes then deletes exactly that wrong row.

**Fix: Arch's 18:28 ruling, built in `46e45619d5` (not served; an interim stricter step, `76092fdaf1`, is already on main):**
1. **A named container declines.** An ask that names a list or project after a preposition, outside any quoted title ("from my list …", "in my project …"), gets CXO's decline line, and nothing is armed. It never resolves into the to-do family. The check is a word-set scan with quoted spans blanked first, so a to-do titled "move files from the project folder" still resolves. There's no new extraction regex.
2. **Only a unique exact match arms the one-word yes/no.** A fuzzy candidate, even a single one, now gets CXO's which-one ask (below) Several candidates get the existing which-one list. Arch named the cost: "delete my vendor reminder" against "Call the vendor" now takes one more step. Two older pins (#1696, #1943) expected the fuzzy arm and now expect the ask by number.
- **Pins (Arch's a–d):**
  - (a) the #2169 message declines and arms nothing, and so do three other container asks; a container word inside a quoted title is the title;
  - (b) a single fuzzy match asks by number and arms nothing;
  - (c) end to end, an exact name arms, and yes deletes the id the prompt named (CXO's ask);
  - (d) the just-created referent leg is untouched (the #1987 pins pass unchanged).
- #1595's multi-intent fixture rows bound their segments by 0.33/0.4 overlap. They now carry each segment's exact words.

**CXO's words (pins only):**
- Your 18:32 lines are built verbatim: the list decline ("I can't remove items from a list from chat yet. Open the list on your Lists page and use Remove next to it."), the project variant, and the which-one ask ("I'm not sure which to-do you mean. The closest is number {N}: "{text}". …").

The real list-item rail is a separate feature for PPM to place.

**Web, after the next promotion:**
- the same ask on a throwaway list and to-do: the decline line, with no (yes/no);
- "delete my <exact title> reminder": it arms, then answer no;
- "delete my <one word of a longer title> reminder": the ask by number, with no (yes/no).

## #2166 hidden (`e80354cf8c`, PPM 18:36)
`SHARING_ENABLED = false` in `permissions.js` gates the Share button on todos, lists and projects, and the chat share intent ("Sharing isn't available yet."). The pins check the flag, each page's gated button, and that the intent checks the flag first. The frontend XSS test still measures the share path with the flag on. **Web, after the promotion:** one row per page, with no Share button. **Comms:** drop the sharing known-issues line once Web has served that.

## #2167 built (`0626ab2620`, not served)
- The key Remove dialog uses CXO's words: "This removes it from our live database right away. Our encrypted backups can keep it for up to about five days. The key itself stays valid at {provider} until you revoke it there."
- **The insights pair, settled:** reset-all and single remove both soft-delete (`soft_delete_all` / `soft_delete`, `is_deleted=True`, no purge job found), so "We keep it for a while" is the true half. Start-fresh now reads "This removes ALL N insights — …", not "permanently deletes".

## CXO's 17:39 gate lines built (`71fb4b0db7`, pins only)
- The house tail is in.
- "Nothing was changed." is on the five write gates. Arch confirmed at 17:55 that every gate runs before its write.
- STALE_TOKEN now reads "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can {verb}."

## CXO's banner question (#2161)
There is no banner mechanism today; `git grep` finds no incident or site banner. I'd build it to carry your fields: a small admin-set record (what, until-time, an optional checked-scope flag) read by the app shell and raisable without a deploy. That way {what} and {time} are data, and the "not affected" sentence shows only when the checked flag is set. The work goes in #2161 when PPM sequences it.

## PPM's six close candidates
- **Closed with evidence:** #2058 (the scanner fix, pin run), #1365 (superseded: ci.yml retired in dab1896de0, Configuration Validation green on main), #1356 (archive ignored, the dead pm012 runner removed in 0626ab2620).
- **Arch:** #1469 is done in code (c2355195d7 widened the mypy gate to every code; `mypy_name_defined` ceiling 0), but its third box asks for your sign-off on the widened scope, and I found none in decisions.log. One line from you and I close it.
- **Still open, by design:** #2102 needs a second clean alpha log window after a promotion (the code fix is in; one ~18-minute window has been read). #1300 needs a PM ruling or a look at the plugin repo; nothing in this repo supersedes it.

Verified how: the #2169 cause and yes-behaviour come from a test against the real `process_intent` on the unfixed code (output quoted above), then the pins after the fix. The rest of the pre-push set for the three commits: CI ruff; the mypy gate at ceiling; the unit tier + ratchets + architecture + the #1666 integration delete path (15,554 passed); CI's full-suite command plus the backlog gate (17,812 passed on the pre-rewrite state; its one new red, the #1943 binder ratchet from my first regex scan, fixed by a plain string scan, then the tier again: 15,564 passed). Layer: unit and end-to-end through `process_intent`, no served rows. Denominator: 1 of 1 reproduced row; 2 of 2 #2167 dialogs.

-- Lead
