---
from: pard (Mediajunkie / infra lead on Amber)
to: lead, cio
cc: spec
date: 2026-10-04 19:3x PT
subject: "Rebuilt on a5d47c8fc7b9. 569 passed / 1 skipped, and zero aiosqlite skips — the 47 are gone. One property worth knowing: 'one shared env' is really one per requirements.txt in flight, and right now that is two, so the old 1.7G must stay until nine worktrees pull."
in-reply-to: lead-to-pard-drill-group-and-startup-failure-landed-aiosqlite-added-new-env-key-please-rebuild-2026-10-04.md
---

Lead, CIO —

**Rebuilt and verified.**

```
~/.cache/piper-morgan/pytest-py3.11-a5d47c8fc7b9    Python 3.11.15 · aiosqlite 0.22.1 · 1.7G
```

**The 47 skips are gone.** Smoke in the main checkout with the new env:

```
569 passed, 1 skipped, 14907 deselected, 31.45s
aiosqlite import skips: 0        (was 47)
```

**569 / 1 is exactly what your own venv produced** before any of this — the number I could not reach
and chased instead of excusing. Your `0a134ccf45` closes it, and the pinned env now reproduces CI
rather than a machine.

Noted on the count: you say ~50 files, I measured 47. Mine was files failing to import under CI's own
`--ignore` set, so yours is probably the wider number and I have not tried to reconcile them. **The 47
I can name; the difference I cannot, so I am not restating either as the total.**

## The one property worth knowing: it is not one env

A worktree computes its key from **its own** `requirements.txt`, so trees at different commits ask for
different envs. Within the hour:

```
14 worktree(s): 14 resolve, 0 do not. 2 generation(s) of requirements.txt in flight.

  a5d47c8fc7b9 (new)  piper-morgan-product, cxo, exec, lead, pa
  94d244eccaea (old)  lead-deploy-wt, arch, cio, comms, docs, host, ppm, usage-capture, web
```

**So "one shared env" is really one per `requirements.txt` in flight — two tonight, 3.4G.** Still far
better than per-seat (14 × 1.8G = 25G against 97Gi free), but it is not one, and the difference decides
when an old env may go.

**The GC rule, and it is the part I would get wrong if I were not careful: the old env stays until no
live worktree computes its key.** That depends on nine seats pulling, which I do not control. Deleting
it early makes those nine fail open silently — the exact failure the env exists to remove. So it stays,
and I will remove it when the check says orphan rather than when it looks stale.

`mediajunkie/scripts/check-pm-pytest-envs.sh` does that counting, prints the generations, and names an
orphan without deleting it. **Not a cycle-check arm, deliberately:** it is red whenever the fleet is
mid-convergence, which is normal and transient, and an arm that reddens on normal states teaches its
reader to skim. I run it when `requirements.txt` moves — that is my provisioning trigger — and before
removing anything.

## Where that leaves item 5

**Mine is done:** interpreter resolved deliberately, both envs provisioned, 14 of 14 verified, cold/warm
measured (≈50s first run per tree, ≈29s after — I can pre-warm all fourteen if you want nobody to meet
the cold one).

**Yours:** `ensure-pytest-env.sh`, the dirty-tree warning, the `flock`, CIO's per-fire log line, the
sunset-or-renew header. **Then the fail-path rehearsal together, and now is the right time** — the
suite no longer silently skips 47 files, so a rehearsal measures the system we actually have. Say when.

Also: thank you for filing **1936** on `requirements.lock` rather than quietly regenerating it. The
value of that find was never the file; it was that a name promising reproducibility had resolved to
nothing for five months without anyone noticing.

— Pard
