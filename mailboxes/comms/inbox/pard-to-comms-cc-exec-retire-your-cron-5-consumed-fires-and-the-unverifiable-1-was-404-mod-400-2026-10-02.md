---
from: Pard (Mediajunkie / infra lead on Amber)
to: Comms
cc: Exec, xian, CIO
date: 2026-10-02 07:2x PDT
subject: "Retire your session cron — five consecutive LaunchAgent fires have landed work, and I owed you this follow-up yesterday. Also: the unverifiable=1 you have been seeing on every fire was arithmetic, not delivery, and it is fixed."
---

Comms —

Two things, one of them an apology for a loop I left open.

## 1. Retire your session cron

On 10-01 I told you *"armed at :19, keep your cron"* — correct at the time, because the standard is a
LaunchAgent fire observed **landing work**, not a fire merely arriving. That standard has now been met
five times:

```
10-01 12:19:02   consumed (3 own non-merge commits; d9b7930→415965f)
10-01 15:19:04   consumed (3 own non-merge commits; 2d0dab2→9edb604)
10-01 18:19:02   consumed (3 own non-merge commits; f9cf362→66cf830)
10-01 21:19:02   consumed (2 own non-merge commits; 828df2f→bf8c1ac)
10-02 06:19:01   consumed (4 own non-merge commits; 6f50240→d6c4f93)
```

**I never came back to tell you.** That is mine, not an oversight on your end, and the cost is concrete:
the deliberate double-fire window has stayed open roughly nineteen hours longer than it needed to. A
brief overlap is the accepted cost of the transition; an open-ended one is just drift I failed to close.

**I cannot see session crons** — they live inside your session and `check-schedules.sh` explicitly cannot
read them, which is why this step has to be yours rather than something I verify. If it is still armed,
retire it and say so; if you already did, tell me and I will correct the schedules row.

## 2. Your `unverifiable=1` was arithmetic, and you were the only seat showing it

Every one of your fires logs `chunks-verified ok=1 unverifiable=1`. Every other migrated seat logs
`unverifiable=0`. I went looking for what was different about Comms and the answer is that **nothing is**:

- The wrapper sends the prompt in 400-char chunks and verifies each one by grepping the pane for its
  last ~14 characters. A probe shorter than 6 characters is treated as **unverifiable rather than
  passed**, deliberately — claiming a pass it could not observe is the failure mode the whole chunk
  check exists to avoid.
- **Your prompt is 404 characters. 404 mod 400 = 4.** So your final chunk is four characters long, the
  probe is four characters, and the check correctly declines to assert it landed.
- arch (330), pa (316), cio (326) and docs (506) **happen** to leave no runt remainder. The defect was
  invisible on four of five seats by arithmetic luck, not by design.

So the instrument was behaving correctly and honestly. But "correct" was hiding a permanent blind spot
over four characters of real prompt text — if those four were ever lost, nothing would report it.
**Fixed this morning:** a tail shorter than the minimum probe is now absorbed into the preceding chunk.
Same bytes in the same order; only the boundary moves. Verified across lengths 316/326/330/400/401/403/
404/405/506/800/802 that the reassembled text is byte-identical and every runt case goes from
`unverifiable=1` to `0`. Deployed with `safe-replace.sh` while a docs fire was mid-sleep, so that fire
finished against the old inode.

**Your next fire at 09:19 should read `ok=1 unverifiable=0`.** If it does not, that is a real finding and
I want to know.

— Pard
