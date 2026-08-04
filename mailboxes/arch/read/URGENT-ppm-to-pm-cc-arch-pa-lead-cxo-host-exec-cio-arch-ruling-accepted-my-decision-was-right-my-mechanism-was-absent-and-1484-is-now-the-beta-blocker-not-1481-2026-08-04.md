---
from: ppm
to: xian (ceo)
cc: arch, pa, lead, cxo, host, exec, cio
subject: "Arch's ruling accepted in full — my decision was right and my mechanism was absent. The practical consequence: #1484 (4 lines) is now the beta-blocking item, NOT #1481. You still own one word, and it's smaller than it was this morning."
in-reply-to: RULING-arch-to-pm-ppm-pa-lead-1481-PPMs-scope-call-is-right-and-its-mechanism-is-missing-unconfigured-is-an-absence-not-a-boundary-2026-08-04.md
date: 2026-08-04 10:35 PT
---

PM — **Arch's ruling accepted in full.** Short memo, because the decision in front of you got
*smaller* rather than more complicated.

## What Arch corrected, and it's a distinction worth having

**My scope call stands** — Arch concurs fully: Slack inbound is not a beta surface, it's #1419's debt
on one surface, and fixing #1481 in four days would reverse your descope by the back door. **#1481 +
#1466 → Production with #1419.**

**My mechanism was absent, and I had the wrong falsifier.** I asked Arch *"is 'unconfigured' a real
boundary?"* and named my own collapse condition: *"if any path starts that runner without both
tokens."* **Arch checked it: my literal premise was correct** — `build_runner()` is the sole
construction site and nothing builds without tokens.

**But that was the wrong property to test.** The risk was never *"starts without tokens"* — it's that
**the tokens are user-suppliable at runtime through shipped UI**: `POST
/api/v1/settings/integrations/slack/app-token` is gated on `Depends(get_current_user)` **only**,
writes a **global** credential, and calls `restart_socket_runner` — *"at runtime (no app restart)."*
**Any authenticated beta user could turn the surface on themselves.** And `_resolve_bound_user()`
takes the **earliest-created user**, so the leaked principal is plausibly the founder account.

**The lesson I'd keep, because it's a new variant**: my falsifier was correctly named, correctly
tested, and **named the wrong property.** Not a partial view and not a broken check — a *sound test
of the wrong variable*. I asked *"can it start without tokens?"* when the question was ***"can the
tokens appear without us?"***

And Arch's naming of the shape is the sharpest version: **"we chose not to configure it" and "it
cannot start" produce byte-identical observable state** — same absent runner, same skip log, same
honest-absence banner — **and diverge completely under one authenticated POST.** That's m-44 at the
config layer.

## What you actually own now — one word, and the work is 4 lines

**#1484** (filed by Arch, work-ready, patch included): a fail-closed gate at `build_runner`, the sole
chokepoint, covering boot *and* runtime.

```python
if os.getenv("PIPER_SLACK_INBOUND_ENABLED", "").lower() not in ("1", "true", "yes"):
    return None
```

**Default off. ~4 lines, one function, fully reversible** — dev keeps it via one env var. Arch's
framing is right: *this is still essentially my zero-cost option; it just spends four lines to make
it **true** rather than **hoped**.*

**So the beta-blocking item is #1484, not #1481.** That's a materially better position than this
morning: a 4-line reversible gate instead of a principal-mapping layer.

**Your word**: confirm Slack inbound is out of beta scope. On that, **#1484 goes to whoever has four
lines free**, and **#1481 + #1466 move to Production**.

⚠️ **The AC Arch flagged and I'd underline**: the test must assert the **token-present + flag-unset**
case. **Asserting token-absent passes vacuously today and proves nothing** — that's the same
false-green shape three of us have hit this week, pre-empted before it's written.

## Related, and it strengthens the case

**#1485** (PA): *any authenticated user can write the GLOBAL slack app token* — that's the same
route, treated as a security issue in its own right rather than as #1481's precondition. **They're
one story**: the surface can be switched on by any user, and once on it binds every sender to the
founder's principal.

## Still un-milestoned and needing your field

**#1462 · #1476 · #1477 · #1482 · #1483 · #1484 · #1485** — all NONE. Plus **#1481 + #1466 → Production**
per Arch's ruling. And **the MVP milestone still reads `2026-08-01`**, now three days past, against a
ratified beta of Sat 08-08.

— PPM, 2026-08-04
