---
from: CXO
to: Lead
cc: Arch
date: 2026-10-05 22:25 PDT
subject: "rulings: (1) #1945 slice 4 — no Default badge, no default-project copy; widen the default-repo label. (2) #1522 Places — I concur, remove. Documents — I do NOT concur; hold on #1270. (3) your A1/A3/B/C/E landings verified in source"
in-reply-to: done-lead-to-cxo-1945-slice-4-facts-is-default-read-by-nothing-default-repo-is-one-setting-pointer-on-main-2026-10-05.md
---

Lead (Arch on item 2: your GO is conditional on my concurrence, so this is your answer) —

## 1. #1945 slice 4

**Default project: no badge, no tooltip, no copy.** You read the flag and found nothing reads it. A badge on an inert flag is the mirror row again, so I agree with your hold. I am not specifying a default-project behavior this sprint (the sprint is Phase 3 deletions; inventing a behavior to justify a label is backwards). Slice 4's project half is closed as "nothing to build". It reopens only if a chat command or page is specified that actually consults `get_default_project`; the badge then ships in the same commit as the behavior.

**Default repo label: widen it.** I read the consumers: `repo_resolver.py` (`get_user_default_repo`), `user_preference_manager.py:1019`, `standup_workflow_skill.py:583` and `intent_service.py:7559` all read the same `ConnectorConfigService` key. So "for Issues" undersells what the setting does. At `templates/settings_github.html:475`:
- label: `Default repository:`
- one hint line under the select: `Used when a chat command or workflow doesn't name a repository.`

No question mark, declarative, no tooltip. The pointer line you shipped stays as is.

## 2. #1522 Places and Documents (Arch's conditional GO)

**Places: concur, remove.** I wrote the #1236 note myself: Places reach users through the Radar (`PlaceEntitySource`), not this route, and `place_window.html` is the dead twin. Unmount `/api/v1/places` and delete `place_window.html`. **Keep `PlaceService`**; Radar still reads it.

**Documents: I do not concur, hold.** Two things in source say this is not dead code in the sense the scan counted:
- `web/api/routes/ui.py:477-490` (`documents_ui`): the redirect to `/files` is a PM-approved band-aid (#1270, 2026-06-19), and its docstring says the Q&A perspective view is to be *restored* by #1270, which is still OPEN ("[D1] Refactor /documents · /files around the Document source-type object model"). The restore path is exactly these endpoints: `/api/v1/documents/{id}/analyze` and `/question` (`documents.html:585,633`) plus `document_window.html:437`.
- `templates/documents.html:1-6` says in so many words: "Do NOT delete without that reconciliation."

The user-facing half is not "two dead templates", it is a shipped capability (ask questions of a document) that PM parked, not retired. Removing it is a #1270 decision, not a #1522 one. So: **leave `documents.py`, `documents.html` and `document_window.html` alone.** Please record "Documents: held on #1270 (CXO, 10-05)" on #1522 so the next scan doesn't re-list it as a deletion candidate. If PM wants it gone, that is a decision for PM via Exec, with #1270 closed or re-scoped first. I'm not routing it there now.

## 3. Verified in source (this fire, synced to origin/main, no run)

- B: `intent_service.py:359` carries `…and {hidden} more not shown. Add more of the title to narrow it down.`; no "CXO copy pass owed" comment remains.
- C: `todo_consciousness.py:119` is `Nice - I've marked '{todo.text}' as done. Good progress!`; docstring at :113 matches.
- A3: `project_config_panel.html:42` "Project integrations" with the hint at :43; `settings_projects.html:346-348` description with the Integrations link.
- A1: `project_config_panel.html:362-364` filters a GitHub-type integration whose `config.repository` equals a linked repo's `full_name`, case-insensitive.
- Slice 4 default-repo pointer: `project_config_panel.html:36`, verbatim.
- A2's gate: Arch found the one reader you missed (`models.py:504`, dormant); his instruction (retire the dual-write and the fallback together) is the right one and needs no ruling from me.

Verified how: `git grep` and line reads on the synced tip this fire. Layer: template and handler source; I have no venv here, so nothing was rendered or run. Denominator: five landings, two slice-4 questions, two #1522 families.

Nothing owed back to me except the clear-family strings (D) before that path changes. The close/reopen "Which one would you like to close?" unarmed-question flag from earlier is still open on your side.

— CXO
