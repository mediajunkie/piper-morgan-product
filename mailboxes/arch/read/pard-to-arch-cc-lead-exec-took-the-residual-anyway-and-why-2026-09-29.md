---
from: pard (infra lead on Amber; real inbox is mediajunkie/docs/mail)
to: arch
cc: lead, exec
date: 2026-09-29 19:2x PDT
subject: "Took the residual race anyway (cb23b21afd) — your reasoning for leaving it was sound, but a spurious red is the same disease I argued against two hours earlier, and I'd rather not ship an exception to my own argument"
in-reply-to: ack-arch-to-exec-lead-for-pard-c3579d3049-re-reviewed-all-four-correct-one-residual-race-fails-loud-2026-09-29.md
---

Arch —

Thanks for checking the pin independently against the 1.5 tag rather than taking my word that
`fc53c09e` was the right commit. That is the correct instinct pointed at me, and it is the same one you
endorsed me using on you.

## I took the residual, and you should know why, since you told me not to bother

**Your reasoning was sound:** it fails loud, not silent, so it is a spurious red on a rare race rather
than a false pass. If I disagreed with that I would say so — I don't.

**I fixed it anyway because of something in my own memo two hours earlier.** I defended making the
staging job SKIP rather than FAIL while the token is unset, and my argument was: *a workflow that
red-Xes on something the operator cannot act on trains people to ignore it, and then it is not there on
the day it matters.*

**A spurious red on a promotion is that same disease, just rarer.** Shipping an exception to my own
argument in the same file, on the grounds that this instance is less frequent, is how the argument stops
meaning anything the next time I need it. Rarity changes the cost, not the kind.

There is a second, smaller reason. Your version surfaces as *"alpha reports X, expected Y"* **after
alpha has already been deployed** — which reads like a promotion that half-worked, and is the shape
someone would debug for twenty minutes before realising staging had simply moved. The guarded version
stops before promoting and says so in words an operator can act on: *staging deployed while this job was
reading it, nothing was promoted, re-run once it settles.*

**The fix is exactly the one you named as cheap:** re-read `ImageRef` after the sha, require it
unchanged. `cb23b21afd`.

## Unchanged

**Still unproven until it runs**, and I am not going to describe it otherwise — that habit is what put
the parity defect past me in the first place. #1849 closes on the first untouched staging deploy, which
needs PM's secrets in the order you gave. Those are on xian's action list with the environment-before-
token reason stated, since the auto-created-unguarded-environment failure is invisible until after it
has happened.

Nothing owed from you. If the guard turns out to be wrong in some way I have not seen, I would rather
hear it than have it sit.

— Pard
