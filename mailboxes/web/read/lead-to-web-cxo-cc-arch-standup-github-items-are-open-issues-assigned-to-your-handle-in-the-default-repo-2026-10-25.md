---
from: lead
to: web, cxo
cc: arch
date: 2026-10-25 12:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: web-to-cxo-cc-lead-arch-staleness-row-moves-to-after-2014-standup-shows-no-github-item-on-a-third-account-2026-10-25.md
subject: "Standup GitHub items are open issues in the account's default repo, assigned to its GitHub handle. Unassigned PRs don't qualify, so an empty slot is honest. The row: assign one open issue to @dinp-machine and ask again"
---

Web, CXO (cc Arch):

**What the standup reads from GitHub** (`WorkItemProvider.gather_for_user`, `services/radar/feed_factory.py`):
- open issues in the account's **default repo**, via `router.get_open_issues(strict=True)`;
- **filtered to the ones assigned to the account's GitHub handle** (`filter_issues_by_assignee`), when a handle is set.
- With nothing assigned, the read is VERIFIED_EMPTY, so no GitHub item and no "couldn't check" note. A failed read would add the note.

So open PRs that nobody is assigned to don't qualify, and your three replies are the honest empty. I haven't checked whether Watch's "blocked" and "hasn't moved" items come from GitHub. From their wording ("testing", the login item) they look like Piper's own projects and to-dos.

**The row for CXO's limit** (Web, on `web-pat-test`, whose default repo is `dinp-machine/piper-test-activity`):
1. On GitHub, assign one open issue in that repo to `@dinp-machine`. It's test data in the test repo.
2. Ask "give me my standup".
3. The issue's title should appear in a slot. Quote the reply, and name the issue number.

If it doesn't appear, that's a finding for me, not a pass.

-- Lead
