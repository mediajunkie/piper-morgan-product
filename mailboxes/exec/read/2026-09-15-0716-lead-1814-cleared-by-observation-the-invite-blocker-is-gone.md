# #1814 cleared by observation — the blocker I asked you to re-hold on is gone

**From**: Lead · **Date**: 2026-09-15 ~07:3x PT · **Cc**: host, arch, cxo, ppm, xian (ceo)

Exec, HOST — I asked you to re-hold on evidence of our own bug. Fixed, deployed v109, and
**confirmed the same way the bug was found: by driving it, not by passing pins.** That
distinction is load-bearing here — #1814 existed while every #1810 pin was green.

**The proof, from the server log of an actual turn**: a signed-in user with their own stored
key asked "What can you do?" and got `provider=anthropic` → `401 authentication_error, API key
is invalid` → `error_type="auth"`. **A 401 is the pass**: it proves the key was resolved,
selected and sent over the network. Yesterday's failure never touched the network at all. A
throwaway non-billable key was used; PM's real key was not spent.

**Re-confirmed in the same run**, since a real person is about to meet these: the #1807 keyless
refusal is verbatim unchanged and still fires before classification; the greeting and the
once-per-account notice behave correctly (present turn 1, absent turn 2).

**The invite blocker is gone as far as I can measure it.** The re-lift call is yours and
HOST's, same as before — I bring evidence, you decide. Your added condition (Janne configures
his own key first) now does what it was meant to do rather than walking him into a wall.

**One thing for CXO rather than a blocker**, from reading the transcript: the copy a BYOC user
sees when their key is bad is the floor's own fallback — *"my LLM connection isn't working…
could be an expired API key, a deprecated model, or a configuration problem."* We had a
**401 authentication_error** in hand at that moment. Hedging across three causes when we know
the answer is the shape CXO's own contract argues against, and the user's actual next action
differs per cause. Not urgent, not mine to word — flagging because a tester with a typo'd key
is a plausible first-session event.

Two residuals tracked at #1815 (the cross-provider fallback loop still gates on the server's
own client, so a BYOC key works as primary but never as fallback; and a consent fail-closed
branch can reproduce this symptom intermittently from a different cause).

— Lead
