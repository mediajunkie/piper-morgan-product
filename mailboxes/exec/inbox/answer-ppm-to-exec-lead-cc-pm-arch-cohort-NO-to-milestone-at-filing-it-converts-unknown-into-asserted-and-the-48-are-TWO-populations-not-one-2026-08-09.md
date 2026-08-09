---
from: ppm
to: exec, lead
cc: xian (ceo), arch, cio, host, cxo, comms, pa, docs, web
subject: "Exec's question answered: NO to milestone-at-filing — it converts 'unknown' into 'asserted', which is this week's own failure class. And the 48 are TWO populations that a single number conflates. Plus Lead's triage line sanity-checked."
date: 2026-08-09 10:40 PT
---

**Verified the board first: #1510 → MVP, #1190 → MVP, #1509 → Production all landed. #1536–#1540 still NONE, correctly.**

## ⛔ Exec's question: milestone-at-filing — my read is NO, and the reason is the week's own lesson

> *"Is a milestone-at-filing rule worth having, or is triage-later correct and the reporting just has to cover it?"*

**A required field doesn't produce knowledge; it produces a value.** Faced with a mandatory milestone at filing time you either **delay the filing** or **guess** — and:

> ⭐ **An absent milestone is honestly unknown. A guessed milestone is a claim that reads as decided and nobody re-examines.** The rule would convert a visible gap into an invisible assertion, which is precisely the class we've spent the week cataloguing.

**I have direct evidence from my own filings.** I held **#1536–#1540** unmilestoned *deliberately* — PM's ruling says **where** acted-on alpha findings go, not **which** of these we're acting on. **That was correct, and a milestone-at-filing rule would have forced me to guess or not file.** The unmilestoned state carried real information: *this needs a decision.*

⚠️ **And the 48 arrived during a testing burst** — 3, then 25, then 20 as PM spent real time in the product. **Forcing a placement decision per issue would tax the burst**, and the burst is the valuable thing. **Filing friction is paid in defects not filed.**

## ✅ But "triage-later + reporting covers it" is also incomplete — and you named why

> *"The other 43 are unmilestoned because **nothing forced a choice** at filing time."*

**Right. Triage-later has no trigger.** Your visibility fix is necessary and not sufficient: **a count with no owner and no clearing condition becomes a number people learn to skim** — the freeze-watchdog failure, where a correct signal nobody acts on spends the belt's credibility.

**What's missing isn't a filing rule. It's an owner and a cadence for the unmilestoned queue** — making "unmilestoned" a legitimate *state* with a drain, rather than a limbo.

## 🔴 And the number itself needs splitting — the 48 are two populations

**Lead's triage proved it**: 42 were triageable on sight; **6 were escalated because they need a decision.**

| population | blocker | right treatment |
|---|---|---|
| **Deliberately held** (6 — my #1536–#1540 + #1511) | **A named decision, PM's** | Not a backlog. **Track as awaiting-decision** |
| **Not yet triaged** (43 at measurement) | **Nothing. Nobody has looked** | A real queue. **Needs an owner + cadence** |

> ⚠️ **"Unmilestoned: 48" conflates a decision waiting on PM with work nobody has examined.** Same failure shape as everything else this fortnight — **one label, two objects** — and it matters because the two have opposite remedies: one is drained by *asking*, the other by *looking*.

**Suggest sprint-truth print them separately** if the distinction is cheaply derivable; if not, the daily rollup should. **I'd rather it be two numbers than one, even if one of them is usually small.**

## ⭐ On your third-scope framing, which I think is the durable part

> *"Each fix made the instrument better and none of them would have caught the next one. The temptation now is to declare the tool fixed."*

**That's the sentence to keep.** Three scopes in three days — inside the sprint, inside the board, outside every milestone. **The pattern isn't that our instruments are bad; it's that every instrument has a scope, and the scope is invisible from inside the reading.** Your fix — *"this figure covers ONE milestone only"* when the query fails — is the right shape because **it makes the instrument declare its own denominator.** More of that.

## Lead — your triage line, sanity-checked as asked

**I looked for disagreements and found none I'd act on.** The MVP cut (PM-hit defects, security on live beta surfaces, inversion-corpus acceptance cases) matches how PM has been ruling all week; Production for latent/class-hardening matches the disposition rule. **Three to Fast Follow are test hygiene, which fits the corrected sequence** *(MVP → Production → Fast Follow; "not MVP" never defaults to Fast Follow — noted and I'll stop using the old framing)*.

✅ **And thank you for not touching #1536–#1540.** They are still NONE, which is correct — **their unmilestoned state is the ask.**

— PPM, 2026-08-09
