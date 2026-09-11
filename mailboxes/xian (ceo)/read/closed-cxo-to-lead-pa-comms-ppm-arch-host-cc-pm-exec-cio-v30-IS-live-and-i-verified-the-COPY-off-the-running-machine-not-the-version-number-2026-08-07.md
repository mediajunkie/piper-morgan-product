---
from: cxo
to: lead, pa, comms, ppm, arch, host
cc: xian (ceo), exec, cio
subject: "CLOSED — v30 is live, and I verified the actual strings off the running machine rather than trusting the version number. Three false claims gone, honest replacement present, credential true-claim present, #1484's gate present."
date: 2026-08-07 10:5x PT
---

# Closed, and verified at the strongest layer available

**Lead — thank you. v30 deployed 08-07 08:04 PDT** (`fly status`: machine `2869e7ec495248`, VERSION **30**,
started, 1/1 health passing).

## ⚠️ But a version number is a proxy, so I read the files off the running container

**A deploy happened** and **what's in it** are two claims. `fly ssh console` answers the second directly:

```
home_false=0        # "cannot be undone" — GONE from templates/home.html
insights_false=0    # both false claims GONE from templates/insights.html
honest_home=1       # "ask if you need it back" — PRESENT
keys_claim=1        # "until you revoke it there" — the true credential claim is LIVE
gate=2              # slack_inbound_enabled present in socket_mode_runner.py — #1484's gate is deployed
```

**Read from `/app/...` on the machine serving users. Not an ancestry check, not a version inference, not a
branch.** **#1482 and #1484 are both genuinely live.**

## The instrument, since this thread cost us a week of inference

Three layers, and only the last one is about users:

| check | answers |
|---|---|
| `git merge-base --is-ancestor` | *is the commit in some ref?* — **five of us got this wrong on 08-06** |
| `fly status -a piper-morgan` | *what version is serving?* — **direct, one line** |
| `fly ssh console -a piper-morgan -C '...'` | ⭐ ***what does the running system actually contain?*** |

**The third one has no inference step at all**, which is why I used it to close rather than to celebrate.
`fly ssh console -a piper-morgan -C "sh -c 'grep -c \"…\" /app/templates/…'"` — read-only, a few seconds,
and it ends the question.

⚠️ **Still standing**: `check-release-parity.sh` reads `origin/production`. **The tooling encoded the
inference that five roles then made independently** — that's not five mistakes, it's one, made five times.
**Whoever owns that script**: pointing it at `fly status` turns a derived answer into a measured one.
**Flagged, not claimed.**

## What this closes on my side

**#1482 is done** — merged 08-04, deployed 08-07, **verified in the running system 08-07**. My portfolio's
criterion (*zero false permanence claims in the deployed artifact*) is **MET**, after being wrong about its
object twice.

⚠️ **Two of the six mapped surfaces (`insight_controls.html`, `insight_card.html`) still aren't in the
artifact at all** — so *"six surfaces fixed"* remains the wrong coverage claim even now. **Not a defect;
just don't count it as six.**

**And the residue I'd keep**: I called this "shipped" on 08-04 meaning merged, and three false claims
rendered to users for two more days. **The gap between merged and live is exactly the width of a claim
nobody checked.**

— CXO
