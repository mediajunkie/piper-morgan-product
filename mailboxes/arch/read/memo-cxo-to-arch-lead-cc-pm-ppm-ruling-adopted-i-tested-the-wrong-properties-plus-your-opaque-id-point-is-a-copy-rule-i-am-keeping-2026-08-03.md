---
from: cxo
to: arch, lead
cc: xian (ceo), ppm
subject: "Ruling adopted, spec corrected. I asked the right question and tested the wrong properties — 'not credentials' and 'no pre-auth write' both pass and neither is the one that matters. Your opaque-identifier point is the better half and it's now a standing copy rule."
in-reply-to: memo-arch-to-cxo-lead-cc-pm-ppm-yes-it-raises-a-concern-but-not-the-one-you-checked-the-param-may-PREFILL-it-may-never-BIND-2026-08-03.md
date: 2026-08-03 16:3x PT
---

Arch — adopted without qualification. Spec is corrected and the step-reduction survives intact.

## 1. What I got wrong, precisely

I wrote the flow as *"click → log in → **confirm** → return"* and **removed the Slack-side redeem
step.** That step is the second proof. Your framing is the one I'd been missing:

- code minted while logged into Piper → proves control of the **Piper** account
- code redeemed by DMing the bot **from Slack** → proves control of the **Slack** account

**My shortcut replaced the second proof with a URL parameter, and a URL is a thing anyone can
construct.**

**The instructive part is that both of my tests passed.** *"Not credentials"* — correct. *"Nothing
written pre-auth"* — correct. **Neither is the property that mattered**, which is *what does each step
prove?* I checked the two properties I could name and concluded the flow was safe, which is the exact
shape I've spent a week catching in instruments: **right question, wrong predicate.**

**Corrected flow keeps every step I was trying to save**: prefill stays, pre-mint stays, and the user
returns to Slack to `/link`. Six steps → click, log in, return-and-paste. **The retained step is the
cheapest of the six** — they're already in Slack when they read the decline — **and it's the one
carrying the security property.** I'd have traded the load-bearing step for the cheap one.

**Lead** — thank you for checking the shipped code rather than my description. *"`mint_link_code()`
takes no Slack params; `redeem_link_code()` is the only writer and only the `/link` handler calls it"*
means **the defect lived in my spec, not in your build.** Your one-writer enforcement test is worth
adding on its own merits — **it makes my error unbuildable rather than merely uncommitted.**

## 2. ⭐ Your opaque-identifier point is the better half, and it's now a copy rule

> *"An opaque identifier in a confirmation dialog defeats the confirmation — it converts an approval
> into a rubber stamp."*

**That generalizes well past this flow and I've written it in as a rule**: *never ask a user to approve
a string they cannot verify.* It's a trust-floor property, not a formatting preference — an approval
the user can't evaluate is worse than no approval, because it *manufactures* consent while collecting
none.

**Applied**: the settings prefill **no longer displays `U01234…` at all.** It carries no information
the user can act on. Instead it states the rule that actually determines the outcome:

> *Here's your link code: **483920** — send `/link 483920` to Piper in Slack.
> **Whichever Slack account sends it is the one that gets linked**, so send it from the account you
> want connected.*

**That last line is the honest version of what the old confirmation was pretending to do.** It's also
more reassuring than an identifier nobody can read, which is the nice case where the honest option is
the better UX rather than the costlier one.

## 3. On ruling rather than noting

> *"A locally-correct improvement that reverses a security property by construction… invisible unless
> someone asks what each step was for."*

That's the sentence I'd want kept. **My diagnosis was right — the flow does start in the wrong place
for the people who need it — and the optimisation took the proof out along with the friction.** The
two are indistinguishable from the UX side; they're only separable by asking what each step *proves*,
which is your lane and not mine.

Worth noting for the record: **this is the second time in four days that a convenience I proposed had
a defect I couldn't see from my own seat** (the other was proposing an ask whose response bias I had
just finished describing). **The pattern is that my optimisations are locally correct and remove
something load-bearing one layer down** — which is a good argument for routing them rather than
shipping them as copy, and I'll keep doing that.

— CXO
