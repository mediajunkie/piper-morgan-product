# Mail v4 pilot review (2026-11-05)

**Reviewer**: CIO (mechanism owner). **Written**: 2026-11-05 06:09 PST. **Pilot**: exec and cio from 10-08, lead from 10-12.
**Window**: after the 10-22 review (10-22 10:30) to 11-05 06:10. **Inputs**: Exec's audit (`dev/2026/11/05/mail-v4-audit-exec-2026-11-05.md`), `scripts/mail4.py` over `piper-morgan-mail` origin/main, `scripts/memo-volume.py` and `git log` over this repo's origin/main.
**The question set for this review** (decisions.log 2026-11-03 13:18): xian judges v4 "as a routing fix" ("this is about routing bottleneck"). Memo volume is a separate question, R16, read 11-11.

## Verdict

v4 delivers. Two reviews and two audits found no missed message. But at three seats it can't answer xian's question, because it carries under 1% of the cohort's mail. Of 2,166 v3 memos in the window, 32 had only pilot participants. Keeping the pilot as it is produces no new information. The decision is whether to widen it to every seat in this repo, and that is xian's call.

**Recommendation: widen to all seats,** on the terms below, with a review two weeks after the switch.

## What the window shows

| Measure | Result | Verified how |
|---|---|---|
| Missed required-ack messages | **0.** Exec: 14 of 14 acted on or needing no action. `check`: 0 overdue | Exec's audit (ack log plus his session logs); `mail4.py check` at 06:06 |
| Canaries, last full week (10-29 to 11-04) | **20 of 21 seat-days.** CIO 7, Lead 7, Exec 6 (missed 10-31). All passed. The 10-22 fix (the first `inbox` runs it) held: before 10-28, Exec missed 4 days and Lead 5 | canary message dates per sender, script over `all_messages` |
| v4 traffic | **19 messages in 14 days** (CIO 12, Lead 5, Exec 2). None from 11-03 until Exec's message this morning | `memo-volume.py 2026-10-22 2026-11-05` |
| v3 traffic | **2,210 memos in 14 days** (158 a day). Lead 472, Arch 304, Exec 232, CXO 229 | same run |
| Why v4 is idle | The pilot rule. Pilot seats sent 757 v3 memos; 32 of them had only pilot participants, so about 96% had to go v3. Those 32 are a smaller habit leak beside 19 sent on v4 | script over each v3 memo's `from:`, `to:` and `cc:` (2,166 with front matter) |
| What v3 costs main | **3,004 `mail(` commits, 31% of main's 9,774** in the window, touching 18,063 mailbox files | `git log origin/main --grep='^mail('` |

## Why the routing question needs the wider pilot

What v3 costs is on main itself. A third of main's commits are mail, and they touched 18,063 mailbox files for 2,210 memos, about 8 per memo: a copy per recipient, the sent copy, the move to `read/` and the manifests rewritten each time. Those writes race other seats' pushes. Yesterday CIO hit a #1731 manifest refusal on Arch's inbox and a non-fast-forward on a log push. Filenames are capped at 180 characters because they carry the routing. v4 moves all of that into one file per message in a private repo, with acks written by their own seat. None of it shows at three seats. With 96% of the pilot seats' own mail going v3, they live on v3 too.

## Terms for widening (proposed)

1. **Every seat in this repo,** at once. Widening one seat at a time keeps the mixed-thread rule, so most traffic stays on v3 until the last seat joins.
2. **v3 stays readable and keeps working** for two weeks as the fallback. A seat that can't send on v4 sends on v3 and says so in its log. External agents (Janus, Pard, Dispatch) keep their own routing.
3. **No change to mail's guards** for public-repo exposure, because v4's repo is private. The people-details rule (CLAUDE.md hard rule 8) still applies to any text copied back into this repo.
4. **The same success and stop criteria** as the pilot (`docs/internal/operations/mail-v4-pilot.md`), plus one: the share of main's commits that are `mail(` falls from 31%.
5. **Work before the switch** (CIO's): `roles.yaml` for every seat; the duty-cycle-tick skill and `check-mailbox` read v4 first; Pard checks that his wake watcher covers every seat (it reads `mail4.py inbox --ids` today).

## What this review does not measure

- Whether a seat acted on a v4 message well. Exec's audit checks that a message was acted on, not how well.
- Memo volume. v4 doesn't reduce how much is written; R16's week (11-04 to 11-10, read 11-11) sizes that separately.
- Anything about v4 at 11 seats. These numbers are from 3 seats and a few messages a day.
