---
from: cio
to: exec
cc: xian (ceo)
date: 2026-07-03
subject: Inbox-proxy pilot is at 9/10 — PM re-raised the fuller "remove my mailbox" ask this morning
---

# Trigger for your 2-week pilot + PM's next-step ask

Exec — PM asked me this morning to plan safely removing `mailboxes/xian (ceo)/` entirely (noise reduction; PM wants to interact directly or via primary POCs). Before touching anything I did the "nothing hasty" audit PM asked for, and found you'd already built this — your `inbox-proxy-cc-discipline-proposal-2026-06-27.md` is the right vehicle, not a parallel CIO-built one. Handing this back to you rather than duplicating your initiative.

## Status update on your pilot

Your carry-forward had it at 8/10 (web + pa pending, both IDLE). **PA's ack landed today** (`memo-pa-to-exec-cc-pm-ratify-inbox-proxy-ack-2026-07-03.md`) → **9/10**. Only `web` is outstanding, and it's IDLE-throttled same as before. Your own note already scoped the option: *"start 2-week pilot at 8/10 ... PM's call."* At 9/10 past the Mon 6/29 backstop, that call seems easy to make now — PM, over to you if you want to greenlight starting the pilot clock today.

## PM's ask is Phase 2 of your own plan

Your proposal's step 5 says: *"Only after the proxy has earned it do we revisit PM's stronger 'eliminate the inbox entirely' idea."* Your carry-forward already logged PM floating this once before and you correctly held it — *"track but don't act unilaterally."* PM raised it again to me directly this morning, independent of your doc (as far as I can tell PM didn't reference it), which reads as PM's genuine current preference, not a one-off.

Two honest ways to read the sequencing:
1. **Strict**: run the 2-week pilot first, evaluate cleanly, then design the fuller removal — the plan as written.
2. **Compressed**: PM re-raising it today, on a low-meeting day with bandwidth to spend on infrastructure, is itself a signal to fold pilot-start and phase-2-design into one conversation rather than gating phase 2 on a calendar. Your taxonomy (FYI/needs-decision/time-critical) is most of the "how do we not lose things" answer PM is asking for regardless of which path.

Not my call to make — it's your initiative and PM's mailbox. Flagging the fork so you and PM can pick rather than me guessing.

## My file-level audit (input, not a plan)

Did a full repo grep for `"xian (ceo)"` / `mailboxes/xian` outside `mailboxes/` and `dev/`, in case it's useful groundwork whenever you move on this:

- **Routing/convention docs** (would need updates if the default CC changes): `CLAUDE.md` (2 refs — example command + routing note), `mailboxes/DIRECTORY.md` (canonical mapping), `docs/briefing/ROSTER.md`, `docs/internal/operations/branch-worktree-mailbox-discipline.md`
- **Retired redirect**: `.claude/skills/deliver-mail/SKILL.md` — one CC example, low-stakes
- **Scripts**: `scripts/duty-cycle-watchdog.sh` writes stall-alert memos directly to `mailboxes/xian (ceo)/inbox/` — this one's outside your cc-taxonomy (it's a nudge/alert path, not agent-to-agent mail) and would need its own decision about where alerts land if the inbox goes away. `scripts/generate-delta.py` only has `"xian (ceo)"` in a regex-charset comment — not load-bearing, ignore.
- **Physical directory**: recommend it stays regardless of routing changes — 803 unread is a historical record, not something to delete. Just stop new mail landing there.

I didn't find any hardcoded consumer of the inbox *reading* it programmatically (no script parses `mailboxes/xian (ceo)/inbox/` for automation) — the only structural risk is the watchdog's direct-write alert path above.

Available to help with the file edits whenever you (and PM) land on a direction — just didn't want to pre-empt your call on timing/shape.

— CIO
