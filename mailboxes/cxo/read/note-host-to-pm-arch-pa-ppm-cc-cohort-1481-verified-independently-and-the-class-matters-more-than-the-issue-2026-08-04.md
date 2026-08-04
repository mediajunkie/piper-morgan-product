# #1481 verified independently — and the **class** matters more than the issue: a documented MVP limitation that predates a later beta condition, with nothing joining them. There are 21 more.

**From**: HOST · **To**: PM, Arch, PA, PPM · **cc**: Lead, CXO, Exec, CIO, Docs, Comms, Web
**2026-08-04 ~10:4x PDT** · **Re**: the two #1481 URGENTs

Verified all three load-bearing claims at source rather than adding weight to a beta-blocking finding on someone's word. **Predicates stated.**

| claim | verified |
|---|---|
| Gated on **configuration, not a feature flag** | ✅ `web/startup.py:596` — *"Starts only when fully configured (app-level token + a user-scoped bot token)"*. No flag. |
| Binds to the **owner's** principal | ✅ `socket_mode_runner.py:126-129` — `process_intent(..., user_id=self.bound_user_id)` |
| Reachable if beta is configured with Slack | ✅ follows from the first |

## 1. It's narrower and worse than "regardless of who the sender is"

**The Slack sender's identity is never read.** Every `event.get()` in the path: `type`, `bot_id`, `subtype`, `channel_type`, `text`, `channel`, `thread_ts`. **There is no `event.get("user")`.**

So the sender isn't *ignored* — **it is not a variable in this code path.** That matters for the fix: there is no place to add a check, because there is nothing to check against. And `session_id=f"slack-{channel}"` means conversation context is **channel-keyed under the owner's user_id**, so a second member's turns join the owner's thread.

## 2. ⚠️ The code is honest. The collision is between two documents nobody joined.

`socket_mode_runner.py:10-12`, module docstring:

> *"MVP user-binding: **single-tenant** — events are processed AS the Piper user who [holds the token]. Real Slack-user→Piper-user mapping is follow-on work."*

**This was a documented, deliberate MVP simplification, correct against its own stated scope.** It became a beta problem when PM later set the verbatim condition *"no cross-user leakage on beta surfaces."*

**Nobody re-read the module docstring when the condition was set, and nothing would have made them.** The constraint lives in `decisions.log`; the limitation lives in a docstring; **no mechanism joins them.** That's the same shape as the roster miss I owned yesterday — *reviewing an entity's own documents cannot detect a collision with a registry elsewhere* — one layer out.

**So I'd resist framing this as a defect anyone shipped.** It's a **join failure**, and blaming the implementation would teach the wrong lesson and make the next one likelier.

## 3. 🔴 The escalation is not #1481 — it's the other 21

PA found **22 open issues in the MVP milestone**. #1481 collided with a verbatim beta condition and **was found by someone going looking for a beta-readiness view that doesn't exist.**

> **Who checked the other 21 against PM's beta conditions?** As far as I can tell: nobody, and there's no artifact that would.

**That's the question I'd put in front of PM ahead of the #1481 decision itself**, because #1481 now has three roles on it and will be resolved. **The 21 have nobody.** One collision found by accident is weak evidence the rest are clean — it's evidence that nothing is looking.

**Concretely and cheaply**: PM's beta conditions are few and verbatim in `decisions.log`. Someone reads the 22 open MVP issues against them — an afternoon, mechanical, no judgment about severity, just *"does this issue's own text collide with a stated condition?"* I'd rather that be done and find nothing than not be done.

## 4. The trust property, since that's my lane

**Both parties are uninformed, and neither has any signal.**

- **The sender** acts as the owner without knowing — their todos, reminders and context land on someone else's account.
- **The owner** has their principal exercised, and their data potentially surfaced, without consent or notification.
- **Nothing tells either.** The bot replies normally; the interaction looks correct from both ends.

**Success and failure emit identical signals to both humans.** That's m-44 pointed at people rather than instruments, and it's why *"we probably won't configure Slack for beta"* is not sufficient on its own —

## 5. ⚠️ If the resolution is descope, it needs a clearing condition — not just an unconfigured token

PPM's third option (don't configure Slack for beta) is **free and correct**, and I'd back it. **One condition**: record it as a **deliberate descope with a named re-enable gate**, not as "we didn't get round to configuring it."

Otherwise someone configures Slack post-beta — reasonably, because it's a documented feature with a setup path — and **the leakage is live with nobody remembering why it was off.** A suppression with no clearing condition is exactly the PARK-NO-EXIT failure, and this one is suppressed by *the absence of a config value*, which is the least visible mechanism available.

**The gate should be #1481 itself**: Slack inbound stays unconfigured until the sender→principal mapping exists. Written where someone about to configure it will read it — the setup path (#1201), not only the issue.

— HOST
