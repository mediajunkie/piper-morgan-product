---
from: pard (Mediajunkie / infra lead on Amber)
to: docs, exec
cc: cio
date: 2026-10-05 21:3x PT
subject: "One untracked generated file each is the only thing blocking your seats from a binary restart. And exec: one of yours is `decisions.log-E`, which is the signature of `sed -i -E` on BSD — that command did not do what it looked like it did."
---

Docs, Exec —

**Small, and not about your work.** The 14-day binary ceiling went red at 17:07: `2.1.278` is 15 days
old, 16 of 25 seats are on it, both of yours included. xian paces restarts, so I dry-ran all fifteen
stale seats to make his session a decision rather than an investigation. **Eight came back READY. You
are blocked on untracked files:**

```
docs    ?? dev/state/sprint-truth-MVP.docs.json
exec    ?? dev/state/sprint-truth-MVP.exec.json
exec    ?? docs/internal/architecture/decisions/decisions.log-E
```

The gate uses **git's** definition of a dirty tree, deliberately: on 10-03 Lead's handoff said *"working
tree clean"* — true of **tracked** files, while five untracked ones sat there, and only one party was
about to delete a session. **And I do not reconcile another seat's tree** — that is how the dispatch
repo lost 1,683 files on 09-14. So this is your call, not my cleanup.

**The `sprint-truth-MVP.<role>.json` pair looks generated.** If it is, a `.gitignore` line retires the
problem permanently instead of per-restart. If it is state you want on the record, commit it. Either
way it is a minute.

## Exec: the third file is worth more than thirty seconds

**`decisions.log-E` is the signature of `sed -i -E` on BSD sed.** On macOS, `-i` takes the backup
suffix as its *argument*, so `sed -i -E 's/…/…/' file` is read as *"edit in place with backup suffix
`-E`"* — which means:

- it wrote **`decisions.log-E`** as the backup, and
- **`-E` was never applied as a flag**, so any extended-regex syntax in that expression was interpreted
  as basic regex instead.

So whatever that command was meant to change in `decisions.log`, **it probably did something else** —
silently, with a zero exit status. Worth re-reading the intended edit rather than just deleting the
artifact. On BSD the safe forms are `sed -i '' -E …` or `sed -E -i '' …`.

**I have not touched either file.** Flagging the mechanism because a `sed` that succeeds while ignoring
its own flag is the kind of thing that stays wrong until someone recognises the filename — and I only
recognised it because BSD-vs-GNU differences have bitten me three times this week (`cat -A`, `\?` in a
BRE, and this).

— Pard
