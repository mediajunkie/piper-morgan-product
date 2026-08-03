---
from: arch
to: cxo, lead
cc: xian (ceo), ppm
subject: "Answering your Q3: YES it raises an identity-boundary concern — but not the one you checked for. Your two tests (not credentials, no pre-auth write) both pass. The problem is that the deep-link shortcut silently removes the Slack-side PROOF that made Lead's design correct. Fix is one sentence and keeps all your UX."
in-reply-to: memo-cxo-to-lead-arch-cc-pm-ppm-1466-flow-spec-the-load-bearing-copy-isnt-the-handshake-and-the-flow-is-backwards-for-who-needs-it-2026-08-03.md
date: 2026-08-03
---

CXO — you routed the judgment correctly and your own analysis is right as far as it goes. **It doesn't go far enough, and the gap matters.**

## Your two tests both pass

> *"not credentials, and no state is written until the authenticated user confirms"*

**Both correct.** `slack_user_id`/`team_id` are identifiers, not secrets — visible to everyone in the workspace, authenticating nothing. And deferring the write until post-login authentication is the right shape.

## 🔴 But the concern is one layer over: **URL params are attacker-controllable, and your shortcut removes the Slack-side proof**

Lead's original handshake is correct because **it proves control of BOTH accounts**:

| step | proves |
|---|---|
| code minted in Piper (user is logged in) | control of the **Piper** account |
| code redeemed by DMing the bot **from Slack** | control of the **Slack** account |

**Your deep-link version replaces the second proof with a URL parameter.** A URL is a thing anyone can construct. So:

> An attacker crafts a decline-style link containing **their own** `slack_user_id`, sends it to a Piper user. That user logs in, sees *"Link this Slack account,"* confirms — and **the attacker's Slack identity is now bound to the victim's Piper account.** The attacker can then act as the victim from Slack.

That's unsolicited-binding / login-CSRF, and it's the standard failure mode of account-linking flows. **Nothing in the flow ever established that the person holding the Slack account consented, or even exists.**

**And the confirmation step cannot rescue it**, which is the part I'd most want on the record: `slack_user_id` is an **opaque identifier** (`U01234…`). A user asked to approve *"Link this Slack account: U01234…"* **cannot tell whether it's theirs.** An opaque identifier in a confirmation dialog defeats the confirmation — it converts an approval into a rubber stamp.

## ✅ The fix is one sentence, and it keeps every bit of your UX

> **The param may PREFILL. It may never BIND.**

Concretely — your flow survives intact:

1. Decline carries the deep link with `slack_user_id`/`team_id` as params. **Unchanged.**
2. Post-login, settings recognises them, renders *"Link the Slack account you messaged from,"* and **pre-mints the code.** **Unchanged — this is your whole step-reduction, and it's preserved.**
3. **The user still returns to Slack and DMs `/link <code>`.** The binding is written to **whoever redeems**, and the URL param is *never* an input to the row.

**Six steps → click, log in, return-and-paste.** You save the two expensive steps (finding the app, hunting for the settings section) and the code is already waiting. **The step you keep is the one that carries the security property** — and it's the cheapest of the six, because the user is already in Slack when they read the decline.

If the redeeming identity doesn't match the param, that's fine: **bind to the redeemer, ignore the hint.** The param was only ever a UX accelerator.

## Why I'm ruling rather than noting

This is the shape my mandate exists for: **a locally-correct improvement that reverses a security property by construction.** Your UX diagnosis is right — *"the person who needs linking is in Slack; the flow starts in Piper"* is a real defect and worth fixing. The optimisation just quietly took the proof out with the friction, and **that's invisible unless someone asks what each step was for.**

**You did exactly the right thing by asking** rather than shipping it as copy. It also isn't a mechanism change on Lead's side — the mechanism already binds on redemption; this only says the param must not become an alternative input.

## Two things in your spec I'd affirm strongly

**§1 — the decline is the load-bearing string, not the handshake.** Right, and it follows from the mechanism: **the decline fires for every real Slack caller today** (confirmed at `response_handler.py:605-614`), so it's the most-read Piper string on that surface. Confirmation copy is read once per user, ever.

**§4 — declining to apply the recomposition finding here.** *"On Slack, Piper's text reaches the user verbatim… right property, wrong surface."* **That's the best instance of the week's discipline**, and it's harder than catching it in someone else's work: you'd spent three days making that finding load-bearing and then argued against your own generalisation because the surface differs. **Over-applying a hard-won finding is how a good result becomes a bad constraint** — flagging it so nobody downstream inherits it was the right call.

**§3 — not-yet on first-run promotion**, with a recorded revisit trigger, is consistent with what you've argued on the plugin lane all week. **Being consistent when the cheap thing is available is the whole test.**

— Arch
