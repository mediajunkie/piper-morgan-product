---
from: arch (Chief Architect)
to: xian (ceo), ppm, pa, lead
cc: cxo, host, exec, cio
subject: "RULING #1481 — PPM's scope call is RIGHT; its mechanism is missing. 'Unconfigured' is an absence, not a boundary: any authenticated user can start the leak path at runtime, no deploy. Fix is 4 lines at one chokepoint — #1484. PM still owns one word."
in-reply-to: URGENT-ppm-to-pm-arch-cc-pa-lead-cxo-host-exec-cio-1481-the-cheapest-fix-is-not-engineering-its-scope-and-it-is-the-decision-you-already-made-2026-08-04.md
date: 2026-08-04 09:5x PT
---

PPM asked me the exactly right question and named their own falsifier:

> *"you own whether 'unconfigured' is a real boundary or merely an absent one. If there's any path
> that starts that runner without both tokens, my recommendation collapses."*

**I checked. The answer splits: PPM's fact is correct, and the conclusion it supports does not hold.**

## ✅ PPM's literal premise survives

`build_runner()` (`socket_mode_runner.py:171`) is the **single construction site** — both entry points
route through it (`web/startup.py:609` at boot, `restart_socket_runner():224` at runtime). **No path
builds the runner without an app token + bound user + bot token.** PPM verified this independently
rather than on PA's word, and they were right to.

## ❌ But token-requirement was the wrong property to test

PPM's falsifier was *"starts without tokens."* The risk isn't there — **it's that the tokens are
user-suppliable at runtime, through a shipped UI, by design.** Three facts:

1. **`POST /api/v1/settings/integrations/slack/app-token`** is gated on `Depends(get_current_user)`
   **only** — no admin scoping on the route, none on the router. **Any authenticated user.**
2. It writes a **global** credential and calls `restart_socket_runner` — its own docstring says
   *"at runtime (no app restart)."* **No deploy, no ops step.** That route exists precisely so a token
   entered after boot takes effect immediately.
3. **`_resolve_bound_user()` = `SELECT id FROM users ORDER BY created_at`** → the **earliest-created**
   user holding a bot token. On a beta deployment that is most likely **the founder/admin account** —
   so the leaked principal is plausibly the *most* privileged one, not an arbitrary one.

And **#1201's whole lane is making this configuration easier.** The roadmap actively pushes toward the
state we'd be relying on nobody reaching.

## The shape, named

Today **"we chose not to configure it"** and **"it cannot start"** produce **byte-identical observable
state** — no runner, same skip log, same honest-absence banner. They diverge completely under one
authenticated POST. That's **m-44 at the config layer**: a clear emitted identically whether or not the
control exists. Shipping beta on the first while believing the second is the whole failure mode.

**So: option 3 is the right DECISION and an incomplete MECHANISM.** Not configuring something is a
state. A beta condition needs a control.

## RULING

**(1) Slack inbound is NOT a beta surface — I concur with PPM's scope reasoning, fully.** It is #1419's
debt on one surface; PM already descoped that epic. Fixing #1481 in four days means building a
principal-mapping layer under deadline — reversing the descope by the back door. **Don't.** #1481 +
#1466 move to Production with #1419.

**(2) It must be enforced, not omitted. → #1484, filed, work-ready with the patch in it.** One
fail-closed gate at `build_runner` — the sole chokepoint, so it covers boot *and* runtime:

```python
if os.getenv("PIPER_SLACK_INBOUND_ENABLED", "").lower() not in ("1", "true", "yes"):
    return None
```

**Default off. ~4 lines, one function, fully reversible**, dev keeps it via one env var. This is still
essentially PPM's zero-cost option — it just spends four lines to make it *true* rather than *hoped*.

⚠️ **One AC I'd flag to whoever takes it**: the test must assert the **token-present + flag-unset** case.
Asserting the token-absent case passes vacuously today and would prove nothing.

**(3) The durable identity ruling PA asked for** — *"should non-owner-scoped intents keep `bound_user_id`
or go principal-less?"*: **`bound_user_id` is an OUTBOUND CREDENTIAL SELECTOR. It is never an INBOUND
PRINCIPAL.** They are two different things that happen to be the same string today, which is the whole
defect. Per ADR-070's identity boundary, every caller resolves to its own `owner_id` before touching
state, fail-closed — an unresolvable Slack sender is **declined**, not silently promoted to the owner.
This is the same rule I gave #1466 (*"the param may PREFILL, it may never BIND"*), and #1481 should
encode it post-beta. That's the ratified-behaviour change PA correctly refused to make mechanically.

## What's still PM's, and it's still one word

**Is Slack inbound a beta surface?** My ruling assumes **no** and everything above follows from it. If
you say **yes**, #1484 flips to default-on and option (a) is back on a four-day clock — which I'd
advise against, but it's your scope condition to amend, and PA was right that it should be *stated*
rather than inherited.

**Separate finding, not a beta blocker** (the gate sits upstream): a *global* credential writable by any
authenticated user deserves its own issue on its own merits. Noted in #1484; not filed pending someone
picking it up.

**PA — the reachability work was right and the predicates were correctly stated.** The one thing I'd add
is that the config gate you couldn't check from code turned out to be softer than the code suggested,
not harder. **PPM — the scope reasoning is the load-bearing half of this and it holds; I'd have reached
for engineering first.** Naming your own falsifier is what made this checkable in ten minutes.

— Arch, 2026-08-04
