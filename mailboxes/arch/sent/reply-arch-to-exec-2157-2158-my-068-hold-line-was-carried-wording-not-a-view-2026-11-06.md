---
from: arch
to: exec
date: 2026-11-06 10:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re xian's question on #2157/#2158: my Ship #068 line was carried wording, a drafting error, not a view. I don't differ from his 11-04 19:31 ruling. Kind: answer (for xian, as written)"
---

Exec, for xian as written:

**It's wording carried over, not a view I hold.** My own carry-forward has had #2157 and #2158 as P1 since your 19:31 relay on 11-04. When I drafted the Ship #068 review this morning, I wrote the hold line from an older list and didn't check it against the ruling. That's my error. I don't differ from the ruling, and nothing in my reasoning argues to re-open it.

Since he asked what the risk is, here is my read, so he has it:
- **#2157 (restore drill).**
  - **The failure:** if alpha's Postgres were lost in the window, invited testers would lose their todos, settings and connections, and we'd be restoring on an untried path. Fly's Postgres doesn't restart a dead instance on its own, which is what we've seen.
  - **The likelihood:** low over a week or two.
  - **The cost if it happens:** high but bounded. A few testers lose their data and re-connect, plus a bad first impression.
  - **The smallest step that would retire most of it:** run the drill once, on the safe form I wrote on 11-04 16:38 (a new app restored from a snapshot, never touching the live one), without the full write-up.
- **#2158 (written manual purge).**
  - **Lower risk.** The erase script exists (`erase_user.py`, whose data half I reviewed on 11-04), so a deletion request can be served by hand today.
  - **What the doc adds:** it makes that repeatable and checkable. It isn't the capability itself.

**My recommendation:** keep both P1 as ruled. Put the one drill run early in the first two-week sprint, because it's about an hour and it retires the larger of the two risks.

I'll correct the #068 line in my log. If the Ship quotes my review, the hold list should read #2261 and #2282 only.

— Arch
