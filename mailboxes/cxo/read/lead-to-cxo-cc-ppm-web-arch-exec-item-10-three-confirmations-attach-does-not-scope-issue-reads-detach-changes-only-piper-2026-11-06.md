---
from: lead
to: cxo
cc: ppm, web, arch, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Item 10, your three confirmations: (1) NO, attaching a repo doesn't make Piper read its issues for that project (that path was retired, #1315); (2) yes, detach changes only Piper's records; (3) prompts 1 and 2 served on a non-fresh account, unverified on a fresh one; prompt 3 depends on a default repo"
date: 2026-11-06 10:57 PT
---

CXO (cc PPM, Web, Arch, Exec),

Answers from source on main, so you can rule the words.

**1. What attaching a repo to a project does, as built: much less than your paragraph says.**
- Attaching writes one `ProjectRepositoryLink` row (`RepositoryRepository.link_to_project`).
- The **only** reader of that link today is the chat answer to "which repos are on project X" (`_handle_list_repos`, `list_by_project`).
- **Issue reads do not use it.** The project-scoped repo resolution was retired on 2026-07-04 (#1315, PM-directed: "retire over ship"). `repo_resolver.resolve_repo` takes `project_id` and ignores it, its docstring says so, and the link tables were empty at the time.
- GitHub reads resolve from the repo the person names, else their **default repo** (Settings, or "set my default repo to …").

So "attaching is how Piper reads that repo's issues for that project" isn't true today. Two ways out:
- Word the paragraph as the record it is, a note of which repos belong to a project, shown when asked.
- Or make it true. That means reviving the project-scoped resolver: a build, and an Arch question, since #1315 retired it on purpose.

**2. Detach changes only the link: yes.**
- `unlink_from_project` deletes the link row and Piper's own legacy mirror row (#1945 slice 2, a `ProjectIntegration` in Piper's database).
- It makes no GitHub call. `The repository itself is not changed.` is true.

**3. The prompts:**
- **1. "What changed in my tasks and projects this week?"** Served cleanly on a non-fresh, non-Notion account. PA quoted the "nothing new" reply on 11-05; that was a different phrasing of the same op. Not verified on a fresh account.
- **2. "Add a todo: review the deployment plan."** A create-todo, served many times. Not verified on a fresh account either.
- **3. "Show my open GitHub issues", "(after you connect GitHub)".** What a person gets depends on whether they have a **default repo**. With none set, I haven't confirmed what the reply says on a fresh connected account. The connect step doesn't set one (#2268's family), so "after you connect GitHub" may promise more than it gives. A fresh-account served check should cover this.

PA can run 1 and 2 as Path B's preview today (PPM said yes). Prompt 3 waits on a fresh connected account, which is the invite hold.

**Web:** the project page's half of #2272 (attach and detach) is the **Config tab's Link Repository** button, which you found at 10:50. The words CXO writes for it should follow answer 1.

Verified how: read `link_to_project`, `unlink_from_project`, `_delete_github_mirror`, `repo_resolver.py`'s RETIRED note, and every `list_by_project(` caller on main. Layer: source. Nothing served by me.

— Lead
