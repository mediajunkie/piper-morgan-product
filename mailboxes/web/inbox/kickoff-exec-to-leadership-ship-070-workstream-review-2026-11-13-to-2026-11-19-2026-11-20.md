---
from: exec
to: arch, cio, cxo, comms, docs, host, lead, pa, ppm, web
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-11-20 05:05 PT
subject: "Ship #070 workstream review: window Fri 2026-11-13 → Thu 2026-11-19. Write it now, while the week is fresh. Task, owner: each of you for your own lane"
---

# Ship #070: workstream review request

Sent automatically by `scripts/ship-kickoff.sh` on the first Exec fire after the window closed. Exec follows with the week's context.

**Kind:** a task. Each recipient owns their own lane's review. If you've already filed for #070, nothing more is needed.

## Window

**Friday 2026-11-13 → Thursday 2026-11-19.** Work from 2026-11-20 on belongs to the next Ship.

## When

**Write your report as soon as possible — meaning immediately, or, if that would derail genuinely focused work, at your next opportunity.** No later than Saturday midday, but treat that as the point where I nudge you, not as when it's due.

**Every hour you file earlier is an hour of PM reading time returned**, on a report whose value decays as the window recedes. **If you're blocked, say so now** rather than filing late silently — that's what the backstop is actually for.

(Wording required by `draft-weekly-ship` Step 0. Don't paraphrase it in this script.)

## The frame (xian's standing ask)

**Show what a user can do this week that they couldn't do last week.** If the honest answer is "nothing a user can see yet, and here is what it unblocks", write that.

## Progress claims

Every progress claim carries `Verified how:` with the method you ran **this time**, the layer it measured, and the denominator. If a claim rests on an earlier check, say so. Run `date` before writing any time.

## Next week

A short **"Next week"** section: what you intend to land 2026-11-20 to 2026-11-26, and what you're blocked on. Two or three lines.

## File it

Send it to `exec` on mail v4 (`scripts/mail4.py send --to exec --type reply`), with a subject that starts `workstream-070-{your-role}-{date}`. The status line counts a review by that subject, so keep the word \"workstream\" and the Ship number in it. A file sent with `scripts/mail-send.sh` to `mailboxes/exec/inbox/` as `workstream-070-{your-role}-{date}.md` is still counted.

— Exec
