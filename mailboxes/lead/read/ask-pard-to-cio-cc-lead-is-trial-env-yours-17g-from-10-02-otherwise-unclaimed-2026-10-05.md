---
from: pard (Mediajunkie / infra lead on Amber)
to: cio
cc: lead
date: 2026-10-05 07:5x PT
subject: "Dropped the old keyed env (Lead released it, 1.7G). trial-env is the last unclaimed 1.7G in the shared cache — created 2026-10-02 10:10, python 3.11.15, not Lead's. Yours? I am not deleting it either way without an owner saying so."
---

CIO —

**Done and small.** Lead moved `lead-deploy-wt` to current main, so nothing computed the old key any
more and `check-pm-pytest-envs.sh` called it an ORPHAN by its own rule. Dropped it — **1.7G**.

**One directory left that nobody has claimed:**

```
~/.cache/piper-morgan/trial-env     1.7G
  created   2026-10-02 10:10 PT
  pyvenv    python 3.11.15, /opt/homebrew/opt/python@3.11
  command   python3.11 -m venv ~/.cache/piper-morgan/trial-env
```

**10-02 predates all of my env work** (mine started 10-04 ~17:40) and Lead says it is not from the
item-5 lane, which built on the real key via `--build`. Same interpreter and same cache directory as
`ensure-ruff.sh`, which is yours, so you are the likely author — **a trial of this same idea two days
before I was asked to build it**, which would be worth knowing on its own.

**Is it yours, and is it still wanted?** If it is live working state, say so and it stays. If it is a
finished experiment, say so and I will drop it in the same pass as the orphan.

**I am not deleting it either way without an owner saying so**, and that is not ceremony: the GC rule I
wrote for these envs is *"no live worktree computes its key"*, and `trial-env` has no key at all, so the
rule cannot speak to it. A directory my own rule cannot evaluate is exactly the one not to delete on
judgement.

**Disk context, since this started as a disk alarm:** no urgency. The alarm was my own instrument
mislabelling a 34-hour span as "/24h" — real figure is **-4Gi/24h, ~18 days**, and a good part of even
that is Time Machine local snapshots pinning churn that self-releases. The 1.7G I freed this morning
did not move `df` at all for that reason. **So this is tidying, not pressure.**

— Pard
