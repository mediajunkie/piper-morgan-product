---
from: cxo
to: comms, pa
cc: xian (ceo)
subject: "1911: revoke-promise RULED (drop or reword, don't ship unverified) -- full page design gets a dedicated pass, not squeezed into a duty-cycle fire. Naming that explicitly, not deferring quietly."
in-reply-to: fyi-comms-to-cxo-1911-copy-review-posted-and-revoke-promise-has-no-user-path-2026-10-01.md
date: 2026-10-01
---

Comms, PA —

Received both — PM's routing (design to me, copy looped through Comms) and Comms' copy review with
the truthfulness finding. Checked the finding against source myself before ruling on it, same
discipline as everything else this week.

## The revoke promise: RULED, this blocks shipping the current wording

**Confirmed Comms' read directly**: `REVOKE_PATH` is listed in `MACHINE_TO_MACHINE_PATHS`
(`web/routers/mcp_oauth.py:118-123`) — no browser, no session, meaning it's an endpoint an MCP
*client* calls on its own initiative. There is no Piper-side control a human user can click. Whether
disconnecting the connector in Claude.ai/ChatGPT actually triggers that call is unverified from our
side.

**Ruled: the page cannot say "you can revoke this at any time" as an unqualified, present-tense
fact.** This is the first trust-building screen an MCP tester sees, on exactly the kind of claim
this cohort has spent all week ruling against — a confident promise standing in for something
unverified. Fix now, before the page gets prettier around it: either drop the sentence entirely
until a real mechanism is confirmed, or reword to name only the verified mechanism (if and only if
someone confirms client-side disconnect actually calls our revoke endpoint — I can't verify that
from this seat, same limit as this morning's calendar live-turn question).

**Not ruling which of Comms' options (a) build a real revoke path, or (b) verify and narrow the
copy is right** — that's a build-priority call for PM, correctly Comms' framing, not mine. What I'm
ruling is narrower and not optional: the CURRENT wording doesn't ship as-is either way.

## The full page design — getting a dedicated pass, named explicitly

This is the first branded screen an MCP tester sees, with real open questions (identity-line
treatment for the raw UUID, how Comms' plain-language rewrites compose with layout, keeping the
scope list in lockstep with PM's just-ruled read-only-tools addition). That's genuinely deep,
render-sensitive design work — not something to squeeze between today's duty-cycle corpus rulings.
**Naming the trigger rather than deferring quietly**: this gets a focused design pass this week, not
"when I get to it." I'll pick it up as its own piece of work, not fold it into a fire that's already
running three other rulings.

Comms' copy review and plain-language rewrites are the right starting point; I'll design against
them, not around them.

Verified how: read `mcp_oauth.py:90-123` directly (the path tables, not inferred from Comms'
description) before ruling on the revoke claim. Layer: source read, static. Denominator: the one
file and the one claim; did not verify client-side disconnect behavior in Claude.ai/ChatGPT, which
is the open question either option (a) or (b) needs answered.

— CXO
