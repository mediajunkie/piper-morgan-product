---
from: pa
to: xian (ceo)
cc: exec
subject: "BYOC hosted-alpha assessment, as promised — the honest gap is bigger than a redirect of focus, and here's what I can actually drive first"
in-reply-to: reply-pa-to-pm-cc-exec-janus-whats-actually-been-sitting-and-the-byoc-focus-is-the-right-call-2026-09-12.md
date: 2026-09-12
---

PM — the assessment I said I'd bring back after reading `ESSENCE.md` fresh and checking PDR-006
against current state, this fire rather than deferred.

## What I found, checked rather than assumed

**Nothing of the hosted MCP server exists yet.** `mcp.pipermorgan.ai` is not deployed — DNS/TLS
hasn't been stood up, and per PDR-006's own text, that deployment is upstream of everything else on
this path (directory listings, tool catalog testing, all of it). This isn't a "mostly built, needs
polish" situation; it's a build that hasn't started.

**The MCP-path work is currently sequenced to start once MVP closes, not now.** ESSENCE.md's own
ratified law (the milestone reconciliation I found and corrected in my carry-forward on 09-08): MCP
work sits at the FRONT of the Production milestone, and MCP-path completion is the public-beta gate —
but it comes *after* MVP closure, which is still 45 issues out per this morning's `sprint-truth.py`.
It's not in the current MVP epic order at all (checked `dev/active/mvp-epic-order-2026-09-09.md`
directly — no mention). So "get it into hosted alpha, on track to converge in beta" either means
overriding that sequencing to start now, in parallel with the MVP tail, or it means the real work
begins once MVP closes and what's needed today is the readiness plan, not the build itself.

**Two concrete, unstarted blockers, not just planning gaps:**
- **#1458** (cross-caller state isolation) — open, unstarted. Redis, in-process floor/context state,
  and rate-limiting under anonymous callers were never traced. This blocks any real multi-tenant
  hosted testing, not just a nice-to-have.
- **The cold-start demonstration criterion currently fails** — PDR-006's own success criteria say
  this is the only one that fails today, and it's flagged as the single load-bearing product claim
  across both surfaces (same wording as the #1386 beta gate).
- **ChatGPT's honest-decline capability sits at ~50% vs. 100% on Claude** — my own N=6 probe from
  July, still the current number. Tracked as an AC on #1462, wording held pending an untested
  protocol-level-error mechanism.

**What IS actually done, and it's real**: the recomposition-rubric design work — the honesty-under-
recomposition gate PDR-006 identifies as the differentiator this whole model depends on. That's
mine, it's substantially further along than anything else on this path (v0.6, both vendors tested,
a working mechanism found), and it's the one piece of "hosted alpha readiness" that doesn't wait on
deployment to make progress.

**Also found and fixed while checking**: PDR-006 itself had a stale citation of the rubric's own
status (said v0.4/one vendor pair; actual is v0.6/both vendors) — corrected in place, same fire.

## What I'd actually drive first, given this

Not overpromising fast convergence — the two real blockers (#1458, the deployment itself) are Lead's
and Arch's build, not mine to make happen alone. What I can own and drive without waiting on anyone:

1. **A hosted-alpha readiness checklist/spec** — the concrete, current list of what has to be true
   before the first real tester touches `mcp.pipermorgan.ai` (deployment, #1458 closed, tool catalog
   built and naming-tested per PPM's open question on situation-shaped vs. object-shaped names, the
   cold-start demonstration passing). Something Lead can execute against without re-deriving it from
   scattered PDR sections, mirroring what PPM just did for the MVP epic order.
2. **Keep pushing the recomposition-rubric work** — it's the one place I can make real progress
   independent of the deployment timeline, and it directly serves commitment 7's gate.
3. **Surface the sequencing question to you directly, since it's yours to call**: does "focus on
   BYOC now" mean override the ratified MVP-first sequencing, or does it mean have the readiness
   plan and design work done so the build starts the moment MVP closes? I don't think I should guess
   which you meant.

Building item 1 next unless you'd rather redirect first.

**Verified how**: read `ESSENCE.md` and `PDR-006` in full this fire; `gh issue view` on #1458/#1463
for live state; `sprint-truth.py`'s output from this morning's Ship #060 report for the MVP
denominator; grepped `dev/active/mvp-epic-order-2026-09-09.md` for MCP-path presence. Layer measured:
current repo state and GitHub issue state, not a status report from anyone else.

— PA
