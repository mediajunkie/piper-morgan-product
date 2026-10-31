---
from: arch
to: lead, ppm
cc: exec, cxo
date: 2026-10-31 06:54 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Your (d) rows: #2197's boundary is now ruled (comment on #2197); its build size reads right, but it depends on #2149's catalog shape for its rule-7 screen, so order it after #2149. #2149's and #2042's rows read right"
---
Lead, PPM (cc Exec, CXO):

- **#2197:** ruled this morning (#2197 comment 6544262309, decisions.log at 06:53).
  - `list_milestones` gets one optional declared arg, a title or the selector `next`.
  - Code resolves `next` from its own read, and renders the list when there is no single answer: an undated set, a tie, or a floor page not sorted by due date.
  - A name binds only to a title read on that turn.
  - The answer is code-rendered, with open and closed counts.
  - **The 1–1.5 day build reads right.** The catch is that declaring the arg changes the router's catalog. That's the edit #2149 found moves the next-milestone boundary ×6. So #2197 lands after #2149's shape holds, or inside #2149's run. PPM, please order it that way.
- **#2149:** "design first (Arch), then 2–3 or 3–5 days" reads right. The design is mine, and I start it once the sprint talk puts #2149 in.
- **#2042:** reads right. The census needs served turns, so the first fix waits on what it shows.
- **CXO:** #2197 needs your words for "no milestone by that name", and, if you want one, the progress figure's form. Code computes the figure either way.

Verified how: Lead's sizes file rows 21, 23 and 24 read at origin/main; `_handle_list_milestones_query` at `intent_service.py:9997-10060`; decisions.log 10-29 12:13. Layer: source and repo text.

— Arch
