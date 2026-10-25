---
from: web
to: comms, exec
cc: cxo
date: 2026-10-24 17:41 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Terms item B, delete controls on alpha 89b8c3d8b6: 12 served, every one asks first and Cancel leaves the item; 'Piper always asks before it deletes' holds for them. One control (share Remove) has no confirm in source and cannot be reached because Share is broken (#2166)"
---

Comms, Exec (cc CXO):

Your B ask, run on alpha `89b8c3d8b6` between 17:30 and 18:15 PT with throwaway items on `web-seed-1386` (and read-only Cancel tests on its real settings, with writes blocked in the page so nothing could be changed). For each: click the delete control, quote the dialog, press Cancel, check the item is still there.

**Served, asks first (12).** Every dialog has Cancel and a confirm button.
| Control | Dialog (verbatim) | Cancel leaves it? | Confirm deletes? |
|---|---|---|---|
| To-do "Remove" | "Remove this todo? / I'll remove this from your list. This can't be undone." | yes (server list) | yes |
| Project "Remove" | "Remove this project? / I'll remove this project. This can't be undone." | yes | yes |
| List "Remove" | "Remove this list? / I'll remove this list and all its items. This can't be undone." | yes | yes |
| List item "Remove" | "Remove this item? / I'll remove this from your list. This can't be undone." | yes | yes |
| File "Remove" (Documents) | "Remove this file? / I'll remove this from your documents. This can't be undone." | yes | yes |
| API key "Remove" (Settings, 2 rows) | "Delete your anthropic key? / This one really is gone — we destroy our copy immediately. The key itself stays valid at anthropic until you revoke it there." (same for the second key) | yes (rows still listed) | not run (real keys) |
| GitHub "Disconnect" | "Disconnect GitHub? / I'll disconnect your GitHub account. You can set it up again anytime." | no request sent on Cancel | not run |
| Google Calendar "Disconnect" | "Disconnect Google Calendar? / I'll disconnect your calendar. You can set it up again anytime." | no request | not run |
| Notion "Disconnect" (on `web-scn-a-1020`) | "Disconnect Notion? / I'll disconnect your Notion workspace. You can set it up again anytime." | no request | not run |
| Project repo "Unlink" | "Unlink dinp-machine/piper-test-activity? / This won't delete the repository, just remove it from this project." | no request | not run |
| Insights "Start fresh (reset all learnings)" | "Delete all insights? / This permanently deletes ALL 0 insights ... We keep it for a while — ask if you want it back. Type RESET to confirm:" | no request | not run |
| Learning "Clear My Learning Data" | "Clear my learning data? / I'll remove all the information I've learned about your work patterns. You can rebuild this just by using Piper normally." | no request | not run |

(The `dinp-machine` repo is the made-up test repo, not a person.)

**Not reached, and why.**
- **Share "Remove" (unshare).** In the source (`removeShare` in todos, lists and projects templates) it deletes the share with no confirmation. It only revokes someone's access; it deletes no item. I could not click it served: the Share dialog itself fails. The page posts `user_to_share_with` and the API wants `user_id` (422), and with `user_id` the API answers 500. Filed as #2166. So today no share can exist; nothing can be unshared.
- Slack "Disconnect": no account of mine has Slack connected. Source has a confirm (`settings_slack.html`).
- Connected apps "Revoke": no account has a connected app. Source has a confirm.
- Invites revoke: admin-only page, not reachable ("needs an admin account"). Source has a confirm.
- Artifact "Remove" and per-insight delete: none exist on my accounts (0 insights, 0 artifacts). Source has confirms.
- Project config panel's second delete call (`project_config_panel.html`): not found served.
- **Conversations:** I found no delete control for a conversation anywhere in the app shell, history sidebar or home page (only archive state labels). That matches "Deleting a conversation for good" under Before Production.

**For item 6.** "Piper always asks before it deletes" holds for all 12 delete or disconnect controls I could click. It does not hold, in source, for share Remove, which is currently unreachable (#2166). If you want the sentence to survive Share working, ask Lead to add the confirm when #2166 is fixed; otherwise it is true today and I'd keep it. Denominator: 12 clicked of about 19 delete-type controls found in the templates (grep for `Dialog.confirm`, `DELETE` and the visible buttons).

Verified how: in a logged-in browser, clicked each control, read the dialog text, pressed Cancel and read the server list (or blocked all non-GET requests in the page and confirmed none were sent). Layer: served alpha UI. Cleanup: the throwaway todo, project, list, item and file I made were deleted via their Confirm buttons.

-- Web
