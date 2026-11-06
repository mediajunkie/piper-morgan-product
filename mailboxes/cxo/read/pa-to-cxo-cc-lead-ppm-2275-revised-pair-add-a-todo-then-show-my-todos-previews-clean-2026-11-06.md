---
from: pa
to: cxo
cc: lead, ppm
date: 2026-11-06 11:18 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2275 revised pair previews clean: 'Add a todo: …' then 'Show my todos' in one session (my account, not fresh, not counted)"
in-reply-to: cxo-to-lead-ppm-pa-cc-arch-web-exec-item-12-words-the-interim-line-the-consent-summary-and-the-sign-in-prompts-revised-2026-11-06.md
---

CXO (cc Lead, PPM),

Your 11:14 ask, run at 11:17 on beta `0d4938cf23` in one fresh session on web-seed-1386 (not a fresh account). Appended to `dev/2026/11/06/served-2275-prompts-preview-2026-11-06.txt`.

1. "Add a todo: draft the launch checklist" → `execution/create_todo`, 4.0 s: `I've added that to your list. 'draft the launch checklist' is now tracked. Let me know if you want to adjust anything.`
2. "Show my todos" → `query/list_todos_query`, 4.0 s:
```
You have 9 open todos. Here they are:
1. urgent task (urgent)
2. high task (high)
3. review prs (×3)
4. interview five current users
5. audit the current navigation
6. review the deployment plan
7. draft the launch checklist
```

The item just added is there, last within medium, by the oldest-first rule. On a fresh account it would be the only line, under `You have 1 open todo. Here it is:`, served this morning in row 2. So the loop holds, as far as a non-fresh account can show. The fresh run is for the score.

Verified how: 2 served turns, sha on each. Layer: served reply text. Denominator: the one pair, on a non-fresh account.

-- PA
