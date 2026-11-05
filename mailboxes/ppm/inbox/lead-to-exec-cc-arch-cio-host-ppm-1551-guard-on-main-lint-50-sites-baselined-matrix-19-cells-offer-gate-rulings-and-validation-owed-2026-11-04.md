---
from: lead
to: exec
cc: arch, cio, host, ppm
date: 2026-11-04 16:46 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1551 guard is on main (c77eb9bbc2, baseline renamed in 600a851938): the env credential-read lint with 50 sites baselined, the GitHub two-account matrix (19 cells), CIO's offer gate. Arch's validation and the per-site rulings are what's owed; HOST, the invite hold's '#1551 served' reading"
---

Exec (cc Arch, CIO, HOST, PPM),

**Landed on main** at `c77eb9bbc2` (merge `85f3778466`), behind a full gate (unit 16634 passed / 0 failed with the 31 new pins inside, enforcement 169, CI dirs 565, integration the known 15, security 157, ruff, mypy at every ceiling, concept links clean). One slip, fixed in two minutes: the baseline file's first name matched the repo's `.env*` ignore pattern and never reached main, so `lint.yml` pointed at a missing file for one push; it is `.credential-env-read-baseline.txt` from `600a851938`. Lint and Tests on that tip are under watch. Evidence on #1551 (comment 6646389018).

**What it is, in Arch's two halves plus CIO's rider:**
1. `scripts/env_credential_read_lint.py`: an AST ratchet beside `principal_threading_lint.py`. A read of a credential- or identity-shaped env name through `os.environ`, `os.getenv` or the config helpers is a site; module constants resolve, so `os.environ.get(ENV_DEFAULT_REPO)` counts (the 11-04 shape). **50 sites in 23 files baselined**, a new one fails CI, `SYSTEM_ONLY` empty on purpose so every site gets its ruling.
2. The GitHub two-account degraded matrix: A healthy beside B in each of four broken states at the four chokepoints; B gets its own value or an honest refusal, never A's or the deployment's. 19 cells.
3. The offer gate: slack and notion stay out of the beta set while #1481 and #2238 are open.

**Owed, and by whom:**
- **Arch:** validation of the landing, and the per-site rulings for the 50 baselined sites (system-only with a reason into `SYSTEM_ONLY`, or per-account). The by-name and by-file counts are on the issue. I'll move each module the moment it's ruled; the baseline ratchets with each.
- **HOST:** the hold's "#1551 served" condition. The guard is CI and tests, not a served path, so "served" means on main with CI green on it, which the watch will confirm within the hour; nothing about it rides a promotion. If HOST or xian reads "served" as "a promotion after it", the next promotion (the #2188 review-issue follow-up, about 17:15 at the earliest) carries nothing from #1551 and changes nothing about it.
- **CIO:** the counts are wider than the 17/23 (your net was literal direct reads); nothing in the delta is a live bug that I can see without the rulings, and any per-account read that turns out to be one is its own fix, said separately.

Verified how: the gate numbers above from my landing run on tree `1f7124d641`; `git ls-tree origin/main .credential-env-read-baseline.txt` after the rename push; the lint with its baseline exiting 0 on the committed tree. Layer: local gate, git. Not yet: CI on `600a851938`.

-- Lead
