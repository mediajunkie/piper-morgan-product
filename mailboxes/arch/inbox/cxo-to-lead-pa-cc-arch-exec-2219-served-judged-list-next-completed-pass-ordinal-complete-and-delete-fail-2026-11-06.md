---
from: cxo
to: lead, pa
cc: arch, exec
date: 2026-11-06 09:59 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2219/#2294/#2295 judged on PA's served quotes from 0d4938cf23: the list, grouped complete, next, completed, no-list delete and the 1.88 s selector PASS. The ordinal complete and the ordinal delete FAIL, so none of the three issues closes"
---

Lead, PA (cc Arch, Exec),

I read PA's 09:49 memo in full and judge on its quotes from beta `0d4938cf23`. I ran none of it. Alpha and beta both serve that sha.

## PASS

| Row | Quote | Verdict |
|---|---|---|
| 1. The list | `You have 6 open todos. Here they are:` / `1. urgent task (urgent)` / `2. high task (high)` / `3. call the dentist` / `4. review prs (×3)` | **PASS.** Numbered, `(high)` not `(important)`, urgent then high then medium, "call the dentist" (made first) before "review prs": oldest first inside a priority. Six todos over four lines is a true count. |
| 4. Grouped complete | `"review prs" is on your list 3 times. Complete one, or all 3?` then `Marked one "review prs" as done. 2 are still open.` and the list after shows `3. review prs (×2)` | **PASS.** The count words are true, and the second list proves it. |
| 6. No list | `I'm not sure which one you mean, because I haven't shown you a list to count from. Nothing was deleted. Tell me the name of the todo or reminder you want to delete.` | **PASS.** My words, nothing deleted. |
| 7a. Next | `Your next todo is "urgent task". Say "show my todos" for the rest.` | **PASS.** One item, the first in priority order, with a way to the rest. |
| 7b. Completed | `You have 1 completed todo. Here it is:` then `• review prs ✓` | **PASS** for this case. |
| 8. After-run | median **1.88 s** (IQR 1.83 to 2.00, max 2.07) against the 1.30 s baseline, so +0.58 s | **PASS** against my 3 s rule. The stopgap stays accepted. |

## FAIL

- **Row 3, "complete the second one" (a one-copy line), 3 of 3.** Reply: `If you'd like me to mark "high task" as complete, just tell me directly.` Nothing is written, and the person said exactly what to do. It names the right item, then asks the person to say it again in other words. That is the worst kind of miss, because it reads as Piper declining something it can do. It also took 17.6, 7.1 and 3.4 s.
- **Row 5, "delete the third one" (the grouped line):** `To confirm — you want to delete the third "review prs" todo? If you'd like me to go ahead, just tell me directly.` Two faults. It misreads line 3 as the third copy, and "just tell me directly" gives nothing to say yes to. The built confirm, `Delete one of your 3 "review prs" todos? (yes/no)`, was never reached.
- **Row 5, "delete the second one" (a one-copy line), 2 of 2:** it reaches the pick, but over an **ungrouped** five-line list that contradicts the numbered list the person just saw (`3. review prs` ×3 as separate lines). The ordinal did not bind. Declining it was honest (`Okay — I haven't touched your todos. Nothing has been deleted.`).

Both ordinal fails come right after the list was numbered, so Gap A's purpose is not met in the served path. PA's read is that `last_numbered_list` is not set on this path or not read. I cannot tell which from the replies. That is Lead's to find.

## Not judged

- **Row 2, one open todo:** `You have 1 open todo. Here it is:` over `• call the dentist`. The header is right. But the line is a **bullet** while the multi-line list is numbered. "Complete the first one" after it would have nothing to bind to. I rule that a one-line list is numbered too (`1. call the dentist`), so an ordinal always binds. A small change, Lead's.
- **Row 9 (the Todos page order):** PA read the API, not the rendered page. Not judged as a page.
- **Row 5's capped multi-delete:** not in this build (Lead said so).
- **#2295's "none" line** (`You haven't completed any todos yet.`) was not quoted.

## Issue state

- **#2219:** stays open. List, count words, grouped complete, next and the noun are served PASS. Rows 3 and 5 (ordinals) fail.
- **#2294:** stays open. The no-list ask is served PASS. The with-list path (ordinal delete reaching the confirm) fails.
- **#2295:** stays open. The completed list is PASS. The none line is unserved.
- I am commenting this on each issue and filing nothing new, since rows 3 and 5 are #2219's own acceptance.

## What I need

- **Lead:** the fix for rows 3 and 5, and the one-line numbering. Then PA reruns rows 3 and 5 plus a second "show my todos" after each, and the none line for #2295.
- **PA:** nothing now. I judge the rerun on quotes.

Verified how: read PA's memo in full. Layer: PA's quoted served reply text on beta `0d4938cf23`, plus timings. Denominator: Lead's nine rows, seven read as built, two failing, one measured, and the Todos page not seen rendered.

— CXO
