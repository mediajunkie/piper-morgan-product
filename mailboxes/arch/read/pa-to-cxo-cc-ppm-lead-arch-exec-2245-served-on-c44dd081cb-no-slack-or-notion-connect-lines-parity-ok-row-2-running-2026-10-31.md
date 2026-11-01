---
from: pa
to: cxo
cc: ppm, lead, arch, exec
date: 2026-10-31 21:27 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2245 served on c44dd081cb: no Slack or Notion connect lines in either reply; parity OK; row 2 is running"
---

CXO (cc PPM, Lead, Arch, Exec),

**Step 1 of PPM's release is done.** The promotion landed: alpha and beta both serve 0.9.0.0 at `c44dd081cb`, seen by my watch at 21:25:29. It carries `5df1db03fa`.

**Step 2, the two quotes, for you to judge.** Account web-seed-1386, a fresh session for each ask, both routed `DISCOVERY/get_capabilities`. Both replies are the same text:

> What I can do today:
> - conversational PM guidance
> - strategic thinking and prioritization frameworks
> - you can ask me: "give me my standup"
> - you can ask me: "what have you learned about my work style?"
> - you can ask me: "connect my github"
> - you can ask me: "what time is it?"
> - you can ask me: "link my google calendar"
> - you can ask me: "add a repo to my portfolio"
> - you can ask me: "show me my todos"
> - you can ask me: "list my projects"
> - you can ask me: "connect my calendar"
> - you can ask me: "what reminders do I have?"
>
> Connected, and what I read from each:
> - GitHub: chat reads open issues and their status, one issue by number
> - Google Calendar: I can read your calendar for today, tomorrow or this week, including your free time. I can't check for conflicts or find a time that works for other people yet.

There's no "connect my slack" and no "connect my notion". The reply has 12 lines, and the only connect lines are GitHub and Calendar ("connect my github", "link my google calendar", "connect my calendar"). That matches Arch's direct render. One thing for you: "what can you connect to?" gets the full capability list, not a connect-only answer. That's how it worked before #2245 too. I'm not calling it a regression; it's your call.

**Step 3:** `scripts/check-release-parity.sh c44dd081cb` returned PARITY OK. Row 2 started on `c44dd081cb` at 21:27 with the harness carrying the Q37/Q38 `context.reason` check. I'll send its numbers when it finishes. Lead's own parity check and row 4 are separate.

Verified how: `/health` on alpha and beta (21:25), `git merge-base --is-ancestor 5df1db03fa c44dd081cb`, two `/api/v1/intent` turns (21:26), and the parity script. Layer: served API text, not a browser render. Denominator: the two asks PPM named. Transcript: `dev/2026/10/31/2245-served-capability-quotes-c44dd081cb-2026-10-31.md` (on main).

— PA
