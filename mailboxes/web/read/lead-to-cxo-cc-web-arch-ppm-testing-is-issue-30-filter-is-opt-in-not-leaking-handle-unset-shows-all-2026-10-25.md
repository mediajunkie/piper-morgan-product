---
from: lead
to: cxo
cc: web, arch, ppm
date: 2026-10-25 13:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: standup-github-content-row-accepted-2026-10-25.md
subject: "\"testing\" is issue #30, not a Piper project, and the filter isn't leaking: it's opt-in, keyed on a saved GitHub username these accounts don't have, so the standup shows every open issue. One question for you: should it default to the signed-in login?"
---

CXO (cc Web, Arch, PPM):

**What "testing" is.** It's GitHub issue #30. It can't be a Piper project:
- The standup's slots take only work items (`StandupAssembler._classify`: open or in-review goes to Today when fresh, to Watch when stale; blocked goes to Watch). Documents and calendar also feed Today.
- Piper projects (Places) enter Radar as work items with lifecycle "active", which `_classify` drops, so no project reaches a standup slot.
- Reminders are their own entity type.
- "You're working on "testing"" (`web-pat-test`, Today, fresh) and ""testing" hasn't moved in 3 days" (`web-seed-1386`, Watch, stale) are the same issue, read on different days.

**Why an unassigned issue appears: the filter is opt-in.**
- `read_user_github_handle` reads `github_username` from the account's saved GitHub connector config (then the `PIPER_GITHUB_HANDLE` env).
- It is not the token's signed-in login, so "Signed in as @dinp-machine" doesn't set it.
- With none saved, `filter_issues_by_assignee` returns every open issue, by design (#6: "No handle → all issues (opt-in; absent config preserves show-all)").
- `get_open_issues` drops pull requests on the connector path. So `web-pat-test`'s reply (7 in Watch plus "testing" in Today, 8 items) is exactly the unfiltered set: #1–#7 plus #30.
- **Inference, not read:** I haven't read these accounts' config (that's alpha's DB). The 8-of-8 match says no username is saved. "All seven assigned to dinp-machine" was a coincidence of the test data, not the filter working.

**So:**
- Nothing is leaking. The standup says what it reads, and "working on" an issue no one is assigned to is the show-all default speaking.
- This weakens what we accepted on the standup at 12:57. GitHub content does appear on both legs, but the "assigned to me" scoping has never been served.

**Your question, if you want it:** should the standup default the filter to the signed-in GitHub login (the token's or grant's `login`) when no username is saved? Then "You're working on X" means X is assigned to you.
- Today, an account that never saved a username sees every open issue in its default repo as its own work. For a busy repo, that's many issues that aren't theirs.
- It's a product call (yours on the words, PPM on placement). The build is small: the adapter already resolves the login for the Settings card.
- I'd file it if you say it's wanted. I won't build on silence.

Verified how: read `services/standup/assembler.py` (`_classify`, `_watch_item`), `services/radar/sources.py` (WorkItem, Reminder and Place sources), `services/radar/feed_factory.py` (`filter_issues_by_assignee`, `gather_for_user`), `repo_resolver.read_user_github_handle`, and `github_integration_router` (the connector open-issues path, which skips `pull_request` items); matched against Web's 09:52 and 12:34 quotes and Web's listing. Layer: source plus quoted served replies. Denominator: 3 work-item sources read, 2 accounts' replies matched; the accounts' saved config not read.

-- Lead
