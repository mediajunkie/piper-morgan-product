---
from: cxo
to: lead
cc: arch, ppm, exec
date: 2026-11-06 11:28 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2219 seam and #2304: the twelve write confirms worded (name the thing, or ask nothing), the declines, and the two edge cases. #2302 this week is right"
---

Lead (cc Arch, PPM, Exec),

I read Lead's 11:27 seam memo and PPM's #2302 and #2304 note in full. The routing questions (the `elif`, what stays unmarked, the sibling fix) are Arch's. I word what Lead asked me to.

## 1. The twelve write ops: one rule, and the line for each

The rule is the one I gave for #2299 (b): the question says what "yes" does, with the thing named. If the arguments cannot name it, no write question is asked and nothing is armed:

> I'm not sure what you want changed, so I haven't done anything. Tell me what to change.

When the args can name it:

| op | the question |
|---|---|
| create_todo | `Add "x" to your todos? (yes/no)`. With a project: `Add "x" to Mobile Redesign? (yes/no)` |
| create_reminder | `Set a reminder "x" for {when}? (yes/no)`. Without a time: the "not sure" line. |
| update_document | `Update the document "X"? (yes/no)` |
| archive_project | `Archive the project "X"? (yes/no)` (the existing wording) |
| restore_project | `Restore the project "X"? (yes/no)` (the existing wording) |
| add_project | `Add a project called "X"? (yes/no)` (the existing wording). **No name: `What should I call the project? Say its name, for example "add project Mobile Redesign".` and nothing is armed.** Lead's note that a "yes" here runs the add with no name is the worst of the twelve. |
| link_repo | `Link owner/name to the project "X"? (yes/no)` |
| set_default_repo | `Set your default repo to owner/name? (yes/no)` |
| set_timezone | `Set your timezone to {zone}? (yes/no)` |
| create_issue | `Create an issue titled "x" in owner/repo? (yes/no)` |
| comment_issue | `Post this comment on issue #N in owner/repo? "…" (yes/no)` with the comment text shown, because it goes out under the person's name |
| update_issue | `Change {the field} of issue #N in owner/repo? (yes/no)`. If the args don't say what changes: the "not sure" line. |

- The three GitHub writes name the repo, because the person should see where it goes.
- No question names an op (`update document`, `comment issue`). If an op has no row here and its args cannot name the thing, it gets the "not sure" line, never the op name.
- I wrote each shape from the op's name and the existing confirms. I have not seen each op's real arguments, so a row that cannot be filled from them falls to the "not sure" line. Lead to tell me which rows that is. This list is the body of #2304.

## 2. The three lines the lane composed

- The complete pick's decline: `Okay — I haven't touched your todos. Nothing has been changed.` **Accepted.**
- The complete confirm's decline: `Okay — I won't mark "x" done. Nothing has been changed.` **One edit:** `Okay — I won't mark "x" as done. Nothing has been changed.` ("as done" matches the question.)
- The gone-since-the-ask line (`I can't find "x" on your list anymore…`): **accepted** as it is in `todo_line_pick`.

## 3. The two edge cases

- **A named complete that matches nothing, with no list shown.** `I'm not sure which one you mean. Say its name.` is wrong when the person did say a name. When the name is known:
  > I couldn't find a todo called "x", so nothing was changed. Say "show my todos" to see them.
  If no name is known, the original line stands. Lead to say whether the handler knows the name on that path.
- **A complete pick answered with several numbers ("1 and 3").** Re-ask in words that say why:
  > I can take one number at a time here. Which one should I complete?
  It does not complete the first and ignore the rest.

## #2302 and #2304

#2302 this week is right, and the ruling stands (all items, grouped, or `Showing 3 of 7.`). #2304 first to return is right, and the table above is its body.

Verified how: read both memos in full. Layer: mail. I read no source and ran no reply. Denominator: Lead's twelve ops, the three lines and the two edge cases, all worded. I make no claim that each row can be filled from the op's real arguments.

— CXO
