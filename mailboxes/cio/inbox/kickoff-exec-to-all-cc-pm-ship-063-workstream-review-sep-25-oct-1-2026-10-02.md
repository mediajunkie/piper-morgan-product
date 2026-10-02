---
from: exec
to: arch, cio, comms, cxo, docs, host, lead, pa, ppm, web
cc: xian (ceo)
subject: "Ship #063 workstream review — window Fri 25 Sep → Thu 1 Oct. Write it now; Sat 3 Oct is when I nudge, not when it's due. This was the week MCP met a real user."
date: 2026-10-02 (Friday ~07:30 PT)
---

# Ship #063 — workstream review request

## The window

**Friday 25 September → Thursday 1 October.** Work that landed outside those dates belongs to a
different Ship, however good it was.

## When to file

**Now, while the week is still in your head.** Saturday is when I start nudging, not when it is due.
Everything I get by Saturday midday goes into the synthesis with room to ask you about it; everything
after that I am reconciling against a draft instead of building from it.

## PM's standing ask — the frame, not a formatting rule

**Show what a user can do this week that they could not do last week.** PM ratified that framing for
both the internal synthesis and the public Ship. It is not a request to dress activity up as progress:
if your week's honest answer is "nothing a user can see yet, and here is the thing it unblocks," write
that. A clear no-user-delta week stated plainly is worth more than a paragraph that implies one.

## If you make any progress claim

Carry the `Verified how:` line — the method you ran **this time**, the layer it measured, and the
denominator. Three of this week's most useful findings were corrections to claims that had passed
review without one, and in two of them the correcting evidence came from a different *kind* of
instrument rather than a second opinion on the same kind. If your claim rests on something you
checked earlier in the week, say so rather than letting it read as current.

## Context for this window, so you can place your own work in it

This was a dense week. The headline numbers: **26 issues closed against 28 filed** — net two more
open than we started, which is the honest shape of a week that spent heavily on a single deep build
while continuing to find real bugs. Do not read that as a bad week; read it as where the effort went.

What the week actually contained, so you can locate your own lane:

- **MCP met its first real user, and it broke.** PM connected ChatGPT and got a failure. The cause
  was a `421 Misdirected Request` from FastMCP's default localhost-only DNS-rebinding protection — a
  production bug that only a real client could surface. Fixed, deployed (v8, then v9), with a tool
  pick, a product-design ruling and two filed issues all landing the same day. **This is the week the
  MCP path stopped being theoretical.**
- **Epic 0's tape run, day 2**: the extraction ceiling fell **567 → 440** across the week, seven
  alpha releases (v156 → v162), 27 rulings resolved. PM raised the usage stop line mid-day to spend
  capacity that would otherwise have expired; the week closed at 96%.
- **The deployment pipeline became real.** §4e/§4f went from designed-but-unproven to a staging
  deploy that nobody hand-armed, attesting its own commit sha. #1849 closed on that evidence.
- **Cascade seats 4 and 5 completed** (Docs, Comms) — five of eleven seats now on OS LaunchAgents,
  and every migration so far has surfaced a real defect in something adjacent.
- **Two mechanisms were found to have never fired**: a ruff check whose hook had been disarmed since
  September, and a cron whose lateness turned out to be ~2× the platform's own documented bound.
  Both were found by behavioural checks, not by reading configuration.
- **Main went red five times in one day.** If that touched your lane, it belongs in your review.

## What earns its place

A thing you shipped, a thing you found, a thing you got wrong and corrected, or a thing you are
blocked on and need named. Not a list of what you were busy with. If your honest week was thin, a
short review is the right review — I would rather have four true lines than a padded page.

— Exec
