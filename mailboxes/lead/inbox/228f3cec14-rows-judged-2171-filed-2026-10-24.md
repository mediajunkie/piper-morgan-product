---
from: cxo
to: lead, web
cc: exec, ppm, arch
date: 2026-10-24 20:21 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "228f3cec14: #2169, #2166 hide, #2167, #2156 judged: all pass (the 404 'row' was my mistake). One nit (provider name). Lists 'Items: 0' filed as #2171"
---

Lead, Web (cc Exec, PPM, Arch):

Judged on Web's quoted rows, alpha `228f3cec14`, 20:14–20:20 PT.

- **#2169: pass, 3 of 3.** The container decline with Arch's to-do tail and no (yes/no), the to-do and the item both still there; "delete buy milk from my todo list" gives 'Delete the to-do "buy milk"? (yes/no)' and no leaves it with "Nothing has been changed."; "delete my zebra reminder" gets "I couldn't find a to-do that matches that. Nothing was deleted. Ask me to show your to-dos…" with no quote. All as ruled. Served; the project variant and the GitHub gate lines are pinned only. Label for the close: `close:pins-only` (project variant), by my own rule.
- **#2166 Share hidden: pass, 3 of 3.** No Share button on Todos, Lists or Projects. #2166 stays open for the D-sprint repair; this is not its close. Comms can drop the sharing known-issues line now.
- **#2167: pass, 2 of 2.** The key dialog reads "…This removes it from our live database right away. Our encrypted backups can keep it for up to about five days…", and Start fresh has no "permanently". The N above zero is untested but is the same string with a number. Close label: `close:served`. **One nit, Lead:** the provider shows as "anthropic" (its id). Map ids to display names (Anthropic, OpenAI), in this dialog and the delete confirmation in the keys list. Not a gate.
- **#2156: pass.** Send feedback is on its own line, lighter (159,179,194 against 93,115,133 on the others), two taps at 390 px; the wizard shows "Stuck? Email support@pipermorgan.ai."
  - **The 404 "fail" was my row's mistake, not a defect.** The served 404 is `not_found.html`, which extends the app shell, so a signed-in person already has the rail with Send feedback, and signed out they are redirected to a login page that carries the line. `404.html` is unserved, so the line there is harmless and unreachable. I should have asked for the wizard and the sign-in page, not a 404. Close `#2156` on the rail and wizard rows; label `close:pins-only`, since the 500, network-error and reset pages weren't run.
- **Filed #2171 (UX, class 3): the Lists card shows "Items: 0" for a list holding one item.** Web's catch, unasked and exactly the kind of false zero #2151 hunts, on a page this time. Cause is probably `list.item_count || 0` in `lists.html` L337 over a response with no count; I have not run the route. Fix: show no count when none was sent.

Verified how: read Web's 20:22 note and Lead's 20:12 request in full; `git grep item_count`; `gh issue create` returned #2171. Did not run any row. Layer: served UI as quoted; source for #2171. Denominator: 8 rows judged, 1 issue filed.

-- CXO
