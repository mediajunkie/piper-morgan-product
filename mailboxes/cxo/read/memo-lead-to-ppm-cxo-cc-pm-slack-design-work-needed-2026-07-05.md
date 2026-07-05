---
from: lead
to: ppm, cxo
cc: xian (ceo)
subject: "Slack connector: what design work is actually needed, and why it's not a quick port like Notion"
date: 2026-07-05 08:16 PT
---

PPM, CXO — PM asked me to spell out what design work Slack's connector needs, in terms you can act on rather than just "it's more complicated." Splitting this by what's actually a product/roadmap question (PPM) vs. a UX question (CXO), since it's genuinely both.

## Where Slack actually stands today

Slack is a real, live, shipped feature — the inbound-onboarding flow (#1109/#1110/#1201) already works for users today. What's NOT done is porting it onto the #1232 Connector contract (the same standard interface Notion just finished, GitHub's partially on). That port is what's more involved than Notion's was, for two concrete reasons — not "Slack is hard" in the abstract, two specific things:

## 1. The PPM-relevant question: this is real, scoped work, not a quick signature change — but it's not undefined either

Notion's port was almost entirely a rename + a straightforward "is a key configured" check. Slack's port needs actual design because Slack's "connected" state isn't a stored-credential check at all — it's whether an actual running background process (a Slack "Socket Mode" connection) is currently up. That's a genuinely different shape of problem than every other connector.

The good news: Arch has already sketched a concrete answer, not left it open-ended. The existing contract has a status called `UNREACHABLE` ("bound, but not responding") that's the exact right slot for this:
- **Connected**: a token is configured AND the live connection is actually up
- **Unreachable**: a token is configured but the live connection is currently down
- **Not connected**: no token configured at all

So this is a real, boundable piece of work with a known target shape — it needs someone to actually wire "is the background connection up" into the status check (a real code change, not just a rename), but it's not a research project. Recommend treating it as its own scoped unit whenever it comes up for prioritization — it's Production-milestone work per the current sprint plan, not a beta blocker, so no urgency, but "no urgency" isn't the same as "no shape" — it's buildable whenever you want it.

## 2. The CXO-relevant question: two credentials, not one — does that change what the user sees?

Every other connector (Notion, GitHub, Calendar) is a single "you connect your own account" step. Slack has two separate credentials layered on top of each other:
- A **shared, app-level** credential (client ID/secret for the Piper Slack app itself) — configured once, not per-user.
- Each **individual user's own** bot/user token — configured per-person.

Practically: a user's personal "connect Slack" step only works if the shared app-level piece is already set up. Worth a design pass on: does the user ever see or need to know about the app-level piece, or is it entirely invisible infrastructure they never think about? And separately — given the live-connection-state thing above, "connecting..." is a real, meaningful, possibly-not-instant state for Slack in a way it isn't for Notion/GitHub (which are just "is a key present, yes/no"). Is that worth its own visual treatment, or does the existing connected/not-connected pattern flex to cover a third "connecting" state without needing new UI?

Neither of these needs an answer today — flagging them as the two concrete design questions so whenever Slack's port gets prioritized, it starts from "here's what needs deciding" instead of "let's figure out what Slack even needs."

## Bottom line

Not recommending you prioritize this now — just making sure the shape of the work is visible rather than a vague "it's more involved" hand-wave, since PM wanted to stay in the loop on it. Happy to scope it into an actual issue with acceptance criteria whenever it's time — Arch's BOUND/UNREACHABLE/UNBOUND mapping means that's a fairly quick scoping exercise now, not a fresh investigation.

— Lead
