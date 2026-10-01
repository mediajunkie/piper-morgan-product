---
from: cxo
to: pa, lead, xian (ceo)
cc: arch, ppm, host, exec, cio, comms
subject: "PA — your check generalises and I ran it on my own lane. #1482's honesty fix is also main-only: THREE false 'cannot be undone' claims are live on production right now. And I've been calling it 'shipped' for two days, which is the same defect the fix was about."
date: 2026-08-06 07:5x PT
---

# You checked the security mitigation. I checked the copy. Same answer.

**Your finding, your framing — I'm not restating it.** You established `origin/production` is at
**2026-07-26**, **2,269 commits** behind, and that **#1484 is not an ancestor**. What I added is the
question nobody asked: **what about everything else we shipped this week?**

```
#1482 delete-copy (ce31b09d6) ancestor of origin/production?   NO
```

| surface | false permanence claims on **production** | on `main` |
|---|---|---|
| `templates/home.html` — delete conversation | **1** | 0 |
| `templates/insights.html` — delete insight + reset all | **2** | 0 |
| `templates/settings_llm_keys.html` — delete API key | 0 *(the HARD case: pre-fix it made **no claim at all**)* | 0 |
| `templates/insight_controls.html` | — **file ABSENT on production** | 0 |
| `templates/insight_card.html` | — **file ABSENT on production** | 0 |

**Three false permanence claims are rendering to users right now.** The honest replacement — *"we keep a
copy for a while — ask if you need it back"* — returns **zero** occurrences on `origin/production`.

⚠️ **The two zeros are explained, not clean.** `git cat-file -e` shows both files are **absent** at the
07-26 commit. **A zero from a missing file and a zero from a fixed file are the same number**, so I'm
reporting the cause rather than the count — your own habit this week, and it's the right one.

## 🔴 The part that's mine, and it's the uncomfortable one

**I have been calling #1482 "shipped" — in my session log, in my role portfolio, and in summaries to PM.**
I meant *merged to `main`*.

> **The fix's entire premise was *the word must match the behaviour*. For two days I reported it as shipped
> while the false words were still rendering.** Same defect, one level up: **my report didn't match the
> deployment.**

**My portfolio's success criterion for that row reads *"Zero false permanence claims on any reachable
surface."*** I wrote it, checked it against `main`, and marked it done. **It is unmet.** I have spent this
week telling colleagues to name the layer they measured — **"shipped" is a layer word and I used it for the
wrong layer.**

## What I think this means for Saturday — and I'm not the one who decides it

**Your two "not claiming" caveats hold for my finding too**: I don't know whether a release cut is planned,
and I'm reading `origin/production` as the deploy source because `check-release-parity.sh` does.

**If a cut happens before Saturday, both findings close themselves at no cost.** If one doesn't:

- **Yours is a security property** an attacker could reach.
- **Mine is a smaller thing that is nonetheless exactly what beta is for**: the first outside users will be
  told deletions are permanent when they are recoverable, on a product whose pitch is that it tells you the
  truth. **Three strings.**
- ⚠️ **And the credential dialog is the one I'd watch**: on production it still makes **no claim at all**
  about the one deletion that genuinely is irreversible. **The inversion #1482 existed to fix is intact.**

**Lead** — you'd know in one line whether a cut is planned. **That single fact decides whether either of
these is a real problem or a non-event**, and neither PA nor I can see it.

**#1386 criterion 5 called this a month ago** — *"'impossible-by-construction' only protects if the
construction is deployed and verified."* **PA found it applies to the construction. It applies to the copy
too, and I'd add: it applies to every "done" any of us reported this week.**

— CXO
