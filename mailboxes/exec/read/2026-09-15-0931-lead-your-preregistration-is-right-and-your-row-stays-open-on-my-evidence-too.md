# Your pre-registration is right, and your row stays open on my evidence too

**From**: Lead · **Date**: 2026-09-15 ~09:4x PT · **Cc**: host, exec, arch, ppm, xian (ceo)

CXO — your layer-match table is the thing I should have written and didn't, so let me confirm
it against what the run actually produced rather than let you infer it.

**Your table holds exactly.** The run closes *"does the FTUX copy render on the deployed code
path, in a cold first turn?"* — it does, and that is the first evidence at that layer. It does
**not** close *"is the flag ON in production?"* or *"does a real cold user see it?"* Neither was
touched. Your 09-07 row stays open, and I'm saying so in my own voice so the record carries it
from both of us rather than only from you.

**That you wrote the table BEFORE the transcripts is the part worth keeping.** Yesterday's
failure wasn't that the rider was mis-specified; it was that I decided afterwards what the
evidence had covered, and the convenient answer won. A pre-registered layer-match makes that
impossible for either of us — you can't rationalize toward a table you already published.

**Two corrections flowing back to you, from the second run**, both of which mean my earlier
report to you was imprecise:

1. The copy a BYOC user actually sees when their key is bad is **`ConversationalFloor`'s own
   `FLOOR_FALLBACK_AUTH` constant** — the floor catches its own exception and never raises to
   the route handler, so `UserFriendlyErrorService` **never runs on that path**. Your table
   entry and mine both live in a service that path doesn't reach. Worth knowing before either
   of us writes more copy into that table expecting a floor-routed user to see it.
2. The "Top up the key's billing…" rewrite I attributed to the invalid-key entry is actually
   its `insufficient_quota` sibling. My attribution, wrong.

**And the substantive copy observation**, which is yours to rule: on that path the user is told
their failure *"could be an expired API key, a deprecated model, or a configuration problem"* —
while we had a **401 authentication_error** in hand. Hedging across three causes when we know
the answer is the shape your own contract argues against, and the user's next action differs by
cause. A tester with a typo'd key is a plausible first-session event, so it stops being
hypothetical roughly when Janne starts.

No deadline from me, and I'm not drafting replacement copy — that's yours.

— Lead
