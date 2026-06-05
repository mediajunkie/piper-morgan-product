---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian)
date: 2026-06-05
subject: Request — parametrize the hardcoded Piper port (main.py:193) + a heads-up on skunkworks test-window overlap
priority: standard — PM-endorsed; not blocking (PA has an interim fix in place)
---

# Two things, both small, both about server-port flexibility

Context: the skunkworks BYOC plugin (#1145) now hits the real local Piper `/api/v1/intent` via an MCP
server. During testing it shares your `:8001` dev server, which surfaced two things.

## 1. The Piper port is hardcoded — worth parametrizing (the real ask)

`main.py:193` binds `port=8001` as a literal, with no `--port` arg and no env var. PM and I hit this
when scoping a dedicated skunkworks Piper instance — it can't be done by config alone; it needs a code
change to `main.py`. **PM agrees the port shouldn't be hardcoded.**

**Request**: parametrize it — e.g. `port = int(os.environ.get("PIPER_PORT", 8001))`, or an argparse
`--port`. Low-risk, default-preserving. Note `main.py` also hardcodes `:8001` in the browser-open /
health-check helper (lines ~106/113/130) — those should read the same source so they don't drift.

**Why it's useful beyond skunkworks**: lets a second instance run for isolated testing (skunkworks,
e2e, demos) without colliding with your live dev server; and removes a magic-number that any
multi-instance or CI scenario trips on. The skunkworks MCP already reads a `PIPER_BASE_URL` override,
so the moment the server can bind a chosen port, isolation is pure config on our side.

This is your lane (it's `main.py`); flagging as a request, not doing it myself. No urgency — PA has an
interim fix (below) so we're unblocked meanwhile.

## 2. Heads-up: skunkworks tests + your dev-server restarts overlap on :8001

When you restart `:8001`, an in-flight skunkworks `ask_piper` call sees a transient failure. Last night
(6/4 ~10:52 PM) one returned Piper's "AI service temporarily unavailable" — a HTTP-200 body that looked
like a real answer but was a reasoning-engine blip (possibly your restart, possibly an LLM hiccup —
cause not established; #1145 notes "don't guess, check logs").

**Interim fix already shipped (PA side, no action for you)**: the skunkworks MCP now tags each failure
mode distinctly — `SERVER-DOWN` / `TIMEOUT` / `HTTP-N` / `PIPER-INTERNAL-ERROR` / `OK` — so we can tell
*your restart* from *our bug* from *a real Piper answer* at a glance. That solves the attribution pain
for now.

**The only ask here**: if you're doing a burst of `:8001` restarts and happen to know I'm testing,
a quick heads-up saves a confused retry. Pure courtesy, not a process. The port-parametrize in #1 is the
real durable fix (dedicated instance → no overlap at all).

## Related discovered work (filed, your lane / floor lane — FYI not asks)
- **#1150** — `/intent` reports wrong time-of-day (said "late evening" at 11:30 AM; `current_time`).
- **#1151** — `/intent` returns `intent.original_message: ""` (empty) — data-fidelity gap in the contract.

Both surfaced by the BYOC consumer-trace; flagging so they're on your radar when the floor/intent lane
comes up. No action requested here.

— PA, 2026-06-05
