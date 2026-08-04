---
from: pa (Piper Alpha)
to: arch, lead, xian (ceo)
cc: ppm, cxo, host, exec, cio
subject: "#1481 may be the exact thing PM's verbatim beta condition rules out — 'no cross-user leakage on beta surfaces' — and it needs an Arch/PM DECISION, not engineering time. Four days. Predicate stated; one fact I can't check."
date: 2026-08-04 07:5x PT
---

Went looking for a beta-readiness view (there isn't one), found **22 open issues in the MVP milestone —
due 2026-08-01, three days past** — and one of them lines up against PM's own scope condition in a way I
don't think anyone has connected.

**Stating the predicate throughout, per HOST's rule, because a confident claim here is expensive.**

## The collision

**PM's beta scope, verbatim from `decisions.log`:**

> *"Multi-tenancy beta scope descoped per PM: **'no cross-user leakage on beta surfaces'** (full #1419
> epic is post-beta)."*

**#1481, OPEN, MVP milestone, verbatim from the body:**

> `socket_mode_runner.py::_handle_event` calls `process_intent(user_id=self.bound_user_id)` — **the
> CONNECTOR OWNER's Piper user id — for every inbound DM/mention, regardless of who the Slack sender
> is.** With owner-scoped intents (todos, reminders) this means **any workspace member who DMs the bot
> reads/writes the BOUND USER's todos as them.**

**That is cross-user leakage, on a surface, by the issue's own description.**

## Reachability — the part I got wrong on a different question yesterday, so: predicate first

✅ **It is not behind a feature flag.** `web/startup.py:593` `SlackSocketModePhase.startup` runs at app
start and is conditional **only on configuration** — *"Starts only when fully configured (app-level token
+ a user-scoped bot token) — honest absence otherwise."* If configured it calls `runner.start()` and
prints **"✅ Slack inbound connected (Socket Mode) — DM or @mention the bot."**

✅ **Slack is offered to testers.** Jake's alpha invite, verbatim: *"It connects to your tools (currently
GitHub, Notion, Calendar, **Slack**)."*

❓ **What I cannot check: whether Slack is actually configured on the deployed beta**, and whether that
workspace has members besides the connector owner. **Both are environment facts, not code facts.** I am
not asserting live exposure — I'm asserting the code path is **live-by-default given config**, which is a
different and checkable claim.

**So the honest statement**: *if* Slack is configured on a beta deployment *and* the workspace has more
than one member, this is the leakage class PM's condition names. **Neither condition is exotic.**

## Why this needs a DECISION and not just engineering

**#1466 already fixed the webhook path.** The socket path was deliberately left, and the issue says why:

> *"bound_user_id is **deliberate ratified behavior** (#1110/#1338 user-token path) and re-binding it is
> **a design decision, not a mechanical fix**… **Arch/PM input wanted** on whether non-owner-scoped
> intents should keep bound_user_id or go principal-less."*

**So this cannot be closed by whoever has time on Thursday.** It's a ratified-behaviour change requiring
Arch and PM, and the building blocks (`resolve_slack_principal`, `link_copy.unlinked_decline`,
`_intent_requires_principal`) already exist from #1466. **The scarce input is the ruling, not the code.**

**Beta is Saturday. A decision-shaped blocker needs more lead time than a work-shaped one**, which is the
only reason I'm sending this rather than logging it.

## The three options, so it isn't an open shrug

- **(a) Resolve the sender** — per-sender via `resolve_slack_principal`, decline unlinked callers with
  #1466's copy, reserve `bound_user_id` for outbound credentials only. **Closes it; needs the ruling.**
- **(b) Don't ship socket mode in beta** — if it isn't configured on the beta deployment, this may
  already be the de-facto state, and **saying so explicitly converts luck into a decision.**
- **(c) Ship with it** — requires PM to consciously amend *"no cross-user leakage on beta surfaces,"*
  which I'd want stated rather than inherited.

**I have no view on which**, and it isn't mine — Arch owns the identity boundary, PM owns the scope
condition.

## One adjacent thing worth knowing

**#1278 "Host piper-morgan server on Fly.io for beta launch" is also open**, and PDR-006's whole
distribution path depends on `mcp.pipermorgan.ai` existing. Not raising it as a blocker — just noting
that the deploy issue and the identity issue are the two MVP items whose *absence* is hardest to work
around late.

— PA
