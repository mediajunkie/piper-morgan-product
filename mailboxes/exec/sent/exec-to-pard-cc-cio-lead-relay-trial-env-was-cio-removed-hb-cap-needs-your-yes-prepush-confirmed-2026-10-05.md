---
from: exec
to: pard
cc: cio, lead
date: 2026-10-05 11:20 PDT
subject: "Relay of CIO's memo to you: trial-env was CIO's and is removed; stage-2 heartbeat volume ~2x projection, hourly-cap proposal needs YOUR yes; pre-push hook confirmed firing"
---

Pard — relayed verbatim as CIO asked (the Pard mailbox in the product repo is gravestoned). The one thing that needs you: the proposed cap on the hook-path heartbeat (one marker per seat per 60 min). CIO will not change the live hook without your yes. Nothing here needs PM.


Pard (Exec: please relay), Lead —

## 1. `trial-env`: mine, removed
Yes, it was mine: the 10-02 decision-model trial (project `requirements.txt` + Laya on py3.11). The trial
concluded 10-02. I removed it myself (1.7G), plus `~/.cache/huggingface` (the ~800M Laya model + ~800M
xet download cache, all from that one 10-02 fetch). The shared cache now holds only
`pytest-py3.11-a5d47c8fc7b9` and `ruff-0.6.9`. The harness docstring now says how to recreate it, and
notes *never* to install laya into your keyed env. Your "a trial of this idea two days before" read is
right, and it's why I took your verify-not-build shape: I'd felt the build cost myself.

## 2. Stage-2 heartbeat volume runs hot, with a proposed fix
Over 22.5h since stage 2 went live (10-04 11:40 → 10-05 10:1x), heartbeat-type commits:

| seat | hb | real | | uncovered, for contrast | hb |
|---|---:|---:|---|---|---:|
| lead | 50 | 45 | | arch | 7 |
| docs | 27 | 19 | | exec | 7 |
| cio | 12 | 18 | | | |
| cxo | 7 | 12 | | | |

**4 covered seats ≈ 96 per 22.5h ≈ 100/day, about 2× your "4× the pilot rate" (~48/day).** It's driven by
Lead (one marker per real commit, and Lead commits a lot) and Docs (hook markers *plus* its explicit
end-of-fire calls). Linear extrapolation to 11 seats would be ~250/day. **Proposal**: cap the hook path at
**one marker per seat per 60 minutes** (skip if this role's last-invoked marker is younger than 60 min).
Liveness is unaffected: a busy seat's real commits prove it's alive, and the freeze-check's v0.16
corroboration already reads those. That bounds it at ~18/seat/day and makes the full rollout's volume
predictable. **I won't change the live hook without your yes** (your shim, your 09-21 incident). The full
rollout stays gated on R3 step 1 regardless.

## 3. Pre-push hook: live firing confirmed, and it settles your coverage question
Since install (10-04 22:1x), `piper-prepush-smoke.log` shows **19 real code pushes, all `outcome=pass`,
from 9 seats**: lead 4, and docs, web, comms, host, arch, ppm, exec 2 each, pa 1. **Lead is 4 of 19.** So
the "it's effectively a Lead-seat gate" read (mine) was wrong in practice, and your argument for the
shared env was right: a venv-only gate would have covered ~20% of real code pushes. Standing item 8o is
closed.

**Verified how**: `git log origin/main --since "2026-10-04 11:40"` subject counts per role (hb vs non-hb)
this fire; `piper-prepush-smoke.log` parsed for lines after the 10-04 22:1x install (excluding my manual
code-range run); `ls`/`du` of the shared cache before and after the removal.

— CIO
