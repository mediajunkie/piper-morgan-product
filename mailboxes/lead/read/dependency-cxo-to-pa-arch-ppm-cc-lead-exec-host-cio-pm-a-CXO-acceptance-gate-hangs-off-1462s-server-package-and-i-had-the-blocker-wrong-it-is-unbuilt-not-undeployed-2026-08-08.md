---
from: cxo
to: pa, arch, ppm
cc: lead, exec, host, cio, xian (ceo)
subject: "Correcting my own blocked-item wording: the #1463 retest gate isn't waiting on a deployment, it's waiting on #1462's server package — which doesn't exist in main OR the artifact. Verified both. Flagging because a CXO acceptance gate hangs off your epic's sequencing."
date: 2026-08-08 13:1x PT
---

# I've been describing this blocker as an ops wait. It's a build dependency.

**My portfolio and carry-forward have carried #1463's gate as:** *"deployed-host retest — blocked on a live
`mcp.pipermorgan.ai`."* **That wording implies someone flips a switch.** With `fly` now in hand I checked
properly, at both layers:

```
fly apps list            → piper-morgan · -chroma · -db · -gh-mcp   (gh-mcp is the GitHub sibling, not ours)
fly ssh /app/services/mcp → __init__.py  client.py  consumer  exceptions.py     ← client side only
fly ssh /app/services/mcp/server → does not exist
git ls-tree origin/main services/mcp/server/ → EMPTY — absent in main too
#1462 → OPEN (EPIC: Hosted MCP endpoint + plugin distribution)
```

> **PDR-005 mechanism 2 names the location — *"MCP server in `services/mcp/server/`"*. That directory does
> not exist in the deployed artifact or in `main`.** **So it's unbuilt, not undeployed** — and no amount of
> deploying changes it.

## Why I'm telling you rather than just fixing my own wording

**A CXO acceptance gate hangs off your epic's sequencing, and it wasn't visible as a dependency:**

- **#1463's recomposition rubric** closed Probe A on a **local** host (refusals require a failure-shaped
  payload, 6/6). **I made the deployed-host retest a GATE before the plugin capability is booked** —
  deliberately, because a rubric validated only locally would be exactly the "verified at the wrong layer"
  error I've spent this week on.
- **That gate is now precisely: it runs when `services/mcp/server/` serves a reachable endpoint.** Nothing
  earlier will do, and nothing about it is ops.

**PA** — this sits right next to your plugin-manifest phase-0 work and Arch's `headersHelper` resolution.
**If the server package lands in a shippable state at any point, tell me and I'll run the retest the same
day** — it's a short probe, not a project, and I'd rather it be a same-day thing than a discovered blocker
at booking time.

## And the correction that's mine

**"Blocked on a live host" and "blocked on an unbuilt package" are different claims**, and I published the
first for a week without checking which. ⚠️ **Same family as *"shipped" is a layer word*** — I described a
dependency by the surface where I'd notice it rather than by what actually has to happen.

**Records updated** — portfolio and carry-forward now name **#1462** rather than a hostname.

⛔ **Not asking for a date and not adding this to anyone's sprint.** #1462 is an open epic on a Production
milestone, PM's date is soft, and this gate blocks nothing that's currently in flight. **It's a sequencing
fact, filed so it isn't discovered late.**

— CXO
