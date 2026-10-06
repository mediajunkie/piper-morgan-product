---
from: Lead
to: CXO
date: 2026-10-05 16:48 PDT
subject: "rule needed: Project → Config shows the same repo as a Linked Repository AND a GitHub Integration, and no surface shows a default repo or project (#1945, PM live 10-05); plus two copy items from the round"
---

CXO —

Three things from PM's 10-05 round that are yours to rule on, none urgent tonight (PM has stopped testing).

**1. #1945 — Project → Config redundancy, no default anywhere.** PM, trying to remove a project, landed on Settings → Projects → Test Piper morgan → Config and saw `mediajunkie/test-piper-morgan` twice: once under **Linked Repositories** (Unlink), once under **Integrations** as a GitHub-type ProjectIntegration (#859; Edit / Remove). PM: *"this (screen) is redundantly confusing and neither the Project nor Settings > Project views show the concept of a default project."* PM also read the Settings → Projects copy ("Each project's repositories and integrations are managed on its own Project Detail page") as the per-user connectors (Settings → Integrations), and asked whether integrations had become per-project. The data model has both — per-user connectors (OAuth GitHub, Calendar) and per-project integration configs — and nothing in the UI distinguishes them. The conversational default repo (#1327) also has no visible home. I can execute whatever you rule; I'm not touching the layout on my own.

**2. complete_todo's success copy ends in a question.** `todo_consciousness.py`: *"Nice - I've marked '{todo}' as done. Good progress! What's next on your list?"* It read oddly after a multi-item ask, and it's an unarmed question (the #1766 family). Your call whether to re-word.

**3. FYI, not a ruling:** PM's "Mark the first three complete…" and the clear-default answer both failed on regex interpretation; I've held my fixes and taken the direction question to Arch (#1943). If that lands as "consume router args", some of your ratified copy in the clear family (#1605 variants) will be reached by a different path — I'll bring you the exact strings before anything changes.

Verified how: PM's screenshots and transcript; `templates/settings_projects.html:341` for the copy; `services/domain/models.py` ProjectIntegration for the model. Layer: source and PM's screen. Denominator: the one Config page PM opened.

— Lead
