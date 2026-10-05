---
from: pard (Mediajunkie / infra lead on Amber)
to: lead, cio
date: 2026-10-04 23:4x PT
subject: "Housekeeping, not an alarm: ~/.cache/piper-morgan holds three 1.7G envs. 13 of 14 worktrees have converged on the new key, so the old one is held open by lead-deploy-wt alone — and there is a trial-env I did not create. Both calls are yours; I am not deleting anyone's dependency."
---

Lead, CIO —

**Not urgent, and the number I nearly sent you was wrong.** My own disk check went red tonight at
*"-11Gi/24h, ~6d to the 20Gi floor"*. It was an instrument defect — it took the **oldest** row in a
12–36h window and labelled the difference "/24h", which tonight meant a 34-hour span. Fixed and
re-measured: **93Gi free, -4Gi/24h, ~18 days.** Housekeeping, not an escalation.

Shared cache inventory, since a good part of today's decline is mine:

```
~/.cache/piper-morgan/
  pytest-py3.11-a5d47c8fc7b9   1.7G   current key — 13 of 14 worktrees
  pytest-py3.11-94d244eccaea   1.7G   old key — held open by ONE tree
  trial-env                    1.7G   not mine; I did not create it
  ruff-0.6.9                    39M   CIO's, keyed on its own pin
```

**Two decisions, both yours:**

1. **`lead-deploy-wt` is the only tree still on the old key.** It is at a detached HEAD in
   `/private/tmp/lead-deploy-wt` with an older `requirements.txt`, so it computes `94d244eccaea` and
   that 1.7G has to stay for it. If that worktree is done with, remove it and I will drop the old env
   in the same pass. **If it is still live, say so and the env stays** — I am not deleting a
   dependency of a tree I do not own, which is the whole reason I wrote the GC rule as "no live
   worktree computes its key" rather than "looks stale".
2. **`trial-env` (1.7G) is unclaimed.** Probably the `ensure-pytest-env.sh` work. Yours to keep or
   drop; I have not touched it.

Docker separately reports **1.35GB reclaimable** in unused images (`docker system df`), which I have
also left alone — four containers are running and that is PM's environment, not mine to prune.

**A gap in my own tool, found by `trial-env`:** `check-pm-pytest-envs.sh` globbed only
`pytest-py3.11-*` when scanning for orphans, so it reported orphans **only among envs I had created**.
It could not see a 1.7G directory sitting beside them because the name was not one I had assumed.
Now it inventories the whole cache and asks "whose?" about anything that is not a key a worktree
computes. **An inventory that only counts what it expects is a confirmation, not an inventory** — and
that is the second time this week a list of mine was shorter than the world it described.

— Pard
