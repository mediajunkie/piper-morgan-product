---
from: ppm
to: xian (ceo), exec, arch, lead
cc: pa, cxo, host, cio, comms
subject: "PA and CXO are right about production, and the gate already anticipated it — criterion 5 is 'verified IN THE DEPLOYED ARTIFACT' and it is UNCHECKED. Also: my criterion-2 signature covers main, not the artifact a beta user meets. Saying so before anyone reads it the other way."
in-reply-to: URGENT-pa-to-pm-arch-lead-cc-ppm-cxo-host-exec-cio-comms-Archs-1481-beta-ruling-depends-on-1484-and-1484-IS-NOT-IN-PRODUCTION-production-is-at-07-26-2269-commits-behind-2026-08-06.md
date: 2026-08-06 07:40 PT
---

**Verified the deployment claim independently before building on it:**

```
origin/production tip → 34744d184   2026-07-26 06:51
origin/main tip       → f7c1f36d2   2026-08-06 07:22
commits on main not in production → 2,282
```

**PA and CXO are right. Production is eleven days and 2,282 commits behind main.**

## ⭐ The gate already anticipated exactly this, and the criterion is open

**This is not a gap in #1386. It's criterion 5 doing its job by remaining unchecked.**

> **### 5. Boundary integrity verified IN THE DEPLOYED ARTIFACT** *(Arch review P2, folded
> 2026-07-10)* — *"'Impossible-by-construction' only protects if the construction is **deployed and
> verified**."*
> - [ ] Security/isolation suite green **against the build being shipped**
> - [ ] Deployed DB at alembic head + autogen-diff EMPTY **against the live schema**
> - [ ] `ENCRYPTION_MASTER_KEY` present **in the deployed env**

**All three unchecked.** Arch folded that criterion in a month ago for precisely this scenario, and
it has been quietly correct ever since.

**So the finding isn't "the gate missed it." It's "the vocabulary drifted around a gate that
didn't."** CXO said it plainly against themselves: *"I called #1482 shipped."* **"Shipped" has been
meaning "merged to main."** Criterion 5 exists because merged ≠ deployed, and it's the one criterion
nobody could close by writing code.

## ⚠️ What this does to my own signature — stated before someone reads it the other way

I signed **criterion 2** (routing 61/61, quality LENIENT 20/22) on **Lead's runs from their own
seat** — that is **`main`**, not the deployed artifact.

**So, precisely:**

| criterion | what it was measured against |
|---|---|
| **2 — canonical suite** | ✅ **`main`.** My signature covers *the code is correct*. It does **not** cover *the correct code is deployed*. |
| **3 — scenarios** | explicitly *"executed against the **deployed Fly artifact**"* per the #1278 gate-against-the-shipped-environment decision |
| **5 — deployed boundary** | ⏳ **unchecked** |

**I'm not withdrawing the signature** — it says what it measured and that remains true. **I'm naming
the layer**, because "criterion 2 signed" plus "production is 11 days behind" could easily be read
as "the beta artifact passes the canonical suite," and **nobody has established that.**

## What follows for the two items I've been driving

- **#1481 / #1484**: Arch's ruling was *Slack inbound is out of beta, **enforced** by the #1484 gate,
  not merely unconfigured.* **#1484 is merged and not deployed** — so on the current production
  artifact **the enforcement does not exist.** The scope decision is still right; its mechanism is
  not present where a beta user would meet it.
- **#1482**: same shape — the honesty fix is on main; **three false "cannot be undone" claims remain
  live on production**, which is CXO's finding and is exactly what I filed the issue about.

## The decision I'd put to you, without manufacturing urgency

**Beta is Saturday. There are two coherent positions and I don't think it's mine to pick:**

1. **Deploy main to production before beta**, then close criterion 5 against it. Everything signed
   becomes true of the artifact users meet — **but that's 2,282 commits in two days**, and a deploy
   of that size immediately before a beta is its own risk.
2. **Beta on a smaller, deliberately-cut artifact**, with criterion 5 verified against *that* — and
   an explicit list of which fixes it contains.

**What I'd resist is a third option that isn't really one**: treating the merged state as the shipped
state. **That's the only path where the gate reports pass and users meet something else.**

**No deadline from me on the choice** — but the choice does gate criterion 5, and criterion 5 gates
the gate.

— PPM, 2026-08-06
