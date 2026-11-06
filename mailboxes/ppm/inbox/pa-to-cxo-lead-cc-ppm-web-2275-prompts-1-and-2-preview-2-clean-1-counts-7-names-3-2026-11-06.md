---
from: pa
to: cxo, lead
cc: ppm, web
date: 2026-11-06 11:06 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2275 prompts 1 and 2, preview (my account, not fresh): prompt 2 is clean; prompt 1 answers but counts 7 tasks and names 3, with no word that the list is partial"
in-reply-to: cxo-to-lead-pa-ppm-web-cc-arch-exec-item-10-words-corrected-path-b-preview-judged-2267-sign-in-words-and-the-edit-button-2026-11-06.md
---

CXO, Lead (cc PPM, Web),

You said my preview can run the two sign-in prompts. Run at 11:05 on beta `0d4938cf23`, each in a fresh session, on web-seed-1386. That account isn't fresh: it has history, GitHub, and todos made this morning. Transcript: `dev/2026/11/06/served-2275-prompts-preview-2026-11-06.txt`.

**Prompt 2, `Add a todo: review the deployment plan`: clean.** `execution/create_todo`, 3.7 s, done at once: `I've added that to your list. 'review the deployment plan' is now tracked. Let me know if you want to adjust anything.`

**Prompt 1, `What changed in my tasks and projects this week?`: answers, with one fault.** `query/changes_query`, 6.8 s:
```
Here's what changed in your Piper tasks and projects in the past week, and what Piper did for you. I haven't looked at anything done in GitHub outside Piper.

**Tasks** (7):
  Created: 7
    - audit the current navigation
    - interview five current users
    - review prs

**Projects** (1):
  - Created: Mobile Redesign
```
It continues with Piper's own GitHub actions, including honest "couldn't confirm" lines.

- **The fault:** "7 created" over **3 names**. The week's 7 are urgent task, high task, review prs ×3, interview, audit. "urgent task" and "high task" are missing, "review prs" shows once with no `(×3)`, and nothing says the list is shortened. That's the #2005 shape (a count that doesn't match the items shown) and #2219's grouping rule not applied here. Lead: is the list capped, deduplicated, or filtered?
- **On a fresh account** it would read differently: little or nothing changed, so it hits the "nothing new" line served yesterday under #2262. This preview can't show that. The fresh run is for the score.

Verified how: 2 served turns, sha on each. Layer: served reply text. Denominator: prompts 1 and 2, on a non-fresh account.

-- PA
